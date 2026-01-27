# Analysis: Tech Design Editor

## Copilot Review

### Assessment of the Request

The prompt requests a standalone web-based editor for `.rdd/config/technical-design-schema.json` with the following characteristics:

**Strengths:**
- Clear deliverable: HTML/CSS/vanilla JavaScript editor in `tech_design_schema_editor` folder
- Well-defined scope: CRUD operations on the schema file
- Independence requirement is explicit
- UI consistency requirement (copy CSS from Technical Design page)

**Weaknesses and Risks:**

1. **Browser File System Limitations**: The prompt mentions "create a local web server to overcome the limitations of browser to manipulate files" but doesn't specify the server technology or architecture. Browsers cannot directly read/write to the file system without user interaction (File API) or a server component.

2. **Incomplete Specification**: 
   - No mention of validation requirements for the schema
   - No specification of how to handle schema versioning or migrations
   - No error handling requirements
   - No guidance on whether to support conditional visibility rules editing
   - No specification of the UI layout structure

3. **Independence vs. CSS Copying Contradiction**: The prompt says "entirely independent" but also says "copy the CSS for Technical Design page." The Technical Design page uses Bootstrap 5 and custom styles. Copying CSS creates a hidden dependency - if the schema structure changes, the editor's CSS might become outdated.

4. **Schema Complexity**: Based on P-001's implementation, the schema is complex with:
   - Multiple categories and groups
   - Various question types (radio, multiselect, dropdown, text, etc.)
   - Conditional visibility rules (`visibleWhen`)
   - No versioning mechanism
   
   Creating a comprehensive editor for all these features is a significant undertaking.

5. **Testing Strategy**: No mention of testing approach or requirements for the editor.

6. **Missing Context**:
   - Should the editor validate question IDs for uniqueness?
   - Should it prevent breaking changes to the schema?
   - Should it support undo/redo?
   - Should it provide schema backup/restore?

### Impact on Existing Functionality

**Low Risk of Breaking Changes:**
- The editor is independent and doesn't modify existing RDD framework code
- It operates on `.rdd/config/technical-design-schema.json` which is read-only for the Technical Design page
- No integration with existing Python scripts or Web UI server

**Potential Issues:**
- If the editor creates an invalid schema, it will break the Technical Design page rendering
- No validation layer between editor and schema consumers
- Schema changes won't be tracked in git history unless user commits manually

### Completeness Assessment

The prompt description is **incomplete** for production-quality implementation. It covers the "what" (CRUD editor) but lacks critical details about:
- Validation rules
- Error handling
- Schema structure documentation
- User experience details beyond "convenient"
- Server architecture specifics
- Security considerations (if using a local server)

**Risk Level: MEDIUM-HIGH** - The implementation could work but might create invalid schemas or poor user experience without additional clarification.

---

## Best Practices

### Web-Based Schema Editors

I cannot perform live internet searches via MCP in this environment. However, based on general best practices for web-based JSON schema editors:

**General Best Practices:**

1. **JSON Schema Validation**:
   - Use JSON Schema standard (draft-07 or later) to define valid schema structure
   - Implement real-time validation with clear error messages
   - Provide schema documentation inline with editing

2. **Editor UX Patterns**:
   - Tree-based navigation for hierarchical structures
   - Form-based editing for structured data
   - JSON view toggle for advanced users
   - Search/filter capabilities
   - Undo/redo support
   - Auto-save with conflict detection

3. **File System Access**:
   - **Browser File System Access API**: Modern browsers support this for local file operations, but requires user interaction for security
   - **Local HTTP Server**: Python http.server or Node.js Express for file operations
   - **Electron/Tauri**: For true desktop app with full file access (overkill for this use case)

4. **Conditional Logic Editing**:
   - Visual rule builders for non-technical users
   - Text-based editor with syntax highlighting for developers
   - Expression validation before save
   - Visual indicators showing which fields depend on others

5. **Data Integrity**:
   - Atomic file writes (write to temp file, then rename)
   - Schema backup before modifications
   - Validation before save
   - Changelog/history tracking

### Relevant Technologies

**For Local Web Server**:
- Python's `http.server` with custom handlers (consistent with existing RDD Web UI)
- Flask/FastAPI for more robust API (adds dependencies)
- Node.js Express (requires Node.js dependency)

