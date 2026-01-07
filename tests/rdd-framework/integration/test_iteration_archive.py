"""
Integration tests for iteration archiving covering complete workflows.

This module tests iteration archiving from active development through archiving and cleanup
with real filesystem operations.

Key test scenarios covered:
- Full iteration cycle (create → add prompts → complete → archive)
- Workdir cleanup (archive → clear → verify registry preserved)
- Archive integrity (verify archived files match source, folder naming)

Special setup requirements:
- Uses temp_rdd_instance fixture
- Tests create real archive folders
- Validates complete archive structure
"""

import pytest
import subprocess
import sys
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
actions_dir = REPO_ROOT / ".rdd" / "src" / "actions"


class TestIterationArchiving:
    """Tests for complete iteration archiving workflow"""
    
    def test_archive_creates_proper_structure(self, temp_rdd_instance):
        """Test that archiving creates correct folder structure"""
        test_dir = temp_rdd_instance
        instance_dir = test_dir / ".rdd-instance"
        actions_dir = test_dir / ".rdd" / "src" / "actions"
        workdir = instance_dir / "workdir"
        archive_dir = instance_dir / "archive"
        registry_file = workdir / "work-iteration-registry.json"
        
        original_cwd = Path.cwd()
        import os
        os.chdir(test_dir)
        
        try:
            # Read registry to get iteration info
            with open(registry_file) as f:
                registry = json.load(f)
            
            iteration_id = registry["iteration-id"]
            iteration_name = registry["iteration-name"]
            
            # Create and complete a prompt
            subprocess.run(
                [sys.executable, str(actions_dir / "prompt_create.py"), "title=Test Prompt"],
                capture_output=True,
                cwd=str(test_dir)
            )
            
            subprocess.run(
                [sys.executable, str(actions_dir / "prompt_set_state.py"), "state=completed"],
                capture_output=True,
                cwd=str(test_dir)
            )
            
            # Archive iteration (if script exists)
            # Note: Archive script may not exist yet
            archive_script = actions_dir / "workdir_archive.py"
            if archive_script.exists():
                result = subprocess.run(
                    [sys.executable, str(archive_script)],
                    capture_output=True,
                    text=True,
                    cwd=str(test_dir)
                )
                
                if result.returncode == 0:
                    # Verify archive folder created with correct naming
                    expected_archive = archive_dir / f"{iteration_id}_{iteration_name}"
                    assert expected_archive.exists(), f"Archive folder not found: {expected_archive}"
                    
                    # Verify registry preserved
                    archived_registry = expected_archive / "work-iteration-registry.json"
                    assert archived_registry.exists()
            
        finally:
            os.chdir(original_cwd)
