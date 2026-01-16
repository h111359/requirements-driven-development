#!/usr/bin/env python3
"""Archive the current workdir into `.rdd-instance/archive/<iteration-id>_<iteration-name>.zip`.

Source of truth:
    `.rdd-instance/workdir/work-iteration-registry.json`
        keys: `iteration-id`, `iteration-name`
    `.rdd-instance/config/instance-config.json`
        keys: `git-enabled` (boolean)

Behavior:
    - Reads `iteration-id` and `iteration-name` from the registry JSON.
    - Copies the entire contents of `.rdd-instance/workdir/` into a new folder:
            `.rdd-instance/archive/<iteration-id>_<iteration-name>/`
    - Creates a zip file from the archived directory
    - Verifies zip integrity and deletes the directory, keeping only the zip file
    - Clears the workdir, creates a fresh empty one, and verifies it's empty
    - If git-enabled is true, performs a git commit with message "Archive iteration: <iteration-id> - <iteration-name>"
    - Refuses to run if the destination archive zip file already exists.
    - Uses two-phase commit approach for safe cleanup:
        1. Archive to directory and verify completeness
        2. Create zip file and verify integrity
        3. Delete directory-based archive
        4. Rename workdir to workdir.deleting
        5. Delete the renamed folder with retry logic
        6. Create fresh empty workdir and verify it's empty
        7. If git-enabled: perform git commit (fails entire operation if commit fails)
    - Fails fast on errors rather than best-effort cleanup

This script is intentionally deterministic and non-interactive.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path


def _repo_root() -> Path:
    # This file lives at: <repo>/.rdd/src/actions/workdir-archive.py
    return Path(__file__).resolve().parents[3]


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


def _read_iteration_name(registry_path: Path) -> str:
    """Read just the iteration name from the registry.
    
    Args:
        registry_path: Path to work-iteration-registry.json
        
    Returns:
        The iteration name string
    """
    with registry_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Registry JSON must be an object: {registry_path}")

    iteration_name = data.get("iteration-name")

    if not isinstance(iteration_name, str) or not iteration_name.strip():
        raise ValueError(f"Missing or empty 'iteration-name' in {registry_path}")

    return iteration_name.strip()


def _read_iteration_id(registry_path: Path) -> str:
    """Read just the iteration ID from the registry.
    
    Args:
        registry_path: Path to work-iteration-registry.json
        
    Returns:
        The iteration ID string
    """
    with registry_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Registry JSON must be an object: {registry_path}")

    iteration_id = data.get("iteration-id")

    if not isinstance(iteration_id, str) or not iteration_id.strip():
        raise ValueError(f"Missing or empty 'iteration-id' in {registry_path}")

    return iteration_id.strip()


def _read_git_enabled(config_path: Path) -> bool:
    """Read the git-enabled flag from instance config.
    
    Args:
        config_path: Path to instance-config.json
        
    Returns:
        True if git integration is enabled, False otherwise
    """
    if not config_path.exists():
        return False
    
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not isinstance(data, dict):
            return False
        
        git_enabled = data.get("git-enabled", False)
        return bool(git_enabled)
    except Exception:
        return False


def _git_commit(repo_root: Path, message: str) -> None:
    """Perform a git commit with the given message.
    
    Args:
        repo_root: The repository root path
        message: The commit message
        
    Raises:
        Exception: If git commit fails
    """
    try:
        # First, add all changes
        result = subprocess.run(
            ["git", "add", "-A"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Then commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True
        )
        
    except subprocess.CalledProcessError as e:
        # Git commit failed - this fails the entire archive operation
        raise Exception(
            f"Git commit failed. The archive was created successfully, "
            f"but the commit operation failed. "
            f"Error: {e.stderr if e.stderr else e.stdout}"
        ) from e
    except FileNotFoundError:
        raise Exception(
            "Git command not found. Ensure git is installed and in your PATH."
        )


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


def _normalize_file_timestamp(file_path: Path) -> bool:
    """Normalize file timestamp to be compatible with ZIP format.
    
    ZIP format does not support timestamps before 1980-01-01 00:00:00.
    This function checks if a file has a pre-1980 timestamp and normalizes
    it to 1980-01-01 00:00:00 if needed.
    
    Args:
        file_path: Path to the file to normalize
        
    Returns:
        True if the timestamp was normalized, False otherwise
        
    Raises:
        Exception: If timestamp normalization fails
    """
    try:
        # Get the current modification time
        stat_info = os.stat(file_path)
        mtime = stat_info.st_mtime
        
        # ZIP format minimum timestamp: 1980-01-01 00:00:00
        # Unix timestamp for 1980-01-01 00:00:00 UTC is 315532800
        MIN_ZIP_TIMESTAMP = 315532800
        
        if mtime < MIN_ZIP_TIMESTAMP:
            # File has a pre-1980 timestamp, normalize it
            os.utime(file_path, (MIN_ZIP_TIMESTAMP, MIN_ZIP_TIMESTAMP))
            return True
        
        return False
    except Exception as e:
        raise Exception(
            f"Failed to normalize timestamp for {file_path}. Error: {e}"
        ) from e


def _create_zip_archive(source_dir: Path, zip_path: Path) -> None:
    """Create a zip file from a directory.
    
    Args:
        source_dir: The directory to compress
        zip_path: The destination zip file path
        
    Raises:
        Exception: If zip creation fails
    """
    normalized_count = 0
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in source_dir.rglob('*'):
                if file_path.is_file():
                    # Normalize timestamp before adding to zip to prevent
                    # "ZIP does not support timestamps before 1980" errors
                    if _normalize_file_timestamp(file_path):
                        normalized_count += 1
                    
                    # Store the path relative to the source directory
                    arcname = file_path.relative_to(source_dir)
                    zipf.write(file_path, arcname)
        
        # Log summary if any timestamps were normalized
        if normalized_count > 0:
            print(
                f"INFO: Normalized {normalized_count} file(s) with pre-1980 timestamps "
                f"to ensure ZIP format compatibility.",
                file=sys.stderr
            )
            
    except Exception as e:
        # Clean up partial zip file on failure
        if zip_path.exists():
            zip_path.unlink()
        raise Exception(
            f"Failed to create zip archive at {zip_path}. Error: {e}"
        ) from e


def _verify_zip_integrity(zip_path: Path) -> bool:
    """Verify that a zip file is valid and can be read.
    
    Args:
        zip_path: Path to the zip file to verify
        
    Returns:
        True if zip file is valid, False otherwise
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            # Test the zip file integrity
            bad_file = zipf.testzip()
            if bad_file is not None:
                return False
            # Ensure we can list all files
            file_list = zipf.namelist()
            return len(file_list) > 0  # Should have at least the registry file
    except Exception:
        return False


