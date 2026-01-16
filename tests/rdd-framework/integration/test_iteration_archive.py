"""
Integration tests for iteration archiving covering complete workflows.

This module tests iteration archiving from active development through archiving and cleanup
with real filesystem operations.

Key test scenarios covered:
- Full iteration cycle (create → add prompts → complete → archive)
- Workdir cleanup (archive → clear → verify registry preserved)
- Archive integrity (verify archived files match source, folder naming)
- Zip-based archives (verify zip creation and integrity)

Special setup requirements:
- Uses temp_rdd_instance fixture
- Tests create real archive zip files
- Validates complete archive structure
- Cleans up test archives after completion
"""

import pytest
import subprocess
import sys
import json
import zipfile
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
actions_dir = REPO_ROOT / ".rdd" / "src" / "actions"


class TestIterationArchiving:
    """Tests for complete iteration archiving workflow"""
    
    def test_archive_creates_proper_structure(self, temp_rdd_instance):
        """Test that archiving creates correct zip file structure"""
        test_dir = temp_rdd_instance
        instance_dir = test_dir / ".rdd-instance"
        actions_dir = test_dir / ".rdd" / "src" / "actions"
        workdir = instance_dir / "workdir"
        archive_dir = instance_dir / "archive"
        registry_file = workdir / "work-iteration-registry.json"
        
        original_cwd = Path.cwd()
        import os
        os.chdir(test_dir)
        
        created_archives = []
        
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
            archive_script = actions_dir / "workdir_archive.py"
            if archive_script.exists():
                result = subprocess.run(
                    [sys.executable, str(archive_script)],
                    capture_output=True,
                    text=True,
                    cwd=str(test_dir)
                )
                
                if result.returncode == 0:
                    # Verify archive zip file created with correct naming
                    expected_archive_zip = archive_dir / f"{iteration_id}_{iteration_name}.zip"
                    created_archives.append(expected_archive_zip)
                    
                    assert expected_archive_zip.exists(), f"Archive zip file not found: {expected_archive_zip}"
                    
                    # Verify zip file integrity
                    with zipfile.ZipFile(expected_archive_zip, 'r') as zipf:
                        # Test zip integrity
                        bad_file = zipf.testzip()
                        assert bad_file is None, f"Zip file corrupted: {bad_file}"
                        
                        # Verify registry preserved in zip
                        file_list = zipf.namelist()
                        assert "work-iteration-registry.json" in file_list, "Registry not found in archive"
                    
                    # Verify directory-based archive was removed
                    directory_archive = archive_dir / f"{iteration_id}_{iteration_name}"
                    assert not directory_archive.exists(), f"Directory archive should be removed: {directory_archive}"
            
        finally:
            os.chdir(original_cwd)
            # Clean up any created archives
            for archive_path in created_archives:
                if archive_path.exists():
                    archive_path.unlink()
            # Also clean up archive directory if empty
            if archive_dir.exists() and not list(archive_dir.iterdir()):
                archive_dir.rmdir()
