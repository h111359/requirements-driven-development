In "Technical Design Schema Editor" enhance the part for setting conditional visibility of questions. The simple text field should be "Conditional Visibility (visibleWhen)" replaced with convenient input elements. 

If in Analyze mode - create in the prompt workdir a simple html file with examples of the different options to achieve the requested.

Improved prompt:

**Context**:
The Technical Design Schema Editor currently uses a plain textarea for configuring conditional visibility (`visibleWhen`), which requires users to manually write JSON expressions. This is error-prone and not user-friendly.

**Goal**:
Replace the `visibleWhen` textarea with a visual rule builder that makes it easy to create and manage visibility conditions without writing JSON manually.

**Requirements**:

1. **UI Component**: Create a condition builder interface with the following features:
   - Add/remove condition rows using + and - buttons
   - Each row contains three dropdowns:
     - Question selector (searchable, shows question labels with IDs)
     - Operator selector (equals, not equals, contains, not contains) - verify what are the current acceptable operators as per the existing functionality
     - Value selector (populated from the selected question's options)
   - AND-only logic between conditions (all conditions must be true)
   - Display count of active conditions
   - Show/hide toggle to collapse the builder when not in use

2. **Question Selector**: 
   - Populate from all questions in the schema
   - Show format: "Category: Question Label (QuestionID)"
   - The User should be able to select first the Category and based on their selection - to be able to select the question from a reduced list based on the Category selection
   - Include search/filter capability
   - Exclude the current question being edited

3. **Value Selector**:
   - For radio/dropdown: show all option labels
   - For multiselect: show all option labels (condition checks if array contains value)
   - For text/textarea/number: provide text input for free-form value
   - For checkbox: show "true" / "false" options

4. **Validation**:
   - Prevent circular references (Question A depends on Question B which depends on Question A)
   - Warn if referenced question doesn't exist
   - Warn if value doesn't match any options (for radio/dropdown/multiselect)
   - Highlight validation errors in red with clear messages

5. **Data Format**:
   - Store conditions as structured JSON array:
     ```json
     {
       "visibleWhen": [
         {"questionId": "Q1", "operator": "equals", "value": "Option1"},
         {"questionId": "Q2", "operator": "contains", "value": "Option2"}
       ]
     }
     ```

6. **Backward Compatibility**:
   - Support reading existing string expressions (legacy format)
   - Show legacy expressions in read-only textarea with warning message
   - Provide "Convert to Builder" button to attempt automatic conversion
   - If conversion fails, allow manual recreation in builder

7. **Auto-save**:
   - Maintain existing auto-save behavior
   - Save on blur events from dropdowns and inputs
   - Show saved indicator

8. **Analyze Mode Deliverable**:
   - Create an HTML demo file `conditional-visibility-demo.html` in the prompt workdir
   - Demo should show:
     - Example 1: Simple single condition (if Product Type = Mobile, show Mobile Platform question)
     - Example 2: Multiple AND conditions (if Cloud = Azure AND Region = US, show Compliance options)
     - Example 3: Multiselect contains check (if Features contains "AI/ML", show ML Platform question)
     - Include both the JSON format and a visual representation of each example
     - Provide code snippets for the UI components

**Out of Scope**:
- OR logic between conditions (future enhancement)
- Nested condition groups (future enhancement)
- Complex expressions with functions or calculations

**Success Criteria**:
- Users can create basic visibility rules without writing JSON
- Validation prevents common errors (invalid IDs, wrong values)
- Existing schemas with visibleWhen expressions continue to work
- Demo file clearly illustrates the different condition types