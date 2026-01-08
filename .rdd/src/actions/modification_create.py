#!/usr/bin/env python3
"""
Create a new modification for a prompt.

This script creates a new modification for a prompt that has completed implementation.
It creates the modification file, updates the registry, and sets up the modifications log.

Usage:
    python modification_create.py description="<modification description>" [prompt-id=<id>]

Example:
    python modification_create.py description="Fix typo in error message"
    python modification_create.py description="Add validation check" prompt-id=P-017
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime


def find_active_prompt(prompts):
    """
    Find the active prompt (state = 'active').
    
    Args:
        prompts (list): List of prompt metadata objects
        
    Returns:
        dict: The active prompt object, or None if not found
    """
    for prompt in prompts:
        if prompt.get('state') == 'active':
            return prompt
    return None


def find_prompt_folder(workdir, prompt_id, prompt_title):
    """
    Find the prompt folder in workdir.
    
    Args:
        workdir (Path): Path to workdir
        prompt_id (str): Prompt ID
        prompt_title (str): Prompt title
        
    Returns:
        Path: Path to prompt folder
    """
    # Expected format: P-XXX_<title>
    folder_prefix = f"{prompt_id}_"
    
    for item in workdir.iterdir():
        if item.is_dir() and item.name.startswith(folder_prefix):
            return item
    
    # If not found, construct the expected name
    return workdir / f"{prompt_id}_{prompt_title}"


def create_modification(description, prompt_id=None):
    """
    Create a new modification for the specified prompt.
    
    Args:
        description (str): The modification description
        prompt_id (str, optional): Prompt ID. If None, uses the active prompt.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    if not description or not description.strip():
        print("ERROR: description parameter is required and cannot be empty")
        return 1
    
    description = description.strip()
    
    # Determine registry path
    registry_path = Path('.rdd-instance/workdir/work-iteration-registry.json')
    
    if not registry_path.exists():
        print(f"ERROR: Work iteration registry not found at {registry_path}")
        print("REMEDIATION: Ensure you are in the repository root and a work iteration has been created.")
        return 1
    
    # Load the registry
    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse work iteration registry: {e}")
        print("REMEDIATION: Check that the registry file is valid JSON.")
        return 1
    except Exception as e:
        print(f"ERROR: Failed to read work iteration registry: {e}")
        return 1
    
    prompts = registry.get('prompts', [])
    
    # Determine which prompt to update
    if prompt_id is None:
        # Find active prompt
        target_prompt = find_active_prompt(prompts)
        if target_prompt is None:
            print("ERROR: No active prompt found (state='active')")
            print("REMEDIATION: Create a prompt or set an existing prompt to 'active' state.")
            return 1
        prompt_id = target_prompt.get('prompt-id')
    else:
        # Find the specified prompt
        target_prompt = None
        for prompt in prompts:
            if prompt.get('prompt-id') == prompt_id:
                target_prompt = prompt
                break
        
        if target_prompt is None:
            print(f"ERROR: Prompt '{prompt_id}' not found in work iteration registry")
            print("REMEDIATION: Check the prompt ID and try again.")
            return 1
    
    # Check that implementation is completed
    if not target_prompt.get('implementation-completed', False):
        print(f"ERROR: Prompt '{prompt_id}' has not completed implementation")
        print("REMEDIATION: Complete the implementation before creating modifications.")
        return 1
    
    # Initialize modifications tracking fields if needed
    if 'modifications-count' not in target_prompt:
        target_prompt['modifications-count'] = 0
    
    if 'current-modification-id' not in target_prompt:
        target_prompt['current-modification-id'] = None
    
    # Check if there's already an active modification
    if target_prompt.get('current-modification-id') is not None:
        print(f"ERROR: Prompt '{prompt_id}' already has an active modification: {target_prompt['current-modification-id']}")
        print("REMEDIATION: Complete the current modification before creating a new one.")
        return 1
    
    # Generate new modification ID
    target_prompt['modifications-count'] += 1
    modification_id = f"{target_prompt['modifications-count']:03d}"
    target_prompt['current-modification-id'] = modification_id
    
    # Find prompt folder
    workdir = Path('.rdd-instance/workdir')
    prompt_folder = find_prompt_folder(workdir, prompt_id, target_prompt.get('prompt-title', ''))
    
    if not prompt_folder.exists():
        print(f"ERROR: Prompt folder not found: {prompt_folder}")
        print("REMEDIATION: Ensure the prompt folder exists in workdir.")
        return 1
    
    # Create modification file
    modification_file = prompt_folder / f"modification-{modification_id}.md"
    try:
        with open(modification_file, 'w', encoding='utf-8') as f:
            f.write(description)
    except Exception as e:
        print(f"ERROR: Failed to create modification file: {e}")
        return 1
    
    # Create modification implementation file (empty)
    modification_impl_file = prompt_folder / f"modification-{modification_id}-implementation.md"
    try:
        with open(modification_impl_file, 'w', encoding='utf-8') as f:
            f.write("")
    except Exception as e:
        print(f"ERROR: Failed to create modification implementation file: {e}")
        return 1
    
    # Create or update modifications-log.json
    modifications_log_file = prompt_folder / "modifications-log.json"
    
    if modifications_log_file.exists():
        try:
            with open(modifications_log_file, 'r', encoding='utf-8') as f:
                modifications_log = json.load(f)
        except Exception as e:
            print(f"ERROR: Failed to read modifications log: {e}")
            return 1
    else:
        modifications_log = {
            "prompt-id": prompt_id,
            "modifications": []
        }
    
    # Add new modification entry
    timestamp = datetime.now().isoformat()
    modifications_log['modifications'].append({
        "modification-id": modification_id,
        "created": timestamp,
        "status": "in-progress",
        "completed": None
    })
    
    # Save modifications log
    try:
        with open(modifications_log_file, 'w', encoding='utf-8') as f:
            json.dump(modifications_log, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR: Failed to write modifications log: {e}")
        return 1
    
    # Save the updated registry
    try:
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR: Failed to write work iteration registry: {e}")
        return 1
    
    print(f"SUCCESS: Modification {modification_id} created for prompt '{prompt_id}'")
    print(f"Modification file: {modification_file}")
    print(f"Implementation file: {modification_impl_file}")
    print(f"Use 'python .rdd/src/actions/prompt_set_execution_mode.py mode=modification' to execute the modification")
    return 0


def main():
    """Main entry point for the script."""
    # Parse command line arguments
    description = None
    prompt_id = None
    
    for arg in sys.argv[1:]:
        if arg.startswith('description='):
            description = arg.split('=', 1)[1]
        elif arg.startswith('prompt-id='):
            prompt_id = arg.split('=', 1)[1]
    
    if description is None:
        print("ERROR: description parameter is required")
        print("Usage: python modification_create.py description=\"<modification description>\" [prompt-id=<id>]")
        sys.exit(1)
    
    # Create modification
    exit_code = create_modification(description, prompt_id)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
