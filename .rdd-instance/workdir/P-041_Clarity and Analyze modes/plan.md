## Plan for Implementing Clarity and Analyze Modes

### Step 1: Rename execution-step.analyze.md to execution-step.clarify.md

Rename the file `.rdd/prompt-snippets/execution-step.analyze.md` to `.rdd/prompt-snippets/execution-step.clarify.md`. This file currently contains the questionnaire generation logic and will continue to serve that purpose under the new "clarify" mode name. No changes to the content of this file are needed at this stage since we are retaining all existing behavior (as per questionnaire answer Q1-opt1).

**Rationale**: The current "analyze" mode generates questionnaires to clarify ambiguities. This functionality will be renamed to "clarify" to better reflect its purpose, making room for a new "analyze" mode.

---

### Step 2: Create new execution-step.analyze.md for analysis mode

Create a new file `.rdd/prompt-snippets/execution-step.analyze.md` based on the content from `.rdd/prompt-snippets/analyze.md`. The new file should follow the structure of other execution-step files (with Definitions and Instructions sections) and should:

1. Include a "Definitions" section referencing `.rdd/prompt-snippets/execution.md`
2. Include an "Execution Step Instructions" section with the analysis generation logic
3. Instruct the copilot to create an `analysis.md` file in the [ACTIVE-PROMPT-FOLDER]
4. The analysis.md file should contain the following chapters:
   - **Copilot Review**: Honest opinion about the requested change
   - **Best Practices**: Internet research results with URLs and summaries
   - **Samples from GitHub**: How similar problems are solved in other repositories
   - **Proposals**: Proposed changes and alternative options
   - **Prompt Modification**: How the prompt could be better written

**Rationale**: This creates the execution step file for the new analyze mode that generates analysis documentation.

---

### Step 3: Update execution.md to reference clarify mode

Update `.rdd/prompt-snippets/execution.md` to:

1. Change the execution-mode name from `"analyze"` to `"clarify"`
2. Update the reference to the snippet file from `execution-step.analyze.md` to `execution-step.clarify.md`
3. Keep all other behavior identical (reset to no-action after completion, generate questionnaire-generated-on timestamp)

**Specific changes**:
- Line with `If \`execution-mode\` is \`"analyze"\`:` should become `If \`execution-mode\` is \`"clarify"\`:`
- Line with `**FIRST ACTION**: Write in the chat "Analyze mode"` should become `**FIRST ACTION**: Write in the chat "Clarify mode"`
- Line with `Follow the instructions in \`.rdd/prompt-snippets/execution-step.analyze.md\`` should become `Follow the instructions in \`.rdd/prompt-snippets/execution-step.clarify.md\``

**Rationale**: Update the main execution orchestration file to recognize and handle the renamed clarify mode.

---

### Step 4: Add analyze mode to execution.md

Add a new execution mode section in `.rdd/prompt-snippets/execution.md` for the "analyze" mode. This should be inserted after the "clarify" mode section and before the "plan" mode section. The new section should:

1. Check if execution-mode is "analyze"
2. Write "Analyze mode" to chat as the first action
3. Follow instructions in `.rdd/prompt-snippets/execution-step.analyze.md`
4. After completion, execute `.rdd/src/actions/prompt_analysis_generated_on.py` (to be created in Step 6)
5. Reset execution-mode to "no-action"
6. Stop execution

**Rationale**: As per questionnaire Q2-opt1, the analyze mode should reset to no-action after completion like other modes. As per Q3-opt2, it should NOT execute prompt_set_executed_on.py since analysis is not implementation execution.

---

### Step 5: Update work-iteration-registry.json schema

Add a new boolean field `analysis-generated` to the prompt objects in `.rdd-instance/workdir/work-iteration-registry.json`. This field should:

1. Be added to all existing prompts with default value `false`
2. Be positioned after `plan-generated` and before `implementation-completed` for consistency
3. Track whether analysis has been generated for a prompt

