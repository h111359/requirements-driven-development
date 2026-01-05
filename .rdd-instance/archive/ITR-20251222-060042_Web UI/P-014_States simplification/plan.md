# Implementation Plan - P-014: States Simplification

## Overview
This plan implements the simplification of prompt states from four states (draft, planned, in-progress, completed) to two states (active, completed). The implementation follows the questionnaire answers and ensures all affected components are updated consistently.

## Questionnaire Summary
Based on the answered questionnaire:
- Q1: New prompts created in `active` state (Option A)
- Q2: Keep the `executed` flag unchanged (Option A)
- Q3: Complete button enabled only for `active` prompts with `executed == true` (Option B)
- Q4: `analyze-enabled` and `plan-enabled` can only be set to `true` for `active` prompts (Option A)
- Q5: Active=warning/yellow, Completed=success/green (Option B)
- Q6: Strictly enforce only one active prompt at a time (Option A)
- Q7: Allow any transition (active ↔ completed) (Option A)
- Q8: Update all error messages to refer to `"state='active'"` (Option A)

## Implementation Steps

### Step 1: Update Requirements File
**File:** `.rdd-instance/specifications/requirements.md`

**Changes:**
1. Update the definition of `active prompt` in the Definitions section:
   - Change from: "The prompt in `.rdd-instance/workdir/work-iteration-registry.json` which is with state `planned` or `in-progress`"
   - Change to: "The prompt in `.rdd-instance/workdir/work-iteration-registry.json` which is with state `active`"

2. Add new user requirement about state simplification:
   - [UR-20251231-0700] The framework shall support two prompt states: `active` and `completed`. The `active` state indicates a prompt is currently being worked on, while `completed` indicates finished work.

3. Add new user requirement about prompt creation state:
   - [UR-20251231-0701] New prompts shall be created in `active` state by default.

4. Add new user requirement about single active prompt:
   - [UR-20251231-0702] The framework shall enforce that only one prompt can be in `active` state at any time, ensuring clear focus on current work.

5. Update [UR-20251230-2003] to reflect new states:
   - Change from: "The framework shall prevent enabling analyze mode for completed prompts."
   - Change to: "The framework shall prevent enabling analyze mode for prompts not in `active` state."

6. Update [UR-20251231-0203] to reflect new states:
   - Change from: "The framework shall prevent enabling plan mode for completed prompts."
   - Change to: "The framework shall prevent enabling plan mode for prompts not in `active` state."

7. Update [TR-20251230-2007] to reflect new states:
   - Change from: "The Web UI shall display analyze mode toggles only for prompts in draft, planned, or in-progress states."
   - Change to: "The Web UI shall display analyze mode toggles only for prompts in `active` state."

8. Update [TR-20251230-2008] to reflect new states:
   - Change from: "The Prompts section table in the Web UI shall include an 'Analyze Mode' column with a toggle switch for non-completed prompts and 'N/A' for completed prompts."
   - Change to: "The Prompts section table in the Web UI shall include an 'Analyze Mode' column with a toggle switch for `active` prompts and 'N/A' for `completed` prompts."

9. Update [TR-20251231-0106] to reflect new states:
   - Change from: "The Web UI shall provide a 'Complete' button in the Actions column for prompts in in-progress state, enabled only when the prompt's executed flag is true, with a tooltip explaining the requirement."
   - Change to: "The Web UI shall provide a 'Complete' button in the Actions column for prompts in `active` state, enabled only when the prompt's executed flag is true, with a tooltip explaining the requirement."

10. Update [TR-20251231-0203] to reflect new states:
    - Change from: "The Web UI shall display plan mode toggles only for prompts in draft, planned, or in-progress states."
    - Change to: "The Web UI shall display plan mode toggles only for prompts in `active` state."

