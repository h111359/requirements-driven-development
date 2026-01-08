# Plan for P-008: Move analyze command in the Web UI

## Overview

This plan addresses the requirement to move the analyze modifier from being a chat-based command to a boolean flag in the work-iteration-registry.json file. This change will enable the Web UI to provide a toggle switch for controlling analyze mode and allow scripts to programmatically control this setting.

## Questionnaire Answers Summary

Based on the questionnaire responses:
- Q1: Auto-disable analyze after execution (Answer A - Yes)
- Q2: Hard block for completed prompts (Answer A - prevent enabling)
- Q3: Per-prompt storage (Answer A - each prompt has its own analyze flag)
- Q4: Default value false (Answer A - disabled by default)
- Q5: Remove chat modifier entirely (Answer A - only use registry flag)
- Q6: Scripts location in `.rdd/src/actions/` (Answer D)
- Q7: Simple toggle switch in UI (Answer A)

## Implementation Steps

### Step 1: Update work-iteration-registry.json convention
Update `.rdd/conventions/work-iteration-registry.convention.md` to add a new boolean key `analyze-enabled` to the `prompt-metadata` object schema. This key will default to `false` and indicates whether analyze mode should be enabled for this specific prompt. Document the validation rule that analyze can only be enabled for prompts with state `planned` or `in-progress`, not for `completed` prompts.

### Step 2: Add analyze-enabled field to existing registry
Manually add the `analyze-enabled` field (set to `false`) to all existing prompts in `.rdd-instance/workdir/work-iteration-registry.json` to bring it into compliance with the new convention.

### Step 3: Create prompt_analyze_on.py script
Create `.rdd/src/actions/prompt_analyze_on.py` script that:
- Accepts a `prompt-id=` parameter (optional, defaults to active prompt)
- Reads work-iteration-registry.json
- Validates the prompt exists and is not in `completed` state
- Sets `analyze-enabled` to `true` for the specified prompt
- Writes the updated registry back to disk
- Provides clear error messages with remediation steps

### Step 4: Create prompt_analyze_off.py script
Create `.rdd/src/actions/prompt_analyze_off.py` script that:
- Accepts a `prompt-id=` parameter (optional, defaults to active prompt)
- Reads work-iteration-registry.json
- Sets `analyze-enabled` to `false` for the specified prompt
- Writes the updated registry back to disk
- Provides clear error messages with remediation steps

### Step 5: Update execution.md prompt snippet
Modify `.rdd/prompt-snippets/execution.md` to:
- Remove the `analyze` modifier from the [MODIFIER] definition
- Add new logic to check the `analyze-enabled` flag in the work-iteration-registry.json for the active prompt
- If `analyze-enabled` is `true`, follow the analyze execution path (same as before)
- Remove all references to checking for "analyze" in the chat text

### Step 6: Update execution-step.analyze.md
Modify `.rdd/prompt-snippets/execution-step.analyze.md` to:
- At the end of the analyze execution, add a step to run the `prompt_analyze_off.py` script to automatically turn off the analyze flag
- This ensures analyze is auto-disabled after each execution (per Q1 answer)

### Step 7: Add CLI domain routing for analyze actions
Update `.rdd/src/rdd.py` to add the analyze actions to the CLI routing:
- Add `prompt analyze-on` and `prompt analyze-off` as available actions
- These will route to the scripts created in steps 3 and 4

### Step 8: Update Web UI - Add analyze toggle to Prompts section
Modify `.rdd/src/web/templates/index.html` and `.rdd/src/web/static/app.js` to:
- Add an "Analyze Mode" toggle switch column in the prompts table
- Only show the toggle for prompts with state `draft`, `planned`, or `in-progress` (not for `completed`)
- The toggle should reflect the current `analyze-enabled` value from the registry
- When toggled, call the appropriate API endpoint to execute `prompt_analyze_on.py` or `prompt_analyze_off.py`
- Disable the toggle for the active prompt if it's currently being executed

