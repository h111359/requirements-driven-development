# Implementation: Remove filter by type in Tech Design page

## Context from specifications

### Technical Design
- Currently contains two answered questions about project scale
- Not directly relevant to this UI change

### Requirements  
- UR-0018: Web UI shall provide Technical Specification page with configuration-driven interactive form
- The current implementation has filters for type and status
- Removing type filter aligns with simplifying the UI

### Files and Folders
- Web UI is located in `.rdd/src/web/`
- Templates in `.rdd/src/web/templates/index.html`
- JavaScript in `.rdd/src/web/static/app.js`

### Prompt Registry Context
- P-001 initially implemented the Technical Design page with filters
- P-003 (current active prompt) takes precedence and requests removal of type filter

## Implementation Steps

### Step 1: Remove type filter dropdown from HTML
Removing the `<select>` element with id `tech-design-filter-type` from the filter bar in index.html.

**Files modified**: 
- `/home/hromar/Desktop/vscode/requirements-driven-development/.rdd/src/web/templates/index.html`

**Changes**:
- Removed the type filter dropdown (col-md-3 with select#tech-design-filter-type)
- Changed the status filter column width from col-md-3 to col-md-6 to maintain layout balance

### Step 2: Remove type filter logic from JavaScript
Removed all references to the type filter from the JavaScript filtering logic.

**Files modified**:
- `/home/hromar/Desktop/vscode/requirements-driven-development/.rdd/src/web/static/app.js`

**Changes in setupTechnicalDesignFilters()**:
- Removed `const filterType` variable declaration
- Removed event listener for filterType change

**Changes in applyTechnicalDesignFilters()**:
- Removed `const filterType` variable declaration
- Removed the type filter logic block that checked `if (filterType && question.type !== filterType)`
- Kept search and status filters intact

## Requirements Analysis

Reviewing existing requirements against this change:

**UR-0018**: "The Web UI shall provide a Technical Specification page enabling editing of technical-design using a configuration-driven interactive form."

The removal of the type filter does not conflict with UR-0018. The requirement specifies that there should be a Technical Specification page with an interactive form, but it does not mandate specific filtering capabilities. The page still provides:
- Search functionality
- Status filtering (answered/unanswered)
- Interactive form for editing

The change simplifies the UI by removing an unnecessary filter, making the interface cleaner while maintaining all core functionality required by UR-0018.

**Conclusion**: No requirement updates needed. The existing requirements are still satisfied.

## Summary

Successfully removed the type filter from the Technical Design page as requested. The page now has:
- Search bar (col-md-6)
- Status filter dropdown (col-md-6)

Both HTML template and JavaScript filtering logic have been updated to remove all traces of the type filter functionality.

