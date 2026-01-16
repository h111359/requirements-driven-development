# Implementation Log - P-002: Commit during archive

## Prompt Summary
When the workdir is archived, changes in the repo are generated and stay uncommitted. Add to the archive iteration functionality to make git commit (if git option is true) with the name of the iteration.

## Questionnaire Answers Applied

The implementation follows the user's questionnaire selections:

- **Q1 (Commit timing)**: Option B - Commit after archiving
  - Git commit happens after the zip file is created and verified, but before workdir cleanup

- **Q2 (Commit message format)**: Option C - Prefixed with context
  - Commit message format: `Archive iteration: <iteration-name>`
  - Example: `Archive iteration: Tests failures fixes`

- **Q3 (Error handling)**: Option A - Fail the entire archive operation
  - If git commit fails, the entire archive operation fails
  - This ensures consistency - archive and commit must both succeed

## Context Review

### Technical Design
- The technical design file is empty, so no specific architectural constraints apply.

### Requirements
Relevant requirements identified:
- **UR-0009**: Framework shall archive working directory content at iteration end
- **UR-0011**: System shall clear workdir folder after archiving
- **UR-0043**: Framework shall support optional git integration during prompt completion, controlled by global config flag
- **TR-0001**: Framework shall implement all automation functionality in Python
- **TR-0004**: Archived workdirs stored in `.rdd-instance/archive/`

The prompt and questionnaire answers take precedence over requirements where there are differences in implementation details.

### Files and Folders
- Archive directory: `.rdd-instance/archive/`
- Workdir: `.rdd-instance/workdir/`
- Config: `.rdd-instance/config/instance-config.json`

## Implementation Steps

### 1. Read Existing Implementation
Read `/home/hromar/Desktop/vscode/requirements-driven-development/.rdd/src/actions/workdir_archive.py` to understand the current workflow.

Current workflow has 4 phases:
1. Archive to directory and verify
2. Create zip archive and verify
3. Delete directory-based archive
4. Two-phase commit cleanup of workdir (rename, delete, recreate)

### 2. Identify Git Config Structure
Confirmed that `.rdd-instance/config/instance-config.json` contains:
```json
{
  "git-enabled": true
}
```

### 3. Code Changes Made

#### Added Import
```python
import subprocess
```

#### Updated Docstring
Added documentation about:
- Reading git-enabled flag from instance-config.json
- Performing git commit when enabled
- Updated phase sequence to include git commit as Phase 3.5

#### Added Helper Functions

**_read_iteration_name(registry_path: Path) -> str**
- Reads just the iteration name from work-iteration-registry.json
- Used for building the commit message
- Validates that iteration-name exists and is non-empty

**_read_git_enabled(config_path: Path) -> bool**
- Reads git-enabled flag from instance-config.json
- Returns False if config file doesn't exist or is malformed
- Gracefully handles JSON parsing errors

**_git_commit(repo_root: Path, message: str) -> None**
- Performs git operations: `git add -A` followed by `git commit -m <message>`
- Runs from repo root directory
- Captures output and error messages
- Raises Exception on failure with descriptive error message
- Handles two failure scenarios:
  - CalledProcessError: git command executed but failed
  - FileNotFoundError: git command not found in PATH

#### Modified main() Function

Added to beginning of main():
```python
config_path = repo_root / ".rdd-instance" / "config" / "instance-config.json"
```

Added reading of iteration name and git flag:
```python
iteration_name = _read_iteration_name(registry_path)
git_enabled = _read_git_enabled(config_path)
```

Added Phase 3.5 after zip creation and verification:
```python
# Phase 3.5: Git Commit (if enabled)
# After archive is created and verified, commit to git if configured
if git_enabled:
    commit_message = f"Archive iteration: {iteration_name}"
    _git_commit(repo_root, commit_message)
```

This phase is positioned:
- AFTER: Zip file creation and verification (Phase 2) and directory cleanup (Phase 3)
- BEFORE: Workdir cleanup begins (Phase 4)

This ensures:
1. Archive exists before committing (per questionnaire Q1-B)
2. Git commit captures the archive in repository history
3. If commit fails, the archive exists but workdir has not been cleaned yet, allowing manual recovery
4. Per Q3-A, git commit failure throws an exception that aborts the entire operation

## Error Handling

The implementation follows the user's choice (Q3-A) to fail the entire archive operation if git commit fails:

1. **No changes to commit**: Git will fail with "nothing to commit" - this fails the archive operation
2. **Git not configured**: Git will fail with author/email missing - this fails the archive operation  
3. **Git not installed**: FileNotFoundError is raised - this fails the archive operation
4. **Any other git error**: CalledProcessError is raised with git's error message - this fails the archive operation

In all failure cases:
- The zip archive has been successfully created at `.rdd-instance/archive/<iteration-id>_<iteration-name>.zip`
- The directory-based archive has been deleted
- The workdir still exists and has NOT been cleaned up
- User can manually investigate and either fix git issues and re-run, or manually clean up

## Testing Recommendations

To verify this implementation:

1. **Test with git-enabled=true and changes to commit**:
   ```bash
   # Make some changes in the repo
   # Archive the workdir
   python .rdd/src/actions/workdir_archive.py
   # Check git log for the commit
   git log -1
   ```

2. **Test with git-enabled=false**:
   - Set git-enabled to false in instance-config.json
   - Archive should succeed without attempting git commit
   - No new commit in git log

3. **Test with git commit failure**:
   - Set git-enabled to true
   - Temporarily break git config (e.g., unset user.name)
   - Archive should fail with clear error message
   - Workdir should still exist
   - Zip archive should exist

4. **Test with nothing to commit**:
   - Set git-enabled to true
   - Ensure repo has no uncommitted changes
   - Archive should fail with "nothing to commit" error

## Requirement Changes Needed

This implementation is new functionality not explicitly covered by existing requirements. The following requirement updates were made:

### New Requirements Created

**UR-0104** (User Requirement):
```
The framework shall perform a git commit operation during workdir archiving when git-enabled 
configuration flag is true, using a commit message in the format 'Archive iteration: <iteration-name>'.
```

**TR-0186** (Technical Requirement):
```
The workdir_archive.py script shall execute git commit after zip archive creation and verification 
but before workdir cleanup, and shall fail the entire archive operation if git commit fails when 
git-enabled is true.
```

These requirements document:
- The git commit feature during archiving (UR-0104)
- The specific implementation behavior including timing and error handling (TR-0186)
- The commit message format matching questionnaire answer Q2-C
- The failure behavior matching questionnaire answer Q3-A
- The timing matching questionnaire answer Q1-B (after archiving)

## Summary

Implementation completed successfully:
- ✅ Added git commit functionality to workdir_archive.py
- ✅ Reads git-enabled flag from instance-config.json
- ✅ Commits after zip creation and verification, before workdir cleanup
- ✅ Uses commit message format: "Archive iteration: <iteration-name>"
- ✅ Fails entire operation if git commit fails
- ✅ Created implementation.md documentation
- ✅ Added requirements UR-0104 and TR-0186

