#!/usr/bin/env python3
"""
bash-to-powershell.py
Converts bash scripts to PowerShell equivalents

This script handles the conversion of common bash patterns to PowerShell,
suitable for the RDD framework scripts.
"""

import sys
import os
import re
from pathlib import Path


def convert_bash_to_powershell(bash_content):
    """Convert bash script content to PowerShell"""
    lines = bash_content.split('\n')
    ps_lines = []
    in_function = False
    
    for line in lines:
        # Skip shebang
        if line.startswith('#!'):
            continue
        
        # Keep comments
        if line.strip().startswith('#') and not line.startswith('#!'):
            ps_lines.append(line)
            continue
        
        # Empty lines
        if not line.strip():
            ps_lines.append('')
            continue
        
        # Convert set -e
        if re.match(r'^\s*set\s+-e', line):
            ps_lines.append('$ErrorActionPreference = "Stop"')
            continue
        
        # Get script directory patterns
        if 'SCRIPT_DIR' in line and 'dirname' in line and 'BASH_SOURCE' in line:
            ps_lines.append('$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path')
            continue
        
        if 'PROJECT_ROOT' in line and 'SCRIPT_DIR/..' in line:
            ps_lines.append('$PROJECT_ROOT = Split-Path -Parent $SCRIPT_DIR')
            continue
        
        # Simple variable assignments
        match = re.match(r'^\s*([A-Z_][A-Z0-9_]*)="([^"]*)"$', line)
        if match:
            ps_lines.append(f'${match.group(1)} = "{match.group(2)}"')
            continue
        
        match = re.match(r"^\s*([A-Z_][A-Z0-9_]*)='([^']*)'$", line)
        if match:
            ps_lines.append(f'${match.group(1)} = \'{match.group(2)}\'')
            continue
        
        # Local variable assignments (in functions)
        match = re.match(r'^\s*local\s+([a-z_][a-z0-9_]*)="([^"]*)"$', line)
        if match:
            ps_lines.append(f'    ${match.group(1)} = "{match.group(2)}"')
            continue
        
        match = re.match(r"^\s*local\s+([a-z_][a-z0-9_]*)='([^']*)'$", line)
        if match:
            ps_lines.append(f'    ${match.group(1)} = \'{match.group(2)}\'')
            continue
        
        # cd commands
        match = re.match(r'^\s*cd\s+"([^"]+)"', line)
        if match:
            ps_lines.append(f'Set-Location "{match.group(1)}"')
            continue
        
        match = re.match(r'^\s*cd\s+([^\s]+)', line)
        if match:
            path = match.group(1)
            # Handle variable references
            path = path.replace('$', '$')
            ps_lines.append(f'Set-Location {path}')
            continue
        
        # echo commands with -e flag (color codes)
        match = re.match(r'^\s*echo\s+-e\s+"([^"]*)"', line)
        if match:
            text = match.group(1)
            # PowerShell doesn't need -e equivalent, Write-Host handles colors differently
            ps_lines.append(f'Write-Host "{text}"')
            continue
        
        # Regular echo commands
        match = re.match(r'^\s*echo\s+"([^"]*)"', line)
        if match:
            text = match.group(1)
            ps_lines.append(f'Write-Host "{text}"')
            continue
        
        match = re.match(r"^\s*echo\s+'([^']*)'", line)
        if match:
            ps_lines.append(f'Write-Host \'{match.group(1)}\'')
            continue
        
        if re.match(r'^\s*echo\s*$', line):
            ps_lines.append('Write-Host ""')
            continue
        
        # mkdir -p
        match = re.match(r'^\s*mkdir\s+-p\s+(.+)$', line)
        if match:
            path = match.group(1).strip()
            ps_lines.append(f'New-Item -ItemType Directory -Force -Path {path} | Out-Null')
            continue
        
        # rm -rf
        match = re.match(r'^\s*rm\s+-rf\s+(.+)$', line)
        if match:
            path = match.group(1).strip()
            ps_lines.append(f'Remove-Item -Recurse -Force {path} -ErrorAction SilentlyContinue')
            continue
        
        # cp -r
        match = re.match(r'^\s*cp\s+-r\s+(\S+)\s+(.+)$', line)
        if match:
            src = match.group(1)
            dst = match.group(2)
            ps_lines.append(f'Copy-Item -Recurse {src} {dst}')
            continue
        
        # cp (simple copy)
        match = re.match(r'^\s*cp\s+(\S+)\s+(.+)$', line)
        if match:
            src = match.group(1)
            dst = match.group(2)
            ps_lines.append(f'Copy-Item {src} {dst}')
            continue
        
        # if [ -n "$VAR" ]
        match = re.match(r'^\s*if\s*\[\s*-n\s+"\$([^"]+)"\s*\]\s*;\s*then\s*$', line)
        if match:
            ps_lines.append(f'if (${match.group(1)}) {{')
            continue
        
        # if [ -z "$VAR" ]
        match = re.match(r'^\s*if\s*\[\s*-z\s+"\$([^"]+)"\s*\]\s*;\s*then\s*$', line)
        if match:
            ps_lines.append(f'if (-not ${match.group(1)}) {{')
            continue
        
        # if [ -d "path" ]
        match = re.match(r'^\s*if\s*\[\s*-d\s+"([^"]+)"\s*\]\s*;\s*then\s*$', line)
        if match:
            ps_lines.append(f'if (Test-Path -PathType Container "{match.group(1)}") {{')
            continue
        
        # if [ -f "path" ]
        match = re.match(r'^\s*if\s*\[\s*-f\s+"([^"]+)"\s*\]\s*;\s*then\s*$', line)
        if match:
            ps_lines.append(f'if (Test-Path -PathType Leaf "{match.group(1)}") {{')
            continue
        
        # else
        if re.match(r'^\s*else\s*$', line):
            ps_lines.append('} else {')
            continue
        
        # fi
        if re.match(r'^\s*fi\s*$', line):
            ps_lines.append('}')
            continue
        
        # source command
        match = re.match(r'^\s*source\s+"([^"]+)"', line)
        if match:
            file = match.group(1).replace('.sh', '.ps1')
            ps_lines.append(f'. "{file}"')
            continue
        
        match = re.match(r'^\s*source\s+(.+)$', line)
        if match:
            file = match.group(1).strip().replace('.sh', '.ps1')
            ps_lines.append(f'. {file}')
            continue
        
        # Function definition
        match = re.match(r'^([a-z_][a-z0-9_]*)\(\)\s*\{?\s*$', line)
        if match:
            ps_lines.append(f'function {match.group(1)} {{')
            in_function = True
            continue
        
        # Closing brace
        if re.match(r'^\s*\}\s*$', line):
            ps_lines.append('}')
            in_function = False
            continue
        
        # return/exit
        match = re.match(r'^\s*return\s+(\d+)\s*$', line)
        if match:
            ps_lines.append(f'    return {match.group(1)}')
            continue
        
        match = re.match(r'^\s*return\s*$', line)
        if match:
            ps_lines.append('    return')
            continue
        
        match = re.match(r'^\s*exit\s+(\d+)\s*$', line)
        if match:
            ps_lines.append(f'    exit {match.group(1)}')
            continue
        
        # Default: keep line with basic variable conversion
        converted = line.replace('${', '$').replace('}', '')
        ps_lines.append(converted)
    
    return '\n'.join(ps_lines)


def main():
    if len(sys.argv) != 3:
        print("Usage: bash-to-powershell.py <input.sh> <output.ps1>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    # Read bash script
    with open(input_file, 'r', encoding='utf-8') as f:
        bash_content = f.read()
    
    # Convert to PowerShell
    ps_content = (
        f"# PowerShell conversion of {os.path.basename(input_file)}\n"
        f"# Auto-generated by bash-to-powershell.py\n\n"
    )
    ps_content += convert_bash_to_powershell(bash_content)
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    
    # Write PowerShell script
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ps_content)
    
    print(f"Converted {input_file} -> {output_file}")


if __name__ == '__main__':
    main()
