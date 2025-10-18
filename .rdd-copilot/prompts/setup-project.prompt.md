
# Role: 

You are here to deploy rdd-copilot product in a new workspace..

# Context:

C01: This prompt should leverage GitHub Copilot to automatically build full requirements driven development tool from `.rdd-copilot` folder. 

C02: In order the prompt to be execute manually, the user should copy-paste the following instruction at the chat area and run it.: 
```
Use and follow instructions in #file:.rdd-copilot/prompts/setup-project.prompt.md exactly.
```

# Rules:

There are **mandatory** rules you must follow when executing the steps.

R01: Do NOT delete any extra user-added files or folders that are not listed; simply ensure the minimum structure exists.

R02: Write before executing each step "Executing <step_number>"

R03: Write after executing each step "Completed <step_number>"

R04: The steps in Steps section must be followed in order.

# Steps:

S01: Display the following banner to the user:

```
───── RDD-COPILOT ─────
 Prompt: Project Setup                                    
 Description:                                             
 > Recreate full project structure from                   
 > .rdd-copilot assets: restore folders, move templates,  
 > seed documentation, and prepare prompts/instructions.  
 ──────────────────────

```

S02: Setup `.github` folder and its contents following the steps below

S02.01: If `.github/` folder does not exist, create it. If it already exists, leave it unchanged and skip all S02.* steps.

S02.02: If `.github/prompts` folder does not exist, create it. If it already exists, leave it unchanged.

S02.03: If `.github/instructions` folder does not exist, create it. If it already exists, leave it unchanged.

S02.04: If `.github/chatmodes` folder does not exist, create it. If it already exists, leave it unchanged.

S02.05: If the file `.rdd-copilot/templates/rdd-copilot.cr-create.prompt.md` exists and `.github/prompts/rdd-copilot.cr-create.prompt.md` does not exist, move it to `.github/prompts/`. If destination file exists, leave both unchanged.

S02.06: If the file `.rdd-copilot/templates/rdd-copilot.cr-clarify.prompt.md` exists and `.github/prompts/rdd-copilot.cr-clarify.prompt.md` does not exist, move it to `.github/prompts/`. If destination file exists, leave both unchanged.

S02.07: If the file `.rdd-copilot/templates/rdd-copilot.cr-design.prompt.md` exists and `.github/prompts/rdd-copilot.cr-design.prompt.md` does not exist, move it to `.github/prompts/`. If destination file exists, leave both unchanged.

S02.08: If the file `.rdd-copilot/templates/rdd-copilot.cr-implement.prompt.md` exists and `.github/prompts/rdd-copilot.cr-implement.prompt.md` does not exist, move it to `.github/prompts/`. If destination file exists, leave both unchanged.

S02.09: If the file `.rdd-copilot/templates/rdd-copilot.python.instructions.md` exists and `.github/instructions/rdd-copilot.python.instructions.md` does not exist, move it to `.github/instructions/`. If destination file exists, leave both unchanged.

S02.10: If the file `.rdd-copilot/templates/rdd-copilot.devops-core-principles.instructions.md` exists and `.github/instructions/rdd-copilot.devops-core-principles.instructions.md` does not exist, move it to `.github/instructions/`. If destination file exists, leave both unchanged.

S02.11: If the file `.rdd-copilot/templates/rdd-copilot.sql-sp-generation.instructions.md` exists and `.github/instructions/rdd-copilot.sql-sp-generation.instructions.md` does not exist, move it to `.github/instructions/`. If destination file exists, leave both unchanged.

S02.12: If the file `.rdd-copilot/templates/rdd-copilot.technologies.instructions.md` exists and `.github/instructions/rdd-copilot.technologies.instructions.md` does not exist, move it to `.github/instructions/`. If destination file exists, leave both unchanged.

S02.13: If the file `.rdd-copilot/templates/rdd-copilot.Agent.chatmode.md` exists and `.github/chatmodes/rdd-copilot.Agent.chatmode.md` does not exist, move it to `.github/chatmodes/`. If destination file exists, leave both unchanged.

S02.14: If the file `.rdd-copilot/templates/copilot-instructions.md` exists and `.github/copilot-instructions.md` does not exist, move it to `.github/`. If destination file exists, leave both unchanged.

S03 Setup `.rdd-docs` folder and its contents following the steps below

S03.01: If `.rdd-docs/` folder does not exist, create it. If it already exists, leave it unchanged and skipp all S03.* steps.

S03.02: If the file `.rdd-docs/requirements.md` does not exist, move the file `.rdd-copilot/templates/requirements.md` to `.rdd-docs/requirements.md`. If destination file exists, leave both unchanged.

S03.03: If the file `.rdd-docs/folder-structure.md` does not exist, move the file `.rdd-copilot/templates/folder-structure.md` to `.rdd-docs/folder-structure.md`. If destination file exists, leave both unchanged.

S03.04: If the file `.rdd-docs/technical-specification.md` does not exist, move the file `.rdd-copilot/templates/technical-specification.md` to `.rdd-docs/technical-specification.md`. If destination file exists, leave both unchanged.

S03.05: Move the folder `.rdd-copilot/templates` to `.rdd-docs/`. If destination folder exists, leave both unchanged.

S03.06: Create folder `.rdd-docs/change-requests`

S04: Provide a summary indicating for each file/folder whether it was "created" or "already-present".


