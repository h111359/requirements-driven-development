## Definitions

- [WI-REGISTRY] is the file `.rdd-instance/workdir/work-iteration-registry.json`
  
- [PROMPT-REGISTRY] is the file `.rdd-instance/workdir/prompts-registry.md`

- [ACTIVE-PROMPT-ID] is the prompt-id of the prompt entry in `.rdd-instance/workdir/work-iteration-registry.json` which is with state `active`. The framework allows only one prompt to be in this state.

- [ACTIVE-PROMPT-FOLDER] is a folder in `.rdd-instance/workdir` with format 
  `<[ACTIVE-PROMPT-ID]>_<prompt-title>`

- [ACTIVE-PROMPT] is the file `prompt.md` in [ACTIVE-PROMPT-FOLDER]

- [PLAN] is the file `plan.md` in [ACTIVE-PROMPT-FOLDER]

- [IMPLEMENTATION] is the file `implementation.md` in [ACTIVE-PROMPT-FOLDER]

- [QUESTIONNAIRE-CONVENTION] is the file `.rdd/conventions/questions-formatting.md`
  
- [QUESTIONNAIRE] is a file containing questions to the user. The file location is in [active-prompt-folder]. The file name convention is `questionnaire.md`.

- [MODIFIER] is a key word written in the chat after the prompt file. The MODIFIER could be:
  * modification


## Instructions - Follow these steps exactly:  

1. **Read the registry**: Open and read the [WI-REGISTRY] file.
      
2. Identify the [ACTIVE-PROMPT-ID], [ACTIVE-PROMPT-FOLDER], [ACTIVE-PROMPT].

3. Check if the [PLAN] is fulfilled. If it is, you shall observe it in the next steps. Do not skip any of the steps in the plan. Do not stop the implementation until the entire plan is completed. 
   
4. Check if there are questions and answers in the [QUESTIONNAIRE]. If there are, you shall comply with the chosen answers in the next steps.

5. Check if the active prompt has `analyze-enabled` set to `true` in [WI-REGISTRY]. If it is set to true:
   * Write in the chat "Analyze mode" 
   * then follow the instructions in `.rdd/prompt-snippets/execution-step.analyze.md` and stop (do not continue with the next instructions here)

5.5. Check if the active prompt has `plan-enabled` set to `true` in [WI-REGISTRY]. If it is set to true:
   * Write in the chat "Plan mode" 
   * then follow the instructions in `.rdd/prompt-snippets/execution-step.plan.md`
   * after the plan execution is completed, execute `.rdd/src/actions/prompt_plan_off.py` to automatically disable plan mode
   * stop (do not continue with the next instructions here - do not execute implementation step)

6. If the user has added a [MODIFIER]
  
  *  modification:
     *  Should be followed by the number of the modification - read the text of the modification from [ACTIVE-PROMPT] (read it again as the user has changed it)
     *   Write in the chat "Modification <ID>" 
     *  Execute the instruction of the modification and stop (do not continue with the next instructions here)

7. If there is no modifier detected and analyze mode is not enabled - 
   * Write in the chat "No modifiers detected"
   * follow the instructions in `.rdd/prompt-snippets/execution-step.plan.md`
   * then follow the instructions in `.rdd/prompt-snippets/execution-step.implementation.md`
   * after the implementation is completed, execute `.rdd/src/actions/prompt_set_executed_on.py`



## Mandatory Rules:  

- **Be verbose in files**: When writing to files in `.rdd-instance/workdir/` folder, provide detailed explanations, reasoning, and context to ensure clarity for future reference. 

- **Keep short chat**: Do not make detailed summaries in the chat when finishing the task, unless for errors. Just write "I am done." 

- It is not supposed the steps to be executed in parallel - always follow the order of the steps as they are defined in the instructions above. Steps depend on the results of the previous steps! 

- At the end of the execution - verify you have followed all the steps. 

- Always read `.rdd-instance/specifications/requirements.md` and comply with it, unless the active prompt provides different instructions; in that case, the active prompt overrides `requirements.md`.

- Never delete already added requirements rows in `.rdd-instance/specifications/requirements.md`. If the entire requirement is already obsolete and nothing shall be left from it - replace its text (after the ID) with "[DELETED]".  

- Maintain existing structure and formatting of `.rdd-instance/specifications/requirements.md` - it should be accordingly the convention in `.rdd/conventions/requirements.convention.md` - always observe the rules in it. Inform the user in case of deviations from the convention. 

- **Error Handling**: At each step, if an error occurs, log error to implementation file, return error response to caller in the chat, preserve partial work (don't delete implementation file or undo changes), provide recovery guidance (re-run with fixes, manual intervention, rollback options) 

- Do not ask for permission (unless explicitly required) to continue if you have no blockers to proceed furhter. Do as much as you can without user input. *
  
- If you can proceed - keep going with the work, do not stop.