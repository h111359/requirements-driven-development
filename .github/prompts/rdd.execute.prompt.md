# Execute Work Iteration Prompt

## Role

You are a developer assistant executing stand-alone prompts from the RDD fix journal.

## Context

The file `.rdd-docs/work-iteration-prompts.md` contains a list of prompts that the agent should execute when instructed. Follow the instructions which exactly prompt to be executed. If nothing provided - execute the smallest as ID prompt from type P. 

The id is the nn number after the letter P in the prompt preffix - format [Pnn]. For example P01 has ID = 1, P02 has ID = 2 and so on. When a given prompt execution is completed, the checkbox in front of it should be marked. 

The text of the promt starts immediately after the [Pnn] id and continuous untill the next promt id (next row starting with "- [ ]" or "- [x]" or "- [X]") or if this is the last promt and no more prompts are found - till the very end of the file. In case the exact text of the prompt can not be detected - stop and ask the user to clarify.

## Mandatory Rules: 

- In a single itteration should be executed only one of these prompts.
- Never execute a prompt (or parts of a prompt) which is marked as completed (starts with "- [x]")
- Never change anything else in the current file than marking a checkbox! Changing the checkbox to `- [x]` is **the only change you are allowed to do**. 


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
   - Read any other relevant files mentioned in the prompt and make a short summary on them in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md`
   - Think first if the prompt instructions are clear and unambiguous. In case of unclarity or unambiguity which leads to multiple possible choices for implementation - ask the user for guidance or chosing an option, following instructions for question formatting in `.rdd/templates/questions-formatting.md`.
   - Write in the `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` your detail plan how you will achieve the result asked in the prompt.
   - Execute the instructions in the prompt exactly as if the user had entered them directly in the chat.   
   - Follow all instructions in the prompt carefully. The instructions in the prompt take precedence over the context.
   - Along with execution add continuously information for the implementation details in the file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` on each step. Especially take care of adding the commands you run!
   - If you are asked to make an analysis, create a plan, plan, research, advice, recommendation, best-practice review or similar - make the analysis in the file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md`.


4. **Update the requirements file**:
   - According to all changes made during the execution of the prompt in the previous step, update the file `.rdd-docs/requirements.md` as adding new requirements rows in it or modifying requirement rows. Especially read the written in `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` and check against it. Never delete already added requirements rows, but if the entire requirement is already obsolete and nothing to be left from it - replace its text with "[DELETED]". Preserve ID sequences (never renumber existing IDs). When adding requirements, continue from highest existing ID in that section. Maintain existing structure and formatting. Validate that all ID sequences remain continuous in the respective secton and if the order is wrong - reorder the rows to be in correct order considering the section.

5. **Update the technical specification file**:
   - According to all changes made during the execution of the prompt in the previous step, update the `.rdd-docs/tech-spec.md`. Ensure all technical details, configurations, and implementation notes are accurate and up-to-date. Preserve ID sequences (never renumber existing IDs). When adding requirements, continue from highest existing ID in that section. Maintain existing structure and formatting. Validate that all ID sequences remain continuousReview all the sections. Especially for section "## Project Folder Structure" do the following:

    * Create or recreate in folder `.rdd-docs\workspace` a script named 
   `.rdd-docs\workspace\list-files.py` which lists all the file, folders and recursively their subfolders and stores the result in `.rdd-docs/workspace/files-list.md`. For each file write its name, relative path and the time of last change. Eclude folders and subfolders which start with "." or folders like "venv". 

   * Execute the script `.rdd-docs\workspace\list-files.py` in a terminal by running the script:
     ```python
     python .rdd-docs/workspace/list-files.py     
     ```
   
   * If it fails - stop and inform the user. Otherwise continue.

   * Create (or revise if exists) the file `.rdd-docs/workspace/files-analysis.md` and check if there are files in `.rdd-docs/workspace/files-list.md` which are missing or are with newer timestapm of the last change. For those - open the file, read it and add a short summary in `.rdd-docs/workspace/files-analysis.md` containing the relative path, type and only if it is readable - short summary of its content. Group the file entries and order them per folder they are in (same for the folders).

   * Based on the information in `.rdd-docs/workspace/files-analysis.md` update the content of `.rdd-docs/tech-spec.md` section "## Project Folder Structure" considering the current content of  this section only as an example of the format expected and not reflection of the reality (as it could be just an example or to be obsolete already). 

   * Compare the current content of `.rdd-docs/tech-spec.md` section "## Project Folder Structure" with the actual folder structure in `.rdd-docs/workspace/files-list.md` and ensure that all files and folders are represented there correctly with their purpose explained. Add missing files/folders, remove obsolete ones, and correct any inaccuracies.

6. **Mark the prompt as completed**:
   - After successfully executing the prompt, mark it as completed by running the script:
     ```python
     python .rdd/scripts/rdd.py prompt mark-completed <PROMPT_ID>
     ```
   - Replace `<PROMPT_ID>` with the actual prompt ID (e.g., `P001`, `P002`, etc.)
   - The script will automatically change the checkbox from `- [ ]` to `- [x]`
   - Never manually edit the work-iteration-prompts.md file to mark checkboxes!

7. **Handle uncertainties**:
   - If there are multiple ways to achieve the prompt's goal, ask the user for their preferences.
   - **Never anticipate or assume you know the user's preference**.
   - Always seek clarification when needed.

## Important Constraints

- **Use the script for marking**: Always use `python .rdd/scripts/rdd.py prompt mark-completed <PROMPT_ID>` to mark prompts as completed. Never manually edit the work-iteration-prompts.md file.
- **Seek clarification**: Always ask for user input when there are multiple options or unclear requirements. When asking questions, follow the guidelines in `.rdd/templates/questions-formatting.md`.
- **Execute one prompt at a time**: Focus on completing one stand-alone prompt fully before moving to another.
- **Keep short**: Do not make detailed summaries when finishing the task. Just write "I am done."

## Example Workflow 1

1. User runs this prompt without specifying an ID
2. You read `.rdd-docs/work-iteration-prompts.md`
3. You find that [P01] is the lowest unchecked prompt
5. You execute the instructions from prompt [P01]
6. You mark [P01] as completed by running: `python .rdd/scripts/rdd.py prompt mark-completed P01`

## Example Workflow 2

1. User runs this prompt specifying P03
2. You read `.rdd-docs/work-iteration-prompts.md`
3. You find that [P03] is an unchecked prompt
5. You execute the instructions from prompt [P03]
6. You mark [P03] as completed by running: `python .rdd/scripts/rdd.py prompt mark-completed P03`