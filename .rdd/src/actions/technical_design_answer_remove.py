#!/usr/bin/env python3
"""
Remove a technical design answer.

This script removes an answer to a technical design question.

Usage:
    python .rdd/src/actions/technical_design_answer_remove.py questionId=<id>

Parameters:
    questionId - The question ID to remove (required)

Examples:
    python .rdd/src/actions/technical_design_answer_remove.py questionId="ProjectScale_OverallScaleCategory"

Exit codes:
    0 - Success
    1 - Error
"""

import json
import os
import sys

def parse_args(args):
    """Parse command line arguments in key=value format."""
    params = {}
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            params[key] = value
    return params

def main():
    """Remove a technical design answer."""
    params = parse_args(sys.argv[1:])
    
    # Validate required parameter
    if 'questionId' not in params:
        print(json.dumps({
            "error": "Missing required parameter: questionId",
            "recovery": "Provide questionId=<id> parameter"
        }), file=sys.stderr)
        return 1
    
    question_id = params['questionId']
    tech_design_path = ".rdd-instance/specifications/technical-design.json"
    
    # Load current answers
    if not os.path.exists(tech_design_path):
        print(json.dumps({
            "success": True,
            "message": "No answers file exists, nothing to remove"
        }))
        return 0
    
    try:
        with open(tech_design_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                answers = {}
            else:
                answers = json.loads(content)
    except Exception as e:
        print(json.dumps({
            "error": "Failed to load existing answers",
            "details": str(e),
            "recovery": "Fix JSON or delete file"
        }), file=sys.stderr)
        return 1
    
    # Remove answer if exists
    if question_id in answers:
        del answers[question_id]
        
        # Write atomically
        temp_path = tech_design_path + ".tmp"
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(answers, f, indent=2, ensure_ascii=False)
            
            os.replace(temp_path, tech_design_path)
            
            print(json.dumps({
                "success": True,
                "questionId": question_id,
                "message": "Answer removed successfully"
            }))
            return 0
        
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            print(json.dumps({
                "error": "Failed to save changes",
                "details": str(e),
                "recovery": "Check file permissions"
            }), file=sys.stderr)
            return 1
    else:
        print(json.dumps({
            "success": True,
            "message": f"Question {question_id} not found in answers, nothing to remove"
        }))
        return 0

if __name__ == "__main__":
    sys.exit(main())
