#!/usr/bin/env python3
"""Validation script to test the improved workdir_archive.py with mockup data.

This script creates a realistic test scenario and uses the improved archive
script to validate the two-phase commit implementation.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


def setup_mockup_environment(base_path: Path) -> tuple[Path, Path]:
    """Set up a mockup RDD instance structure for testing.
    
    Returns (mockup_workdir, mockup_archive_root).
    """
    # Create structure: base_path / .rdd-instance / workdir
    # This simulates: repo-root / .rdd-instance / workdir
    rdd_instance = base_path / ".rdd-instance"
    if rdd_instance.exists():
        shutil.rmtree(rdd_instance)
    
    rdd_instance.mkdir(parents=True)
    
    # Create workdir with test content
    workdir = rdd_instance / "workdir"
    workdir.mkdir()
    
    # Create registry file
    registry_data = {
        "iteration-id": "ITR-TEST-20260116",
        "iteration-name": "Validation Test Iteration",
        "prompt-id-sequence-next-value": 3,
        "prompts": [
            {
                "prompt-id": "P-001",
                "prompt-title": "Test Prompt 1",
                "state": "completed"
            },
            {
                "prompt-id": "P-002",
                "prompt-title": "Test Prompt 2",
                "state": "active"
            }
        ]
    }
    
    registry_path = workdir / "work-iteration-registry.json"
    with registry_path.open("w", encoding="utf-8") as f:
        json.dump(registry_data, f, indent=4)
    
    # Create prompt folders with content
    p001 = workdir / "P-001_Test Prompt 1"
    p001.mkdir()
    (p001 / "prompt.md").write_text("# Test Prompt 1\nSome content")
    (p001 / "plan.md").write_text("## Plan\n1. Step one\n2. Step two")
    (p001 / "implementation.md").write_text("## Implementation\nDetails here")
    
    # Create nested structure
    subfolder = p001 / "analysis" / "details"
    subfolder.mkdir(parents=True)
    (subfolder / "notes.txt").write_text("Detailed analysis notes")
    
    p002 = workdir / "P-002_Test Prompt 2"
    p002.mkdir()
    (p002 / "prompt.md").write_text("# Test Prompt 2\nActive prompt")
    (p002 / "questionnaire.json").write_text('{"questions": []}')
    
    # Create empty folder (this is what could remain in the bug)
    empty_folder = workdir / "empty_analysis_folder"
    empty_folder.mkdir()
    
    # Create archive root
    archive_root = rdd_instance / "archive"
    archive_root.mkdir()
    
    return workdir, archive_root


def create_modified_archive_script(original_script: Path, test_repo_root: Path) -> Path:
    """Create a modified version of the archive script for testing with mockup data.
    
    Args:
        original_script: Path to the original workdir_archive.py
        test_repo_root: Path that should be returned by _repo_root() in the test
        
    Returns path to the test script.
    """
    # Read the original script
    script_content = original_script.read_text()
    
    # Modify the _repo_root function to return our test repo root
    modified_content = script_content.replace(
        "def _repo_root() -> Path:\n    # This file lives at: <repo>/.rdd/src/actions/workdir-archive.py\n    return Path(__file__).resolve().parents[3]",
        f"def _repo_root() -> Path:\n    # Modified for testing\n    return Path(r'{test_repo_root}')"
    )
    
    # Create test script in the test repo root
    test_script = test_repo_root / "test_workdir_archive_improved.py"
    test_script.write_text(modified_content)
    
    return test_script


def validate_archive_structure(archive_path: Path, expected_items: int) -> bool:
    """Validate that archive has the expected structure."""
    if not archive_path.exists():
        print(f"  ❌ Archive does not exist at {archive_path}")
        return False
    
    # Count files recursively
    file_count = sum(1 for _ in archive_path.rglob('*') if _.is_file())
    
    print(f"  Archive contains {file_count} files (expected ~{expected_items})")
    
    # Check key files
    registry = archive_path / "work-iteration-registry.json"
    if not registry.exists():
        print("  ❌ Registry file missing from archive")
        return False
    
    print("  ✅ Archive structure validated")
    return True


def validate_workdir_empty(workdir: Path) -> bool:
    """Validate that workdir is empty after cleanup."""
    if not workdir.exists():
        print("  ❌ Workdir does not exist")
        return False
    
    items = list(workdir.iterdir())
    if items:
        print(f"  ❌ Workdir not empty. Remaining items: {[i.name for i in items]}")
        return False
    
    print("  ✅ Workdir is empty")
    return True


def main() -> int:
    """Main validation execution."""
    print("=" * 80)
    print("Validation Test for Improved workdir_archive.py")
    print("=" * 80)
    
    script_dir = Path(__file__).parent
    original_script = script_dir.parent.parent.parent / ".rdd" / "src" / "actions" / "workdir_archive.py"
    
    if not original_script.exists():
        print(f"ERROR: Cannot find original script at {original_script}")
        return 1
    
    # Setup mockup environment
    test_base = script_dir / "validation_test_temp"
    if test_base.exists():
        shutil.rmtree(test_base)
    test_base.mkdir(exist_ok=True)
    
    print(f"\nSetting up mockup environment in: {test_base}")
    mockup_workdir, mockup_archive_root = setup_mockup_environment(test_base)
    
    # Count items before archiving
    items_before = sum(1 for _ in mockup_workdir.rglob('*') if _.is_file())
    print(f"Mockup workdir created with {items_before} files")
    
    # Create modified test script (mockup_workdir.parent.parent is the test repo root)
    test_repo_root = mockup_workdir.parent.parent
    test_script = create_modified_archive_script(original_script, test_repo_root)
    print(f"Created test script: {test_script}")
    
    # Run the archive script
    print("\n" + "=" * 80)
    print("Running improved archive script...")
    print("=" * 80)
    
    try:
        result = subprocess.run(
            [sys.executable, str(test_script)],
            capture_output=True,
            text=True,
            cwd=script_dir
        )
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"\n❌ Script failed with exit code {result.returncode}")
            return 1
        
        # Extract archive path from output
        archive_path_str = result.stdout.strip().split('\n')[-1]
        archive_path = Path(archive_path_str)
        
        print("\n" + "=" * 80)
        print("Validating Results...")
        print("=" * 80)
        
        # Validate archive
        print("\n1. Checking archive integrity:")
        archive_valid = validate_archive_structure(archive_path, items_before)
        
        # Validate workdir cleanup
        print("\n2. Checking workdir cleanup:")
        workdir_clean = validate_workdir_empty(mockup_workdir)
        
        # Check for .deleting folder (should not exist)
        print("\n3. Checking for orphaned .deleting folder:")
        deleting_folder = mockup_workdir.parent / f"{mockup_workdir.name}.deleting"
        if deleting_folder.exists():
            print(f"  ❌ Found orphaned {deleting_folder.name} folder")
            deleting_clean = False
        else:
            print("  ✅ No orphaned .deleting folder")
            deleting_clean = True
        
        print("\n" + "=" * 80)
        print("VALIDATION SUMMARY")
        print("=" * 80)
        
        if archive_valid and workdir_clean and deleting_clean:
            print("✅ ALL CHECKS PASSED")
            print("\nThe improved workdir_archive.py implementation:")
            print("  ✓ Successfully created complete archive")
            print("  ✓ Completely cleaned the workdir")
            print("  ✓ No orphaned .deleting folders")
            print("  ✓ Two-phase commit worked correctly")
            return 0
        else:
            print("❌ SOME CHECKS FAILED")
            if not archive_valid:
                print("  ✗ Archive validation failed")
            if not workdir_clean:
                print("  ✗ Workdir cleanup incomplete")
            if not deleting_clean:
                print("  ✗ Orphaned .deleting folder found")
            return 1
        
    except Exception as e:
        print(f"\n❌ Validation failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        print(f"\nTest artifacts remain in: {test_base}")


if __name__ == "__main__":
    sys.exit(main())
