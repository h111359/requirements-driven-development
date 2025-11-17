#!/usr/bin/env python3
"""
Script to list all files and folders in the project, excluding dot-folders and venv
"""

import os
from pathlib import Path
from datetime import datetime

def should_exclude(path_name):
    """Check if a path should be excluded"""
    exclude_patterns = ['venv', '__pycache__', '.pytest_cache', 'node_modules', '.git']
    # Check if path starts with a dot (hidden folder/file)
    if path_name.startswith('.') and path_name not in ['.rdd', '.rdd-docs', '.github', '.vscode']:
        return True
    return any(pattern == path_name for pattern in exclude_patterns)

def get_file_list(root_dir):
    """Get list of all files with metadata"""
    file_list = []
    
    for root, dirs, files in os.walk(root_dir):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if not should_exclude(d)]
        
        rel_root = os.path.relpath(root, root_dir)
        if rel_root == '.':
            rel_root = ''
        
        for file in files:
            if should_exclude(file):
                continue
            
            full_path = os.path.join(root, file)
            rel_path = os.path.join(rel_root, file) if rel_root else file
            
            try:
                mtime = os.path.getmtime(full_path)
                mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                
                file_list.append({
                    'name': file,
                    'path': rel_path,
                    'modified': mtime_str
                })
            except OSError:
                continue
    
    return sorted(file_list, key=lambda x: x['path'])

def main():
    """Main function"""
    # Get project root (3 levels up from workspace)
    script_dir = Path(__file__).parent.absolute()
    project_root = script_dir.parent.parent
    
    print(f"Scanning project: {project_root}")
    
    files = get_file_list(project_root)
    
    # Write output
    output_file = script_dir / 'files-list.md'
    with open(output_file, 'w') as f:
        f.write('# Project Files List\n\n')
        f.write(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        f.write('| File Name | Relative Path | Last Modified |\n')
        f.write('|-----------|---------------|---------------|\n')
        
        for file_info in files:
            f.write(f"| {file_info['name']} | {file_info['path']} | {file_info['modified']} |\n")
    
    print(f"✓ File list written to: {output_file}")
    print(f"  Total files: {len(files)}")

if __name__ == '__main__':
    main()
