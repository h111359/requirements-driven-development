# Plan for P-012: Plan Mode Implementation

## Overview

This plan implements a "Plan mode" feature similar to the existing "Analyze mode". Plan mode allows users to generate an implementation plan without proceeding to actual implementation, giving them a chance to review and approve the plan before execution.

## Implementation Steps

### Step 1: Add plan-enabled field to work iteration registry schema

**What will be done:**
- Add a new boolean field `plan-enabled` (default: false) to each prompt object in the work iteration registry schema
- This field will control whether plan mode is active for a specific prompt
- The field follows the same naming convention as `analyze-enabled` for consistency

**Files to modify:**
- This step establishes the data model foundation but doesn't require actual file changes yet (field will be added when prompts are created or when scripts initialize them)

**Requirements addressed:**
- Based on questionnaire Q3, answer A: Use `plan-enabled` as the field name

### Step 2: Create prompt_plan_on.py action script

**What will be done:**
- Create a new script `.rdd/src/actions/prompt_plan_on.py` that:
  - Accepts optional `prompt-id=<id>` parameter (defaults to active prompt if not provided)
  - Sets the `plan-enabled` field to `true` for the specified prompt
  - Validates that the prompt is not in 'completed' state
  - Automatically disables `analyze-enabled` if it is currently enabled (mutual exclusivity enforcement)
  - Saves the updated registry
  - Provides detailed error messages with remediation steps
- The script will follow the exact pattern used in `prompt_analyze_on.py`

**Files to create:**
- `.rdd/src/actions/prompt_plan_on.py`

**Requirements addressed:**
- Based on questionnaire Q6, answer A: Create action scripts similar to analyze mode
- Based on questionnaire Q2, answer A: Automatically disable one mode when the other is enabled
- Based on questionnaire Q5, answer A: Backend automatically disables the other mode

### Step 3: Create prompt_plan_off.py action script

**What will be done:**
- Create a new script `.rdd/src/actions/prompt_plan_off.py` that:
  - Accepts optional `prompt-id=<id>` parameter (defaults to active prompt if not provided)
  - Sets the `plan-enabled` field to `false` for the specified prompt
  - Saves the updated registry
  - Provides detailed error messages with remediation steps
- The script will follow the exact pattern used in `prompt_analyze_off.py`

**Files to create:**
- `.rdd/src/actions/prompt_plan_off.py`

**Requirements addressed:**
- Based on questionnaire Q6, answer A: Create action scripts similar to analyze mode

### Step 4: Update execution.md to handle plan mode

**What will be done:**
- Modify `.rdd/prompt-snippets/execution.md` to add plan mode check:
  - After checking for analyze mode (step 5), add a new step 5.5 to check for plan mode
  - If `plan-enabled` is true, execute only the plan generation step (`.rdd/prompt-snippets/execution-step.plan.md`)
  - After plan generation completes, automatically disable plan mode by calling `prompt_plan_off.py`
  - Stop execution without proceeding to implementation step
- The check should occur after analyze mode check but before the modifier check
- Plan mode and analyze mode are mutually exclusive - both cannot be enabled simultaneously

**Files to modify:**
- `.rdd/prompt-snippets/execution.md`

**Requirements addressed:**
- Main requirement from prompt: Execute plan step only when plan mode is enabled
- Based on questionnaire Q4, answer A: Automatically disable plan mode after execution

### Step 5: Add Plan Mode toggle column to Web UI prompts table

**What will be done:**
- Modify `.rdd/src/web/static/app.js` to:
  - Add a new table header "Plan Mode" next to the "Analyze Mode" column in the prompts table
  - For each prompt row, display a toggle switch (for non-completed prompts) or "N/A" (for completed prompts)
  - The toggle should show "ON" or "OFF" label based on the `plan-enabled` field value
  - Bind the toggle to a new `togglePlanMode(promptId, enabled)` JavaScript function
- The implementation will mirror the analyze mode toggle implementation

**Files to modify:**
- `.rdd/src/web/static/app.js`

**Requirements addressed:**
- Based on questionnaire Q1, answer A: Add as a new column next to Analyze Mode
- Main requirement from prompt: Provide a switcher in the Web UI

### Step 6: Implement togglePlanMode JavaScript function

**What will be done:**
- Add a new JavaScript function `togglePlanMode(promptId, enabled)` in `.rdd/src/web/static/app.js` that:
  - Calls the appropriate action script (`plan_on` or `plan_off`) via the API
  - Updates the toggle label to reflect the new state
  - Shows success/error alerts
  - Reloads the registry to ensure consistency
  - If plan mode is being enabled and analyze mode is currently on, it will be automatically disabled by the backend
  - Reverts the toggle if the operation fails
- The function will mirror the `toggleAnalyzeMode` implementation

**Files to modify:**
- `.rdd/src/web/static/app.js`

**Requirements addressed:**
- Based on questionnaire Q2, answer A: Backend automatically handles mutual exclusivity
- Web UI integration for plan mode control

### Step 7: Add mutual exclusivity enforcement to plan_on and analyze_on scripts

**What will be done:**
- Update `.rdd/src/actions/prompt_plan_on.py` to:
  - Before enabling plan mode, check if `analyze-enabled` is true
  - If analyze is enabled, set it to false before enabling plan mode
  - Log a message indicating the automatic disable
- Update `.rdd/src/actions/prompt_analyze_on.py` to:
  - Before enabling analyze mode, check if `plan-enabled` is true
  - If plan is enabled, set it to false before enabling analyze mode
  - Log a message indicating the automatic disable

