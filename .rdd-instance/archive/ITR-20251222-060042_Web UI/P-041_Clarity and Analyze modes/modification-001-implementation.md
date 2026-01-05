# Modification 001 Implementation

## Objective
Make the icons of statuses to be right above the buttons for the execution modes and to reflect the respective mode. Clarify will have two icons - for generated and answered.

## Implementation Steps

### Step 1: Analyze current structure
The current implementation in `.rdd/src/web/templates/index.html` shows:
- Execution mode buttons are in a button group (lines 135-167)
- Workflow status flags are displayed below the buttons in a single row (lines 170-203)

Current mapping of workflow status flags:
- flag-questionnaire-generated
- flag-questionnaire-answered
- flag-plan-generated
- flag-analysis-generated
- flag-implementation-completed
- flag-executed
- flag-modifications-count
- flag-current-modification

### Step 2: Design new layout structure
The new structure should have icons above each execution mode button:
- **No Action**: No icons
- **Clarify**: Two icons (questionnaire-generated, questionnaire-answered)
- **Analyze**: One icon (analysis-generated)
- **Plan**: One icon (plan-generated)
- **Implement**: Two icons (implementation-completed, executed)
- **Modification**: Modification indicators (modifications-count, current-modification)

The "executed" flag is placed with the Implement mode since execution happens after implementation.

### Step 3: Restructure HTML
Replace the button group structure to include icons above each button. Each execution mode button will be wrapped in a container that also contains its status icons.

### Step 4: Update CSS (if needed)
May need to add CSS to properly align and style the icons above buttons.

### Step 5: Update JavaScript
The `updateWorkflowFlags()` function in `.rdd/src/web/static/app.js` remains largely the same since the flag IDs don't change.

## Detailed Implementation

### Changed index.html

Replaced the execution mode selector section (lines 135-203) with a new structure where each button has its icons displayed above it.

**Changes made:**
1. Removed the `btn-group` wrapper which forced buttons to be grouped together
2. Created individual flex containers for each execution mode button
3. Each container has two parts:
   - A top section (20px height) for status icons
   - A bottom section for the button itself
4. Icon distribution per mode:
   - No Action: Empty space (no icons)
   - Clarify: questionnaire-generated + questionnaire-answered
   - Analyze: analysis-generated
   - Plan: plan-generated
   - Implement: implementation-completed + executed
   - Modification: modifications-count + current-modification
5. Changed button size from default to `btn-sm` for consistency
6. Removed the separate "Workflow Status Flags" section that was below the buttons

The JavaScript code in `app.js` (`updateWorkflowFlags()` function) remains unchanged since all the flag IDs are preserved.

### Testing considerations

After this change:
- The Web UI should be tested to ensure icons appear correctly above buttons
- Icons should update dynamically when workflow state changes
- Tooltips should still work when hovering over icons
- Button clicks should still properly set the execution mode

## Requirements Update

Updated requirement [UR-20260104-1400] in `.rdd-instance/specifications/requirements.md` to reflect the new icon positioning:

**Previous text:**
"The Web UI Active Prompt page shall display visual indicators for prompt workflow state flags in the buttons row area, showing the status of questionnaire-generated, questionnaire-answered, plan-generated, implementation-completed, and executed boolean flags, as well as displaying modifications-count and current-modification-id values with short labels to provide immediate visibility of the prompt's lifecycle state without requiring navigation through tabs or registry inspection."

**Updated text:**
"The Web UI Active Prompt page shall display visual indicators for prompt workflow state flags positioned directly above their corresponding execution mode buttons, with each execution mode showing relevant status icons (Clarify mode displaying questionnaire-generated and questionnaire-answered icons, Analyze mode displaying analysis-generated icon, Plan mode displaying plan-generated icon, Implement mode displaying implementation-completed and executed icons, and Modification mode displaying modifications-count and current-modification-id values), providing immediate visibility of the prompt's lifecycle state aligned with each mode's function."

**Rationale for update:**
The modification changed the positioning of status icons from a separate row below the buttons to individual icon containers directly above each execution mode button. The requirement needed to be updated to accurately reflect this new layout and to explicitly document which icons correspond to which execution modes. This provides better clarity for future developers and ensures the requirement accurately describes the implemented behavior.

## Summary

The modification successfully reorganized the Web UI layout to place workflow status icons directly above their corresponding execution mode buttons. The key changes were:

1. Restructured HTML to use flex containers for each mode with icons on top
2. Distributed icons logically across modes based on their function
3. Updated the relevant user requirement to reflect the new design
4. Maintained all existing functionality and IDs for JavaScript compatibility

No JavaScript changes were required since all element IDs were preserved.


