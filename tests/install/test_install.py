"""
test_install.py
Tests for install.py script
"""

import pytest
import sys
import os
import json
from pathlib import Path
from unittest.mock import patch, Mock

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

import install


class TestPreFlightChecks:
    """Test pre-flight checks"""
    
    def test_check_python_version_success(self):
        """Test Python version check succeeds for 3.7+"""
        # Should not raise error
        install.check_python_version()
    
    @patch('subprocess.run')
    def test_check_git_installed_success(self, mock_run):
        """Test Git installation check succeeds"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="git version 2.30.0"
        )
        assert install.check_git_installed() == True
    
    @patch('subprocess.run')
    def test_check_git_installed_failure(self, mock_run):
        """Test Git installation check fails gracefully"""
        mock_run.side_effect = FileNotFoundError()
        with pytest.raises(SystemExit):
            install.check_git_installed()
    
    def test_check_git_repo_valid(self, mock_git_repo_for_install):
        """Test Git repository check succeeds"""
        assert install.check_git_repo(mock_git_repo_for_install) == True
    
    def test_check_git_repo_invalid(self, temp_install_dir):
        """Test Git repository check fails for non-git directory"""
        with pytest.raises(SystemExit):
            install.check_git_repo(temp_install_dir)


class TestExistingInstallationDetection:
    """Test detection of existing RDD installation"""
    
    def test_detect_existing_installation_none(self, mock_git_repo_for_install):
        """Test no existing installation detected"""
        assert install.detect_existing_installation(mock_git_repo_for_install) == False
    
    def test_detect_existing_installation_found(self, mock_git_repo_for_install):
        """Test existing installation detected"""
        # Create RDD structure
        rdd_dir = mock_git_repo_for_install / ".rdd"
        rdd_dir.mkdir()
        (rdd_dir / "scripts").mkdir()
        (rdd_dir / "scripts" / "rdd.py").write_text("# RDD")
        
        assert install.detect_existing_installation(mock_git_repo_for_install) == True


class TestFileOperations:
    """Test file copying and operations"""
    
    def test_copy_prompts(self, mock_rdd_archive, mock_git_repo_for_install):
        """Test copying prompt files"""
        install.copy_prompts(mock_rdd_archive, mock_git_repo_for_install)
        
        prompts_dir = mock_git_repo_for_install / ".github" / "prompts"
        assert prompts_dir.exists()
        assert (prompts_dir / "test.prompt.md").exists()
    
    def test_copy_framework(self, mock_rdd_archive, mock_git_repo_for_install):
        """Test copying framework files"""
        install.copy_rdd_framework(mock_rdd_archive, mock_git_repo_for_install)
        
        rdd_dir = mock_git_repo_for_install / ".rdd"
        assert rdd_dir.exists()
        assert (rdd_dir / "scripts" / "rdd.py").exists()
        assert (rdd_dir / "scripts" / "rdd_utils.py").exists()
        assert (rdd_dir / "templates" / "test.md").exists()
        # Verify user-guide.md is copied (P01 change)
        assert (rdd_dir / "user-guide.md").exists()
    
    def test_copy_seed_templates(self, mock_rdd_archive, mock_git_repo_for_install):
        """Test copying seed templates to .rdd-docs"""
        install.copy_rdd_docs_seeds(mock_rdd_archive, mock_git_repo_for_install)
        
        rdd_docs = mock_git_repo_for_install / ".rdd-docs"
        assert rdd_docs.exists()
        assert (rdd_docs / "config.json").exists()
        assert (rdd_docs / "requirements.md").exists()
        assert (rdd_docs / "tech-spec.md").exists()


class TestLauncherScriptInstallation:
    """Test launcher script installation based on OS"""
    
    @patch('os.name', 'nt')
    def test_install_launcher_windows(self, mock_rdd_archive, mock_git_repo_for_install):
        """Test installing rdd.bat on Windows"""
        install.install_launcher_script(mock_rdd_archive, mock_git_repo_for_install)
        
        launcher = mock_git_repo_for_install / "rdd.bat"
        assert launcher.exists()
        
        content = launcher.read_text()
        assert "@echo off" in content
        assert ".rdd\\scripts\\rdd.py" in content
    
    @patch('os.name', 'posix')
    def test_install_launcher_linux(self, mock_rdd_archive, mock_git_repo_for_install):
        """Test installing rdd.sh on Linux/macOS"""
        install.install_launcher_script(mock_rdd_archive, mock_git_repo_for_install)
        
        launcher = mock_git_repo_for_install / "rdd.sh"
        assert launcher.exists()
        
        content = launcher.read_text()
        assert "#!/bin/bash" in content
        assert ".rdd/scripts/rdd.py" in content
    
    @pytest.mark.skipif(os.name == "nt", reason="Unix-only permission test")
    @patch('os.name', 'posix')
    def test_launcher_executable_permissions_unix(self, mock_rdd_archive, mock_git_repo_for_install):
        """Test that rdd.sh gets executable permissions on Unix"""
        install.install_launcher_script(mock_rdd_archive, mock_git_repo_for_install)
        
        launcher = mock_git_repo_for_install / "rdd.sh"
        
        # Check that file is executable (at least user execute bit)
        import stat
        mode = launcher.stat().st_mode
        assert mode & stat.S_IXUSR  # User execute bit should be set


class TestSettingsMerge:
    """Test VS Code settings merge logic"""
    
    def test_merge_settings_empty_target(self, mock_git_repo_for_install):
        """Test merging into empty settings file"""
        rdd_settings = {
            "chat.promptFilesRecommendations": ["test.md"],
            "editor.rulers": [80, 120]
        }
        
        target_settings_file = mock_git_repo_for_install / ".vscode" / "settings.json"
        target_settings_file.parent.mkdir(parents=True, exist_ok=True)
        target_settings_file.write_text("{}")
        
        merged = install.merge_settings(rdd_settings, {})
        
        assert "chat.promptFilesRecommendations" in merged
        assert "editor.rulers" in merged
        assert merged["editor.rulers"] == [80, 120]
    
    def test_merge_settings_existing_values(self):
        """Test merging with existing settings"""
        rdd_settings = {
            "chat.promptFilesRecommendations": ["new.md"],
            "editor.rulers": [80, 120]
        }
        
        existing_settings = {
            "chat.promptFilesRecommendations": ["existing.md"],
            "editor.rulers": [100]
        }
        
        merged = install.merge_settings(rdd_settings, existing_settings)
        
        # Array settings should be merged
        assert "existing.md" in merged["chat.promptFilesRecommendations"]
        assert "new.md" in merged["chat.promptFilesRecommendations"]
        
        # Editor settings should be replaced
        assert merged["editor.rulers"] == [80, 120]
    
    def test_merge_settings_object_merge(self):
        """Test merging object-type settings"""
        rdd_settings = {
            "files.associations": {
                "*.jsonl": "jsonlines"
            }
        }
        
        existing_settings = {
            "files.associations": {
                "*.custom": "custom-language"
            }
        }
        
        merged = install.merge_settings(rdd_settings, existing_settings)
        
        # Both associations should be present
        assert merged["files.associations"]["*.jsonl"] == "jsonlines"
        assert merged["files.associations"]["*.custom"] == "custom-language"


class TestGitignoreUpdate:
    """Test .gitignore update logic"""
    
    def test_update_gitignore_new_file(self, mock_git_repo_for_install):
        """Test creating new .gitignore"""
        install.update_gitignore(mock_git_repo_for_install)
        
        gitignore = mock_git_repo_for_install / ".gitignore"
        assert gitignore.exists()
        
        content = gitignore.read_text()
        assert ".rdd-docs/workspace/" in content
    
    def test_update_gitignore_existing_file(self, mock_git_repo_for_install):
        """Test updating existing .gitignore"""
        gitignore = mock_git_repo_for_install / ".gitignore"
        gitignore.write_text("# Existing rules\n*.log\n")
        
        install.update_gitignore(mock_git_repo_for_install)
        
        content = gitignore.read_text()
        assert "*.log" in content  # Preserved existing
        assert ".rdd-docs/workspace/" in content  # Added new
    
    def test_update_gitignore_already_present(self, mock_git_repo_for_install):
        """Test .gitignore when workspace rule already exists"""
        gitignore = mock_git_repo_for_install / ".gitignore"
        gitignore.write_text(".rdd-docs/workspace/\n")
        
        install.update_gitignore(mock_git_repo_for_install)
        
        content = gitignore.read_text()
        # Should not duplicate
        assert content.count(".rdd-docs/workspace/") == 1


class TestVerification:
    """Test post-installation verification"""
    
    def test_verify_installation_success(self, mock_git_repo_for_install, mock_rdd_archive):
        """Test verification succeeds for complete installation"""
        # Install all components
        install.copy_rdd_framework(mock_rdd_archive, mock_git_repo_for_install)
        install.copy_prompts(mock_rdd_archive, mock_git_repo_for_install)
        
        # Verify should pass
        assert install.verify_installation(mock_git_repo_for_install) == True
    
    def test_verify_installation_missing_files(self, mock_git_repo_for_install):
        """Test verification fails for incomplete installation"""
        # Don't install anything
        assert install.verify_installation(mock_git_repo_for_install) == False


class TestOutputFunctions:
    """Test installer output functions"""
    
    def test_print_banner(self, capsys):
        install.print_banner()
        captured = capsys.readouterr()
        assert "RDD Framework Installer" in captured.out
    
    def test_print_success(self, capsys):
        install.print_success("Test message")
        captured = capsys.readouterr()
        assert "Test message" in captured.out
        assert "✓" in captured.out
    
    def test_print_error(self, capsys):
        install.print_error("Error message")
        captured = capsys.readouterr()
        assert "Error message" in captured.err
        assert "✗" in captured.err
