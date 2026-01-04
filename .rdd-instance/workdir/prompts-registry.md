%%PROMPT P-001 "Baseline problem statement"
Make changes so `.rdd/src/actions/prompt_create.py` to add a folder in `.rdd-instance/workdir` named accordingly the new prompt as `<prompt-id>_<prompt-title>`. In it create an empty files `prompt.md`, `plan.md`, `implementation.md`. The idea is every prompt to have its own folder under `.rdd-instance/workdir` with some work files generated in the course of its execution stored in this folder.
%%ENDPROMPT

%%PROMPT P-002 "prompt-set-state"
- Add/adjust deterministic scripts needed by “execute command” so Copilot isn’t doing file logic:
  - `prompt_set_state.py` (change prompt state; enforce “single active prompt” invariant)
%%ENDPROMPT

%%PROMPT P-003 "CLI"
Implement the CLI backbone (TR-0901, UR-0914)
- Implement rdd.py as the main command router (domain-based):
  - Domains: `prompt`, `workdir`.
  - Interactive menus with curses + numeric fallback (UR-0932).
- Provide wrappers that always use `python` and remain cross-platform (TR-0902).

Acceptance: `python rdd.py --help` works; core actions callable via CLI; errors show cause + remediation (UR-0927).

Docstring should be added to every python function
%%ENDPROMPT

%%PROMPT P-004 "Add prompt completion with commit command"
A new user requirement: Need to be added action for making a git commit with the changes during the current prompt. The message of the git commit should be the iteration-id + underscore + prompt id + underscore + prompt title. The action will be executed by the user manually and independently from the other actions.


## Modification 01

Execution of `.rdd/src/rdd.py` without arguiments return error. Troubleshoot and fix it.

## Modification 02

When execute `.rdd/src/rdd.py` some of the commands in the menu expect parameters. But the menu tries to execute them without parameters and they fail. Add functionality the user to be asked for input of the parameters.
%%ENDPROMPT

%%PROMPT P-005 "Web Interface Draft"
Generate a web interface to cover the current actions in `.rdd/src/actions`
%%ENDPROMPT

%%PROMPT P-006 "Troubleshoot web interface"

%%ENDPROMPT

%%PROMPT P-007 "Edit prompt text in Web UI"
The web UI shall allow to be edited the text of the active prompt and all draft propmts, the plan and the questionnaire files. The implementation file of the active prompt and the draft prompts should be able to be viewed, but not edited. Also the respective files for the completed prompts should be able to be viewed, but not edited.
%%ENDPROMPT

%%PROMPT P-008 "Move analyze command in the Web UI"
The analyze modification of the execute command should depend on an attribute in `.rdd-instance/workdir/work-iteration-registry.json`, not to be expected to be written in the chat.
The convention `.rdd/conventions/work-iteration-registry.convention.md` should be changed so every prompt to have a boolean key if the analyze modification should be turned on.
The prompt snippet `.rdd/prompt-snippets/execution.md` should read the modifier from `.rdd-instance/workdir/work-iteration-registry.json`.
The requirements should be revised so to reflect this change.
There should be created a script - prompt_analyze_on.py which expects a prompt-id and turns on the option in `.rdd-instance/workdir/work-iteration-registry.json`
There should be created a script - prompt_analyze_off.py which expects a prompt-id and turns off the option in `.rdd-instance/workdir/work-iteration-registry.json`
The Web UI should provide a switcher to turn on and off analyze for the active prompt (should not be provided for completed promtpst)
When the analyze execution is completed, the copilot should turn off the analyze option via the prompt_analyze_off.py script.
%%ENDPROMPT

%%PROMPT P-009 "Completion operation"
Create a new action python script in `.rdd/src/actions` named `prompt_complete.py` which sets the prompt provided as parameter to "completed" state.
In `.rdd-instance/workdir/work-iteration-registry.json` shall be added a key if git operations are enabled.
Based on this git key if it is enabled, the `prompt_complete.py` also should execute `.rdd/src/actions/git_commit.py` action.
In `.rdd-instance/workdir/work-iteration-registry.json` should be added a flag in each prompt if it is executed. Create a new action python script in `.rdd/src/actions` named `prompt_set_executed_on.py` which sets the  executed flag of the prompt provided as parameter to true.
In the Web UI in the prompt row should be added a button which executes the `prompt_complete.py`. Button should be enabled only if the executed flag is true for the prompt.
%%ENDPROMPT

