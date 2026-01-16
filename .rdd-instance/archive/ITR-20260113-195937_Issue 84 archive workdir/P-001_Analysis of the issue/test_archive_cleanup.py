#!/usr/bin/env python3
"""Test script to reproduce and validate workdir archive cleanup issue.

This script creates mockup folder structures and tests both the current
cleanup approach and the improved approach. It operates ONLY on temporary
folders in the prompt directory.

DO NOT run this against the actual .rdd-instance/workdir!
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Callable


def create_test_scenarios(base_path: Path) -> dict[str, Path]:
    """Create various test scenarios in temporary folders.
    
    Returns dict mapping scenario name to the created workdir path.
    """
    scenarios = {}
    
    # Scenario 1: Normal folder with files
    scenario1 = base_path / "scenario1_normal"
    scenario1.mkdir()
    workdir1 = scenario1 / "workdir"
    workdir1.mkdir()
    (workdir1 / "P-001_Test").mkdir()
    (workdir1 / "P-001_Test" / "file.txt").write_text("test content")
    (workdir1 / "P-002_Another").mkdir()
    (workdir1 / "P-002_Another" / "data.json").write_text('{"key": "value"}')
    scenarios["normal"] = workdir1
    
    # Scenario 2: Empty folders
    scenario2 = base_path / "scenario2_empty"
    scenario2.mkdir()
    workdir2 = scenario2 / "workdir"
    workdir2.mkdir()
    (workdir2 / "empty_folder_1").mkdir()
    (workdir2 / "empty_folder_2").mkdir()
    scenarios["empty_folders"] = workdir2
    
    # Scenario 3: Nested structure
    scenario3 = base_path / "scenario3_nested"
    scenario3.mkdir()
    workdir3 = scenario3 / "workdir"
    workdir3.mkdir()
    nested = workdir3 / "P-001" / "subfolder1" / "subfolder2"
    nested.mkdir(parents=True)
    (nested / "deep_file.txt").write_text("deep content")
    scenarios["nested"] = workdir3
    
    # Scenario 4: Mixed content
    scenario4 = base_path / "scenario4_mixed"
    scenario4.mkdir()
    workdir4 = scenario4 / "workdir"
    workdir4.mkdir()
    (workdir4 / "P-001_Prompt").mkdir()
    (workdir4 / "P-001_Prompt" / "file.txt").write_text("content")
    (workdir4 / "empty_folder").mkdir()
    (workdir4 / "standalone_file.md").write_text("# Readme")
    scenarios["mixed"] = workdir4
    
    # Scenario 5: Hidden files (simulated - some systems might ignore)
    scenario5 = base_path / "scenario5_hidden"
    scenario5.mkdir()
    workdir5 = scenario5 / "workdir"
    workdir5.mkdir()
    folder_with_hidden = workdir5 / "folder_with_hidden"
    folder_with_hidden.mkdir()
    # Try to create hidden files (different per platform)
    try:
        (folder_with_hidden / ".hidden_file").write_text("hidden")
    except Exception:
        # Fallback if hidden file creation fails
        (folder_with_hidden / "regular_file").write_text("content")
    scenarios["hidden_files"] = workdir5
    
    # Scenario 6: Registry file should be preserved during cleanup
    scenario6 = base_path / "scenario6_with_registry"
    scenario6.mkdir()
    workdir6 = scenario6 / "workdir"
    workdir6.mkdir()
    (workdir6 / "work-iteration-registry.json").write_text(json.dumps({
        "iteration-id": "ITR-TEST",
        "iteration-name": "Test Iteration"
    }))
    (workdir6 / "P-001_Test").mkdir()
    (workdir6 / "P-001_Test" / "file.txt").write_text("content")
    scenarios["with_registry"] = workdir6
    
    return scenarios


def cleanup_current_approach(workdir: Path) -> tuple[bool, list[str]]:
    """Simulate the current cleanup approach from workdir_archive.py.
    
    Returns (success, remaining_items).
    """
    remaining = []
    all_deleted = True
    
    for child in workdir.iterdir():
        try:
            if child.is_dir() and not child.is_symlink():
                shutil.rmtree(child)
            else:
                child.unlink()
        except Exception as e:
            # Best-effort cleanup: report but continue
            print(f"  WARNING: Could not delete {child}: {e}")
            remaining.append(str(child.name))
            all_deleted = False
    
    return all_deleted, remaining


def verify_archive_complete(source: Path, dest: Path) -> bool:
    """Verify that archive copy is complete."""
    if not dest.exists() or not dest.is_dir():
        return False
    
    # Count files in both directories
    def count_files(path: Path) -> int:
        return sum(1 for _ in path.rglob('*') if _.is_file())
    
    source_count = count_files(source)
    dest_count = count_files(dest)
    
    return source_count == dest_count


def delete_with_retry(path: Path, max_retries: int = 3, delay: float = 0.5) -> None:
    """Delete a path with retry logic for transient failures."""
    for attempt in range(max_retries):
        try:
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
            return
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Retry {attempt + 1}/{max_retries} after error: {e}")
                time.sleep(delay)
            else:
                raise


def cleanup_two_phase_approach(workdir: Path, archive_path: Path) -> tuple[bool, list[str]]:
    """Simulate the improved two-phase commit cleanup approach.
    
    Returns (success, remaining_items).
    """
    # Phase 1: Verify archive is complete
    if not verify_archive_complete(workdir, archive_path):
        print("  ERROR: Archive verification failed!")
        return False, ["VERIFICATION_FAILED"]
    
    # Phase 2: Two-phase commit
    workdir_deleting = workdir.parent / f"{workdir.name}.deleting"
    
    try:
        # Rename workdir to workdir.deleting
        workdir.rename(workdir_deleting)
        
        # Delete the renamed folder with retry
        delete_with_retry(workdir_deleting, max_retries=3, delay=0.3)
        
        # Create fresh empty workdir
        workdir.mkdir()
        
        # Final verification: check workdir is empty
        remaining = list(workdir.iterdir())
        if remaining:
            print(f"  ERROR: New workdir not empty: {[r.name for r in remaining]}")
            return False, [r.name for r in remaining]
        
        return True, []
        
    except Exception as e:
        print(f"  ERROR during two-phase cleanup: {e}")
        # If workdir.deleting still exists, we have a failure state
        if workdir_deleting.exists():
            return False, [f"CLEANUP_FAILED: {workdir_deleting.name} exists"]
        return False, ["UNKNOWN_ERROR"]


def test_scenario(
    scenario_name: str,
    workdir: Path,
    cleanup_func: Callable,
    approach_name: str
) -> dict:
    """Test a single scenario with a cleanup function."""
    print(f"\n  Testing {scenario_name} with {approach_name}:")
    
    # Create archive copy to simulate the archive operation
    archive_path = workdir.parent / "archive"
    if archive_path.exists():
        shutil.rmtree(archive_path)
    shutil.copytree(workdir, archive_path)
    
    # Count items before cleanup
    items_before = len(list(workdir.iterdir()))
    print(f"    Items before cleanup: {items_before}")
    
    # Run cleanup
    success, remaining = cleanup_func(workdir, archive_path) if approach_name == "two-phase" else cleanup_func(workdir)
    
    # Verify result
    items_after = len(list(workdir.iterdir())) if workdir.exists() else 0
    print(f"    Items after cleanup: {items_after}")
    
    if remaining:
        print(f"    Remaining items: {remaining}")
    
    result = {
        "scenario": scenario_name,
        "approach": approach_name,
        "success": success,
        "items_before": items_before,
        "items_after": items_after,
        "remaining": remaining,
        "fully_cleaned": items_after == 0
    }
    
    return result


def main():
    """Main test execution."""
    print("=" * 80)
    print("Testing Workdir Archive Cleanup Issue")
    print("=" * 80)
    
    # Create temporary test directory
    script_dir = Path(__file__).parent
    test_base = script_dir / "test_archive_temp"
    
    # Clean up any previous test runs
    if test_base.exists():
        shutil.rmtree(test_base)
    
    test_base.mkdir()
    
    print(f"\nCreating test scenarios in: {test_base}")
    scenarios = create_test_scenarios(test_base)
    print(f"Created {len(scenarios)} test scenarios")
    
    # Results collection
    results = []
    
    # Test each scenario with current approach
    print("\n" + "=" * 80)
    print("TESTING CURRENT APPROACH (best-effort cleanup)")
    print("=" * 80)
    
    for name, workdir in scenarios.items():
        # Make a copy for testing (since cleanup modifies the folder)
        test_workdir = workdir.parent / f"{workdir.name}_test_current"
        if test_workdir.exists():
            shutil.rmtree(test_workdir)
        shutil.copytree(workdir, test_workdir)
        
        result = test_scenario(name, test_workdir, cleanup_current_approach, "current")
        results.append(result)
    
    # Recreate scenarios for two-phase testing
    print("\n" + "=" * 80)
    print("TESTING TWO-PHASE COMMIT APPROACH")
    print("=" * 80)
    
    for name, workdir in scenarios.items():
        # Make a copy for testing
        test_workdir = workdir.parent / f"{workdir.name}_test_twophase"
        if test_workdir.exists():
            shutil.rmtree(test_workdir)
        shutil.copytree(workdir, test_workdir)
        
        result = test_scenario(name, test_workdir, cleanup_two_phase_approach, "two-phase")
        results.append(result)
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    current_results = [r for r in results if r["approach"] == "current"]
    twophase_results = [r for r in results if r["approach"] == "two-phase"]
    
    print("\nCurrent Approach:")
    current_success = sum(1 for r in current_results if r["fully_cleaned"])
    print(f"  Fully cleaned: {current_success}/{len(current_results)}")
    for r in current_results:
        if not r["fully_cleaned"]:
            print(f"    ❌ {r['scenario']}: {r['items_after']} items remaining")
    
    print("\nTwo-Phase Approach:")
    twophase_success = sum(1 for r in twophase_results if r["fully_cleaned"])
    print(f"  Fully cleaned: {twophase_success}/{len(twophase_results)}")
    for r in twophase_results:
        if not r["fully_cleaned"]:
            print(f"    ❌ {r['scenario']}: {r['items_after']} items remaining")
        else:
            print(f"    ✅ {r['scenario']}: Successfully cleaned")
    
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    
    if twophase_success > current_success:
        print(f"✅ Two-phase approach is more reliable ({twophase_success} vs {current_success} scenarios)")
    elif twophase_success == current_success == len(current_results):
        print("✅ Both approaches work on these test scenarios")
        print("   However, two-phase provides better error handling for real-world failures")
    else:
        print("⚠️  Results need investigation")
    
    print(f"\nTest artifacts remain in: {test_base}")
    print("Review the folders to see what was left behind in each scenario.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
