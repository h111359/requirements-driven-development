# P-024 Implementation Log: Enhance value selection in Conditional Visibility

## Execution Context
- **Prompt ID**: P-024
- **Prompt Title**: Enhance value selection in Conditional Visibility part of Technical Design Schema
- **Execution Mode**: Implementation
- **Date Started**: 2026-01-24

## Objective
Enhance the value field in the conditional visibility builder to provide convenient value selection for questions with predefined options (radio, multiselect, dropdown). Instead of manual text input, users should be able to select from available options of the referenced question.

## Questionnaire Decisions
The user has provided clear guidance via questionnaire responses:
1. **Q1 (UI Component Type)**: User selected "A" - Simple dropdown for option selection
2. **Q2 (Free-text questions behavior)**: User selected "A" - Keep simple text input (current behavior)
3. **Q3 (Display vs Store)**: User selected "C" - Display option labels but store option IDs
4. **Q4 (Multiselect value handling)**: User selected "B" - Allow selecting multiple values with OR semantics (differs from recommended "A")

## Technical Context
- **Technical Design Status**: Currently empty JSON object (`{}`)
- **Requirements**: 48 user requirements define the framework, with UR-0024 specifically requiring conditional/hierarchical logic in technical design
- **Files and Folders**: Contains tech_design_schema_editor folder with server.py and static/app.js

## Implementation Steps

### Step 1: Understanding Current Implementation
**Status**: Complete

The conditional visibility builder in tech_design_schema_editor/static/app.js currently:
- Allows creating multiple condition rows
- Each row has: Category selector → Question selector → Operator selector → Value input
- Value field is a plain text input (type="text")
- Operators vary by question type (radio/dropdown use equals/notEquals, multiselect uses contains/notContains, etc.)
- Current function `createConditionRow()` at line 1049 handles value field creation

**Relevant Files**:
- tech_design_schema_editor/static/app.js - Main client-side logic
- tech_design_schema_editor/static/style.css - UI styling
- tech_design_schema_editor/index.html - HTML markup

### Step 2: Implementation Plan (Based on Questionnaire)

Following the questionnaire decisions, the implementation will:

1. **For questions WITH predefined options** (radio, dropdown, multiselect):
   - Replace plain text input with a dropdown showing option labels
   - Store the corresponding option IDs in the condition value
   - Display logic: Show labels to user, Store IDs internally (Q3 decision: "C")

2. **For questions WITHOUT predefined options** (text, textarea, number):
   - Keep current text input behavior (Q2 decision: "A")
   - No changes needed for free-text questions

3. **For multiselect questions** (Q4 decision: "B"):
   - Allow users to select multiple values in the value field
   - Use OR semantics (if any of the selected values match)
   - Multiple selected values will be stored as an array in the condition

### Step 3: Code Changes Required

**File**: tech_design_schema_editor/static/app.js

#### 3.1 Add helper function to get options for a question
Need to add function to retrieve the options array for a referenced question:
```javascript
function getOptionsForQuestion(questionId) {
  // Find question in schema and return its options array
}
```

#### 3.2 Modify `createConditionRow()` function
- Add logic to detect if referenced question has predefined options
- For option-based questions: generate dropdown with option labels instead of text input
- For free-text questions: keep current text input behavior

#### 3.3 Update value handling
- When rendering: convert stored option IDs back to option labels for display
- When saving: convert selected labels back to option IDs
- For multiselect: handle array of IDs

#### 3.4 Update event handlers
- Modify value field change handlers to handle dropdown vs text input

### Step 4: CSS Updates (If Needed)
May need to add CSS for dropdown styling if using custom styles

## Implementation Progress

### Completed Changes

#### Step 3.1: Added Helper Functions (app.js - before renderConditionRows)

Added four new helper functions to support dynamic value field selection:

1. **getOptionsForQuestion(questionId)** - Retrieves the options array for a question and normalizes it to {id, label} format
2. **getQuestionById(questionId)** - Finds and returns a question object by its ID
3. **hasOptionsQuestion(questionId)** - Checks if a question has predefined options and is of type radio/dropdown/multiselect
4. **renderConditionRows()** - Existing function (no changes), now works with enhanced createConditionRow

