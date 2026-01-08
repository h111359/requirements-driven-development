#!/usr/bin/env python3
"""Script to execute the completion commands in sequence."""
import subprocess
import sys
from pathlib import Path

repo_root = Path(__file__).parent

commands = [
    [sys.executable, ".rdd/src/actions/prompt_set_executed_on.py"],
    [sys.executable, ".rdd/src/actions/prompt_implementation_completed_on.py"],
    [sys.executable, ".rdd/src/actions/prompt_set_execution_mode.py", "mode=no-action"]
]

for cmd in commands:
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)
    print(f"STDOUT: {result.stdout}")
    if result.stderr:
        print(f"STDERR: {result.stderr}")
    print(f"Return code: {result.returncode}\n")
    
    if result.returncode != 0:
        print("ERROR: Command failed!")
        sys.exit(1)

print("All completion commands executed successfully!")
