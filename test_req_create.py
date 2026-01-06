#!/usr/bin/env python3
"""Test script to verify Config page implementation."""
import sys
import os

# Add the repo root to path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(repo_root, '.rdd', 'src', 'actions'))

# Import and run the requirement creation
from requirement_ur_create import main as create_ur

# Create the requirement
result = create_ur([
    'text=The Web UI shall provide a Config page enabling users to view and modify instance configuration settings including the git-enabled flag through an intuitive interface with toggle switches'
])

print(f"Requirement creation result: {result}")
