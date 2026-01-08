#!/usr/bin/env python3
"""
Set implementation-completed flag to true for a prompt.

Usage:
    python prompt_implementation_completed_on.py [prompt-id=<id>]
"""

import json
import os
import sys


def find_active_prompt(prompts):
    for prompt in prompts:
        if prompt.get('state') == 'active':
            return prompt
    return None


def set_implementation_completed(prompt_id=None, value=True):
    registry_path = '.rdd-instance/workdir/work-iteration-registry.json'
    
    if not os.path.exists(registry_path):
        print(f"ERROR: Work iteration registry not found at {registry_path}")
        return 1
    
    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse work iteration registry: {e}")
        return 1
    except Exception as e:
        print(f"ERROR: Failed to read work iteration registry: {e}")
        return 1
    
    prompts = registry.get('prompts', [])
    
    if prompt_id is None:
        target_prompt = find_active_prompt(prompts)
        if target_prompt is None:
            print("ERROR: No active prompt found (state='active')")
            return 1
        prompt_id = target_prompt.get('prompt-id')
    else:
        target_prompt = None
        for prompt in prompts:
            if prompt.get('prompt-id') == prompt_id:
                target_prompt = prompt
                break
        
        if target_prompt is None:
            print(f"ERROR: Prompt '{prompt_id}' not found in work iteration registry")
            return 1
    
    target_prompt['implementation-completed'] = value
    
    try:
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR: Failed to write work iteration registry: {e}")
        return 1
    
    print(f"SUCCESS: implementation-completed set to {value} for prompt '{prompt_id}'")
    return 0


def main():
    prompt_id = None
    for arg in sys.argv[1:]:
        if arg.startswith('prompt-id='):
            prompt_id = arg.split('=', 1)[1]
    
    exit_code = set_implementation_completed(prompt_id, True)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
