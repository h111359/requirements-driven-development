#!/usr/bin/env python3
"""
list-files.py
Lists all files and folders recursively in the workspace, excluding folders starting with "."
Outputs results to files-list.md
"""

import os
from pathlib import Path
from datetime import datetime

def get_file_info(root_dir):
    """
    Recursively list all files and folders, excluding those starting with "."
    Returns list of tuples: (relative_path, is_dir, last_modified)
    """
    results = []
    root_path = Path(root_dir)
    
    for item in root_path.rglob('*'):
        # Skip items in directories starting with "."
        if any(part.startswith('.git') for part in item.parts):
           continue
        
        relative_path = item.relative_to(root_path)
        is_dir = item.is_dir()
        
        try:
            last_modified = datetime.fromtimestamp(item.stat().st_mtime)
            results.append((str(relative_path), is_dir, last_modified))
        except (OSError, FileNotFoundError):
            # Skip files that can't be accessed
            continue
    
    return sorted(results)

def format_file_list(file_info):
    """Format file information as markdown"""
    lines = ["# Project Files List\n"]
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("\n## Files and Folders\n")
    
    current_folder = None
    
    for relative_path, is_dir, last_modified in file_info:
        path_obj = Path(relative_path)
        folder = str(path_obj.parent) if path_obj.parent != Path('.') else 'root'
        
        # Add folder header when we enter a new folder
        if folder != current_folder:
            current_folder = folder
            lines.append(f"\n### {folder}\n")
        
        # Format entry
        item_type = "📁 Folder" if is_dir else "📄 File"
        mod_time = last_modified.strftime('%Y-%m-%d %H:%M:%S')
        lines.append(f"- **{relative_path}** - {item_type} - Last modified: {mod_time}\n")
    
    return ''.join(lines)

def main():
    # Get workspace root (parent of .rdd-docs/workspace/)
    script_dir = Path(__file__).parent
    workspace_root = script_dir.parent.parent
    
    print(f"Scanning: {workspace_root}")
    
    # Get file information
    file_info = get_file_info(workspace_root)
    
    # Format as markdown
    markdown = format_file_list(file_info)
    
    # Write to output file
    output_file = script_dir / "files-list.md"
    output_file.write_text(markdown)
    
    print(f"✓ File list written to: {output_file}")
    print(f"  Total items: {len(file_info)}")

if __name__ == "__main__":
    main()
