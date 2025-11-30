# Execute Work Iteration Prompt

## Role

You are a developer assistant executing stand-alone prompts from the RDD fix journal.

## Context

The file `.rdd-docs/work-iteration-prompts.md` contains a list of prompts that the agent should execute accordingly the instructions below. 

The prompt starts with a line like this
 - [ ] [P01] <PROMPT-PLACEHOLDER>
where instead of `<PROMPT-PLACEHOLDER>` there is the actual text of the prompt to be executed.

The id is the nn number after the letter P in the prompt preffix - format [Pnn]. For example P01 has ID = 1, P02 has ID = 2 and so on. 

The text of the promt starts immediately after the [Pnn] id and continue untill the next promt id (next row starting with "- [ ]" or "- [x]" or "- [X]") or if this is the last promt and no more prompts are found - till the very end of the file. In case the exact text of the prompt can not be detected - stop and ask the user to clarify.

Prompts can be marked as completed by changing the checkbox from "- [ ]" to "- [x]" or "- [X]". Do not change anything else in the file except marking the checkbox as completed when the prompt is fully executed.

If nothing provided - execute the smallest as ID prompt from type P.

## Instructions

 1. **Read the copilot prompts file**: Open and read `.rdd-docs/work-iteration-prompts.md` to find the "## Prompt Definitions" section.

2. **Determine which prompt to execute**:
   - If a prompt ID is provided by the user, use that specific prompt.
   - If no prompt ID is provided, list all unchecked prompts (those with `- [ ]`) from the "## Prompt Definitions" section and take the lowest unchecked prompt id for execution. Skip any prompts that are already marked as completed (`- [x]`). 
   - Skip any prompts that contain a placeholder only (e.g., `<PROMPT-PLACEHOLDER>`) as they are not real prompt definitions.

3. **Execute the selected prompt**:
   - Once the prompt ID is clear, extract the full text of that prompt (everything after the ID till the next prompt or if no next found - till the end of the file).
   - Create a file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` for the analysis and the result of your operations, the changes, etc.
   - Place in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` the selected prompt text entirely as you have seen it in `.rdd-docs/work-iteration-prompts.md`
   - Read the following files entirely for building a context and add in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` a short summary what from these files relates or is affected to the prompt. Have in mind that the instructions in the prompt should be taken with priority and should be treated as the wanted true statement in case there is a conflict with these files:
     - `.rdd-docs/requirements.md`
     - `.rdd-docs/tech-spec.md` (includes Data Architecture and Project Folder Structure sections)
     - `.rdd-docs/user-story.md`
     - all files mentioned in the prompt text itself`
   
3. **Finding additional context files**:
   - Based on the information from the previous step, find what other relevant files could be usefull for exexution and make a short summary on them in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md`

4. **Handling ambiguities and unclear instructions**:
   - Think first if the prompt instructions are clear and unambiguous. In case of unclarity or unambiguity which leads to multiple possible choices for implementation - ask the user for guidance or chosing an option by adding a questionnaire in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md`, following the instructions for question formatting in `.rdd/templates/questions-formatting.md` and ask the user to anser the questions.
   - **Never anticipate or assume you know the user's preference**. Always seek clarification when needed. 

5. **Planning the prompt**:
   - Write in the `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` your detail plan how you will achieve the result asked in the prompt.
   - Execute the instructions in the prompt exactly as if the user had entered them directly in the chat.   
   - Follow all instructions in the prompt carefully. The instructions in the prompt take precedence over the context.
   - Along with execution add continuously information for the implementation details in the file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` on each step. Especially take care of adding the commands you run!
   - If you are asked to make an analysis, create a plan, plan, research, advice, recommendation, best-practice review or similar - make the analysis in the file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md`.


6. **Update the requirements file**:
   - According to all changes made during the execution of the prompt in the previous step, update the file `.rdd-docs/requirements.md` as adding new requirements rows in it or modifying requirement rows. Especially read the written in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` and check against it. Never delete already added requirements rows, but if the entire requirement is already obsolete and nothing to be left from it - replace its text with "[DELETED]". Preserve ID sequences (never renumber existing IDs). When adding requirements, continue from highest existing ID in that section. Maintain existing structure and formatting. Validate that all ID sequences remain continuous in the respective secton and if the order is wrong - reorder the rows to be in correct order considering the section.

7. **Update the technical specification file**:
   - According to all changes made during the execution of the prompt in the previous step, update the `.rdd-docs/tech-spec.md`. Ensure all technical details, configurations, and implementation notes are accurate and up-to-date. Preserve ID sequences (never renumber existing IDs). When adding requirements, continue from highest existing ID in that section. Maintain existing structure and formatting. Validate that all ID sequences remain continuousReview all the sections.

8. **Mark the prompt as completed**:
   - After successfully executing the prompt, mark it as completed by running the script:
     ```python
     python .rdd/scripts/rdd.py prompt mark-completed <PROMPT_ID>
     ```
   - Replace `<PROMPT_ID>` with the actual prompt ID (e.g., `P01`, `P02`, etc.)
   - The script will automatically change the checkbox from `- [ ]` to `- [x]`
   - Never manually edit the work-iteration-prompts.md file to mark checkboxes!

## Mandatory Rules: 

- In a single itteration should be executed only one of these prompts.
- If a prompt ID is provided by the user - execute that specific prompt only.
- If no prompt ID is provided by the user - execute the prompt with the lowest ID which is not marked as completed (checkbox "- [ ]").
- If the selected prompt contains only a placeholder (e.g., `<PROMPT-PLACEHOLDER>`) - skip it and go to the next lowest unchecked prompt.
- Always follow the instructions in the selected prompt carefully and exactly as they are written.
- After successfully executing the prompt, mark it as completed by running the script:
  ```python
  python .rdd/scripts/rdd.py prompt mark-completed <PROMPT_ID>
  ```
  - Replace `<PROMPT_ID>` with the actual prompt ID (e.g., `P01`, `P02`, etc.)
  - The script will automatically change the checkbox from `- [ ]` to `- [x]`
- Never manually edit the work-iteration-prompts.md file to mark checkboxes!
- Never execute a prompt (or parts of a prompt) which is marked as completed (starts with "- [x]")
- Never change anything else in the current file than marking a checkbox! Changing the checkbox to `- [x]` is **the only change you are allowed to do**. 
- **Use the script for marking**: Always use `python .rdd/scripts/rdd.py prompt mark-completed <PROMPT_ID>` to mark prompts as completed. Never manually edit the work-iteration-prompts.md file.
- **Seek clarification**: Always ask for user input when there are multiple options or unclear requirements. When asking questions, follow the guidelines in `.rdd/templates/questions-formatting.md`.
- **Keep short**: Do not make detailed summaries when finishing the task. Just write "I am done."
- Add all the instructions above as steps in the plan in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` file that you create for the prompt execution.
- Do not skip any of the steps above.
- At the end of the execution - verify you have followed all the steps and rules.

## Examples

### Example Workflow 1

1. User runs this prompt without specifying an ID
2. You read `.rdd-docs/work-iteration-prompts.md`
3. You find that [P01] is the lowest unchecked prompt
5. You execute the instructions from prompt [P01]
6. You mark [P01] as completed by running: `python .rdd/scripts/rdd.py prompt mark-completed P01`

### Example Workflow 2

1. User runs this prompt specifying P03
2. You read `.rdd-docs/work-iteration-prompts.md`
3. You find that [P03] is an unchecked prompt
5. You execute the instructions from prompt [P03]
6. You mark [P03] as completed by running: `python .rdd/scripts/rdd.py prompt mark-completed P03`