def main() -> int:
    repo_root = _repo_root()

    workdir = repo_root / ".rdd-instance" / "workdir"
    registry_path = workdir / "work-iteration-registry.json"
    archive_root = repo_root / ".rdd-instance" / "archive"
    config_path = repo_root / ".rdd-instance" / "config" / "instance-config.json"

    if not workdir.is_dir():
        raise FileNotFoundError(f"Workdir not found: {workdir}")
    if not registry_path.is_file():
        raise FileNotFoundError(f"Work iteration registry not found: {registry_path}")

    archive_name = _read_iteration_archive_name(registry_path)
    iteration_name = _read_iteration_name(registry_path)
    iteration_id = _read_iteration_id(registry_path)
    git_enabled = _read_git_enabled(config_path)
    
    dest_dir = archive_root / archive_name
    zip_path = archive_root / f"{archive_name}.zip"

    # Check if zip archive already exists
    if zip_path.exists():
        print(f"Archive zip file already exists ({zip_path}); nothing to do.")
        return 0

    archive_root.mkdir(parents=True, exist_ok=True)

    # Phase 1: Archive to Directory and Verify
    # Copy the entire directory tree to archive location
    shutil.copytree(workdir, dest_dir)
    
    # Verify the archive copy is complete before proceeding
    if not _verify_archive_complete(workdir, dest_dir):
        raise RuntimeError(
            f"Archive verification failed. The archive at {dest_dir} does not "
            f"match the source at {workdir}. File counts differ. "
            f"Archive created but further processing aborted for safety."
        )

    # Phase 2: Create Zip Archive and Verify
    # Create zip file from the archived directory
    _create_zip_archive(dest_dir, zip_path)
    
    # Verify the zip file integrity
    if not _verify_zip_integrity(zip_path):
        raise RuntimeError(
            f"Zip archive verification failed. The zip file at {zip_path} "
            f"failed integrity check. Directory archive at {dest_dir} preserved for safety."
        )
    
    # Phase 3: Delete Directory-Based Archive
    # Now that zip is verified, remove the directory-based archive
    try:
        _delete_with_retry(dest_dir, max_retries=3, delay=0.5)
    except Exception as e:
        raise RuntimeError(
            f"Failed to delete directory archive at {dest_dir}. "
            f"Zip archive successfully created at {zip_path}. "
            f"You may manually delete the directory archive if needed. "
            f"Error: {e}"
        ) from e

    # Phase 4: Two-Phase Commit Cleanup of Workdir
    # Rename workdir to mark it as being deleted (atomic operation)
    workdir_deleting = workdir.parent / f"{workdir.name}.deleting"
    
    try:
        workdir.rename(workdir_deleting)
    except Exception as e:
        raise RuntimeError(
            f"Failed to rename {workdir} to {workdir_deleting}. "
            f"Archive successfully created at {zip_path}, but cleanup could not proceed. "
            f"Error: {e}"
        ) from e
    
    # Delete the renamed folder with retry logic for transient failures
    try:
        _delete_with_retry(workdir_deleting, max_retries=3, delay=0.5)
    except Exception as e:
        raise RuntimeError(
            f"Failed to delete {workdir_deleting}. "
            f"Archive successfully created at {zip_path}. "
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
            f"Archive created at {zip_path} and old workdir deleted, "
            f"but the new workdir at {workdir} is not empty. "
            f"Unexpected items: {remaining_names}"
        )

    # Phase 5: Git Commit (if enabled)
    # After all cleanup operations succeed and verification passes, commit to git if configured
    # This ensures the commit represents the complete final state with a verified empty workdir
    if git_enabled:
        commit_message = f"Archive iteration: {iteration_id} - {iteration_name}"
        _git_commit(repo_root, commit_message)

    # Keep stdout single-line and agent-friendly - return the zip path
    print(str(zip_path))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