**For Frontend**:
- Vanilla JavaScript with Web Components for modularity
- Monaco Editor (VS Code's editor) for JSON editing with syntax highlighting
- JSON Forms library for auto-generating forms from JSON schema
- Bootstrap 5 (already used in Technical Design page)

**For Validation**:
- Ajv (JavaScript JSON Schema validator)
- Custom validation rules for RDD-specific requirements

---

## Proposals

### Proposal 1: Minimal Viable Editor (Recommended for Speed)

**Approach**: Create a simple editor that focuses on the core need - editing questions.

**Implementation**:
1. Simple Python HTTP server (similar to existing Web UI server)
2. Two-panel layout: category tree on left, question editor on right
3. JSON-based editing with validation
4. No visual rule builder for `visibleWhen` - just text editing with validation
5. Basic validation: required fields, unique IDs, valid question types

**Pros**:
- Fast to implement (1-2 days)
- Minimal dependencies
- Focuses on actual user needs
- Consistent with RDD framework patterns

**Cons**:
- Less sophisticated UI
- Requires understanding JSON structure for complex edits

**Requirement Modifications**:
- Add UR requirement: "The framework shall provide a schema editor for `.rdd/config/technical-design-schema.json` that supports CRUD operations on categories and questions with validation"
- Add TR requirement: "The schema editor shall use Python http.server for file operations and vanilla JavaScript for UI, maintaining independence from RDD instance files"

### Proposal 2: Comprehensive Visual Editor

**Approach**: Full-featured editor with visual rule builders and advanced UX.

**Implementation**:
1. Python Flask server with RESTful API
2. React or Vue frontend (contradicts vanilla JS requirement - would need to be vanilla JS with components)
3. Visual rule builder for conditional logic
4. Drag-and-drop for question reordering
5. Rich validation with inline error display
6. Undo/redo support
7. Schema diff viewer

**Pros**:
- Professional user experience
- Fewer user errors
- Better for non-technical users

**Cons**:
- 1-2 weeks development time
- More complex codebase
- Potential over-engineering for actual usage frequency

**Not Recommended**: Too much effort for a developer tool used infrequently.

### Proposal 3: Hybrid Approach (RECOMMENDED)

**Approach**: Balance between simplicity and usability.

**Implementation**:
1. Python HTTP server with REST API endpoints (similar to `.rdd/src/web/server.py`)
2. Two-panel layout with tree navigation
3. Form-based editing for question properties
4. Text editor with syntax highlighting for `visibleWhen` rules
5. Real-time validation with clear error messages
6. Extract and adapt relevant CSS (not full copy)
7. Local server includes:
   - GET `/schema` - Load schema
   - POST `/schema` - Save schema with validation
   - POST `/validate` - Validate without saving
   - GET `/backup` - Create backup before editing

**Pros**:
- Good balance of functionality and simplicity
- Prevents most common errors through validation
- Professional appearance with extracted CSS
- Can be extended later if needed

**Cons**:
- Slightly more complex than minimal approach
- Requires defining validation rules

**Requirement Modifications**:
- **UR-XXXX**: The framework shall provide a web-based schema editor for `.rdd/config/technical-design-schema.json` that enables creating, editing, and deleting categories and questions with real-time validation
- **UR-XXXX**: The schema editor shall validate schema structure before saving to prevent invalid schemas that would break the Technical Design page
- **TR-XXXX**: The schema editor shall be implemented as a standalone tool in `tech_design_schema_editor/` using Python HTTP server and vanilla JavaScript, with no dependencies on `.rdd/` or `.rdd-instance/` runtime files
- **TR-XXXX**: The schema editor shall provide a REST API with endpoints for loading, saving, and validating the schema file
- **TR-XXXX**: The schema editor shall validate question IDs for uniqueness and ensure all required fields are present before allowing save operations

### Alternative Implementations

**Option A: Browser-Only with File System Access API**
- Use modern File System Access API
- No server required
- User must select file on each load
- Works only in Chromium browsers (Chrome, Edge)
- **Not Recommended**: Poor UX, limited browser support

**Option B: VS Code Extension**
- Create a VS Code extension for schema editing
- Native file system access
- Better integration with development workflow
- **Not Recommended**: Adds dependency on VS Code, more complex than needed

**Option C: CLI-Based Editor**
- Terminal-based interactive editor using `curses`
- No web UI needed
- **Not Recommended**: Poor UX for complex schema editing

### Trade-offs Analysis

| Approach | Dev Time | UX Quality | Maintenance | Validation | Risk |
|----------|----------|------------|-------------|------------|------|
| Minimal | 1-2 days | Basic | Easy | Basic | Low |
| Comprehensive | 1-2 weeks | Excellent | Medium | Advanced | Medium |
| Hybrid (Recommended) | 3-5 days | Good | Easy | Good | Low |
| Browser-Only | 2-3 days | Poor | Easy | Basic | Medium |

---

## Prompt Modification

Here's how I would write the prompt with more clarity and specificity:

---

**Title**: Technical Design Schema Editor - Standalone Web Tool

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
   - Can be run by developers when they need to modify the schema

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

---

### Summary of Improvements

The modified prompt is better because it:

1. **Provides Clear Context**: Explains why this editor is needed and what it affects
2. **Specifies Technology**: Exact stack with rationale (consistency with existing patterns)
3. **Defines UI Layout**: Removes ambiguity about structure
4. **Lists Validation Rules**: Specific requirements for data integrity
5. **Includes Error Handling**: Prevents undefined behavior
6. **Provides API Specification**: Clear contract between frontend and backend
7. **Sets Acceptance Criteria**: Testable outcomes
8. **Documents Out of Scope**: Manages expectations and prevents scope creep
9. **References Best Practices**: Points to Hybrid Approach from analysis
10. **Includes Documentation Requirements**: Ensures future maintainability

This prompt would result in a more predictable, higher-quality implementation with fewer iterations and edge cases.
