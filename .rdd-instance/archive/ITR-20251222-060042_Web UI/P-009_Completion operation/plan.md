# Implementation Plan for P-009: Completion Operation

## Step 1: Add git-enabled flag to work iteration registry
Add a new root-level boolean field `"git-enabled"` to the work iteration registry JSON structure at `.rdd-instance/workdir/work-iteration-registry.json`. This field will control whether git operations should be executed during prompt completion. Default value should be `false` to maintain backward compatibility.

## Step 2: Add executed flag to each prompt in registry
Extend each prompt object in the work iteration registry with a new boolean field `"executed"` with default value `false`. This field indicates whether the prompt has been executed through the framework's workflow.

## Step 3: Create prompt_set_executed_on.py action script
Create a new Python script at `.rdd/src/actions/prompt_set_executed_on.py` that:
- Accepts an optional `prompt-id=` parameter (defaults to active prompt if not provided)
- Validates that the specified prompt exists in the registry
- Sets the `executed` field to `true` for the specified prompt
- Saves the updated registry back to disk
- Provides clear error messages if the prompt doesn't exist or other errors occur

## Step 4: Create prompt_complete.py action script
Create a new Python script at `.rdd/src/actions/prompt_complete.py` that:
- Accepts an optional `prompt-id=` parameter (defaults to active prompt if not provided)
- Validates that the specified prompt exists in the registry
- Changes the prompt's state to "completed"
- Checks the root-level `git-enabled` flag in the registry
- If `git-enabled` is `true`, executes `.rdd/src/actions/git_commit.py` using subprocess
- If git commit fails due to no changes, logs a warning but continues with the state change
- Saves the updated registry after state change
- Provides clear error messages for various failure scenarios

## Step 5: Update Web UI to display executed flag
Modify `.rdd/src/web/static/app.js` to:
- Display the `executed` status for each prompt in the prompts table (e.g., with a checkmark icon or badge)
- Read this status from the registry data when loading prompts

## Step 6: Add Complete button to Web UI
Modify `.rdd/src/web/static/app.js` to:
- Add a "Complete" button in the Actions column for each prompt row
- The button should only be visible for prompts with state "in-progress"
- The button should only be enabled when the prompt's `executed` flag is `true`
- When clicked, the button should call the `/api/action` endpoint with action "prompt_complete" and the prompt-id
- Display success or error messages based on the API response
- Reload the prompts table after successful completion

## Step 7: Update requirements.md
Add the following new requirements to `.rdd-instance/specifications/requirements.md`:

**User Requirements section:**
- [UR-20251231-XXXX] The framework shall provide a mechanism to mark prompts as executed and track execution status in the work iteration registry.
- [UR-20251231-XXXX] The framework shall provide a prompt completion command that transitions prompts to completed state and optionally triggers git commit operations.
- [UR-20251231-XXXX] The Web UI shall display execution status for each prompt and provide a completion button that is enabled only for executed prompts in in-progress state.
- [UR-20251231-XXXX] The framework shall support optional git integration during prompt completion, controlled by a global configuration flag.

**Technical Requirements section:**
- [TR-20251231-XXXX] The work iteration registry shall include a root-level boolean field `git-enabled` (default: false) to control git operations during prompt completion.
- [TR-20251231-XXXX] Each prompt object in the work iteration registry shall include an `executed` boolean field (default: false) to track execution status.
- [TR-20251231-XXXX] The framework shall provide a script `.rdd/src/actions/prompt_set_executed_on.py` that sets the executed flag for a specified prompt or the active prompt.
- [TR-20251231-XXXX] The framework shall provide a script `.rdd/src/actions/prompt_complete.py` that sets a prompt to completed state and conditionally executes git commit based on the git-enabled flag.
- [TR-20251231-XXXX] The prompt completion action shall handle git commit failures gracefully, logging warnings but proceeding with state changes when no repository changes exist.
- [TR-20251231-XXXX] The Web UI shall display prompt execution status and provide completion controls only for prompts in in-progress state with executed flag set to true.

## Step 8: Test the implementation
Manually test the complete workflow:
- Set git-enabled flag in the registry
- Create a test prompt and set it to in-progress
- Mark it as executed using prompt_set_executed_on.py
- Verify the Complete button appears and is enabled in the Web UI
- Test completion with and without git changes
- Verify proper error handling for edge cases