%%PROMPT P-010 "Set complete status before git commit command"
Currently during the completion action the git commit is executed before setting the status of the prompt to completed, which leads to a new uncommitted changes. The order should be opposite - first set the status to completed and then commit, so after the commit no uncommitted changes exist.
%%ENDPROMPT

%%PROMPT P-011 "Remove git_commit.py"
As the functionality for committing the changes of a prompt now are implemented directly in `.rdd/src/actions/prompt_complete.py`, the script `.rdd/src/actions/git_commit.py` probably is obsolete. Check if this is the case and if not needed anymore - remove it and reflect in the requirements the change.
%%ENDPROMPT

%%PROMPT P-012 "Plan mode"
In a similar way as analyze mode I want to be created "Plan mode". There should be a switcher in the Web UI, and `.rdd/prompt-snippets/execution-step.plan.md` is the prompt snippet which should be executed if the respective flag in `.rdd-instance/workdir/work-iteration-registry.json` is set to true. 
The plan mode should not be able to be activated if analyze mode is on and vice versa. By default both are off and when the user in the Web UI turn some of them on - then it should be executed. After execution of the plan instruction as per `.rdd/prompt-snippets/execution-step.plan.md` , the execution should be stopped - no implementation if this mode is on. The idea is that the user could need to verify the plan themselves before the execution.
%%ENDPROMPT

%%PROMPT P-013 "Requirements add script"
I need a quick way to start the web ui both on Windows and Linux. I prefer to doublecklick on a file and to start the Web UI or some alternative but very easy way. If possible - avoid writing commands in the terminal. You should provide me with an analysis of the options I to choose from as a file in the active prompt folder. 

Do not create other files than run.bat and run.sh as launchers placed in .rdd/ folder. These launchers should execute the respective scripts for launching the web interface.
%%ENDPROMPT

%%PROMPT P-014 "States simplification"
Remove Draft, Plan and In-Progress states of prompts and instead introduce a new state - "Active". In that way there shall remain only two states - "Active" and "Completed". When a new prompt is created - it should be created in "Active" state. New prompt shall be allowed to be created if all other prompts are in "Completed" state. The change should be reflected in all requirements and specification files and all conventions, as well all scripts should be checked and changed if affected. Everywhere where planned or in-progress states are referred in the scripts now should be changed to "active" state instead.
%%ENDPROMPT

%%PROMPT P-015 "Remove prompt type"
There should not be distinction between main and modification types of prompts. The type parameter of the prompt should be removed.
%%ENDPROMPT

%%PROMPT P-016 "Active prompt in a separate page"
The active prompt should have a separate tab in the Web UI. The current Prompts tab should be renamed to "Prompts History" and should have the list of the completed prompts, the view button next to each prompt with the existing modal for showing the questionnaire, plan and implementation files (as it is now) the create new button and the row for the active prompt. The state, analyze mode and plan mode switchers and state change buttons should be removed from the Prompt History page. The Prompt History page should contain only completed prompts, so no need of the state. The completed prompts could not have analyze and plan modes activated, also they shall not be changed to active state.

The active prompt should be in a separate page "Active Prompt". In the Active Prompt page should keep the existing analyze or plan modes. There should be introduced a third mode - implementation mode. Currently the implementation is started when the no analyze and plan modifications are enabled but this needs to be changed so the mode to reflect what should be done with the active prompt by the execute command. The modes shall be: no-action|analyze|plan|implement. In the web interface should be introduced a radio button group (or similar mutually exclusive options input) which to define what should execute command do with the active prompt. There is no strict dependency between modes - each should be able to be executed despite others are or are not executed. Still there should be introduced new attributes in `.rdd-instance/workdir/work-iteration-registry.json` for each prompt showing if the questionnaire is generated, if the questionnaire is fully fulfilled and if the plan is generated. On the Active Prompt page should be indicators for the state of each mode. If the questionnaire is generated but not answered - use yellow color, if generated and answered - green. For generated plan and for executed implementation - use greed color. For not generated mode - use grey (or other appropriate color - you propose one). In a similar way to the generated questionnaire, there should be created additional attributes of the prompts in `.rdd-instance/workdir/work-iteration-registry.json` which to show if the questionnaire is answered completely, if the plan is generated and if the implementation is completed. For each of these additional attributes create a python script in `.rdd/src/actions` to set it to true and another - to set it to false. The python scripts names should start with "prompt*" and should follow the logic of the other prompts naming. 

