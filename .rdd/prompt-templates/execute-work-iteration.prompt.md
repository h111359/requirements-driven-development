# Execute Work Iteration Prompt 

## Role 

You are an experienced developer assistant who follows instructions precisely and executes accordingly a prompt in a file. 

## Definitions

- [WI-REGISTRY] is the file `.rdd-instance/workdir/rdd-prompt-setup.json`
- [WI-MODE] is the value of the attribute `mode` in [WI-REGISTRY]
- [ACTIVE-USER-STORY-ID] is `active.active-user-story-id` in [WI-REGISTRY]
- [ACTIVE-TASK-ID] is `active.active-task-id` in [WI-REGISTRY]
- [USER-STORY] is the object in `userStories[]` whose `user-story-id` equals [ACTIVE-USER-STORY-ID]
- [PROMPT-TEXT] is the full content of the file referenced by `[USER-STORY].prompt-file`
- [WI-REGISTRY] is the file `.rdd-instance/workdir/rdd-prompt-setup.json`

## Context 

- The work iteration can execute either:
	- a **User Story** (with its own prompt and its own stage tracking), or
	- an independent **Task** from the top-level `tasks` queue.

- When [WI-MODE] is `userStory`, the prompt to execute is [PROMPT-TEXT] from `[USER-STORY].prompt-file`.

- A User Story prompt SHOULD follow the structure in `.rdd/templates/rdd-prompt.md`.

- Instead of [PROMPT-TEXT] shall be written the actual prompt text with all the instructions that should be executed - consider it as a value of the variable [PROMPT-TEXT] in the following instructions.  

- [WI-REGISTRY] contains the registry of the current work iteration execution - see `.rdd/conventions/work-iteration-registry.convention.md` for details about its format and attributes.

- If [WI-MODE] is `userStory`, use the stage attributes **inside** [USER-STORY] (e.g. `[USER-STORY].clarity.state`) to decide which steps should be executed or skipped.

- If [WI-MODE] is `task`, do NOT execute a User Story; instead follow the task execution workflow (see `.rdd/prompt-templates/execute-task.prompt.md`).


## Instructions - Follow these steps exactly:  

0. **Read [WI-REGISTRY] and determine mode**:

- If [WI-MODE] is `task`:
	- execute `.rdd/prompt-templates/execute-task.prompt.md` behavior for [ACTIVE-TASK-ID]
	- stop here.

- If [WI-MODE] is `userStory`:
	- continue with the steps below.

1. **Resolve the active user story**:

- Read [ACTIVE-USER-STORY-ID] and locate [USER-STORY] in `userStories[]`.
- If not found or if `[USER-STORY].prompt-file` is empty/missing - stop and inform the user.

2. **Read the user story prompt**: Open and read the [PROMPT-TEXT] from `[USER-STORY].prompt-file`.

3. **Gather the context**: 

- Follow the instructions in `.rdd/prompt-snippets/execution-step.context.md`

4. **Ensure clarity**: 

- If `[USER-STORY].clarity.state` attribute is "ready-to-start" - follow the instructions in `.rdd/prompt-snippets/execution-step.clarity.md`, otherwise skip this step.
 
5. **Ensure questionnaire is answered**: 

- If `[USER-STORY].clarity.state` attribute is "generated" - follow the instructions in `.rdd/prompt-snippets/execution-step.questionnaire.md`, otherwise skip this step. 

6. **Plan the prompt**: 

- If `[USER-STORY].plan.state` attribute is "ready-to-start" - follow the instructions in `.rdd/prompt-snippets/execution-step.plan.md`, otherwise skip this step.  

7. **Implement the prompt**: 

- If `[USER-STORY].implementation.state` is "ready-to-start" and `[USER-STORY].implementation.approved` is "true" - follow the instructions in `.rdd/prompt-snippets/execution-step.implementation.md` without asking for confirmation, otherwise skip this step.  


## Mandatory Rules:  

- Execute the instructions in the prompt exactly as if the user had entered them directly in the chat.     

- Follow all instructions in the prompt carefully. The instructions in the prompt take precedence over the context. 

- Never change the `.rdd-instance/workdir/rdd-prompt.md` file! If the file is missing or malformed - stop and inform the user.  

- If the repo still contains `.rdd-instance/workdir/rdd-prompt.md` from older schema, treat it as legacy and ignore it unless `[USER-STORY].prompt-file` points to it explicitly.

- **Be verbose in files**: When writing to files in `.rdd-instance/workdir/` folder, provide detailed explanations, reasoning, and context to ensure clarity for future reference. 

- **Keep short chat**: Do not make detailed summaries in the chat when finishing the task, unless for errors. Just write "I am done." 

- It is not supposed the steps to be executed in parallel - always follow the order of the steps as they are defined in the instructions above. Steps depend on the results of the previous steps! 

- Read again the content of [WI-REGISTRY] (as it could be manually changed by the user meanwhile) before each step to decide if the step should be executed or skipped.
- When [WI-MODE] is `userStory`, re-locate the active [USER-STORY] after each re-read and use that object’s stage states.
 
- At the end of the execution - verify you have followed all the steps in the implementation plan. 

- Never delete already added requirements rows in `.rdd-instance/requirements.md`. If the entire requirement is already obsolete and nothing shall be left from it - replace its text (after the ID) with "[DELETED]".  

- Preserve ID sequences in `.rdd-instance/requirements.md` (never renumber existing IDs).  

- When adding requirements in `.rdd-instance/requirements.md`, first read the convention in `.rdd/conventions/requirements-format.md` and then decide in which section to add them, then continue the sequence from highest existing ID in that section. Inform the user in case of deviations from the convention. 

- Maintain existing structure and formatting of `.rdd-instance/requirements.md` - it should be accordingly the convention in `.rdd/conventions/requirements-format.md` - always observe the rules in it. 

- **Error Handling**: At each step, if an error occurs, log error to implementation file, return error response to caller in the chat, preserve partial work (don't delete implementation file or undo changes), provide recovery guidance (re-run with fixes, manual intervention, rollback options) 

- Do not ask for permission (unless explicitly required) to continue if you have no blockers to proceed furhter. Do as much as you can without user input. 
