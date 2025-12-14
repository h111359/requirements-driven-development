### Web UI Architecture

The framework provides a browser-based interface for prompt management, technical specification editing, requirements management, and workspace operations.

#### Web Server Implementation
- **Technology**: Python's built-in `http.server.ThreadingHTTPServer` or equivalent stdlib component
- **Binding**: Localhost (`127.0.0.1`) with ephemeral port (OS-assigned)
- **Security**: Random session token generated on startup, required in `Authorization` header or query parameter
- **Lifecycle**: Server starts automatically when RDD framework invoked without CLI arguments; opens default browser to `http://127.0.0.1:<port>/?token=<token>`
- **Shutdown**: User closes browser tab; server terminates on idle timeout or explicit shutdown command

#### UI Technology Stack
- **Inline Assets**: All HTML, CSS, and JavaScript served as inline strings from Python handler (no external files)
- **Styling**: Minimalist CSS based on existing RDD styles (see system-questionnaire.html for reference)
- **No External Dependencies**: No npm, webpack, or third-party JS libraries required
- **Client-Side Logic**: Vanilla JavaScript for form handling, AJAX requests, and page navigation

#### Page Structure and Routing
The Web UI consists of six main pages, each served by a dedicated route:

1. **`/` or `/prompts`** - Prompt Management Page
   - Displays current content of `.rdd-instance/workdir/work-iteration-prompt.md`
   - Provides text editor for in-place editing
   - Shows generated questionnaire (if any) with input fields
   - Displays implementation plan (if any)
   - Buttons: Save, Execute Command, Load Predefined Prompt

2. **`/techspec`** - Technical Specification Page
   - Sub-tab: Technical Design JSON editor (form-based)
   - Sub-tab: File & Folder Structure visualizer
   - Loads design config JSON to generate form dynamically
   - Supports conditional/hierarchical questions
   - Button: Set Default Answers, Save Design

3. **`/requirements`** - Requirements Page
   - Button: Generate Add Requirement Prompt
   - Button: Reverse-Engineer Requirements
   - Displays generated prompts for review before copying to `work-iteration-prompt.md`

4. **`/vcs`** - Version Control & Workspace Management Page
   - Buttons: Create Branch, Update from Default, Commit Changes, Switch to Default, Merge Branch
   - Buttons: Archive Workspace, Load Archived Workspace
   - Displays git status, branch info, and operation results

5. **`/admin`** - Administration Page
   - Configuration editor: defaultBranch, gitMode, localOnly, version
   - Displays current config values
   - Allows saving updated config back to `config.json`

6. **`/library`** - Predefined Prompts Library
   - Lists all `.md` files in `.rdd/prompts/`
   - Shows preview of each prompt
   - Button: Load into `work-iteration-prompt.md`

#### Data Persistence and File Operations
- **File Read/Write**: Web server handler uses Python's `open()`, `json.load()`, `json.dump()` for file operations
- **Git Operations**: Executes git commands via `subprocess` module, respecting `gitMode` from config
- **Validation**: Server-side validation of all user inputs before file writes
- **Error Handling**: Returns JSON responses with `{success: bool, message: str, data: obj}` format

#### Execute Command Integration
- **Endpoint**: `POST /api/execute`
- **Behavior**: 
  - Reads `.rdd-instance/workdir/work-iteration-prompt.md`
  - Invokes execute command handler (from `rdd_utils.py` or dedicated module)
  - Streams execution logs back to client via JSON polling or SSE
  - Updates implementation file in real-time
  - Returns completion status and links to generated files
- **Concurrency**: Only one execute command may run at a time; subsequent requests return "busy" status

### Cross-Platform Implementation

**Current Implementation**: Python-based (`rdd.py` and `rdd_utils.py`)
- Cross-platform compatible (Windows, Linux, macOS)
- Single codebase for all platforms
- Native Python libraries for file operations, JSON handling, and subprocess management

**Legacy Implementation**: Bash and PowerShell scripts (archived)
- Previously maintained separate implementations for Linux (bash) and Windows (PowerShell)
- Located in `src/linux/.rdd/scripts/` and `src/windows/.rdd/scripts/`
- Bash scripts from `.rdd/scripts/` archived to workspace during Python migration

