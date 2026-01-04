# Implementation Plan - P-042: Active Prompt Page Design Change

## Overview

This plan details the implementation steps to reorganize button layout, standardize button colors to blue, remove execution mode success messages, and add automatic execution mode setting when modifications are created.

## Questionnaire Answers Summary

Based on the answered questionnaire:
- **Q1**: Use Bootstrap primary blue (#0d6efd) for all buttons
- **Q2**: All buttons (action and execution mode) should use the same blue color
- **Q3**: Set execution mode to modification immediately when API call succeeds
- **Q4**: Remove the showAlert call completely for execution mode changes
- **Q5**: Position Complete button at the far right end of the entire banner
- **Q6**: Position Mod button after both execution mode buttons and their workflow flag icons

## Implementation Steps

### Step 1: Restructure HTML Layout for Button Positioning

**File**: `.rdd/src/web/templates/index.html`

**Changes**:
- Modify the sticky-controls-panel div structure from two-column layout (col-md-4, col-md-8) to a flexbox layout with three regions
- Region 1: New button (left)
- Region 2: Execution mode buttons with workflow flags (center, flex-grow)
- Region 3: Mod and Complete buttons (right)

**Specific HTML modifications**:
```html
<!-- Replace the current row/col structure around line 115-240 -->
<div class="sticky-controls-panel">
    <div class="d-flex gap-2 align-items-center">
        <!-- Region 1: New Button -->
        <div>
            <button class="btn btn-sm btn-primary" onclick="showCreatePromptModal()" title="Create New Prompt">
                <i class="bi bi-plus-circle"></i> New
            </button>
        </div>
        
        <!-- Region 2: Execution Mode Buttons (flex-grow) -->
        <div class="flex-grow-1">
            <div class="d-flex gap-1 flex-wrap justify-content-center">
                <!-- All execution mode buttons with their flags -->
                <!-- (No Action, Clarify, Analyze, Plan, Implement, Modification) -->
            </div>
        </div>
        
        <!-- Region 3: Workflow Action Buttons (right) -->
        <div class="d-flex gap-1">
            <button class="btn btn-sm btn-primary" id="add-modification-btn" onclick="showAddModificationModal()" disabled title="Add Modification">
                <i class="bi bi-plus-circle"></i> Mod
            </button>
            <button class="btn btn-sm btn-primary" id="complete-prompt-btn" onclick="completeActivePrompt()" disabled title="Complete Prompt">
                <i class="bi bi-check-lg"></i> Complete
            </button>
        </div>
    </div>
</div>
```

**Rationale**: This three-region layout provides clear visual separation, ensures Complete button is at the far right, positions Mod after execution modes, and maintains responsive behavior through flexbox.

### Step 2: Update Button CSS Classes to Use Primary Blue

**File**: `.rdd/src/web/templates/index.html`

**Changes**:
- Change all button classes from their current colors to `btn-primary`
- Update execution mode button labels from `btn-outline-secondary` to `btn-primary`
- Ensure active state styling is maintained through Bootstrap's `.btn-check` mechanism

**Specific changes**:
- New button: Change from `btn-success` to `btn-primary`
- Mod button: Already `btn-primary`, keep as is
- Complete button: Change from `btn-success` to `btn-primary`
- All execution mode labels: Change from `btn-outline-secondary` to `btn-primary`

**Example for execution mode buttons**:
```html
<!-- Before -->
<label class="btn btn-outline-secondary btn-sm" for="mode-clarify" onclick="updateExecutionMode('clarify')">
    Clarify
</label>

<!-- After -->
<label class="btn btn-primary btn-sm" for="mode-clarify" onclick="updateExecutionMode('clarify')">
    Clarify
</label>
```

**Rationale**: Using `btn-primary` for all buttons creates the consistent blue appearance requested. Bootstrap's button-check pattern will automatically style the active mode differently.

### Step 3: Add Custom CSS for Active Execution Mode Visual Distinction

**File**: `.rdd/src/web/static/style.css`

**Changes**:
- Add CSS rules to ensure active execution mode button is visually distinct even though all buttons are now blue
- Use box-shadow or darker shade to indicate active state

**New CSS rules to add**:
```css
/* Enhanced active state for execution mode buttons */
.btn-check:checked + .btn-primary {
    background-color: #0a58ca; /* Darker blue for active state */
    border-color: #0a58ca;
    box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.5);
}

/* Ensure execution mode buttons have proper hover state */
.btn-primary:hover {
    background-color: #0b5ed7;
    border-color: #0a58ca;
}
```

**Rationale**: This ensures users can still clearly see which execution mode is active, despite all buttons being blue.

### Step 4: Remove Success Alert from updateExecutionMode Function

**File**: `.rdd/src/web/static/app.js`

**Changes**:
- Locate the `updateExecutionMode` function (around line 727)
- Remove the `showAlert('success', ...)` call
- Keep error alert handling intact

**Current code** (approximately line 747):
```javascript
if (result.success) {
    showAlert('success', `Execution mode set to: ${mode}`);
    await loadRegistry();
} else {
    showAlert('danger', 'Failed to update execution mode: ' + (result.error || result.stderr));
}
```

**Modified code**:
```javascript
if (result.success) {
    // Silent success - visual feedback from button state is sufficient
    await loadRegistry();
} else {
    showAlert('danger', 'Failed to update execution mode: ' + (result.error || result.stderr));
}
```

**Rationale**: Per questionnaire answer Q4, success messages should be removed completely, relying on visual feedback from the radio button state change.

### Step 5: Implement Automatic Execution Mode Setting After Modification Creation

**File**: `.rdd/src/web/static/app.js`

**Changes**:
- Locate the `addModification` function
- After successful modification creation, immediately call `updateExecutionMode('modification')`
- This should happen right after the API call succeeds, before modal close

**Current flow** (approximate):
```javascript
async function addModification() {
    // ... validation code
    const result = await executeAction('modification', 'create', params);
    if (result.success) {
        showAlert('success', 'Modification created successfully');
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('addModificationModal'));
        modal.hide();
        // Reload modifications
        await loadModifications();
    }
}
```

**Modified flow**:
```javascript
async function addModification() {
    // ... validation code
    const result = await executeAction('modification', 'create', params);
    if (result.success) {
        showAlert('success', 'Modification created successfully');
        // Immediately set execution mode to modification
        await updateExecutionMode('modification');
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('addModificationModal'));
        modal.hide();
        // Reload modifications
        await loadModifications();
    }
}
```

**Rationale**: Per questionnaire answer Q3 (option A), the execution mode should be set immediately when the API call succeeds, providing instant workflow continuity.

### Step 6: Update CSS for Responsive Behavior

**File**: `.rdd/src/web/static/style.css`

**Changes**:
- Add media query rules to handle button wrapping on smaller screens
- Ensure gap spacing is maintained when buttons wrap
- Verify sticky-controls-panel maintains proper spacing

**New CSS rules to add**:
```css
/* Responsive behavior for control panel */
@media (max-width: 768px) {
    .sticky-controls-panel .d-flex {
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .sticky-controls-panel > div > div:last-child {
        width: 100%;
        justify-content: center;
        margin-top: 0.5rem;
    }
}
```

**Rationale**: Ensures the new three-region layout remains usable on tablet and mobile devices.

### Step 7: Test and Verify All Changes

**Testing checklist**:
1. Verify Complete button appears at far right of control panel
2. Verify Mod button appears after execution mode buttons and before Complete
3. Verify all buttons (New, Mod, Complete, all execution modes) display in blue
4. Verify active execution mode is still visually distinguishable
5. Verify no success message appears when changing execution mode
6. Verify error messages still appear if execution mode change fails
7. Verify creating a modification automatically sets execution mode to "modification"
8. Verify layout is responsive on different screen sizes
9. Verify workflow flags still appear above appropriate execution mode buttons
10. Verify tooltips still work correctly

### Step 8: Update Implementation Documentation

**File**: `.rdd-instance/workdir/P-042_Active Prompt page design chage/implementation.md`

**Changes**:
- Document all file modifications made
- Record exact line numbers changed
- Note any unexpected issues encountered
- Confirm all questionnaire requirements were met

## Requirements Impact Assessment

### Requirements Changes: NONE REQUIRED

**Rationale**: As analyzed during the clarify phase, all changes are implementation refinements of existing functionality:

1. **Button repositioning** falls under existing requirement UR-20251224-0904 for "a modern, responsive interface"
2. **Color standardization** is covered by UR-20251224-0904 for "color-coded status indicators"
3. **Silent mode changes** align with UR-20251224-0935 for "graceful handling of errors with informative messages"
4. **Automatic mode setting** is a workflow enhancement of existing modification requirements (UR-20260101-1610 through UR-20260101-1617)

The existing requirements provide sufficient coverage. No new requirement rows need to be added to `.rdd-instance/specifications/requirements.md`.

### Technical Design Changes: NONE REQUIRED

No changes to `.rdd-instance/specifications/technical-design.json` are needed as these are UI implementation details, not architectural or technical design decisions.

### Files and Folders Changes: NONE REQUIRED

No changes to `.rdd-instance/specifications/files-and-folders.md` are needed as no new files are being created or removed.

## Files to be Modified

1. **`.rdd/src/web/templates/index.html`**
   - Restructure sticky-controls-panel layout (Step 1)
   - Update button CSS classes to btn-primary (Step 2)

2. **`.rdd/src/web/static/style.css`**
   - Add active state distinction CSS (Step 3)
   - Add responsive layout rules (Step 6)

3. **`.rdd/src/web/static/app.js`**
   - Remove success alert from updateExecutionMode (Step 4)
   - Add automatic mode setting to addModification (Step 5)

## Success Criteria

Implementation is complete when:
1. ✓ Complete button is positioned at the far right edge of the control panel
2. ✓ Mod button is positioned after execution mode buttons and workflow flags
3. ✓ All buttons use Bootstrap primary blue color (#0d6efd)
4. ✓ Active execution mode remains visually distinguishable
5. ✓ No success message displays when changing execution mode
6. ✓ Error messages still display for failed mode changes
7. ✓ Creating a modification automatically sets execution mode to "modification"
8. ✓ Layout remains responsive and functional on all screen sizes

## Estimated Complexity

- **Technical Complexity**: Low to Medium
- **Time Estimate**: 1-2 hours for implementation and testing
- **Risk Level**: Low (pure UI changes, no backend logic affected)

## Notes

- The three-region flexbox layout is preferred over the two-column Bootstrap grid for better control over button positioning
- Bootstrap's `.btn-check` pattern automatically handles active state for radio buttons, but custom CSS enhances the visual distinction
- Immediate automatic mode setting (Q3 option A) provides better UX than waiting for modal close, as it gives instant feedback
- All changes maintain backward compatibility with existing functionality
