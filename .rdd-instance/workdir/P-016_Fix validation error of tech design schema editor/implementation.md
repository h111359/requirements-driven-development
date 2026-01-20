# Implementation: Fix validation error of tech design schema editor

## Prompt Summary
The Technical Design Schema Editor is incorrectly validating `visibleWhen` fields as strings when they should be arrays of condition objects. The validation code needs to be fixed to accept the correct format.

## Questionnaire Answers
- **Q1**: Fix the validation code to accept arrays of condition objects
- **Q2**: Expected structure is object with questionId (string) and equals (array of strings)
- **Q3**: Multiple condition objects in visibleWhen array → AND logic, Multiple values in the equals array → OR logic

## Context from Specifications

### Technical Design (empty)
No relevant content - technical-design.json is currently empty.

### Requirements
- [TR-0188]: Schema shall support conditional visibility rules using simple questionId equals value objects
- [TR-0193]: Web UI shall evaluate conditional visibility rules with AND logic where all rules must match

### Files and Folders
The tech_design_schema_editor directory contains the validation logic that needs to be fixed.

## Implementation Steps

### Step 1: Locate and examine the validation code

Found the issue in `tech_design_schema_editor/server.py` at line 276. The validation incorrectly checks:
```python
if not isinstance(question['visibleWhen'], str):
    errors.append(f"{path}.visibleWhen: must be a string")
```

However, the actual schema format uses arrays of condition objects. Example from `.rdd/config/technical-design-schema.json`:
```json
"visibleWhen": [
  {
    "questionId": "Compute_PrimaryModel",
    "equals": ["Containers / Kubernetes", "Mixed model (hybrid compute)"]
  }
]
```

### Step 2: Fix the validation to accept array of condition objects

The validation should:
1. Check that `visibleWhen` is an array
2. Each element is an object with `questionId` (string) and `equals` (array of strings)
3. Support AND logic for multiple conditions (array entries)
4. Support OR logic for multiple values in `equals` array

**Command executed:**
Updated `tech_design_schema_editor/server.py` lines 273-276 with proper array validation.

The new validation:
- Checks `visibleWhen` is an array
- Validates each condition object has `questionId` (string) and `equals` (array)
- Ensures `equals` array is non-empty
- Provides clear error messages for each validation failure

### Step 3: Verify the fix works

Let me test the validation by running the schema editor server and validating the schema.

**Command executed:**
```bash
cd /home/hromar/Desktop/vscode/requirements-driven-development/tech_design_schema_editor && python server.py
```

### Step 4: Update documentation

Updated `tech_design_schema_editor/README.md` to document the correct `visibleWhen` format:
- Changed from "must be a string" to "must be an array of condition objects"
- Added detailed structure explanation with questionId and equals fields
- Documented AND/OR logic behavior
- Added example JSON

## Summary

Fixed the validation error in the Technical Design Schema Editor by:
1. Updated server.py validation to accept `visibleWhen` as an array of condition objects
2. Added proper validation for each condition's structure (questionId + equals fields)
3. Updated README.md documentation to reflect the correct format

The schema now correctly validates `visibleWhen` arrays with:
- AND logic for multiple condition objects in the array
- OR logic for multiple values in the equals array

This aligns with requirement TR-0193 and the actual schema structure used throughout the technical-design-schema.json file.

## Requirements Updates

Created new requirement TR-0196 to document the schema editor's validation behavior:
```bash
python .rdd/src/actions/requirement_tr_create.py text="The Technical Design Schema Editor shall validate visibleWhen fields as arrays of condition objects where each condition contains questionId (string) and equals (array of strings) fields, supporting AND logic across multiple conditions and OR logic within each condition's equals array."
```

**Rationale:** This requirement formalizes the validation logic that was incorrectly implemented (was checking for string instead of array). The fix ensures the schema editor correctly validates the visibleWhen structure as defined in TR-0188 and TR-0193, and as used throughout the actual technical-design-schema.json file.
