# Plan for P-011: Remove git_commit.py

## Context

The script `.rdd/src/actions/git_commit.py` was originally created to handle git commits for active prompts. During P-010, its functionality was integrated directly into `.rdd/src/actions/prompt_complete.py` to avoid state management issues. This created code duplication. Based on the questionnaire answers:
- Remove git_commit.py completely (Q1: A)
- Remove the entire git domain from CLI (Q2: A)
- Mark related requirements as [DELETED] (Q3: A)
- Remove Git section from web UI entirely (Q4: C)

## Steps

### Step 1: Verify Current State

Read and analyze the following files to confirm the current implementation:
- `.rdd/src/actions/git_commit.py` - the standalone script
- `.rdd/src/actions/prompt_complete.py` - contains inline git commit logic
- `.rdd/src/rdd.py` - CLI routing with git domain
- `.rdd/src/web/static/app.js` - Web UI git functionality
- `.rdd/src/web/templates/index.html` - Web UI git section

Confirm that:
- `prompt_complete.py` contains complete git commit functionality inline
- `git_commit.py` is not used by any other scripts
- CLI routes `git commit` to `git_commit.py`
- Web UI has a Git section that calls the git commit action

### Step 2: Remove git_commit.py Script

Delete the file `.rdd/src/actions/git_commit.py` since its functionality is now completely integrated into `prompt_complete.py`.

### Step 3: Remove Git Domain from CLI

Update `.rdd/src/rdd.py` to remove all git domain references:
- Remove git domain from help text (line 11)
- Remove git example from help text (line 23)
- Remove `_git_domain_menu()` function (around line 366-381)
- Remove git domain from main menu options (line 393)
- Remove git domain handling from main menu (lines 405-406)
- Remove git domain handling from direct domain routing (lines 442-443)
- Update domain validation error messages to only mention 'prompt' and 'workdir' (lines 446, 456)

### Step 4: Remove Git Section from Web UI

#### Step 4.1: Update index.html

Remove the Git section from `.rdd/src/web/templates/index.html`:
- Locate and remove the entire Git section div (search for "Git" heading and nav link)
- This includes the navigation link and the content section

#### Step 4.2: Update app.js

Remove git-related functions from `.rdd/src/web/static/app.js`:
- Remove `gitCommit()` function (around lines 552-562)
- Remove `loadGitStatus()` function (starts around line 567)
- Remove any other git-related code

### Step 5: Update Requirements File

Update `.rdd-instance/specifications/requirements.md` to mark obsolete requirements as [DELETED]:

#### Step 5.1: Mark User Requirements as Deleted
- [UR-20251229-1841] - Mark as [DELETED] (git commit command requirement)
- [UR-20251229-1842] - Mark as [DELETED] (commit message format requirement)
- [UR-20251229-1843] - Mark as [DELETED] (auto-stage changes requirement)
- [UR-20251229-1844] - Mark as [DELETED] (validate changes before commit requirement)

#### Step 5.2: Mark Technical Requirements as Deleted
- [TR-20251229-1841] - Mark as [DELETED] (CLI git domain extension)
- [TR-20251229-1842] - Mark as [DELETED] (git_commit.py script requirement)
- [TR-20251229-1843] - Mark as [DELETED] (git commit error messages requirement)
- [TR-20251229-1844] - Mark as [DELETED] (CLI main menu git domain inclusion)
- [TR-20251230-1436] - Mark as [DELETED] (Web UI Git section requirement)

Note: Requirements related to prompt_complete.py git integration ([UR-20251231-0101], [UR-20251231-0103], [TR-20251231-0100], [TR-20251231-0103], [TR-20251231-0104]) remain unchanged as they describe the current implementation.

### Step 6: Verify Changes

After all deletions and updates:
- Verify no remaining references to git_commit.py exist in the codebase
- Verify CLI help text is correct and shows only 'prompt' and 'workdir' domains
- Verify Web UI no longer displays Git section
- Verify requirements file properly marks deleted requirements
- Test that prompt completion with git-enabled=true still works correctly via prompt_complete.py

## Requirements Changes

### Requirements to Mark as [DELETED]

The following requirements will be marked as [DELETED] with the format `- [ID] [DELETED]`:

**User Requirements:**
- [UR-20251229-1841] - git commit command
- [UR-20251229-1842] - commit message format
- [UR-20251229-1843] - auto-stage changes
- [UR-20251229-1844] - validate changes before commit

**Technical Requirements:**
- [TR-20251229-1841] - CLI git domain
- [TR-20251229-1842] - git_commit.py script
- [TR-20251229-1843] - git commit error messages
- [TR-20251229-1844] - CLI git domain menu option
- [TR-20251230-1436] - Web UI Git section

### No New Requirements

No new requirements will be added as this is a cleanup/removal task.

## Expected Outcome

After completing this plan:
- `git_commit.py` file will be deleted
- CLI will no longer have a git domain
- Web UI will no longer have a Git section
- Git commit functionality remains available only through prompt completion (via `prompt_complete.py`)
- Requirements document will accurately reflect that standalone git commit functionality is removed
- Code duplication will be eliminated
- The framework will have a single, consistent way to commit changes: through prompt completion
