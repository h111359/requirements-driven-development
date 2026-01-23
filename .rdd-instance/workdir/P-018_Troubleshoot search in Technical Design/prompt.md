The search filed in Technical Design page is not working. 

**Root Cause:**
The search functionality in the Technical Design page is failing because the code in `applySearchFilter()` function (line 3514 in app.js) attempts to iterate over `category.groups`, but the schema was flattened in prompt P-007 ("Flatten categories content of Tech Design") which removed the groups structure entirely. Categories now directly contain a `questions` array instead of having a nested `groups` structure.

The console sais:
app.js:3517 Uncaught TypeError: Cannot read properties of undefined (reading 'forEach')
    at app.js:3517:25
    at Array.forEach (<anonymous>)
    at applySearchFilter (app.js:3514:33)
    at applyTechnicalDesignFilters (app.js:3478:5)
    at HTMLInputElement.<anonymous> (app.js:3455:9)

Troubleshoot, find the root cause. Implement the best fix. Test.

Beyond fixing search, audit entire app.js for any other references to removed schema structures.

Improved prompt:

**Context**:
- In prompt P-007, the Technical Design schema was flattened to remove the groups accordion structure
- Categories now directly contain `questions` arrays instead of nested `groups` structures
- The schema change was implemented in `.rdd/config/technical-design-schema.json`
- Normal category browsing was updated to work with the flattened structure
- However, the search functionality was not updated and is now broken

**Current Behavior**:
When typing in the search field on the Technical Design page, the following error appears in the browser console:
```
app.js:3517 Uncaught TypeError: Cannot read properties of undefined (reading 'forEach')
    at app.js:3517:25
    at Array.forEach (<anonymous>)
    at applySearchFilter (app.js:3514:33)
    at applyTechnicalDesignFilters (app.js:3478:5)
    at HTMLInputElement.<anonymous> (app.js:3455:9)
```

**Root Cause**:
The `applySearchFilter()` function at line 3514 in `.rdd/src/web/static/app.js` still attempts to iterate over `category.groups`, which no longer exists in the flattened schema.

**Expected Behavior**:
Search should filter questions across all categories based on matching text in:
- Question labels
- Question help text  
- Option labels

**Tasks**:
1. **Audit**: Search for all references to `category.groups` in `.rdd/src/web/static/app.js`
2. **Fix**: Update `applySearchFilter()` to iterate over `category.questions` directly
3. **Verify**: Check related functions `renderSearchResults()` and `renderFilteredCategoryList()` for schema assumptions
4. **Test**: Verify search works for:
   - Single-word searches
   - Multi-word searches
   - Searches matching labels, help text, and options
   - Search with no results
   - Clearing search filter

**Files to Modify**:
- `.rdd/src/web/static/app.js` (lines around 3514)

**Acceptance Criteria**:
- Search field accepts input without console errors
- Search correctly filters questions across all categories
- Matching questions are displayed with their category context
- "No results" message appears when search has no matches
- Clearing search returns to normal category view
- All test scenarios pass