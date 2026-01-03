#!/usr/bin/env python3
"""
Script to set description for a file in the files listing CSV.

Usage:
    python files_list_csv_set_description.py file-name=<name> relative-path=<path> description=<text>

This script updates the Description field for a specific file entry in the CSV.
"""

import csv
import sys
from pathlib import Path


# Define the repository root (parent of .rdd)
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
CSV_FILE = REPO_ROOT / ".rdd-instance" / "specifications" / "files-list.csv"


def parse_arguments() -> dict:
    """
    Parse command-line arguments in key=value format.
    
    Returns:
        dict: Parsed arguments
    """
    args = {}
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            args[key] = value
    return args


def read_csv() -> list:
    """
    Read the CSV file and return all rows.
    
    Returns:
        list: List of row dictionaries
    """
    if not CSV_FILE.exists():
        print(f"Error: CSV file does not exist: {CSV_FILE}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            return list(reader)
    except Exception as e:
        print(f"Error: Could not read CSV file: {e}", file=sys.stderr)
        sys.exit(1)


def write_csv(rows: list):
    """
    Write rows back to the CSV file.
    
    Args:
        rows: List of row dictionaries to write
    """
    try:
        with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ["File Name", "Relative Path", "Modification Time", "Description"]
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
            
            writer.writeheader()
            writer.writerows(rows)
    except Exception as e:
        print(f"Error: Could not write CSV file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main execution function."""
    # Parse arguments
    args = parse_arguments()
    
    # Validate required parameters
    required = ["file-name", "relative-path", "description"]
    missing = [param for param in required if param not in args]
    
    if missing:
        print(f"Error: Missing required parameters: {', '.join(missing)}", file=sys.stderr)
        print(f"\nUsage: {sys.argv[0]} file-name=<name> relative-path=<path> description=<text>", file=sys.stderr)
        sys.exit(1)
    
    file_name = args["file-name"]
    relative_path = args["relative-path"]
    description = args["description"]
    
    # Read CSV
    rows = read_csv()
    
    # Find and update the matching row
    found = False
    for row in rows:
        if row["File Name"] == file_name and row["Relative Path"] == relative_path:
            row["Description"] = description
            found = True
            break
    
    if not found:
        print(f"Error: No matching file found with File Name='{file_name}' and Relative Path='{relative_path}'", file=sys.stderr)
        sys.exit(1)
    
    # Write updated CSV
    write_csv(rows)
    
    print(f"Successfully updated description for {relative_path}")


if __name__ == "__main__":
    main()
