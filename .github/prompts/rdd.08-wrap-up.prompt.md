````prompt
# RDD: Wrap-Up Branch

## Purpose
Complete and finalize a development task by updating documentation, archiving the workspace, committing all changes, and pushing to remote.

## Context
After completing enhancement or fix work, the wrap-up process ensures that:
- Project documentation reflects all changes made
- Workspace is properly archived for historical reference
- All changes are committed and pushed to remote
- The branch is ready for Pull Request creation

This prompt combines documentation updates and branch finalization into a single workflow.

## Instructions

**S01: Update Documentation**

Before wrapping up, ensure project documentation reflects your changes:

1. **Analyze changes**: Review `.rdd-docs/workspace/.rdd.copilot-prompts.md` to identify completed prompts (marked with `[x]`). For each completed prompt, search for implementation files named `<PROMPT_ID>-implementation.md` in `.rdd-docs/workspace/`. Read and extract relevant changes from these files.

2. **Update affected documentation files**:
   - **Requirements changes** → `.rdd-docs/requirements.md`
     - Add new requirements with next sequential ID in format: `- **[ID] Title**: Description`
     - Modify existing requirements by ID, preserving structure
     - Mark deletions as `- **[ID] [DELETED]` (never delete lines)
   - **Technical changes** → `.rdd-docs/tech-spec.md`
   - **Folder structure changes** → `.rdd-docs/folder-structure.md`
   - **Data model changes** → `.rdd-docs/data-model.md`

3. **Important guidelines**:
   - Preserve ID sequences (never renumber existing IDs)
   - Mark deletions with `[DELETED]` instead of removing lines
   - When adding requirements, continue from highest existing ID in that section
   - Maintain existing structure and formatting
   - Validate that all ID sequences remain continuous
   - When updating `.rdd-docs/requirements.md`, ensure it aligns with `.rdd/templates/requirements-format.md`

**S02: Execute Wrap-Up**

Run the wrap-up command:

```bash
python .rdd/scripts/rdd.py change wrap-up
```

The script will:
1. Validate you're on an enhancement or fix branch (enh/* or fix/*)
2. Display wrap-up plan
3. Ask for user confirmation
4. Archive workspace to `.rdd-docs/archive/[sanitized-branch-name]`
5. Stage and commit all changes (including documentation updates) with message: "wrap up <branch-name>"
6. Push changes to remote branch
7. Display completion summary with next steps

**S03: Create Pull Request**

After wrap-up completes:
1. Create a Pull Request on GitHub to merge your changes
2. Review and complete the PR process
3. After the PR is merged, run cleanup:

```bash
python .rdd/scripts/rdd.py branch cleanup
```

**Alternative: Specify Branch Name**

If you want to specify the branch name explicitly during cleanup:

```bash
python .rdd/scripts/rdd.py branch cleanup <branch-name>
```

## Notes

- **Documentation first**: Always update documentation before running wrap-up command
- **Validation**: The script validates you're on an enh/* or fix/* branch before proceeding
- **Auto-commit**: All uncommitted changes (including documentation updates) are automatically committed
- **Confirmation required**: User confirmation prevents accidental execution
- **Standardized format**: Commit message format is "wrap up <branch-name>"
- **Complete archive**: All workspace content is archived with branch-specific naming
- **Clean workflow**: Cleanup removes both local and remote branches after PR merge

````

