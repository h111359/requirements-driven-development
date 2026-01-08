#!/usr/bin/env python3
"""
Delete questionnaire file and reset questionnaire flags for the active prompt.

This script deletes the questionnaire.json (or questionnaire.md) file for the 
currently active prompt and resets both questionnaire-generated and 
questionnaire-answered flags to false, as if the questionnaire was never executed.

Usage:
    python prompt_questionnaire_delete.py

Note: This script only works with the active prompt (no prompt-id parameter).
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


def delete_questionnaire():
    """
    Delete questionnaire file and reset flags for the active prompt.
    
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
    
    # Find active prompt
    target_prompt = find_active_prompt(prompts)
    if target_prompt is None:
        print("ERROR: No active prompt found (state='active')")
        print("REMEDIATION: Create a prompt or set an existing prompt to 'active' state.")
        return 1
    
    prompt_id = target_prompt.get('prompt-id')
    prompt_title = target_prompt.get('prompt-title', '')
    
    # Construct the prompt folder path
    prompt_folder = f".rdd-instance/workdir/{prompt_id}_{prompt_title}"
    
    if not os.path.exists(prompt_folder):
        print(f"ERROR: Prompt folder not found at {prompt_folder}")
        print("REMEDIATION: Ensure the prompt folder exists.")
        return 1
    
    # Check for both possible questionnaire file formats
    questionnaire_json = os.path.join(prompt_folder, "questionnaire.json")
    questionnaire_md = os.path.join(prompt_folder, "questionnaire.md")
    
    file_deleted = False
    
    # Delete questionnaire.json if it exists
    if os.path.exists(questionnaire_json):
        try:
            os.remove(questionnaire_json)
            print(f"SUCCESS: Deleted {questionnaire_json}")
            file_deleted = True
        except Exception as e:
            print(f"ERROR: Failed to delete {questionnaire_json}: {e}")
            print("REMEDIATION: Check file permissions and try again.")
            return 1
    
    # Delete questionnaire.md if it exists
    if os.path.exists(questionnaire_md):
        try:
            os.remove(questionnaire_md)
            print(f"SUCCESS: Deleted {questionnaire_md}")
            file_deleted = True
        except Exception as e:
            print(f"ERROR: Failed to delete {questionnaire_md}: {e}")
            print("REMEDIATION: Check file permissions and try again.")
            return 1
    
    if not file_deleted:
        print(f"WARNING: No questionnaire file found to delete in {prompt_folder}")
        # Continue to reset flags anyway in case of inconsistent state
    
    # Reset both questionnaire-generated and questionnaire-answered flags
    target_prompt['questionnaire-generated'] = False
    target_prompt['questionnaire-answered'] = False
    
    # Save the updated registry
    try:
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR: Failed to write work iteration registry: {e}")
        print("REMEDIATION: Check file permissions and try again.")
        return 1
    
    print(f"SUCCESS: Reset questionnaire-generated and questionnaire-answered flags to false for prompt '{prompt_id}'")
    return 0


def main():
    exit_code = delete_questionnaire()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