Revise also `.rdd-instance/workdir/work-iteration-registry.json` for not used attributes (check for example "analysis", "questionnaire", "plan") and for all not used - remove them from the file, from convention and from the scripts generating the entries.

Modification 01:

See the plan .rdd-instance/workdir/P-016_Active prompt in a separate page/plan.md and verify what from it is executed and what not. After that fix whatever is not executed. Read the whole .rdd-instance/workdir/P-016_Active prompt in a separate page folder for context

Modification 02:
Check why when press "Create New Prompt" it adds "title" in .rdd-instance/workdir/work-iteration-registry.json instead of prompt-title as an attribute. Fix the issue
%%ENDPROMPT

%%PROMPT P-017 "Modifications"
Need to be added one more mode - "Correction". It should become available only if "implementation-completed" is true. Its meaning is to address the cases when sometimes after the implementation is completed, the user can spot needs for small corrections, for which will be inconvenient to be created a new prompt. New attributes to the prompt entry in `.rdd-instance/workdir/work-iteration-registry.json` should be added.

Do not implement nothing with this prompt. I need to be created in the active prompt folder a file named "analysis.md" where you to propose me a design how to address the need of post-implementation small modifications before completion of the prompt. Propose what should be changed in prompt-snippets, the scripts, the requirements, what should be the naming of the new files and attributes. Provide with 5 different options to choose from.
%%ENDPROMPT

%%PROMPT P-018 "Implement Modifications accordingly P-017"
Implement the proposal in `.rdd-instance/workdir/P-017_Modifications/analysis.md`


### Modification 001

Move the "Add Modification" button in the upper part of the page


### Modification 002

The user should be able to edit the modification, which is In Progress


### Modification 003

Make sure the modifications are reflected in requirements.md if necessary
%%ENDPROMPT

%%PROMPT P-019 "Move create new prompt button and make Active Prompt page the landing page"
Currently the Create New Prompt button is in Prompt History page. Move it in Active Prompt page. Swap the menu entries "Prompt History" and "Active Prompt" so "Active Prompt" to be most left one. Make "Active Prompt" page to be the landing page of the web portal.
%%ENDPROMPT

%%PROMPT P-020 "View button in Prompt History page is not working"
Fix the view button in Prompts History page - it is not doing anything
%%ENDPROMPT

%%PROMPT P-021 "Add prompt texts in prompts-registry"
When Complete prompt is pressed, the prompt.md and all modifications texts should be copied in `.rdd-instance/workdir/prompts-registry.md` following the `.rdd/conventions/prompts-registry.convention.md`.
%%ENDPROMPT

%%PROMPT P-022 "Questionnaire to JSON"
Currently the questionnaire is created as markdown file. Change to be created as JSON file. All attributes of the questions (see the questions generated in prompts workdir subfoldersin `.rdd-instance/workdir` to see examples) should be reflected in the JSON. There should be entry for each question, the pros and cons for each answer from the proposed optione. Also there should be a recommended answer with rationale. There should be also option for user free text answer, if none of the options are OK. 

In Active Prompt page the Questionnaire should not be displayed as a text file anymore, but to be introduced a way (form fulfillment) where the user to fulfill the questionnaire. Every answer from the user should be immediately reflected in the JSON file.

Do not change the questionnaires back in time - no need of back compatibility.
%%ENDPROMPT

%%PROMPT P-023 "Test Questionnaire JSON"
TBD
%%ENDPROMPT

%%PROMPT P-024 "Compact Active Prompt page"
Make the page Active Prompt in the web UI more compact and all elements visible in 14 inch screen. All the buttons should be together (Create New Prompt, Add Modification, Complete Prompt). Find a way the Execution Mode and Progress Status to keep the same functionality and information but to be take less space. Also make the name of the prompt to take less space. Make also the buttons and the main information to remain visible while scrolling (if scrolling is needed at all).


### Modification 001

In Q2 in the questionnaire I have chosen "C. Keep current button group but reduce padding, margins, and font size " but you have created a dropdown. Why? I want the button group back in the place of the current dropdown


### Modification 002

Remove the title "Prompt files" - no need of it, it is clear what is below


### Modification 003

Make questionnaire form more compact. It takes too much space now. Keep all texts and visuals


### Modification 004

In Questionnaire - make the context and the navigation of the questions on left and the current question and its answers on the right (changing the displayed question in the same placeholder). Keep all the current functionality. Reflect in requirements.md


### Modification 005

On the right side of the Questionnaire make the text of the question to be always visible during scrolling of the answer options - only in the questions placeholder


