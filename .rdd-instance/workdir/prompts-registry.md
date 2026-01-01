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
