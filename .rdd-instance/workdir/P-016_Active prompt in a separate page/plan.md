# Implementation Plan: Active Prompt in a Separate Page

## Overview
This plan implements a major redesign of the Web UI to separate the active prompt view from the prompts history, introduce execution mode selection (no-action|analyze|plan|implement), add new tracking attributes to the work iteration registry, clean up unused attributes, and create corresponding Python scripts for managing the new attributes.

---

## Step 1: Update Work Iteration Registry Schema

**Objective:** Add new tracking attributes to prompt entries and remove unused attributes.

**Actions:**
1. Add four new boolean attributes to each prompt object in `.rdd-instance/workdir/work-iteration-registry.json`:
   - `questionnaire-generated`: boolean (default: false) - Indicates if questionnaire has been generated
   - `questionnaire-answered`: boolean (default: false) - Indicates if questionnaire is completely answered
   - `plan-generated`: boolean (default: false) - Indicates if plan has been generated
   - `implementation-completed`: boolean (default: false) - Indicates if implementation is completed

2. Remove the following unused nested objects and their sub-attributes from all prompt entries:
   - `analysis` object (with `approval` and `state` sub-attributes)
   - `questionnaire` object (with `approval` and `state` sub-attributes)
   - `plan` object (with `approval` and `state` sub-attributes)

3. Add a new attribute `execution-mode` to each prompt object:
   - Type: string
   - Valid values: "no-action" | "analyze" | "plan" | "implement"
   - Default: "no-action"

4. Update the current active prompt (P-016) and all existing completed prompts in the registry file to include these new attributes with appropriate default values.

**Rationale:** This simplifies the registry structure, removes complexity that was not being used, and adds clear tracking for the states that matter (questionnaire generation/completion, plan generation, implementation completion). The execution-mode attribute makes the current mode explicit and persistent.

---

## Step 2: Create Python Scripts for Managing New Attributes

**Objective:** Create action scripts for setting and unsetting the new boolean attributes.

**Actions:**
Create the following Python scripts in `.rdd/src/actions/` following the pattern of existing `prompt_analyze_on.py` and `prompt_analyze_off.py`:

1. `prompt_questionnaire_generated_on.py` - Sets `questionnaire-generated` to true for active prompt
2. `prompt_questionnaire_generated_off.py` - Sets `questionnaire-generated` to false for active prompt
3. `prompt_questionnaire_answered_on.py` - Sets `questionnaire-answered` to true for active prompt
4. `prompt_questionnaire_answered_off.py` - Sets `questionnaire-answered` to false for active prompt
5. `prompt_plan_generated_on.py` - Sets `plan-generated` to true for active prompt
6. `prompt_plan_generated_off.py` - Sets `plan-generated` to false for active prompt
7. `prompt_implementation_completed_on.py` - Sets `implementation-completed` to true for active prompt
8. `prompt_implementation_completed_off.py` - Sets `implementation-completed` to false for active prompt
9. `prompt_set_execution_mode.py` - Sets the `execution-mode` attribute for active prompt, accepts parameter `mode=` with values: no-action|analyze|plan|implement

**Script Implementation Details:**
- All scripts should follow the same pattern as existing prompt action scripts
- Load the work iteration registry JSON file
- Find the active prompt
- Update the specific attribute
- Save the registry back to file
- Print success message
- Handle errors gracefully with clear error messages

**Rationale:** These scripts provide deterministic, scriptable control over the new attributes, consistent with the framework's design principle that prompts call scripts for modifications rather than implementing logic directly.

---

## Step 3: Update Backend API Endpoints

**Objective:** Modify the web server to support new attributes and execution mode setting.

**Actions:**
1. Update `.rdd/src/web/server.py` to expose the new action scripts:
   - Add routes for all new `prompt_*_on.py` and `prompt_*_off.py` scripts
   - Add route for `prompt_set_execution_mode.py` with mode parameter support

2. Ensure the `/api/registry` endpoint returns the new attributes when fetching the work iteration registry

3. Ensure the `/api/action` POST endpoint can invoke the new scripts with appropriate parameters

**Rationale:** The backend needs to support the new functionality and make it accessible via the Web UI.

---

## Step 4: Redesign Frontend Navigation and Structure

**Objective:** Implement two separate pages - "Prompts History" and "Active Prompt" - with proper navigation.

**Actions:**
1. Modify `.rdd/src/web/templates/index.html`:
   - Add two main navigation tabs in the navbar: "Prompts History" and "Active Prompt"
   - Keep existing "Workdir", "Git", and "Files" sections as they are

2. Create two main view containers:
   - `#prompts-history-view` - For the Prompts History page
   - `#active-prompt-view` - For the Active Prompt page

