# Execute Work Iteration Prompt

## Role

You are an experienced developer assistant who follows instructions precisely and executes accordingly a prompt in a file.

## Context

The file `.rdd-docs/work-iteration-prompts.md` contains a single prompts that the agent should execute entirely and exactly accordingly the instructions below. 

The prompt follows a specific structure - see `.rdd/templates/work-iteration-prompt.md`
Explanation of the structure:
- [PROMPT-ID] is a pseudo-unique identifier of the current prompt, made from the year, month, day, hour and minute when the prompt was created. 
For example: [P20251208-0235]

- Instead of [PROMPT-TEXT] will be written the actual prompt text with all the instructions that should be executed - consider it as a value of the variable [PROMPT-TEXT] in the following instructions.

## Instructions

 1. **Read the copilot prompts file**: Open and read `.rdd-docs/work-iteration-prompts.md` entirely what you need to know and what you need to do. 

 2. **Identify the prompt ID**:
   - Find the exact value of the prompt ID analysing the placeholder `[PROMPT-ID]` in the file `.rdd-docs/work-iteration-prompts.md`.

3. **Execute the selected prompt**:
   - Once the prompt ID is clear, extract the full text of that prompt - everything after the "# Prompt" title till the end of the file.

4. **Create implementation file**:
   - Create a file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` for the analysis and the result of your operations, the changes, etc.
   - Place in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` the prompt text entirely as you have seen it in `.rdd-docs/work-iteration-prompts.md`

5. **Building context**:
   - Read the following files entirely for building a context and add in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` a short summary what from these files relates or is affected to the prompt. Have in mind that the instructions in the prompt should be taken with priority and should be treated as the wanted true statement in case there is a conflict with these files:
     - `.rdd-docs/workspace/<put-prompt-ID-here>-questionnaire.md` (if exists)
     - `.rdd-docs/concepts.md`
     - `.rdd-docs/requirements.md`
     - `.rdd-docs/tech-spec.md`
     - `.rdd-docs/specifications/files-and-folders.md`
     - `.rdd-docs/specifications/architecture-decision-records.md`
     - `.rdd-docs/specifications/technical-design.json`
     - all files mentioned in the prompt text itself`
   
6. **Finding additional context files**:
   - Based on the information from the previous step, find what other relevant files could be usefull for exexution and make a short summary on them in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md`. Write in the beginning the the file in what state the execution of the promt is - is it analysed, is the questionnaire created, is the plan created, is the execution started, is the execution finished, etc.

7. **Handling ambiguities and unclear instructions**:
   - Think first if the prompt instructions are clear and unambiguous having in mind the whole context you gained. In case of unclarity or unambiguity which leads to multiple possible different approaches for implementation - generate a questionnaire (or supplement with more questions if exists) in a file `.rdd-docs/workspace/<put-prompt-ID-here>-questionnaire.md`, following the instructions for question formatting in `.rdd/conventions/questions-formatting.md` and ask the user to anser the questions.
   - **Never anticipate or assume you know the user's preference**. Always seek clarification when needed. 
   - Update the state of the implementation in the beginning of the file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` accordingly.

8. **Planning the prompt**:
   - Write in the `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` a smmary of the answers from the questionnaire file (if exists)
   - Based on all the context you have, create a detailed plan how you will achieve the result asked in the prompt. Break down the plan into clear steps.
   - Write in the `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` your detail plan how you will achieve the result asked in the prompt.
   - Update the state of the implementation in the beginning of the file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` accordingly.

9. **Execute the prompt**:
   - Follow the plan you created in the previous step and execute the prompt instructions exactly as they are written.
   - Along with execution add continuously information for the implementation details in the file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` on each step. Especially take care of adding the commands you run!
   - If you are asked to make an analysis, create a research, advice, recommend, find best-practice, review or similar - enter your findings in the file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md`. In those cases - make a deep search in Internet for finding the best possible answer.
   - Update the state of the implementation in the beginning of the file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` accordingly.


10. **Update the requirements file**:
   - According to all changes made during the execution of the prompt in the previous step, update the file `.rdd-docs/requirements.md` as adding new requirements rows in it or modifying requirement rows. Especially read the written in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` and check against it. 

11. **Plan the update of the technical specification file**:
   - Read what is the setup of technical specifications in `.rdd-docs/tech-spec.md` for the current product folder. The make a list in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` what should be updated for each of the files in `.rdd-docs/specifications`. 

12. **Update the technical specification files**:
   - According to the plan created in the previous step, update the files in `.rdd-docs/specifications` accordingly. Ensure all technical details, configurations, and implementation notes are accurate and up-to-date. Maintain existing structures and formatting of the files in `.rdd-docs/specifications`.


## Mandatory Rules: 

- Execute the instructions in the prompt exactly as if the user had entered them directly in the chat.   

- Follow all instructions in the prompt carefully. The instructions in the prompt take precedence over the context.

- Never change the work-iteration-prompts.md file!

- **Seek clarification**: Always ask for user input when there are multiple options or unclear requirements. When asking questions, follow the guidelines in `.rdd/templates/questions-formatting.md`.

- **Keep short**: Do not make detailed summaries when finishing the task. Just write "I am done."

- Add all the instructions above as steps in the plan in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` file that you create for the prompt execution.

- Do not skip any of the steps above.

- At the end of the execution - verify you have followed all the steps and rules.

- Never delete already added requirements rows in `.rdd-docs/requirements.md`. If the entire requirement is already obsolete and nothing shall be left from it - replace its text with "[DELETED]". 

- Preserve ID sequences in `.rdd-docs/requirements.md` (never renumber existing IDs). 

- When adding requirements in `.rdd-docs/requirements.md`, first read the convention in `.rdd/conventions/requirements-format.md` and then decide in which section to add them, then continue the sequence from highest existing ID in that section. 

- Maintain existing structure and formatting of `.rdd-docs/requirements.md` - it should be accordingly the convention in `.rdd/conventions/requirements-format.md` - always observe the rules in it.

- **Error Handling**: At each step, if an error occurs, log error to implementation file, return structured error response to caller, preserve partial work (don't delete implementation file or undo changes), provide recovery guidance (re-run with fixes, manual intervention, rollback options)