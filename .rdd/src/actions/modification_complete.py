#!/usr/bin/env python3
"""
Mark a modification as complete.

This script marks the current modification as complete, updates the modifications log,
and resets the current-modification-id in the registry.

Usage:
    python modification_complete.py [prompt-id=<id>]

Example:
    python modification_complete.py
    python modification_complete.py prompt-id=P-017
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


def complete_modification(prompt_id=None):
    """
    Mark the current modification as complete for the specified prompt.
    
    Args:
        prompt_id (str, optional): Prompt ID. If None, uses the active prompt.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
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
    
    # Check if there's an active modification
    current_mod_id = target_prompt.get('current-modification-id')
    if current_mod_id is None:
        print(f"ERROR: No active modification for prompt '{prompt_id}'")
        print("REMEDIATION: Create a modification before trying to complete it.")
        return 1
    
    # Find prompt folder
    workdir = Path('.rdd-instance/workdir')
    prompt_folder = find_prompt_folder(workdir, prompt_id, target_prompt.get('prompt-title', ''))
    
    if not prompt_folder.exists():
        print(f"ERROR: Prompt folder not found: {prompt_folder}")
        print("REMEDIATION: Ensure the prompt folder exists in workdir.")
        return 1
    
    # Load modifications log
    modifications_log_file = prompt_folder / "modifications-log.json"
    
    if not modifications_log_file.exists():
        print(f"ERROR: Modifications log not found: {modifications_log_file}")
        print("REMEDIATION: Ensure modifications-log.json exists.")
        return 1
    
    try:
        with open(modifications_log_file, 'r', encoding='utf-8') as f:
            modifications_log = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to read modifications log: {e}")
        return 1
    
    # Find the modification in the log and update it
    modifications = modifications_log.get('modifications', [])
    found = False
    
    for mod in modifications:
        if mod.get('modification-id') == current_mod_id:
            mod['status'] = 'completed'
            mod['completed'] = datetime.now().isoformat()
            found = True
            break
    
    if not found:
        print(f"ERROR: Modification {current_mod_id} not found in modifications log")
        print("REMEDIATION: Check the modifications-log.json file.")
        return 1
    
    # Save modifications log
    try:
        with open(modifications_log_file, 'w', encoding='utf-8') as f:
            json.dump(modifications_log, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR: Failed to write modifications log: {e}")
        return 1
    
    # Reset current-modification-id in registry
    target_prompt['current-modification-id'] = None
    
    # Save the updated registry
    try:
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR: Failed to write work iteration registry: {e}")
        return 1
    
    print(f"SUCCESS: Modification {current_mod_id} marked as complete for prompt '{prompt_id}'")
    return 0


def main():
    """Main entry point for the script."""
    # Parse command line arguments
    prompt_id = None
    
    for arg in sys.argv[1:]:
        if arg.startswith('prompt-id='):
            prompt_id = arg.split('=', 1)[1]
    
    # Complete modification
    exit_code = complete_modification(prompt_id)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