**Rationale**: As per questionnaire Q4-opt1, adding this flag provides consistency with questionnaire-generated and plan-generated tracking, and enables the UI to display analysis status.

---

### Step 6: Create prompt_analysis_generated_on.py script

Create a new Python script `.rdd/src/actions/prompt_analysis_generated_on.py` that:

1. Updates the `analysis-generated` field to `true` in the work-iteration-registry.json for the active prompt
2. Follows the same pattern as existing scripts like `prompt_questionnaire_generated_on.py` and `prompt_plan_generated_on.py`

**Rationale**: This script is needed to track when analysis has been generated, supporting the new analysis-generated flag.

---

### Step 7: Remove analyze.md file

Delete the file `.rdd/prompt-snippets/analyze.md` since its content has been migrated to the new `execution-step.analyze.md` file.

**Rationale**: This file is no longer needed after its content is incorporated into the execution-step structure.

---

### Step 8: Update manifest.json to remove ANALYZE snippet

Remove the `[[[ANALYZE]]]` entry from the `promptSnippets` array in `.rdd/config/manifest.json`.

**Rationale**: As per questionnaire Q5-opt2, analyze is now an execution mode (like clarify, plan, implement), not a user-insertable prompt snippet. It should be invoked via execution-mode setting, not via snippet insertion.

---

### Step 9: Update Web UI to support clarify and analyze modes

Update the Web UI components to:

1. Replace all references to "analyze" mode with "clarify" mode in the execution mode selection interface
2. Add "analyze" as a new execution mode option
3. Display the `analysis-generated` flag in the prompt status indicators
4. Ensure the execution mode selector includes both "clarify" and "analyze" options
5. Create new tab for analysis.md file and show it when `analysis-generated` is true

**Files to update**:
- `.rdd/src/web/templates/active_prompt.html` (if it has execution mode controls)
- `.rdd/src/web/static/js/active-prompt.js` (if it handles mode selection)
- Any other UI files that reference execution modes

**Rationale**: The Web UI needs to reflect the new execution mode structure and provide access to both clarify and analyze modes.

---

### Step 10: Update requirements.md

Add new technical requirements to `.rdd-instance/specifications/requirements.md` to document:

1. The clarify execution mode for questionnaire generation
2. The analyze execution mode for analysis document generation
3. The analysis-generated tracking flag
4. The separation of clarification from analysis functionality

**New requirements to add**:

- [TR-YYYYMMDD-NNNN] The framework shall provide a "clarify" execution mode that generates a questionnaire to clarify ambiguous or missing information in the active prompt.

- [TR-YYYYMMDD-NNNN] The framework shall provide an "analyze" execution mode that generates an analysis.md file containing copilot review, best practices research, GitHub samples, proposals, and prompt modifications.

- [TR-YYYYMMDD-NNNN] The framework shall track whether analysis has been generated for each prompt using an "analysis-generated" boolean flag in the work iteration registry.

- [TR-YYYYMMDD-NNNN] The clarify and analyze modes shall automatically reset execution-mode to "no-action" after completion.

**Rationale**: Requirements must be updated to reflect the new execution modes and their behavior.

---

### Step 11: Update files-and-folders.md

Update `.rdd-instance/specifications/files-and-folders.md` to document:

1. The renamed `execution-step.clarify.md` file
2. The new `execution-step.analyze.md` file
3. The removal of `analyze.md` file
4. The new `prompt_analysis_generated_on.py` script
5. The `analysis.md` file that gets generated in prompt workdir folders

**Rationale**: The files and folders specification must accurately reflect the new file structure.

---

## Summary

This plan implements the separation of clarification (questionnaire generation) from analysis (creating analysis.md) by:

1. Renaming the current analyze mode to clarify mode
2. Creating a new analyze mode for generating analysis documents
3. Updating all references and configurations
4. Adding tracking for analysis generation
5. Removing the standalone analyze.md snippet since analyze is now a mode
6. Updating specifications to document the changes

All changes maintain backward compatibility for existing prompts while enabling the new dual-mode structure for future prompts.