11. Update [TR-20251231-0204] to reflect new states:
    - Change from: "The Prompts section table in the Web UI shall include a 'Plan Mode' column with a toggle switch for non-completed prompts and 'N/A' for completed prompts."
    - Change to: "The Prompts section table in the Web UI shall include a 'Plan Mode' column with a toggle switch for `active` prompts and 'N/A' for `completed` prompts."

12. Update [TR-20251230-1438] to reflect new states:
    - Change from: "The Prompts section shall provide an integrated prompt editor that displays Edit buttons for prompts in draft, planned, or in-progress states and View buttons for prompts in completed state."
    - Change to: "The Prompts section shall provide an integrated prompt editor that displays Edit buttons for prompts in `active` state and View buttons for prompts in `completed` state."

13. Add new technical requirement about state validation:
    - [TR-20251231-0700] The `prompt_set_state.py` script shall accept only `active` or `completed` as valid state values.

14. Add new technical requirement about state transitions:
    - [TR-20251231-0701] The framework shall allow bidirectional state transitions between `active` and `completed` states without restrictions.

15. Add new technical requirement about prompt creation validation:
    - [TR-20251231-0702] The `prompt_create.py` script shall validate that no other prompt is in `active` state when creating a new prompt, and shall fail with a clear error message if validation fails.

### Step 2: Update Work Iteration Registry Convention
**File:** `.rdd/conventions/work-iteration-registry.convention.md`

**Changes:**
1. Update the validation rules section for prompt creation:
   - Change from: "If creating a prompt with state `planned` or `in-progress`, the tool MUST validate that no other prompt currently has state `planned` or `in-progress`."
   - Change to: "If creating a prompt with state `active`, the tool MUST validate that no other prompt currently has state `active`."

2. Update the `state` field documentation in `prompt-metadata` section:
   - Change the description from: "Defines if the prompt is still a draft, if it is planned for execution, in progress or completed. Only one prompt could be in a state 'planned' or 'in-progress' at a given time..."
   - Change to: "Defines if the prompt is currently active or completed. Only one prompt can be in `active` state at a given time, and this is the prompt which `execute command` (as defined in `.rdd-instance/specifications/requirements.md`) will run."
   - Change possible values from: `["draft" | "planned" | "in-progress" | "completed"]`
   - Change to: `["active" | "completed"]`

3. Update the `analyze-enabled` field validation rules:
   - Change from: "Can only be set to `true` for prompts with state `draft`, `planned`, or `in-progress`"
   - Change to: "Can only be set to `true` for prompts with state `active`"

4. Add documentation for `plan-enabled` field (if not already present):
   - Add validation rules: "Can only be set to `true` for prompts with state `active`"
   - Add note: "Cannot be enabled for prompts with state `completed`"

5. Update the canonical example to use new states:
   - Change state values in example from `draft`, `planned`, `in-progress` to `active`
   - Keep one prompt as `completed` for reference

### Step 3: Update Python Script - prompt_set_state.py
**File:** `.rdd/src/actions/prompt_set_state.py`

**Changes:**
1. Update the module docstring to reflect new states
2. Update `_PROMPT_STATES` constant from `{"draft", "planned", "in-progress", "completed"}` to `{"active", "completed"}`
3. Update usage examples in docstring to use `active` instead of `in-progress` or `planned`
4. Update `_find_active_prompt()` function docstring:
   - Change from: "Find the prompt currently in 'planned' or 'in-progress' state."
   - Change to: "Find the prompt currently in 'active' state."
5. Update logic in `_find_active_prompt()`:
   - Change from: `if p.get("state") in {"planned", "in-progress"}:`
   - Change to: `if p.get("state") == "active":`
6. Update error messages:
   - Change from: "No active prompt found (no prompt in 'planned' or 'in-progress' state)"
   - Change to: "No active prompt found (no prompt in 'active' state)"
7. Update single-active invariant check:
   - Change from: `if new_state in {"planned", "in-progress"}:`
   - Change to: `if new_state == "active":`
