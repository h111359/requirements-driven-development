# Technical Design Schema Editor

A standalone web-based editor for managing the RDD Framework's technical design schema file.

## Overview

This editor provides a user-friendly interface for creating, editing, and managing the Technical Design schema file (`.rdd/config/technical-design-schema.json`). The schema defines the questions, categories, and options shown in the RDD Framework's Technical Design page.

**Key Features:**
- ✅ Full CRUD operations on categories and questions
- ✅ Reorder categories, questions, and options with up/down arrows
- ✅ Keyboard shortcuts (Alt+Up/Down) for quick reordering
- ✅ Real-time validation with detailed error messages
- ✅ Automatic backup creation before saves
- ✅ Two-panel layout with tree navigation
- ✅ Support for all question types (radio, multiselect, text, etc.)
- ✅ Conditional visibility rule editing
- ✅ Search and filter capabilities
- ✅ Completely independent from RDD runtime

## Quick Start

### Starting the Editor

**Linux/Mac:**
```bash
./run_editor.sh
```

**Windows:**
```
run_editor.bat
```

The editor will:
1. Start a local HTTP server on port 8765
2. Automatically open your default browser to http://localhost:8765
3. Load the schema from `../.rdd/config/technical-design-schema.json`

### Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## System Requirements

- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No external dependencies required

## Usage Guide

### Navigation

The editor uses a two-panel layout:

**Left Sidebar:**
- Tree view showing categories and questions
- Search box to filter questions
- "Expand All" / "Collapse All" toggle
- "+ Category" button to add new categories

**Right Panel:**
- Form editor for the selected category or question
- Changes are automatically saved as you type
- Validate and delete buttons available

### Working with Categories

**Create a new category:**
1. Click "+ Category" in the sidebar
2. Fill in the Category ID (use PascalCase, e.g., "Product", "Architecture")
3. Enter a display label
4. Optionally add a description
5. Changes are saved automatically

**Edit an existing category:**
1. Click the category name in the sidebar
2. Modify the fields
3. Changes are saved automatically

**Delete a category:**
1. Select the category
2. Click "🗑️ Delete Category"
3. Confirm the deletion (this will also delete all questions in the category)

**Reorder categories:**
1. Click the ↑ (up) or ↓ (down) arrow buttons next to a category name
2. Or select a category and use Alt+Up or Alt+Down keyboard shortcuts
3. Changes are saved automatically

### Working with Questions

**Add a question to a category:**
1. Select the category in the sidebar
2. Click "+ Add Question"
3. Fill in the question details:
   - **Question ID**: Unique identifier (use `CategoryName_QuestionName` format)
   - **Label**: The question text shown to users
   - **Type**: Select the question type (radio, multiselect, text, etc.)
   - **Help Text**: Optional additional context
   - **Conditional Visibility**: JavaScript expression for when to show this question
4. If using radio/multiselect/dropdown, add options
5. Changes are saved automatically

**Edit a question:**
1. Click the question in the sidebar
2. Modify the fields
3. Changes are saved automatically

**Delete a question:**
1. Select the question
2. Click "🗑️ Delete Question"
3. Confirm the deletion

**Reorder questions:**
1. Click the ↑ (up) or ↓ (down) arrow buttons next to a question name
2. Or select a question and use Alt+Up or Alt+Down keyboard shortcuts
3. Changes are saved automatically

### Question Types

The editor supports the following question types:

- **radio**: Single choice from a list of options (radio buttons)
- **multiselect**: Multiple choices from a list (checkboxes)
- **dropdown**: Single choice from a dropdown menu
- **text**: Short text input (single line)
- **textarea**: Long text input (multiple lines)
- **number**: Numeric input
- **checkbox**: Boolean yes/no choice

### Answer Options

For questions with types `radio`, `multiselect`, or `dropdown`:

1. Each option needs an **ID** and **Label**
2. Click "+ Add Option" to add more options
3. Use the ↑↓ arrow buttons to reorder options
4. Use the 🗑️ button to delete an option
5. Enable "Allow Other" to let users enter custom text

### Keyboard Shortcuts

The editor supports keyboard shortcuts for efficient editing:

- **Alt+Up**: Move the currently selected category or question up
- **Alt+Down**: Move the currently selected category or question down

These shortcuts work when viewing a category or question in the editor panel.

### Conditional Visibility

Questions can be shown or hidden based on answers to other questions using the `visibleWhen` field.

**Syntax:**
```javascript
answers["OtherQuestion_ID"] === "DesiredValue"
```

**Examples:**
```javascript
// Show when Product category is "Mobile application"
answers["Product_PrimaryProductCategory"] === "Mobile application"

// Show when deployment is Cloud
answers["Deployment_TargetEnvironment"] === "Cloud"

// Complex condition with multiple checks
answers["Security_DataSensitivity"] === "High" && answers["Product_External"] === true
```

**Important:** The visibleWhen expression is a JavaScript expression that has access to the `answers` object.

### Validation

The editor validates the schema structure:

**Automatic validation:**
- Checks for required fields (ID, label, type)
- Ensures question IDs are unique across the entire schema
- Validates question types are valid
- Verifies options exist for choice-based questions
- Checks option IDs are unique within a question

**Manual validation:**
Click the "✓ Validate" button in the top toolbar to validate without saving.

**Validation errors** will be shown in a dialog with specific details about what needs to be fixed.

