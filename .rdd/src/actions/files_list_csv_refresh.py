#!/usr/bin/env python3
"""
Script to refresh the files listing CSV.

This script scans the repository recursively and maintains a CSV file with:
- File Name: The name of the file
- Relative Path: Path relative to repository root
- Modification Time: ISO8601 formatted timestamp
- Description: Manually maintained description (preserved for unchanged files)

The script:
- Adds new files with empty descriptions
- Updates modification times and clears descriptions for modified files
- Removes deleted files from the CSV
- Preserves descriptions for unchanged files
"""

import os
import csv
import sys
from pathlib import Path
from datetime import datetime

# Define the repository root (parent of .rdd)
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
CSV_FILE = REPO_ROOT / ".rdd-instance" / "specifications" / "files-list.csv"

# Directories to exclude
EXCLUDED_DIRS = {"venv", "__pycache__", ".git", ".rdd-instance"}


def should_exclude(path: Path) -> bool:
    """Check if a path should be excluded from the listing."""
    # Exclude if any part of the path starts with "." or is in excluded dirs
    for part in path.parts:
        if part.startswith(".") or part in EXCLUDED_DIRS:
            return True
    return False


def get_modification_time(file_path: Path) -> str:
    """Get file modification time in ISO8601 format."""
    mtime = file_path.stat().st_mtime
    dt = datetime.fromtimestamp(mtime)
    return dt.isoformat()


def scan_repository() -> dict:
    """
    Scan repository for all files.
    
    Returns:
        dict: Map of relative_path -> {file_name, mtime}
    """
    files_data = {}
    
    for root, dirs, files in os.walk(REPO_ROOT):
        root_path = Path(root)
        
        # Skip excluded directories
        if should_exclude(root_path.relative_to(REPO_ROOT)):
            dirs[:] = []  # Don't recurse into this directory
            continue
        
        # Remove excluded directories from dirs list to prevent recursion
        dirs[:] = [d for d in dirs if not (d.startswith(".") or d in EXCLUDED_DIRS)]
        
        # Process files in this directory
        for file in files:
            file_path = root_path / file
            rel_path = str(file_path.relative_to(REPO_ROOT))
            
            # Skip if file itself starts with "."
            if file.startswith("."):
                continue
            
            files_data[rel_path] = {
                "file_name": file,
                "mtime": get_modification_time(file_path)
            }
    
    return files_data


def read_existing_csv() -> dict:
    """
    Read existing CSV file if it exists.
    
    Returns:
        dict: Map of relative_path -> {file_name, mtime, description}
    """
    if not CSV_FILE.exists():
        return {}
    
    existing_data = {}
    
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                rel_path = row.get("Relative Path", "").strip()
                if rel_path:
                    existing_data[rel_path] = {
                        "file_name": row.get("File Name", ""),
                        "mtime": row.get("Modification Time", ""),
                        "description": row.get("Description", "")
                    }
    except Exception as e:
        print(f"Warning: Could not read existing CSV: {e}", file=sys.stderr)
        return {}
    
    return existing_data


def write_csv(data: dict):
    """
    Write updated data to CSV file.
    
    Args:
        data: dict mapping relative_path -> {file_name, mtime, description}
    """
    # Ensure directory exists
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Sort by relative path for consistent output
    sorted_paths = sorted(data.keys())
    
    with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ["File Name", "Relative Path", "Modification Time", "Description"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
        
        writer.writeheader()
        
        for rel_path in sorted_paths:
            entry = data[rel_path]
            writer.writerow({
                "File Name": entry["file_name"],
                "Relative Path": rel_path,
                "Modification Time": entry["mtime"],
                "Description": entry.get("description", "")
            })


def main():
    """Main execution function."""
    print("Scanning repository for files...")
    current_files = scan_repository()
    
    print(f"Found {len(current_files)} files in repository")
    
    print("Reading existing CSV...")
    existing_data = read_existing_csv()
    
    print(f"Found {len(existing_data)} entries in existing CSV")
    
    # Build updated data
    updated_data = {}
    
    for rel_path, file_info in current_files.items():
        if rel_path in existing_data:
            # File exists in CSV
            existing = existing_data[rel_path]
            
            if file_info["mtime"] != existing["mtime"]:
                # File has been modified - update mtime and clear description
                updated_data[rel_path] = {
                    "file_name": file_info["file_name"],
                    "mtime": file_info["mtime"],
                    "description": ""
                }
                print(f"Updated (modified): {rel_path}")
            else:
                # File unchanged - preserve description
                updated_data[rel_path] = {
                    "file_name": file_info["file_name"],
                    "mtime": file_info["mtime"],
                    "description": existing["description"]
                }
        else:
            # New file - add with empty description
            updated_data[rel_path] = {
                "file_name": file_info["file_name"],
                "mtime": file_info["mtime"],
                "description": ""
            }
            print(f"Added (new): {rel_path}")
    
    # Check for deleted files
    for rel_path in existing_data:
        if rel_path not in current_files:
            print(f"Removed (deleted): {rel_path}")
    
    print(f"\nWriting updated CSV with {len(updated_data)} entries...")
    write_csv(updated_data)
    
    print(f"Successfully updated {CSV_FILE}")


if __name__ == "__main__":
    main()