8. Update error message:
   - Change from: "Only one prompt may be in 'planned' or 'in-progress' at a time."
   - Change to: "Only one prompt may be in 'active' state at a time."

### Step 4: Update Python Script - prompt_create.py
**File:** `.rdd/src/actions/prompt_create.py`

**Changes:**
1. Update `_PROMPT_STATES` constant from `{"draft", "planned", "in-progress", "completed"}` to `{"active", "completed"}`
2. Update usage documentation to reflect new states
3. Update default state from `"draft"` to `"active"`
4. Update single-active invariant enforcement:
   - Change from: `if state in {"planned", "in-progress"}:`
   - Change to: `if state == "active":`
5. Update validation check:
   - Change from: `if s in {"planned", "in-progress"}:`
   - Change to: `if s == "active":`
6. Update error message:
   - Change from: "Only one prompt may be in state 'planned' or 'in-progress' at a time"
   - Change to: "Only one prompt may be in 'active' state at a time"

### Step 5: Update Python Script - prompt_analyze_on.py
**File:** `.rdd/src/actions/prompt_analyze_on.py`

**Changes:**
1. Update module docstring:
   - Change from: "to the currently active prompt (one in 'planned' or 'in-progress' state)."
   - Change to: "to the currently active prompt (one in 'active' state)."
2. Update `_find_active_prompt()` function docstring:
   - Change from: "Find the active prompt (state = 'planned' or 'in-progress')."
   - Change to: "Find the active prompt (state = 'active')."
3. Update logic in `_find_active_prompt()`:
   - Change from: `if prompt.get('state') in ['planned', 'in-progress']:`
   - Change to: `if prompt.get('state') == 'active':`
4. Update error messages:
   - Change from: "No active prompt found (state='planned' or 'in-progress')"
   - Change to: "No active prompt found (state='active')"
   - Change from: "Create a prompt or set an existing prompt to 'planned' or 'in-progress' state."
   - Change to: "Create a prompt or set an existing prompt to 'active' state."
5. Update state validation:
   - Change from: `if prompt.get('state') not in ['draft', 'planned', 'in-progress']:`
   - Change to: `if prompt.get('state') != 'active':`
6. Update error message:
   - Change from: "Analyze mode can only be enabled for prompts in 'draft', 'planned', or 'in-progress' state."
   - Change to: "Analyze mode can only be enabled for prompts in 'active' state."

### Step 6: Update Python Script - prompt_analyze_off.py
**File:** `.rdd/src/actions/prompt_analyze_off.py`

**Changes:**
1. Update module docstring:
   - Change from: "to the currently active prompt (one in 'planned' or 'in-progress' state)."
   - Change to: "to the currently active prompt (one in 'active' state)."
2. Update `_find_active_prompt()` function docstring:
   - Change from: "Find the active prompt (state = 'planned' or 'in-progress')."
   - Change to: "Find the active prompt (state = 'active')."
3. Update logic in `_find_active_prompt()`:
   - Change from: `if prompt.get('state') in ['planned', 'in-progress']:`
   - Change to: `if prompt.get('state') == 'active':`
4. Update error messages:
   - Change from: "No active prompt found (state='planned' or 'in-progress')"
   - Change to: "No active prompt found (state='active')"
   - Change from: "Create a prompt or set an existing prompt to 'planned' or 'in-progress' state."
   - Change to: "Create a prompt or set an existing prompt to 'active' state."

### Step 7: Update Python Script - prompt_plan_on.py
**File:** `.rdd/src/actions/prompt_plan_on.py`

**Changes:**
1. Update module docstring:
   - Change from: "to the currently active prompt (one in 'planned' or 'in-progress' state)."
   - Change to: "to the currently active prompt (one in 'active' state)."
2. Update `_find_active_prompt()` function docstring:
   - Change from: "Find the active prompt (state = 'planned' or 'in-progress')."
   - Change to: "Find the active prompt (state = 'active')."
