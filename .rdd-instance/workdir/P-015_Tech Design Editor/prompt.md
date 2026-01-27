I need an editor of the `.rdd/config/technical-design-schema.json` with web interface.
It should be created with html, css and vanila JavaScript in a new folder "tech_design_schema_editor" in the repo root
The editor should be able to read and write `.rdd/config/technical-design-schema.json`
If needed, create a local web server to overcome the limitations of browser to manipulate files in the file system
The editor should be able to create new questions, edit the existing questions and delete questions from the current `.rdd/config/technical-design-schema.json`
The editor should be entirely independent from the scripts in .rdd and .rdd-instance folders
Copy the css for Technical Design page so to have same look and feel

**Objective**: Create a standalone web-based editor for managing the Technical Design schema file (`.rdd/config/technical-design-schema.json`) with full CRUD capabilities and validation.

**Context**:
- The Technical Design schema defines the questions, categories, and options shown in the RDD Framework's Technical Design page
- The schema structure is defined in P-001 implementation with categories, groups, questions, and conditional visibility rules
- This editor must be independent of the RDD framework runtime - it should work as a standalone tool that can be run separately
- The schema file is critical infrastructure - invalid schemas will break the Technical Design page

**Requirements**:

1. **Location & Independence**:
   - Create in folder: `tech_design_schema_editor/` at repository root
   - Must not depend on `.rdd/` or `.rdd-instance/` runtime scripts or files
   - Should work when run standalone, even if moved to a different location
   - Can be run by developers when they need to modify the schema via run_editor.bat and run_editor.sh files in `tech_design_schema_editor/`

2. **Technology Stack**:
   - Server: Python HTTP server (similar to `.rdd/src/web/server.py` pattern)
   - Frontend: HTML, CSS, vanilla JavaScript only
   - CSS: Extract relevant styles from Technical Design page (`.rdd/src/web/static/style.css`) for consistent look and feel
   - No external JavaScript libraries except for optional syntax highlighting

3. **Functionality**:
   - **Load Schema**: Read `.rdd/config/technical-design-schema.json` on startup
   - **Navigate**: Browse categories and questions with tree/sidebar navigation
   - **Create**: Add new categories, groups, and questions
   - **Edit**: Modify existing questions, options, help text, conditional rules
   - **Delete**: Remove categories, groups, or questions
   - **Validate**: Real-time validation of schema structure before save
   - **Save**: Write validated schema back to file with atomic write operation

4. **UI Layout**:
   - Two-panel layout:
     - Left sidebar: Tree navigation showing categories → groups → questions
     - Right panel: Form editor for selected item
   - Top toolbar: Save, Validate, Reload, Backup buttons
   - Status bar: Validation messages and save status

5. **Validation Requirements**:
   - Required fields present (id, label, type for questions)
   - Question IDs are unique across entire schema
   - Valid question types (radio, multiselect, dropdown, text, number, etc.)
   - Valid option structures for choice-based questions
   - Conditional visibility rules (`visibleWhen`) are syntactically valid
   - No circular dependencies in visibility rules

6. **Question Types to Support**:
   Based on the existing schema structure (from P-001):
   - `radio` - single selection from options
   - `multiselect` - multiple selections from options  
   - `dropdown` - single selection dropdown
   - `text` - free text input
   - `number` - numeric input
   - `textarea` - multi-line text
   - Support for `visibleWhen` conditional rules on any question

7. **Error Handling**:
   - Show validation errors inline with specific field references
   - Prevent saving invalid schemas
   - Create automatic backup before each save
   - Provide clear error messages for file system failures
   - Handle malformed JSON gracefully with recovery options

8. **Server API Endpoints**:
   - `GET /api/schema` - Load schema from file
   - `POST /api/schema` - Save schema to file (with validation)
   - `POST /api/validate` - Validate schema without saving
   - `POST /api/backup` - Create timestamped backup of current schema
   - `GET /` - Serve the editor HTML page

9. **Implementation Approach**:
   - Start with the Hybrid Approach (see Proposal 3 in analysis)
   - Two-panel layout with form-based editing
   - Text editor for `visibleWhen` rules with syntax highlighting
   - Bootstrap 5 for UI components (consistent with existing Web UI)
   - Atomic file writes (write to temp, then rename)

10. **Testing & Documentation**:
    - Include README.md in `tech_design_schema_editor/` with:
      - How to start the server
      - How to access the editor
      - Schema structure documentation
      - Validation rules
    - Manual testing checklist for CRUD operations
    - Example of adding a new category and question

**Acceptance Criteria**:
1. Server starts successfully and opens editor in browser
2. Can load existing schema without errors
3. Can create new category with questions
4. Can edit existing questions and options
5. Can delete questions and categories
6. Validation catches common errors (duplicate IDs, missing required fields)
7. Invalid schemas cannot be saved
8. Saved schemas can be loaded by Technical Design page without errors
9. UI is responsive and matches Technical Design page style
10. All operations provide clear user feedback (success/error messages)

**Out of Scope** (can be added later if needed):
- Drag-and-drop reordering
- Undo/redo functionality
- Visual rule builder for conditional logic (use text editor instead)
- Multi-language support
- Real-time collaboration

**Implementation Notes Required**:
- Document the schema validation rules implemented
- Explain the atomic write approach for file safety
- Document any limitations or known issues
- Provide examples of adding different question types