#!/usr/bin/env python3
"""
list-files.py
Lists all files and folders in the project, recursively.
Excludes folders starting with "." and virtual environment folders.
Stores the result in .rdd-docs/workspace/files-list.md
"""

import os
from pathlib import Path
from datetime import datetime

def should_exclude_dir(dir_name):
    """Check if directory should be excluded"""
    exclude_patterns = ['.', 'venv', '__pycache__', 'node_modules']
    return any(dir_name.startswith(pattern) or dir_name == pattern for pattern in exclude_patterns)

def get_file_info(root_path):
    """Get all file information recursively"""
    files_info = []
    root = Path(root_path)
    
    for item in root.rglob('*'):
        # Skip excluded directories
        if any(should_exclude_dir(part) for part in item.parts):
            continue
            
        # Only process files
        if item.is_file():
            try:
                stat = item.stat()
                modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                relative_path = item.relative_to(root)
                
                files_info.append({
                    'name': item.name,
                    'path': str(relative_path),
                    'modified': modified,
                    'folder': str(relative_path.parent) if relative_path.parent != Path('.') else '(root)'
                })
            except (OSError, PermissionError):
                # Skip files we can't access
                pass
    
    return files_info

def write_files_list(files_info, output_path):
    """Write files list to markdown file"""
    # Sort by folder, then by name
    files_info.sort(key=lambda x: (x['folder'], x['name']))
    
    with open(output_path, 'w') as f:
        f.write('# Project Files List\n\n')
        f.write(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        
        current_folder = None
        for file_info in files_info:
            if file_info['folder'] != current_folder:
                current_folder = file_info['folder']
                f.write(f'\n## {current_folder}\n\n')
            
            f.write(f'- **{file_info["name"]}**\n')
            f.write(f'  - Path: `{file_info["path"]}`\n')
            f.write(f'  - Last modified: {file_info["modified"]}\n')

def main():
    # Get project root (3 levels up from this script)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    
    print(f"Scanning project at: {project_root}")
    
    # Get all files
    files_info = get_file_info(project_root)
    
    print(f"Found {len(files_info)} files")
    
    # Write output
    output_path = script_dir / 'files-list.md'
    write_files_list(files_info, output_path)
    
    print(f"Files list written to: {output_path}")

if __name__ == '__main__':
    main()
