# RDD Scripts Migration Guide

**Version:** 1.0.0  
**Date:** November 2, 2025  
**Migration Target:** From individual scripts to unified `rdd.sh` wrapper

---

## Table of Contents

1. [Overview](#overview)
2. [Why Migrate?](#why-migrate)
3. [Command Mapping](#command-mapping)
4. [Breaking Changes](#breaking-changes)
5. [Migration Checklist](#migration-checklist)
6. [Step-by-Step Migration](#step-by-step-migration)
7. [Side-by-Side Examples](#side-by-side-examples)
8. [Troubleshooting](#troubleshooting)
9. [Rollback Procedure](#rollback-procedure)
10. [Timeline](#timeline)

---

## Overview

The RDD framework is migrating from multiple individual scripts to a unified wrapper script (`rdd.sh`). This migration:

- **Consolidates** 7 top-level scripts into one entry point
- **Organizes** functionality into 9 focused utility scripts
- **Maintains** all existing functionality without data loss
- **Improves** user experience with consistent command structure

### What's Changing

**OLD STRUCTURE:**
```
.rdd/scripts/
├── archive.sh
├── clarify-changes.sh
├── create-change.sh
├── delete-branch.sh
├── delete-merged-branches.sh
├── fix-management.sh
└── general.sh
```

**NEW STRUCTURE:**
```
.rdd/scripts/
├── rdd.sh                 # Main wrapper (ONLY script you need to call)
├── core-utils.sh          # Core utilities
├── git-utils.sh           # Git operations
├── workspace-utils.sh     # Workspace management
├── branch-utils.sh        # Branch management
├── requirements-utils.sh  # Requirements operations
├── clarify-utils.sh       # Clarification phase
├── prompt-utils.sh        # Prompt management
├── pr-utils.sh            # Pull request operations
└── change-utils.sh        # Change workflow
```

---

## Why Migrate?

### Benefits

1. **Single Command Interface**
   - Remember one command: `rdd.sh`
   - Consistent syntax: `rdd.sh <domain> <action> [options]`

2. **Better Discoverability**
   - Built-in help system: `rdd.sh --help`
   - Domain-specific help: `rdd.sh branch --help`

3. **Improved Organization**
   - Related functions grouped by domain
   - No code duplication
   - Easier to maintain and extend

4. **Enhanced Error Messages**
   - Helpful suggestions for typos
   - Clear validation messages
   - Better error context

5. **Consistent User Experience**
   - Uniform command structure
   - Predictable behavior
   - Standard option handling

---

## Command Mapping

### Complete OLD → NEW Command Reference

#### Branch Management

| Old Command | New Command | Notes |
|------------|-------------|-------|
| `./create-change.sh my-feature feat` | `rdd.sh change create my-feature feat` | Creates branch + workspace |
| `./delete-branch.sh my-branch` | `rdd.sh branch delete my-branch` | Single branch deletion |
| `./delete-branch.sh --force` | `rdd.sh branch delete --force` | Force delete current branch |
| `./delete-merged-branches.sh` | `rdd.sh branch delete-merged` | Batch delete merged branches |
| N/A | `rdd.sh branch status <name>` | NEW: Check merge status |
| N/A | `rdd.sh branch list [filter]` | NEW: List branches |

#### Workspace Management

| Old Command | New Command | Notes |
|------------|-------------|-------|
| `./archive.sh` | `rdd.sh workspace archive` | Archive workspace |
| `./archive.sh --keep` | `rdd.sh workspace archive --keep` | Archive and keep workspace |
| N/A | `rdd.sh workspace init <type>` | NEW: Initialize workspace |
| N/A | `rdd.sh workspace backup` | NEW: Backup workspace |
| N/A | `rdd.sh workspace restore` | NEW: Restore from backup |
| N/A | `rdd.sh workspace clear` | NEW: Clear workspace |

#### Change/Fix Workflow

| Old Command | New Command | Notes |
|------------|-------------|-------|
| `./create-change.sh my-feature feat` | `rdd.sh change create my-feature feat` | Create feature change |
| `./create-change.sh my-fix fix` | `rdd.sh change create my-fix fix` | Create fix change |
| `./.rdd/scripts/fix-management.sh init my-fix` | `rdd.sh fix init my-fix` | Initialize fix (alias) |
| `./.rdd/scripts/fix-management.sh wrap-up` | `rdd.sh change wrap-up` | Complete change |
| `./.rdd/scripts/fix-management.sh wrap-up` | `rdd.sh fix wrap-up` | Complete fix (alias) |

#### Requirements Management

| Old Command | New Command | Notes |
|------------|-------------|-------|
| `./.rdd/scripts/clarify-changes.sh validate` | `rdd.sh requirements validate` | Validate format |
| `./.rdd/scripts/general.sh merge-requirements-changes` | `rdd.sh requirements merge` | Merge requirements |
| `./.rdd/scripts/general.sh preview-requirements-merge` | `rdd.sh requirements preview` | Preview merge |
| `./.rdd/scripts/general.sh requirements-impact` | `rdd.sh requirements analyze` | Analyze impact |
| N/A | `rdd.sh requirements merge --dry-run` | NEW: Dry run merge |

#### Clarification Phase

| Old Command | New Command | Notes |
|------------|-------------|-------|
| `./.rdd/scripts/clarify-changes.sh init` | `rdd.sh clarify init` | Initialize clarification |
| `./.rdd/scripts/clarify-changes.sh log "Q" "A"` | `rdd.sh clarify log "Q" "A"` | Log Q&A |
| `./.rdd/scripts/clarify-changes.sh log "Q" "A" "User"` | `rdd.sh clarify log "Q" "A" "User"` | Log with answeredBy |
| N/A | `rdd.sh clarify show [session]` | NEW: Show clarifications |
| N/A | `rdd.sh clarify count` | NEW: Count clarifications |

#### Prompt Management

| Old Command | New Command | Notes |
|------------|-------------|-------|
| `./.rdd/scripts/fix-management.sh mark-prompt-completed P01` | `rdd.sh prompt mark-completed P01` | Mark prompt done |
| `./.rdd/scripts/fix-management.sh log-prompt-execution P01 "Details"` | `rdd.sh prompt log-execution P01 "Details"` | Log execution |
| N/A | `rdd.sh prompt list` | NEW: List all prompts |
| N/A | `rdd.sh prompt list --status=unchecked` | NEW: List unchecked |

#### Pull Request Operations

| Old Command | New Command | Notes |
|------------|-------------|-------|
| `./.rdd/scripts/fix-management.sh create-pr` | `rdd.sh pr create` | Create PR |
| `./.rdd/scripts/fix-management.sh create-pr --draft` | `rdd.sh pr create --draft` | Create draft PR |
| N/A | `rdd.sh pr workflow` | NEW: Automated PR workflow |
| N/A | `rdd.sh pr request-review <reviewers>` | NEW: Request reviews |

#### Git Operations

| Old Command | New Command | Notes |
|------------|-------------|-------|
| `./.rdd/scripts/general.sh compare` | `rdd.sh git compare` | Compare with main |
| `./.rdd/scripts/general.sh modified-files` | `rdd.sh git modified-files` | List modified files |
| `./.rdd/scripts/general.sh file-diff <file>` | `rdd.sh git file-diff <file>` | Show file diff |
| `./.rdd/scripts/fix-management.sh push` | `rdd.sh git push` | Push to remote |

---

## Breaking Changes

### 1. Command Structure Change

**OLD:**
```bash
./create-change.sh <name> <type>
./.rdd/scripts/fix-management.sh <action>
```

**NEW:**
```bash
rdd.sh <domain> <action> [options]
```

**Impact:** All scripts now called through `rdd.sh`  
**Migration:** Use command mapping table above

### 2. Script Location

**OLD:** Scripts in multiple locations (root + `.rdd/scripts/`)  
**NEW:** All scripts in `.rdd/scripts/`, only `rdd.sh` is called

**Impact:** Direct script paths need updating  
**Migration:** Replace script paths with `rdd.sh` commands

### 3. Option Syntax Standardization

**OLD:** Inconsistent option handling  
**NEW:** Standardized options (e.g., `--keep`, `--force`, `--dry-run`)

**Impact:** Some option names may differ  
**Migration:** Check help for each command: `rdd.sh <domain> --help`

### 4. Error Message Format

**OLD:** Varied error message formats  
**NEW:** Consistent colored output with symbols (✓, ✗, ⚠, ℹ)

**Impact:** Scripts parsing output may need updates  
**Migration:** Update any output parsing logic

### 5. Return Codes

**OLD:** Inconsistent return codes  
**NEW:** Standardized return codes (0=success, 1=error, 2+=specific errors)

**Impact:** Scripts checking exit codes may need updates  
**Migration:** Review error handling in calling scripts

---

## Migration Checklist

### Phase 1: Preparation (Week 1)

- [ ] **Read this migration guide completely**
- [ ] **Review command mapping table**
- [ ] **Identify all scripts/automation using old commands**

---

## Step-by-Step Migration

### Step 1: Verify Installation

Check that `rdd.sh` exists and is executable:

```bash
ls -la .rdd/scripts/rdd.sh
# Should show: -rwxr-xr-x ... rdd.sh
```

Test basic functionality:

```bash
./.rdd/scripts/rdd.sh --version
# Should output: RDD Framework v1.0.0

./.rdd/scripts/rdd.sh --help
# Should show main help
```

### Step 2: Create Alias (Optional)

Add to your `.bashrc` or `.zshrc`:

```bash
alias rdd='cd /path/to/your/repo && ./.rdd/scripts/rdd.sh'
```

Then use simply:

```bash
rdd branch list
rdd change create my-feature feat
```

### Step 3: Update Individual Commands

Replace old commands one by one using the mapping table.

**Example - Updating a Shell Script:**

**BEFORE:**
```bash
#!/bin/bash
# Old create-feature script
./create-change.sh my-new-feature feat
./.rdd/scripts/clarify-changes.sh init
./.rdd/scripts/fix-management.sh mark-prompt-completed P01
```

**AFTER:**
```bash
#!/bin/bash
# Updated create-feature script
./.rdd/scripts/rdd.sh change create my-new-feature feat
./.rdd/scripts/rdd.sh clarify init
./.rdd/scripts/rdd.sh prompt mark-completed P01
```

### Step 4: Update GitHub Actions

**BEFORE:**
```yaml
- name: Create change
  run: ./create-change.sh feature-name feat

- name: Archive workspace
  run: ./archive.sh
```

**AFTER:**
```yaml
- name: Create change
  run: ./.rdd/scripts/rdd.sh change create feature-name feat

- name: Archive workspace
  run: ./.rdd/scripts/rdd.sh workspace archive
```

### Step 5: Update Documentation

Search and replace in all documentation:

```bash
# Find all references to old scripts
grep -r "create-change.sh" docs/
grep -r "fix-management.sh" docs/

# Update to rdd.sh commands
```

---

## Side-by-Side Examples

### Example 1: Creating a New Feature

**OLD WORKFLOW:**
```bash
# Step 1: Create change
./create-change.sh my-feature feat

# Step 2: Initialize clarification
./.rdd/scripts/clarify-changes.sh init

# Step 3: Log clarification
./.rdd/scripts/clarify-changes.sh log "What is X?" "X is Y"

# Step 4: Validate requirements
./.rdd/scripts/clarify-changes.sh validate

# Step 5: Complete and create PR
./.rdd/scripts/fix-management.sh wrap-up
```

**NEW WORKFLOW:**
```bash
# Step 1: Create change
./.rdd/scripts/rdd.sh change create my-feature feat

# Step 2: Initialize clarification
./.rdd/scripts/rdd.sh clarify init

# Step 3: Log clarification
./.rdd/scripts/rdd.sh clarify log "What is X?" "X is Y"

# Step 4: Validate requirements
./.rdd/scripts/rdd.sh requirements validate

# Step 5: Complete and create PR
./.rdd/scripts/rdd.sh change wrap-up
```

### Example 2: Branch Management

**OLD WORKFLOW:**
```bash
# Delete a branch
./delete-branch.sh old-feature

# Delete all merged branches
./delete-merged-branches.sh
```

**NEW WORKFLOW:**
```bash
# Delete a branch
./.rdd/scripts/rdd.sh branch delete old-feature

# Delete all merged branches
./.rdd/scripts/rdd.sh branch delete-merged

# NEW: Check merge status
./.rdd/scripts/rdd.sh branch status my-branch

# NEW: List all branches
./.rdd/scripts/rdd.sh branch list
```

### Example 3: Requirements Management

**OLD WORKFLOW:**
```bash
# Compare with main
./.rdd/scripts/general.sh compare

# Preview requirements merge
./.rdd/scripts/general.sh preview-requirements-merge

# Merge requirements
./.rdd/scripts/general.sh merge-requirements-changes
```

**NEW WORKFLOW:**
```bash
# Compare with main
./.rdd/scripts/rdd.sh git compare

# Preview requirements merge
./.rdd/scripts/rdd.sh requirements preview

# Dry-run merge (NEW!)
./.rdd/scripts/rdd.sh requirements merge --dry-run

# Actual merge
./.rdd/scripts/rdd.sh requirements merge
```

### Example 4: Prompt Management

**OLD WORKFLOW:**
```bash
# Mark prompt as completed
./.rdd/scripts/fix-management.sh mark-prompt-completed P01

# Log execution
./.rdd/scripts/fix-management.sh log-prompt-execution P01 "Implemented feature X"
```

**NEW WORKFLOW:**
```bash
# Mark prompt as completed
./.rdd/scripts/rdd.sh prompt mark-completed P01

# Log execution
./.rdd/scripts/rdd.sh prompt log-execution P01 "Implemented feature X"

# NEW: List unchecked prompts
./.rdd/scripts/rdd.sh prompt list --status=unchecked
```

---

## Troubleshooting

### Issue 1: Command Not Found

**Symptom:**
```
bash: rdd.sh: command not found
```

**Solution:**
```bash
# Check if file exists
ls -la .rdd/scripts/rdd.sh

# Make executable if needed
chmod +x .rdd/scripts/rdd.sh

# Use absolute path
./.rdd/scripts/rdd.sh --help
```

### Issue 2: Old Scripts Still Being Called

**Symptom:**
```
Using old script behavior
```

**Solution:**
```bash
# Check which script is being executed
which create-change.sh

# Update your scripts to use rdd.sh
# Search for old script calls
grep -r "create-change.sh" .
grep -r "fix-management.sh" .
```

### Issue 3: Function Not Found Errors

**Symptom:**
```
bash: create_branch: command not found
```

**Cause:** Trying to call utility functions directly instead of through `rdd.sh`

**Solution:**
Always use `rdd.sh` as entry point:
```bash
# Wrong:
create_branch feat my-feature

# Correct:
./.rdd/scripts/rdd.sh branch create feat my-feature
```

### Issue 4: Unknown Domain/Action

**Symptom:**
```
✗ Unknown domain: branches
```

**Solution:**
Check the help system for correct domain names:
```bash
# Main help shows all domains
./.rdd/scripts/rdd.sh --help

# Domain-specific help
./.rdd/scripts/rdd.sh branch --help
```

**Note:** The error message provides suggestions for typos!

### Issue 5: Different Output Format

**Symptom:**
Script parsing output breaks

**Cause:** New scripts use colored output with symbols

**Solution:**
Update parsing logic to handle new format:
```bash
# OLD parsing:
if [[ $output == *"Success"* ]]; then

# NEW parsing (symbols):
if [[ $output == *"✓"* ]]; then
```

Or disable colors if needed (feature not yet implemented, but can be added).

### Issue 6: Missing Utility Scripts

**Symptom:**
```
ERROR: core-utils.sh not found
```

**Solution:**
Ensure all utility scripts are present:
```bash
ls .rdd/scripts/*-utils.sh
# Should show: branch-utils.sh, change-utils.sh, clarify-utils.sh,
#              core-utils.sh, git-utils.sh, pr-utils.sh,
#              prompt-utils.sh, requirements-utils.sh, workspace-utils.sh
```

If missing, restore from repository or re-run setup.

---

## Rollback Procedure

If you need to rollback to old scripts:

### Quick Rollback

Old scripts are not immediately deleted - they remain in `.rdd/scripts/` during the transition period.

```bash
# Old scripts still work:
./create-change.sh my-feature feat
./.rdd/scripts/fix-management.sh mark-prompt-completed P01
```

### Full Rollback (Emergency)

If new scripts cause issues:

1. **Stop using `rdd.sh`**
   ```bash
   # Revert to old commands
   ./create-change.sh instead of rdd.sh change create
   ```

2. **Report issues**
   - Document the problem
   - Include error messages
   - Note which command failed
   - Report to team lead

3. **Wait for fix**
   - Old scripts remain functional
   - Continue normal work
   - Retry migration after fix

### After Old Scripts Archived

Once old scripts are moved to `.rdd/scripts/archive/`:

1. **Copy scripts back**
   ```bash
   cp .rdd/scripts/archive/*.sh .rdd/scripts/
   chmod +x .rdd/scripts/*.sh
   ```

2. **Or restore specific script**
   ```bash
   cp .rdd/scripts/archive/create-change.sh .rdd/scripts/
   chmod +x .rdd/scripts/create-change.sh
   ```

### Data Safety

**No data is lost during migration:**
- All workspace files remain unchanged
- Archive structure unchanged
- Requirements files unchanged
- Git history preserved
- Journal and logs intact

The migration only changes **how** you invoke commands, not **what** they do.

---

## Timeline

### Phase 1: Transition Period (Now - February 1, 2026)

**Duration:** 3 months  
**Status:** Both old and new scripts functional

**Actions:**
- ✅ New `rdd.sh` wrapper available
- ✅ All utility scripts created
- ✅ Old scripts remain in place
- ✅ Documentation updated
- ⏳ Users migrate at their own pace

**Recommendation:** Start migration immediately but no pressure.

### Phase 2: Deprecation Warnings (February 1 - March 1, 2026)

**Duration:** 1 month  
**Status:** Old scripts show deprecation warnings

**Actions:**
- ⚠️ Old scripts print deprecation warnings
- ⚠️ Warnings include migration instructions
- ✅ Both old and new scripts still functional
- ✅ Documentation emphasizes new commands

**Recommendation:** Complete migration during this period.

### Phase 3: Archive (March 1, 2026)

**Status:** Old scripts archived

**Actions:**
- 🗑️ Old scripts moved to `.rdd/scripts/archive/`
- ✅ Only `rdd.sh` used going forward
- 📚 Archive includes README with restoration instructions
- 📋 Archive preserved for reference

**Requirement:** All users must have migrated by this date.

### Important Dates

| Date | Milestone | Action Required |
|------|-----------|----------------|
| Nov 2, 2025 | Migration guide published | Read and plan migration |
| Nov 9, 2025 | Team training session | Attend training |
| Dec 1, 2025 | Mid-transition checkpoint | 50% migration target |
| Feb 1, 2026 | Deprecation warnings added | Complete migration |
| Mar 1, 2026 | Old scripts archived | Use only `rdd.sh` |

---

## Additional Resources

### Help Commands

```bash
# Main help
./.rdd/scripts/rdd.sh --help

# Domain-specific help
./.rdd/scripts/rdd.sh branch --help
./.rdd/scripts/rdd.sh workspace --help
./.rdd/scripts/rdd.sh requirements --help
./.rdd/scripts/rdd.sh change --help
./.rdd/scripts/rdd.sh fix --help
./.rdd/scripts/rdd.sh clarify --help
./.rdd/scripts/rdd.sh prompt --help
./.rdd/scripts/rdd.sh pr --help
./.rdd/scripts/rdd.sh git --help
```

### Version Information

```bash
# Check version
./.rdd/scripts/rdd.sh --version
```

### Quick Reference Card

```bash
# Most common commands:
rdd.sh change create <name> <type>   # Create change
rdd.sh change wrap-up                # Complete change
rdd.sh branch delete <name>          # Delete branch
rdd.sh requirements merge            # Merge requirements
rdd.sh prompt mark-completed <id>    # Mark prompt done
rdd.sh git compare                   # Compare with main
```

---

## Feedback and Support

### Questions?

- Check this migration guide
- Run `rdd.sh --help` or `rdd.sh <domain> --help`
- Review implementation plan: `.rdd-docs/workspace/scripts-refactor-implementation-plan.md`

### Issues?

- Document the problem clearly
- Include commands that failed
- Note error messages
- Check troubleshooting section above

### Suggestions?

Migration feedback is welcome! The new system is designed to be extensible.

---

## Summary

### Key Takeaways

1. **One Command:** `rdd.sh` replaces 7 different scripts
2. **Same Functionality:** No features removed, some added
3. **Better UX:** Consistent syntax, better help, clearer errors
4. **Safe Migration:** Old scripts remain during transition
5. **No Data Loss:** Only command syntax changes
6. **3-Month Timeline:** Plenty of time to migrate
7. **Full Support:** Documentation, help system, troubleshooting

### Quick Migration Steps

1. ✅ Read this guide
2. ✅ Test `rdd.sh` commands
3. ✅ Update your scripts using mapping table
4. ✅ Update documentation
5. ✅ Test thoroughly
6. ✅ Complete by February 1, 2026

### Success Metrics

✓ All commands work through `rdd.sh`  
✓ No old script references in your code  
✓ Documentation updated  
✓ Team trained  
✓ Workflows tested  

---

**Last Updated:** November 2, 2025  
**Migration Guide Version:** 1.0.0  
**Questions?** Review troubleshooting section or contact team lead
