#!/usr/bin/env python3
"""
List all modifications for a prompt.

This script lists all modifications for a prompt by reading the modifications-log.json file.

Usage:
    python modification_list.py [prompt-id=<id>]

Example:
    python modification_list.py
    python modification_list.py prompt-id=P-017
"""

import json
import os
import sys
from pathlib import Path


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


def list_modifications(prompt_id=None):
    """
    List all modifications for the specified prompt.
    
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
    
    # Determine which prompt to use
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
    
    # Find prompt folder
    workdir = Path('.rdd-instance/workdir')
    prompt_folder = find_prompt_folder(workdir, prompt_id, target_prompt.get('prompt-title', ''))
    
    if not prompt_folder.exists():
        print(f"ERROR: Prompt folder not found: {prompt_folder}")
        print("REMEDIATION: Ensure the prompt folder exists in workdir.")
        return 1
    
    # Check for modifications log
    modifications_log_file = prompt_folder / "modifications-log.json"
    
    if not modifications_log_file.exists():
        print(f"No modifications found for prompt '{prompt_id}'")
        return 0
    
    # Load modifications log
    try:
        with open(modifications_log_file, 'r', encoding='utf-8') as f:
            modifications_log = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to read modifications log: {e}")
        return 1
    
    modifications = modifications_log.get('modifications', [])
    
    if not modifications:
        print(f"No modifications found for prompt '{prompt_id}'")
        return 0
    
    # Print modifications
    print(f"Modifications for prompt '{prompt_id}':")
    print("-" * 80)
    
    for mod in modifications:
        mod_id = mod.get('modification-id')
        created = mod.get('created', 'N/A')
        status = mod.get('status', 'unknown')
        completed = mod.get('completed', 'N/A')
        
        print(f"Modification ID: {mod_id}")
        print(f"  Status:    {status}")
        print(f"  Created:   {created}")
        print(f"  Completed: {completed}")
        
        # Try to read description from modification file
        mod_file = prompt_folder / f"modification-{mod_id}.md"
        if mod_file.exists():
            try:
                description = mod_file.read_text(encoding='utf-8').strip()
                # Truncate if too long
                if len(description) > 100:
                    description = description[:97] + "..."
                print(f"  Description: {description}")
            except Exception:
                pass
        
        print("-" * 80)
    
    # Print summary from registry
    current_mod_id = target_prompt.get('current-modification-id')
    mod_count = target_prompt.get('modifications-count', 0)
    
    print(f"\nSummary:")
    print(f"  Total modifications: {mod_count}")
    print(f"  Current modification ID: {current_mod_id if current_mod_id else 'None'}")
    
    return 0


def main():
    """Main entry point for the script."""
    # Parse command line arguments
    prompt_id = None
    
    for arg in sys.argv[1:]:
        if arg.startswith('prompt-id='):
            prompt_id = arg.split('=', 1)[1]
    
    # List modifications
    exit_code = list_modifications(prompt_id)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
