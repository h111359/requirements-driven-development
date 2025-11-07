## Project Backlog
This file defines user stories, features, and tasks for GitHub Copilot to use as development context.


## Issues

### Issue 4: Add gitignore

#### Overview:

**Status:** CLOSED
**Created by:** h111359
**Created at:** 2025-10-31

#### Description (first comment):

> ## What:
> 
> Appropriate to the repo content .gitignore file to be added.
> 
> ## Why:
> 
> To be avoided unnecessary tracking of files which are not contributing to the main code > of the repo
> 
> ## Acceptance Criteria:
> 
> - The whole repo and all the files in it (main branch) should be revised so to be well > understood the repo structure and meaning
> - .gitignore file to be created in the root folder of the repo
> - gitignore to follow the best practices, still to be avoided unnecessary complexity
> - .github, .vscode and .rdd should not be excluded
> - The development to be made in a separate fix branch named as per the specified in .> rdd-docs/version-control.md
> - PR with added .gitignore file 


### Issue 12: Replace change with enhancement

#### Overview:

**Status:** CLOSED
**Created by:** h111359
**Created at:** 2025-11-02

#### Description (first comment):

> ## What:
>
> I want to stop using "change" as term in RDD and to start using "enhancement" instead. For branches prefixes instead of "feat" should be used "enh".
>
> ## Why:
>
> Enhancement is more popular term and more clearly represent the idea of applying feature/issue/user story.
>
> ## Acceptance Criteria:
>
> - When creating a new branch the possible options to be enhancement and fix
> - the script change-utils.sh should remain with the same name, but to be revised as code and whenever inside is used feat or feature - to be changed to enh/enhancement
> - The file .rdd-docs/requirements.md to be updated with enhancement terminology. To be explained that change = enhncement or fix
> - To be searched all the files in .github and the terminology to be changed whenever appropriate
> - To be searched all the files in .rdd and the terminology to be changed whenever appropriate
> - To be searched all the files in .rdd-docs and the terminology to be changed whenever appropriate


### Issue 13: journal becomes copilot-prompts

#### Overview:

**Status:** CLOSED
**Created by:** h111359
**Created at:** 2025-11-02

#### Description (first comment):

> ## What:
>
> Rename journal.md to copilot-prompts.md
>
> ## Why:
>
> Journal term do not represent the true meaning.
>
> ## Acceptance Criteria
>
> - The template journal.md to be renamed to copilot-prompts.md
> - All the references to journal.md in the files in .github/prompts/, .rdd/scripts/, .rdd/templates, .rdd-docs/ to be changed to copilot-prompts.md


### Issue 18: clarification taxonomy to checklist

#### Overview:

**Status:** CLOSED
**Created by:** h111359
**Created at:** 2025-11-02

#### Description (first comment):

> ## What:
>
> Rename `clarity-taxonomy.md` to `clarity-checklist.md`.
>
> ## Why:
>
> The new name better represents the purpose and content of the file.
>
> ## Acceptance Criteria:
>
> - The file `.rdd/templates/clarity-taxonomy.md` is renamed to `.rdd/templates/clarity-checklist.md`.
> - All scripts in `.rdd/scripts` are revised, and all references to `clarity-taxonomy.md` are changed to `clarity-checklist.md`.
> - All files in `.rdd/templates` are revised, and all references to `clarity-taxonomy.md` are changed to `clarity-checklist.md`.
> - All files in `.rdd-docs` or its subfolders (excluding `archive`) are revised, and all references to `clarity-taxonomy.md` are changed to `clarity-checklist.md`.
> - All files in `.github` or its subfolders are revised, and all references to `clarity-taxonomy.md` are changed to `clarity-checklist.md`.


### Issue 21: rdd terminal menu

#### Overview:

**Status:** CLOSED
**Created by:** h111359
**Created at:** 2025-11-03

#### Description (first comment):

> ## **What**
>
> Enhance `.rdd/scripts/rdd.sh` so that when it is executed **without parameters**, it displays a **navigable terminal menu**.
> The menu should allow **keyboard navigation (arrow keys / numbers / Enter)** and display a list of available actions.
> When a user selects an option, the script should execute the corresponding command.
>
> ## **Why**
>
> Users may not easily remember all available script options.
> A **visual, interactive terminal menu** helps users quickly explore available functionalities and execute desired actions with minimal typing and effort.
>
> ## **Acceptance Criteria**
>
> * [ ] Running `.rdd/scripts/rdd.sh` without arguments opens an **ASCII-based interactive menu**.
> * [ ] The menu is **visually structured** and user-friendly.
> * [ ] Users can **navigate** through options using the **keyboard** (e.g., arrow keys or numbers).
> * [ ] Upon selection, the script **executes** the corresponding command.
> * [ ] Optional: Include a **"Help" or "Exit"** option for better UX.
> * [ ] Highlight the currently selected option for clarity.
> * [ ] Support submenus or grouped commands if needed.
> * [ ] Ensure compatibility with common terminal emulators (bash, zsh).


