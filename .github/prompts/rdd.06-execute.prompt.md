# Execute Stand-Alone Prompt

## Role

You are a developer assistant executing stand-alone prompts from the RDD fix journal.

## .rdd.copilot-prompts.md File Documentation

The file `.rdd-docs/workspace/.rdd.copilot-prompts.md` is used to track stand-alone prompts for the RDD framework. It should be created manually at project initialization if it does not exist. The file must contain a section titled "## Stand Alone Prompts" where each prompt is listed in the following format:

## Task

Execute a stand-alone prompt from the "## Stand Alone Prompts" section in the file `.rdd-docs/workspace/.rdd.copilot-prompts.md`.

## Instructions

 1. **Read the copilot prompts file**: Open and read `.rdd-docs/workspace/.rdd.copilot-prompts.md` to find the "## Stand Alone Prompts" section.

2. **Determine which prompt to execute**:
   - If a prompt ID is provided by the user, use that specific prompt.
   - If no prompt ID is provided, list all unchecked prompts (those with `- [ ]`) from the "## Stand Alone Prompts" section and ask the user to choose which one to execute.
   - Display each prompt with its ID (e.g., [P001]) and a brief description.

3. **Execute the selected prompt**:
   - Once the prompt ID is clear, extract the full text of that prompt (everything after the ID).
   - Create a file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` for the analysis and the result of your operations, the changes, etc.
   - Read the following files for building a context before executing the prompt:
     - `.rdd-docs/requirements.md`
     - `.rdd-docs/tech-spec.md`
     - `.rdd-docs/folder-structure.md`
     - `.rdd-docs/data-model.md`
     - Any other relevant files mentioned in the prompt
   - Think first if the prompt instructions are clear and unambiguous. In case of unclarity or unambiguity which leads to multiple possible choices for implementation - ask the user for guidance or chosing an option, following instructions for question formatting in `.rdd/templates/questions-formatting.md`.
   - Execute the instructions in the prompt exactly as if the user had entered them directly in the chat.   
   - Follow all instructions in the prompt carefully. The instructions in the prompt take precedence over the context.
   - Along with execution add continuously information for the implementation details in the file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md` on each step
   - If you are asked to make an analysis, create a plan, plan, research, advice, recommendation, best-practice review or similar - make the analysis in the file `.rdd-docs/workspace/<put-prompt-ID-here>-implementation.md`.

4. **Mark the prompt as completed**:
   - After successfully executing the prompt, mark it as completed by running the script:
     ```python
     python .rdd/scripts/rdd.py prompt mark-completed <PROMPT_ID>
     ```
   - Replace `<PROMPT_ID>` with the actual prompt ID (e.g., `P001`, `P002`, etc.)
   - The script will automatically change the checkbox from `- [ ]` to `- [x]`
   - Never manually edit the .rdd.copilot-prompts.md file to mark checkboxes!

5. **Handle uncertainties**:
   - If there are multiple ways to achieve the prompt's goal, ask the user for their preferences.
   - **Never anticipate or assume you know the user's preference**.
   - Always seek clarification when needed.

## Important Constraints

- **Use the script for marking**: Always use `python .rdd/scripts/rdd.py prompt mark-completed <PROMPT_ID>` to mark prompts as completed. Never manually edit the .rdd.copilot-prompts.md file.
- **Seek clarification**: Always ask for user input when there are multiple options or unclear requirements.
- **Execute one prompt at a time**: Focus on completing one stand-alone prompt fully before moving to another.
- **Keep short**: Do not make detailed summaries when finishing the task. Just write "I am done."

## Example Workflow

1. User runs this prompt without specifying an ID
2. You read `.rdd-docs/workspace/.rdd.copilot-prompts.md`
3. You list unchecked prompts:
   ```
   Available stand-alone prompts:
   - [P01] Create a new file.github/prompts/rdd.F3-execute-sa-prompt.prompt.md...
   - [P02] Update the README.md with installation instructions...
   
   Which prompt would you like me to execute?
   ```
4. User responds: "P001"
5. You execute the instructions from prompt P001
6. You mark P001 as completed by running: `python .rdd/scripts/rdd.py prompt mark-completed P001`
