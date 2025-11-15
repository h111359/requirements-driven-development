# Work Iteration Prompts

## Prompt Definitions

 - [x] [P01] Write a python script in `scripts` named `config-management.py` which should work in a terminal. The script should read the file `.rdd-docs/config.json`, displays the current values for the version, the default branch and the local only flag from it to the user and asks if the major version, minor version, patch version or the default branch should be changed. If version major, the script should add 1 to the major part of the version - for example from 1.11.22 should become 2.11.22. If the choice of the user is version minor - the script should increase the minor version with 1, for example from 1.11.22 should become 1.12.22. And if patch - the script should increase the patch version with 1, for example from 1.11.22 should become 1.11.23. If the choice is the default branch - the script should list all the branches with numbers and the user should choose a number and the name of the branch should be written as "defaultBranch" value.
  
 - [x] [P02] Change `scripts/config-management.py` so each time when a change is made, to update the value of "lastModified" with the current time, keeping the format as it is currently.

 - [x] [P03] The file `templates/user-guide.md` is not included in the release while `scripts/build.py` is executed. Fix that.
 
 - [x] [P04] The files `.rdd-docs/folder-structure.md` and `.rdd-docs/data-model.md` should not exist as files anymore, but the information should be part of `.rdd-docs/tech-spec.md` and should be maintained up to date after each prompt there. All the references to `.rdd-docs/folder-structure.md` should be replaced with reference to a section "## Project Folder Structure" in `.rdd-docs/tech-spec.md`. All the references to `.rdd-docs/data-model.md` should be replaced with reference to a section "## Data Architecture" in `.rdd-docs/tech-spec.md`. The file `templates/tech-spec.md` is modified manually to reflect the new requirements. Modify `.rdd-docs/tech-spec.md` to include in it the current content of `.rdd-docs/folder-structure.md` and `.rdd-docs/data-model.md`. Also reflect these new requirements in:
 - .github/prompts/rdd.execute.prompt.md
 - .rdd/scripts/rdd.py
 - .rdd-docs/requirements.md
 - .rdd-docs/tech-spec.md
 - scripts/build.py
 - scripts/install.py
 - templates/user-guide.md
 - tests/build/conftest.py
 - tests/build/test_build.py
 - tests/python/conftest.py

 - [x] [P05] During installation when running the script install.py should remove all rdd.* prompts first, before installing (copying in `.github/prompts`) the rdd. prompts from the installation. Aim is to be replaced all prompts starting with "rdd." as there could be some left from previous releases.
  
 - [x] [P06] Do the following change as checking the functionality of all scripts and prompts to reflect it:
       1. The file `.rdd/templates/copilot-prompts.md` should be renamed to `.rdd/templates/work-iteration-prompts.md` (run a terminal command for that). 
       2. Change the expected location of `.rdd-docs/workplace/work-iteration-prompts.md` to `.rdd-docs/work-iteration-prompts.md`. 
       3. Change the logic in the scripts in `.rdd/scripts` so the file to be seeded from `.rdd/templates/work-iteration-prompts.md`. During execution of "3. Complete current iteration" step when running `.rdd/scripts/rdd.py`, make functionality `.rdd-docs/work-iteration-prompts.md` to be copied in the folder `.rdd-docs/workspace` + overwritten from `.rdd/templates/work-iteration-prompts.md` so to be reset to its initial state.  

- [x] [P07] Create a file user-story.md in `.rdd/templates` with a standard user story definition structure for answering the questions "What is needed?", "Why is needed and for whom?", "What are the acceptance criteria?", "What other considerations should be taken into account?". Change the functionalities so this file to be copied in `.rdd-docs` when "  1. Create new iteration" step is executed. The file should be seeded from .rdd/templates/user-story.md and when completing the iteration - to be copied in the workspace + rewritten from the template. During execution of "3. Complete current iteration" step when running `.rdd/scripts/rdd.py`, make functionality `.rdd-docs/user-story.md` to be copied in the folder `.rdd-docs/workspace` + overwritten from `.rdd/templates/user-story.md` so to be reset to its initial state.  
  
- [x] [P08] Add the logic in `scripts/config-management.py` in `.rdd/scripts/rdd.py` and make a menu entry for it - "5. Configuration". Change "5. Exit" to "9. Exit". Add also option to be edited "Local only flag"
  