**Location**: tech_design_schema_editor/static/app.js, lines ~1049-1096

#### Step 3.2: Modified createConditionRow() Function

Enhanced the value field generation (lines ~1127-1165):
- **For option-based questions** (radio, dropdown, multiselect):
  - Creates `<select>` element showing option labels
  - Stores option IDs as values (Q3 decision: "C" - Display labels, store IDs)
  - For multiselect questions: Creates multiple-select dropdown with helper text "Select one or more values (OR logic)"
  - For single-select questions (radio/dropdown): Creates single-select dropdown

- **For free-text questions** (text, textarea, number):
  - Keeps existing text input behavior
  - Supports array values (displays as JSON if value is array)

**Key change**: Value field type now depends on question type, implementing Q2 decision "A" and Q3 decision "C"

#### Step 3.3: Updated Event Listeners in createConditionRow

Modified event listener attachment (lines ~1167-1193):
- Added detection for three types of value fields:
  - `.condition-value-multiselect` - Multiple select dropdown
  - `.condition-value-select` - Single select dropdown  
  - `.condition-value-input` - Text input
- Routes events to appropriate handlers based on field type

#### Step 3.4: Added New Event Handler Functions

Added two new handler functions (after handleConditionOperatorChange):

1. **handleConditionValueChangeSelect(event, index)**
   - Handles single-select dropdowns for radio/dropdown questions
   - Stores the selected option ID directly
   - Follows Q1 decision: "A" (Simple dropdown)

2. **handleConditionValueChangeMultiselect(event, index)**
   - Handles multiple-select dropdowns for multiselect questions
   - Stores selected values as an array of option IDs
   - Follows Q4 decision: "B" (Allow selecting multiple values)
   - Array support enables OR logic (if any selected value matches)

### Implementation Details

**Questionnaire Compliance**:
- ✅ Q1 "UI Component Type": Implemented simple dropdown selector (User choice: "A")
- ✅ Q2 "Free-text behavior": Keep text input (User choice: "A")
- ✅ Q3 "Display vs Store": Display option labels, store option IDs (User choice: "C")
- ✅ Q4 "Multiselect values": Support multiple value selection with OR logic (User choice: "B")

**Technical Implementation**:
- Helper functions enable dynamic field type detection at render time
- Graceful fallback to text input if options not available
- Proper escaping of special characters in HTML
- JSON.stringify support for array values in text display
- Clean separation between label display and ID storage

### Files Modified
- **tech_design_schema_editor/static/app.js**:
  - Added: getOptionsForQuestion, getQuestionById, hasOptionsQuestion
  - Modified: renderConditionRows (added helper functions before it)
  - Modified: createConditionRow (enhanced value field creation)
  - Modified: Event listeners in createConditionRow (added multiselect handlers)
  - Added: handleConditionValueChangeSelect, handleConditionValueChangeMultiselect

### Testing Recommendations

The implementation should be tested with the following scenarios:
1. Create a question with predefined options (radio/dropdown)
2. Create a multiselect question with multiple options
3. Create a conditional visibility rule using these questions
4. Verify dropdown appears for option-based questions
5. Verify text input appears for free-text questions
6. Verify multiselect dropdown works with multiple selections
7. Verify stored values are option IDs (not labels)
8. Verify labels display correctly in the dropdowns

### No Requirement Changes Required

The implementation is self-contained within the technical design editor and does not require updates to:
- User Requirements (no framework-level requirements changes)
- Technical Requirements (no new technical requirements)
- Technical Design (empty JSON - schema-driven approach doesn't apply here)

The enhancement directly implements the prompt objective: "The form should give the user a convenient way to select the value, not to write it."

## Execution Completion

**Post-Implementation Actions Executed**:
1. ✅ python .rdd/src/actions/prompt_set_executed_on.py
   - Output: P-024 executed=true

2. ✅ python .rdd/src/actions/prompt_implementation_completed_on.py
   - Output: SUCCESS: implementation-completed set to True for prompt 'P-024'

3. ✅ python .rdd/src/actions/prompt_set_execution_mode.py mode=no-action
   - Output: SUCCESS: execution-mode set to 'no-action' for prompt 'P-024'

**Status**: Implementation complete and registered in framework registry

