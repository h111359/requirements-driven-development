# RDD Framework User Guide

**Requirements-Driven Development Framework**  
*Version 1.0 - A comprehensive guide to AI-assisted development with GitHub Copilot*

---

## 📖 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Understanding RDD Workflow](#understanding-rdd-workflow)
5. [Working with the Terminal Menu](#working-with-the-terminal-menu)
6. [Working with Copilot Prompts](#working-with-copilot-prompts)
7. [Complete Workflow Example](#complete-workflow-example)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The Requirements-Driven Development (RDD) framework is designed to enhance your development workflow with GitHub Copilot. It provides:

- **Structured Documentation**: Keep requirements, tech specs, and architecture docs synchronized with code
- **Guided Workflows**: Step-by-step process for requirement clarification, development, and documentation
- **AI-Optimized**: Specifically designed for GitHub Copilot interaction
- **Change Management**: Built-in version control and iteration tracking

### Key Concepts

- **Iteration**: A unit of work performed on a feature branch (create → develop → complete)
- **Workspace**: Your active working area (`.rdd-docs/workspace/`) containing prompts and implementation notes
- **Prompts**: Instructions for GitHub Copilot stored in `.rdd.copilot-prompts.md`
- **Documentation**: Core project docs (requirements, tech-spec, folder-structure, data-model)

---

## Prerequisites

Before using RDD, ensure you have:

### Required Software

1. **Python 3.7+** - Runtime for RDD scripts
   ```bash
   python --version  # Should show Python 3.7 or higher
   ```

2. **Git 2.23+** - Version control
   ```bash
   git --version
   ```

3. **VS Code** - Recommended editor (optional but enhances experience)
   - Download from: https://code.visualstudio.com/

4. **GitHub Copilot** - AI assistant (optional but recommended)
   - Requires active GitHub Copilot license
   - Install extension in VS Code

### Python Command Setup (Linux)

The RDD framework uses the `python` command (not `python3`). If not available:

```bash
# Debian/Ubuntu
sudo apt install python-is-python3

# Fedora/RHEL
sudo dnf install python-unversioned-command

# Or create an alias
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc
```

### Repository Setup

- Initialize a Git repository for your project
- Have a default branch (main/master/dev)
- Optionally connect to GitHub remote (or use local-only mode)

---

## Installation

### Step 1: Download Release

1. Visit [GitHub Releases](https://github.com/h111359/requirements-driven-development/releases)
2. Download the latest `rdd-v{version}.zip`
3. Extract the archive to a temporary folder

### Step 2: Run Installer

**For Linux/macOS:**
```bash
cd rdd-v{version}
chmod +x install.sh
./install.sh
```

**For Windows:**
```cmd
cd rdd-v{version}
install.bat
```

**Alternative (Direct Python):**
```bash
python install.py
```

### Step 3: Choose Installation Target

The installer will:
1. Prompt you to select the target project directory
2. Ask if you want to use GitHub remote or local-only mode
3. Prompt for the default branch name (main/dev/custom)
4. Copy framework files to your project
5. Merge VS Code settings
6. Update `.gitignore`

### Step 4: Verify Installation

```bash
cd /your/project
python .rdd/scripts/rdd.py --version
```

You should see: `RDD Framework v{version} (Python)`

---

## Understanding RDD Workflow

The RDD workflow follows a cyclical pattern:

```
┌─────────────────────────────────────────────────────────┐
│                    RDD ITERATION CYCLE                   │
└─────────────────────────────────────────────────────────┘

1. CREATE ITERATION
   ├─ On default branch
   ├─ Empty workspace
   └─ Create feature branch
         ↓
2. DEFINE WORK
   ├─ Edit .rdd.copilot-prompts.md
   └─ List specific prompts for Copilot
         ↓
3. EXECUTE PROMPTS
   ├─ Use /rdd.execute in Copilot chat
   ├─ Copilot performs work
   └─ Implementation files created
         ↓
4. UPDATE (if needed)
   ├─ Sync with default branch
   └─ Merge latest changes
         ↓
5. DOCUMENT CHANGES
   ├─ Use framework prompts in .rdd.copilot-prompts.md in Copilot chat
   └─ Update requirements, tech-spec, etc.
         ↓
6. COMPLETE ITERATION
   ├─ Archive workspace
   ├─ Commit all changes
   ├─ Push to remote
   └─ Return to default branch
         ↓
7. CREATE PULL REQUEST
   ├─ On GitHub (manual step)
   └─ Request review
         ↓
8. CLEANUP (after merge)
   └─ Delete merged branches
```

### Workflow States

- **On default branch + empty workspace** → Ready to create iteration
- **On feature branch + populated workspace** → Active development
- **On feature branch + completed work** → Ready to complete iteration
- **Back on default branch** → Ready for next iteration

---

## Working with the Terminal Menu

The RDD terminal menu provides a simplified interface for common operations.

### Starting the Menu

From your project root:

```bash
# Linux/macOS
./rdd.sh

# Windows
rdd.bat

# Or directly with Python
python .rdd/scripts/rdd.py
```

### Menu Options

```
╔══════════════════════════════════════════════════════════╗
║            RDD Framework - Main Menu                     ║
╚══════════════════════════════════════════════════════════╝

Current branch: feature-my-work
Default branch: main

  1. Create new iteration
  2. Update from default
  3. Complete current iteration
  4. Delete merged branches
  5. Exit
```

---

### 1. Create New Iteration

**When to use:** Starting new work on a feature or fix

**Prerequisites:**
- Must be on default branch
- Workspace must be empty

**What it does:**
1. Prompts for branch name (normalized to kebab-case)
2. Pulls latest from default branch (if using remote)
3. Creates and checks out new branch
4. Initializes workspace with `.rdd.copilot-prompts.md` template
5. Displays next steps

**Example:**
```
Enter branch name: Fix Bug in Login
  ↓
Normalized to: fix-bug-in-login
  ↓
Branch created: fix-bug-in-login
Workspace: .rdd-docs/workspace/.rdd.copilot-prompts.md
```

**Next Steps After Creation:**
1. Open `.rdd-docs/workspace/.rdd.copilot-prompts.md`
2. Define your prompts (see "Working with Copilot Prompts")
3. Use Copilot to execute prompts

---

### 2. Update from Default

**When to use:** Syncing your branch with latest changes from default branch

**Prerequisites:**
- Must be on a feature branch (not default)
- Other developers may have merged changes

**What it does:**
1. Stashes your uncommitted changes
2. Fetches and pulls latest default branch
3. Merges default branch into your current branch
4. Restores your stashed changes
5. Reports any conflicts

**Workflow:**
```
Your Branch: feature-a
   ↓
Update from default (main)
   ↓
Stash → Fetch → Merge → Restore
   ↓
Your Branch: feature-a (with latest main changes)
```

**Handling Conflicts:**
If merge conflicts occur:
1. Menu will show conflicted files
2. Resolve conflicts manually in your editor
3. Stage resolved files: `git add <file>`
4. Complete merge: `git commit`
5. Restore stash: `git stash pop`

---

### 3. Complete Current Iteration

**When to use:** Finishing work on your feature branch

**Prerequisites:**
- Must be on a feature branch (not default)
- Workspace must contain work (not empty)

**What it does:**
1. Archives entire workspace to `.rdd-docs/archive/<branch-name>/`
2. Commits all changes with message: "Completing work on <branch-name>"
3. Prompts to push to remote (if not local-only mode)
4. Clears workspace
5. Checks out default branch

**Archive Contents:**
- All workspace files preserved with timestamp
- `.archive-metadata` file with branch info, commit hash, author

**Next Steps After Completion:**
1. Create pull request on GitHub (if pushed)
2. Request code review
3. Merge after approval
4. Run "Delete merged branches" to clean up

---

### 4. Delete Merged Branches

**When to use:** Cleaning up after pull requests are merged

**Prerequisites:**
- Best used when on default branch
- Branches should be fully merged into default branch

**What it does:**
1. Lists all branches fully merged into default branch
2. Excludes protected branches (default, main, master, dev)
3. Allows selection of branches to delete
4. Deletes selected branches locally
5. Optionally deletes from remote (if not local-only)

**Interactive Selection:**
```
Merged branches:
  1. feature-old-work
  2. fix-bug-123
  3. enhancement-abc

Enter numbers to delete (comma-sep or 'all'): 1,2
  ↓
Deletes: feature-old-work, fix-bug-123

Also delete from remote? (y/n): y
  ↓
Remote branches deleted
```

**Protected Branches (Never Deleted):**
- Default branch (from config)
- `main`
- `master`
- `dev`

---

### 5. Exit

Closes the terminal menu. You can restart it anytime using `./rdd.sh` or `rdd.bat`.

---

## Working with Copilot Prompts

The heart of RDD development is the `.rdd.copilot-prompts.md` file in your workspace.

### Understanding the Prompts File

**Location:** `.rdd-docs/workspace/.rdd.copilot-prompts.md`

**Purpose:** Contains stand-alone prompts that GitHub Copilot will execute

**Structure:**
```markdown
## Stand Alone Prompts

 - [ ] [P01] Create login validation function
 - [ ] [P02] Add unit tests for user authentication
 - [ ] [P03] Update README with API documentation
 - [x] [P04] Fix bug in password reset (already completed)
```

### Prompt Format

Each prompt follows this format:

```markdown
 - [STATUS] [ID] Detailed instruction for Copilot
```

**Components:**
- **STATUS**: `[ ]` for unchecked (pending), `[x]` for checked (completed)
- **ID**: Unique identifier like `P01`, `P02`, etc.
- **Instruction**: Clear, detailed description of what Copilot should do

### Writing Effective Prompts

**Good Prompts:**
- ✅ Specific and actionable
- ✅ Include file paths and references
- ✅ Mention expected outcomes
- ✅ Reference relevant documentation

**Example Good Prompt:**
```markdown
 - [ ] [P01] Create a new file `src/utils/validator.py` with functions to 
   validate email and phone number formats. Include unit tests in 
   `tests/test_validator.py`. Follow the coding style in existing utils files.
```

**Bad Prompts:**
- ❌ Too vague: "Fix the login"
- ❌ Multiple tasks in one: "Create API and tests and docs"
- ❌ No context: "Add validation"

**Better Alternatives:**
- ✅ "Fix the login function in `src/auth.py` line 45 where empty passwords are accepted"
- ✅ "Create REST API endpoints in `src/api/`, then [P02] add tests, then [P03] update docs"
- ✅ "Add email validation to the User model in `src/models.py` using regex pattern"

---

### Executing Prompts in Copilot

1. **Open VS Code** with GitHub Copilot installed
2. **Open Copilot Chat** (Ctrl+Shift+I / Cmd+Shift+I)
3. **Switch to Agent Mode** (select a capable model like Claude Sonnet 4.5 or GPT-4)
4. **Execute the prompt:**

   ```
   /rdd.execute P01
   ```

   Replace `P01` with the prompt ID you want to execute.

5. **Copilot will:**
   - Read the prompt from `.rdd.copilot-prompts.md`
   - Read relevant context files (requirements, tech-spec, etc.)
   - Execute the instructions
   - Create an implementation file: `.rdd-docs/workspace/P01-implementation.md`
   - Mark the prompt as completed: `- [x] [P01] ...`

---

### Prompt Execution Workflow

```
1. You define prompts in .rdd.copilot-prompts.md:
   - [ ] [P01] Create feature X
   - [ ] [P02] Add tests for X
   - [ ] [P03] Update docs

2. Execute first prompt:
   You: /rdd.execute P01
   Copilot: [reads P01, creates feature X]
   Result: P01-implementation.md created, checkbox marked [x]

3. Execute next prompt:
   You: /rdd.execute P02
   Copilot: [reads P02, adds tests]
   Result: P02-implementation.md created, checkbox marked [x]

4. Continue until all prompts completed

5. Update documentation:
   You: /rdd.execute
   Copilot: [reads implementation files, updates docs]
   Result: requirements.md, tech-spec.md, etc. updated
```

---

### Implementation Files

For each executed prompt, Copilot creates:

**File:** `.rdd-docs/workspace/<PROMPT_ID>-implementation.md`

**Contents:**
- Prompt description
- Analysis performed
- Files created/modified
- Commands executed
- Implementation details
- Test results (if applicable)

**Example:** `P01-implementation.md`
```markdown
# P01 - Create Login Validation Implementation

## Prompt Description
Create login validation function with email and password checks.

## Analysis
Reviewed existing auth module structure...

## Implementation
Created files:
- src/auth/validator.py (validation logic)
- tests/test_validator.py (unit tests)

Commands executed:
- pytest tests/test_validator.py (all tests passed)

## Changes Made
- Added email validation using regex
- Added password strength checking
- 15 unit tests added (100% coverage)
```

---

### Automatic Prompt Marking

**You should NEVER manually edit checkboxes in `.rdd.copilot-prompts.md`!**

Copilot automatically marks prompts as completed by running:
```bash
python .rdd/scripts/rdd.py prompt mark-completed P01
```

This ensures proper tracking and prevents errors.

---

### Multiple Prompts and Order

You can:
- Execute prompts in any order (if independent)
- Execute multiple prompts in sequence
- Re-execute if needed (Copilot will detect previous work)

**Sequential Example:**
```markdown
 - [ ] [P01] Create database schema
 - [ ] [P02] Create ORM models (depends on P01)
 - [ ] [P03] Add API endpoints (depends on P02)
```

Execute in order: P01 → P02 → P03

**Parallel Example:**
```markdown
 - [ ] [P01] Update frontend styling
 - [ ] [P02] Add backend logging
 - [ ] [P03] Write deployment docs
```

Execute in any order (independent tasks)

---

## Complete Workflow Example

Let's walk through a complete iteration from start to finish.

### Scenario: Adding User Profile Feature

**Goal:** Add a user profile page with avatar upload

---

### Phase 1: Setup

**Initial State:**
- On default branch: `main`
- Workspace empty
- Requirements and tech-spec populated

**Documents to Review:**
```bash
# Check your project documentation
cat .rdd-docs/requirements.md
cat .rdd-docs/tech-spec.md
```

---

### Phase 2: Create Iteration

**Action:** Run RDD terminal menu
```bash
./rdd.sh
```

**Select:** Option 1 (Create new iteration)

**Input:**
```
Enter branch name: feature user profile page
  ↓
Normalized: feature-user-profile-page
  ↓
Confirm? y
```

**Result:**
- Branch created: `feature-user-profile-page`
- Workspace initialized
- File created: `.rdd-docs/workspace/.rdd.copilot-prompts.md`

---

### Phase 3: Define Work

**Edit:** `.rdd-docs/workspace/.rdd.copilot-prompts.md`

```markdown
## Stand Alone Prompts

 - [ ] [P01] Create UserProfile model in `src/models/profile.py` with fields: 
   user_id, display_name, bio, avatar_url, created_at, updated_at. Include 
   database migration script in `migrations/`.

 - [ ] [P02] Create API endpoints in `src/api/profile.py` for GET, PUT, DELETE 
   profile operations. Follow RESTful conventions used in other API files. 
   Include authentication middleware.

 - [ ] [P03] Add avatar upload functionality in `src/utils/upload.py` with 
   validation (max size 5MB, allowed formats: jpg, png, gif). Store files 
   in `uploads/avatars/` with UUID filenames.

 - [ ] [P04] Create frontend profile page in `frontend/src/pages/Profile.vue` 
   with form for editing display_name and bio, and avatar upload widget. 
   Use Vuex store for state management.

 - [ ] [P05] Add comprehensive unit tests for all new modules in `tests/` 
   directory. Aim for >80% code coverage. Include test fixtures.

 - [ ] [P06] Update API documentation in `docs/api.md` with new profile 
   endpoints, request/response examples, and error codes.
```

**Save the file**

---

### Phase 4: Execute Prompts

**Open VS Code Copilot Chat**

**Execute each prompt:**

```
You: /rdd.execute P01

Copilot: [Creates UserProfile model and migration]
Files created:
- src/models/profile.py
- migrations/20251109_add_profile.sql
- .rdd-docs/workspace/P01-implementation.md
Prompt marked completed ✓
```

```
You: /rdd.execute P02

Copilot: [Creates API endpoints]
Files created:
- src/api/profile.py
- .rdd-docs/workspace/P02-implementation.md
Prompt marked completed ✓
```

**Continue for P03, P04, P05, P06...**

**Check progress anytime:**
```
cat .rdd-docs/workspace/.rdd.copilot-prompts.md

 - [x] [P01] Create UserProfile model... (completed)
 - [x] [P02] Create API endpoints... (completed)
 - [x] [P03] Add avatar upload... (completed)
 - [ ] [P04] Create frontend profile page (pending)
 - [ ] [P05] Add unit tests (pending)
 - [ ] [P06] Update API docs (pending)
```

---

### Phase 5: Update from Default (Optional)

**Scenario:** Another developer merged changes to `main`

**Action:** Run RDD menu → Option 2 (Update from default)

**What happens:**
```
Stashing your changes...
Fetching origin/main...
Merging main into feature-user-profile-page...
Restoring stashed changes...

Update complete! ✓
```

**If conflicts:**
```
Merge conflicts detected!
Conflicts in:
  - src/models/profile.py

Resolve manually:
1. Edit conflicted files
2. git add <file>
3. git commit
4. git stash pop
```

---

### Phase 6: Document Changes

**All prompts completed?** Check:
```markdown
 - [x] [P01] Create UserProfile model...
 - [x] [P02] Create API endpoints...
 - [x] [P03] Add avatar upload...
 - [x] [P04] Create frontend profile page...
 - [x] [P05] Add unit tests...
 - [x] [P06] Update API docs...
```

**Execute documentation prompt:**

```
You: /rdd.execute F02

Copilot: [Analyzes all implementation files]
Reading:
- P01-implementation.md
- P02-implementation.md
- P03-implementation.md
- P04-implementation.md
- P05-implementation.md
- P06-implementation.md

Updating documentation:
- .rdd-docs/requirements.md (added FR-100, FR-101, FR-102)
- .rdd-docs/tech-spec.md (updated API section)
- .rdd-docs/folder-structure.md (added new directories)
- .rdd-docs/data-model.md (added UserProfile table)

Documentation updated ✓
```

---

### Phase 7: Complete Iteration

**Action:** Run RDD menu → Option 3 (Complete current iteration)

**What happens:**

```
1/4 Archiving workspace...
  Archived to: .rdd-docs/archive/feature-user-profile-page/
  ✓

2/4 Committing changes...
  Commit: "Completing work on feature-user-profile-page"
  ✓

3/4 Push to remote...
  Push branch? (y/n): y
  ✓ Branch pushed

4/4 Switching to main...
  ✓ Now on main

╔══════════════════════════════════════════════════╗
║            Iteration Complete!                   ║
╚══════════════════════════════════════════════════╝

Summary:
• Workspace archived
• Changes committed
• Now on branch: main

Next steps:
1. Create pull request on GitHub
2. Request code review
3. Merge after approval
```

---

### Phase 8: Create Pull Request (Manual)

**On GitHub:**
1. Navigate to your repository
2. Click "Compare & pull request" for `feature-user-profile-page`
3. Fill in PR description (use archived implementation docs as reference)
4. Request reviewers
5. Wait for approval

**PR Description Template:**
```markdown
## Feature: User Profile Page

### Changes
- Added UserProfile model and database migration
- Created profile API endpoints (GET, PUT, DELETE)
- Implemented avatar upload with validation
- Built frontend profile page with Vue
- Added comprehensive unit tests (85% coverage)
- Updated API documentation

### Implementation Details
See archived implementation files in:
.rdd-docs/archive/feature-user-profile-page/

### Testing
All tests passing:
- pytest tests/ (100+ tests)
- eslint frontend/src/ (no errors)

### Documentation
Updated:
- requirements.md (FR-100, FR-101, FR-102)
- tech-spec.md (API endpoints section)
- data-model.md (UserProfile table)
```

5. **Merge PR** (after approval)

---

### Phase 9: Cleanup

**After PR merged to main:**

**Action:** Run RDD menu → Option 4 (Delete merged branches)

**What happens:**
```
Merged branches:
  1. feature-user-profile-page
  2. fix-old-bug
  3. another-old-feature

Enter numbers to delete (comma-sep or 'all'): 1

About to delete:
  - feature-user-profile-page

Proceed? (y/n): y
✓ Deleted locally

Also delete from remote? (y/n): y
✓ Deleted from origin

Cleanup complete!
```

**Final State:**
- On default branch: `main`
- Workspace empty
- Feature merged and branch cleaned up
- Ready for next iteration

---

## Best Practices

### 1. Documentation First

**Always start with clear documentation:**
- Update `.rdd-docs/requirements.md` before coding
- Keep `.rdd-docs/tech-spec.md` technical and detailed
- Maintain `.rdd-docs/folder-structure.md` as project grows

### 2. Atomic Prompts

**Keep prompts focused and single-purpose:**

❌ **Bad:**
```markdown
 - [ ] [P01] Create user auth, add tests, update docs, fix bugs
```

✅ **Good:**
```markdown
 - [ ] [P01] Create user authentication module in src/auth/
 - [ ] [P02] Add unit tests for authentication in tests/test_auth.py
 - [ ] [P03] Update API documentation with auth endpoints
 - [ ] [P04] Fix authentication bug where tokens expire immediately
```

### 3. Frequent Updates

**Sync with default branch regularly:**
- Use "Update from default" option daily (if team is active)
- Merge early, merge often
- Resolve conflicts while they're small

### 4. Clear Branch Names

**Use descriptive, kebab-case names:**

✅ **Good:**
- `feature-user-profile-page`
- `fix-20251109-login-timeout`
- `enhancement-api-performance`

❌ **Avoid:**
- `work` (too vague)
- `My Branch` (spaces, not normalized)
- `temp123` (not descriptive)

### 5. Commit Messages

**Let RDD auto-generate commit messages:**
- "Completing work on feature-user-profile-page" (descriptive)
- Includes branch name for context

**For manual commits (before completion):**
```bash
git commit -m "Implement profile API endpoints (P02)"
git commit -m "Add avatar upload validation (P03)"
```

### 6. Test Before Completing

**Always verify your work before completing iteration:**
```bash
# Run tests
pytest tests/

# Run linters
pylint src/

# Check for issues
python .rdd/scripts/rdd.py git compare
```

### 7. Archive Usage

**Leverage archived implementation files:**
- Reference for future similar work
- PR description material
- Historical context for decisions
- Training material for new team members

**Location:** `.rdd-docs/archive/<branch-name>/`

### 8. Configuration Management

**Understand your RDD config:**

```bash
# View config
python .rdd/scripts/rdd.py config show

# Get default branch
python .rdd/scripts/rdd.py config get defaultBranch

# Change default branch
python .rdd/scripts/rdd.py config set defaultBranch dev
```

**Config location:** `.rdd-docs/config.json`

### 9. Local-Only Mode

**For projects without GitHub remote:**

During installation, choose "local-only mode"

**Effect:**
- Skips push to remote
- Skips fetch from remote
- All operations remain local

**Config:**
```json
{
  "localOnly": true
}
```

### 10. Workspace Hygiene

**Keep workspace clean:**
- Start iterations with empty workspace
- Complete iterations fully (don't leave partial work)
- Archive before starting new iteration

**Check workspace:**
```bash
ls -la .rdd-docs/workspace/
```

Should be empty when on default branch.

---

## Troubleshooting

### Common Issues

#### 1. "Cannot create iteration: not on default branch"

**Problem:** Trying to create iteration from feature branch

**Solution:**
```bash
# Complete current work first
./rdd.sh → Option 3 (Complete iteration)

# Or manually switch
git checkout main
```

---

#### 2. "Cannot create iteration: workspace not empty"

**Problem:** Workspace has leftover files from previous iteration

**Solution:**
```bash
# Option A: Complete the current iteration
./rdd.sh → Option 3 (Complete iteration)

# Option B: Clear workspace (WARNING: deletes files)
python .rdd/scripts/rdd.py workspace clear

# Option C: Archive without completing
python .rdd/scripts/rdd.py workspace archive --keep
```

---

#### 3. "Cannot complete iteration: on default branch"

**Problem:** Trying to complete work while on default branch

**Solution:**
```bash
# Create a branch first
./rdd.sh → Option 1 (Create new iteration)
```

---

#### 4. Merge Conflicts During Update

**Problem:** Conflicts when syncing with default branch

**Solution:**
```bash
# Conflicts are shown in menu output
# Manually resolve:

1. Edit conflicted files (VS Code shows conflict markers)
2. Choose which changes to keep
3. Remove conflict markers (<<<<<<, ======, >>>>>>)
4. Stage resolved files:
   git add <file>
5. Complete merge:
   git commit
6. Restore stashed changes:
   git stash pop
```

**Conflict Example:**
```python
<<<<<<< HEAD
# Your version
def login(username, password):
    return authenticate_v2(username, password)
=======
# Main branch version
def login(username, password):
    return authenticate_v3(username, password, token=True)
>>>>>>> main
```

**Resolved:**
```python
# Combined version (if both needed)
def login(username, password):
    return authenticate_v3(username, password, token=True)
```

---

#### 5. "Failed to push to remote"

**Problem:** Push fails during completion

**Possible causes:**
- No internet connection
- Remote branch already exists
- Authentication issues

**Solutions:**

**A. Network Issues:**
```bash
# Check connection
ping github.com

# Retry push manually
git push -u origin <branch-name>
```

**B. Authentication:**
```bash
# Re-authenticate with GitHub
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# For HTTPS (use token, not password)
git push

# For SSH
ssh-keygen -t ed25519 -C "your@email.com"
# Add key to GitHub: Settings → SSH Keys
```

**C. Use Local-Only Mode:**
```bash
# If not using GitHub remote
python .rdd/scripts/rdd.py config set localOnly true
```

---

#### 6. Prompt Not Found: "Prompt P01 not found"

**Problem:** Copilot can't find prompt in workspace file

**Solution:**
```bash
# Check file exists
ls -la .rdd-docs/workspace/.rdd.copilot-prompts.md

# Verify prompt format
cat .rdd-docs/workspace/.rdd.copilot-prompts.md

# Correct format:
 - [ ] [P01] Description here
 
# Not:
 - [] [P01] Description  (missing space in checkbox)
 - [ ] P01 Description  (missing brackets around ID)
```

---

#### 7. Python Command Not Found (Linux)

**Problem:** `python` command not available

**Solution:**
```bash
# Install python-is-python3
sudo apt install python-is-python3

# Or use python3 directly (temporary)
python3 .rdd/scripts/rdd.py

# Or create alias (add to ~/.bashrc)
alias python=python3
```

---

#### 8. Can't Delete Branch: "Branch not fully merged"

**Problem:** Trying to delete branch with unmerged commits

**Solution:**
```bash
# Option A: Force delete (if safe)
git branch -D <branch-name>

# Option B: Merge first
git checkout main
git merge <branch-name>

# Option C: Check if actually merged
git branch --merged main | grep <branch-name>
```

---

#### 9. Workspace Files Persist After Completion

**Problem:** Files remain in workspace after completing iteration

**Expected:** Workspace should be empty after completion

**Solution:**
```bash
# Check workspace
ls -la .rdd-docs/workspace/

# If files remain, clear manually
python .rdd/scripts/rdd.py workspace clear

# Verify empty
ls -la .rdd-docs/workspace/
# Should show: No such file or directory OR empty directory
```

---

#### 10. Git Status Shows Uncommitted Changes

**Problem:** Changes exist but iteration won't complete

**Solution:**
```bash
# View changes
git status

# Option A: Commit everything (RDD will auto-commit)
# Just run completion again

# Option B: Stash unwanted changes
git stash

# Option C: Discard unwanted changes (WARNING: irreversible)
git checkout -- <file>
```

---

### Getting Help

**Check Documentation:**
```bash
# Framework version
python .rdd/scripts/rdd.py --version

# Command help
python .rdd/scripts/rdd.py --help
python .rdd/scripts/rdd.py branch --help
python .rdd/scripts/rdd.py git --help
```

**Debug Mode:**
```bash
# Enable verbose output
export DEBUG=1
./rdd.sh

# Or
DEBUG=1 python .rdd/scripts/rdd.py
```

**Repository Issues:**
- GitHub: https://github.com/h111359/requirements-driven-development/issues
- Email: h111359@gmail.com

---

## Appendix: Command Reference

### Terminal Menu Commands

```bash
# Start menu (Linux/macOS)
./rdd.sh

# Start menu (Windows)
rdd.bat

# Start menu (direct Python)
python .rdd/scripts/rdd.py
```

### CLI Commands (Advanced)

```bash
# Branch operations
python .rdd/scripts/rdd.py branch create enh my-feature
python .rdd/scripts/rdd.py branch delete my-feature
python .rdd/scripts/rdd.py branch list

# Git operations
python .rdd/scripts/rdd.py git compare
python .rdd/scripts/rdd.py git modified-files
python .rdd/scripts/rdd.py git update-from-default-branch

# Workspace operations
python .rdd/scripts/rdd.py workspace init change
python .rdd/scripts/rdd.py workspace archive
python .rdd/scripts/rdd.py workspace clear

# Prompt operations
python .rdd/scripts/rdd.py prompt mark-completed P01
python .rdd/scripts/rdd.py prompt list --status=unchecked

# Config operations
python .rdd/scripts/rdd.py config show
python .rdd/scripts/rdd.py config get defaultBranch
python .rdd/scripts/rdd.py config set defaultBranch dev
```

### Copilot Prompts

```
/rdd.execute P01          # Execute specific prompt
/rdd.execute              # Execute next uncompleted prompt (auto-select)
/rdd.execute F02          # Update all documentation
```

---

## Summary

**RDD Framework provides:**
- ✅ Structured workflow for AI-assisted development
- ✅ Clear separation of work iterations
- ✅ Automatic documentation synchronization
- ✅ Change tracking and archiving
- ✅ Simplified terminal menu
- ✅ Integration with GitHub Copilot

**Key Takeaways:**
1. Always start on default branch with empty workspace
2. Define clear, atomic prompts for Copilot
3. Execute prompts one by one
4. Update documentation when done
5. Complete iteration to archive and commit
6. Create PR, merge, and clean up

**Questions?**
- Documentation: `.rdd-docs/` in your project
- Issues: https://github.com/h111359/requirements-driven-development/issues
- Email: h111359@gmail.com

---

*Happy developing with RDD! 🚀*
