#!/usr/bin/env python
"""
RDD Instance Seed Script

Validates and initializes the RDD instance structure by ensuring all required
files and folders exist with correct content based on manifest.json configuration.

This script is idempotent and safe for repeated execution. It:
- Creates missing folders recursively (like mkdir -p)
- Creates missing required files with minimal valid content
- Preserves existing files without modification
- Validates created files (JSON syntax, UTF-8 encoding)
- Fails fast with specific error messages when configuration is invalid

Usage:
    python .rdd/src/actions/rdd-instance_seed.py [--verbose]

Exit Codes:
    0 - Success
    1 - Failure (manifest missing/invalid, convention file missing, validation failed)
"""

import argparse
import json
import logging
import sys
from pathlib import Path


def _setup_logging(verbose: bool) -> None:
    """
    Configure logging based on verbosity flag.
    
    Args:
        verbose: If True, set logging level to DEBUG; otherwise INFO
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s'
    )


def _get_repo_root() -> Path:
    """
    Get the repository root directory.
    
    Returns:
        Path object pointing to the repository root
    """
    # Script is at .rdd/src/actions/rdd-instance_seed.py
    # Repo root is 3 levels up
    return Path(__file__).resolve().parent.parent.parent.parent


def _load_manifest(repo_root: Path) -> dict:
    """
    Load and validate the manifest.json configuration file.
    
    Args:
        repo_root: Path to the repository root directory
        
    Returns:
        Parsed manifest data as a dictionary
        
    Raises:
        SystemExit: If manifest is missing or malformed
    """
    manifest_path = repo_root / '.rdd' / 'config' / 'manifest.json'
    
    if not manifest_path.exists():
        logging.error(f"Manifest file not found: {manifest_path}")
        logging.error("Remediation: Ensure the RDD framework is properly installed.")
        sys.exit(1)
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Manifest file is malformed: {e}")
        logging.error(f"File: {manifest_path}")
        logging.error("Remediation: Check manifest.json syntax and repair or reinstall the framework.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error reading manifest file: {e}")
        sys.exit(1)
    
    # Validate required keys exist
    if 'requiredPaths' not in manifest or 'instance' not in manifest['requiredPaths']:
        logging.error("Manifest is missing 'requiredPaths.instance' key")
        logging.error("Remediation: Verify manifest.json structure or reinstall the framework.")
        sys.exit(1)
    
    if 'requiredInstanceFiles' not in manifest:
        logging.error("Manifest is missing 'requiredInstanceFiles' key")
        logging.error("Remediation: Verify manifest.json structure or reinstall the framework.")
        sys.exit(1)
    
    logging.debug(f"Loaded manifest from {manifest_path}")
    return manifest


def _ensure_folders(repo_root: Path, manifest_data: dict) -> int:
    """
    Ensure all required folders exist, creating them recursively if needed.
    
    Args:
        repo_root: Path to the repository root directory
        manifest_data: Parsed manifest data
        
    Returns:
        Count of folders created
    """
    required_folders = manifest_data['requiredPaths']['instance']
    created_count = 0
    
    for folder_path in required_folders:
        full_path = repo_root / folder_path
        
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created folder: {full_path}")
            created_count += 1
        else:
            logging.debug(f"Folder already exists: {full_path}")
    
    return created_count


def _generate_file_content(file_path: Path, convention_path: Path, repo_root: Path) -> str:
    """
    Generate appropriate initial content for an instance file based on its type.
    
    Args:
        file_path: Path where the file will be created
        convention_path: Path to the convention file (for reference only)
        repo_root: Path to the repository root directory
        
    Returns:
        Generated content as a string
    """
    file_name = file_path.name
    
    if file_name == 'requirements.md':
        # Generate minimal valid requirements file
        return """## Product Name

TBD

## Product Overview

TBD

## Definitions

TBD

## User Requirements

TBD

## Technical Requirements

TBD
"""
    
    elif file_name == 'technical-design.json':
        # Generate empty JSON object
        return "{}\n"
    
    elif file_name == 'files-and-folders.md':
        # Generate minimal valid structure documentation
        return """## Files and Folders Structure

### Root Folder Structure

repo-root/

