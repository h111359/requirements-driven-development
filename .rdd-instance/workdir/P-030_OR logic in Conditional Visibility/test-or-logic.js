/**
 * Test script for OR logic in conditional visibility
 * Tests the isQuestionVisible function with various scenarios
 */

// Mock techDesignAnswers
let techDesignAnswers = {};

/**
 * Check if a question should be visible based on visibleWhen rules
 * 
 * Supports both string and array formats for rule.equals:
 * - String: exact match (e.g., "equals": "Cloud")
 * - Array: OR logic - answer must match ANY value (e.g., "equals": ["Cloud", "Hybrid"])
 * 
 * For multiselect answers, uses ANY match logic:
 * - If equals is ["A", "B"] and answer is ["B", "C"], rule matches (B is in both)
 */
function isQuestionVisible(question) {
    if (!question.visibleWhen || question.visibleWhen.length === 0) {
        return true;
    }
    
    // All rules must be satisfied (AND logic between rules)
    for (const rule of question.visibleWhen) {
        const dependentAnswer = techDesignAnswers[rule.questionId];
        if (!dependentAnswer) {
            return false;
        }
        
        const value = dependentAnswer.value;
        
        // Support both string and array formats for rule.equals
        const equalsValues = Array.isArray(rule.equals) ? rule.equals : [rule.equals];
        
        // Check if answer matches ANY of the equals values (OR logic)
        let ruleMatches = false;
        
        if (Array.isArray(value)) {
            // Multiselect answer: check if ANY equals value is in the answer array
            for (const equalsValue of equalsValues) {
                if (value.includes(equalsValue)) {
                    ruleMatches = true;
                    break;
                }
            }
        } else {
            // Single value answer (radio/text): check if value matches ANY equals value
            ruleMatches = equalsValues.includes(value);
        }
        
        if (!ruleMatches) {
            return false;
        }
    }
    
    return true;
}