### Saving Changes

Changes are **automatically saved** as you edit:
- When you modify category or question fields, changes are saved immediately
- The status bar shows "Saving..." during save and "Saved" when complete
- Automatic backups are created in `./backups/` before each save
- The save operation uses atomic writes to prevent data corruption

**Note:** You can press Enter in form fields to trigger validation and save immediately.

### Backups

**Automatic backups:**
- Created automatically before each save
- Stored in `./backups/` with timestamp
- Format: `technical-design-schema_YYYYMMDD_HHMMSS.json`

**Manual backups:**
Click "📦 Backup" in the top toolbar to create a backup without saving.

### Reloading

Click "🔄 Reload" to reload the schema from the file system.

## Schema Structure

The schema file has this structure:

```json
{
  "title": "Technical Design Questionnaire",
  "description": "...",
  "categories": [
    {
      "id": "CategoryID",
      "label": "Category Display Name",
      "description": "Optional category description",
      "questions": [
        {
          "id": "Category_QuestionID",
          "label": "Question text",
          "type": "radio",
          "help": "Optional help text",
          "options": [
            {
              "id": "option1",
              "label": "Option 1"
            }
          ],
          "allowOther": true,
          "otherPlaceholder": "Please specify...",
          "visibleWhen": "answers['Other_Question'] === 'value'"
        }
      ]
    }
  ]
}
```

## Validation Rules

The editor enforces these rules:

1. **Schema must be valid JSON**
2. **Required top-level fields:**
   - `categories` (array)

3. **Category requirements:**
   - `id` (unique across categories)
   - `label`
   - `questions` (array, can be empty)

4. **Question requirements:**
   - `id` (unique across ALL questions in the schema)
   - `label`
   - `type` (must be one of: radio, multiselect, dropdown, text, textarea, number, checkbox)

5. **For radio/multiselect/dropdown questions:**
   - Must have `options` array
   - Must have at least one option
   - Each option must have `id` or `label`
   - Option IDs must be unique within the question

6. **visibleWhen (if present):**
   - Must be an array of condition objects
   - Each condition must have:
     - `questionId` (string): ID of the question to check
     - `equals` (array of strings): Values that make this question visible
   - Multiple conditions in array = AND logic (all must match)
   - Multiple values in `equals` = OR logic (any can match)
   - Example:
     ```json
     "visibleWhen": [
       {
         "questionId": "Product_Category",
         "equals": ["WebApp", "MobileApp"]
       }
     ]
     ```

## Tips and Best Practices

1. **ID Naming Convention:**
   - Categories: Use PascalCase (e.g., `Product`, `Architecture`, `DataManagement`)
   - Questions: Use `CategoryName_QuestionName` format (e.g., `Product_PrimaryCategory`)
   - Options: Use descriptive IDs (e.g., `CloudNative`, `OnPremise`)

2. **Create backups before major changes:**
   - Click "📦 Backup" before restructuring categories
   - Backups are in `./backups/` directory

3. **Test your changes:**
   - Use the "✓ Validate" button to check for errors
   - Reload the Technical Design page after saving to verify rendering

4. **Keep questions focused:**
   - One concept per question
   - Use help text for additional context
   - Break complex questions into multiple simpler ones

5. **Use conditional visibility wisely:**
   - Only show questions when relevant
   - Test the logic carefully
   - Avoid circular dependencies

## Troubleshooting

**Problem: Cannot connect to server**
- Solution: Make sure the server is running on port 8765. Check if another application is using that port.

**Problem: Schema file not found**
- Solution: The editor expects the schema at `../.rdd/config/technical-design-schema.json`. Make sure you're running the editor from the `tech_design_schema_editor` directory.

**Problem: Changes not saving**
- Solution: Check the browser console (F12) for errors. Make sure you have write permissions to the schema file.

**Problem: Validation errors after editing**
- Solution: Click "✓ Validate" to see specific errors. Fix the issues and changes will be saved automatically.

**Problem: Browser doesn't open automatically**
- Solution: Manually open http://localhost:8765 in your browser.

## Architecture

The editor consists of:

**Server (server.py):**
- Python HTTP server with REST API
- Endpoints:
  - `GET /api/schema` - Load schema
  - `POST /api/schema` - Save schema with validation
  - `POST /api/validate` - Validate without saving
  - `POST /api/backup` - Create backup
  - `GET /api/backup/list` - List backups
- Atomic file writes for data safety

**Frontend (index.html, static/*):**
- Vanilla JavaScript (no external libraries)
- Two-panel layout with tree navigation
- Form-based editing
- Client-side validation before save
- Search and filter capabilities

## Independence

This editor is **completely independent** from the RDD framework runtime:

- No dependencies on `.rdd/` scripts
- No dependencies on `.rdd-instance/` files
- Can be moved to a different location
- Works standalone with just Python 3

The only connection is reading/writing the schema file at `../.rdd/config/technical-design-schema.json`.

## Development

To extend the editor:

1. **Add new question type:**
   - Update `validate_schema_data()` in server.py
   - Add to dropdown in index.html
   - Update `handleQuestionTypeChange()` in app.js

2. **Add new validation rule:**
   - Update `validate_schema_data()` or `validate_question()` in server.py

3. **Modify UI layout:**
   - Edit index.html and static/style.css

## License

This editor is part of the RDD Framework and follows the same license (MIT).
