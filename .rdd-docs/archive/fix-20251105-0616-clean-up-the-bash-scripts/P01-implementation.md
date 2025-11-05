# P01 Implementation: Create Clean-Up Prompt

## Task
Create prompt `.github/prompts/rdd.09-clean-up.prompt.md` which should be executed after the PR is merged and should clean up the local environment via execution of the command "python3 .rdd/scripts/rdd.py branch cleanup".

## Analysis of Existing Prompts

Reviewed all prompts in `.github/prompts/`:
- rdd.01-initiate.prompt.md - Creates new changes (enh/fix)
- rdd.06-execute.prompt.md - Executes stand-alone prompts
- rdd.07-update-docs.prompt.md - Updates documentation
- rdd.08-wrap-up.prompt.md - Finalizes branch work
- rdd.G1-update-backlog.prompt.md - Updates backlog from GitHub issues
- rdd.G2-detect-docs-changes.prompt.md - Detects documentation changes
- rdd.G4-update-from-main.prompt.md - Updates branch from main

## Common Format Identified

The prompts follow this structure:
1. **Header**: Title with "RDD:" prefix
2. **Purpose**: Brief one-liner explaining the prompt's goal
3. **Context** (optional): Additional background information
4. **Instructions**: Step-by-step instructions (labeled S01, S02, etc.)
5. **Notes** (optional): Additional considerations or warnings

Key patterns:
- Short and concise instructions
- Clear step labels (S01, S02, etc.)
- Code blocks for commands
- Bullet points for explanations
- Clear "Why" or "Purpose" sections

## Implementation

Creating `.github/prompts/rdd.09-clean-up.prompt.md` following the identified format.

## Documentation Updates

Updated the following documentation files:

### 1. requirements.md
- Added **[GF-11] Post-Merge Branch Cleanup**: New general functionality for post-merge cleanup workflow
- Added **[FR-46] Post-Merge Cleanup Workflow**: Functional requirement for the new cleanup prompt

### 2. tech-spec.md
- Updated **Phase-Based Workflow** section to include step 6: Clean-Up phase

### 3. folder-structure.md
- Updated `.github/prompts/` listing to include `rdd.09-clean-up.prompt.md`

## Files Created

- `.github/prompts/rdd.09-clean-up.prompt.md` - New cleanup prompt following RDD format standards

## Summary

Successfully created the cleanup prompt and updated all relevant documentation to reflect the new post-merge cleanup workflow in the RDD framework.
