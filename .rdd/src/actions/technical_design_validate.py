#!/usr/bin/env python3
"""
Validate technical design answers against schema.

This script validates that all answers in technical-design.json reference
valid schema questions and have appropriate value types.

Usage:
    python .rdd/src/actions/technical_design_validate.py

Output:
    JSON object with validation results

Exit codes:
    0 - Valid
    1 - Invalid or error
"""

import json
import os
import sys

def load_schema():
    """Load the technical design schema."""
    schema_path = ".rdd/config/technical-design-schema.json"
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None, f"Failed to load schema: {e}"

def get_all_question_ids(schema):
    """Extract all valid question IDs from schema."""
    question_map = {}
    for category in schema.get('categories', []):
        # Support both flattened structure (categories → questions) and grouped structure (categories → groups → questions)
        # Check direct questions in category (flattened structure)
        for question in category.get('questions', []):
            question_map[question['id']] = question
        # Check questions in groups (legacy grouped structure)
        for group in category.get('groups', []):
            for question in group.get('questions', []):
                question_map[question['id']] = question
    return question_map

def validate_answer(question_id, answer, question_def):
    """Validate a single answer against its question definition."""
    errors = []
    
    # Check type match
    if answer.get('type') != question_def.get('type'):
        errors.append(f"Type mismatch: answer has '{answer.get('type')}', schema expects '{question_def.get('type')}'")
    
    # Validate value type
    value = answer.get('value')
    answer_type = answer.get('type')
    
    if answer_type == 'multiselect':
        if not isinstance(value, list):
            errors.append(f"Multiselect value must be array, got {type(value).__name__}")
    elif answer_type in ['radio', 'text', 'dropdown']:
        if not isinstance(value, str):
            errors.append(f"{answer_type} value must be string, got {type(value).__name__}")
    
    # Check required fields
    if 'questionId' not in answer:
        errors.append("Missing 'questionId' field")
    if 'answeredAt' not in answer:
        errors.append("Missing 'answeredAt' field")
    
    return errors

def main():
    """Validate technical design answers."""
    # Load schema
    result = load_schema()
    if isinstance(result, tuple):
        schema, error = result
        if schema is None:
            print(json.dumps({
                "valid": False,
                "error": error
            }), file=sys.stderr)
            return 1
    else:
        schema = result
    
    # Get all valid questions
    questions = get_all_question_ids(schema)
    
    # Load answers
    tech_design_path = ".rdd-instance/specifications/technical-design.json"
    if not os.path.exists(tech_design_path):
        print(json.dumps({
            "valid": True,
            "message": "No answers file exists, nothing to validate"
        }))
        return 0
    
    try:
        with open(tech_design_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                answers = {}
            else:
                answers = json.loads(content)
    except json.JSONDecodeError as e:
        print(json.dumps({
            "valid": False,
            "error": "Invalid JSON in technical-design.json",
            "details": str(e)
        }), file=sys.stderr)
        return 1
    except Exception as e:
        print(json.dumps({
            "valid": False,
            "error": "Failed to load answers",
            "details": str(e)
        }), file=sys.stderr)
        return 1
    
    # Validate each answer
    validation_errors = []
    
    for question_id, answer in answers.items():
        if question_id not in questions:
            validation_errors.append({
                "questionId": question_id,
                "error": "Question ID not found in schema"
            })
            continue
        
        question_def = questions[question_id]
        errors = validate_answer(question_id, answer, question_def)
        
        if errors:
            validation_errors.append({
                "questionId": question_id,
                "errors": errors
            })
    
    # Output results
    if validation_errors:
        print(json.dumps({
            "valid": False,
            "errorCount": len(validation_errors),
            "errors": validation_errors
        }, indent=2), file=sys.stderr)
        return 1
    else:
        print(json.dumps({
            "valid": True,
            "message": f"All {len(answers)} answers are valid"
        }))
        return 0

if __name__ == "__main__":
    sys.exit(main())