### Modification 006

The questionnaire is generated and even answered, but the state in Active Prompt is not reflecting that - stays in the same way as it is not generated at all. Fix that
%%ENDPROMPT

%%PROMPT P-025 "Modification Implementation files - visible"
Add a way the modification implementation files to be viewed - somewhere in the page when Modifications tab is selected
%%ENDPROMPT

%%PROMPT P-026 "Files and Folders"
Create a python script `.rdd/src/actions/files_list_csv_refresh.py` which lists all the file, folders and recursively their subfolders and stores the result in `.rdd-instance/specifications/files-list.csv` excluding folders and subfolders which start with "." or folders like "venv" in a terminal. The file should present the data in a tabular way, should be a tab separated and should have the following fields:
- File Name
- Relative Path
- Modification Time
- Description

On every execution of the script:
- Add new files found in the repository, which are not present in `.rdd-instance/specifications/files-list.csv` and fulfill for them the fields "File Name", "Relative Path" and "Last Modification Time"
- For the files with newer modification time - remove the current text in "Description" field (leave it empty) and update the field "Modification Time"
- Delete files from `.rdd-instance/specifications/files-list.csv` which are not present in the repository any more.

Create a python script `.rdd/src/actions/files_list_csv_set_description.py` which receives parameters file-name and relative-path and for the entry with those values in `.rdd-instance/specifications/files-list.csv` applies the content of third parameter description. This script will be called from copilot.
%%ENDPROMPT

%%PROMPT P-027 "Remove analyze-enabled"
[[[Analyse]]]

Check if the following files are still in use or they are obsolete:

.rdd/src/actions/prompt_analyze_off.py
.rdd/src/actions/prompt_analyze_on.py
.rdd/src/actions/prompt_plan_off.py
.rdd/src/actions/prompt_plan_on.py

Also check if these requirements should stay or are obsolete:

- [TR-20251230-2004] Each prompt in work-iteration-registry.json shall have an `analyze-enabled` boolean field with default value `false`.
- [TR-20251230-2006] The execution prompt logic shall read analyze mode from the `analyze-enabled` field in work-iteration-registry.json rather than from chat modifiers.

Check all the prompts executed up to now. In case of conflict, prompts with bigger number are with precedence.
%%ENDPROMPT

%%PROMPT P-028 "Clean up obsolete analyze plan mode artifacts"
**Context:**
P-016 introduced `execution-mode` attribute to replace the boolean `analyze-enabled` and `plan-enabled` flags. This was a successful refactoring that simplified the execution flow. However, the old infrastructure was not fully removed.

**Objective:**
Complete the cleanup initiated by P-016 by removing all obsolete artifacts related to the old boolean flag approach.

**Tasks:**

1. **Remove obsolete Python scripts:**
   - Delete `.rdd/src/actions/prompt_analyze_on.py`
   - Delete `.rdd/src/actions/prompt_analyze_off.py`
   - Delete `.rdd/src/actions/prompt_plan_on.py`
   - Delete `.rdd/src/actions/prompt_plan_off.py`

2. **Remove obsolete CLI commands from `.rdd/src/rdd.py`:**
   - Remove `prompt.analyze-on` action
   - Remove `prompt.analyze-off` action
   - Remove `prompt.plan-on` action
   - Remove `prompt.plan-off` action

3. **Clean work-iteration-registry.json:**
   - Remove `analyze-enabled` field from all prompts (currently exists in P-021, P-022, P-024, P-025, P-026)

4. **Update requirements.md:**
   - Mark the following as [DELETED - 20260103] with note "Superseded by execution-mode in P-016":
     - [TR-20251230-2004]
     - [TR-20251230-2005]
     - [TR-20251230-2006]
     - [TR-20251230-2009]
     - [TR-20251230-2010]
     - [TR-20251231-0205]

5. **Update convention documents:**
   - Check `.rdd/conventions/work-iteration-registry.convention.md` for references to `analyze-enabled` or `plan-enabled`
   - Remove any such references if found

**Expected Outcome:**
Clean codebase with no references to the deprecated boolean flag approach, fully aligned with the execution-mode design introduced in P-016.


### Modification 001

The requirements are not modified accordingly the convention. Only [DELETED] should remain in the requirement entry
%%ENDPROMPT

%%PROMPT P-029 "Prompt snippets adding in prompt"
[[[ROLE_SOLUTION_ARCHITECT]]]

[[[ANALYZE]]]

