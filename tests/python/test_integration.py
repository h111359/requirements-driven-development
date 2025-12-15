"""
test_integration.py
Integration tests for RDD workflow
Tests end-to-end scenarios
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch
import subprocess
import json

sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".rdd" / "scripts"))

import rdd_utils


@pytest.mark.integration
class TestChangeWorkflow:
    """Test complete change workflow"""
    
    def test_fix_branch_workflow(self, rdd_workdir):
        """Test creating a fix branch and initializing workdir"""
        os.chdir(rdd_workdir)
        
        # Create fix branch
        branch_name = "fix/test-bug"
        subprocess.run(["git", "checkout", "-b", branch_name], check=True, capture_output=True)
        
        # Initialize workdir
        workdir = rdd_workdir / ".rdd-instance" / "workdir"
        
        # Create config file
        config = {
            "type": "fix",
            "name": "test-bug",
            "branch": branch_name,
            "created": rdd_utils.get_timestamp(),
            "author": "test@example.com"
        }
        config_file = workdir / f".rdd.fix.{branch_name.replace('/', '-')}"
        config_file.write_text(json.dumps(config, indent=2))
        
        # Verify workdir initialized
        assert config_file.exists()
        assert workdir.exists()
        
        # Verify we can find the config
        found_config = rdd_utils.find_change_config()
        assert found_config is not None


@pytest.mark.integration
class TestRequirementsManagement:
    """Test requirements management workflow"""
    
    def test_requirements_changes_format(self, rdd_workdir, sample_requirements_changes):
        """Test requirements changes file format"""
        os.chdir(rdd_workdir)
        
        workdir = rdd_workdir / ".rdd-instance" / "workdir"
        changes_file = workdir / "requirements-changes.md"
        changes_file.write_text(sample_requirements_changes)
        
        # Read and validate format
        content = changes_file.read_text()
        assert "[ADDED]" in content
        assert "[MODIFIED]" in content
        assert "[DELETED]" in content


@pytest.mark.integration
class TestworkdirArchiving:
    """Test workdir archiving workflow"""
    
    def test_workdir_backup_creation(self, rdd_workdir):
        """Test creating workdir backup"""
        os.chdir(rdd_workdir)
        
        workdir = rdd_workdir / ".rdd-instance" / "workdir"
        backups_dir = workdir / ".backups"
        backups_dir.mkdir(parents=True, exist_ok=True)
        
        # Create some workdir files
        (workdir / "test-file.md").write_text("Test content")
        
        # Create backup
        timestamp = rdd_utils.get_timestamp_filename()
        backup_dir = backups_dir / timestamp
        backup_dir.mkdir(parents=True)
        
        # Copy workdir files
        import shutil
        for item in workdir.iterdir():
            if item.name != ".backups" and item.is_file():
                shutil.copy2(item, backup_dir / item.name)
        
        # Verify backup created
        assert backup_dir.exists()
        assert (backup_dir / "test-file.md").exists()


@pytest.mark.integration
@pytest.mark.requires_git
class TestGitIntegration:
    """Test git integration"""
    
    def test_branch_creation_and_switching(self, mock_git_repo):
        """Test creating and switching branches"""
        os.chdir(mock_git_repo)
        
        # Create new branch
        subprocess.run(["git", "checkout", "-b", "test-branch"], check=True, capture_output=True)
        
        # Verify current branch
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True
        )
        assert result.stdout.strip() == "test-branch"
    
    def test_uncommitted_changes_detection(self, mock_git_repo):
        """Test detecting uncommitted changes"""
        os.chdir(mock_git_repo)
        
        # Create a file
        test_file = mock_git_repo / "test.txt"
        test_file.write_text("test content")
        
        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        assert len(result.stdout.strip()) > 0


@pytest.mark.integration
class TestConfigManagement:
    """Test configuration management"""
    
    def test_config_read_write_cycle(self, rdd_workdir):
        """Test reading and writing configuration"""
        os.chdir(rdd_workdir)
        
        # Read initial value
        original_branch = rdd_utils.get_rdd_config("defaultBranch")
        assert original_branch == "main"
        
        # Update value
        rdd_utils.set_rdd_config("defaultBranch", "dev")
        
        # Read updated value
        updated_branch = rdd_utils.get_rdd_config("defaultBranch")
        assert updated_branch == "dev"
        
        # Restore original
        rdd_utils.set_rdd_config("defaultBranch", original_branch)
    
    def test_config_default_branch(self, rdd_workdir):
        """Test default branch configuration"""
        os.chdir(rdd_workdir)
        
        # Read default branch from config
        default_branch = rdd_utils.get_default_branch()
        assert default_branch == "main"  # From fixture config