### Step 9: Update Web UI - Add API endpoint for analyze actions
Modify `.rdd/src/web/server.py` to:
- Add handling in the `/api/action` endpoint for `prompt analyze-on` and `prompt analyze-off` actions
- These will execute the scripts created in steps 3 and 4 via the existing action execution mechanism

### Step 10: Update requirements.md
Add new requirements to `.rdd-instance/specifications/requirements.md`:
- User requirement: The framework shall provide a toggle mechanism to enable/disable analyze mode for prompts through the Web UI
- User requirement: The framework shall automatically disable analyze mode after each analyze execution completes
- User requirement: The framework shall prevent enabling analyze mode for completed prompts
- Technical requirement: Each prompt in work-iteration-registry.json shall have an `analyze-enabled` boolean field (default: false)
- Technical requirement: The framework shall provide scripts `prompt_analyze_on.py` and `prompt_analyze_off.py` in `.rdd/src/actions/` for controlling analyze mode
- Technical requirement: The execution prompt logic shall read analyze mode from the `analyze-enabled` field in work-iteration-registry.json rather than from chat modifiers
- Technical requirement: The Web UI shall display analyze mode toggles only for prompts in draft, planned, or in-progress states

### Step 11: Test the implementation
- Test creating a new prompt (should have analyze-enabled = false by default)
- Test toggling analyze on/off via CLI scripts
- Test toggling analyze on/off via Web UI
- Test that analyze mode executes when flag is true
- Test that analyze mode auto-disables after execution
- Test that completed prompts cannot have analyze enabled (both in UI and via script)
- Test error handling for invalid prompt IDs and edge cases

## Files to be Modified

1. `.rdd/conventions/work-iteration-registry.convention.md` - Add analyze-enabled field documentation
2. `.rdd-instance/workdir/work-iteration-registry.json` - Add analyze-enabled field to existing prompts
3. `.rdd/src/actions/prompt_analyze_on.py` - New script
4. `.rdd/src/actions/prompt_analyze_off.py` - New script
5. `.rdd/prompt-snippets/execution.md` - Remove chat modifier, add registry flag check
6. `.rdd/prompt-snippets/execution-step.analyze.md` - Add auto-disable step
7. `.rdd/src/rdd.py` - Add CLI routing (if not already present via action discovery)
8. `.rdd/src/web/templates/index.html` - Add analyze toggle UI
9. `.rdd/src/web/static/app.js` - Add analyze toggle logic
10. `.rdd/src/web/server.py` - Add analyze action handling
11. `.rdd-instance/specifications/requirements.md` - Add new requirements

## Dependencies and Order

- Steps 1-2 must be completed first (establish the data model)
- Steps 3-4 can be done in parallel (independent scripts)
- Step 5 depends on steps 1-2 (needs the registry field to exist)
- Step 6 depends on step 4 (needs the analyze_off script)
- Step 7 depends on steps 3-4 (needs the scripts to exist)
- Steps 8-9 depend on steps 1-4 (need registry field and scripts)
- Step 10 can be done any time but should be done before completion
- Step 11 must be last (comprehensive testing)

## Requirements Impact

This change aligns with existing requirements and adds new capabilities:
- Supports UR-20251224-0904 (Web UI for managing framework operations)
- Supports TR-20251224-0936 (automation scripts in .rdd/src/)
- Supports TR-20251224-0909 (REST endpoints for RDD commands)
- Enhances the unified execution model (UR-20251224-0905)
- Improves developer experience (UR-20251224-0926)

## Success Criteria

The implementation will be successful when:
1. All prompts in the registry have the analyze-enabled field
2. Scripts can enable/disable analyze mode via CLI
3. Web UI displays analyze toggles and can control the setting
4. Execute command reads analyze mode from registry instead of chat
5. Analyze mode auto-disables after execution
6. Completed prompts cannot have analyze enabled
7. All tests pass
8. Requirements are updated to reflect the changes