**Files to modify:**
- `.rdd/src/actions/prompt_plan_on.py`
- `.rdd/src/actions/prompt_analyze_on.py`

**Requirements addressed:**
- Main requirement from prompt: Plan mode and analyze mode should not be able to be activated simultaneously
- Based on questionnaire Q2 and Q5, answer A: Automatic mutual exclusivity enforcement

### Step 8: Add plan-on and plan-off actions to CLI menu

**What will be done:**
- Modify `.rdd/src/rdd.py` to add "plan-on" and "plan-off" to the prompt domain action list
- These actions will route to the `prompt_plan_on.py` and `prompt_plan_off.py` scripts
- The implementation mirrors how "analyze-on" and "analyze-off" are currently registered

**Files to modify:**
- `.rdd/src/rdd.py`

**Requirements addressed:**
- Consistency with existing analyze mode implementation
- CLI support for plan mode operations

### Step 9: Update requirements.md with new requirements

**What will be done:**

Add new User Requirements:
- [UR-YYYYMMDD-HHmm] The framework shall provide a plan mode that allows users to generate implementation plans without proceeding to execution, enabling plan review and approval.
- [UR-YYYYMMDD-HHmm] The framework shall automatically disable plan mode after the plan generation completes.
- [UR-YYYYMMDD-HHmm] The framework shall ensure that plan mode and analyze mode are mutually exclusive and cannot be enabled simultaneously for the same prompt.
- [UR-YYYYMMDD-HHmm] The framework shall prevent enabling plan mode for completed prompts.
- [UR-YYYYMMDD-HHmm] The framework shall provide a toggle mechanism to enable/disable plan mode for prompts through the Web UI.

Add new Technical Requirements:
- [TR-YYYYMMDD-HHmm] Each prompt in work-iteration-registry.json shall have a `plan-enabled` boolean field with default value `false`.
- [TR-YYYYMMDD-HHmm] The framework shall provide scripts `prompt_plan_on.py` and `prompt_plan_off.py` in `.rdd/src/actions/` for controlling plan mode.
- [TR-YYYYMMDD-HHmm] The execution prompt logic shall read plan mode from the `plan-enabled` field in work-iteration-registry.json and execute only the plan generation step when enabled.
- [TR-YYYYMMDD-HHmm] The Web UI shall display plan mode toggles only for prompts in draft, planned, or in-progress states.
- [TR-YYYYMMDD-HHmm] The Prompts section table in the Web UI shall include a "Plan Mode" column with a toggle switch for non-completed prompts and "N/A" for completed prompts.
- [TR-YYYYMMDD-HHmm] The CLI prompt domain menu shall include "plan-on" and "plan-off" actions that route to the prompt_plan_on.py and prompt_plan_off.py scripts.
- [TR-YYYYMMDD-HHmm] The plan execution step shall automatically invoke the prompt_plan_off.py script after completing the plan generation to disable the plan flag.
- [TR-YYYYMMDD-HHmm] When enabling plan mode, the system shall automatically disable analyze mode if it is currently enabled, and vice versa, to enforce mutual exclusivity.

**Files to modify:**
- `.rdd-instance/specifications/requirements.md`

**Requirements addressed:**
- Mandatory rule from execution.md: Update requirements.md to reflect changes
- Follows conventions in `.rdd/conventions/requirements.convention.md`

### Step 10: Initialize plan-enabled field for existing prompts

**What will be done:**
- Update the current work iteration registry to add `plan-enabled: false` to all existing prompts that don't have this field
- This ensures backward compatibility and proper functioning for existing prompts

**Files to modify:**
- `.rdd-instance/workdir/work-iteration-registry.json`

**Requirements addressed:**
- Ensures all prompts have the required field before the new functionality is used

### Step 11: Test the implementation

**What will be done:**
- Manually test the following scenarios:
  - Enable plan mode via CLI for a prompt in planned/in-progress state
  - Enable plan mode via Web UI toggle
  - Verify that enabling plan mode disables analyze mode
  - Verify that enabling analyze mode disables plan mode  
  - Verify that plan mode cannot be enabled for completed prompts
  - Execute the framework with plan mode enabled and verify only plan is generated
  - Verify that plan mode is automatically disabled after plan generation
  - Verify Web UI displays plan mode toggle correctly for different prompt states

**Requirements addressed:**
- Quality assurance to ensure all functionality works as expected

## Verification Checklist

After implementation, verify:
- [ ] `plan-enabled` field exists in registry schema
- [ ] `prompt_plan_on.py` script exists and works correctly
- [ ] `prompt_plan_off.py` script exists and works correctly
- [ ] Execution logic checks for plan mode and executes only plan step
- [ ] Plan mode is automatically disabled after plan generation
- [ ] Web UI shows Plan Mode column with toggle switches
- [ ] Toggle switches work and update the registry
- [ ] Mutual exclusivity is enforced (plan and analyze cannot both be on)
- [ ] Plan mode cannot be enabled for completed prompts
- [ ] CLI includes plan-on and plan-off actions
- [ ] Requirements.md is updated with all new requirements
- [ ] All existing prompts have the plan-enabled field initialized

## Dependencies and Risks

**Dependencies:**
- Existing analyze mode implementation serves as the pattern
- Web UI framework and API endpoints are already in place
- Execution flow infrastructure exists

**Risks:**
- Low risk: Implementation follows established patterns
- Potential issue: Ensuring mutual exclusivity is enforced consistently across UI and backend
- Mitigation: Follow the analyze mode pattern closely and test mutual exclusivity thoroughly
