## What

Create a prompt `.github/prompts/F1-create-fix-branch.prompt.md` which takes the current uncommitted state and creates a new branch locally and remotely. Ask the user for a name (normalize in kebab-case). See prompts `rdd.01-create-change.prompt.md` and `rdd.02-clarify-requirements.prompt.md` for style and formatting. Create a script `.rdd/scripts/fix-management.sh` for all scriptable actions. The script should copy only `.rdd/templates/change.md` in the workspace folder. The prompt should ask the user iteratively about the fix What and Why and fill the respective sections in `change.md`. For Acceptance Criteria enter 'N/A'. The script should checkout the new branch and make it active for further changes.

Extend `.rdd/scripts/fix-management.sh` with a wrap-up flow tailored for fixes that archives the current `.rdd-docs/workspace` content into `.rdd-docs/archive/fixes`, creates a wrap-up commit (if changes exist), pushes the fix branch, and opens a pull request against `main` (using GitHub CLI when available, otherwise offering manual instructions).

Additionally, describe the script `scripts/delete-merged-branches.sh`:

This script provides an interactive tool for cleaning up git branches that have already been merged into the default branch (usually `main` or `master`). It:
- Checks for a git repository
- Determines the default branch
- Fetches latest changes from remote
- Lists all local branches merged into the default branch (excluding default/current branch)
- Indicates for each branch if it exists locally, remotely, or both
- Presents an interactive menu for selection (arrow keys, j/k, spacebar, a/n, Enter, q)
- Asks for confirmation before deletion
- Deletes selected branches locally (with force if needed) and remotely (if present)
- Provides color-coded feedback for each action
- Exits gracefully if no branches are selected or user cancels.
  

Add also prompts:
rdd.F1-create-fix-branch.prompt.md
rdd.F6-wrap-up.prompt.md


## Why

Add convenience to wrap up the things at the end of the feature + provide a mechanizm for quick fixes without bothering with requirements. Automating the fix wrap-up keeps the documentation archived, ensures the branch is pushed, and reduces the manual steps required to request a merge.

## Acceptance Criteria:

N/A
