"""
Test script for OR logic in conditional visibility
Tests the isQuestionVisible function logic with various scenarios
"""

# Mock techDesignAnswers
tech_design_answers = {}

def is_question_visible(question):
    """
    Check if a question should be visible based on visibleWhen rules
    
    Supports both string and array formats for rule['equals']:
    - String: exact match (e.g., "equals": "Cloud")
    - Array: OR logic - answer must match ANY value (e.g., "equals": ["Cloud", "Hybrid"])
    
    For multiselect answers, uses ANY match logic:
    - If equals is ["A", "B"] and answer is ["B", "C"], rule matches (B is in both)
    """
    visible_when = question.get('visibleWhen', [])
    
    if not visible_when:
        return True
    
    # All rules must be satisfied (AND logic between rules)
    for rule in visible_when:
        question_id = rule.get('questionId')
        dependent_answer = tech_design_answers.get(question_id)
        
        if not dependent_answer:
            return False
        
        value = dependent_answer.get('value')
        equals = rule.get('equals')
        
        # Support both string and array formats for rule.equals
        equals_values = equals if isinstance(equals, list) else [equals]
        
        # Check if answer matches ANY of the equals values (OR logic)
        rule_matches = False
        
        if isinstance(value, list):
            # Multiselect answer: check if ANY equals value is in the answer array
            for equals_value in equals_values:
                if equals_value in value:
                    rule_matches = True
                    break
        else:
            # Single value answer (radio/text): check if value matches ANY equals value
            rule_matches = value in equals_values
        
        if not rule_matches:
            return False
    
    return True

