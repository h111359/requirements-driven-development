# Implementation Details - P-030: OR Logic in Conditional Visibility

## Prompt Summary
Implement OR logic for conditional visibility using array values in the `equals` field. Currently, the Technical Design schema supports conditional visibility with AND logic between rules, but the convention document mentions support for OR logic via array values in `equals`. This feature needs to be implemented in the UI code.

## Questionnaire Answers Summary

Based on the answered questionnaire:

1. **Q1**: Support both string and array formats - `equals` can be either a string (single value) or an array of strings (OR logic) - **Answer: A**
2. **Q2**: ANY match - If `equals` is `['A', 'B']` and answer is `['B', 'C']`, rule matches because 'B' is in both - **Answer: A**
3. **Q3**: Do NOT update the Technical Design Schema JSON file - Only update convention document and code comments - **Answer: B**
4. **Q4**: Add validation - Validate that equals array has no duplicates and contains only valid option IDs for the referenced question - **Answer: A**
5. **Q5**: Add multi-select or tag input UI for the `equals` field in the conditional visibility editor - **Answer: A**

## Relevant Context

### From Technical Design
- Current technical design has deployment model with "Personal machine" selected, demonstrating the multiselect question type that will be affected by this implementation

### From Requirements
- UR-0018: The Web UI shall provide a Technical Specification page enabling editing of technical-design using a configuration-driven interactive form
- The OR logic enhancement directly improves the conditional visibility feature used in that form

### From Files and Folders
- Implementation files are located in `tech_design_schema_editor/` folder:
  - `tech_design_schema_editor/static/app.js` - Frontend JavaScript (contains `isQuestionVisible()` function)
  - `tech_design_schema_editor/server.py` - Backend Python server
  - `tech_design_schema_editor/index.html` - UI markup

### From P-029 Report
- Current implementation only supports string values in `equals` field
- Multiple rules in `visibleWhen` are combined with AND logic
- For multiselect questions, current code checks if value is present using `value.includes(rule.equals)`
- The `isQuestionVisible()` function is in `app.js` at lines 3106-3133

## Implementation Steps

### Step 1: Create implementation.md file
**Status**: Completed
**Action**: Created this file to track implementation details

### Step 2: Update isQuestionVisible() function to support array in equals
**Status**: Completed
**Location**: `.rdd/src/web/static/app.js` lines 3106-3153
**Changes Made**:
- Modified the `isQuestionVisible()` function to support both string and array formats for `rule.equals`
- Implemented OR logic: if `equals` is an array, the answer must match ANY value in the array
- For multiselect answers with array equals: uses ANY match logic (if any value from equals array is in the answer array, rule matches)
- For single-value answers with array equals: uses includes() to check if value matches any equals value
- Added comprehensive JSDoc comments explaining the OR logic behavior
- Maintained backward compatibility: string values are converted to single-element arrays internally

**Logic Details**:
1. Convert `rule.equals` to array format (if string, wrap in array)
2. For multiselect answers: iterate through equals values and check if any is in the answer array
3. For single-value answers: check if the value is included in the equals values array
4. All rules in visibleWhen must still be satisfied (AND logic between rules)

### Step 3: Add validation for equals array in schema editor
**Status**: Completed
**Location**: `tech_design_schema_editor/static/app.js`
**Changes Made**:

1. **Updated saveConditionsToQuestion() function** (lines ~1427-1516):
   - Added validation for equals arrays to check for duplicates
   - Added validation to ensure all values in equals array are valid option IDs for the referenced question
   - Converts single-element arrays to strings for cleaner JSON
   - Transforms internal condition format (questionId, operator, value) to visibleWhen format (questionId, equals)
   - Displays validation errors in console when issues are detected
   - Skips empty arrays in conditions

2. **Validation Logic**:
   - Detects duplicate values in equals arrays using Set comparison
   - Validates that all option IDs exist for questions that have predefined options
   - Reports errors with condition index for easy debugging
   - Logs errors to console.error and console.warn

3. **Format Conversion**:
   - Internal condition builder uses: `{questionId, operator, value}`
   - Stored visibleWhen format uses: `{questionId, equals}` where equals can be string or array
   - Single-element arrays are automatically simplified to strings
   - Empty arrays are skipped (condition is removed)

**Note**: The UI already had multiselect support for the value field (Q5 decision was already partially implemented). The multiselect dropdown allows users to select multiple values which are stored as an array, implementing the OR logic as required.

### Step 4: Enhance UI for conditional visibility editor
**Status**: Completed (Already implemented)
**Note**: The Technical Design Schema Editor already had a multiselect dropdown UI component for conditional visibility when the referenced question has options. This was discovered during implementation - Q5 was already addressed in previous work.

### Step 5: Update technical design convention documentation
**Status**: Completed
**Location**: `.rdd/conventions/technical-design.convention.md`
**Changes Made**:
- Expanded the "Conditional Visibility" section to clearly document both string and array formats for the `equals` field
- Added explicit subsections for "Format Support for `equals` Field" explaining:
  - String format (single value match)
  - Array format (OR logic - multiple value match)
  - Behavior for single-select vs multiselect questions
- Added a concrete example demonstrating OR logic usage
- Clarified the AND logic between multiple conditions vs OR logic within equals array
- Improved formatting and structure for better readability

