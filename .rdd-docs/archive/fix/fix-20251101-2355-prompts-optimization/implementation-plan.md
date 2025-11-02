# Scripts Refactor Implementation Plan

## Overview

This document outlines the refactoring plan for the RDD framework scripts. The goal is to create a single wrapper script (`rdd.sh`) that orchestrates all functionality through a set of focused, non-redundant helper scripts.

## Current State Analysis

### Existing Scripts and Their Functionality

1. **archive.sh**
   - Archive workspace files to branch-specific folder
   - Create metadata for archived workspaces
   - Optional workspace cleanup
   - Auto-commit archive changes

2. **clarify-changes.sh**
   - Initialize workspace for clarification phase
   - Log clarification Q&A entries
   - Manage backup/restore of workspace
   - Validate requirements-changes.md format
   - Clear workspace for main branch

3. **create-change.sh**
   - Create new change with flat structure
   - Initialize workspace with templates
   - Create branch (feat/fix)
   - Initialize tracking files (.current-change, clarification-log.jsonl, etc.)

4. **delete-branch.sh**
   - Delete branch locally and remotely
   - Check for uncommitted changes
   - Verify branch is merged before deletion
   - Safety checks and confirmations

5. **delete-merged-branches.sh**
   - Batch delete merged branches
   - Clean up both local and remote branches
   - User confirmation before deletion

6. **fix-management.sh**
   - Initialize fix branches
   - Archive fix workspace
   - Create wrap-up commits
   - Create pull requests
   - Mark stand-alone prompts as completed
   - Log prompt execution details
   - Push and cleanup operations

7. **general.sh**
   - Get modified files compared to main
   - Get file-specific changes
   - Analyze requirements impact
   - Compare with main branch
   - Merge/preview requirements changes
   - ID auto-assignment for requirements

## Functional Grouping Analysis

### Core Functional Areas

1. **Branch Management**
   - Create branches (feat/fix)
   - Delete branches (single/multiple)
   - Check merge status
   - Switch branches

2. **Workspace Management**
   - Initialize workspace
   - Archive workspace
   - Backup/restore workspace
   - Clear workspace
   - Template management

3. **Requirements Management**
   - Validate requirements-changes.md
   - Merge requirements changes
   - Preview requirements merge
   - Auto-assign IDs
   - Track ID mappings

4. **Change/Fix Workflow**
   - Create change/fix
   - Initialize change tracking
   - Wrap-up workflow
   - Archive change workspace

5. **Git Operations**
   - Check uncommitted changes
   - Compare with main
   - Get modified files
   - Get file diffs
   - Push to remote
   - Auto-commit

6. **Clarification Management**
   - Initialize clarification phase
   - Log clarification entries
   - Manage open questions

7. **Prompt Management**
   - Mark prompts as completed
   - Log prompt execution
   - Track prompt sessions

8. **Pull Request Management**
   - Create PR
   - Request Copilot review
   - PR workflow automation

## Proposed Architecture

### Main Wrapper Script

**File:** `.rdd/scripts/rdd.sh`

**Purpose:** Single entry point for all RDD operations

**Structure:**
```bash
rdd.sh <domain> <action> [options]
```

**Domains:**
- `branch` - Branch management operations
- `workspace` - Workspace management operations  
- `requirements` - Requirements management operations
- `change` - Change workflow operations
- `fix` - Fix workflow operations
- `clarify` - Clarification management operations
- `prompt` - Prompt management operations
- `pr` - Pull request operations
- `git` - Git utility operations

### Utility Scripts Organization

#### 1. **branch-utils.sh**
**Responsibilities:**
- Create branches (feat/fix)
- Delete single branch (with checks)
- Delete multiple merged branches
- Check merge status
- List branches

**Functions:**
- `create_branch()`
- `delete_branch()`
- `delete_merged_branches()`
- `check_merge_status()`
- `list_branches()`

**Replaces functionality from:**
- `create-change.sh` (branch creation)
- `delete-branch.sh` (complete)
- `delete-merged-branches.sh` (complete)
- `fix-management.sh` (branch creation)

---

#### 2. **workspace-utils.sh**
**Responsibilities:**
- Initialize workspace with templates
- Archive workspace to branch-specific folder
- Backup/restore workspace
- Clear workspace
- Copy templates

