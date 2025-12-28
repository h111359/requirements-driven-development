## Definitions

- [WI-REGISTRY] is the file `.rdd-instance/workdir/work-iteration-registry.json`
  
- [PROMPT-REGISTRY] is the file `.rdd-instance/workdir/prompts-registry.md`

* [active-prompt] - The prompt in `.rdd-instance/workdir/work-iteration-registry.json` which is with state `planned` or `in-progress`. The framework allows only one prompt to be in some of those states and this prompt is considered to be the `active prompt`



## Instructions - Follow these steps exactly:  

1. **Read the registry**: Open and read the [WI-REGISTRY] file.
   
2. Identify the ID of the [active-prompt].

3. Identify the [active-prompt] in [PROMPT-REGISTRY] and execute its instructions.



## Mandatory Rules:  

- Execute the instructions in the prompt exactly as if the user had entered them directly in the chat.     

- Follow all instructions in the prompt carefully. The instructions in the prompt take precedence over the context. 

- **Be verbose in files**: When writing to files in `.rdd-instance/workdir/` folder, provide detailed explanations, reasoning, and context to ensure clarity for future reference. 

- **Keep short chat**: Do not make detailed summaries in the chat when finishing the task, unless for errors. Just write "I am done." 

- It is not supposed the steps to be executed in parallel - always follow the order of the steps as they are defined in the instructions above. Steps depend on the results of the previous steps! 

- At the end of the execution - verify you have followed all the steps in the implementation plan. 

- Never delete already added requirements rows in `.rdd-instance/specifications/requirements.md`. If the entire requirement is already obsolete and nothing shall be left from it - replace its text (after the ID) with "[DELETED]".  

- Maintain existing structure and formatting of `.rdd-instance/specifications/requirements.md` - it should be accordingly the convention in `.rdd/conventions/requirements.convention.md` - always observe the rules in it. Inform the user in case of deviations from the convention. 

- **Error Handling**: At each step, if an error occurs, log error to implementation file, return error response to caller in the chat, preserve partial work (don't delete implementation file or undo changes), provide recovery guidance (re-run with fixes, manual intervention, rollback options) 

- Do not ask for permission (unless explicitly required) to continue if you have no blockers to proceed furhter. Do as much as you can without user input. *