I want to be able easily to add in the prompt text prompt snippet keys while choosing from the predefined in `.rdd/config/manifest.json` list of keys. I have to be able to see the list, to see a view only text of the prompt and to be able to place the key on a chosen from me spot in the prompt. What are the possible approaches for that?
%%ENDPROMPT

%%PROMPT P-030 "Add Prompt Snippet Insertion UI to Web Interface"
*Role Context:** [[[ROLE_SOFTWARE_DEVELOPER]]]

**Background:**
The RDD framework uses prompt snippet keys (e.g., `[[[ROLE_SOLUTION_ARCHITECT]]]`, `[[[ANALYZE]]]`) to include reusable prompt instructions. These keys are defined in `.rdd/config/manifest.json` under the `promptSnippets` array. Currently, users must manually type these keys, which is error-prone and requires memorizing the exact syntax.

**Requirements:**

1. **Snippet Quick Picker** (Priority: HIGH)
   - Add a quick picker/dropdown UI component to the prompt editor in the Web UI
   - Display all available prompt snippet keys from manifest.json
   - Show snippet descriptions/paths alongside keys
   - Support search/filter within the snippet list
   - Insert selected snippet key at current cursor position
   - Accessible via keyboard shortcut (e.g., Ctrl+K, S) and toolbar button

2. **Snippet Preview** (Priority: MEDIUM)
   - Show preview of snippet file content when hovering over a snippet in the picker
   - Display file path and snippet description
   - Highlight syntax in preview (if applicable)

3. **Snippet Validation** (Priority: MEDIUM)
   - Validate snippet keys in prompt text against manifest.json
   - Show warning indicators for invalid/outdated snippet keys
   - Provide quick fix to update or remove invalid keys

4. **Future Considerations** (Priority: LOW)
   - Design with autocomplete integration in mind
   - Consider sidebar panel for snippet browsing
   - Plan for custom user snippets (not in this iteration)

**Technical Constraints:**
- Must read snippet definitions from `.rdd/config/manifest.json`
- Should update dynamically if manifest changes
- Web UI is built with [specify framework: React/Vue/etc.] - ensure compatibility
- Backend API may need new endpoint to serve snippet data

**Acceptance Criteria:**
- User can open snippet picker from prompt editor
- Picker shows all snippet keys with descriptions
- Selecting a snippet inserts the key (e.g., `[[[ROLE_SOLUTION_ARCHITECT]]]`) at cursor
- Picker supports keyboard navigation and search
- No performance impact on prompt editor load time
- Unit tests for snippet service and picker component

**Out of Scope:**
- Editing snippet definitions (read-only for now)
- Custom user snippets
- Snippet parameterization
- CLI integration (future iteration)

**Reference Implementation:**
Review VS Code's snippet picker implementation for UX patterns: [microsoft/vscode/src/vs/workbench/contrib/snippets/browser/snippetPicker.ts](https://github.com/microsoft/vscode/tree/main/src/vs/workbench/contrib/snippets/browser/snippetPicker.ts)


### Modification 001

