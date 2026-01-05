# Implementation Log for P-012: Plan Mode

## Implementation Date
December 31, 2025

## Overview
This log documents the implementation of the Plan Mode feature, which allows users to generate implementation plans without proceeding to actual execution.

## Implementation Steps Completed

### Step 1: Created prompt_plan_on.py action script
**File:** `.rdd/src/actions/prompt_plan_on.py`

**Details:**
- Created a new Python script that enables plan mode for prompts
- Accepts optional `prompt-id=<id>` parameter (defaults to active prompt)
- Sets `plan-enabled` field to `true` in the work iteration registry
- Validates that the prompt is not in 'completed' state
- Automatically disables `analyze-enabled` if currently enabled (mutual exclusivity)
- Provides detailed error messages with remediation steps
- Follows the same pattern as `prompt_analyze_on.py`

**Key Features:**
- Mutual exclusivity enforcement with analyze mode
- Active prompt detection when no prompt-id specified
- Comprehensive error handling
- User-friendly success and error messages

### Step 2: Created prompt_plan_off.py action script
**File:** `.rdd/src/actions/prompt_plan_off.py`

**Details:**
- Created a new Python script that disables plan mode for prompts
- Accepts optional `prompt-id=<id>` parameter (defaults to active prompt)
- Sets `plan-enabled` field to `false` in the work iteration registry
- Provides detailed error messages with remediation steps
- Follows the same pattern as `prompt_analyze_off.py`

**Key Features:**
- Active prompt detection when no prompt-id specified
- Comprehensive error handling
- User-friendly success and error messages

### Step 3: Updated prompt_analyze_on.py for mutual exclusivity
**File:** `.rdd/src/actions/prompt_analyze_on.py`

**Modification:**
- Added code to check if `plan-enabled` is true before enabling analyze mode
- Automatically disables plan mode when analyze mode is being enabled
- Logs an informational message about the automatic disable

**Code Added (lines ~103-106):**
```python
# Enforce mutual exclusivity: disable plan mode if enabled
if target_prompt.get('plan-enabled', False):
    print(f"INFO: Automatically disabling plan mode for prompt '{prompt_id}' (mutual exclusivity)")
    target_prompt['plan-enabled'] = False
```

### Step 4: Updated execution.md to handle plan mode
**File:** `.rdd/prompt-snippets/execution.md`

**Modification:**
- Added new step 5.5 to check for plan mode after analyze mode check
- When `plan-enabled` is true:
  - Display "Plan mode" message in chat
  - Execute only the plan generation step (`.rdd/prompt-snippets/execution-step.plan.md`)
  - Automatically disable plan mode by calling `prompt_plan_off.py`
  - Stop execution without proceeding to implementation step

**Code Added (after step 5, before step 6):**
```markdown
5.5. Check if the active prompt has `plan-enabled` set to `true` in [WI-REGISTRY]. If it is set to true:
   * Write in the chat "Plan mode" 
   * then follow the instructions in `.rdd/prompt-snippets/execution-step.plan.md`
   * after the plan execution is completed, execute `.rdd/src/actions/prompt_plan_off.py` to automatically disable plan mode
   * stop (do not continue with the next instructions here - do not execute implementation step)
```

### Step 5: Added Plan Mode column to Web UI
**File:** `.rdd/src/web/static/app.js`

**Modifications:**

1. **Table Header** (line ~183):
   - Added "Plan Mode" column header after "Analyze Mode"

2. **Data Extraction** (line ~196):
   - Added `const planEnabled = prompt['plan-enabled'] || false;` to extract plan mode status

3. **Plan Mode Toggle HTML** (lines ~227-241):
   - Created plan toggle HTML similar to analyze toggle
   - Shows toggle switch for non-completed prompts
   - Shows "N/A" for completed prompts
   - Toggle displays "ON" or "OFF" based on current state
   - Calls `togglePlanMode()` function on change

4. **Table Row** (line ~273):
   - Added `<td>${planToggleHtml}</td>` to display plan mode column

### Step 6: Implemented togglePlanMode JavaScript function
**File:** `.rdd/src/web/static/app.js`

**Details:**
- Added new function `togglePlanMode(promptId, enabled)` after `toggleAnalyzeMode()`
- Calls appropriate action (`plan_on` or `plan_off`) via API
- Updates toggle label to reflect new state
- Shows success/error alerts
- Reloads registry to ensure consistency (updates both plan and analyze toggles)
- Reverts toggle if operation fails

**Function Added (lines ~467-499):**
```javascript
async function togglePlanMode(promptId, enabled) {
    const action = enabled ? 'plan_on' : 'plan_off';
    const params = {
        'prompt-id': promptId
    };
    
    const result = await executeAction('prompt', action, params);
    
    if (result.success) {
        showAlert('success', `Plan mode ${enabled ? 'enabled' : 'disabled'} for prompt ${promptId}`);
        
        // Update the label next to the toggle
        const toggleId = `plan-toggle-${promptId}`;
        const toggleElement = document.getElementById(toggleId);
        if (toggleElement) {
            const label = toggleElement.nextElementSibling;
            if (label) {
                label.textContent = enabled ? 'ON' : 'OFF';
            }
        }
        
        // Reload registry to ensure consistency
        await loadRegistry();
    } else {
        showAlert('danger', `Failed to ${enabled ? 'enable' : 'disable'} plan mode: ` + (result.error || result.stderr));
        
        // Revert the toggle state
        const toggleId = `plan-toggle-${promptId}`;
        const toggleElement = document.getElementById(toggleId);
        if (toggleElement) {
            toggleElement.checked = !enabled;
        }
    }
}
```

