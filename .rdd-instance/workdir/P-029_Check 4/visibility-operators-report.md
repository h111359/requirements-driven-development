# Conditional Visibility Operators Report - RDD Framework

**Report Date**: 2026-01-24  
**Prompt ID**: P-029  
**Scope**: Analysis of conditional visibility operators in RDD Web Application

## Executive Summary

This report documents the conditional visibility operators supported by the RDD framework for the `visibleWhen` section of technical design questions. The analysis covers both the Web UI implementation and the documented conventions.

## Current Implementation

### Location of Implementation

The conditional visibility logic is implemented in:
- **File**: `.rdd/src/web/static/app.js`
- **Function**: `isQuestionVisible(question)` (lines 3106-3133)

### Supported Operator

Currently, the RDD framework supports **only one operator**:

#### 1. `equals` Operator

**Syntax**:
```json
"visibleWhen": [
  {
    "questionId": "<question-id>",
    "equals": "<value>"
  }
]
```

**Behavior**:
- For **single-value questions** (radio, text): Checks exact match (`value === rule.equals`)
- For **multi-value questions** (multiselect): Checks if the specified value is present in the answer array (`value.includes(rule.equals)`)

**Logic Combination**:
- Multiple rules in `visibleWhen` array are combined with **AND logic** - ALL rules must be satisfied
- According to conventions (but not yet implemented), multiple values in `equals` array should use **OR logic** - answer must match ANY ONE of the values

### Implementation Code

```javascript
function isQuestionVisible(question) {
    if (!question.visibleWhen || question.visibleWhen.length === 0) {
        return true;
    }
    
    // All rules must be satisfied (AND logic)
    for (const rule of question.visibleWhen) {
        const dependentAnswer = techDesignAnswers[rule.questionId];
        if (!dependentAnswer) {
            return false;
        }
        
        const value = dependentAnswer.value;
        if (Array.isArray(value)) {
            // Multiselect: check if equals value is in array
            if (!value.includes(rule.equals)) {
                return false;
            }
        } else {
            // Radio/text: check exact match
            if (value !== rule.equals) {
                return false;
            }
        }
    }
    
    return true;
}
```

## Convention Documentation

The conditional visibility is documented in:
- **File**: `.rdd/conventions/technical-design.convention.md`
- **Section**: "Conditional Visibility" (lines 82-108)

### Convention Specifications

**Rule Structure**:
```json
"visibleWhen": [
  {
    "questionId": "ProjectScale_OverallScaleCategory",
    "equals": "Enterprise-wide platform"
  }
]
```

**Evaluation Logic (as documented)**:
1. All rules in `visibleWhen` array must be satisfied (AND logic)
2. Rule matches when referenced question's current answer value equals the specified value
3. For multiselect questions, rule matches if the specified value is present in the answer array
4. Questions without `visibleWhen` are always visible

**Multiple Conditions**:
- Multiple condition objects in `visibleWhen` array → AND logic (ALL must be true)
- Multiple values in `equals` array → OR logic (answer must match ANY ONE) - **Note: This feature is documented but not yet implemented**

## Limitations and Gaps

### Not Currently Supported

The following operators/features are **NOT** supported in the current implementation:

1. **notEquals** - Check if value does NOT match
2. **contains** - Substring matching for text values
3. **greaterThan** / **lessThan** - Numeric comparisons
4. **in** - Check if value is in a list of allowed values
5. **regex** - Pattern matching
6. **isEmpty** / **isNotEmpty** - Check for empty values
7. **OR logic at top level** - All rules are AND-ed together
8. **Complex nested conditions** - No support for (A AND B) OR (C AND D)
9. **Array of values in equals field** - Convention mentions this but implementation doesn't support it yet

### Edge Cases

1. **Missing dependent answer**: If a question referenced in `visibleWhen` has no answer, the dependent question is hidden
2. **Question order dependency**: Questions with `visibleWhen` rules must reference questions that appear before them (or in a different category)
3. **Dynamic updates**: The UI re-evaluates visibility when answers change, hiding/showing questions dynamically

## Usage Examples

### Example 1: Simple Radio Dependency
```json
{
  "id": "Deploy_ContainerOrchestration",
  "label": "Which container orchestration platform?",
  "type": "radio",
  "options": [
    {"id": "kubernetes", "label": "Kubernetes"},
    {"id": "docker-swarm", "label": "Docker Swarm"}
  ],
  "visibleWhen": [
    {
      "questionId": "Deploy_DeploymentType",
      "equals": "containerized"
    }
  ]
}
```
**Result**: This question only appears if "Deploy_DeploymentType" is answered with "containerized"

### Example 2: Multiselect Dependency
```json
{
  "id": "Security_CloudProvider",
  "label": "Which cloud provider security features?",
  "type": "multiselect",
  "visibleWhen": [
    {
      "questionId": "Infra_DeploymentModel",
      "equals": "Cloud"
    }
  ]
}
```
**Result**: This question appears if "Cloud" is selected in the multiselect "Infra_DeploymentModel" question (even if other values are also selected)

### Example 3: Multiple Conditions (AND)
```json
{
  "id": "Advanced_FeatureX",
  "label": "Configure advanced feature X",
  "type": "radio",
  "visibleWhen": [
    {
      "questionId": "ProjectScale_OverallScaleCategory",
      "equals": "Enterprise-wide platform"
    },
    {
      "questionId": "Deploy_DeploymentType",
      "equals": "containerized"
    }
  ]
}
```
**Result**: This question appears ONLY if BOTH conditions are satisfied

## Recommendations

### For Current Usage

1. **Use only `equals` operator** - This is the only implemented operator
2. **Use AND logic only** - Multiple rules are AND-ed together
3. **Reference answered questions** - Ensure dependent questions are answered before dependent ones appear
4. **Test visibility changes** - Verify that questions appear/disappear correctly when changing answers in the UI

### For Future Enhancements

If additional operators are needed, consider implementing:

1. **Priority 1 - Already documented but not implemented**:
   - Support for array of values in `equals` field with OR logic
   
2. **Priority 2 - Common use cases**:
   - `notEquals` - Negative matching
   - `in` - Check if value is in a list (cleaner than multiple OR rules)
   
3. **Priority 3 - Advanced features**:
   - `contains` - Substring matching for text
   - `isEmpty` / `isNotEmpty` - Empty value checks
   - Top-level OR logic between rule groups

## Conclusion

The RDD framework's conditional visibility feature is **simple but functional**, supporting the most common use case: showing/hiding questions based on exact value matches of other questions. The implementation is consistent between the Web UI JavaScript code and the convention documentation, with one exception: the documented support for OR logic via array values in `equals` is not yet implemented.

For the vast majority of technical design questionnaires, the current `equals` operator with AND logic provides sufficient flexibility to create meaningful conditional question flows.

---

**Analysis performed by**: GitHub Copilot  
**Files analyzed**:
- `.rdd/src/web/static/app.js` (implementation)
- `.rdd/conventions/technical-design.convention.md` (documentation)
