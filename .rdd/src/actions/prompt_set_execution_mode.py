#!/usr/bin/env python3
"""
Set execution-mode for a prompt.

This script sets the execution-mode attribute for a specified prompt
in the work iteration registry. If no prompt-id is provided, it defaults
to the currently active prompt (one in 'active' state).

Usage:
    python prompt_set_execution_mode.py mode=<mode> [prompt-id=<id>]

Modes:
    no-action    - No execution action
    analyze      - Generate questionnaire
    plan         - Generate plan
    implement    - Execute implementation
    modification - Execute a modification (only available after implementation-completed=true)

Example:
    python prompt_set_execution_mode.py mode=analyze
    python prompt_set_execution_mode.py mode=plan prompt-id=P-003
"""

import json
import os
import sys


VALID_MODES = ['no-action', 'analyze', 'plan', 'implement', 'modification']


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


def set_execution_mode(mode, prompt_id=None):
    """
    Set execution-mode for the specified prompt.
    
    Args:
        mode (str): The execution mode to set
        prompt_id (str, optional): Prompt ID. If None, uses the active prompt.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Validate mode
    if mode not in VALID_MODES:
        print(f"ERROR: Invalid mode '{mode}'. Valid modes are: {', '.join(VALID_MODES)}")
        return 1
    
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
            print("REMEDIATION: Check the prompt ID and try again.")
            return 1
    
    # Set execution-mode
    target_prompt['execution-mode'] = mode
    
    # Save the updated registry
    try:
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR: Failed to write work iteration registry: {e}")
        return 1
    
    print(f"SUCCESS: execution-mode set to '{mode}' for prompt '{prompt_id}'")
    return 0


def main():
    """Main entry point for the script."""
    # Parse command line arguments
    mode = None
    prompt_id = None
    
    for arg in sys.argv[1:]:
        if arg.startswith('mode='):
            mode = arg.split('=', 1)[1]
        elif arg.startswith('prompt-id='):
            prompt_id = arg.split('=', 1)[1]
    
    if mode is None:
        print("ERROR: mode parameter is required")
        print("Usage: python prompt_set_execution_mode.py mode=<mode> [prompt-id=<id>]")
        print(f"Valid modes: {', '.join(VALID_MODES)}")
        sys.exit(1)
    
    # Set execution mode
    exit_code = set_execution_mode(mode, prompt_id)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