3. Implement tab switching logic in `.rdd/src/web/static/app.js`:
   - Show/hide appropriate views based on selected tab
   - Load data when switching to each tab

**Rationale:** This provides clear separation between historical prompts and the current active work, as specified in the prompt requirements. Following the questionnaire answer for Question 1 (Option A), we implement separate tabs for clear separation and easy switching.

---

## Step 5: Implement Prompts History Page

**Objective:** Create the Prompts History page showing only completed prompts with simplified interface.

**Actions:**
1. In the HTML template, create the Prompts History view section with:
   - Table showing completed prompts with columns:
     - Prompt ID
     - Title
     - Questionnaire indicator (badge showing if generated/answered)
     - Plan indicator (badge showing if generated)
     - Implementation indicator (badge showing if completed)
     - View button (opens modal with questionnaire, plan, implementation files)
   - "Create New Prompt" button at the top

2. Remove from Prompts History page (these were in the old Prompts section):
   - State column
   - Analyze Mode toggle
   - Plan Mode toggle
   - State change buttons
   - Complete button

3. Badge/Indicator styling (following questionnaire answers):
   - Gray badge: Not generated/not completed
   - Green badge: Generated/completed
   - Use icon-based indicators with color coding (Question 4, Option D)

4. Implement the View button functionality:
   - Reuse existing modal dialog that shows questionnaire.md, plan.md, and implementation.md
   - Make all files read-only in this view since prompts are completed

5. Filter prompts to show only those with `state: "completed"`

**Rationale:** This creates a clean, focused history view that shows only completed work and provides quick visual feedback about what was generated for each prompt. Following the questionnaire answer for Question 10 (Option C), we show detailed information with indicators.

---

## Step 6: Implement Active Prompt Page

**Objective:** Create the Active Prompt page with execution mode selection and status indicators.

**Actions:**
1. In the HTML template, create the Active Prompt view section with:
   - Prompt title and ID display
   - Mode selection component (button group with 4 buttons: no-action, analyze, plan, implement)
   - Status indicators section showing:
     - Questionnaire status (with icon and color: gray = not generated, yellow = generated but not answered, green = answered)
     - Plan status (with icon and color: gray = not generated, green = generated)
     - Implementation status (with icon and color: gray = not completed, green = completed)
   - Prompt editor (reuse existing tabbed interface for prompt.md, plan.md, questionnaire.md, implementation.md)

