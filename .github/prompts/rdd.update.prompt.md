## Context

The documentation files should be updated accordingly the development task performed after completing a work iteration to be ensured that project documentation reflects all changes made. Execute the following instructions in the order specified below:

## Instructions

   **Step 01: Analyze changes**: 
   - Review `.rdd-docs/work-iteration-prompts.md` to identify completed prompts (marked with `[x]`). For each completed prompt, search for implementation files named `<PROMPT_ID>-implementation.md` in `.rdd-docs/workspace/`. Read also the rest of the documents in `.rdd-docs/workspace/` and extract relevant changes from these files.
   - Scan recursively the project directory to identify any new files, directories, or structural changes. (Exclude `.rdd-docs/archive`, `.venv`, `venv`, and `.git` directories)
   - Create a full list of all changes made in a file '.rdd-docs/workspace/.rdd.changes.md', categorizing them into:
     - New features
     - Bug fixes
     - Improvements
     - Documentation updates
     - Data model changes

   **Step 02: Update affected documentation files**:
   - **Requirements changes** → `.rdd-docs/requirements.md`
   - Add new requirements with next sequential ID in format: `- **[ID] Title**: Description`
   - Modify existing requirements by ID, preserving structure
   - Mark deletions as replacing the requirement text with `[DELETED]` (never delete lines and their IDs)
   - Preserve ID sequences (never renumber existing IDs)
   - When adding requirements, continue from highest existing ID in that section
   - Maintain existing structure and formatting
   - Validate that all ID sequences remain continuous

   **Step 03: Update Tests**:
   - If the project includes automated tests, update or add new test cases to cover the changes made.
   - Ensure that all new features and bug fixes are adequately tested.
   - Execute the test suite to verify that all tests pass successfully after the updates. Fix any issues that arise during testing. Loop back to update requirements and technical specifications if new issues are found. Itterate until all tests pass.
   
   **Step 04: Update Technical Specifications**:
   - Review changes in implementation files and update `.rdd-docs/tech-spec.md` accordingly the analysis you have made.
   - Ensure all technical details, configurations, and implementation notes are accurate and up-to-date.
   - Update the folder structure:
       1. Compare the documented folder structure with the actual project structure
       2. Add new folders/files to documentation
       3. Update modified folders/files in documentation
       4. Remove obsolete/non-existent folders from documentation
       5. Verify each documented folder actually exists
   - Update the data model
   - Preserve ID sequences (never renumber existing IDs)
   - When adding requirements, continue from highest existing ID in that section
   - Maintain existing structure and formatting
   - Validate that all ID sequences remain continuous   