- [x] [P09] Revise the `.github/prompts/rdd.analyse-and-plan.prompt.md` prompt. This prompt could be executed multiple times but will have different effect based on the state of the file `.rdd-docs/user-story.md`. Change it so it is appropriate for any state in which `.rdd-docs/user-story.md` could be. The states are defined in the current partially fulfilled user story `.rdd-docs/user-story.md`. Use the story `.rdd-docs/user-story.md` as example for the needed format. Change the `.rdd/templates/user-story.md` template to reflect this new format. The prompt `.github/prompts/rdd.analyse-and-plan.prompt.md`  should:
    1. Detect in which state the user story is and if the state correctly reflects the reality (and change it if not)
    2. Should generate a "Requirements Questionnaire" including all the questions, that need to be answered. For the purpose should follow the instructions in `.rdd/templates/requirements-format.md` how to generate the questions. Also should use `.rdd/templates/clarity-checklist.md` to find if those checks are covered. It is not necessary the `.rdd/user-story.md` itself to cover all the checks - some of the answers could be written already in `.rdd-docs/requirements.md` or in `.rdd-docs/tech-spec.md` - verify agains those files as well, without changing them. And if still the information is not found - generate a question.
    3. When all the questions are generated and answered, the prompt should check if there is need of more questions. If yes - adds the question, if no - proceed with generation of the plan.
    4. If the state is '"Execution Plan" is considered not detailed enough and revision is needed' - the prompt should take care either to generate more questions (and to reflect the status to some appropriate earlier state) or directly to generate more detailed plan
The generted plan should follown the structure of `.rdd/templates/work-iteration-prompts.md` and should start with the lowest P id accordingly `.rdd-docs/work-iteration-prompts.md`.
The current state in `.rdd-docs/user-story.md` is only an example - do not execute it and do not change it.

- [x] [P10] Using the collected information in `.rdd-docs/user-story.md`, complete rewrite of `templates/user-guide.md` with the following structure and content:
  
  **Structure:**
  1. **Introduction** - Brief overview of RDD framework and what this guide covers
  2. **Installation** - Combined Windows/Linux installation steps with OS-specific notes (use install.sh for Linux/macOS, install.bat for Windows)
  3. **Initial Setup** - Running rdd.bat/rdd.sh in VS Code or separate terminal, initial configuration (default branch, version, local-only flag) using the interactive menu
  4. **Core Workflow** - Normal development cycle from iteration creation to completion
  5. **Creating New Iteration** - Using menu option 1 to create new iteration, brief explanation of what happens (branch creation, workspace initialization)
  6. **Working with Prompts** - Explain `.rdd-docs/work-iteration-prompts.md` file structure, how to write prompts, using `/rdd.execute` command in GitHub Copilot Chat
  7. **Special Prompts** - Explain `.rdd.update` prompt purpose (updating documentation), `.rdd.analyze` prompt (warning: use in ChatGPT not GitHub Copilot due to iterative nature and premium requests)
  8. **Completing Iteration** - Using menu option 3 to complete iteration (archiving, committing, pushing reminder)
  9. **Branch Merging** - Clear statement that merging work iteration branch to default/other branch is NOT part of RDD framework, handled by user's standard Git workflow
  10. **RDD Concepts** - Separate chapter explaining: Simplicity (one prompt, workspace-based), Documentation (continuous sync), Thoughtfulness (documented prompts), Thriftiness (Copilot for high-value work), Verbosity (detailed logging), Incrementality (series of increments), Historicity (work archiving), Agnostic (cross-platform), Upgradeability (easy to extend)
  11. **Best Practices & Guidelines** - Inline tips throughout workflow steps covering: start new chat per prompt, avoid writing prompts in advance (execute then add next), don't write too simple/complex prompts, always cite full relative paths, ask Copilot to fix issues alone with reproduction steps, be careful with installations (check venv), edit `.vscode/settings.json` to add auto-approve commands
  
  **Requirements:**
  - Target audience: intermediate developers
  - Medium detail level: include commands with short examples
  - OS-specific notes inline where relevant (e.g., "On Linux/macOS use `./rdd.sh`, on Windows use `rdd.bat`")
  - Both VS Code integrated terminal and external terminal usage shown
  - All commands referenced from existing scripts in `.rdd/scripts/` (especially `rdd.py`)
  - Reference existing documentation: `.rdd-docs/requirements.md`, `.rdd-docs/tech-spec.md`
  - Clear, concise language suitable for self-service usage
  - Include examples for complex concepts
  - Cross-reference with existing prompt files in `.github/prompts/`
  
  **Style:**
  - Use markdown formatting with proper headers, code blocks, lists
  - Include visual separators between major sections
  - Use callout boxes (> **Note:**) for important information
  - Code examples in appropriate syntax-highlighted blocks
  - Consistent terminology matching `requirements.md` and `tech-spec.md`

- [x] [P11] Add `templates/RDD-Framework-User-Guide.pdf` in the build and installation scripts so it appears in the same location as the file user-giude.md