# Test cases
def run_tests():
    global tech_design_answers
    print('=== Testing OR Logic in Conditional Visibility ===\n')
    
    passed = 0
    failed = 0
    
    # Test 1: String equals with single value answer (backward compatibility)
    tech_design_answers = {'Q1': {'value': 'Cloud'}}
    test1 = is_question_visible({'visibleWhen': [{'questionId': 'Q1', 'equals': 'Cloud'}]})
    print(f'Test 1 - String equals with matching single value: {"✓ PASS" if test1 else "✗ FAIL"}')
    passed += 1 if test1 else 0
    failed += 0 if test1 else 1
    
    # Test 2: String equals with non-matching single value
    tech_design_answers = {'Q1': {'value': 'OnPrem'}}
    test2 = not is_question_visible({'visibleWhen': [{'questionId': 'Q1', 'equals': 'Cloud'}]})
    print(f'Test 2 - String equals with non-matching value: {"✓ PASS" if test2 else "✗ FAIL"}')
    passed += 1 if test2 else 0
    failed += 0 if test2 else 1
    
    # Test 3: Array equals with matching single value (OR logic)
    tech_design_answers = {'Q1': {'value': 'Cloud'}}
    test3 = is_question_visible({'visibleWhen': [{'questionId': 'Q1', 'equals': ['Cloud', 'Hybrid']}]})
    print(f'Test 3 - Array equals ["Cloud", "Hybrid"] with value "Cloud": {"✓ PASS" if test3 else "✗ FAIL"}')
    passed += 1 if test3 else 0
    failed += 0 if test3 else 1
    
    # Test 4: Array equals with second matching value (OR logic)
    tech_design_answers = {'Q1': {'value': 'Hybrid'}}
    test4 = is_question_visible({'visibleWhen': [{'questionId': 'Q1', 'equals': ['Cloud', 'Hybrid']}]})
    print(f'Test 4 - Array equals ["Cloud", "Hybrid"] with value "Hybrid": {"✓ PASS" if test4 else "✗ FAIL"}')
    passed += 1 if test4 else 0
    failed += 0 if test4 else 1
    
    # Test 5: Array equals with non-matching value
    tech_design_answers = {'Q1': {'value': 'OnPrem'}}
    test5 = not is_question_visible({'visibleWhen': [{'questionId': 'Q1', 'equals': ['Cloud', 'Hybrid']}]})
    print(f'Test 5 - Array equals ["Cloud", "Hybrid"] with value "OnPrem": {"✓ PASS" if test5 else "✗ FAIL"}')
    passed += 1 if test5 else 0
    failed += 0 if test5 else 1
    
    # Test 6: Multiselect answer with string equals
    tech_design_answers = {'Q1': {'value': ['Cloud', 'OnPrem']}}
    test6 = is_question_visible({'visibleWhen': [{'questionId': 'Q1', 'equals': 'Cloud'}]})
    print(f'Test 6 - String equals "Cloud" with multiselect ["Cloud", "OnPrem"]: {"✓ PASS" if test6 else "✗ FAIL"}')
    passed += 1 if test6 else 0
    failed += 0 if test6 else 1
    
    # Test 7: Multiselect answer with array equals (ANY match)
    tech_design_answers = {'Q1': {'value': ['OnPrem', 'Edge']}}
    test7 = is_question_visible({'visibleWhen': [{'questionId': 'Q1', 'equals': ['Cloud', 'OnPrem', 'Hybrid']}]})
    print(f'Test 7 - Array equals ["Cloud", "OnPrem", "Hybrid"] with multiselect ["OnPrem", "Edge"]: {"✓ PASS" if test7 else "✗ FAIL"}')
    passed += 1 if test7 else 0
    failed += 0 if test7 else 1
    
    # Test 8: Multiselect answer with array equals (no match)
    tech_design_answers = {'Q1': {'value': ['Edge', 'Embedded']}}
    test8 = not is_question_visible({'visibleWhen': [{'questionId': 'Q1', 'equals': ['Cloud', 'Hybrid']}]})
    print(f'Test 8 - Array equals ["Cloud", "Hybrid"] with multiselect ["Edge", "Embedded"]: {"✓ PASS" if test8 else "✗ FAIL"}')
    passed += 1 if test8 else 0
    failed += 0 if test8 else 1
    
    # Test 9: Multiple rules with AND logic (both must match)
    tech_design_answers = {
        'Q1': {'value': 'Cloud'},
        'Q2': {'value': 'Enterprise'}
    }
    test9 = is_question_visible({
        'visibleWhen': [
            {'questionId': 'Q1', 'equals': ['Cloud', 'Hybrid']},
            {'questionId': 'Q2', 'equals': 'Enterprise'}
        ]
    })
    print(f'Test 9 - Multiple rules (both match): {"✓ PASS" if test9 else "✗ FAIL"}')
    passed += 1 if test9 else 0
    failed += 0 if test9 else 1
    
    # Test 10: Multiple rules with AND logic (one fails)
    tech_design_answers = {
        'Q1': {'value': 'OnPrem'},
        'Q2': {'value': 'Enterprise'}
    }
    test10 = not is_question_visible({
        'visibleWhen': [
            {'questionId': 'Q1', 'equals': ['Cloud', 'Hybrid']},
            {'questionId': 'Q2', 'equals': 'Enterprise'}
        ]
    })
    print(f'Test 10 - Multiple rules (one fails): {"✓ PASS" if test10 else "✗ FAIL"}')
    passed += 1 if test10 else 0
    failed += 0 if test10 else 1
    
    # Test 11: No visibleWhen (always visible)
    test11 = is_question_visible({})
    print(f'Test 11 - No visibleWhen (always visible): {"✓ PASS" if test11 else "✗ FAIL"}')
    passed += 1 if test11 else 0
    failed += 0 if test11 else 1
    
    # Test 12: Missing dependent answer
    tech_design_answers = {}
    test12 = not is_question_visible({'visibleWhen': [{'questionId': 'Q1', 'equals': 'Cloud'}]})
    print(f'Test 12 - Missing dependent answer (hidden): {"✓ PASS" if test12 else "✗ FAIL"}')
    passed += 1 if test12 else 0
    failed += 0 if test12 else 1
    
    print(f'\n=== Test Results ===')
    print(f'Passed: {passed}')
    print(f'Failed: {failed}')
    print(f'Total: {passed + failed}')
    
    return failed == 0

# Run tests
if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
