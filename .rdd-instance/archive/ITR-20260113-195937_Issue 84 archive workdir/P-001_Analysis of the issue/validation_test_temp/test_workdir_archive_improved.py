#!/usr/bin/env python3
"""Archive the current workdir into `.rdd-instance/archive/<iteration-id>_<iteration-name>/`.

Source of truth:
    `.rdd-instance/workdir/work-iteration-registry.json`
        keys: `iteration-id`, `iteration-name`

Behavior:
    - Reads `iteration-id` and `iteration-name` from the registry JSON.
    - Copies the entire contents of `.rdd-instance/workdir/` into a new folder:
            `.rdd-instance/archive/<iteration-id>_<iteration-name>/`
    - Refuses to run if the destination archive folder already exists.
    - Uses two-phase commit approach for safe cleanup:
        1. Archive and verify completeness
        2. Rename workdir to workdir.deleting
        3. Delete the renamed folder with retry logic
        4. Create fresh empty workdir
    - Fails fast on errors rather than best-effort cleanup

This script is intentionally deterministic and non-interactive.
"""

from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path


def _repo_root() -> Path:
    # Modified for testing
    return Path(r'/home/hromar/Desktop/vscode/requirements-driven-development/.rdd-instance/workdir/P-001_Analysis of the issue/validation_test_temp')


def _read_iteration_archive_name(registry_path: Path) -> str:
    with registry_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Registry JSON must be an object: {registry_path}")

    iteration_id = data.get("iteration-id")
    iteration_name = data.get("iteration-name")

    if not isinstance(iteration_id, str) or not iteration_id.strip():
        raise ValueError(f"Missing or empty 'iteration-id' in {registry_path}")
    if not isinstance(iteration_name, str) or not iteration_name.strip():
        raise ValueError(f"Missing or empty 'iteration-name' in {registry_path}")

    # Exact requested shape: <iteration-id> + "_" + <iteration-name>
    archive_name = f"{iteration_id.strip()}_{iteration_name.strip()}"

    # Safety: disallow path separators; keep name as a single folder.
    if "/" in archive_name or "\\" in archive_name:
        raise ValueError(
            "Invalid iteration registry values (must not contain path separators): "
            f"{archive_name!r}"
        )

    return archive_name


def _verify_archive_complete(source: Path, dest: Path) -> bool:
    """Verify that the archive copy is complete.
    
    Compares file counts and directory structure between source and destination
    to ensure the archive operation succeeded completely.
    
    Args:
        source: The source workdir path
        dest: The destination archive path
        
    Returns:
        True if archive is complete and valid, False otherwise
    """
    if not dest.exists() or not dest.is_dir():
        return False
    
    # Count all files recursively in both directories
    def count_files(path: Path) -> int:
        return sum(1 for _ in path.rglob('*') if _.is_file())
    
    source_count = count_files(source)
    dest_count = count_files(dest)
    
    # Archive must have the same number of files as source
    return source_count == dest_count


def _delete_with_retry(
    path: Path,
    max_retries: int = 3,
    delay: float = 0.5
) -> None:
    """Delete a path with retry logic for transient failures.
    
    Handles transient failures like temporary file locks or antivirus scanning
    by retrying the deletion operation with delays.
    
    Args:
        path: Path to delete (file or directory)
        max_retries: Maximum number of retry attempts
        delay: Delay in seconds between retries
        
    Raises:
        Exception: If deletion fails after all retry attempts
    """
    last_error = None
    
    for attempt in range(max_retries):
        try:
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
            return  # Success
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                # Not the last attempt, wait and retry
                time.sleep(delay)
            else:
                # Last attempt failed, raise the error
                raise Exception(
                    f"Failed to delete {path} after {max_retries} attempts. "
                    f"Last error: {e}. "
                    f"Suggestion: Check for file locks, permissions, or close "
                    f"applications that might be using files in this directory."
                ) from last_error


def main() -> int:
    repo_root = _repo_root()

    workdir = repo_root / ".rdd-instance" / "workdir"
    registry_path = workdir / "work-iteration-registry.json"
    archive_root = repo_root / ".rdd-instance" / "archive"

    if not workdir.is_dir():
        raise FileNotFoundError(f"Workdir not found: {workdir}")
    if not registry_path.is_file():
        raise FileNotFoundError(f"Work iteration registry not found: {registry_path}")

    archive_name = _read_iteration_archive_name(registry_path)
    dest_dir = archive_root / archive_name

    if dest_dir.exists():
        print(f"Archive destination already exists ({dest_dir}); nothing to do.")
        return 0

    archive_root.mkdir(parents=True, exist_ok=True)

    # Phase 1: Archive and Verify
    # Copy the entire directory tree to archive location
    shutil.copytree(workdir, dest_dir)
    
    # Verify the archive copy is complete before proceeding to cleanup
    if not _verify_archive_complete(workdir, dest_dir):
        raise RuntimeError(
            f"Archive verification failed. The archive at {dest_dir} does not "
            f"match the source at {workdir}. File counts differ. "
            f"Archive created but workdir cleanup skipped for safety."
        )

    # Phase 2: Two-Phase Commit Cleanup
    # Rename workdir to mark it as being deleted (atomic operation)
    workdir_deleting = workdir.parent / f"{workdir.name}.deleting"
    
    try:
        workdir.rename(workdir_deleting)
    except Exception as e:
        raise RuntimeError(
            f"Failed to rename {workdir} to {workdir_deleting}. "
            f"Archive successfully created at {dest_dir}, but cleanup could not proceed. "
            f"Error: {e}"
        ) from e
    
    # Delete the renamed folder with retry logic for transient failures
    try:
        _delete_with_retry(workdir_deleting, max_retries=3, delay=0.5)
    except Exception as e:
        raise RuntimeError(
            f"Failed to delete {workdir_deleting}. "
            f"Archive successfully created at {dest_dir}. "
            f"The folder has been renamed to indicate deletion failure. "
            f"Please manually investigate and remove {workdir_deleting}. "
            f"Error: {e}"
        ) from e
    
    # Create fresh empty workdir
    workdir.mkdir(parents=True, exist_ok=True)
    
    # Final verification: ensure the new workdir is empty
    remaining_items = list(workdir.iterdir())
    if remaining_items:
        remaining_names = [item.name for item in remaining_items]
        raise RuntimeError(
            f"Workdir cleanup verification failed. "
            f"Archive created at {dest_dir} and old workdir deleted, "
            f"but the new workdir at {workdir} is not empty. "
            f"Unexpected items: {remaining_names}"
        )

    # Keep stdout single-line and agent-friendly.
    print(str(dest_dir))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