**Functions:**
- `init_workspace()`
- `archive_workspace()`
- `backup_workspace()`
- `restore_workspace()`
- `clear_workspace()`
- `copy_template()`

**Replaces functionality from:**
- `archive.sh` (complete)
- `clarify-changes.sh` (backup/restore/clear)
- `create-change.sh` (workspace init)
- `fix-management.sh` (workspace archiving)

---

#### 3. **requirements-utils.sh**
**Responsibilities:**
- Validate requirements-changes.md format
- Merge requirements changes to requirements.md
- Preview merge operations
- Auto-assign requirement IDs
- Track ID mappings
- Analyze requirements impact

**Functions:**
- `validate_requirements()`
- `merge_requirements()`
- `preview_merge()`
- `get_next_id()`
- `track_id_mapping()`
- `analyze_requirements_impact()`

**Replaces functionality from:**
- `clarify-changes.sh` (validation)
- `general.sh` (merge/preview/ID management/analysis)

---

#### 4. **change-utils.sh**
**Responsibilities:**
- Create new change (feat/fix)
- Initialize change tracking files
- Wrap-up change workflow
- Create change config

**Functions:**
- `create_change()`
- `init_change_tracking()`
- `wrap_up_change()`
- `create_change_config()`

**Replaces functionality from:**
- `create-change.sh` (complete)
- `fix-management.sh` (wrap-up workflow)

---

#### 5. **clarify-utils.sh**
**Responsibilities:**
- Initialize clarification phase
- Log clarification Q&A entries
- Manage open questions
- Copy clarity taxonomy

**Functions:**
- `init_clarification()`
- `log_clarification()`
- `manage_open_questions()`
- `copy_taxonomy()`

**Replaces functionality from:**
- `clarify-changes.sh` (init/log/taxonomy)
- `create-change.sh` (clarification initialization)

---

#### 6. **prompt-utils.sh**
**Responsibilities:**
- Mark prompts as completed
- Log prompt execution details
- Track prompt sessions
- Validate prompt status

**Functions:**
- `mark_prompt_completed()`
- `log_prompt_execution()`
- `track_prompt_session()`
- `validate_prompt_status()`

**Replaces functionality from:**
- `fix-management.sh` (mark-prompt-completed/log-prompt-execution)

---

#### 7. **pr-utils.sh**
**Responsibilities:**
- Create pull requests
- Update pull requests
- Request reviews
- PR automation workflows

**Functions:**
- `create_pr()`
- `update_pr()`
- `request_review()`
- `pr_workflow()`

**Replaces functionality from:**
- `fix-management.sh` (PR creation)

---

#### 8. **git-utils.sh**
**Responsibilities:**
- Check git repository status
- Check uncommitted changes
- Compare with main branch
- Get modified files
- Get file diffs
- Fetch latest changes
- Push to remote
- Auto-commit changes

**Functions:**
- `check_git_repo()`
- `check_uncommitted_changes()`
- `compare_with_main()`
- `get_modified_files()`
- `get_file_diff()`
- `fetch_main()`
- `push_to_remote()`
- `auto_commit()`

**Replaces functionality from:**
- `archive.sh` (git checks/commits)
- `delete-branch.sh` (git checks)
- `general.sh` (comparison/file tracking)
- `fix-management.sh` (push operation)

---

#### 9. **core-utils.sh**
**Responsibilities:**
- Common utility functions
- Colored output functions
- Validation functions
- Error handling
- Configuration management

**Functions:**
- `print_success()`
- `print_error()`
- `print_warning()`
- `print_info()`
- `print_step()`
- `print_banner()`
- `validate_name()`
- `get_config()`
- `set_config()`

**Replaces functionality from:**
- All scripts (common utilities)

## Implementation Prompts

### Phase 1: Foundation and Utilities

#### [R001] Create core-utils.sh
**Objective:** Create the foundational utility script with common functions

**Tasks:**
1. Create `.rdd/scripts/core-utils.sh`
2. Implement colored output functions (print_success, print_error, print_warning, print_info, print_step, print_banner)
3. Implement validation functions (validate_name, validate_branch_name, validate_file_exists)
4. Implement configuration functions (get_config, set_config)
5. Add error handling utilities
6. Add help message generation functions
7. Make all functions exportable