// Test cases
function runTests() {
    console.log('=== Testing OR Logic in Conditional Visibility ===\n');
    
    let passed = 0;
    let failed = 0;
    
    // Test 1: String equals with single value answer (backward compatibility)
    techDesignAnswers = {
        'Q1': { value: 'Cloud' }
    };
    const test1 = isQuestionVisible({
        visibleWhen: [{ questionId: 'Q1', equals: 'Cloud' }]
    });
    console.log('Test 1 - String equals with matching single value:', test1 ? '✓ PASS' : '✗ FAIL');
    test1 ? passed++ : failed++;
    
    // Test 2: String equals with non-matching single value
    techDesignAnswers = {
        'Q1': { value: 'OnPrem' }
    };
    const test2 = !isQuestionVisible({
        visibleWhen: [{ questionId: 'Q1', equals: 'Cloud' }]
    });
    console.log('Test 2 - String equals with non-matching value:', test2 ? '✓ PASS' : '✗ FAIL');
    test2 ? passed++ : failed++;
    
    // Test 3: Array equals with matching single value (OR logic)
    techDesignAnswers = {
        'Q1': { value: 'Cloud' }
    };
    const test3 = isQuestionVisible({
        visibleWhen: [{ questionId: 'Q1', equals: ['Cloud', 'Hybrid'] }]
    });
    console.log('Test 3 - Array equals ["Cloud", "Hybrid"] with value "Cloud":', test3 ? '✓ PASS' : '✗ FAIL');
    test3 ? passed++ : failed++;
    
    // Test 4: Array equals with second matching value (OR logic)
    techDesignAnswers = {
        'Q1': { value: 'Hybrid' }
    };
    const test4 = isQuestionVisible({
        visibleWhen: [{ questionId: 'Q1', equals: ['Cloud', 'Hybrid'] }]
    });
    console.log('Test 4 - Array equals ["Cloud", "Hybrid"] with value "Hybrid":', test4 ? '✓ PASS' : '✗ FAIL');
    test4 ? passed++ : failed++;
    
    // Test 5: Array equals with non-matching value
    techDesignAnswers = {
        'Q1': { value: 'OnPrem' }
    };
    const test5 = !isQuestionVisible({
        visibleWhen: [{ questionId: 'Q1', equals: ['Cloud', 'Hybrid'] }]
    });
    console.log('Test 5 - Array equals ["Cloud", "Hybrid"] with value "OnPrem":', test5 ? '✓ PASS' : '✗ FAIL');
    test5 ? passed++ : failed++;
    
    // Test 6: Multiselect answer with string equals
    techDesignAnswers = {
        'Q1': { value: ['Cloud', 'OnPrem'] }
    };
    const test6 = isQuestionVisible({
        visibleWhen: [{ questionId: 'Q1', equals: 'Cloud' }]
    });
    console.log('Test 6 - String equals "Cloud" with multiselect ["Cloud", "OnPrem"]:', test6 ? '✓ PASS' : '✗ FAIL');
    test6 ? passed++ : failed++;
    
    // Test 7: Multiselect answer with array equals (ANY match)
    techDesignAnswers = {
        'Q1': { value: ['OnPrem', 'Edge'] }
    };
    const test7 = isQuestionVisible({
        visibleWhen: [{ questionId: 'Q1', equals: ['Cloud', 'OnPrem', 'Hybrid'] }]
    });
    console.log('Test 7 - Array equals ["Cloud", "OnPrem", "Hybrid"] with multiselect ["OnPrem", "Edge"]:', test7 ? '✓ PASS' : '✗ FAIL');
    test7 ? passed++ : failed++;
    
    // Test 8: Multiselect answer with array equals (no match)
    techDesignAnswers = {
        'Q1': { value: ['Edge', 'Embedded'] }
    };
    const test8 = !isQuestionVisible({
        visibleWhen: [{ questionId: 'Q1', equals: ['Cloud', 'Hybrid'] }]
    });
    console.log('Test 8 - Array equals ["Cloud", "Hybrid"] with multiselect ["Edge", "Embedded"]:', test8 ? '✓ PASS' : '✗ FAIL');
    test8 ? passed++ : failed++;
    
    // Test 9: Multiple rules with AND logic (both must match)
    techDesignAnswers = {
        'Q1': { value: 'Cloud' },
        'Q2': { value: 'Enterprise' }
    };
    const test9 = isQuestionVisible({
        visibleWhen: [
            { questionId: 'Q1', equals: ['Cloud', 'Hybrid'] },
            { questionId: 'Q2', equals: 'Enterprise' }
        ]
    });
    console.log('Test 9 - Multiple rules (both match):', test9 ? '✓ PASS' : '✗ FAIL');
    test9 ? passed++ : failed++;
    
    // Test 10: Multiple rules with AND logic (one fails)
    techDesignAnswers = {
        'Q1': { value: 'OnPrem' },
        'Q2': { value: 'Enterprise' }
    };
    const test10 = !isQuestionVisible({
        visibleWhen: [
            { questionId: 'Q1', equals: ['Cloud', 'Hybrid'] },
            { questionId: 'Q2', equals: 'Enterprise' }
        ]
    });
    console.log('Test 10 - Multiple rules (one fails):', test10 ? '✓ PASS' : '✗ FAIL');
    test10 ? passed++ : failed++;
    
    // Test 11: No visibleWhen (always visible)
    const test11 = isQuestionVisible({});
    console.log('Test 11 - No visibleWhen (always visible):', test11 ? '✓ PASS' : '✗ FAIL');
    test11 ? passed++ : failed++;
    
    // Test 12: Missing dependent answer
    techDesignAnswers = {};
    const test12 = !isQuestionVisible({
        visibleWhen: [{ questionId: 'Q1', equals: 'Cloud' }]
    });
    console.log('Test 12 - Missing dependent answer (hidden):', test12 ? '✓ PASS' : '✗ FAIL');
    test12 ? passed++ : failed++;
    
    console.log(`\n=== Test Results ===`);
    console.log(`Passed: ${passed}`);
    console.log(`Failed: ${failed}`);
    console.log(`Total: ${passed + failed}`);
    
    return failed === 0;
}

// Run tests
const success = runTests();
process.exit(success ? 0 : 1);
