# RDD: Wrap-Up Branch

## Purpose
Complete and finalize a development task by archiving the workspace, committing all changes, and pushing to remote.

## Instructions

**S01: Execute Wrap-Up**

Run the wrap-up command:

```bash
python3 .rdd/scripts/rdd.py change wrap-up
```

The script will:
1. Validate you're on an enhancement or fix branch (enh/* or fix/*)
2. Display wrap-up plan
3. Ask for user confirmation
4. Archive workspace to `.rdd-docs/archive/[sanitized-branch-name]`
5. Stage and commit all changes (including any uncommitted changes) with message: "wrap up <branch-name>"
6. Push changes to remote branch
7. Display completion summary with next steps

**Important Notes:**
- The script will stop if you're not on an enh/* or fix/* branch
- All uncommitted changes will be automatically committed during wrap-up
- User confirmation is required before proceeding
- All workspace content is properly archived with branch-specific naming

**S02: Follow Next Steps**

After the wrap-up completes, follow the displayed instructions to:
1. Create a Pull Request on GitHub to merge your changes
2. Review and complete the PR process
3. After the PR is merged, clean up your local environment:

```bash
python3 .rdd/scripts/rdd.py branch cleanup
```

This command will:
- Switch to the main branch
- Fetch and pull the latest changes from remote
- Delete the merged feature/fix branch (both local and remote)
- Display completion summary

Alternatively, if you want to specify the branch name explicitly:
```bash
python3 .rdd/scripts/rdd.py branch cleanup <branch-name>
```

## Notes

- The script validates you're on an enhancement or fix branch before proceeding
- Uncommitted changes are expected and will be automatically committed
- User confirmation prevents accidental execution
- The commit message format is standardized: "wrap up <branch-name>"
- Clear feedback is provided at each step