**Acceptance Criteria:**
- All color output functions work correctly
- Validation functions return appropriate status codes
- Configuration functions can read/write settings
- Functions are properly documented with inline comments

---

#### [R002] Create git-utils.sh
**Objective:** Create git operations utility script

**Tasks:**
1. Create `.rdd/scripts/git-utils.sh`
2. Source core-utils.sh for common functions
3. Implement `check_git_repo()`
4. Implement `check_uncommitted_changes()`
5. Implement `get_default_branch()`
6. Implement `fetch_main()`
7. Implement `compare_with_main()`
8. Implement `get_modified_files()`
9. Implement `get_file_diff()`
10. Implement `push_to_remote()`
11. Implement `auto_commit()`
12. Add usage documentation

**Acceptance Criteria:**
- All git operations work correctly
- Error handling is robust
- Functions integrate with core-utils.sh
- Works with both main and master branches

**Dependencies:** [R001]

---

### Phase 2: Core Management Scripts

#### [R003] Create workspace-utils.sh
**Objective:** Create workspace management utility script

**Tasks:**
1. Create `.rdd/scripts/workspace-utils.sh`
2. Source core-utils.sh and git-utils.sh
3. Implement `init_workspace(type)` - type can be 'change' or 'fix'
4. Implement `archive_workspace(branch_name, keep_workspace)`
5. Implement `backup_workspace()`
6. Implement `restore_workspace()`
7. Implement `clear_workspace()`
8. Implement `copy_template(template_name, destination)`
9. Add metadata creation for archives
10. Add usage documentation

**Acceptance Criteria:**
- Workspace initialization works for both change and fix types
- Archive creates proper metadata
- Backup/restore preserves all workspace files
- Clear workspace has safety confirmations
- Template copying validates source files exist

**Dependencies:** [R001], [R002]

---

#### [R004] Create branch-utils.sh
**Objective:** Create branch management utility script

**Tasks:**
1. Create `.rdd/scripts/branch-utils.sh`
2. Source core-utils.sh and git-utils.sh
3. Implement `create_branch(branch_type, branch_name)` - supports feat/fix
4. Implement `delete_branch(branch_name, force, skip_checks)`
5. Implement `delete_merged_branches()`
6. Implement `check_merge_status(branch_name, base_branch)`
7. Implement `list_branches(filter)`
8. Add comprehensive safety checks for deletion
9. Add usage documentation

**Acceptance Criteria:**
- Branch creation validates naming conventions
- Branch deletion has proper safety checks
- Merge status check is accurate
- Batch deletion prompts for confirmation
- Handles both local and remote branches

**Dependencies:** [R001], [R002]

---

#### [R005] Create requirements-utils.sh
**Objective:** Create requirements management utility script

**Tasks:**
1. Create `.rdd/scripts/requirements-utils.sh`
2. Source core-utils.sh and git-utils.sh
3. Implement `validate_requirements(file_path)`
4. Implement `get_next_id(prefix, file_path)` - auto ID assignment
5. Implement `track_id_mapping(old_id, new_id, mapping_file)`
6. Implement `merge_requirements(dry_run, create_backup)`
7. Implement `preview_merge()`
8. Implement `analyze_requirements_impact()`
9. Handle ADDED/MODIFIED/DELETED requirement types
10. Add usage documentation

**Acceptance Criteria:**
- Validation detects format errors
- ID auto-assignment avoids conflicts
- Merge correctly processes all requirement types
- Preview shows accurate change summary
- ID mapping is logged for traceability

**Dependencies:** [R001], [R002]

---

### Phase 3: Workflow Scripts

#### [R006] Create clarify-utils.sh
**Objective:** Create clarification management utility script

**Tasks:**
1. Create `.rdd/scripts/clarify-utils.sh`
2. Source core-utils.sh and workspace-utils.sh
3. Implement `init_clarification()`
4. Implement `log_clarification(question, answer, answered_by, session_id)`
5. Implement `create_open_questions_template()`
6. Implement `copy_taxonomy()`
7. Create clarification-log.jsonl structure
8. Add usage documentation

**Acceptance Criteria:**
- Clarification phase initialization creates all required files
- Q&A logging creates valid JSONL entries
- Open questions template is created correctly
- Taxonomy copying validates source file

