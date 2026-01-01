#!/usr/bin/env python3
"""
Enable analyze mode for a prompt.

This script sets the analyze-enabled flag to true for a specified prompt
in the work iteration registry. If no prompt-id is provided, it defaults
to the currently active prompt (one in 'active' state).

Usage:
    python prompt_analyze_on.py [prompt-id=<id>]

Example:
    python prompt_analyze_on.py prompt-id=P-003
    python prompt_analyze_on.py  # Uses active prompt
"""

import json
import os
import sys


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


def enable_analyze_mode(prompt_id=None):
    """
    Enable analyze mode for the specified prompt.
    
    Args:
        prompt_id (str, optional): Prompt ID to enable analyze for.
                                   If None, uses the active prompt.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Determine registry path
    registry_path = '.rdd-instance/workdir/work-iteration-registry.json'
    
    if not os.path.exists(registry_path):
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
            print("REMEDIATION: Check the prompt ID and try again. Use 'rdd.py prompt list' to see available prompts.")
            return 1
    
    # Validate that the prompt is in active state
    if target_prompt.get('state') != 'active':
        print(f"ERROR: Cannot enable analyze mode for prompt '{prompt_id}' in state '{target_prompt.get('state')}'")
        print("REMEDIATION: Analyze mode can only be enabled for prompts in 'active' state.")
        return 1
    
    # Enforce mutual exclusivity: disable plan mode if enabled
    if target_prompt.get('plan-enabled', False):
        print(f"INFO: Automatically disabling plan mode for prompt '{prompt_id}' (mutual exclusivity)")
        target_prompt['plan-enabled'] = False
    
    # Set analyze-enabled to true
    target_prompt['analyze-enabled'] = True
    
    # Save the updated registry
    try:
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR: Failed to write work iteration registry: {e}")
        return 1
    
    print(f"SUCCESS: Analyze mode enabled for prompt '{prompt_id}'")
    return 0


def main():
    """Main entry point for the script."""
    # Parse command line arguments
    prompt_id = None
    for arg in sys.argv[1:]:
        if arg.startswith('prompt-id='):
            prompt_id = arg.split('=', 1)[1]
    
    # Enable analyze mode
    exit_code = enable_analyze_mode(prompt_id)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
