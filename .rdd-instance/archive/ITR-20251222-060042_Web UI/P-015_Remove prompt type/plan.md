# Plan for P-015: Remove prompt type

## Overview
This plan outlines the steps to remove the "type" field distinction between "main" and "modification" prompts from the RDD framework. Based on the questionnaire answers, we will:
- Remove the `parent-id` field entirely (Q1: Option A)
- Remove type field from all existing prompts (Q2: Option B)
- Remove type parameter completely from CLI (Q3: Option A)
- Remove parent-id parameter from prompt.create CLI (Q4: Option C)
- Remove parent-id field completely (Q5: Option D)

## Implementation Steps

### Step 1: Update prompt_create.py to remove type and parent-id handling
- Remove the type parameter from the create_prompt function signature
- Remove all validation logic related to type (lines 248-260)
- Remove parent-id parameter from the function
- Remove any parent-id validation logic
- Update the function to not include type or parent-id when creating new prompt entries

### Step 2: Update rdd.py CLI to remove type and parent-id prompts
- Remove the prompt type selection in the CLI (around line 198)
- Remove parent-id input prompts from the prompt creation workflow
- Update the create_prompt command call to not pass type or parent-id parameters

### Step 3: Update work-iteration-registry.json schema by removing type and parent-id from all existing prompts
- Create a migration script or update existing script to:
  - Load the work-iteration-registry.json file
  - Iterate through all prompts and remove the "type" field
  - Iterate through all prompts and remove the "parent-id" field if it exists
  - Save the updated registry back to the file
- Execute this migration as part of the implementation

### Step 4: Update any other scripts that read or write the type field
- Search for all occurrences of "type" field usage in Python scripts in `.rdd/src/`
- Update or remove code that depends on the type field
- Search for all occurrences of "parent-id" field usage
- Update or remove code that depends on the parent-id field

### Step 5: Update documentation and prompt snippets
- Review `.rdd/prompt-snippets/` for any references to prompt types or parent-id
- Update execution.md and other documentation files that reference type or parent-id
- Update any references in README.md or other documentation

### Step 6: Update Web UI components
- Review web UI JavaScript files for type field references
- Remove type and parent-id display/editing from the UI
- Update API endpoints if they expose or accept type/parent-id parameters

### Step 7: Verify test compatibility
- Check if any tests in `build/scripts/tests/` depend on type or parent-id fields
- Update tests to work without these fields

### Step 8: Update requirements.md
Add a new technical requirement documenting the simplified prompt model:

```markdown
- [TR-20260101-1000] The framework shall not distinguish between different types of prompts. All prompts shall be treated equally without type classification or parent-child relationships.
```

This requirement should be added to the Technical Requirements section.

### Step 9: Final verification
- Verify that all files in the work iteration registry no longer contain type or parent-id fields
- Test prompt creation through CLI to ensure it works without type/parent-id prompts
- Test prompt creation through Web UI to ensure it works correctly
- Run any existing tests to ensure no regressions

## Files to be modified

### Python Scripts
- `.rdd/src/actions/prompt_create.py` - Remove type and parent-id handling
- `.rdd/src/rdd.py` - Remove CLI prompts for type and parent-id
- Any other scripts in `.rdd/src/` that reference type or parent-id fields

### Data Files
- `.rdd-instance/workdir/work-iteration-registry.json` - Remove type and parent-id from all prompt entries

### Documentation
- `.rdd/prompt-snippets/execution.md` - Remove references to prompt types and parent-id
- `.rdd-instance/specifications/requirements.md` - Add new technical requirement

### Web UI (if applicable)
- Web UI JavaScript files that display or edit prompt type/parent-id

## Requirements Updates

The following requirement will be added to `.rdd-instance/specifications/requirements.md`:

**Location:** Technical Requirements section, after existing TR entries

**New Requirement:**
```
- [TR-20260101-1000] The framework shall not distinguish between different types of prompts. All prompts shall be treated equally without type classification or parent-child relationships.
```

This requirement codifies the removal of the type distinction and ensures the framework maintains a simple, unified prompt model going forward.

## Expected Outcome

After executing this plan:
1. All prompts will be treated equally without type distinction
2. The work-iteration-registry.json will have a cleaner schema without type or parent-id fields
3. The CLI will have a simpler prompt creation workflow
4. The codebase will be simpler with less validation logic
5. The framework will maintain backward compatibility by automatically migrating existing prompts