### Step 6: Test the implementation
**Status**: Completed
**Test File**: `.rdd-instance/workdir/P-030_OR logic in Conditional Visibility/test-or-logic.py`
**Test Results**: All 12 tests passed ✓

**Test Coverage**:
1. ✓ String equals with matching single value (backward compatibility)
2. ✓ String equals with non-matching single value
3. ✓ Array equals with first matching value (OR logic)
4. ✓ Array equals with second matching value (OR logic)
5. ✓ Array equals with non-matching value
6. ✓ Multiselect answer with string equals
7. ✓ Multiselect answer with array equals (ANY match)
8. ✓ Multiselect answer with array equals (no match)
9. ✓ Multiple rules with AND logic (both match)
10. ✓ Multiple rules with AND logic (one fails)
11. ✓ No visibleWhen (always visible)
12. ✓ Missing dependent answer (hidden)

**Test Command**:
```bash
python .rdd-instance/workdir/P-030_OR\ logic\ in\ Conditional\ Visibility/test-or-logic.py
```

The tests verify:
- Backward compatibility with string format
- OR logic with array format for both single-select and multi-select questions
- AND logic between multiple rules
- Edge cases (missing answers, no conditions)

### Step 7: Update requirements
**Status**: Completed
**Requirements Updated**:

1. **TR-0193**: Updated to reflect OR logic support in equals arrays
   - **Before**: "The Web UI shall evaluate conditional visibility rules in real-time by checking visibleWhen arrays with AND logic where all rules must match either exact equals for radio/text or array includes for multiselect questions, re-rendering questions after each answer save or clear operation."
   - **After**: "The Web UI shall evaluate conditional visibility rules in real-time by checking visibleWhen arrays with AND logic where all rules must match, supporting both string and array formats for the equals field where arrays use OR logic (answer must match ANY value), handling exact equals for radio/text and array includes for multiselect questions, and re-rendering questions after each answer save or clear operation."
   - **Rationale**: Clarified that equals field can be string or array, with arrays using OR logic

2. **TR-0196**: Updated to clarify equals field format and add validation requirement
   - **Before**: "The Technical Design Schema Editor shall validate visibleWhen fields as arrays of condition objects where each condition contains questionId (string) and equals (array of strings) fields, supporting AND logic across multiple conditions and OR logic within each condition's equals array."
   - **After**: "The Technical Design Schema Editor shall validate visibleWhen fields as arrays of condition objects where each condition contains questionId (string) and equals (string or array of strings) fields, supporting AND logic across multiple conditions and OR logic when equals is an array, with validation to check for duplicate values and valid option IDs."
   - **Rationale**: Added backward compatibility for string format and specified the validation requirements implemented in this prompt

**Commands Executed**:
```bash
python .rdd/src/actions/requirement_tr_modify.py id="TR-0193" text="The Web UI shall evaluate conditional visibility rules in real-time by checking visibleWhen arrays with AND logic where all rules must match, supporting both string and array formats for the equals field where arrays use OR logic (answer must match ANY value), handling exact equals for radio/text and array includes for multiselect questions, and re-rendering questions after each answer save or clear operation."

python .rdd/src/actions/requirement_tr_modify.py id="TR-0196" text="The Technical Design Schema Editor shall validate visibleWhen fields as arrays of condition objects where each condition contains questionId (string) and equals (string or array of strings) fields, supporting AND logic across multiple conditions and OR logic when equals is an array, with validation to check for duplicate values and valid option IDs."
```

## Summary

Successfully implemented OR logic for conditional visibility in the RDD framework's Technical Design feature. The implementation:

1. **Core Functionality**: Updated `isQuestionVisible()` function in `.rdd/src/web/static/app.js` to support both string and array formats for the `equals` field with OR logic
2. **Validation**: Added comprehensive validation in the Technical Design Schema Editor to check for duplicates and valid option IDs
3. **UI Support**: Confirmed existing multiselect UI component supports the feature
4. **Documentation**: Updated convention document with clear examples and explanations
5. **Testing**: Created and executed comprehensive test suite with 12 passing tests
6. **Requirements**: Updated TR-0193 and TR-0196 to reflect the new capability

The feature maintains full backward compatibility with existing string-based equals values while enabling powerful OR logic through array values.

## Post-Implementation Actions

1. ✓ Executed `python .rdd/src/actions/prompt_set_executed_on.py`
2. ✓ Executed `python .rdd/src/actions/prompt_implementation_completed_on.py`
3. ✓ Executed `python .rdd/src/actions/prompt_set_execution_mode.py mode=no-action`
4. ✓ Verified no errors in modified JavaScript files

## Files Modified

1. `.rdd/src/web/static/app.js` - Updated `isQuestionVisible()` function (lines 3106-3153)
2. `tech_design_schema_editor/static/app.js` - Updated `saveConditionsToQuestion()` function with validation
3. `.rdd/conventions/technical-design.convention.md` - Enhanced conditional visibility documentation
4. `.rdd-instance/specifications/requirements.md` - Updated TR-0193 and TR-0196 via requirement scripts

## Files Created

1. `.rdd-instance/workdir/P-030_OR logic in Conditional Visibility/implementation.md` - This file
2. `.rdd-instance/workdir/P-030_OR logic in Conditional Visibility/test-or-logic.py` - Test suite (12/12 tests passing)
3. `.rdd-instance/workdir/P-030_OR logic in Conditional Visibility/test-or-logic.js` - Node.js version of tests (for reference)

