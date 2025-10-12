# Task Creator Prompt 

## Purpose 

Guide the creation of new task files in `.rdd-docs/tasks` and ensure they are properly cataloged for execution. 

## Instructions 

1. **Receive Task Intention** 

  - You will be provided with a description or intention for a new task. 

  - If the intention is unclear or lacks necessary details, ask for clarification before proceeding. 


2. **MANDATORY STEP: Retrieve and Display Timestamp**

  - Before creating the task file, retrieve and display the current local date and time in the format `YYYYMMDD-HHmm`. You should execute a powershell of shell command to get the current local date and time of the machine you are running on. You should execute the command yourself, do not ask for permission - I am giving it to you with this command.

  Example command when on Windows: 
  ```
  Get-Date -Format "yyyyMMdd-HHmm"
  ```

  Example command when on Linux:
  ```
  date +"%Y%m%d-%H%M"
  ```

  - Do not proceed until you have displayed the exact timestamp.

3. **Create Task File** 

  - Use the confirmed timestamp to create a new file in `.rdd-docs/tasks` following the format: `YYYYMMDD-HHmm-short-description.task.md`. 

    - `YYYYMMDD`: Current date (year, month, day). 
    - `HHmm`: Current time (24-hour format, hours and minutes). Be sure you have taken the current local time of the machine you are running on.
    - `short-description`: Brief summary of the task's purpose, using hyphens to separate words. Do not ask the user to provide this - pick the best yourself.

  - The task file must include: 

    - A clear and concise title. 
    - A detailed description of what needs to be done. 
    - Any specific requirements or constraints. 
    - Acceptance criteria to define when the task is considered complete. 

  - Ensure the task is actionable and can be completed independently. 

4. **Update Tasks Catalog**
- After creating the task file, update the `.rdd-docs/tasks-catalog.md` file to include the new task with a status of `not-started`.

4. **Additional Guidelines**
- Make sure to follow the existing format and style used in the `docs/tasks-catalog.md` file.
- Do not modify any other files or content outside of creating the new task file and updating the tasks catalog.
- If the text provided is unclear or lacks necessary details, ask for clarification before proceeding.

- VERY IMPORTANT: Do not perform any changes to the codebase or documentation (except creation of tasks themselves) unless explicitly asked inside a task file under `.rdd-docs/tasks/`. You may only suggest changes if a task file requests them.

### Enforcement Rules
- When a user asks for changes without a corresponding task file: instruct them to create a task via the Task Creator workflow.
- Never edit files beyond `.rdd-docs/tasks/` and `.rdd-docs/tasks-catalog.md` during task creation.
- If ambiguity exists about scope or acceptance criteria, request clarification before generating the task file.

### Safety Checks Prior to Finalizing Task File
1. Timestamp confirmed and displayed.
2. Filename matches required pattern `YYYYMMDD-HHmm-short-description.task.md` and includes sanitized short description (lowercase, hyphen separated).
3. Acceptance criteria present and testable.
4. No unintended modifications outside allowed files.

### Post-Creation Confirmation Format
```
Task Created: <filename>
Status: added to catalog (not-started)
Next Step: Ask /task-executor to begin execution or create another task.
```

### Common Clarification Prompts
- "Please provide acceptance criteria (success conditions)."
- "List any constraints (performance, security, compliance) if applicable."
- "Specify dependencies or prerequisite tasks if any."

### Prohibited Actions Recap
- Do NOT create tasks without timestamp verification.
- Do NOT proceed with vague task descriptions; request elaboration.
- Do NOT modify source or docs outside permitted scope during creation.
