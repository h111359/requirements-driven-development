# Implementation Log - P-054: Remove view button in Workdir

## Prompt Summary
Remove the redundancy in the Workdir registry table where both the View button and clicking on the prompt name open the same modal.

## Questionnaire Answers
- Q1: Option A - Remove the View button from the Actions column, keep the clickable title
- Q2: Option C - Remove the Actions column entirely 
- Q3: Option C - Add cursor:pointer and subtle color change on hover, but no underline

## Relevant Context

From requirements.md:
- [UR-0091] The Web UI Workdir page shall display the work iteration registry in a comprehensive, human-readable format showing iteration metadata and a table of all prompts with their states, execution modes, and workflow flags

From files-and-folders.md:
- Web UI static files: `.rdd/src/web/static/app.js`, `.rdd/src/web/static/style.css`
- Web UI templates: `.rdd/src/web/templates/index.html`

## Implementation Steps

### Step 1: Update renderRegistryView function in app.js

Removing the Actions column header and View button from the Workdir registry table.

File: `.rdd/src/web/static/app.js`

Changes:
1. Remove the "Actions" column header from the table (was 12th column)
2. Remove the View button code from each prompt row
3. Update colspan in "no prompts" row from 12 to 11 to match new column count

The clickable title link functionality remains unchanged - it already calls `openPromptFromRegistry(promptId)` which opens the view modal.

### Step 2: Add hover styling for clickable title

File: `.rdd/src/web/static/style.css`

Added CSS rules for the `.prompt-title-link` class:
- `cursor: pointer` - Changes cursor to indicate clickability
- `transition: color 0.2s ease` - Smooth color transition on hover
- On hover: color changes to darker blue (#0056b3) with no text decoration

This provides visual feedback to users that the title is clickable while maintaining a clean table appearance.

## Summary of Changes

Successfully removed the redundant View button from the Workdir registry table:

1. **app.js changes:**
   - Removed "Actions" column header (line ~1895)
   - Added `prompt-title-link` CSS class to title links for styling
   - Removed View button code and variable (lines ~1922-1925)
   - Removed View button table cell from row output (line ~1938)
   - Updated colspan from 12 to 11 in "no prompts" message (line ~1943)

2. **style.css changes:**
   - Added `.prompt-title-link` class with cursor:pointer
   - Added hover effect with color change to #0056b3

The table is now cleaner and more compact with 11 columns instead of 12. Users can click on the prompt title to view the prompt modal, which is a standard and intuitive UI pattern.

## Requirements Analysis

Reviewing requirements.md:
- [UR-0091] already covers the Workdir registry display requirements
- No new requirements needed - this is a UI refinement/cleanup

The changes align with existing requirements and improve the user experience by:
- Reducing visual clutter
- Following standard UI patterns (clickable titles)
- Maintaining all functionality while improving usability

No requirement changes needed for this implementation.

