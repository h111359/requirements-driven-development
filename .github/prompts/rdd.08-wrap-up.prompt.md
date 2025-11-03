# RDD: Wrap-Up Branch

## Purpose
Complete and finalize a development task by archiving the workspace, committing changes, and pushing to remote.

## Instructions

**S01: Display Banner**

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   RDD FRAMEWORK - Branch Wrap-Up
   
   → Archive workspace content
   → Commit and push changes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**S02: Check for Uncommitted Changes**

Check git status:
```bash
git status --short
```

If there are uncommitted changes (output is not empty):
- Display error message: "⚠️ There are uncommitted changes in the repository."
- Display: "Please commit or stash your changes before proceeding with wrap-up."
- Show the uncommitted changes using `git status`
- **STOP** - Do not proceed further

If no uncommitted changes (output is empty), continue to S03.

**S03: Display Wrap-Up Plan**

Display:
```markdown
## 📋 Wrap-Up Plan

This will perform the following actions:

1. ✓ Move workspace content to `.rdd-docs/archive/{branch-name}`
2. ✓ Create commit with message: "archive: moved workspace to archive"
3. ✓ Push changes to remote branch

Current branch: [display current branch name]
Archive destination: .rdd-docs/archive/[sanitized-branch-name]
```

**S04: Request User Confirmation**

Ask:
```
**Please confirm to proceed: (Y/N)**
```

If user responds with "N" or "n" or "no":
- Display: "Wrap-up cancelled by user."
- Exit gracefully

If user responds with "Y" or "y" or "yes":
- Continue to S05

**S05: Execute Archive Workspace**

Get current branch name:
```bash
git branch --show-current
```

Execute:
```bash
./.rdd/scripts/rdd.sh workspace archive
```

This will:
- Move all workspace content to `.rdd-docs/archive/{branch-name}`
- Clear the workspace directory
- Display progress and feedback

Display result:
```
✓ Workspace archived to: .rdd-docs/archive/[branch-name]
```

**S06: Create Commit**

Execute:
```bash
git add -A
git commit -m "archive: moved workspace to archive"
```

Display:
```
✓ Commit created: "archive: moved workspace to archive"
```

If commit fails (no changes to commit):
- Display: "ℹ️ No changes to commit (archive may already be up to date)"
- Continue to S07

**S07: Push to Remote**

Execute:
```bash
./.rdd/scripts/rdd.sh git push
```

Display result:
```
✓ Changes pushed to remote branch
```

If push fails:
- Display error: "✗ Failed to push to remote"
- Display: "Please check your network connection and permissions"
- Display: "You can manually push later with: git push"

**S08: Display Completion Summary**

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✓ WRAP-UP COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Summary

✓ Workspace archived to: .rdd-docs/archive/[branch-name]
✓ Commit created with message: "archive: moved workspace to archive"
✓ Changes pushed to remote branch: [current-branch]

## Next Steps

1. Create a Pull Request on GitHub to merge your changes
2. Review and complete the PR process
3. After merge, you can delete the local and remote branches

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Error Handling

**If not on a feature/fix branch:**
```
⚠️ Wrap-up must be executed from a feature or fix branch
Current branch: [current-branch]

Please switch to a feature or fix branch before running wrap-up.
```

**If workspace directory is empty:**
```
⚠️ Workspace directory is empty or does not exist
Location: .rdd-docs/workspace

There is nothing to archive. This may indicate:
- The workspace was already archived
- No work was done in the workspace
- Wrong branch or directory

Do you want to continue anyway? (Y/N)
```

**If archive directory already exists:**
```
⚠️ Archive directory already exists: .rdd-docs/archive/[branch-name]

This may indicate the workspace was already archived.

Options:
- (O) Overwrite existing archive
- (C) Cancel wrap-up

Your choice:
```

## Notes

- This prompt ensures all workspace content is properly archived before finalizing
- The commit message "archive: moved workspace to archive" is standardized for consistency
- User confirmation prevents accidental wrap-up execution
- Clear feedback is provided at each step
- Wrap-up can be safely re-run if it fails partway through

