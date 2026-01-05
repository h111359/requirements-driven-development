# Implementation Plan: Add Prompt Snippet Insertion UI to Web Interface

## Overview
This plan implements prompt snippet insertion functionality in the Web UI, allowing users to insert snippet keys (e.g., `[[[ROLE_SOLUTION_ARCHITECT]]]`) into prompts through an autocomplete dropdown interface with preview capabilities and validation on save.

## User Selections from Questionnaire
- **Q1**: Custom autocomplete dropdown (like VS Code IntelliSense) - triggers on typing `[[[`
- **Q2**: Preview pane within the picker (split view) - show snippet content
- **Q3**: Validate only on save/submit with error dialog

## Implementation Steps

### Step 1: Backend API - Snippet Data Endpoint
Create a new API endpoint to serve snippet definitions from manifest.json.

**Actions:**
- Add `/api/snippets` GET endpoint in `.rdd/src/web/app.py`
- Endpoint should read `.rdd/config/manifest.json`
- Return JSON array with snippet keys, paths, and file contents:
  ```json
  {
    "snippets": [
      {
        "key": "[[[ROLE_SOLUTION_ARCHITECT]]]",
        "path": ".rdd/prompt-snippets/role.solution-architect.md",
        "description": "Act as Solution Architect",
        "content": "<file content>"
      }
    ]
  }
  ```
- Handle file reading errors gracefully
- Cache snippet data to avoid repeated file reads

### Step 2: Frontend Service - Snippet Manager
Create a JavaScript service to manage snippet data and operations.

**Actions:**
- Create new file: `.rdd/src/web/static/snippet-service.js`
- Implement `SnippetService` class with methods:
  - `loadSnippets()`: Fetch snippets from `/api/snippets`
  - `searchSnippets(query)`: Filter snippets by key or description
  - `getSnippetByKey(key)`: Get single snippet details
  - `validateSnippetKeys(text)`: Find invalid snippet keys in text
- Handle caching of snippet data after first load
- Provide error handling for API failures

### Step 3: Autocomplete Dropdown Component
Create an autocomplete dropdown UI component that triggers when user types `[[[`.

**Actions:**
- Create new file: `.rdd/src/web/static/snippet-autocomplete.js`
- Implement autocomplete component with:
  - Event listener on prompt textarea for input changes
  - Detect when user types `[[[` sequence
  - Show dropdown positioned below cursor
  - Display filtered snippet list based on typed text after `[[[`
  - Highlight matching parts in snippet keys
  - Handle keyboard navigation (Arrow Up/Down, Enter, Escape)
  - Handle mouse selection
  - Auto-close on blur or Escape
- Position dropdown absolutely relative to cursor position in textarea
- Style dropdown with Bootstrap classes for consistency

### Step 4: Split View Preview Panel
Add a preview panel to the autocomplete dropdown showing snippet content.

**Actions:**
- Extend autocomplete dropdown to include two panes:
  - Left pane: Snippet list (40% width)
  - Right pane: Preview content (60% width)
- When user hovers or navigates to a snippet in list:
  - Display snippet key and file path in preview header
  - Display snippet file content in preview body
  - Apply syntax highlighting for markdown content
- Preview should scroll independently from the list
- Use monospace font for snippet content display
- Add loading indicator while fetching snippet content

### Step 5: Snippet Insertion Logic
Implement the logic to insert selected snippet key at cursor position.

**Actions:**
- In `snippet-autocomplete.js`, add `insertSnippet(snippetKey)` method
- Calculate correct cursor position in textarea
- Insert snippet key text at cursor position
- Update textarea value and trigger input event
- Close autocomplete dropdown after insertion
- Set focus back to textarea with cursor after inserted text
- Handle edge cases (selection replacement, multiple cursors not needed)

### Step 6: Snippet Validation on Save
Implement validation that checks for invalid snippet keys when user saves prompt.

**Actions:**
- Modify prompt save handler in `.rdd/src/web/static/app.js`
- Before saving, call `SnippetService.validateSnippetKeys(promptText)`
- If invalid keys found:
  - Show Bootstrap modal dialog with error message
  - List all invalid snippet keys found
  - Provide options: "Fix Manually" (cancel save) or "Save Anyway"
  - If "Save Anyway", proceed with save
  - If "Fix Manually", keep prompt editor open
- If no invalid keys, proceed with normal save

### Step 7: UI Integration - Toolbar Button
Add a toolbar button to manually trigger snippet picker (alternative to typing `[[[`).

**Actions:**
- Add button to prompt editor toolbar in `index.html`:
  - Label: "Insert Snippet" or icon representation
  - Position: Next to other prompt editor actions
  - Click handler: Opens autocomplete dropdown at cursor position
