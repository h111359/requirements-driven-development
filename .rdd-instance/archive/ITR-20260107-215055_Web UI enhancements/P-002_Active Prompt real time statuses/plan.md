# Implementation Plan: Active Prompt Real-Time Statuses

## Context

The Active Prompt page currently has a 2-second polling mechanism (`refreshActivePromptStatuses()`) that updates workflow status flag indicators (questionnaire-generated, questionnaire-answered, plan-generated, implementation-completed, executed). The file view buttons (Questionnaire, Analysis, Plan, Implementation, Modifications) only update their enabled/disabled states on initial page load. This plan extends the existing polling mechanism to also update file button states in real-time.

## Questionnaire Decisions

- **Q1**: Use registry flags only (no file existence checks) - consistent with framework design
- **Q2**: Update delete buttons in real-time alongside view buttons - for complete UX consistency
- **Q3**: Reuse existing `updateFileButtonStates()` function - follows DRY principle

## Implementation Steps

### Step 1: Locate and review the existing refresh mechanism

File: `.rdd/src/web/static/app.js`

Review the `refreshActivePromptStatuses()` function to understand:
- How it currently fetches registry data
- What status flags it updates
- How it handles errors
- The 2-second interval setup via `setInterval`

### Step 2: Review the updateFileButtonStates function

File: `.rdd/src/web/static/app.js`

Examine the `updateFileButtonStates()` function to understand:
- Which buttons it controls (file view buttons: Questionnaire, Analysis, Plan, Implementation, Modifications)
- Which delete buttons it controls (Questionnaire, Analysis, Plan delete buttons)
- How it determines button states from registry flags
- Current calling locations (page load only)

### Step 3: Extend refreshActivePromptStatuses to call updateFileButtonStates

File: `.rdd/src/web/static/app.js`

Modify the `refreshActivePromptStatuses()` function to:
- After successfully fetching and processing registry data
- After updating the status flag indicators
- Call `updateFileButtonStates(activePrompt)` passing the active prompt data
- This ensures file view buttons and delete buttons update every 2 seconds

The change will be minimal - adding one function call at the appropriate point in the refresh flow.

### Step 4: Test the real-time update behavior

Verification steps:
1. Open Active Prompt page in browser
2. Keep browser window open
3. In a separate terminal, execute action scripts that change registry flags:
   - `python .rdd/src/actions/prompt_questionnaire_generated_on.py` 
   - `python .rdd/src/actions/prompt_plan_generated_on.py`
   - `python .rdd/src/actions/prompt_implementation_completed_on.py`
4. Observe that within 2 seconds:
   - Status flag indicators update
   - File view buttons (Questionnaire, Plan, Implementation) become enabled/visible
   - Delete buttons become enabled when applicable
5. Test deletion scenarios:
   - Use Web UI delete buttons for questionnaire/plan
   - Verify buttons disable within 2 seconds after deletion
6. Test various workflow states to ensure correct button visibility

### Step 5: Verify no performance degradation

Performance checks:
- Monitor browser console for errors during refresh cycles
- Check network tab for API call timing (should remain ~100-200ms per refresh)
- Verify DOM update performance is smooth (no visible lag or flicker)
- Confirm 2-second interval remains consistent
- Test with slower machines/connections if available

### Step 6: Update requirements if needed

Check if existing requirements fully cover the implemented behavior:
- UR-0076 covers status flag indicators above execution mode buttons
- Need to verify if real-time file button updates are explicitly covered
- If not covered, add new requirement using:

```bash
python .rdd/src/actions/requirement_ur_create.py text="The Web UI Active Prompt page shall update file view button states (Questionnaire, Analysis, Plan, Implementation, Modifications) and their corresponding delete buttons in real-time via 2-second polling to reflect current workflow state from the work iteration registry"
```

Note: Review during implementation to determine if new requirement is necessary or if existing requirements sufficiently cover this behavior.

### Step 7: Update files-and-folders specification

File: `.rdd-instance/specifications/files-and-folders.md`

Verify that `app.js` is documented with updated description reflecting the real-time button state update mechanism. If description needs update, modify the entry for `.rdd/src/web/static/app.js` to mention:
- 2-second polling for status and button state updates
- Real-time synchronization with work iteration registry

### Step 8: Document the implementation

File: Will be auto-created as `implementation.md` during implement mode

This step will occur during implementation mode execution and will document:
- Exact code changes made to `refreshActivePromptStatuses()`
- Testing results and observations
- Any edge cases discovered
- Performance measurements
- Requirement updates performed

## Requirements Compliance

### Existing Requirements Observed

- **UR-0004**: Web UI provides modern, responsive interface with real-time feedback - extended by this change
- **UR-0076**: Status indicators positioned above execution mode buttons - mechanism being extended
- **UR-0093**: Delete buttons for execution mode outputs - state updates extended to real-time
- **UR-0094**: Delete buttons enabled only when generated flag is true - enforced in real-time
- **TR-0001**: Framework uses vanilla JavaScript - implementation maintains this constraint
- **TR-0063**: Web interface implemented using vanilla JavaScript, HTML, Bootstrap 5 - no framework dependencies added

### Potential New Requirement

During implementation, assess whether to add new requirement explicitly covering real-time file button updates (see Step 6 above). This would formalize the behavior as a framework capability rather than an implicit extension of existing real-time feedback requirements.

## Technical Design Updates

No technical design updates needed - the technical design file is currently empty and this implementation follows established patterns in the existing codebase.

## Files and Folders Updates

Update description for `.rdd/src/web/static/app.js` if needed to reflect enhanced real-time synchronization capabilities (see Step 7).

## Risk Assessment

**Low Risk Changes:**
- Reusing existing `updateFileButtonStates()` function eliminates new logic
- Single function call addition to existing refresh mechanism
- No API changes required
- No data model changes

**Potential Issues:**
- Performance impact from additional DOM updates every 2 seconds (mitigated by reusing existing efficient function)
- Browser compatibility with frequent updates (mitigated by already proven 2-second polling pattern)

**Mitigation:**
- Thorough testing across different prompt states
- Performance monitoring during development
- Fallback to page reload if issues detected