TBD
"""
    
    elif file_name == 'work-iteration-registry.json':
        # Generate empty work iteration registry
        return """{
    "iteration-id": null,
    "iteration-name": null,
    "prompt-id-sequence-next-value": 1,
    "git-enabled": false,
    "prompts": []
}
"""
    
    elif file_name == 'prompts-registry.md':
        # Generate empty prompts registry
        return "# Prompts Registry\n\nNo prompts recorded yet.\n"
    
    elif file_path.suffix == '.json':
        # Default for any other JSON file
        return "{}\n"
    
    elif file_path.suffix == '.md':
        # Default for any other Markdown file
        return f"# {file_path.stem}\n\nTBD\n"
    
    else:
        # Default for unknown file types
        return ""


def _validate_file(file_path: Path) -> None:
    """
    Validate a created file to ensure it's well-formed.
    
    Args:
        file_path: Path to the file to validate
        
    Raises:
        SystemExit: If validation fails
    """
    if file_path.suffix == '.json':
        # Validate JSON syntax
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            logging.debug(f"JSON validation passed: {file_path}")
        except json.JSONDecodeError as e:
            logging.error(f"Created file has invalid JSON syntax: {file_path}")
            logging.error(f"JSON error: {e}")
            logging.error("Remediation: This is a bug in the seed script. Please report it.")
            sys.exit(1)
    
    elif file_path.suffix == '.md':
        # Validate UTF-8 encoding
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read()
            logging.debug(f"UTF-8 encoding validation passed: {file_path}")
        except UnicodeDecodeError as e:
            logging.error(f"Created file has invalid UTF-8 encoding: {file_path}")
            logging.error(f"Encoding error: {e}")
            logging.error("Remediation: This is a bug in the seed script. Please report it.")
            sys.exit(1)


def _create_instance_file(file_path: Path, convention_path: Path, repo_root: Path) -> None:
    """
    Create an instance file with appropriate initial content.
    
    Args:
        file_path: Path where the file should be created
        convention_path: Path to the convention file (relative to repo root)
        repo_root: Path to the repository root directory
        
    Raises:
        SystemExit: If convention file is missing or file creation fails
    """
    # Verify convention file exists
    full_convention_path = repo_root / convention_path
    if not full_convention_path.exists():
        logging.error(f"Convention file not found: {full_convention_path}")
        logging.error(f"Required for creating: {file_path}")
        logging.error("Remediation: Check framework installation and ensure all convention files are present.")
        sys.exit(1)
    
    # Generate content
    content = _generate_file_content(file_path, full_convention_path, repo_root)
    
    # Write file
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f"Created file: {file_path}")
    except Exception as e:
        logging.error(f"Failed to create file: {file_path}")
        logging.error(f"Error: {e}")
        sys.exit(1)
    
    # Validate created file
    _validate_file(file_path)


def _ensure_files(repo_root: Path, manifest_data: dict) -> tuple:
    """
    Ensure all required instance files exist, creating them if needed.
    
    Args:
        repo_root: Path to the repository root directory
        manifest_data: Parsed manifest data
        
    Returns:
        Tuple of (created_count, skipped_count)
    """
    required_files = manifest_data['requiredInstanceFiles']
    created_count = 0
    skipped_count = 0
    
    for file_entry in required_files:
        file_path = repo_root / file_entry['path']
        convention_path = file_entry['convention']
        
        if file_path.exists():
            logging.info(f"File already exists (skipped): {file_path}")
            skipped_count += 1
        else:
            _create_instance_file(file_path, convention_path, repo_root)
            created_count += 1
    
    return (created_count, skipped_count)


def _print_summary(folders_created: int, files_created: int, files_skipped: int) -> None:
    """
    Print a summary of the seeding operation.
    
    Args:
        folders_created: Number of folders created
        files_created: Number of files created
        files_skipped: Number of existing files skipped
    """
    summary = f"Seed complete: {folders_created} folders created, {files_created} files created, {files_skipped} files skipped"
    print(summary)
    logging.info(summary)


def main() -> int:
    """
    Main entry point for the seed script.
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Validate and initialize RDD instance structure'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable DEBUG level logging'
    )
    args = parser.parse_args()
    
    # Setup logging
    _setup_logging(args.verbose)
    
    try:
        # Get repository root
        repo_root = _get_repo_root()
        logging.debug(f"Repository root: {repo_root}")
        
        # Load and validate manifest
        manifest = _load_manifest(repo_root)
        
        # Ensure folders exist
        folders_created = _ensure_folders(repo_root, manifest)
        
        # Ensure files exist
        files_created, files_skipped = _ensure_files(repo_root, manifest)
        
        # Print summary
        _print_summary(folders_created, files_created, files_skipped)
        
        return 0
        
    except SystemExit as e:
        # Re-raise SystemExit from helper functions
        return e.code if e.code is not None else 1
    except Exception as e:
        logging.error(f"Unexpected error during seeding: {e}")
        logging.error("Remediation: Check the error message above and ensure the framework is properly installed.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
