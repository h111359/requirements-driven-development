# RDD Framework Scripts Catalogue

This document provides a mapping between the interactive menu options in `.rdd/scripts/rdd.py` and their equivalent command-line invocations, along with a description of their meaning and impact.

## Simplified Interactive Menu (v1.0.3+)

The RDD framework now features a simplified 4-option menu focused on the core workflow:

| Menu Option                     | Description                                                                                           | Internal Function(s)                                    |
|---------------------------------|-------------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| **1. Complete current iteration** | Archives workspace, commits changes, optionally pushes to remote, returns to default branch         | `complete_iteration()`, `archive_workspace()`, `auto_commit()`, `push_to_remote()` |
| **2. Create new iteration**       | Creates new branch from default, initializes workspace with copilot-prompts.md                       | `create_iteration()`, git branch creation, template copy |
| **3. Delete merged branches**     | Lists merged branches interactively, deletes selected branches locally and optionally remotely       | `cleanup_after_merge()`, `interactive_branch_cleanup()` |
| **4. Update from default**        | Fetches/pulls default branch, merges into current branch                                             | `update_from_default_branch()`, `pull_default_branch()`, `merge_default_branch_into_current()` |
| **5. Exit**                       | Exits the interactive menu                                                                           | N/A                                                     |

### Workflow Details

#### 1. Complete Current Iteration

**Safety Checks:**
- Verifies NOT on default branch (stops if on default)
- Verifies workspace is NOT empty (stops if empty)

**Process:**
1. Archives all workspace files to `.rdd-docs/archive/<branch-name>/`
2. Commits changes with message "Completing work on <branch-name>"
3. Asks user if they want to push to remote (if not local-only mode)
4. Pushes branch if requested
5. Reminds user to create pull request
6. Checkouts to default branch

#### 2. Create New Iteration

**Safety Checks:**
- Verifies ON default branch (stops if not)
- Verifies workspace IS empty (stops if not empty)

**Process:**
1. Prompts for branch name (with normalization and validation)
2. Pulls latest from default branch (if not local-only mode)
3. Creates and checks out new branch
4. Copies `.rdd/templates/copilot-prompts.md` to `.rdd-docs/workspace/.rdd.copilot-prompts.md`
5. Shows summary with next steps

**Note:** No fix/enhancement type selection - all branches are treated uniformly.

#### 3. Delete Merged Branches

**Process:**
1. Fetches from remote (if not local-only mode)
2. Lists all branches fully merged into default branch
3. Allows user to select branches to delete (by number or "all")
4. Deletes selected branches locally
5. Optionally deletes from remote (if not local-only mode)

**Protected Branches:**
- Default branch (from config)
- "main"
- "master"
- "dev"

#### 4. Update from Default

**Safety Check:**
- Stops if already on default branch

**Process:**
1. Stashes any uncommitted changes
2. Fetches and pulls latest from default branch
3. Merges default branch into current branch
4. Restores stashed changes
5. Shows summary

## Command-Line Interface (CLI Mode)

For advanced users, all operations are still available via CLI commands:

### Core Workflow Commands (No Direct CLI Equivalent)

The simplified menu options 1 and 2 are designed for interactive use. However, legacy commands still exist:

| Legacy CLI Command              | Description                                              | Notes                                    |
|---------------------------------|----------------------------------------------------------|------------------------------------------|
| `rdd.py change create`          | Legacy: Creates change with type selection               | Still works but more complex than menu   |
| `rdd.py change wrap-up`         | Legacy: Wraps up change workflow                         | Similar to "Complete iteration" but different flow |

### Available CLI Domains

| Domain      | Actions                              | Description                                                           |
|-------------|--------------------------------------|-----------------------------------------------------------------------|
| **branch**  | create, delete, list, cleanup        | Branch management operations (advanced)                               |
| **workspace** | init, archive, clear               | Workspace management (advanced)                                       |
| **change**  | create, wrap-up                      | Legacy change workflow (kept for compatibility)                       |
| **git**     | compare, modified-files, push, update-from-default-branch | Git operations                  |
| **prompt**  | mark-completed, list                 | Stand-alone prompt management                                         |
| **config**  | show, get, set                       | Configuration management                                              |

### CLI Examples

```bash
# Git operations
python .rdd/scripts/rdd.py git compare
python .rdd/scripts/rdd.py git modified-files
python .rdd/scripts/rdd.py git push
python .rdd/scripts/rdd.py git update-from-default-branch

# Branch operations (advanced)
python .rdd/scripts/rdd.py branch delete my-old-branch
python .rdd/scripts/rdd.py branch list
python .rdd/scripts/rdd.py branch cleanup

# Prompt management
python .rdd/scripts/rdd.py prompt mark-completed P01
python .rdd/scripts/rdd.py prompt list

# Configuration
python .rdd/scripts/rdd.py config show
python .rdd/scripts/rdd.py config get defaultBranch
python .rdd/scripts/rdd.py config set defaultBranch dev

# Help
python .rdd/scripts/rdd.py --help
python .rdd/scripts/rdd.py <domain> --help
```

## Recommendation

**Use the interactive menu for daily workflow!** Simply run:

```bash
python .rdd/scripts/rdd.py
```

The CLI commands are available for scripting and advanced use cases, but the interactive menu provides the simplest and most user-friendly experience.

```
