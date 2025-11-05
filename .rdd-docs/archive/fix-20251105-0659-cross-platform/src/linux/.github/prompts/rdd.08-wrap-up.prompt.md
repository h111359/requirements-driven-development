# RDD: Wrap-Up Branch

## Purpose
Complete and finalize a development task by archiving the workspace, committing changes, and pushing to remote.

## Instructions

**S01: Execute Wrap-Up**

Determine the current branch type and execute the appropriate wrap-up command:

For enhancement branches (starting with `enh/`):
```bash
./.rdd/scripts/rdd.sh change wrap-up
```

For fix branches (starting with `fix/`):
```bash
./.rdd/scripts/rdd.sh fix wrap-up
```

The script will:
1. Check for uncommitted changes (stops if any exist)
2. Display wrap-up plan
3. Ask for user confirmation
4. Archive workspace to `.rdd-docs/archive/[sanitized-branch-name]`
5. Create commit with message: "archive: moved workspace to archive"
6. Push changes to remote branch
7. Display completion summary with next steps

**S02: Follow Next Steps**

After the wrap-up completes, follow the displayed instructions to:
1. Create a Pull Request on GitHub to merge your changes
2. Review and complete the PR process
3. After the PR is merged, clean up your local environment:

```bash
./.rdd/scripts/rdd.sh branch cleanup
```

This command will:
- Switch to the main branch
- Fetch and pull the latest changes from remote
- Delete the merged feature/fix branch (both local and remote)
- Display completion summary

Alternatively, if you want to specify the branch name explicitly:
```bash
./.rdd/scripts/rdd.sh branch cleanup <branch-name>
```

## Notes

- The script validates you're on an enhancement or fix branch
- User confirmation prevents accidental execution
- All workspace content is properly archived with branch-specific naming
- The commit message is standardized for consistency across the project
- Clear feedback is provided at each step