### Issue 24: rdd.08-wrap-up

#### Overview:

**Status:** CLOSED
**Created by:** h111359
**Created at:** 2025-11-03

#### Description (first comment):

> ##b **What:**
> Create a new GitHub Copilot prompt file named `.github/prompts/rdd.08-wrap-up.prompt.md`.
> This prompt should automate the finalization of a development task by:
>
> 1. Checks if there are uncommitted changes and if there are - notifies and stops
> 2. Moving the workspace content into an archive directory
> 3. Committing to include the archived content 
> 5. Push to remote
>
> ## **Why:**
> To make the completion of a fix or enhancement simple, consistent, and reliable — minimizing manual operations while maintaining user control through confirmations.
>
> ## **Acceptance Criteria:**
>
> * [ ] Use the scripts in `.rdd/scripts` for actions. If there is no appropriate script or command in it - create a new functionality in `.rdd/scripts/branch-utils.sh`
> * [ ] `.github/prompts/rdd.08-wrap-up.prompt.md` file created.
> * [ ] The files in workspace is moved into new subfolder under `.rdd-docs/archive` with a name equal to the name of the branch
> * [ ] After move of the files in the workspace, a commit is created to capture archived files with message: `"archive: moved workspace to archive"`.
> * [ ] The script pushes changes to the remote branch.
> * [ ] Ask for user confirmation before execution.
> * [ ] The process displays clear terminal feedback after each action.


### Issue 26: G4-update-from-main

#### Overview:

**Status:** CLOSED
**Created by:** h111359
**Created at:** 2025-11-03

#### Description (first comment):

> **What:**
> Create a new GitHub Copilot prompt file named `.github/prompts/rdd.G4-update-from-main.prompt.md`.
> This prompt should automatically update the current branch with the latest commits from `main`, while safely handling local changes and stopping for manual resolution if conflicts arise.
>
> **Why:**
> To keep the current branch synchronized with `main` after others merge changes — ensuring stability, preserving local work, and allowing manual control when conflicts occur.
>
> **Acceptance Criteria:**
>
> * [ ] `.github/prompts/rdd.G4-branch-main-apply.prompt.md` file created.
> * [ ] Prompt remains short and minimal.
> * [ ] Calls `.rdd/scripts/rdd.sh` for all automatable operations.
> * [ ] Missing functionality should be added or extended in `.rdd/scripts`.
> * [ ] The process must:
>   1. **Stash** all uncommitted local changes.
>   2. **Pull** the latest `main` branch from remote.
>   3. **Merge** `main` into the current branch.
>   4. **Restore** the stashed changes (leave them uncommitted).
> * [ ] If merge conflicts occur, **pause** and let the user resolve them manually.
> * [ ] Provide clear terminal feedback at every step.
> * [ ] Execute automatically, with **no confirmations** required.


### Issue 29: Build for Windows

#### Overview:

**Status:** OPEN
**Created by:** h111359
**Created at:** 2025-11-03

#### Description (first comment):

> **What:**
> Enhance the build process so that executing `scripts/build.sh` automatically creates **two platform-specific release zip files** in the `build` folder:
>
> * `rdd-linux-<version>.zip` → containing the standard Linux `.sh` scripts and prompts.
> * `rdd-windows-<version>.zip` → containing automatically generated PowerShell (`.ps1`) equivalents of the same scripts and prompts.
>
> **Why:**
> To maintain synchronized, cross-platform releases for Linux and Windows — while keeping Linux as the main development environment and generating Windows-compatible versions automatically.
>
> **Acceptance Criteria:**
>
> * [ ] Running `scripts/build.sh` produces two zip files: one for Linux, one for Windows.
> * [ ] Filenames include version tagging (e.g., `rdd-linux-v1.3.2.zip`).
> * [ ] Folder and file structure in both archives is identical.
> * [ ] PowerShell scripts are generated automatically from the corresponding Linux `.sh` scripts — including consistent functionality, comments, and parameters.
> * [ ] Only `.ps1` scripts are included in the Windows build (no `.sh` files).
> * [ ] The process integrates cleanly into the existing build flow.
> * [ ] Console output clearly indicates build progress and results.


