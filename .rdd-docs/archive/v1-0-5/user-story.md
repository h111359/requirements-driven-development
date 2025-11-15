# User Story

## State

 - [ ] State 1: Not fulfilled "What is needed?"
 - [ ] State 2 "What is needed?" is fulfilled and not fulfilled "Why is it needed and for whom?"
 - [ ] State 3: "Why is it needed and for whom?" is fulfilled and not fulfilled "What are the acceptance criteria?"
 - [ ] State 4: All the main questions are answered - "What is needed?", "Why is it needed and for whom?", "What are the acceptance criteria?" and "What other considerations should be taken into account?" is not fulfilled
 - [ ] State 5: All the main questions are answered - "What is needed?", "Why is it needed and for whom?", "What are the acceptance criteria?", "What other considerations should be taken into account?" are fulfilled. "Requirements Questionnaire" is not generated
 - [ ] State 6: "Requirements Questionnaire" is generated, but not all questions are answered
 - [ ] State 7: "Requirements Questionnaire" is generated, all questions are answered, still not confirmed that no more questions are needed
- [x] State 8: No more questions are needed so the "Execution Plan" is generated, but not confirmed that it is detailed enough
- [ ] State 9: "Execution Plan" is considered not detailed enough and revision is needed

## What is needed?

<!-- Describe the feature, functionality, or change that needs to be implemented -->

Rewrite the existing RDD User Guide as a complete, simplified, and self-service oriented document. The new version must provide clear installation steps, execution instructions, workflow guidance, and conceptual explanations targeted at intermediate technical users. The content must be merged into a single, coherent guide stored at `templates/user-guide.md`.

 

Make it much simpler. Cover the following: 

- How to install 

- Running the rdd.bat or rdd.sh in VS Code or in separate terminal for initial Configuration of the default branch, version and local only flag 

- Use the menu to createnew  iteration. Brief explanation of the options in the script 

- When the iteration is created – explanation to use the `.rdd-docs/work-iteration-prompts.md` file to write prompts and then to use "/rdd.execute" command to run them 

- What is the meaning of .rdd.update prompt 
- 
- Explain that .rdd.analyze prompt is not intended to be executed using premium request needed models in GitHub Copilot chat but in a ChatGPT session as it is too iterative. 

- When finished – to use again the menu option to complete the iteration  

- To be clear that merge of the branch of the working iteration to the default or other branch is not part of the framework 

- To be explained the normal cycle of work 

 


Add RDD Concepts: 

 

- Simplicity: it has just one prompt, all work is done in the workspace folder. 

- Documentation: Keep the documentation in sync continuously 

- Thoughtfulness: Each prompt to be carefully written in a file and with that - documented in the project 

- Thriftiness: Copilot to be used only for "higly intellectual work" 

- Verbosity: Execution of each prompt to be logged in detail 

- Incrementality: The development is done via series of incremental changes without pre-defining the size of the increment 

- Historicity: All the work to be archived after work iteration completion 

- Agnostic: To be cross platform ready - both for Windows and Linux 

- Upgradeability: Easiness to upgrade and extend 

 

Add the following guidances: 

- Start new chat for each new prompt 
- Avoid writing next prompts in advance. Execute the latest written and then add the new one in wor-iteration-prompts.md 
- Do not write too simple (wasting premium requests) or too complex (could confuse the copilot) prompts 

- Always cite the full relative path to the files intended to be created. Do not assume the copilot will write them the correect place 
- Ask the copilot to fix the issue you are seeing alone. Explain how to reproduce and tell it to work until the issue is fixed. 
- Be careful when the copilot asks to install something – check if you are in venv. In general – installations are better to be done from humat (for now) 
- You can edit .vscode/settings.json to add commands so not to be asked to approve 
 

## Why is it needed and for whom?

<!-- Explain the problem being solved, the value delivered, and who will benefit from this change -->

The RDD framework currently lacks a clear and simple user guide suitable for users who want to install, configure, and work with the system independently.  
This story requires a complete rewrite of the User Guide, making it easier to understand while fully documenting the standard workflow, commands, prompts, concepts, and best practices. So the users to be able to install and work with the system on self-service base.

## What are the acceptance criteria?

<!-- List specific, measurable criteria that must be met for this user story to be considered complete -->

- [ ] The file `templates/user-guide.md` is updated accordingly the requirements
- [ ] The resulting guide must serve as a complete, step-by-step reference.
- [ ] The guide must: Explain installation steps for both Windows and Linux in a combined workflow with small OS-specific notes.
- [ ] The guide must: Describe how to run `rdd.bat` or `rdd.sh` inside VS Code terminal or a standalone terminal.
- [ ] The guide must: Explain initial configuration: default branch, version, and "local only" flag.
- [ ] The guide must: Describe using the menu to create a new iteration, including short explanations of all script options.
- [ ] The guide must: Document the prompt-based workflow using `.rdd-docs/work-iteration-prompts.md`.
- [ ] The guide must: Explain usage of `/rdd.execute`, `.rdd.update`, `.rdd.analyze` (and warning that `.rdd.analyze` must be run in ChatGPT, not GitHub Copilot).
- [ ] The guide must: Describe completing an iteration using the menu.
- [ ] The guide must: Clarify that branch merging is outside the RDD framework and left to the user’s standard Git workflow.
- [ ] The guide must: Introduce core RDD Concepts (simplicity, documentation, thoughtfulness, thriftiness, verbosity, incrementality, historicity, agnostic, upgradeability).
- [ ] The guide must: Provide best-practice tips throughout each step (new chat per prompt, avoid too trivial or too complex prompts, cite full relative paths, ask Copilot to fix issues iteratively, installation caution, using `.vscode/settings.json`).



