#!/usr/bin/env python3
"""
Set or update a technical design answer.

This script sets or updates an answer to a technical design question.

Usage:
    python .rdd/src/actions/technical_design_answer_set.py questionId=<id> type=<type> value=<value> [rationale=<text>]

Parameters:
    questionId - The question ID from the schema (required)
    type - Question type: radio, multiselect, text, etc. (required)
    value - The answer value (required)
    rationale - Optional explanation for the answer

Examples:
    python .rdd/src/actions/technical_design_answer_set.py questionId="ProjectScale_OverallScaleCategory" type="radio" value="Enterprise-wide platform"
    python .rdd/src/actions/technical_design_answer_set.py questionId="Frontend_Frameworks" type="multiselect" value="react,typescript" rationale="Modern stack"

Exit codes:
    0 - Success
    1 - Error (validation or I/O)
"""

import json
import os
import sys
from datetime import datetime, timezone

def parse_args(args):
    """Parse command line arguments in key=value format."""
    params = {}
    for arg in args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            params[key] = value
    return params

def load_schema():
    """Load the technical design schema."""
    schema_path = ".rdd/config/technical-design-schema.json"
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(json.dumps({
            "error": "Failed to load schema",
            "details": str(e),
            "recovery": "Ensure .rdd/config/technical-design-schema.json exists"
        }), file=sys.stderr)
        return None

def validate_question_id(schema, question_id):
    """Validate that questionId exists in schema."""
    for category in schema.get('categories', []):
        for group in category.get('groups', []):
            for question in group.get('questions', []):
                if question['id'] == question_id:
                    return question
    return None

def parse_value(value_str, question_type):
    """Parse value string based on question type."""
    if question_type == 'multiselect':
        # Split comma-separated values
        return [v.strip() for v in value_str.split(',') if v.strip()]
    elif question_type in ['text', 'radio', 'dropdown']:
        return value_str
    else:
        return value_str

def main():
    """Set or update a technical design answer."""
    params = parse_args(sys.argv[1:])
    
    # Validate required parameters
    if 'questionId' not in params:
        print(json.dumps({
            "error": "Missing required parameter: questionId",
            "recovery": "Provide questionId=<id> parameter"
        }), file=sys.stderr)
        return 1
    
    if 'type' not in params:
        print(json.dumps({
            "error": "Missing required parameter: type",
            "recovery": "Provide type=<radio|multiselect|text|...> parameter"
        }), file=sys.stderr)
        return 1
    
    if 'value' not in params:
        print(json.dumps({
            "error": "Missing required parameter: value",
            "recovery": "Provide value=<answer> parameter"
        }), file=sys.stderr)
        return 1
    
    question_id = params['questionId']
    question_type = params['type']
    value_str = params['value']
    rationale = params.get('rationale', '')
    
    # Load and validate schema
    schema = load_schema()
    if not schema:
        return 1
    
    question = validate_question_id(schema, question_id)
    if not question:
        print(json.dumps({
            "error": f"Question ID not found in schema: {question_id}",
            "recovery": "Check question ID spelling and schema"
        }), file=sys.stderr)
        return 1
    
    # Parse value
    value = parse_value(value_str, question_type)
    
    # Load current answers
    tech_design_path = ".rdd-instance/specifications/technical-design.json"
    answers = {}
    if os.path.exists(tech_design_path):
        try:
            with open(tech_design_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    answers = json.loads(content)
        except Exception as e:
            print(json.dumps({
                "error": "Failed to load existing answers",
                "details": str(e),
                "recovery": "Fix JSON or delete file"
            }), file=sys.stderr)
            return 1
    
    # Create or update answer
    answers[question_id] = {
        "questionId": question_id,
        "type": question_type,
        "value": value,
        "answeredAt": datetime.now(timezone.utc).isoformat()
    }
    
    if rationale:
        answers[question_id]["rationale"] = rationale
    
    # Write atomically (temp + rename)
    temp_path = tech_design_path + ".tmp"
    try:
        with open(temp_path, 'w', encoding='utf-8') as f:
            json.dump(answers, f, indent=2, ensure_ascii=False)
        
        os.replace(temp_path, tech_design_path)
        
        print(json.dumps({
            "success": True,
            "questionId": question_id,
            "message": "Answer saved successfully"
        }))
        return 0
    
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(json.dumps({
            "error": "Failed to save answer",
            "details": str(e),
            "recovery": "Check file permissions"
        }), file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