**Dependencies:** [R001], [R003]

---

#### [R007] Create prompt-utils.sh
**Objective:** Create prompt management utility script

**Tasks:**
1. Create `.rdd/scripts/prompt-utils.sh`
2. Source core-utils.sh
3. Implement `mark_prompt_completed(prompt_id, journal_file)`
4. Implement `log_prompt_execution(prompt_id, execution_details, session_id)`
5. Implement `list_prompts(status)` - filter by unchecked/checked/all
6. Implement `validate_prompt_status(prompt_id, journal_file)`
7. Handle JSONL logging format
8. Add usage documentation

**Acceptance Criteria:**
- Prompt marking changes only the checkbox
- Execution logging creates valid JSONL entries
- List prompts filters correctly
- Handles missing journal.md gracefully

**Dependencies:** [R001]

---

#### [R008] Create pr-utils.sh
**Objective:** Create pull request management utility script

**Tasks:**
1. Create `.rdd/scripts/pr-utils.sh`
2. Source core-utils.sh and git-utils.sh
3. Implement `create_pr(branch_name, title, body, draft)`
4. Implement `update_pr(pr_number, updates)`
5. Implement `request_review(pr_number, reviewers)`
6. Implement `pr_workflow(branch_name, archive_path)` - automated PR creation
7. Check for GitHub CLI availability
8. Add usage documentation

**Acceptance Criteria:**
- PR creation works with GitHub CLI
- Gracefully degrades if CLI not available
- Automated workflow creates descriptive PRs
- Review requests work correctly

**Dependencies:** [R001], [R002]

---

#### [R009] Create change-utils.sh
**Objective:** Create change workflow utility script

**Tasks:**
1. Create `.rdd/scripts/change-utils.sh`
2. Source core-utils.sh, git-utils.sh, branch-utils.sh, workspace-utils.sh, clarify-utils.sh
3. Implement `create_change(change_name, change_type)` - supports feat/fix
4. Implement `init_change_tracking(change_id, branch_name, change_type)`
5. Implement `create_change_config(config_data)`
6. Implement `wrap_up_change()` - complete workflow
7. Integrate branch creation, workspace init, clarification init
8. Add usage documentation

**Acceptance Criteria:**
- Change creation validates naming conventions
- All workspace files are initialized correctly
- .current-change config is created with proper JSON
- Wrap-up workflow archives and creates PR
- Works for both feat and fix types

**Dependencies:** [R001], [R002], [R003], [R004], [R006]

---

### Phase 4: Main Wrapper

#### [R010] Create rdd.sh wrapper script
**Objective:** Create the main wrapper script that orchestrates all functionality

**Tasks:**
1. Create `.rdd/scripts/rdd.sh`
2. Source all utility scripts (core-utils.sh, git-utils.sh, workspace-utils.sh, branch-utils.sh, requirements-utils.sh, clarify-utils.sh, prompt-utils.sh, pr-utils.sh, change-utils.sh)
3. Implement domain-based routing (branch, workspace, requirements, change, fix, clarify, prompt, pr, git)
4. Create comprehensive help system
5. Implement command parsing and validation
6. Add auto-completion support
7. Create usage examples
8. Add version information
9. Make script executable

**Command Structure:**
```bash
rdd.sh branch create <type> <name>
rdd.sh branch delete [name] [--force]
rdd.sh branch delete-merged
rdd.sh branch status <name>

rdd.sh workspace init <type>
rdd.sh workspace archive [--keep]
rdd.sh workspace backup
rdd.sh workspace restore
rdd.sh workspace clear

rdd.sh requirements validate
rdd.sh requirements merge [--dry-run] [--backup]
rdd.sh requirements preview
rdd.sh requirements analyze

rdd.sh change create <name> <type>
rdd.sh change wrap-up

rdd.sh fix init <name>
rdd.sh fix wrap-up

rdd.sh clarify init
rdd.sh clarify log "<question>" "<answer>" [answeredBy]

rdd.sh prompt mark-completed <id>
rdd.sh prompt log-execution <id> "<details>"
rdd.sh prompt list [--status=unchecked]

rdd.sh pr create [--draft]
rdd.sh pr request-review <reviewers>

rdd.sh git compare
rdd.sh git modified-files
rdd.sh git file-diff <file>
rdd.sh git push
```