3. Update logic in `_find_active_prompt()`:
   - Change from: `if prompt.get('state') in ['planned', 'in-progress']:`
   - Change to: `if prompt.get('state') == 'active':`
4. Update error messages:
   - Change from: "No active prompt found (state='planned' or 'in-progress')"
   - Change to: "No active prompt found (state='active')"
   - Change from: "Create a prompt or set an existing prompt to 'planned' or 'in-progress' state."
   - Change to: "Create a prompt or set an existing prompt to 'active' state."
5. Update state validation:
   - Change from: `if prompt.get('state') not in ['draft', 'planned', 'in-progress']:`
   - Change to: `if prompt.get('state') != 'active':`
6. Update error message:
   - Change from: "Plan mode can only be enabled for prompts in 'draft', 'planned', or 'in-progress' state."
   - Change to: "Plan mode can only be enabled for prompts in 'active' state."

### Step 8: Update Python Script - prompt_plan_off.py
**File:** `.rdd/src/actions/prompt_plan_off.py`

**Changes:**
1. Update module docstring:
   - Change from: "to the currently active prompt (one in 'planned' or 'in-progress' state)."
   - Change to: "to the currently active prompt (one in 'active' state)."
2. Update `_find_active_prompt()` function docstring:
   - Change from: "Find the active prompt (state = 'planned' or 'in-progress')."
   - Change to: "Find the active prompt (state = 'active')."
3. Update logic in `_find_active_prompt()`:
   - Change from: `if prompt.get('state') in ['planned', 'in-progress']:`
   - Change to: `if prompt.get('state') == 'active':`
4. Update error messages:
   - Change from: "No active prompt found (state='planned' or 'in-progress')"
   - Change to: "No active prompt found (state='active')"
   - Change from: "Create a prompt or set an existing prompt to 'planned' or 'in-progress' state."
   - Change to: "Create a prompt or set an existing prompt to 'active' state."

### Step 9: Update Python Script - prompt_set_executed_on.py
**File:** `.rdd/src/actions/prompt_set_executed_on.py`

**Changes:**
1. Update `_find_active_prompt()` function docstring:
   - Change from: "Find the prompt currently in 'planned' or 'in-progress' state."
   - Change to: "Find the prompt currently in 'active' state."
2. Update logic in `_find_active_prompt()`:
   - Change from: `if p.get("state") in {"planned", "in-progress"}:`
   - Change to: `if p.get("state") == "active":`
3. Update error messages:
   - Change from: "No active prompt found (no prompt in 'planned' or 'in-progress' state)"
   - Change to: "No active prompt found (no prompt in 'active' state)"
   - Change from: "Either specify a prompt-id or set a prompt to 'planned' or 'in-progress' state."
   - Change to: "Either specify a prompt-id or set a prompt to 'active' state."

### Step 10: Update Python Script - prompt_complete.py
**File:** `.rdd/src/actions/prompt_complete.py`

**Changes:**
1. Update `_find_active_prompt()` function docstring:
   - Change from: "Find the prompt currently in 'planned' or 'in-progress' state."
   - Change to: "Find the prompt currently in 'active' state."
2. Update logic in `_find_active_prompt()`:
   - Change from: `if p.get("state") in {"planned", "in-progress"}:`
   - Change to: `if p.get("state") == "active":`
3. Update error messages:
   - Change from: "No active prompt found (no prompt in 'planned' or 'in-progress' state)"
   - Change to: "No active prompt found (no prompt in 'active' state)"
   - Change from: "Either specify a prompt-id or set a prompt to 'planned' or 'in-progress' state."
   - Change to: "Either specify a prompt-id or set a prompt to 'active' state."

### Step 11: Update CLI - rdd.py
**File:** `.rdd/src/rdd.py`

**Changes:**
1. Update the prompt for state in the interactive menu:
   - Change from: `"Enter new state (draft/planned/in-progress/completed)"`
   - Change to: `"Enter new state (active/completed)"`

