"""
test_rdd_utils.py
Unit tests for rdd_utils.py
Tests utility functions in isolation
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# Add parent directory to path to import rdd_utils
sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".rdd" / "scripts"))

import rdd_utils


class TestOutputFunctions:
    """Test color output functions"""
    
    def test_print_success(self, capsys):
        rdd_utils.print_success("Test message")
        captured = capsys.readouterr()
        assert "Test message" in captured.out
        assert "✓" in captured.out
    
    def test_print_error(self, capsys):
        rdd_utils.print_error("Error message")
        captured = capsys.readouterr()
        assert "Error message" in captured.err
        assert "✗" in captured.err
    
    def test_print_warning(self, capsys):
        rdd_utils.print_warning("Warning message")
        captured = capsys.readouterr()
        assert "Warning message" in captured.out
        assert "⚠" in captured.out
    
    def test_print_info(self, capsys):
        rdd_utils.print_info("Info message")
        captured = capsys.readouterr()
        assert "Info message" in captured.out
        assert "ℹ" in captured.out


class TestValidationFunctions:
    """Test validation utility functions"""
    
    def test_validate_name_valid(self):
        assert rdd_utils.validate_name("valid-name-123") == True
    
    def test_validate_name_with_spaces(self):
        assert rdd_utils.validate_name("invalid name") == False
    
    def test_validate_name_with_special_chars(self):
        assert rdd_utils.validate_name("invalid@name") == False
    
    def test_validate_name_empty(self):
        assert rdd_utils.validate_name("") == False
    
    def test_normalize_to_kebab_case(self):
        assert rdd_utils.normalize_to_kebab_case("Test Name 123") == "test-name-123"
        assert rdd_utils.normalize_to_kebab_case("CamelCase") == "camelcase"
        assert rdd_utils.normalize_to_kebab_case("with_underscores") == "with-underscores"
        assert rdd_utils.normalize_to_kebab_case("UPPER CASE") == "upper-case"
    
    def test_validate_file_exists(self, temp_dir):
        test_file = temp_dir / "test.txt"
        test_file.write_text("test")
        assert rdd_utils.validate_file_exists(str(test_file)) == True
        assert rdd_utils.validate_file_exists(str(temp_dir / "nonexistent.txt")) == False
    
    def test_validate_dir_exists(self, temp_dir):
        assert rdd_utils.validate_dir_exists(str(temp_dir)) == True
        assert rdd_utils.validate_dir_exists(str(temp_dir / "nonexistent")) == False


class TestGitFunctions:
    """Test git-related utility functions"""
    
    @patch('subprocess.run')
    def test_check_git_repo_valid(self, mock_run, temp_dir):
        (temp_dir / ".git").mkdir()
        mock_run.return_value = Mock(returncode=0)
        assert rdd_utils.check_git_repo(str(temp_dir)) == True
    
    @patch('subprocess.run')
    def test_check_git_repo_invalid(self, mock_run, temp_dir):
        mock_run.return_value = Mock(returncode=1)
        assert rdd_utils.check_git_repo(str(temp_dir), exit_on_error=False) == False
    
    @patch('subprocess.run')
    def test_get_current_branch(self, mock_run):
        mock_run.return_value = Mock(
            returncode=0,
            stdout="main\n"
        )
        assert rdd_utils.get_current_branch() == "main"
    
    @patch('subprocess.run')
    def test_get_default_branch_from_config(self, mock_run, rdd_workspace):
        os.chdir(rdd_workspace)
        # Config has defaultBranch: "main"
        assert rdd_utils.get_default_branch() == "main"
    
    @patch('subprocess.run')
    def test_get_branch_type_fix(self, mock_run):
        mock_run.return_value = Mock(returncode=0, stdout="fix/test-bug\n")
        assert rdd_utils.get_branch_type() == "fix"
    
    @patch('subprocess.run')
    def test_get_branch_type_enh(self, mock_run):
        mock_run.return_value = Mock(returncode=0, stdout="enh/new-feature\n")
        assert rdd_utils.get_branch_type() == "enh"
    
    @patch('subprocess.run')
    def test_get_branch_type_main(self, mock_run):
        mock_run.return_value = Mock(returncode=0, stdout="main\n")
        # main branch should return empty string, not "main"
        assert rdd_utils.get_branch_type() == ""
    
    @patch('subprocess.run')
    def test_is_enh_or_fix_branch(self, mock_run):
        mock_run.return_value = Mock(returncode=0, stdout="fix/test\n")
        assert rdd_utils.is_enh_or_fix_branch() == True
        
        mock_run.return_value = Mock(returncode=0, stdout="main\n")
        assert rdd_utils.is_enh_or_fix_branch() == False


class TestTimestampFunctions:
    """Test timestamp utility functions"""
    
    def test_get_timestamp_format(self):
        timestamp = rdd_utils.get_timestamp()
        # Check format: YYYY-MM-DDTHH:MM:SSZ
        assert len(timestamp) == 20
        assert timestamp[10] == "T"
        assert timestamp[-1] == "Z"
    
    def test_get_timestamp_filename_format(self):
        timestamp = rdd_utils.get_timestamp_filename()
        # Check format: YYYYMMDD-HHMM
        assert len(timestamp) == 13
        assert timestamp[8] == "-"


class TestConfigFunctions:
    """Test configuration management functions"""
    
    def test_get_rdd_config_existing_key(self, rdd_workspace):
        os.chdir(rdd_workspace)
        version = rdd_utils.get_rdd_config("version")
        assert version == "1.0.0"
    
    def test_get_rdd_config_missing_key_with_default(self, rdd_workspace):
        os.chdir(rdd_workspace)
        value = rdd_utils.get_rdd_config("nonexistent", default="default_value")
        assert value == "default_value"
    
    def test_set_rdd_config(self, rdd_workspace):
        os.chdir(rdd_workspace)
        rdd_utils.set_rdd_config("testKey", "testValue")
        
        # Read config and verify
        config_path = rdd_workspace / ".rdd-docs" / "config.json"
        with open(config_path) as f:
            config = json.load(f)
        assert config["testKey"] == "testValue"
        assert "lastModified" in config
    
    def test_get_rdd_config_path(self, rdd_workspace):
        os.chdir(rdd_workspace)
        config_path = rdd_utils.get_rdd_config_path()
        expected = rdd_workspace / ".rdd-docs" / "config.json"
        assert Path(config_path) == expected


class TestWorkspaceUtilities:
    """Test workspace management utilities"""
    
    def test_ensure_dir_creates_directory(self, temp_dir):
        test_dir = temp_dir / "new_dir" / "nested"
        rdd_utils.ensure_dir(str(test_dir))
        assert test_dir.exists()
        assert test_dir.is_dir()
    
    def test_ensure_dir_existing_directory(self, temp_dir):
        # Should not raise error
        rdd_utils.ensure_dir(str(temp_dir))
        assert temp_dir.exists()


class TestPromptFunctions:
    """Test prompt management functions"""
    
    def test_mark_prompt_completed(self, rdd_workspace):
        os.chdir(rdd_workspace)
        
        # Create prompts file with unchecked prompt
        prompts_file = rdd_workspace / ".rdd-docs" / "workspace" / ".rdd.copilot-prompts.md"
        prompts_file.write_text("""## Stand Alone Prompts

 - [ ] [P01] Test prompt description
 - [ ] [P02] Another prompt
""")
        
        # Mark P01 as completed
        rdd_utils.mark_prompt_completed("P01")
        
        # Read and verify
        content = prompts_file.read_text()
        assert "- [x] [P01]" in content
        assert "- [ ] [P02]" in content


class TestConfirmAction:
    """Test user confirmation function"""
    
    @patch('builtins.input', return_value='y')
    def test_confirm_action_yes(self, mock_input):
        assert rdd_utils.confirm_action("Test question") == True
    
    @patch('builtins.input', return_value='n')
    def test_confirm_action_no(self, mock_input):
        assert rdd_utils.confirm_action("Test question") == False
    
    @patch('builtins.input', return_value='yes')
    def test_confirm_action_yes_full(self, mock_input):
        assert rdd_utils.confirm_action("Test question") == True
    
    @patch('builtins.input', return_value='invalid')
    def test_confirm_action_invalid(self, mock_input):
        # Should return False for invalid input
        assert rdd_utils.confirm_action("Test question") == False
