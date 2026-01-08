#!/usr/bin/env python3
"""Add requirement for Config page."""
import subprocess
import sys
from pathlib import Path

repo_root = Path(__file__).parent
script_path = repo_root / ".rdd" / "src" / "actions" / "requirement_ur_create.py"

result = subprocess.run(
    [sys.executable, str(script_path), 
     'text=The Web UI shall provide a Config page enabling users to view and modify instance configuration settings including the git-enabled flag through an intuitive interface with toggle switches'],
    capture_output=True,
    text=True,
    cwd=repo_root
)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)
