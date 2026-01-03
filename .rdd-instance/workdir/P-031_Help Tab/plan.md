# Implementation Plan for P-031: Help Tab

## Overview
This plan implements a new Help tab in the Web UI that displays the user guide. The user guide will be completely recreated to provide clear, simple instructions for using the RDD framework through the Web UI.

## User Selections from Questionnaire
- **Q1**: Place Help tab at the end (after Files tab)
- **Q2**: Convert markdown to HTML on the server side 
- **Q3**: Include brief mentions of .rdd/ and .rdd-instance/ folders when relevant to user actions
- **Q4**: Web UI only - describe only how to use the web interface
- **Q5**: Multiple short workflow examples for different scenarios

## Implementation Steps

### Step 1: Recreate User Guide Content
Recreate `.rdd/docs/user-guide.md` with comprehensive but concise documentation focused on Web UI usage. The new guide will include:
- Introduction to RDD Framework and its purpose
- Quick start guide (installation and first steps)
- Multiple short workflow scenarios:
  - Creating and executing a simple prompt
  - Working with questionnaires
  - Using plan mode
  - Working with modifications
  - Completing prompts
- Web UI sections explanation (Active Prompt, Prompts History, Workdir, Files)
- Brief mentions of .rdd/ and .rdd-instance/ folder structure when relevant to user actions
- Troubleshooting common issues

The guide will avoid technical implementation details and focus on practical user workflows. It will be written in simple, clear language following a logical structure.

### Step 2: Add Server-Side Markdown Rendering
Modify `.rdd/src/web/server.py` to add:
- A new API endpoint `GET /api/help/user-guide` that reads `.rdd/docs/user-guide.md` and converts it to HTML using Python's markdown library
- Proper error handling if the markdown file is not found or cannot be read
- Content-Type header set to `application/json` with the HTML content in the response

### Step 3: Update HTML Template for Help Tab
Modify `.rdd/src/web/templates/index.html` to add:
- A new navigation tab "Help" after the "Files" tab in the navbar
- A new section `<div id="section-help">` that will display the rendered user guide
- The Help section will include a container div with proper Bootstrap styling for the rendered markdown content
- Initial loading state with a spinner while fetching the guide

### Step 4: Implement Help Tab JavaScript Functionality
Modify `.rdd/src/web/static/app.js` to add:
- A new `showSection('help')` case in the section display logic
- A function `loadUserGuide()` that fetches markdown from `/api/help/user-guide` endpoint and renders it in the Help section
- Call `loadUserGuide()` automatically when the Help tab becomes visible
- Error handling with user-friendly messages if loading fails
- Styling application for the rendered markdown content (headings, lists, code blocks, etc.)

### Step 5: Add CSS Styling for Help Content
Modify `.rdd/src/web/static/style.css` to add:
- Styling for the rendered markdown content to ensure proper spacing, typography, and readability
- Styles for headings (h1-h6), paragraphs, lists, code blocks, and links
- Responsive styling to ensure the guide displays well on different screen sizes
- Consistent styling with the rest of the Web UI theme

### Step 6: Update Requirements
Add new requirements to `.rdd-instance/specifications/requirements.md`:

```
- [UR-20260103-XXXX] The Web UI shall provide a Help tab that displays the user guide to assist users in understanding how to work with the RDD framework.

- [UR-20260103-XXXX] The user guide shall focus on practical Web UI workflows without exposing technical implementation details, providing multiple short workflow examples for different development scenarios.
```

Add new technical requirements:

```
- [TR-20260103-XXXX] The web server shall provide a GET /api/help/user-guide endpoint that reads `.rdd/docs/user-guide.md`, converts it to HTML using a Python markdown library, and returns the rendered HTML in JSON format.

- [TR-20260103-XXXX] The Help tab shall be positioned after the Files tab in the Web UI navigation bar and shall automatically load and display the rendered user guide when accessed.

- [TR-20260103-XXXX] The user guide markdown rendering shall be performed server-side using Python's markdown library to avoid client-side dependencies.
```

### Step 7: Update Files and Folders Specification
Update `.rdd-instance/specifications/files-and-folders.md` to document:
- `.rdd/docs/user-guide.md` - User guide documentation in markdown format displayed in the Web UI Help tab
- The Help tab implementation in the Web UI (index.html, app.js, style.css, server.py)

### Step 8: Testing
After implementation, verify:
- Help tab appears in navigation bar after Files tab
- Clicking Help tab loads and displays the user guide
- User guide content is properly formatted with headings, lists, and styling
- All links in the user guide work correctly
- The guide is readable and provides clear, actionable information
- Error handling works if the user guide file is missing
- Page loads quickly and markdown rendering is performant

## Files to be Modified
1. `.rdd/docs/user-guide.md` - Complete rewrite
2. `.rdd/src/web/server.py` - Add `/api/help/user-guide` endpoint
3. `.rdd/src/web/templates/index.html` - Add Help navigation tab and section
4. `.rdd/src/web/static/app.js` - Add Help tab display and loading logic
5. `.rdd/src/web/static/style.css` - Add styling for rendered markdown
6. `.rdd-instance/specifications/requirements.md` - Add new requirements
7. `.rdd-instance/specifications/files-and-folders.md` - Update documentation

## Dependencies
- Python markdown library (likely already available in standard library or will use simple implementation)
- Bootstrap CSS framework (already in use)
- No new external dependencies required