**Acceptance Criteria:**
- All domain commands route correctly
- Help system is comprehensive and clear
- Error messages are informative
- Unknown commands show helpful suggestions
- Script is properly documented
- Works with all utility scripts

**Dependencies:** [R001] through [R009]

---

### Phase 5: Testing and Migration

#### [R011] Create integration tests
**Objective:** Ensure all scripts work together correctly

**Tasks:**
1. Create test script `.rdd/scripts/test-rdd.sh`
2. Test branch creation workflow
3. Test workspace management workflow
4. Test requirements merge workflow
5. Test change/fix creation workflow
6. Test prompt management workflow
7. Test git operations
8. Test error handling scenarios
9. Document test results

**Acceptance Criteria:**
- All workflows execute successfully
- Error cases are handled gracefully
- No regression in functionality
- Test coverage is comprehensive

**Dependencies:** [R010]

---

#### [R012] Create migration guide
**Objective:** Document migration from old scripts to new wrapper

**Tasks:**
1. Create `.rdd-docs/migration-guide.md`
2. Document command mapping (old script → new rdd.sh command)
3. Identify breaking changes
4. Create migration checklist
5. Add troubleshooting section
6. Document rollback procedure

**Command Mapping:**
```
OLD: ./create-change.sh my-feature feat
NEW: rdd.sh change create my-feature feat

OLD: ./archive.sh
NEW: rdd.sh workspace archive

OLD: ./delete-branch.sh my-branch
NEW: rdd.sh branch delete my-branch

OLD: ./.rdd/scripts/fix-management.sh init my-fix
NEW: rdd.sh fix init my-fix

OLD: ./.rdd/scripts/fix-management.sh mark-prompt-completed P001
NEW: rdd.sh prompt mark-completed P001

OLD: ./.rdd/scripts/clarify-changes.sh init
NEW: rdd.sh clarify init

OLD: ./.rdd/scripts/general.sh merge-requirements-changes
NEW: rdd.sh requirements merge
```

**Acceptance Criteria:**
- All old commands have documented equivalents
- Breaking changes are clearly identified
- Migration is achievable without data loss
- Rollback procedure is tested

**Dependencies:** [R010], [R011]

---

#### [R013] Deprecate old scripts
**Objective:** Phase out old scripts in favor of new wrapper

**Tasks:**
1. Add deprecation warnings to old scripts
2. Update all documentation to use rdd.sh
3. Update GitHub prompts to use rdd.sh
4. Create symbolic links for backward compatibility (optional)
5. Set timeline for final removal
6. Archive old scripts to `.rdd/scripts/archive/`

**Acceptance Criteria:**
- Deprecation warnings are clear and informative
- All documentation references new commands
- Backward compatibility maintained during transition period
- Old scripts archived for reference

**Dependencies:** [R012]

---



## Success Criteria

1. **Single Entry Point:** All RDD operations accessible through `rdd.sh`
2. **No Functionality Loss:** All features from old scripts are preserved
3. **No Redundancy:** Each function exists in exactly one utility script
4. **Clear Organization:** Utility scripts have focused, well-defined responsibilities
5. **Maintainability:** Code is DRY, well-documented, and follows consistent patterns
6. **User-Friendly:** Clear help messages, intuitive commands, good error messages
7. **Backward Compatible:** Migration path exists for existing users
8. **Tested:** All workflows have integration tests

## Benefits

1. **Single Command Interface:** Users only need to remember `rdd.sh`
2. **Consistent UX:** Uniform command structure across all domains
3. **Better Discoverability:** Help system shows all available commands
4. **Easier Maintenance:** Focused scripts are easier to understand and modify
5. **Reduced Duplication:** Common functions centralized in core-utils.sh
6. **Scalability:** Easy to add new domains and commands
7. **Testability:** Modular structure enables comprehensive testing

## Notes

- Each utility script should be independently testable
- All scripts should follow the same error handling conventions
- Configuration should be centralized where possible
- Documentation should be inline and comprehensive
- Consider adding shell completion for rdd.sh commands
- Use consistent naming conventions across all scripts
- Ensure all scripts handle both `main` and `master` branches gracefully
- The `-utils.sh` suffix clearly indicates these are utility/helper scripts for specific domains
