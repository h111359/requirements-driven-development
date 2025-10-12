# Project Setup Instructions

> Use these instructions with GitHub Copilot to automatically recreate the full project template from only the `.rdd-copilot` folder. This will restore all folders and files as described below, with exact content for each file.

## 1. Create `.vscode` folder and its contents

- Create folder: `.vscode`
- Create file: `.vscode/settings.json` with three color values for:
  - `titleBar.activeBackground`
  - `titleBar.inactiveBackground`
    (use template content from `.rdd-copilot/templates/vscode-settings.json`)

## 2. Setup `.github` folder and its contents

- If `.github/` folder does not exist, create it. If it already exists, leave it unchanged.

- Create file: `.github/prompts/rdd-copilot.cr-create-tasks.prompt.md` (use template content from `.rdd-copilot/templates/rdd-copilot.task-creator.prompt.md`)

- Create file: `.github/prompts/rdd-copilot.task-execute.prompt.md` (use template content from `.rdd-copilot/templates/rdd-copilot.task-executor.prompt.md`)

- Create file: `.github/prompts/rdd-copilot.cr-create.prompt.md` (use template content from `.rdd-copilot/templates/cr-create.prompt.md`)

- Create file: `.github/prompts/rdd-copilot.cr-clarify.prompt.md` (use template content from `.rdd-copilot/templates/cr-clarify.prompt.md`)

- Create file: `.github/prompts/rdd-copilot.cr-design.prompt.md` (use template content from `.rdd-copilot/templates/cr-design.prompt.md`)

- Create file: `.github/prompts/rdd-copilot.cr-complete.prompt.md` (use template content from `.rdd-copilot/templates/cr-complete.prompt.md`)

- Create file: `.github/instructions/rdd-copilot.python.instructions.md` (use template content from `.rdd-copilot/templates/rdd-copilot.python.instructions.md`)

- Create file: `.github/instructions/rdd-copilot.devops-core-principles.instructions.md` (use template content from `.rdd-copilot/templates/rdd-copilot.devops-core-principles.instructions.md`)

- Create file: `.github/instructions/rdd-copilot.sql-sp-generation.instructions.md` (use template content from `.rdd-copilot/templates/rdd-copilot.sql-sp-generation.instructions.md`)

- Create file: `.github/instructions/rdd-copilot.technologies.instructions.md` (use template content from `.rdd-copilot/templates/rdd-copilot.technologies.instructions.md`)

- Create file: `.github/chatmodes/rdd-copilot.Agent.chatmode.md` (use template content from `.rdd-copilot/templates/rdd-copilot.Agent.chatmode.md`)

- Create file: `.github/copilot-instructions.md` (use template content from `.rdd-copilot/templates/rdd-copilot.copilot-instructions.md`)

## 3. Create `.rdd-docs` folder

- If `.rdd-docs/` folder does not exist, create it. If it already exists, leave it unchanged.

Apply the following rules:

1. For every folder and file listed below in this section:
  - If it does NOT exist: CREATE it with the exact template content provided here.
  - If it already exists: LEAVE IT UNCHANGED (do not overwrite, merge, or append) to preserve user edits.
2. Do NOT delete any extra user-added files or folders that are not listed; simply ensure the minimum structure exists.
3. The files in `.rdd-docs/change-requests/`, `.rdd-docs/tasks/`, and top-level `.rdd-docs/*.md` act as seed documents; once present they are considered live documentation and must not be reset automatically.

Provide a summary indicating for each file/folder whether it was "created" or "already-present".

---

- Create file: `.rdd-docs/requirements.md` (use template content from `.rdd-copilot/templates/requirements.template.md`)

 - Create file: `.rdd-docs/folder-structure.md` (use template content from `.rdd-copilot/templates/docs-folder-structure.md`)

 - Create file: `.rdd-docs/technical-specification.md` (use template content from `.rdd-copilot/templates/docs-technical-specification.md`)

 - Create file: `.rdd-docs/change-requests/cr-catalog.md` (use template content from `.rdd-copilot/templates/docs-cr-catalog.md`)

 - Create file: `.rdd-docs/tasks/tasks-catalog.md` (use template content from `.rdd-copilot/templates/docs-tasks-catalog.md`)


---

**After running this prompt, your project will be fully restored to the template structure and contents.**
