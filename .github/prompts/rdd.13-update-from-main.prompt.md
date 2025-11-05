# RDD: Update Branch from Main

## Purpose
Update the current branch with the latest commits from `main`, safely handling local changes and stopping for manual resolution if conflicts arise.

## Why
Keep the current branch synchronized with `main` after others merge changes — ensuring stability, preserving local work, and allowing manual control when conflicts occur.

## Instructions

**S01: Execute Update Command**

Run the automated update process:

```bash
python ./.rdd/scripts/rdd.py git update-from-main
```

This command will:
1. **Stash** all uncommitted local changes (including untracked files)
2. **Pull** the latest `main` branch from remote
3. **Merge** `main` into the current branch
4. **Restore** the stashed changes (leave them uncommitted)

**S02: Handle Result**

The command runs automatically with **no confirmations** required.

- **If successful**: Your branch is now up-to-date with `main`, and your local changes are restored as uncommitted.

- **If merge conflicts occur**: The process will **pause** with clear instructions:
  - Conflicts will be listed in the terminal
  - Follow the on-screen instructions to resolve conflicts manually:
    1. Edit conflicted files
    2. Stage resolved files: `git add <file>`
    3. Complete merge: `git commit`
    4. Restore your stashed changes: `git stash pop`

- **If stash restore fails**: Your changes remain safely in the stash. Restore manually with:
  ```bash
  git stash pop
  ```

## Notes

- This command is meant for feature/enhancement/fix branches only
- Cannot be run on the `main` branch itself
- All steps provide clear terminal feedback
- Local changes are preserved in git stash if issues occur
- No data loss - stashed changes can always be recovered
