# RDD: Clean Up After Merge

## Purpose
Clean up local environment after a PR is merged to main.

## Context
After your enhancement or fix branch is merged via PR, this prompt removes the local and remote branches to keep your workspace clean.

## Instructions

**S01: Execute Clean-Up**

Run the cleanup command:

```bash
python .rdd/scripts/rdd.py branch cleanup
```

The script will:
1. Switch to the `main` branch
2. Fetch and pull the latest changes from remote
3. Delete the merged feature/fix branch (both local and remote)
4. Display completion summary

**Alternative: Specify Branch Name**

If you want to clean up a specific branch explicitly:

```bash
python .rdd/scripts/rdd.py branch cleanup <branch-name>
```

## Notes

- Run this only after your PR is merged
- Ensures local and remote branches are removed
- Keeps your workspace synchronized with main
- Safe to run - validates branch exists before deletion
