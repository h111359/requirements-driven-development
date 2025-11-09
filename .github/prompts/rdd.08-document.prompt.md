````prompt
# RDD: Update Documentation

## Purpose
To be updated the documentation files accordingly the development task performed.

## Context
After completing a work iteration the documentation process ensures that project documentation reflects all changes made.

## Instructions

**S01: Update Documentation**

Ensure project documentation reflects your changes and the real state of the project. Update the following documentation files as needed:

1. **Analyze changes**: 
   - Review `.rdd-docs/workspace/.rdd.copilot-prompts.md` to identify completed prompts (marked with `[x]`). For each completed prompt, search for implementation files named `<PROMPT_ID>-implementation.md` in `.rdd-docs/workspace/`. Read also the rest of the documents in `.rdd-docs/workspace/` and extract relevant changes from these files.
   - Scan recursively the project directory to identify any new files, directories, or structural changes. (Exclude `.rdd-docs/archive`, `.venv`, `venv`, and `.git` directories)
   - Create a full list of all changes made in a file '.rdd-docs/workspace/.rdd.changes.md', categorizing them into:
     - New features
     - Bug fixes
     - Improvements
     - Documentation updates
     - Data model changes

2. **Update affected documentation files**:
   - **Requirements changes** → `.rdd-docs/requirements.md`
   - Add new requirements with next sequential ID in format: `- **[ID] Title**: Description`
   - Modify existing requirements by ID, preserving structure
   - Mark deletions as `- **[ID] [DELETED]` (never delete lines)
   - Preserve ID sequences (never renumber existing IDs)
   - When adding requirements, continue from highest existing ID in that section
   - Maintain existing structure and formatting
   - Validate that all ID sequences remain continuous

3. **Update Technical Specifications**:
   - Review changes in implementation files and update `.rdd-docs/tech-spec.md` accordingly the analysis you have made.
   - Ensure all technical details, configurations, and implementation notes are accurate and up-to-date.
   - Preserve ID sequences (never renumber existing IDs)
   - When adding requirements, continue from highest existing ID in that section
   - Maintain existing structure and formatting
   - Validate that all ID sequences remain continuous   

4. **Update Folder Structure**:
   - Reflect any new files, directories, or structural changes in `.rdd-docs/folder-structure.md`.
   - Ensure descriptions are clear and concise. 

5. **Update Data Model**:
   - Review changes in data-related files (e.g., JSON, YAML, database schemas).
   - Update `.rdd-docs/data-model.md` to reflect any additions, deletions, or modifications to the data model.

````