### Step 7: Added plan-on and plan-off to CLI
**File:** `.rdd/src/rdd.py`

**Modifications:**

1. **Parameter Specifications** (lines ~210-215):
   - Added parameter specs for `prompt.plan-on` and `prompt.plan-off`
   - Both accept optional `prompt-id` parameter

2. **Prompt Domain Menu** (lines ~323-324):
   - Added "plan-on" and "plan-off" to the prompt domain action list
   - Descriptions: "Enable plan mode for a prompt" and "Disable plan mode for a prompt"

**Code Added:**
```python
"prompt.plan-on": [
    {"name": "prompt-id", "prompt": "Enter prompt ID (or leave empty for active prompt)", "required": False},
],
"prompt.plan-off": [
    {"name": "prompt-id", "prompt": "Enter prompt ID (or leave empty for active prompt)", "required": False},
],
```

```python
{"key": "plan-on", "desc": "Enable plan mode for a prompt"},
{"key": "plan-off", "desc": "Disable plan mode for a prompt"},
```

### Step 8: Initialized plan-enabled field for existing prompts
**Command executed:**
```bash
python -c "
import json
registry_path = '.rdd-instance/workdir/work-iteration-registry.json'
with open(registry_path, 'r', encoding='utf-8') as f:
    registry = json.load(f)
for prompt in registry['prompts']:
    if 'plan-enabled' not in prompt:
        prompt['plan-enabled'] = False
with open(registry_path, 'w', encoding='utf-8') as f:
    json.dump(registry, f, indent=4, ensure_ascii=False)
print('Successfully added plan-enabled field to all prompts')
"
```

**Result:**
- Successfully added `plan-enabled: false` to all 12 existing prompts in the registry
- Ensures backward compatibility

### Step 9: Updated requirements.md
**File:** `.rdd-instance/specifications/requirements.md`

**Added New Section:** "## Plan Mode Requirements"

**New User Requirements (UR-20251231-02XX):**
- [UR-20251231-0200] Plan mode feature for generating plans without execution
- [UR-20251231-0201] Automatic plan mode disable after plan generation
- [UR-20251231-0202] Mutual exclusivity between plan and analyze modes
- [UR-20251231-0203] Prevent enabling plan mode for completed prompts
- [UR-20251231-0204] Toggle mechanism in Web UI for plan mode

**New Technical Requirements (TR-20251231-02XX):**
- [TR-20251231-0200] `plan-enabled` boolean field in registry with default false
- [TR-20251231-0201] Scripts `prompt_plan_on.py` and `prompt_plan_off.py`
- [TR-20251231-0202] Execution logic reads plan mode and executes only plan step
- [TR-20251231-0203] Web UI displays toggles only for non-completed prompts
- [TR-20251231-0204] Plan Mode column in Web UI prompts table
- [TR-20251231-0205] CLI plan-on and plan-off actions
- [TR-20251231-0206] Automatic plan mode disable after execution
- [TR-20251231-0207] Mutual exclusivity enforcement in backend

## Files Created
1. `.rdd/src/actions/prompt_plan_on.py` - 144 lines
2. `.rdd/src/actions/prompt_plan_off.py` - 124 lines

## Files Modified
1. `.rdd/src/actions/prompt_analyze_on.py` - Added mutual exclusivity check
2. `.rdd/prompt-snippets/execution.md` - Added plan mode execution step
3. `.rdd/src/web/static/app.js` - Added Plan Mode column and toggle function
4. `.rdd/src/rdd.py` - Added plan-on and plan-off CLI actions
5. `.rdd-instance/workdir/work-iteration-registry.json` - Added plan-enabled field to all prompts
6. `.rdd-instance/specifications/requirements.md` - Added Plan Mode requirements section

## Testing Considerations

The following scenarios should be tested:
1. Enable plan mode via CLI for a prompt
2. Enable plan mode via Web UI toggle
3. Verify mutual exclusivity: enabling plan mode disables analyze mode
4. Verify mutual exclusivity: enabling analyze mode disables plan mode
5. Verify plan mode cannot be enabled for completed prompts
6. Execute framework with plan mode enabled and verify only plan is generated
7. Verify plan mode is automatically disabled after plan generation
8. Verify Web UI displays plan mode toggle correctly for different states

## Implementation Summary

The Plan Mode feature has been fully implemented following the established patterns from Analyze Mode. The implementation includes:

- ✅ Backend action scripts for enabling/disabling plan mode
- ✅ Mutual exclusivity enforcement between plan and analyze modes
- ✅ Updated execution flow to handle plan mode
- ✅ Web UI column and toggle for plan mode
- ✅ CLI integration with plan-on and plan-off actions
- ✅ Registry field initialization for backward compatibility
- ✅ Complete requirements documentation

The feature is ready for testing and use.
