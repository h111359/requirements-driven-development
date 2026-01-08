## Definitions

- [WI-REGISTRY] is the file `.rdd-instance/workdir/work-iteration-registry.json`
  
- [PROMPT-REGISTRY] is the file `.rdd-instance/workdir/prompts-registry.md`

- [ACTIVE-PROMPT-ID] is the prompt-id of the prompt entry in [WI-REGISTRY] which is with state `active`. The framework allows only one prompt to be in this state.

- [ACTIVE-PROMPT-FOLDER] is a folder in `.rdd-instance/workdir` with format `<[ACTIVE-PROMPT-ID]>_<prompt-title>`

- [ACTIVE-PROMPT] is the file `prompt.md` in [ACTIVE-PROMPT-FOLDER]

- [PLAN] is the file `plan.md` in [ACTIVE-PROMPT-FOLDER]

- [ANALYSIS] is the file `analysis.md` in [ACTIVE-PROMPT-FOLDER]

- [IMPLEMENTATION] is the file `implementation.md` in [ACTIVE-PROMPT-FOLDER]

- [QUESTIONNAIRE-CONVENTION] is the file `.rdd/conventions/questions-formatting.md`
  
- [QUESTIONNAIRE] is the questionnaire artifact in [ACTIVE-PROMPT-FOLDER]. Primary format: `questionnaire.json` (per `.rdd/conventions/questionnaire-json-schema.md`)

- [CURRENT-MODIFICATION-ID] is the value of `current-modification-id` field in [WI-REGISTRY] for the active prompt

- [MODIFICATION-FILE] is the file `modification-<[CURRENT-MODIFICATION-ID]>.md` in [ACTIVE-PROMPT-FOLDER]

- [MODIFICATION-IMPLEMENTATION] is the file `modification-<[CURRENT-MODIFICATION-ID]>-implementation.md` in [ACTIVE-PROMPT-FOLDER]

- [MODIFICATIONS-LOG] is the file `modifications-log.json` in [ACTIVE-PROMPT-FOLDER]

- [REQUIREMENTS] is the file `.rdd-instance/specifications/requirements.md`

- [FILES-AND-FOLDERS] is the file `.rdd-instance/specifications/files-and-folders.md`

- [TECHNICAL-DESIGN] is the file `.rdd-instance/specifications/technical-design.json`


## Requirements Management Rules

**CRITICAL - Requirements File Safety:**

NEVER edit `.rdd-instance/specifications/requirements.md` directly. Always use the requirement management scripts to ensure format consistency and prevent data corruption.

**Available Scripts:**

Create new requirement:
```bash
python .rdd/src/actions/requirement_ur_create.py text="The system shall..."
python .rdd/src/actions/requirement_tr_create.py text="The framework shall..."
```

Modify existing requirement:
```bash
python .rdd/src/actions/requirement_ur_modify.py id="UR-XXXX" text="Updated text..."
python .rdd/src/actions/requirement_tr_modify.py id="TR-XXXX" text="Updated text..."
```

Delete requirement (marks as [DELETED]):
```bash
python .rdd/src/actions/requirement_ur_delete.py id="UR-XXXX"
python .rdd/src/actions/requirement_tr_delete.py id="TR-XXXX"
```

**Validation:**
- Default: Basic validation (10-2048 chars, contains "shall")
- Skip validation: Add `validation=none` parameter

**Examples:**
```bash
# Create with validation
python .rdd/src/actions/requirement_ur_create.py text="The system shall export data in CSV format"

# Create without validation (for special cases)
python .rdd/src/actions/requirement_tr_create.py text="See external document XYZ" validation=none
```


## Instructions - Follow these steps exactly:  

1. **Read the registry**: Open and read the [WI-REGISTRY].
      
2. Identify the [ACTIVE-PROMPT-ID], [ACTIVE-PROMPT-FOLDER], [ACTIVE-PROMPT].

3. **Check for prompt snippet keys in [ACTIVE-PROMPT]**:

   * A prompt-snippet-key is any string starting with `[[[` and ending with `]]]`.
   * For each found key:

     * Look up the corresponding file path in `.rdd/config/manifest.json` under `promptSnippets`
     * Read that snippet file immediately
     * Treat snippet file content as if it was copy-pasted into the prompt at that position.
   * If snippet content explicitly overrides normal execution flow, follow it.
   * IMPORTANT: Snippets may change WHAT work is done, but do not skip mode-specific completion steps unless the snippet explicitly says to skip them.  

4. Read [TECHNICAL-DESIGN] and log exactly one sentence in chat describing what is relevant to [ACTIVE-PROMPT].

5. Read [REQUIREMENTS] and log exactly one sentence in chat describing what is relevant to [ACTIVE-PROMPT].

6. Read [FILES-AND-FOLDERS] and log exactly one sentence in chat describing what is relevant to [ACTIVE-PROMPT].

7. Read [PROMPT-REGISTRY] and log exactly one sentence in chat describing what is relevant to [ACTIVE-PROMPT] (highest prompt-id wins on conflicts; [ACTIVE-PROMPT] always wins).

8. If [QUESTIONNAIRE] exists and has any answered question (any user-selection.type != null), comply with those answers in subsequent steps.

9. If [PLAN] exists, follow it strictly only in implement mode (and modification mode when it contains applicable steps). Do not apply [PLAN] in no-action/clarify/analyze/plan modes unless [ACTIVE-PROMPT] explicitly instructs otherwise.