### Step 12: Update Web UI JavaScript - app.js
**File:** `.rdd/src/web/static/app.js`

**Changes:**
1. Update the `isEditable` check in prompt editor:
   - Change from: `const isEditable = (state === 'draft' || state === 'planned' || state === 'in-progress');`
   - Change to: `const isEditable = (state === 'active');`

2. Update the complete button condition:
   - Change from: `if (state === 'in-progress') {`
   - Change to: `if (state === 'active') {`

3. Update the state badge mapping:
   - Remove entries for 'draft', 'planned', and 'in-progress'
   - Add entry for 'active': `'active': '<span class="badge bg-warning">Active</span>'`
   - Keep 'completed': `'completed': '<span class="badge bg-success">Completed</span>'`

4. Update analyze mode and plan mode toggle visibility logic:
   - Change any checks like `state !== 'completed'` or `state in ['draft', 'planned', 'in-progress']`
   - Change to: `state === 'active'`

### Step 13: Update Execution Prompt Snippets
**File:** `.rdd/prompt-snippets/execution.md`

**Changes:**
1. Update the definition of [ACTIVE-PROMPT-ID]:
   - Change from: "is the prompt-id of the prompt entry in `.rdd-instance/workdir/work-iteration-registry.json` which is with state `planned` or `in-progress`"
   - Change to: "is the prompt-id of the prompt entry in `.rdd-instance/workdir/work-iteration-registry.json` which is with state `active`"

2. Update any other references to the old states in execution instructions

### Step 14: Update Other Prompt Snippets
Search for and update any other files in `.rdd/prompt-snippets/` that reference the old states.

### Step 15: Update Test Files (if any exist)
Search for test files that may have assertions or test data using the old states and update them to use the new states.

### Step 16: Verify All Changes
1. Search the entire codebase for any remaining references to "draft", "planned", or "in-progress" in the context of prompt states
2. Ensure all Python scripts, JavaScript files, conventions, requirements, and prompt snippets have been updated
3. Verify that error messages are consistent and helpful
4. Ensure that the single active prompt validation is properly implemented everywhere

## Migration Notes

This is a breaking change that affects the structure of `work-iteration-registry.json`. Existing instances may have prompts in the old states. Consider adding a migration note or script if needed, though based on the prompt text, it appears the user wants a clean implementation without backward compatibility concerns.

## Files to be Modified

### Python Scripts (10 files)
1. `.rdd/src/actions/prompt_set_state.py`
2. `.rdd/src/actions/prompt_create.py`
3. `.rdd/src/actions/prompt_analyze_on.py`
4. `.rdd/src/actions/prompt_analyze_off.py`
5. `.rdd/src/actions/prompt_plan_on.py`
6. `.rdd/src/actions/prompt_plan_off.py`
7. `.rdd/src/actions/prompt_set_executed_on.py`
8. `.rdd/src/actions/prompt_complete.py`
9. `.rdd/src/rdd.py`

### Web UI Files (1 file)
10. `.rdd/src/web/static/app.js`

### Convention Files (1 file)
11. `.rdd/conventions/work-iteration-registry.convention.md`

### Requirements Files (1 file)
12. `.rdd-instance/specifications/requirements.md`

### Prompt Snippets (1+ files)
13. `.rdd/prompt-snippets/execution.md`
14. Any other prompt snippet files that reference states

## Testing Recommendations

After implementation:
1. Test creating a new prompt - should be created in 'active' state
2. Test that only one prompt can be in 'active' state at a time
3. Test state transitions (active ↔ completed)
4. Test analyze mode can only be enabled for active prompts
5. Test plan mode can only be enabled for active prompts
6. Test completion button in Web UI appears only for active prompts with executed=true
7. Test that badges display correctly (yellow for active, green for completed)
8. Verify all error messages are clear and helpful