2. Mode Selection Component (following questionnaire Question 2, Option B):
   - Implement as button group (Bootstrap's btn-group style)
   - Four mutually exclusive buttons: "No Action", "Analyze", "Plan", "Implement"
   - Active state highlighting for selected mode
   - Clicking a button immediately updates the `execution-mode` attribute in the registry

3. Status Indicators (following questionnaire Question 4, Option D):
   - Use icon-based indicators (checkmark, warning, clock icons) with color coding
   - Questionnaire status colors:
     - Gray (#CCCCCC): Not generated (following Question 3, Option A)
     - Yellow: Generated but not answered (following Question 5, Option D - show "In Progress")
     - Green: Answered (following Question 5, Option D - show "Complete")
   - Plan status colors:
     - Gray: Not generated
     - Green: Generated
   - Implementation status colors:
     - Gray: Not completed
     - Green: Completed

4. Default Mode (following questionnaire Question 8, Option B):
   - Implement smart default based on current state:
     - If questionnaire not generated → "analyze"
     - Else if plan not generated → "plan"
     - Else if implementation not completed → "implement"
     - Else → "no-action"

5. Handle case when no active prompt exists:
   - Display message: "No active prompt. Create a new prompt from the Prompts History page."
   - Disable/hide the mode selection and status indicators

**Rationale:** This creates a focused workspace for the active prompt, provides clear visual feedback about current state, and allows the user to select the execution mode that will be used by the execute command. Following the questionnaire answer for Question 9 (Option E), mode selection updates the registry but doesn't trigger execution (execution happens in VS Code).

---

## Step 7: Update Frontend JavaScript Logic

**Objective:** Implement all the client-side logic for the new UI.

**Actions:**
1. In `.rdd/src/web/static/app.js`, implement:
   - `loadPromptsHistory()` - Loads and displays completed prompts in the history view
   - `loadActivePrompt()` - Loads and displays the active prompt with status indicators
   - `updateExecutionMode(mode)` - Calls the backend to update execution-mode attribute
   - `renderStatusIndicators(prompt)` - Renders status badges based on prompt attributes
   - `renderModeSelector(currentMode)` - Renders the mode selection button group
   - Tab switching logic between History and Active Prompt views

2. Update existing functions:
   - Modify `loadPrompts()` to work specifically for the history view
   - Keep existing prompt editor functions but ensure they load from the active prompt's folder

3. Implement mode selection handler:
   - When user clicks a mode button, call API to execute `prompt_set_execution_mode.py` with the selected mode
   - Update the UI to reflect the selected mode
   - Show success/error messages

4. Implement status indicator logic:
   - Read the new boolean attributes from the registry
   - Determine colors and icons based on attribute values
   - Update indicators dynamically when registry changes

5. Remove old functionality:
   - Remove analyze mode toggle from Prompts table
   - Remove plan mode toggle from Prompts table
   - Remove state change dropdowns
   - Update Complete button logic (it may need to be moved or adjusted)

**Rationale:** This implements all the interactive behavior needed for the new UI design, ensuring smooth user experience and proper integration with the backend.

---

## Step 8: Update CLI to Support New Actions

**Objective:** Add CLI commands for the new attribute management scripts.

**Actions:**
1. Verify that the CLI router in `.rdd/src/rdd.py` will automatically discover and route to the new action scripts (it should work by convention)

2. Test CLI commands like:
   - `python .rdd/src/rdd.py prompt questionnaire-generated-on`
   - `python .rdd/src/rdd.py prompt set-execution-mode mode=analyze`

3. If needed, update the help text or menu options to include the new actions

**Rationale:** Ensures the new functionality is accessible via both Web UI and CLI, maintaining consistency across interfaces.

---

## Step 9: Update Execution Prompt Logic

**Objective:** Modify the execution flow to read and respect the new execution-mode attribute.

**Actions:**
1. Update `.rdd/prompt-snippets/execution.md` to:
   - Read the `execution-mode` attribute from the work iteration registry
   - Based on the mode value:
     - `no-action`: Do nothing, inform user that no action mode is selected
     - `analyze`: Follow instructions in `execution-step.analyze.md` (existing)
     - `plan`: Follow instructions in `execution-step.plan.md` (existing)
     - `implement`: Follow instructions in `execution-step.implementation.md` (existing)

2. Remove the current logic that checks for `analyze-enabled` and `plan-enabled` boolean flags, replace with execution-mode checking

3. Keep the modifier-based execution (e.g., "modification <ID>") as a separate override that works regardless of execution mode

4. Update the automatic disabling logic:
   - After analyze completes: set execution-mode to "no-action" (instead of calling prompt_analyze_off.py) by executing in the terminal the respective action
   - After plan completes: set execution-mode to "no-action" (instead of calling prompt_plan_off.py) by executing in the terminal the respective action
   - After implementation completes: set execution-mode to "no-action" , set `implementation-completed` to true by executing in the terminal the respective action

**Rationale:** This simplifies the execution logic by using a single mode attribute instead of separate boolean flags, making the system more intuitive and maintainable. The mode clearly indicates what the execute command will do.

---

## Step 10: Update Conventions and Documentation

**Objective:** Document the new registry structure and remove references to old attributes.

**Actions:**
1. Check if there's a convention file for the work iteration registry structure
2. If it exists, update it to:
   - Document the new attributes: questionnaire-generated, questionnaire-answered, plan-generated, implementation-completed, execution-mode
   - Remove documentation for: analysis, questionnaire, plan nested objects
   - Remove documentation for: analyze-enabled, plan-enabled boolean flags

3. Update any README or documentation files that reference the old structure

4. Update any example or template files that show the registry structure

**Rationale:** Keeps documentation in sync with the actual implementation, preventing confusion for future development.

---

## Step 11: Test and Validate

**Objective:** Ensure all new functionality works correctly.

**Actions:**
1. Manual testing:
   - Create a new prompt, verify it has all new attributes with default values
   - Switch between execution modes in the Web UI, verify registry updates
   - Check status indicators update correctly
   - Test the Prompts History view with multiple completed prompts
   - Test the Active Prompt view with an active prompt
   - Verify the execute command respects the execution-mode

2. Verify data migration:
   - Check that P-016 and all existing prompts have been updated with new attributes
   - Verify no old attributes remain in the registry

3. Test error cases:
   - Try to set invalid execution mode
   - Try to access Active Prompt when no prompt is active

4. Test backwards compatibility:
   - Ensure completed prompts still display correctly
   - Ensure existing functionality (like create prompt, set state) still works

**Rationale:** Thorough testing ensures the redesign works as intended and doesn't break existing functionality.

---

## Requirements Updates

The following updates should be made to `.rdd-instance/specifications/requirements.md`:

### New User Requirements to Add:

1. Add after [UR-20251224-0935]:
```
- [UR-20260101-1200] The Web UI shall provide separate pages for "Prompts History" showing completed prompts and "Active Prompt" showing the currently active prompt with execution mode selection and status indicators.

- [UR-20260101-1201] The Active Prompt page shall display status indicators for questionnaire (not generated/generated but not answered/answered), plan (not generated/generated), and implementation (not completed/completed) using icon-based visual indicators with color coding.

- [UR-20260101-1202] The Active Prompt page shall provide execution mode selection (no-action, analyze, plan, implement) allowing users to control what the execute command will do with the active prompt.

- [UR-20260101-1203] The Prompts History page shall display only completed prompts with visual indicators showing which artifacts (questionnaire, plan, implementation) were generated for each prompt.

- [UR-20260101-1204] The framework shall track questionnaire generation status, questionnaire completion status, plan generation status, and implementation completion status for each prompt.
```

### New Technical Requirements to Add:

1. Add after [TR-20260101-1000]:
```
- [TR-20260101-1200] Each prompt object in work-iteration-registry.json shall include boolean attributes: `questionnaire-generated`, `questionnaire-answered`, `plan-generated`, and `implementation-completed`, all defaulting to false.

- [TR-20260101-1201] Each prompt object in work-iteration-registry.json shall include an `execution-mode` string attribute with valid values "no-action", "analyze", "plan", or "implement", defaulting to "no-action".

- [TR-20260101-1202] The framework shall provide Python scripts in `.rdd/src/actions/` for managing the new attributes: `prompt_questionnaire_generated_on.py`, `prompt_questionnaire_generated_off.py`, `prompt_questionnaire_answered_on.py`, `prompt_questionnaire_answered_off.py`, `prompt_plan_generated_on.py`, `prompt_plan_generated_off.py`, `prompt_implementation_completed_on.py`, `prompt_implementation_completed_off.py`, and `prompt_set_execution_mode.py`.

- [TR-20260101-1203] The execution prompt logic shall read the `execution-mode` attribute from work-iteration-registry.json to determine which execution step to perform (analyze, plan, or implement).

- [TR-20260101-1204] The Web UI shall implement a button group component for execution mode selection on the Active Prompt page, with immediate persistence of mode changes to the work iteration registry.

- [TR-20260101-1205] The Web UI status indicators shall use color coding: gray for not generated/not completed states, yellow for generated but not answered (questionnaire only), and green for generated/completed states.

- [TR-20260101-1206] The Web UI shall display icon-based status indicators using standard icons (checkmark for complete, warning/clock for in-progress, gray icons for not started).
```

### Requirements to Modify:

1. Modify [TR-20251230-2006]:
```
OLD: The execution prompt logic shall read analyze mode from the `analyze-enabled` field in work-iteration-registry.json rather than from chat modifiers.

NEW: The execution prompt logic shall read the execution mode from the `execution-mode` field in work-iteration-registry.json to determine what action to perform.
```

2. Modify [TR-20251231-0202]:
```
OLD: The execution prompt logic shall read plan mode from the `plan-enabled` field in work-iteration-registry.json and execute only the plan generation step when enabled.

NEW: The execution prompt logic shall execute only the plan generation step when the `execution-mode` is set to "plan".
```

### Requirements to Mark as Deleted:

1. Mark the following requirements as [DELETED] since they reference the old attribute structure:
   - [TR-20251230-2004] - References analyze-enabled field
   - [TR-20251230-2007] - References analyze mode toggles in wrong location
   - [TR-20251230-2008] - References Analyze Mode column in Prompts table
   - [TR-20251230-2009] - References analyze-on/off CLI actions (replaced by execution-mode setting)
   - [TR-20251230-2010] - References automatic analyze flag disabling (replaced by mode setting)
   - [TR-20251231-0200] - References plan-enabled field
   - [TR-20251231-0203] - References plan mode toggles in wrong location
   - [TR-20251231-0204] - References Plan Mode column in Prompts table
   - [TR-20251231-0205] - References plan-on/off CLI actions (replaced by execution-mode setting)
   - [TR-20251231-0206] - References automatic plan flag disabling (replaced by mode setting)
   - [TR-20251231-0207] - References mutual exclusivity enforcement (now handled by single execution-mode)

---

## Summary

This plan implements a comprehensive redesign of the Web UI to:
1. Separate active prompt management from historical prompt viewing
2. Replace boolean flags (analyze-enabled, plan-enabled) with a unified execution-mode attribute
3. Add explicit tracking for questionnaire, plan, and implementation states
4. Clean up unused attributes from the registry schema
5. Provide clear visual feedback about prompt status and execution mode
6. Create all necessary Python scripts for managing the new attributes
7. Update requirements documentation to reflect the new design

The implementation follows the questionnaire answers provided by the user and maintains consistency with the framework's design principles of using scripts for deterministic actions and maintaining simple file-based data storage.
