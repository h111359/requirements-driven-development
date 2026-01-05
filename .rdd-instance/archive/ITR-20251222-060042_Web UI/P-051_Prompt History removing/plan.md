# Implementation Plan: Remove Prompts History Tab

## Overview

This plan details the steps to remove the Prompts History tab/page from the Web UI since all prompt information is now available in the Workdir section through the registry view. The questionnaire responses indicate that:
- View/edit functionality is already migrated to Workdir (Q1)
- API endpoints should be checked for usage in other pages before removal (Q2)
- JavaScript functions should be checked for usage before removal (Q3)
- Navigation menu item should be removed entirely (Q4)
- All references should be found and updated comprehensively (Q5)

## Implementation Steps

### Step 1: Verify Current State of View/Edit Functionality in Workdir

Check the Workdir page implementation to confirm that the view/edit modal functionality is already available when clicking on prompts in the registry view. Review the code to understand how it's currently implemented and ensure it's fully functional.

**Files to check:**
- `.rdd/src/web/static/app.js` - look for registry prompt click handlers
- `.rdd/src/web/templates/index.html` - check Workdir section structure

### Step 2: Identify All Code Related to Prompts History Page

Perform a comprehensive search to identify all code elements related to the Prompts History page:

**In HTML (`index.html`):**
- Navigation menu item for Prompts History (`<li>` with `onclick="showSection('prompts-history')"`)
- Section div `section-prompts-history`
- All child elements within the Prompts History section
- Any modal dialogs specifically for Prompts History

**In JavaScript (`app.js`):**
- `loadPromptsHistory()` function
- Any functions called only from Prompts History context
- Event handlers bound to Prompts History elements
- References to `'prompts-history'` section in `showSection()` calls

**In Backend (`server.py`):**
- `/api/prompts-list` endpoint
- Any other endpoints used exclusively by Prompts History

**In CSS (`style.css` if exists):**
- Styles specific to Prompts History section

### Step 3: Check API Endpoint Dependencies

Search for all usages of the `/api/prompts-list` endpoint:
- Check if it's used in the Workdir page
- Check if it's used in any other Web UI pages
- Check if it's used in CLI scripts or other automation

If the endpoint is only used by the Prompts History page, mark it for removal.
If it's used elsewhere, keep it and only remove the Prompts History UI elements.

### Step 4: Check JavaScript Function Dependencies

Analyze the `loadPromptsHistory()` function and related functions:
- Identify which functions are called only from Prompts History context
- Identify which functions are shared with other pages (like `viewCompletedPrompt` modal)
- Check if Workdir page already has its own implementation of viewing prompts

If there are shared functions that are also used by Workdir, keep them.
If functions are Prompts History-specific, mark them for removal.

### Step 5: Remove Navigation Menu Item

Remove the Prompts History navigation menu item from the top navigation bar:

**File:** `.rdd/src/web/templates/index.html`

Remove the entire `<li class="nav-item">` block that contains:
```html
<a class="nav-link" href="#" onclick="showSection('prompts-history')">
    <i class="bi bi-clock-history"></i> Prompts History
</a>
```

### Step 6: Remove Prompts History Section HTML

Remove the entire Prompts History section from the HTML:

**File:** `.rdd/src/web/templates/index.html`

Remove the complete `<div id="section-prompts-history" class="section">` block and all its child elements including:
- Card header
- Refresh button
- Table container
- All related markup

### Step 7: Remove Prompts History JavaScript Functions

Remove JavaScript functions that are exclusively used by Prompts History page:

**File:** `.rdd/src/web/static/app.js`

Remove:
- `loadPromptsHistory()` function (if not used elsewhere)
- Any helper functions called only from `loadPromptsHistory()`
- Event handlers specific to Prompts History elements

Keep:
- Any shared modal functions used by Workdir (if they exist)
- Shared utility functions

Update the `showSection()` function if it contains specific handling for `'prompts-history'` section.

### Step 8: Remove Backend API Endpoint (If Not Used)

If Step 3 confirmed the endpoint is not used elsewhere:

**File:** `.rdd/src/web/server.py`

Remove the `/api/prompts-list` endpoint handler including:
- The `elif path == "/api/prompts-list":` block
- The call to `self.execute_action("prompt", "list", {})`
- All related code in that block

If the endpoint is still used by other pages, skip this step and keep the endpoint.

