# Implementation Log - P-037: No other field in Technical Design

## Problem Statement

The Technical Design page is not displaying the "Other" field for questions that have `allowOther: true` in the schema. According to the questionnaire answers, users should be able to enter custom values when this field is enabled.

## Technical Context

**Technical Design Schema** (`.rdd/config/technical-design-schema.json`):
- Contains questions with `allowOther: true` property
- Includes `otherPlaceholder` field to guide users on what to enter
- Examples: `Product_PrimaryProductCategory`, `Product_PrimaryConsumptionMode`

**Requirements** (UR-0018):
- Web UI shall provide Technical Specification page with configuration-driven interactive form

**Files and Folders**:
- Web UI app.js is at `.rdd/src/web/static/app.js`
- Contains `renderQuestion()` function starting at line 3157

**Questionnaire Answers** (all answered with option A):
- Q1: For multiselect, add dedicated checkbox labeled 'Other' that reveals text input when checked
- Q2: For radio, add radio button labeled 'Other' that reveals inline text input when selected
- Q3: Store custom text directly in value array/field alongside predefined options
- Q4: Detect custom values by checking if saved value matches schema options
- Q5: Use `otherPlaceholder` as placeholder attribute for Other text input

## Investigation

### Current Code Analysis

Examined `.rdd/src/web/static/app.js` lines 3157-3350 - the `renderQuestion()` function:

**Current implementation**:
- Handles `radio` type with options (lines ~3189-3212)
- Handles `multiselect` type with options (lines ~3213-3237)
- Handles `text` type (lines ~3238-3245)
- **MISSING**: No logic to check `question.allowOther` property
- **MISSING**: No rendering of "Other" checkbox/radio + text input

**Storage format** (confirmed):
- Uses `techDesignAnswers[question.id]` object with `value` field
- Multiselect: value is array
- Radio: value is string
- Matches Q3 answer - custom values stored directly

## Implementation Plan

Per questionnaire answers, implement the following:

1. **For multiselect questions with allowOther=true**:
   - Add "Other" checkbox after all predefined options
   - When checked, reveal text input field below it
   - Use `otherPlaceholder` as placeholder
   - On save, append custom text to value array

2. **For radio questions with allowOther=true**:
   - Add "Other" radio button after all predefined options
   - When selected, reveal inline text input field
   - Use `otherPlaceholder` as placeholder
   - On save, store custom text as value string

3. **Detect and display existing custom values**:
   - Compare saved value against schema option IDs
   - If no match, assume it's custom and pre-populate Other field

## Changes Made

### 1. Modified renderQuestion() for Radio Type with allowOther

**File**: `.rdd/src/web/static/app.js`

**Changes**:
- Added logic to detect custom values (values not in predefined options)
- Added "Other" radio button at the end of options list when `question.allowOther === true`
- Added text input field below "Other" radio that:
  - Is hidden by default, shown when "Other" radio is selected
  - Uses `question.otherPlaceholder` as placeholder text
  - Pre-populates with custom value if answer contains one
  - Saves on blur and Enter key press
  - Has left margin (ms-4 class) for visual alignment

**Implementation Details**:
- Custom value detection: Compare `currentAnswer.value` against all `option.id` values
- If no match found, value is considered custom
- Text input ID: `${question.id}-other-text`
- Radio value: `__other__` (special marker, not saved)

### 2. Modified renderQuestion() for Multiselect Type with allowOther

**File**: `.rdd/src/web/static/app.js`

**Changes**:
- Added logic to detect custom values in answer array
- Added "Other" checkbox at the end of options list when `question.allowOther === true`
- Added text input field below "Other" checkbox that:
  - Is hidden by default, shown when "Other" checkbox is checked
  - Uses `question.otherPlaceholder` as placeholder text
  - Pre-populates with custom values (comma-separated) if answer contains them
  - Saves on blur and Enter key press
  - Unchecking "Other" clears the text input and saves
  - Supports multiple custom values separated by commas

**Implementation Details**:
- Custom values detection: Filter answer array for values not in schema options
- Text input shows all custom values as comma-separated string
- Checkbox toggles text input visibility
- Text input ID: `${question.id}-other-text`

### 3. Modified saveMultiselectAnswer() Function

**File**: `.rdd/src/web/static/app.js`

**Changes**:
- Filter out `__other__` checkbox value (it's just a UI control)
- Check if "Other" checkbox is checked
- If checked, read text input value
- Split by comma to support multiple custom entries
- Trim and filter empty values
- Append custom values to the selected predefined options
- Save combined array

**Implementation Details**:
- Uses `split(',')` to parse comma-separated custom values
- Applies `trim()` and `filter()` for clean data
- Spreads custom values into main values array using spread operator

## Testing Recommendations

Manual testing should verify:

1. **Radio with allowOther**:
   - "Other" radio appears for questions with allowOther=true
   - Text input hidden initially
   - Clicking "Other" reveals text input and focuses it
   - Placeholder text matches schema otherPlaceholder
   - Typing and blurring saves the custom value
   - Pressing Enter saves the custom value
   - Reloading page shows saved custom value with "Other" selected

2. **Multiselect with allowOther**:
   - "Other" checkbox appears for questions with allowOther=true
   - Text input hidden initially
   - Checking "Other" reveals text input
   - Can enter single custom value
   - Can enter multiple comma-separated values
   - Unchecking "Other" hides input and clears custom values
   - Saved answers show both predefined and custom values
   - Reloading page shows all saved values correctly

3. **Storage format**:
   - Custom values stored directly in value field (not separately)
   - For radio: string value
   - For multiselect: array including both predefined IDs and custom strings
   - Check `.rdd-instance/specifications/technical-design.json` format

4. **Edge cases**:
   - Empty custom value doesn't save
   - Leading/trailing spaces are trimmed
   - Comma-separated values work correctly
   - Switching between predefined and Other options
   - Clearing answers works correctly

## Requirements Impact

No new requirements needed. Implementation fulfills existing requirements:
- **UR-0018**: Technical Design page with schema-driven form - enhanced to support allowOther field
- **TR-0154 to TR-0186**: Technical Design implementation requirements already cover schema-driven rendering

The allowOther field was already in the schema (see P-001 prompt registry), just missing UI implementation.

## Verification

Verified the implementation:
- Modified `.rdd/src/web/static/app.js` with three changes
- No syntax errors detected
- Web server confirmed running on http://localhost:8080
- Code review confirms proper handling of:
  - Custom value detection on page load
  - Storage format (Q3 answer A: direct storage in value field)
  - UI pattern (Q1-A for multiselect, Q2-A for radio)
  - Placeholder usage (Q5-A: otherPlaceholder as placeholder attribute)

## Summary

Successfully implemented "Other" field functionality for Technical Design questions with `allowOther: true`:

✅ Radio questions show "Other" radio button + conditional text input
✅ Multiselect questions show "Other" checkbox + conditional text input  
✅ Custom values detected and pre-populated on page load
✅ Values stored directly in answer value field (no separate customValue field)
✅ Placeholder text from schema used appropriately
✅ Supports comma-separated multiple custom values in multiselect

The fix addresses the issue reported in the prompt: "Other field is not present for the questions it is turned on in Technical Design."
