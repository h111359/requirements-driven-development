#!/usr/bin/env python3
"""
Enable plan mode for a prompt.

This script sets the plan-enabled flag to true for a specified prompt
in the work iteration registry. If no prompt-id is provided, it defaults
to the currently active prompt (one in 'planned' or 'in-progress' state).

When plan mode is enabled, analyze mode is automatically disabled to enforce
mutual exclusivity.

Usage:
    python prompt_plan_on.py [prompt-id=<id>]

Example:
    python prompt_plan_on.py prompt-id=P-003
    python prompt_plan_on.py  # Uses active prompt
"""

import json
import os
import sys


def find_active_prompt(prompts):
    """
    Find the active prompt (state = 'planned' or 'in-progress').
    
    Args:
        prompts (list): List of prompt metadata objects
        
    Returns:
        dict: The active prompt object, or None if not found
    """
    for prompt in prompts:
        if prompt.get('state') in ['planned', 'in-progress']:
            return prompt
    return None


def enable_plan_mode(prompt_id=None):
    """
    Enable plan mode for the specified prompt.
    
    Args:
        prompt_id (str, optional): Prompt ID to enable plan for.
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
            print("ERROR: No active prompt found (state='planned' or 'in-progress')")
            print("REMEDIATION: Create a prompt or set an existing prompt to 'planned' or 'in-progress' state.")
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
    
    # Validate that the prompt is not completed
    if target_prompt.get('state') == 'completed':
        print(f"ERROR: Cannot enable plan mode for completed prompt '{prompt_id}'")
        print("REMEDIATION: Plan mode can only be enabled for prompts in 'draft', 'planned', or 'in-progress' state.")
        return 1
    
    # Enforce mutual exclusivity: disable analyze mode if enabled
    if target_prompt.get('analyze-enabled', False):
        print(f"INFO: Automatically disabling analyze mode for prompt '{prompt_id}' (mutual exclusivity)")
        target_prompt['analyze-enabled'] = False
    
    # Set plan-enabled to true
    target_prompt['plan-enabled'] = True
    
    # Save the updated registry
    try:
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR: Failed to save work iteration registry: {e}")
        return 1
    
    print(f"SUCCESS: Plan mode enabled for prompt '{prompt_id}'")
    return 0


def main():
    """Main entry point."""
    # Parse command-line arguments
    prompt_id = None
    for arg in sys.argv[1:]:
        if arg.startswith('prompt-id='):
            prompt_id = arg.split('=', 1)[1]
    
    # Enable plan mode
    exit_code = enable_plan_mode(prompt_id)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