## What other considerations should be taken into account?

<!-- Note any technical constraints, dependencies, risks, or other factors that should be considered during implementation -->

**Installation & Setup**:
- Provide a combined Windows/Linux installation process.
- Include OS-specific notes where relevant.
- Describe how to launch the RDD script from:
  - VS Code integrated terminal
  - External terminal

**Initial Configuration**:
- Describe how users configure:
  - Default branch
  - Version


## Requirements Questionnaire


**1. Scope of Rewrite**

* [x] **a) Complete rewrite from scratch**
* [ ] b) Partial rewrite
* [ ] c) Merge with existing structure
* [ ] z) Other

---

**2. Level of Detail**

* [ ] a) High-level only
* [x] **b) Medium detail (commands + short examples)**
* [ ] c) Full step-by-step detail
* [ ] z) Other

---

**3. Target Audience Technical Level**

* [ ] a) Beginner developers
* [x] **b) Intermediate developers**
* [ ] c) Advanced users
* [ ] z) Other

---

**4. OS Instructions**

* [x] **a) Combined workflow with OS-specific notes**
* [ ] b) Fully separate sections
* [ ] c) Only Windows
* [ ] d) Only Linux
* [ ] z) Other

---

**5. Script Execution Context**

* [x] **a) Show both VS Code terminal and external terminal usage**
* [ ] b) Recommend one and mention the other
* [ ] c) Generic terminal usage only
* [ ] z) Other

---

**6. RDD Concepts Placement**

* [x] **a) Separate chapter in the User Guide**
* [ ] b) Integrated throughout steps
* [ ] c) Short conceptual overview at top
* [ ] z) Other

---

**7. Guidance & Best Practices Formatting**

* [ ] a) Checklist
* [ ] b) “Best Practices” chapter
* [x] **c) Inline tips inside workflow steps**
* [ ] z) Other

---

**8. Acceptance Criteria Additions**

* [x] **a) Style requirements**
* [ ] b) Test user validation
* [ ] c) PO/maintainer review
* [ ] d) Markdown/lint check
* [ ] z) Other

---

**9. Branch Merging Clarification**

* [ ] a) Explicit warning **not** to perform merges
* [ ] b) Only clarify merges are outside the framework
* [x] **c) Provide minimal Git guidance ("merge in your usual workflow")**
* [ ] z) Other





## Execution Plan

- [ ] [P10] Complete rewrite of `templates/user-guide.md` with the following structure and content:
  
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

- [ ] [P11] Update `.rdd-docs/requirements.md` to add the following requirement (find the highest FR ID and increment by 1):
  
  **New Requirement:**
  - **[FR-XXX] User Guide Documentation**: The framework shall provide a comprehensive user guide (`templates/user-guide.md`) that explains the complete workflow, terminal menu options, Copilot prompt usage, RDD concepts (simplicity, documentation, thoughtfulness, thriftiness, verbosity, incrementality, historicity, agnostic, upgradeability), best practices, and self-service installation/operation guidance for intermediate technical users
  
  Ensure the ID is properly sequenced and the requirement follows the existing format in `requirements.md`.

- [ ] [P12] Update `.rdd-docs/tech-spec.md` in the "## Infrastructure" > "### Project Folder Structure" section to reflect that `templates/user-guide.md` is the authoritative user guide file and mention it is installed to `.rdd/` during the installation process for easy runtime access. Ensure consistency with the build and installation processes documented in the tech spec.

- [ ] [P13] Verify that `scripts/build.py` already includes `templates/user-guide.md` in the build archive (as mentioned in P03 of work-iteration-prompts.md). If not, update the build script to copy `templates/user-guide.md` to `.rdd/user-guide.md` in the build staging area so it's included in the release archive and available at runtime after installation.

- [ ] [P14] Review and test the complete user guide by:
  1. Reading through `templates/user-guide.md` to verify all sections are present and complete
  2. Checking that all file paths referenced exist (`.rdd/scripts/rdd.py`, `.rdd-docs/work-iteration-prompts.md`, `.github/prompts/rdd.*.prompt.md`, etc.)
  3. Verifying all command examples are accurate and work as documented
  4. Ensuring cross-references to requirements.md and tech-spec.md are correct
  5. Confirming OS-specific notes are present for both Windows and Linux/macOS
  6. Validating that the tone and detail level match the target audience (intermediate developers)
  7. Fix any issues found during this review




