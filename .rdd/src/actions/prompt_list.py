#!/usr/bin/env python3
"""List all prompts in the active work iteration.

This script displays all prompts from the work iteration registry with their
current state and metadata.

Usage:
  prompt_list.py

Output:
  Prints a formatted table of all prompts to stdout.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def _repo_root() -> Path:
    """Get the repository root directory.
    
    Returns:
        Path: Absolute path to the repository root.
    """
    # This file lives at: <repo>/.rdd/src/actions/prompt_list.py
    return Path(__file__).resolve().parents[3]


def _registry_path() -> Path:
    """Get the path to the work iteration registry file.
    
    Returns:
        Path: Absolute path to work-iteration-registry.json.
    """
    return _repo_root() / ".rdd-instance" / "workdir" / "work-iteration-registry.json"


def _load_registry() -> Dict[str, Any]:
    """Load the work iteration registry.
    
    Returns:
        Registry data as a dictionary.
        
    Raises:
        SystemExit: If registry file not found or invalid.
    """
    registry_file = _registry_path()
    
    if not registry_file.exists():
        print(f"Error: Registry file not found: {registry_file}", file=sys.stderr)
        print(f"Remediation: Initialize a work iteration using 'workdir new-setup'", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(registry_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in registry file: {e}", file=sys.stderr)
        print(f"Remediation: Check registry file format at {registry_file}", file=sys.stderr)
        sys.exit(1)


def _format_prompt_table(prompts: List[Dict[str, Any]]) -> None:
    """Format and print prompts as a table.
    
    Args:
        prompts: List of prompt dictionaries.
    """
    if not prompts:
        print("No prompts found in registry.")
        return
    
    # Calculate column widths
    id_width = max(len(p.get("prompt-id", "")) for p in prompts)
    id_width = max(id_width, len("ID"))
    
    title_width = max(len(p.get("title", p.get("prompt-title", ""))) for p in prompts)
    title_width = max(title_width, len("Title"))
    
    state_width = max(len(p.get("state", "")) for p in prompts)
    state_width = max(state_width, len("State"))
    
    type_width = max(len(p.get("type", "")) for p in prompts)
    type_width = max(type_width, len("Type"))
    
    # Print header
    header = f"{'ID':<{id_width}}  {'Title':<{title_width}}  {'State':<{state_width}}  {'Type':<{type_width}}"
    print(header)
    print("=" * len(header))
    
    # Print rows
    for p in prompts:
        prompt_id = p.get("prompt-id", "")
        title = p.get("title", p.get("prompt-title", ""))
        state = p.get("state", "")
        ptype = p.get("type", "")
        
        print(f"{prompt_id:<{id_width}}  {title:<{title_width}}  {state:<{state_width}}  {ptype:<{type_width}}")


def main() -> int:
    """Main entry point for prompt list command.
    
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    try:
        registry = _load_registry()
        prompts = registry.get("prompts", [])
        
        print()
        print(f"Work Iteration: {registry.get('iteration-name', 'Unknown')} ({registry.get('iteration-id', 'Unknown')})")
        print()
        
        _format_prompt_table(prompts)
        print()
        
        return 0
    
    except Exception as e:
        print(f"Error: Unexpected error listing prompts: {e}", file=sys.stderr)
        print(f"Remediation: Check system logs and registry file integrity", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