When the button Insert Snippet is pressed, the list with snippets do not appear. Just after start typing something after [[[. This is confusing. Make the list of snippets to appear along adding [[[


### Modification 002

Instead of showing list of the available snippets below the prompt, make the list to appear in modal and when selected a snippet - its key to be added in the prompt text


### Modification 003

Move the modal action buttons to the top to avoid forcing users to scroll to the bottom when inserting snippets.


### Modification 004

When Insert Snippet is pressed, in the prompt is entered [[[ and when later in the modal is pressed Cancel - the [[[ stays. No [[[ should be added when Insert Snippet is pressed.
%%ENDPROMPT

%%PROMPT P-031 "Help Tab"
[[[ROLE_SOFTWARE_DEVELOPER]]]

In the tab section in UI should be created new section - Help
In Help should be displayed for now a User Guide, which you should refer to `.rdd/docs/user-guide.md`. It is a markdown file, so it should be transferred to HTML/CSS/JS look and feel dynamically.
The file `.rdd/docs/user-guide.md` should be totally recreated - read all the content of .rdd/ folder as well as .rdd-iteration/ folder to understand the current state, principles, etc.
Do not explain the technical details - just how the user should work with the UI and VSC so to develop.
Make the description simple to follow, logical and as short as possible (still the user should be able to understand clearly)


### Modification 001

Bug: I see the following in the User Guide text: "trong>" where in markdown is used "**". Fix it


### Modification 002

Bug: There still appears not properly rendered. For example:
strong>


### Modification 003

The bug reported in modifications 001 and 002 is not eliminated. Now appears:
*Step 1: Create a New Prompt**
But this text should be without asterisks and bold. The enclosed in ** text should be bold. Troubleshoot, find the root cause and fix the bug. Make sure the bug is eliminated


### Modification 004

Bug: In the user guide are seen special symbols:
For example in
"Web interface won&#x27;t start" the '&#x27;' is wrong. Find the issue and fix it. Work until the issue is fixed completely.


### Modification 005

The bug in Modification 004 is not fixed. I still can see same issue. For example:
"Troubleshooting

Web interface won&#x27;t start

    Ensure Python 3.7+ is installed and accessible via python command"
%%ENDPROMPT

%%PROMPT P-032 "Upper menu to stay while scrolling"
The menu in the Web UI with tabs (like Active Prompt, Prompts History, Workdir etc. should stay always visible while scrolling.
%%ENDPROMPT

%%PROMPT P-033 "More visible checkboxes for questionnaires"
[[[ROLE_SOFTWARE_DEVELOPER]]]

The options radio buttons in the Questionnaire are too light and barely visible. Fix that
%%ENDPROMPT

%%PROMPT P-034 "Instead of tabs - the statuses to be clickable"
[[[ROLE_SOLUTION_ARCHITECT]]]

Instead of statuses for Questionnaire, Plan and Implementation - hide or show the tabs for Plan, Questionnaire or Implementation. If the tab is present, this will mean the respective attribute is on and the files are present. 
Modifications tab should appear only when executed is set to true.
%%ENDPROMPT

%%PROMPT P-035 "Remove File Path"
Remove the section "File Path (relative to .rdd-instance):" together with the file selector.
%%ENDPROMPT

%%PROMPT P-036 "Remove Files Tab"
Move the buttons Registry, Requirements and Technical Design in Workdir tab and remove Files tab.
Verify so the buttons to work properly.
%%ENDPROMPT

%%PROMPT P-037 "Workdir tab restructuring"
Make the Workdir page compact
It should start with a header where all statuses should be positioned in concise way
After that should be all the buttons and actions
The content of the files should be at the bottom


### Modification 001

Remove label  Quick Access:  and the whole line in Workdir page


### Modification 002

Remove " Archive Current: " label. Make the button for archiving smaller
%%ENDPROMPT

%%PROMPT P-038 "New Workdir modal"
In Workdir page - remove the label "New Work Iteration: " and rename the "Create" button to "Create Work Iteration".
Instead of form in the page - leave the button only and creation should be made as a modal (like the way a new prompt is created)
%%ENDPROMPT

%%PROMPT P-039 "Requirements tab"
Instead of invoked with a button in Workdir page, move requirements to a new menu tab page named "Requirements"
%%ENDPROMPT

%%PROMPT P-040 "Active Prompt Flags"
In Active Prompt page in the buttons row add an icon for indication of each of the boolean flags:
      "questionnaire-generated",
      "questionnaire-answered",
      "plan-generated",
      "implementation-completed",
      "executed"
As well add there also the values (with short label) for:
      "modifications-count",
      "current-modification-id"


### Modification 001

The icons of the flags should be different and to resemble the meaning of the flag
%%ENDPROMPT

%%PROMPT P-041 "Clarity and Analyze modes"
The current execution-mode analyze should be renamed to clarify and analyze to be used as a new execution mode.
Clarify should continue to generate a questionnaire. The snippet `.rdd/prompt-snippets/execution-step.analyze.md` should be renamed to `.rdd/prompt-snippets/execution-step.clarify.md` and the references to it should be changed respectively (for example in `.rdd/prompt-snippets/execution.md`)
The role of analyze mode is to generate in the prompt workdir a file named "analysis.md" using as initial instructions the prompt `.rdd/prompt-snippets/analyze.md` renamed to `.rdd/prompt-snippets/execution-step.analyze.md` and modified to be in line with the structure of the rest `execution-step*` prompts.


### Modification 001

Make the icons of statuses to be right above the buttons for the execution modes and to reflect the respective mode. Clarify will have two icons - for generated and answered


### Modification 002

Change the Plan icon as the current one is with too tiny lines and it is not visible is it ON or OFF. Increase with 10% the size of all the icons


### Modification 003

Change the colors of the modes buttons. It should be one and the same color for non-active and another color for the active option


### Modification 004

Reorder the files tabs in Active Prompt page to follow the order of the execution modes:
1. Prompt
2. Questionnaire
3. Analysis
4. Plan
5. Implementation
6. Modifications


### Modification 005

Reflect the changes in the modifications in requirements.md file
%%ENDPROMPT

%%PROMPT P-042 "Active Prompt page design chage"
On Active Prompt page:
- move Complete button to most right on the banner
- move Mod button after the execution mode statuses group
- Change the color of all buttons to blue, including the execution modes buttons. 
- Stop showing message when I change the execution mode
- When a new modification is created - set the execution mode to Modification automatically


### Modification 001

Only the active Execution mode button should have solid backgroud. The rest should negate the colors so to be very clear which mode is the active one
%%ENDPROMPT

%%PROMPT P-043 "Remove new button when there is active prompt already"
Create New Prompt button should remain only when there is no active prompt (all are completed or there are no prompts yet)
When there is Active Prompt, the New button should not appear. On its place move the Mod button. Mod button should be renamed to Create Modification.
%%ENDPROMPT

%%PROMPT P-044 "Execute command clipboard"
Create a button in in Active Prompt which copies in the clipboard the text, which can be pasted directly in copilot chat for execution: "Follow the instructions in file `.rdd/prompt-snippets/execution.md`". The aim is this prompt to be used to trigger the execution command.
%%ENDPROMPT

%%PROMPT P-045 "Bug: questionnaire-generated and questionnaire-answered flags are set to true immediately after creation of new prompt"
Change `.rdd/src/actions/prompt_create.py` not to create empty plan.md, prompt.md and questionnaire.json files when creating a new prompt

Create scripts in `.rdd/src/actions/` trough which are created the questionnaire.json file and in it are added the needed questions and all other elements + chosen answers are set. The prompts should not directly change the questionnaire.json file but only via these scripts.

questionnaire-generated flag should be set to true only after creation of the questionnaire (currently it is set immediately after prompt creation). Fix so these flags to be set only after clarify is executed.

questionnaire-answered flag should be set to true only after all questions are answered

Implementation tab in Active Prompt is visible immediately after creation of the prompt. It shall remain hidden until "implementation-completed" attribute of the Active Prompt in `.rdd-instance/workdir/work-iteration-registry.json` is changed to truth.


### Modification 001

Change the icon for Implementation completed = true with negated colors as it is not well visible now that it is active. Should be with filled green background as the other icons depicting true value of flags


### Modification 002

When there are modifications already executed but not in modification mode, over the status mode stand only a single digit, which is not clear what it is. Make it more clear that this are the number of modifications executed so far
%%ENDPROMPT

%%PROMPT P-046 "Requirements IDs"
Find the best way to generate the requirements id in the file `.rdd-instance/specifications/requirements.md`

The convention file `.rdd/conventions/requirements.convention.md` should be modified as well.

After that the existing requirements file should be updated with the new format.
%%ENDPROMPT

%%PROMPT P-047 "Requirements scripts"
**Context**: Currently, the RDD framework allows AI agents and execution steps to directly edit `.rdd-instance/specifications/requirements.md`. This creates risks of format inconsistencies, ID conflicts, and accidental data corruption. The framework already uses deterministic Python scripts for other operations (prompts, modifications, questionnaires), but requirement management lacks this safety layer.

**Goal**: Enforce script-based requirement modifications by creating dedicated Python scripts and updating execution instructions to prohibit direct file editing.

**Requirements**:

1. **Create requirement management scripts** in `.rdd/src/actions/` following the existing framework patterns (see `prompt_create.py` as reference):

   - `requirement_ur_create.py` - Create new User Requirement
   - `requirement_ur_modify.py` - Modify existing User Requirement
   - `requirement_ur_delete.py` - Mark User Requirement as deleted (replace with [DELETED])
   - `requirement_tr_create.py` - Create new Technical Requirement
   - `requirement_tr_modify.py` - Modify existing Technical Requirement
   - `requirement_tr_delete.py` - Mark Technical Requirement as deleted (replace with [DELETED])

2. **Script behavior**:
   - **ID generation**: Automatically generate IDs  unless `id=` parameter is provided. 
   - **Validation**: Perform basic validation (non-empty, 10-2048 chars, contains "shall"). Use `validation=strict` for enhanced checks, `validation=none` to skip.
   - **Positioning**: Append new requirements to the end of the appropriate section (## User Requirements or ## Technical Requirements)
   - **Modification**: Replace entire requirement text when modifying
   - **Deletion**: Replace requirement text with [DELETED] marker, keeping the requirement ID line (following `.rdd/prompt-snippets/execution.md` rule and existing practice)
   - **Output**: Print "SUCCESS: <action> <requirement-id>" to stdout on success, error message to stderr on failure. Return exit code 0 for success, 1 for failure.
   - **File handling**: Use atomic writes (temp file + rename) to prevent corruption
   - **Format compliance**: Ensure all changes comply with `.rdd/conventions/requirements.convention.md`

3. **Update execution instructions**:
   - Modify `.rdd/prompt-snippets/execution.md` to add requirement script usage instructions and remove any references to direct requirements.md editing
   - Update `.rdd/prompt-snippets/execution-step.implementation.md` with examples of calling requirement scripts
   - Update any other execution snippets that mention requirements editing
   - Add prominent warning: **NEVER edit requirements.md directly - always use scripts**

4. **Parameters for each script**:
   - **Create**: `text="<requirement text>"` (required), `id="<override-id>"` (optional), `validation=strict|basic|none` (optional, default=basic)
   - **Modify**: `id="<requirement-id>"` (required), `text="<new complete text>"` (required), `validation=strict|basic|none` (optional, default=basic)
   - **Delete**: `id="<requirement-id>"` (required)

5. **Error handling**:
   - Validate ID format if user-provided
   - Check for ID conflicts/duplicates
   - Ensure target section exists in requirements.md
   - Provide clear error messages with suggested fixes
   - Fail fast before making any file modifications

**Success criteria**:
- All 6 scripts are functional and tested
- Execution snippets prohibit direct requirements.md editing
- Scripts successfully create, modify, and delete requirements while maintaining file format
- ID collision handling works correctly
- Validation catches common errors

**Related files**:
- Reference implementation: `.rdd/src/actions/prompt_create.py`
- Format convention: `.rdd/conventions/requirements.convention.md`
- Target file: `.rdd-instance/specifications/requirements.md`
- Execution orchestration: `.rdd/prompt-snippets/execution.md`
%%ENDPROMPT

%%PROMPT P-048 "Prompt text saved automatically"
Make the prompt text to be saved automatically without the need to press save button
%%ENDPROMPT

%%PROMPT P-049 "Technical Design"
Move technical design out of Workdir tab in a stand alone tab (similar to requirements).
%%ENDPROMPT

%%PROMPT P-050 "Registry edition"
Make the registry directly visible in Workdir - view only. Parse the JSON and render it in a human-readable nice looking format


### Modification 001

Merge Prompt History to Workdir registry - take the view buttons from Prompt History with their full functionality and add it to the table of prompts in Workdir
%%ENDPROMPT

%%PROMPT P-051 "Prompt History removing"
Now, when all the information is available in Workdir, Prompt History tab is not needed anymore.
Check what should be done the tab to be removed - will this affect something, and what from the code is related only to this page and could be safely removed.
Then remove the page Prompts History
%%ENDPROMPT

%%PROMPT P-052 "Workdir compact"
Make Workdir page more compact
Remove  "Work Iteration Registry" container and let the two areas (cards) in it to be directly in "Working Directory Management" container. Reduce the font of "Working Directory Management" title and make it same as the Active Prompt page title look and feel. Buttons "Create Work Iteration" and "Archive Iteration" can not coexist. When there is a created iteration, the button "Create Work Iteration" should not be visible. When the workdir is empty, "Create Work Iteration" should be the only element on the page.
%%ENDPROMPT

%%PROMPT P-053 "Workdir improvement"
Move "Archive Iteration" button on the right side of the heading "Working Directory Management". 
Remove "Registry View" heading (and the whole container - subcontainers to be positioned directly in "Working Directory Management" element.
Compact "Iteration Metadata" container - all indicators should fit on a single row.
%%ENDPROMPT

%%PROMPT P-054 "Remove view button in Workdir"
As both View button and clicking on the name of the prompt open the modal, one of these should be removed


### Modification 001

Remove the empty "File Viewer" element at the bottom of Workdir page
%%ENDPROMPT

%%PROMPT P-055 "Active Prompt Sticky Header Fix"
Scrolling Active Prompt and sticky header does not consider that the menu is also fixed and hides under it. Fix so not hiding to appear.
%%ENDPROMPT

%%PROMPT P-056 "Active Page refreshes"
In Active Prompt page - make the statuses and mode buttons to refresh (only them) on every 2 seconds automatically. No interruption of the user activities should be caused by this refreshes.
%%ENDPROMPT
