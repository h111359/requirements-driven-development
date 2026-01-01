#!/usr/bin/env python3
"""Migration script to remove 'type' and 'parent-id' fields from work-iteration-registry.json.

This script:
1. Loads the work-iteration-registry.json
2. Removes 'type' and 'parent-id' fields from all prompts
3. Saves the updated registry back to the file

This is a one-time migration for P-015.
"""

import json
import sys
from pathlib import Path


def _repo_root() -> Path:
    # This file lives at: <repo>/.rdd/src/actions/
    return Path(__file__).resolve().parents[3]


def main() -> int:
    repo_root = _repo_root()
    registry_path = repo_root / ".rdd-instance" / "workdir" / "work-iteration-registry.json"
    
    if not registry_path.is_file():
        print(f"ERROR: Registry not found: {registry_path}", file=sys.stderr)
        return 1
    
    # Load the registry
    with registry_path.open("r", encoding="utf-8") as f:
        registry = json.load(f)
    
    if not isinstance(registry, dict):
        print(f"ERROR: Registry must be an object", file=sys.stderr)
        return 1
    
    prompts = registry.get("prompts")
    if not isinstance(prompts, list):
        print(f"ERROR: Missing or invalid 'prompts' array", file=sys.stderr)
        return 1
    
    # Track changes
    removed_type_count = 0
    removed_parent_id_count = 0
    
    # Remove type and parent-id from all prompts
    for prompt in prompts:
        if not isinstance(prompt, dict):
            continue
        
        if "type" in prompt:
            del prompt["type"]
            removed_type_count += 1
        
        if "parent-id" in prompt:
            del prompt["parent-id"]
            removed_parent_id_count += 1
    
    # Save the updated registry
    with registry_path.open("w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4)
        f.write("\n")
    
    print(f"Migration completed successfully:")
    print(f"  - Removed 'type' field from {removed_type_count} prompts")
    print(f"  - Removed 'parent-id' field from {removed_parent_id_count} prompts")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
