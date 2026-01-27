# Implementation Plan: Troubleshoot search in Technical Design

## Overview
Fix the broken search functionality in the Technical Design page that fails with "Cannot read properties of undefined (reading 'forEach')" error. The issue stems from the schema flattening in P-007 where the `groups` structure was removed, but the search code was not updated.

## Step 1: Audit app.js for references to category.groups

Search the entire `.rdd/src/web/static/app.js` file for all occurrences of `category.groups` or similar patterns that assume the old nested schema structure.

**Actions**:
- Use grep or code search to find all instances of `.groups` in the Technical Design section of app.js
- Document the line numbers and functions affected
- Identify which functions need modification

**Expected findings**:
- `applySearchFilter()` function (around line 3514)
- Potentially `renderSearchResults()` function
- Potentially `renderFilteredCategoryList()` function
- Any other search-related utility functions

## Step 2: Fix applySearchFilter() function

Update the `applySearchFilter()` function to iterate directly over `category.questions` instead of `category.groups`.

**Current problematic code pattern**:
```javascript
category.groups.forEach(group => {
    group.questions.forEach(question => {
        // search logic
    });
});
```

**Target code pattern**:
```javascript
category.questions.forEach(question => {
    // search logic
});
```

**Actions**:
- Remove the outer loop over `category.groups`
- Adjust the search logic to work directly with questions
- Ensure question matching logic remains intact
- Verify that visibility filtering (`isQuestionVisible()`) is still called correctly

## Step 3: Verify and fix renderSearchResults() function

Check if `renderSearchResults()` assumes a groups structure and update if necessary.

**Actions**:
- Locate the function definition
- Review how it iterates over search results
- If it references groups, update to work with the flattened structure
- Ensure proper rendering of category context for search results
- Verify that the "no results" message displays correctly

## Step 4: Verify and fix renderFilteredCategoryList() function

Check if `renderFilteredCategoryList()` has any assumptions about the groups structure.

**Actions**:
- Locate the function definition
- Review its implementation
- Update any references to groups if found
- Ensure it correctly renders the category sidebar during search

## Step 5: Test search functionality with comprehensive test cases

Execute manual testing of all search scenarios listed in the prompt's acceptance criteria.

**Test Cases**:
1. **Single-word search**: Search for "security" - should match questions in Security category
2. **Multi-word search**: Search for "data retention" - should match relevant questions
3. **Label matching**: Verify search finds matches in question labels
4. **Help text matching**: Verify search finds matches in help text
5. **Option matching**: Verify search finds matches in option labels
6. **No results**: Search for "xyz123" - should show "no results" message
7. **Clear search**: Click clear button or delete search text - should restore full category view
8. **Cross-category search**: Enter generic term that appears in multiple categories - verify all matches shown

**For each test**:
- Verify no console errors appear
- Verify results are displayed correctly
- Verify category context is preserved
- Verify the UI responds as expected

## Step 6: Verify no other code paths reference removed structures

Perform a broader audit to ensure no other functionality relies on the old groups structure.

**Actions**:
- Search for any remaining references to `groups` in Technical Design functions
- Check related utility functions (`isQuestionVisible()`, etc.)
- Verify that the schema loading and validation code expects the flattened structure
- Document any findings

**Expected outcome**:
- Confirm that only search-related functions were affected
- Normal category browsing already works (uses `renderCategoryQuestions()` which correctly accesses `category.questions`)

## Step 7: Document the fix in implementation.md

Create detailed documentation of:
- Root cause analysis
- Functions modified
- Code changes made
- Test results
- Lessons learned

**Implementation log should include**:
- Before/after code snippets
- Test execution results
- Any edge cases discovered
- Confirmation that all acceptance criteria are met

## Requirements Review

After reviewing `.rdd-instance/specifications/requirements.md`, the following requirements are relevant to this fix:

**Existing requirements that apply**:
- **UR-0025**: "The Web UI shall provide a Technical Specification page for editing of technical-design" - This fix ensures the search feature works as part of the Technical Design page
- **UR-0027**: "Error messages shall include specific problem description and suggested remediation steps" - The current error is a raw stack trace; we're fixing it to prevent the error entirely
- **UR-0030**: "Scripts shall handle errors gracefully and provide recovery guidance" - While this applies to scripts, the principle extends to UI code handling unexpected states
- **TR-0195**: "The Web UI Technical Design page search functionality shall filter across all categories and questions simultaneously..." - This is the exact functionality being fixed

**No new requirements are needed** for this fix as it's correcting an oversight from P-007's schema flattening. The existing requirements already mandate proper search functionality.

**No modifications to existing requirements** are needed. The fix aligns with existing requirements without changing their intent or scope.

## Files and Folders Review

After reviewing `.rdd-instance/specifications/files-and-folders.md`:

**Files to be modified**:
- `.rdd/src/web/static/app.js` - The main JavaScript file containing the Technical Design page logic

**No changes needed to files-and-folders.md** as we're modifying existing files, not adding new ones.

## Technical Design Review

The technical design file (`.rdd-instance/specifications/technical-design.json`) is currently empty, so there are no architectural constraints or decisions that impact this fix.

## Plan Summary

This is a straightforward bug fix with clear scope:
1. Audit code for schema structure assumptions
2. Update 3-4 functions to work with flattened schema (removing groups references)
3. Test comprehensively across all search scenarios
4. Document the fix

**Estimated complexity**: Low
**Risk level**: Low - The fix is isolated to search functionality
**Testing requirement**: Manual testing with defined test cases

All steps follow the existing code patterns established in P-007 for normal category rendering, ensuring consistency across the Technical Design page implementation.
