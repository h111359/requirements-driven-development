````prompt
# RDD: Wrap-Up Branch

## Purpose
Complete and finalize a development task by updating documentation, archiving the workspace, committing all changes, and pushing to remote.

## Context
After completing a work iteration the documentation process ensures that project documentation reflects all changes made.

## Instructions

**S01: Update Documentation**

Ensure project documentation reflects your changes:

1. **Analyze changes**: Review `.rdd-docs/workspace/.rdd.copilot-prompts.md` to identify completed prompts (marked with `[x]`). For each completed prompt, search for implementation files named `<PROMPT_ID>-implementation.md` in `.rdd-docs/workspace/`. Read also the rest of the documents in `.rdd-docs/workspace/` and extract relevant changes from these files.

2. **Update affected documentation files**:
   - **Requirements changes** → `.rdd-docs/requirements.md`
     - Add new requirements with next sequential ID in format: `- **[ID] Title**: Description`
     - Modify existing requirements by ID, preserving structure
     - Mark deletions as `- **[ID] [DELETED]` (never delete lines)
   - **Technical changes** → `.rdd-docs/tech-spec.md`
   - **Folder structure changes** → `.rdd-docs/folder-structure.md`
   - **Data model changes** → `.rdd-docs/data-model.md`
   - **Release notes** → `.rdd-docs/release-notes-<version>.md` (where `<version>` is the new version from `.rdd-docs/config.json`) - create or update release notes file, summarize key changes, new features, bug fixes and follow the existing format for consistency.

3. **Update Folder Structure**:
   - Scan recursively the project directory to identify any new files, directories, or structural changes. (Exclude `.rdd-docs/archive`, `.venv`, `venv`, and `.git` directories)
   - Reflect any new files, directories, or structural changes in `.rdd-docs/folder-structure.md`.
   - Ensure descriptions are clear and concise. 

4. **Update Data Model**:
   - Review changes in data-related files (e.g., JSON, YAML, database schemas).
   - Update `.rdd-docs/data-model.md` to reflect any additions, deletions, or modifications to the data model.

## **Important guidelines**:
   - Preserve ID sequences (never renumber existing IDs)
   - When adding requirements, continue from highest existing ID in that section
   - Maintain existing structure and formatting
   - Validate that all ID sequences remain continuous

## Notes

- **Documentation first**: Always update documentation before running wrap-up command
- **Validation**: The script validates you're on an enh/* or fix/* branch before proceeding
- **Auto-commit**: All uncommitted changes (including documentation updates) are automatically committed
- **Confirmation required**: User confirmation prevents accidental execution
- **Standardized format**: Commit message format is "wrap up <branch-name>"
- **Complete archive**: All workspace content is archived with branch-specific naming
- **Clean workflow**: Cleanup removes both local and remote branches after PR merge

````

