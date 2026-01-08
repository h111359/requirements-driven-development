#!/usr/bin/env python3
"""
Set questionnaire-generated flag to true for a prompt.

This script sets the questionnaire-generated flag to true for a specified prompt
in the work iteration registry. If no prompt-id is provided, it defaults
to the currently active prompt (one in 'active' state).

Usage:
    python prompt_questionnaire_generated_on.py [prompt-id=<id>]

Example:
    python prompt_questionnaire_generated_on.py prompt-id=P-003
    python prompt_questionnaire_generated_on.py  # Uses active prompt
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


def set_questionnaire_generated(prompt_id=None, value=True):
    """
    Set questionnaire-generated flag for the specified prompt.
    
    Args:
        prompt_id (str, optional): Prompt ID. If None, uses the active prompt.
        value (bool): The value to set (default: True)
    
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
            print("REMEDIATION: Check the prompt ID and try again.")
            return 1
    
    # Set questionnaire-generated to the specified value
    target_prompt['questionnaire-generated'] = value
    
    # Save the updated registry
    try:
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR: Failed to write work iteration registry: {e}")
        return 1
    
    print(f"SUCCESS: questionnaire-generated set to {value} for prompt '{prompt_id}'")
    return 0


def main():
    """Main entry point for the script."""
    # Parse command line arguments
    prompt_id = None
    for arg in sys.argv[1:]:
        if arg.startswith('prompt-id='):
            prompt_id = arg.split('=', 1)[1]
    
    # Set questionnaire-generated flag
    exit_code = set_questionnaire_generated(prompt_id, True)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