### Step 9: Update References in showSection() Function

**File:** `.rdd/src/web/static/app.js`

In the `showSection()` function, remove any special handling for the `'prompts-history'` section, such as:
- Automatic data loading when section is shown
- Section-specific initialization code

### Step 10: Search and Update All References

Perform comprehensive search for all references to "Prompts History" or "prompts-history":

**Search patterns:**
- `prompts-history` (exact string)
- `Prompts History` (exact string with capitals)
- `PromptsHistory` (camelCase)
- `prompts_history` (snake_case)

**Files to search:**
- All `.py` files in `.rdd/src/`
- All `.js` files in `.rdd/src/web/static/`
- All `.html` files in `.rdd/src/web/templates/`
- All `.md` files in `.rdd/` and `.rdd-instance/`
- Any configuration files

**Actions for found references:**
- Code: Remove if obsolete, update if redirecting to Workdir
- Documentation: Update to mention Workdir instead
- Comments: Remove or update to reflect new structure
- Error messages: Update to reference Workdir

### Step 11: Update Documentation

Update any documentation files that mention Prompts History:

**Potential files:**
- `.rdd/docs/user-guide.md` - update navigation instructions
- README.md - update if it mentions Prompts History
- Help section content in Web UI
- Any tutorial or getting-started documents

Replace references to Prompts History with references to the Workdir registry view.

### Step 12: Clean Up CSS (If Applicable)

If there are CSS styles specific to Prompts History:

**File:** `.rdd/src/web/static/style.css` (if it exists)

Remove:
- Styles targeting `#section-prompts-history`
- Styles for Prompts History specific elements
- Any classes used only in Prompts History section

Keep:
- Shared styles used by other sections
- General utility classes

### Step 13: Update Help Documentation in Web UI

If the Help tab has instructions about navigating to Prompts History:

**Check:** Help section in `.rdd/docs/user-guide.md`

Update any sections that mention:
- How to view completed prompts (change from "Prompts History tab" to "Workdir registry view")
- Navigation instructions
- Workflow descriptions

### Step 14: Verify No Broken Links or References

After all removals:

1. Start the Web UI server
2. Navigate through all remaining sections (Active Prompt, Workdir, Technical Design, Requirements, Help)
3. Check browser console for JavaScript errors
4. Verify clicking on prompts in Workdir registry opens the view/edit modal properly
5. Verify all navigation menu items work correctly
6. Test that no functionality is broken

### Step 15: Update Requirements File

Based on the changes made, update the requirements file using the requirement scripts:

**No new requirements to add** - this is a removal/simplification task.

**No existing requirements to modify** - the existing UR-0004 and UR-0017 already describe the Web UI functionality at a high level without specifically mandating a Prompts History page. The Workdir registry view (implemented in P-050) satisfies the need for viewing prompts.

**No requirements to delete** - all existing requirements remain valid as the Workdir registry provides the needed functionality.

**Rationale:** The removal of Prompts History is an implementation detail that simplifies the UI while maintaining compliance with all existing requirements. UR-0004 requires "a web-based user interface for creating, editing, and managing prompts" which is still provided through the Active Prompt page and Workdir registry. UR-0017 requires "a Prompt Management page" which is fulfilled by the Active Prompt page. The redundant Prompts History page was never explicitly required.

### Step 16: Update Technical Design File (If Applicable)

Review `.rdd-instance/specifications/technical-design.json`:

If it contains any references to Prompts History page structure, update or remove them.
Otherwise, no changes needed as this is primarily a UI implementation detail.

### Step 17: Update Files and Folders Documentation

Review `.rdd-instance/specifications/files-and-folders.md`:

If it documents Web UI components or page structure in detail, update any references to Prompts History.
Otherwise, no changes needed as this file primarily documents the repository structure, not UI pages.

## Success Criteria

- Navigation menu no longer shows Prompts History item
- No JavaScript errors in browser console
- All remaining pages function correctly
- Clicking prompts in Workdir registry successfully opens view/edit functionality
- No broken references or links in code or documentation
- All comprehensive searches return no obsolete references to Prompts History
- Code is cleaner and more maintainable without redundant page

## Risk Mitigation

- Thorough dependency checking before removing API endpoints
- Verification testing after each removal step
- Git commit after successful removal to allow easy rollback if needed
