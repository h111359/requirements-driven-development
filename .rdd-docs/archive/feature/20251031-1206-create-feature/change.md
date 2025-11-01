## What

After creation of a subfolder in .rdd-docs, where the current work will be done, the work of clarification of requirements should start. For the purpose the prompt `.github/prompts/rdd.02-clarify-requirements.prompt.md` should be used. A proper file structure and process should be established and this prompt should be updated so to be generated clarified and complete requirements-changes.md file with all needed to be planned for technical execution and developed in the later stages.

Expected outcome:

- In the folder .rdd-docs should be created (even with the create-change.sh script) a folder `workspace` in which will be made the requirements clarification and technical execution planning and monitoring accordingly the current feature or fix
- to be invented a way from the files or from the folder structure in .rdd-docs/workspace to be  detectable which is the current feature or fix which the user works in (and this should be equal to the branch name). It could be in some configuration file or some other way.
- If you are in main branch - the workspace should be clean and with standard content, so it again makes it clear that this is main. For the purpose just before merging in main it will be allowed the feature/fix state to resembles the state as of main so after the commit the branch to be merged in appropriate way in main
- All merged in main previous features or fixes to be able to be fetched/pulled from main at any time by git command in the feature or fix branches
- In .rdd-docs to be maintained the latest commited in main files like requirements.md merged in main before the current feature of fix (or refreshed during its development
- The create-change.sh script should copy in the workspace folder the file clarify-taxonomy.md from .rdd-docs, so a specific taxonomy to be used for specific feature or fix
-  To be changed the prompt .github/prompts/rdd.02-clarify-requirements.prompt.md so to use the checklist in the file .rdd-docs/workspace/clarity-taxonomy.md and to verify if the requirements are clear. If not clear - to ask the user questions with predefined answers to be chosen from, allowing the user to provide own answer as well
-  After execution of this step should be creted a file requirements-changes.md with the collected information from the user what is the change towards the existing requirements file. Each statement in this file should be marked with [ADDED|MODIFIED|DELETED] preffix so to be clear later how to merge in the master requirements.md file
-  The prompt `.github/prompts/rdd.02-clarify-requirements.prompt.md` should be able to be executed multiple times. Each execution should be able to build on top of the previous, without loosing information from previous runs, unless this is required
-  Create a script `.rdd/scripts/clarify-changes.sh` which to be called by the prompt for different actions
-  Create a .vscode folder where add a settings file (or if exists - update it only) with allowance the scripts in `.rdd/scripts` to be executed by the agent without the need or approval 
-  For the purpose of more predictable execution of the prompt `.github/prompts/rdd.02-clarify-requirements.prompt.md`, when the actions can be executed by a script - add the functionality in `.rdd/scripts/clarify-changes.sh` with option it to be executed by providing parameters to the script
-  To be created in .rdd/templates/ a questions-formating.md file where is defined how to be generated in an user friendly way the questions and asks for user input in the chat sessions. All the prompts should use this format for questioning of the uers.
-  This initial change.md file should not be modified by the agent. A new files should be created in workspace folder for:
    - checklist with open questions which are inspred from (but not only from) the clarify taxonomy. It is OK to be added questions, which are critical for later execution phase, but are not in the taxonomy
    - recuirements-changes.md - for amendments in the requirement (as described above)
- In case the prompt `.github/prompts/rdd.02-clarify-requirements.prompt.md` is re-executed, the existing questions file and requirements-changes files should be taken in consideration and replaced with improved versions. The script can be used for the purpose (for example to create a temp copy and then replace or some more clever way - fill free to propose)

## Why

To achieve smooth experience of the developer to focus on clarification of the requirements without bothering with technical issues. Also to allow mutual work of many developers using the same rdd framework.

## Acceptance Criteria:

- [ ] All the points in the Expected outcome above to be covered