10. Read execution-mode once at start from [WI-REGISTRY] and treat it as SELECTED-MODE for this run. Later scripts may update it but do not re-evaluate within this run. Based on SELECTED-MODE:
   
   * If `no-action`:
     * **FIRST ACTION**:  Write in the chat "No action mode selected"
     * **FINAL ACTION**: Stop execution and inform the user to set a different execution mode via the Web UI or CLI
   
   * If `clarify`:
     * **FIRST ACTION**: Write in the chat "Clarify mode"
     * **SECOND ACTION**: Follow the instructions in `.rdd/prompt-snippets/execution-step.clarify.md`
     * **AFTER**: After clarify execution is completed:
       - Execute `python .rdd/src/actions/prompt_questionnaire_generated_on.py`
       - Execute `python .rdd/src/actions/prompt_set_execution_mode.py mode=no-action` to reset mode
     * **FINAL ACTION**: Stop
   
   * If `analyze`:
     * **FIRST ACTION**: Write in the chat "Analyze mode"
     * **SECOND ACTION**: Follow the instructions in `.rdd/prompt-snippets/execution-step.analyze.md`
     * **AFTER**: After analyze execution is completed:
       - Execute `python .rdd/src/actions/prompt_analysis_generated_on.py`
       - Execute `python .rdd/src/actions/prompt_set_execution_mode.py mode=no-action` to reset mode
     * **FINAL ACTION**: Stop 
   
   * If `plan`:
     * **FIRST ACTION**: Write in the chat "Plan mode"
     * **SECOND ACTION**: Follow the instructions in `.rdd/prompt-snippets/execution-step.plan.md`
     * **AFTER**: After plan execution is completed:
       - Execute `python .rdd/src/actions/prompt_plan_generated_on.py`
       - Execute `python .rdd/src/actions/prompt_set_execution_mode.py mode=no-action` to reset mode
     * **FINAL ACTION**: Stop (do not execute implementation)
   
   * If `implement`:
     * **FIRST ACTION**:  Write in the chat "Implementation mode"
     * **SECOND ACTION**: Follow the instructions in `.rdd/prompt-snippets/execution-step.implementation.md`
     * **AFTER**: After implementation is completed:
       - Execute `python .rdd/src/actions/prompt_set_executed_on.py`
       - Execute `python .rdd/src/actions/prompt_implementation_completed_on.py`
       - Execute `python .rdd/src/actions/prompt_set_execution_mode.py mode=no-action` to reset mode
     * **FINAL ACTION**: Stop 
   
   * If `modification`:
     * **FIRST ACTION**:  Write in the chat "Modification mode"
     * **SECOND ACTION**: Follow the instructions in `.rdd/prompt-snippets/execution-step.modification.md`
     * **AFTER**: After modification execution is completed:
       - Execute `python .rdd/src/actions/modification_complete.py`
       - Execute `python .rdd/src/actions/prompt_set_execution_mode.py mode=no-action` to reset mode
     * **FINAL ACTION**: Stop (do not continue with the next instructions here)

11. Requirements updates guardrail:
* Only in `implement` and `modification` modes: update [REQUIREMENTS] using requirement scripts if needed.
* In `clarify`, `analyze`, `plan` modes: do NOT update [REQUIREMENTS].
* In all cases where requirements are changed: record rationale in [IMPLEMENTATION] (or [MODIFICATION-IMPLEMENTATION] for modification mode).

12. FINAL chat message:
* Write exactly: `I am done with <execution-mode>.`
* If execution-mode is modification, append the modification-id: `I am done with modification <ID>.`


## Mandatory Rules:  

* **Snippet keys**: If [ACTIVE-PROMPT] contains `[[[...]]]`, always resolve via `.rdd/config/manifest.json` and follow the snippet content as part of the prompt.

* **Be verbose in files**: When writing to files in `.rdd-instance/workdir/`, provide detailed reasoning and context for future reference.

* **Keep chat short**: Apart from the mandatory mode announcements and the final done message, do not provide long summaries unless there is an error.

* **Sequential execution**: Do not execute steps in parallel. Follow the steps in order. Each step depends on the previous results.

* **Precedence order (highest to lowest)**:

  1. [ACTIVE-PROMPT]
  2. Snippet files referenced by keys in [ACTIVE-PROMPT]
  3. [QUESTIONNAIRE] answers
  4. [PLAN] steps
  5. [REQUIREMENTS], [TECHNICAL-DESIGN], [FILES-AND-FOLDERS]
  6. [PROMPT-REGISTRY] (historical reference; higher prompt-id has precedence in conflicts)

* **Analysis**: The [ANALYSIS] is for human reading only. If needed, the user will modify the [ACTIVE-PROMPT]. Do not consider it during the implementation.

- At the end of the execution - verify you have followed all the steps. 

* **Follow Requirements**: [REQUIREMENTS] are binding unless [ACTIVE-PROMPT], [QUESTIONNAIRE] answers or [PLAN] explicitly overrides. 

* **Do not delete requirement entry**: Never delete requirement ID rows in [REQUIREMENTS]. If obsolete, replace only the text after the ID with `[DELETED]`.

* **Error handling**: If an error occurs:

  * Log the error in the appropriate implementation file
  * Return an error response in chat with recovery guidance
  * Preserve partial work (do not delete logs)

* **Do not pause**: Do not pause for confirmation; proceed unless user input is required.