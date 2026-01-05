# Implementation Plan for P-025: Modification Implementation files - visible

## Context

The Active Prompt page currently shows modifications in the Modifications tab, displaying the modification description text from `modification-XXX.md` files. However, the `modification-XXX-implementation.md` files (which contain detailed logs of what was changed during each modification) are not visible in the Web UI. This plan outlines how to add viewing capability for these implementation files.

## Questionnaire Summary

Based on the answered questionnaire:
- **Q1 (Option A)**: Add a 'View Implementation' button next to each modification that opens the implementation file in a modal/dialog
- **Q2 (Option A)**: Implementation files should be read-only (not editable)
- **Q3 (Option A)**: Display content as plain text in a textarea or pre element with monospace font

## Implementation Steps

### Step 1: Analyze Current Modifications Display Structure

**Objective:** Understand how modifications are currently displayed in the Active Prompt page.

**Actions:**
1. Review the current implementation in `.rdd/src/web/static/app.js` - specifically the `loadModifications()` function
2. Review the modifications list HTML structure in `.rdd/src/web/templates/index.html`
3. Identify where the "View Implementation" button should be added in the UI
4. Understand how modification data is fetched from the backend

**Expected Findings:**
- The `loadModifications()` function fetches modification data via `/api/modification/list`
- Each modification is displayed in a list with edit button for in-progress modifications
- The modifications tab is in the active prompt editor section

### Step 2: Create Modal Dialog for Implementation Display

**Objective:** Add a Bootstrap modal dialog to display modification implementation files.

**Actions:**
1. Add a new modal in `.rdd/src/web/templates/index.html` after the existing modals:
   - Modal ID: `viewModificationImplementationModal`
   - Modal title: "Modification [ID] - Implementation Log"
   - Modal body: textarea or pre element with `readonly` attribute
   - Modal footer: Close button
   - Use monospace font for the content area

2. Style the content area with:
   - `font-family: monospace`
   - `white-space: pre-wrap` to preserve formatting
   - `height: 60vh` or similar for adequate viewing space
   - `overflow-y: auto` for scrolling long logs

**Files to Modify:**
- `.rdd/src/web/templates/index.html`

### Step 3: Add View Implementation Button to Modifications List

**Objective:** Add a "View Implementation" button next to each modification in the list.

**Actions:**
1. Modify the `loadModifications()` function in `.rdd/src/web/static/app.js`:
   - For each modification in the list, add a "View Implementation" button
   - Button should have icon (e.g., `<i class="bi bi-file-earmark-text"></i>`)
   - Button should call a new function `viewModificationImplementation(modificationId)`
   - Position button next to existing Edit/Delete buttons

2. Button should be visible for all modifications (both in-progress and completed)

**Files to Modify:**
- `.rdd/src/web/static/app.js`

### Step 4: Implement viewModificationImplementation() Function

**Objective:** Create JavaScript function to load and display modification implementation file.

**Actions:**
1. Add new function `viewModificationImplementation(modificationId)` in `.rdd/src/web/static/app.js`:
   - Construct filepath: `${currentPromptFolder}/modification-${modificationId}-implementation.md`
   - Fetch file content via `/api/file/` endpoint with proper URL encoding
   - Handle cases where implementation file doesn't exist (show appropriate message)
   - Open the modal and populate the content area
   - Set modal title with modification ID

2. Error handling:
   - If file doesn't exist: show message "Implementation log not yet created"
   - If file load fails: show error message in modal
   - If file is empty: show message "No implementation log recorded"

**Files to Modify:**
- `.rdd/src/web/static/app.js`

### Step 5: Test the Implementation

**Objective:** Verify the feature works correctly.

**Test Cases:**
1. Open Active Prompt page with a prompt that has modifications
2. Navigate to Modifications tab
3. Click "View Implementation" button on a completed modification
4. Verify modal opens with properly formatted content
5. Verify content is read-only (cannot be edited)
6. Close modal and verify it can be reopened
7. Test with modification that has no implementation file yet
8. Test with long implementation logs (verify scrolling works)

**Expected Results:**
- Modal opens smoothly
- Content displays with preserved formatting (whitespace, line breaks)
- Content is clearly read-only
- Modal closes properly
- Error cases handled gracefully

### Step 6: Update Requirements Documentation

**Objective:** Document the new feature in requirements.md.

**Actions:**
1. Add new user requirement in `.rdd-instance/specifications/requirements.md`:
   - Requirement ID: `[UR-20260102-XXXX]` (use appropriate timestamp)
   - Requirement text: "The Web UI Active Prompt page shall provide a 'View Implementation' button for each modification in the Modifications tab that displays the modification's implementation log file in a read-only modal dialog with monospace font formatting."
   - Category: User Requirements
   - Insert in chronological order by requirement ID

**Files to Modify:**
- `.rdd-instance/specifications/requirements.md`

## Summary

This implementation adds viewing capability for modification implementation logs in the Web UI by:
1. Adding a modal dialog to display implementation file content
2. Adding "View Implementation" buttons next to each modification
3. Loading and displaying `modification-XXX-implementation.md` files in read-only format with monospace font
4. Handling error cases (missing files, load failures)
5. Documenting the feature in requirements.md

The approach follows Option A from Q1 (button + modal), Option A from Q2 (read-only), and Option A from Q3 (plain text with monospace font), providing a simple and consistent way to view implementation logs without cluttering the UI.
