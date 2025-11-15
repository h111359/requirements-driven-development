# RDD Framework User Guide

**Requirements-Driven Development Framework**  
*A comprehensive guide for AI-assisted development with GitHub Copilot*

---

## 📖 Table of Contents

1. [Introduction](#1-introduction)
2. [Installation](#2-installation)
3. [Initial Setup](#3-initial-setup)
4. [Core Workflow](#4-core-workflow)
5. [Creating New Iteration](#5-creating-new-iteration)
6. [Working with Prompts](#6-working-with-prompts)
7. [Special Prompts](#7-special-prompts)
8. [Completing Iteration](#8-completing-iteration)
9. [Branch Merging](#9-branch-merging)
10. [RDD Concepts](#10-rdd-concepts)
11. [Best Practices & Guidelines](#11-best-practices--guidelines)

---

## 1. Introduction

The Requirements-Driven Development (RDD) framework is a structured workflow system designed to streamline development with GitHub Copilot. It provides a simple, workspace-based approach to managing iterations, documenting requirements, and executing development tasks through AI assistance.

### What This Guide Covers

This guide will teach you how to:
- Install and configure the RDD framework in your project
- Use the interactive terminal menu to manage development iterations
- Write and execute prompts for GitHub Copilot
- Maintain synchronized documentation throughout development
- Follow best practices for effective AI-assisted development

### Who This Guide Is For

This guide is written for intermediate developers who are comfortable with:
- Command-line interfaces and terminal usage
- Git version control basics
- VS Code or similar code editors
- Basic Python concepts

---

## 2. Installation

The RDD framework installation process is straightforward and consistent across Windows, Linux, and macOS platforms.

### Prerequisites

Before installing, ensure you have:
- **Python 3.7+** installed and accessible via the `python` command
- **Git 2.23+** for version control
- A Git repository initialized in your project directory

> **Note for Linux/macOS users**: The framework uses the `python` command. If not available, install `python-is-python3` on Debian/Ubuntu (`sudo apt install python-is-python3`) or create an alias in your shell configuration.

### Download the Release

1. Visit the [RDD GitHub Releases page](https://github.com/h111359/requirements-driven-development/releases)
2. Download the latest `rdd-v{version}.zip` file
3. Extract the archive to a temporary location

### Run the Installer

**On Linux/macOS:**
```bash
cd /path/to/extracted/rdd-v{version}
chmod +x install.sh
./install.sh
```

**On Windows:**
```cmd
cd C:\path\to\extracted\rdd-v{version}
install.bat
```

> **Note**: You can also run the installer directly with Python: `python install.py`

### Installation Options

The installer will guide you through several configuration options:

1. **Target Directory**: Choose your project folder (use GUI browser or enter path manually)
2. **Local-Only Mode**: Select whether your repository uses a GitHub remote or operates locally only
3. **Default Branch**: Choose from existing branches (main, dev, master, or enter custom name)

The installer automatically:
- Copies RDD framework files to `.rdd/` in your project
- Installs GitHub Copilot prompts to `.github/prompts/`
- Copies documentation templates to `.rdd-docs/`
- Merges VS Code settings (if `.vscode/settings.json` exists)
- Updates `.gitignore` to exclude workspace files
- Installs launcher scripts (`rdd.sh` for Linux/macOS, `rdd.bat` for Windows) to your project root

### Verify Installation

After installation completes, verify it's working:

```bash
cd /your/project/directory
python .rdd/scripts/rdd.py --version
```

Expected output: `RDD Framework v{version} (Python)`

> **Tip**: You can now run the RDD menu from your project root using `./rdd.sh` (Linux/macOS) or `rdd.bat` (Windows) instead of typing the full Python command.

---

## 3. Initial Setup

After installation, run the RDD menu to configure the framework for your project.

### Starting the RDD Menu

You can run the RDD menu in two ways:

**Using the launcher script (recommended):**
```bash
# Linux/macOS - from VS Code integrated terminal or external terminal
./rdd.sh

# Windows - from VS Code integrated terminal or external terminal
rdd.bat
```

**Using Python directly:**
```bash
python .rdd/scripts/rdd.py
```

> **Tip**: The launcher scripts work in both VS Code's integrated terminal and external terminal windows. Use whichever you prefer.

### Initial Configuration

When you first run the RDD menu, you'll see the main menu with your current branch and default branch displayed:

```
╔══════════════════════════════════════════════════════════╗
║                    RDD Framework                         ║
║            Requirements-Driven Development               ║
╚══════════════════════════════════════════════════════════╝

Current branch: main
Default branch: main

RDD Framework - Main Menu:
1. Create new iteration
2. Update from default
3. Complete current iteration
4. Delete merged branches
5. Configuration
9. Exit

Enter your choice (1-9):
```

### Configuration Menu (Option 5)

Select option 5 to access the configuration menu where you can:

- **Update version** (major, minor, or patch increments)
- **Change default branch** (select from list of existing branches)
- **Toggle local-only flag** (enable/disable GitHub remote operations)

Example configuration session:
```
Configuration Menu:
1. Update version (major)
2. Update version (minor)
3. Update version (patch)
4. Change default branch
5. Toggle local-only mode (currently: disabled)
6. Back to main menu

Enter your choice (1-6): 4

Available branches:
  1. main
  2. dev
  3. master

Select branch number: 2

✓ Default branch changed to: dev
```

> **Note**: Configuration changes are saved to `.rdd-docs/config.json` and persist across sessions.

> **Tip**: When managing installations, be careful to check if you're working in a virtual environment. It's generally better to let humans handle installations for now rather than letting Copilot install packages that might affect your system.

---

## 4. Core Workflow

The RDD framework follows a simple, repeatable cycle for each development iteration.

### Normal Development Cycle

```
┌────────────────────────────────────────────────────────┐
│               ITERATION WORKFLOW CYCLE                  │
└────────────────────────────────────────────────────────┘

1. CREATE NEW ITERATION (Menu Option 1)
   • Start from default branch with empty workspace
   • Provide branch name
   • Framework creates branch and initializes workspace
         ↓
2. DEFINE WORK IN PROMPTS FILE
   • Edit .rdd-docs/work-iteration-prompts.md
   • Write clear, specific prompts for Copilot
   • Cite full relative paths to files
         ↓
3. EXECUTE PROMPTS WITH COPILOT
   • Use /rdd.execute command in GitHub Copilot Chat
   • Copilot implements each prompt
   • Implementation files created in workspace
         ↓
4. (OPTIONAL) UPDATE FROM DEFAULT (Menu Option 2)
   • Sync your branch with latest default branch changes
   • Resolve conflicts if any
         ↓
5. COMPLETE ITERATION (Menu Option 3)
   • Archives workspace with timestamp
   • Commits all changes
   • Optionally pushes to remote
   • Returns to default branch
         ↓
6. CREATE PULL REQUEST (Manual, Outside RDD)
   • Use GitHub web interface
   • Request code review
         ↓
7. MERGE & CLEANUP (Menu Option 4)
   • After PR is merged, delete merged branches
```

### Understanding Workflow States

- **Ready to start**: On default branch, workspace empty → Use option 1
- **Active development**: On feature branch, executing prompts → Use /rdd.execute
- **Ready to complete**: All prompts done → Use option 3
- **After PR merge**: Branches merged to default → Use option 4

> **Best Practice**: Start a new chat session for each prompt execution. This keeps the context focused and reduces confusion from previous conversations.

---

## 5. Creating New Iteration

Starting a new iteration creates a feature branch and sets up your workspace for development.

### Using Menu Option 1

Select option 1 from the main menu: **Create new iteration**

### Prerequisites

Before creating a new iteration:
- ✓ You must be on the default branch
- ✓ Workspace must be empty (`.rdd-docs/workspace/` should not exist or be empty)

If these conditions aren't met, the framework will display an error and guide you to fix the issue.

### What Happens During Creation

1. **Branch Name Prompt**: You'll be asked to enter a branch name
   ```
   Enter branch name: fix user login bug
   ```

2. **Name Normalization**: The name is automatically converted to kebab-case
   ```
   Normalized: fix-user-login-bug
   ```

3. **Branch Creation**: A new Git branch is created and checked out
   ```bash
   git checkout -b fix-user-login-bug
   ```

4. **Workspace Initialization**: The workspace is initialized with a prompts file
   - File created: `.rdd-docs/work-iteration-prompts.md`
   - Seeded from template: `.rdd/templates/work-iteration-prompts.md`

### After Creation

You're now ready to define work. Open `.rdd-docs/work-iteration-prompts.md` and start adding prompts for Copilot to execute.

Example initial workspace:
```markdown
# Work Iteration Prompts

## Prompt Definitions

 - [ ] [P01] <Add your first prompt here>
```

> **Tip**: Don't write all prompts in advance. Execute one prompt, see the results, then add the next prompt. This iterative approach keeps you responsive to what Copilot discovers during implementation.

---

## 6. Working with Prompts

The heart of RDD development is the `work-iteration-prompts.md` file where you define specific tasks for GitHub Copilot to execute.

### The Prompts File Structure

**Location**: `.rdd-docs/work-iteration-prompts.md`

**Format**:
```markdown
# Work Iteration Prompts

## Prompt Definitions

 - [ ] [P01] Create user authentication module in `src/auth.py` with login 
   and logout functions. Include input validation.
 - [ ] [P02] Add unit tests for authentication in `tests/test_auth.py`. Cover 
   valid login, invalid password, and missing username cases.
 - [x] [P03] Update README.md with authentication usage examples
```

**Components**:
- **Checkbox**: `- [ ]` for pending, `- [x]` for completed
- **Prompt ID**: `[P01]`, `[P02]`, etc. (unique identifier)
- **Instructions**: Clear, detailed description with file paths

### Writing Effective Prompts

**Good Prompt Characteristics**:
- ✓ Specific and actionable
- ✓ Includes full relative file paths
- ✓ References existing patterns or files
- ✓ Has clear expected outcomes
- ✓ Single responsibility

**Example Good Prompt**:
```markdown
 - [ ] [P01] Create a validation utility in `src/utils/validators.py` with 
   functions for email validation (RFC 5322 format) and phone number validation 
   (E.164 format). Include docstrings following Google style guide. Add 
   comprehensive unit tests in `tests/utils/test_validators.py` with 100% 
   coverage.
```

**Example Bad Prompt** (too vague):
```markdown
 - [ ] [P01] Add validation
```

**Why It's Bad**: No file path, no specifics on what to validate, no examples

> **Best Practice**: Always cite the full relative path to files you want Copilot to create or modify. Don't assume Copilot will figure out where files should go.

### Executing Prompts in GitHub Copilot Chat

1. Open **VS Code** with GitHub Copilot installed
2. Open **Copilot Chat** (Ctrl+Shift+I / Cmd+Shift+I)
3. Ensure you're using an appropriate model (e.g., Claude Sonnet 4, GPT-4)
4. Execute the prompt:

```
/rdd.execute P01
```

Or execute the next uncompleted prompt automatically:

```
/rdd.execute
```

### What Happens During Execution

When you run `/rdd.execute P01`, Copilot:

1. **Reads the prompt** from `.rdd-docs/work-iteration-prompts.md`
2. **Reads context files** (`.rdd-docs/requirements.md`, `.rdd-docs/tech-spec.md`)
3. **Executes the instructions** (creates files, writes code, runs tests)
4. **Creates implementation file** at `.rdd-docs/workspace/P01-implementation.md`
5. **Marks prompt completed** by running:
   ```bash
   python .rdd/scripts/rdd.py prompt mark-completed P01
   ```

> **Important**: Never manually edit checkboxes in `work-iteration-prompts.md`. Let the framework mark them automatically.

### Implementation Files

For each executed prompt, an implementation file is created:

**File**: `.rdd-docs/workspace/P<ID>-implementation.md`

**Example** (`P01-implementation.md`):
```markdown
# P01 Implementation - User Authentication Module

## Prompt Text
Create user authentication module in src/auth.py with login and logout 
functions. Include input validation.

## Analysis
Reviewed existing project structure. Found auth patterns in src/api/ that 
should be followed.

## Implementation Details
Created files:
- src/auth.py (authentication logic)
- tests/test_auth.py (unit tests)

Commands executed:
- pytest tests/test_auth.py

Results:
- All 12 tests passed
- 100% code coverage achieved

## Changes Made
- Added login() function with username/password validation
- Added logout() function with session cleanup
- Added input sanitization for SQL injection prevention
```

> **Tip**: Ask Copilot to fix issues it encounters on its own. Describe how to reproduce the problem and tell it to iterate until fixed. This leverages Copilot's problem-solving capabilities.

### Prompt Execution Order

You can execute prompts in any order if they're independent:

**Sequential (Dependent)**:
```markdown
 - [ ] [P01] Create database schema in migrations/001_init.sql
 - [ ] [P02] Create User model in src/models/user.py (depends on P01)
 - [ ] [P03] Create user API in src/api/users.py (depends on P02)
```
Execute: P01 → P02 → P03

**Parallel (Independent)**:
```markdown
 - [ ] [P01] Update frontend styles in static/css/
 - [ ] [P02] Add backend logging in src/utils/logger.py
 - [ ] [P03] Write deployment docs in docs/deploy.md
```
Execute: Any order (P01, P02, P03 or P02, P01, P03, etc.)

---

## 7. Special Prompts

The RDD framework includes special-purpose prompts for documentation and planning.

### The `.rdd.update` Prompt

**Purpose**: Update documentation after completing development work

**Location**: `.github/prompts/rdd.update.prompt.md`

**When to Use**:
- After all development prompts are executed
- Before completing the iteration
- To synchronize requirements and tech spec with code changes

**Usage in Copilot Chat**:
```
/rdd.update
```

or add as a prompt in your work-iteration-prompts.md:
```markdown
 - [ ] [P99] Use the .rdd.update prompt to update all documentation
```

**What It Does**:
1. Analyzes all implementation files in `.rdd-docs/workspace/`
2. Identifies changes (new features, bug fixes, documentation updates)
3. Updates `.rdd-docs/requirements.md` with new/modified requirements
4. Updates `.rdd-docs/tech-spec.md` (including Project Folder Structure and Data Architecture sections)
5. Ensures documentation stays in sync with code

> **Tip**: Always run `.rdd.update` before completing an iteration to keep your project documentation accurate.

### The `.rdd.analyze` Prompt

**Purpose**: Iterative requirement clarification and execution planning

**Location**: `.github/prompts/rdd.analyse-and-plan.prompt.md`

**When to Use**:
- At the start of a complex iteration
- When requirements are unclear
- To generate a detailed execution plan

> **⚠️ WARNING**: This prompt is iterative and could consume multiple premium requests. Try to clarify the user story manually or outside VS Code with GitHub Copilot first.

**What It Does**:
1. Reads your user story from `.rdd-docs/user-story.md`
2. Guides you through requirement clarification using a state-based workflow
3. Generates a Requirements Questionnaire with multiple-choice questions
4. Creates a detailed execution plan with sequenced prompts
5. Ensures all clarity criteria are met before implementation

**State-Based Workflow**:
- States 1-4: Collect main questions (What, Why, Acceptance Criteria, Other Considerations)
- State 5: Generate Requirements Questionnaire
- State 6-7: Answer questions and confirm completeness
- State 8-9: Generate and refine Execution Plan

---

## 8. Completing Iteration

When all prompts are executed and documentation is updated, complete the iteration using menu option 3.

### Using Menu Option 3

Select option 3 from the main menu: **Complete current iteration**

### Prerequisites

Before completing:
- ✓ You must be on a feature branch (NOT on default branch)
- ✓ Workspace must NOT be empty (you must have done some work)

### What Happens During Completion

1. **Workspace Archiving**:
   - All files from `.rdd-docs/workspace/` are copied to `.rdd-docs/archive/<branch-name>/`
   - Archive metadata file created with timestamp, branch name, author, commit info
   - Example archive location: `.rdd-docs/archive/fix-user-login-bug/`

2. **Automatic Commit**:
   - All changes committed with message: `"Completing work on <branch-name>"`
   - Includes code changes, documentation updates, and workspace files

3. **Push Prompt** (if not in local-only mode):
   ```
   Push branch to remote? (y/n):
   ```
   - If yes: Branch is pushed to origin
   - Displays reminder to create pull request on GitHub

4. **Return to Default Branch**:
   - Checks out the default branch
   - Workspace is cleared (ready for next iteration)

### After Completion

Your iteration is now complete:
- ✓ Work is archived and committed
- ✓ You're back on the default branch
- ✓ Workspace is empty and ready for the next iteration

**Next Steps**:
1. Create a pull request on GitHub (see section 9)
2. Request code review from team members
3. Merge after approval
4. Use menu option 4 to delete the merged branch locally

---

## 9. Branch Merging

**Important**: Merging your work iteration branch to the default branch or any other branch is **NOT part of the RDD framework**. This is handled through your standard Git workflow.

### The RDD Framework Stops Here

The RDD framework helps you:
- ✓ Create and manage work iteration branches
- ✓ Execute development tasks with Copilot
- ✓ Document changes automatically
- ✓ Archive completed work
- ✓ Commit and optionally push changes

The RDD framework does **NOT**:
- ✗ Create pull requests
- ✗ Merge branches
- ✗ Handle code reviews
- ✗ Manage branch protection rules

### Your Standard Git Workflow

After completing an iteration (menu option 3), you should:

1. **Create Pull Request**:
   - Go to your GitHub repository
   - Create a PR from your feature branch to the default branch
   - Fill in description, link issues, add reviewers

2. **Code Review**:
   - Team members review your changes
   - Address feedback and make revisions if needed
   - Push additional commits to the same branch

3. **Merge**:
   - After approval, merge the PR using GitHub's interface
   - Choose your merge strategy (merge commit, squash, rebase)
   - Delete the remote branch (GitHub can do this automatically)

4. **Cleanup Locally**:
   - Use RDD menu option 4 to delete merged branches locally
   - This keeps your local repository clean

### Example Workflow

```bash
# After completing iteration with RDD (option 3)
# Your branch was pushed: fix-user-login-bug

# On GitHub:
1. Create PR: fix-user-login-bug → main
2. Request review
3. Address feedback (push more commits if needed)
4. Merge PR after approval
5. Delete branch on GitHub

# Back in RDD terminal:
./rdd.sh
# Select option 4 (Delete merged branches)
# Select the merged branch to delete locally
```

---

## 10. RDD Concepts

The RDD framework is built on ten core concepts that guide its design and usage.

### 1. Simplicity

**One prompt to rule them all, workspace-based approach**

RDD provides a single entry point (`.rdd/scripts/rdd.py` or launcher scripts) for all operations. Everything happens in the workspace directory, keeping the mental model simple.

- Single menu interface for all operations
- Single command for prompt execution (`/rdd.execute`)
- All work contained in `.rdd-docs/` directory
- No complex configuration files or scattered state

### 2. Documentation

**Keep documentation in sync continuously**

Documentation is not an afterthought—it's updated throughout the development cycle. The `.rdd.update` prompt ensures requirements and technical specifications stay current with code changes.

- Requirements updated after every iteration
- Tech spec reflects actual implementation
- Implementation files provide historical context
- No documentation drift

### 3. Thoughtfulness

**Documented prompts encourage careful planning**

Each prompt is written down in `work-iteration-prompts.md` before execution. This forces you to think through what you're asking Copilot to do and creates a permanent record of development decisions.

- Prompts are explicit and reviewable
- Implementation is traceable to specific prompts
- Team members can see what was requested and why
- Historical record of all development work

### 4. Thriftiness

**Copilot for high-value intellectual work only**

Use GitHub Copilot for complex development tasks where AI adds significant value. Don't waste premium requests on trivial tasks you can do manually.

- Let Copilot handle complex logic and algorithms
- Let Copilot write comprehensive tests
- Let Copilot update documentation systematically
- Don't use Copilot for simple renaming or formatting

> **Tip**: Don't write prompts that are too simple (waste of premium requests) or too complex (might confuse Copilot). Find the sweet spot where Copilot adds real value.

### 5. Verbosity

**Detailed logging of each prompt execution**

Every prompt execution creates an implementation file that documents what was done, why, and how. This verbose logging provides transparency and aids debugging.

- Implementation files capture all details
- Commands executed are logged
- Results and outcomes documented
- Easy to trace issues back to specific prompts

### 6. Incrementality

**Series of small increments without predefined size**

Development happens through a series of prompts of varying size and complexity. There's no forced increment size—you choose what makes sense for each task.

- Work breakdown is flexible
- Increments can be as small or large as needed
- Each prompt stands alone
- Easy to pause and resume work

### 7. Historicity

**Complete archiving of all work iterations**

When you complete an iteration, the entire workspace is archived with metadata. This creates a permanent historical record of every development cycle.

- Archives in `.rdd-docs/archive/<branch-name>/`
- Includes all implementation files
- Metadata with timestamps, author, commit info
- Never lose context from past iterations

### 8. Agnostic

**Cross-platform ready (Windows, Linux, macOS)**

The framework works identically on Windows, Linux, and macOS. Python-based implementation ensures consistent behavior across all platforms.

- Same commands work everywhere
- Launcher scripts for each platform
- No platform-specific dependencies
- Consistent file paths and operations

### 9. Upgradeability

**Easy to extend and customize**

The framework is designed to be extended. Add new prompts, customize templates, integrate additional tools—the modular design supports growth.

- Custom prompts in `.github/prompts/`
- Customizable templates in `.rdd/templates/`
- Python scripts are readable and modifiable
- Clear separation of concerns

### 10. (Reserved)

**Space for future concepts as framework evolves**

---

## 11. Best Practices & Guidelines

Follow these practices to get the most out of the RDD framework.

### Start New Chat for Each Prompt

**Why**: Keeps context focused, prevents confusion from previous conversations

**Do This**:
```
1. Execute P01 in Copilot Chat
2. Close chat or start new conversation
3. Execute P02 in fresh Copilot Chat
```

**Don't Do This**:
```
1. Execute P01
2. Execute P02 in same chat
3. Execute P03 in same chat (context polluted)
```

### Avoid Writing Prompts in Advance

**Why**: Implementation reveals new requirements, pre-written prompts become stale

**Do This**:
```
1. Write P01, execute it
2. Review results, learn from implementation
3. Write P02 based on what you learned
4. Execute P02, repeat cycle
```

**Don't Do This**:
```
1. Write P01, P02, P03, P04, P05 all at once
2. Execute them sequentially
3. Discover P03-P05 are no longer relevant
```

> **Tip**: Execute one prompt, see what happens, then decide what comes next. This responsive approach is more effective than planning everything upfront.

### Always Cite Full Relative Paths

**Why**: Prevents Copilot from guessing where files should go

**Do This**:
```markdown
 - [ ] [P01] Create authentication module in `src/auth/authenticator.py`
```

**Don't Do This**:
```markdown
 - [ ] [P01] Create authentication module
```

**More Examples**:
- ✓ `Update the API documentation in docs/api/endpoints.md`
- ✗ `Update the API documentation`
- ✓ `Add unit tests to tests/unit/test_validators.py`
- ✗ `Add unit tests`

### Ask Copilot to Fix Issues Alone

**Why**: Leverages Copilot's problem-solving capabilities, reduces manual debugging

**Do This**:
```
Copilot, the test in tests/test_auth.py is failing with "AttributeError: 
'NoneType' object has no attribute 'username'". This happens when running 
`pytest tests/test_auth.py::test_login_success`. Please investigate, fix 
the issue, and verify all tests pass.
```

**Don't Do This**:
```
Copilot, there's a test failure. What should I do?
```

**Include**:
- Error message (full text)
- Steps to reproduce
- Which file/test is affected
- What behavior is expected

> **Tip**: Ask Copilot to work iteratively until the issue is fixed. Give it room to try different approaches.

### Be Careful with Installations

**Why**: Package installations can affect your system environment

**Do This**:
1. Check if you're in a virtual environment (`venv` or `conda`)
2. Review what Copilot wants to install
3. Consider doing installations manually

**Don't Do This**:
- Let Copilot install system-wide packages without review
- Install packages blindly in production environments

> **Tip**: When Copilot suggests installing packages, verify you're in the correct environment (check for `venv` activation). It's generally safer to handle installations manually for now.

### Configure Auto-Approve Commands

**Why**: Speeds up workflow, reduces interruptions for trusted scripts

**Do This**:

Edit `.vscode/settings.json`:
```json
{
  "chat.tools.terminal.autoApprove": [
    ".rdd/scripts/**"
  ]
}
```

This auto-approves all RDD framework script executions.

**Benefits**:
- No confirmation prompts for trusted RDD scripts
- Faster prompt execution
- Smoother workflow

> **Note**: Only auto-approve scripts you trust. The RDD framework scripts are safe to auto-approve.

### Keep Prompts at the Right Complexity Level

**Too Simple (Wastes Premium Requests)**:
```markdown
 - [ ] [P01] Fix typo in README
```
→ You can do this manually in 5 seconds

**Too Complex (Might Confuse Copilot)**:
```markdown
 - [ ] [P01] Redesign the entire authentication system, migrate the database, 
   update all API endpoints, rewrite the frontend, update all tests, and 
   deploy to production
```
→ Break into 10+ smaller prompts

**Just Right**:
```markdown
 - [ ] [P01] Refactor authentication module in `src/auth.py` to use JWT tokens 
   instead of session cookies. Update login/logout functions, add token 
   validation middleware, and update unit tests in `tests/test_auth.py`.
```
→ Substantial work, clear scope, actionable

### Reference Existing Documentation

**Why**: Ensures consistency, helps Copilot understand context

**Do This**:
```markdown
 - [ ] [P01] Add user registration endpoint following the patterns in 
   .rdd-docs/tech-spec.md section "API Design Patterns". Create endpoint 
   in src/api/users.py matching the structure of src/api/auth.py.
```

**Don't Do This**:
```markdown
 - [ ] [P01] Add user registration endpoint
```

**Reference These Files**:
- `.rdd-docs/requirements.md` for functional requirements
- `.rdd-docs/tech-spec.md` for architecture and patterns
- Existing code files for style and structure

### Use Update-From-Default Regularly

**Why**: Prevents large merge conflicts, keeps your branch current

**Do This**:
- Run menu option 2 (Update from default) daily or every few commits
- Merge small changes frequently
- Resolve conflicts while they're small

**Don't Do This**:
- Work for weeks without syncing
- Wait until completion to merge default branch
- Accumulate large divergences

**When to Update**:
- Start of each day
- After teammates merge to default branch
- Before completing your iteration

### Verify Work Before Completing

**Why**: Catch issues before archiving and committing

**Do This**:
```bash
# Run tests
pytest tests/

# Check linting
pylint src/
flake8 src/

# Verify changes
git diff
git status

# Test manually if applicable
python src/main.py
```

**Don't Do This**:
- Complete iteration without running tests
- Assume Copilot's implementation is perfect
- Skip manual verification

---

## Summary

The RDD framework provides:

✅ **Simple Interface**: Single menu for all operations  
✅ **Prompt-Driven Development**: Clear, documented tasks for Copilot  
✅ **Automatic Documentation**: Requirements and specs stay in sync  
✅ **Complete Archiving**: Historical record of all work  
✅ **Cross-Platform**: Works on Windows, Linux, and macOS  

**Key Takeaways**:

1. Always start iterations from default branch with empty workspace
2. Write one prompt at a time, execute, then add the next
3. Cite full relative file paths in every prompt
4. Use `.rdd.update` to sync documentation before completing
5. Use `.rdd.analyze` in ChatGPT (not Copilot) for complex planning
6. Complete iterations to archive work and commit changes
7. Create PRs and merge through your standard Git workflow
8. Clean up merged branches with menu option 4

**Need Help?**

- GitHub Issues: https://github.com/h111359/requirements-driven-development/issues
- Documentation: Check `.rdd-docs/` in your project
- User Guide: Available at `.rdd/user-guide.md` after installation

---

*Happy developing with RDD! 🚀*
