"""
test_rdd_main.py
Unit tests for rdd.py main entry point
Tests command routing and CLI interface
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, call
from io import StringIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".rdd" / "scripts"))

import rdd


class TestCLIHelp:
    """Test CLI help and version commands"""
    
    @patch('sys.argv', ['rdd.py', '--version'])
    @patch('rdd.get_framework_version', return_value='1.0.0')
    def test_version_command(self, mock_version, capsys):
        with pytest.raises(SystemExit) as exc_info:
            rdd.main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "RDD Framework" in captured.out or "1.0.0" in captured.out
    
    @patch('sys.argv', ['rdd.py', '--help'])
    def test_help_command(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            rdd.main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Usage:" in captured.out
        assert "domains:" in captured.out.lower()


class TestDomainRouting:
    """Test domain-based command routing"""
    
    @patch('sys.argv', ['rdd.py', 'config', 'show'])
    @patch('rdd.route_config')
    def test_config_show_routing(self, mock_route_config):
        mock_route_config.return_value = 0
        # main() returns the value from route_config, it doesn't sys.exit directly
        result = rdd.main()
        assert result == 0
        mock_route_config.assert_called_once()
    
    @patch('sys.argv', ['rdd.py', 'workspace', 'init'])
    @patch('rdd.route_workspace')
    def test_workspace_init_routing(self, mock_route_workspace):
        mock_route_workspace.return_value = 0
        result = rdd.main()
        assert result == 0
        mock_route_workspace.assert_called_once()


class TestChangeCommands:
    """Test change management commands"""
    
    @patch('sys.argv', ['rdd.py', 'change', 'create'])
    @patch('rdd_utils.get_repo_root', return_value='/fake/repo')
    @patch('rdd_utils.get_current_branch', return_value='feature-branch')
    @patch('rdd_utils.get_default_branch', return_value='main')
    def test_change_create_requires_default_branch(self, mock_default_branch, mock_current_branch, mock_repo_root):
        # Should return 1 when not on default branch (no sys.exit in this path)
        result = rdd.main()
        assert result == 1


class TestMenuInteraction:
    """Test interactive menu functionality"""
    
    @patch('curses.wrapper')
    def test_curses_menu_selection(self, mock_wrapper):
        # Mock curses menu to return first option (index 0 = fix)
        mock_wrapper.return_value = 0
        
        result = rdd.select_change_type_interactive()
        # Index 0 should return "fix"
        assert result == "fix"


class TestValidationCommands:
    """Test validation and checks"""
    
    @patch('sys.argv', ['rdd.py', 'invalid-domain'])
    def test_check_repo_valid(self, capsys):
        # Invalid domain should exit with code 1
        with pytest.raises(SystemExit) as exc_info:
            rdd.main()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Unknown domain" in captured.err


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    @patch('sys.argv', ['rdd.py'])
    def test_no_command_shows_help(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            rdd.main()
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Usage:" in captured.out
    
    @patch('sys.argv', ['rdd.py', 'invalid_domain'])
    def test_invalid_domain_error(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            rdd.main()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Unknown domain" in captured.err
    
    @patch('sys.argv', ['rdd.py', 'change', 'invalid_action'])
    def test_invalid_action_error(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            rdd.main()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Unknown" in captured.err or "action" in captured.err