- Button should be disabled when no prompt is active
- Add tooltip explaining the feature and keyboard shortcut

### Step 8: CSS Styling
Create CSS styles for the autocomplete dropdown and preview panel.

**Actions:**
- Add styles to `.rdd/src/web/static/style.css`:
  - `.snippet-autocomplete-container`: Main dropdown container
  - `.snippet-list`: Left pane with snippet options
  - `.snippet-preview`: Right pane with content preview
  - `.snippet-list-item`: Individual snippet in list
  - `.snippet-list-item.active`: Highlighted/selected snippet
  - `.snippet-preview-header`: Preview panel header
  - `.snippet-preview-content`: Preview panel body
- Ensure responsive behavior (collapse preview on small screens)
- Use z-index to ensure dropdown appears above other elements
- Add smooth transitions for hover states

### Step 9: Error Handling and Edge Cases
Implement robust error handling for various edge cases.

**Actions:**
- Handle network errors when loading snippets (show user-friendly message)
- Handle empty snippet list (show "No snippets available")
- Handle typing `[[[` in non-editable contexts (disabled state)
- Handle rapid typing (debounce autocomplete trigger by 150ms)
- Handle cursor at start/end of textarea
- Handle already-complete snippet keys (don't show autocomplete)
- Prevent autocomplete from breaking prompt editing flow
- Log errors to console for debugging

### Step 10: Testing and Documentation
Test the feature thoroughly and update documentation.

**Actions:**
- Manual testing:
  - Test autocomplete triggers correctly on typing `[[[`
  - Test keyboard navigation (arrows, enter, escape)
  - Test mouse selection
  - Test preview panel shows correct content
  - Test snippet insertion at various cursor positions
  - Test validation catches invalid snippet keys
  - Test save dialog allows fix or override
  - Test toolbar button opens picker
- Cross-browser testing (Chrome, Firefox, Edge)
- Test on different screen sizes
- Update user documentation (if exists)
- Add inline code comments for maintainability

## Updates to Specification Files

### Requirements Updates (`.rdd-instance/specifications/requirements.md`)

Add new user requirement:
```
- [UR-20251226-0922] The Web UI shall provide a snippet insertion feature for the prompt editor that enables users to insert predefined prompt snippet keys through an autocomplete dropdown interface. The autocomplete shall trigger when user types '[[[' and display available snippets with preview content. The system shall validate snippet keys against manifest.json on save and warn about invalid keys.
```

### Technical Design Updates (`.rdd-instance/specifications/technical-design.json`)

Add technical specification entries (to be populated in JSON format during implementation):
- Component: Web UI - Snippet Service
  - Technology: Vanilla JavaScript
  - API Endpoint: /api/snippets
  - Data source: .rdd/config/manifest.json
  
- Component: Web UI - Autocomplete Dropdown
  - Technology: Vanilla JavaScript + Bootstrap 5
  - Trigger: User types '[[[' in prompt textarea
  - Features: Search, keyboard navigation, preview panel
  
- Component: Validation
  - Timing: On prompt save/submit
  - Behavior: Modal dialog with invalid keys list and options

### Files and Folders Updates (`.rdd-instance/specifications/files-and-folders.md`)

Add new files:
- `.rdd/src/web/static/snippet-service.js` - Snippet data management service
- `.rdd/src/web/static/snippet-autocomplete.js` - Autocomplete UI component

Modify existing files:
- `.rdd/src/web/app.py` - Add /api/snippets endpoint
- `.rdd/src/web/static/app.js` - Add validation on save
- `.rdd/src/web/templates/index.html` - Add snippet button to toolbar
- `.rdd/src/web/static/style.css` - Add autocomplete styles

## Compliance with Existing Requirements

This implementation complies with:
- **UR-20251224-0904**: Extends Web UI functionality for prompt editing
- **UR-20251224-0907**: Provides controlled modification through UI
- **UR-20251224-0902**: Leverages existing prompt snippet library
- **UR-20251224-0906**: Works on both Windows and Linux (web-based)
- **UR-20251224-0910**: Uses scripts/APIs for deterministic actions (validation, data loading)

## Success Criteria

Implementation is complete when:
1. User can type `[[[` in prompt editor and see autocomplete dropdown
2. Autocomplete shows all available snippets from manifest.json
3. User can navigate snippets with keyboard (arrows, enter, escape)
4. Preview panel shows snippet content when snippet is selected
5. Clicking or pressing Enter inserts snippet key at cursor
6. Toolbar button manually opens snippet picker
7. Save validates snippet keys and shows error dialog for invalid keys
8. All edge cases are handled gracefully
9. Feature works across supported browsers
10. Code is documented and maintainable
