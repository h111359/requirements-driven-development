## Component Architecture

### Script Components

#### Main Entry Point
- **File**: `.rdd/scripts/rdd.py`
- **Purpose**: Unified command interface with domain routing
- **Version Management**: Uses `get_framework_version()` to read version from `.rdd/about.json`
- **Responsibilities**:
  - Parse command-line arguments
  - Route commands to appropriate domain handlers
  - Display help and version information
  - Execute workflow operations

**Note**: Legacy bash implementation (rdd.sh and utility scripts) archived in workspace during migration to Python.

#### Utility Scripts (Domain-Specific)
The Python implementation (`rdd_utils.py`) provides utility functions organized by domain:

1. **Core utilities**: Foundation functions
   - Color output (print_success, print_error, print_info, print_warning)
   - Validation (validate_name, normalize_to_kebab_case)
   - Configuration management (get_config, set_config)
   - Timestamp generation

2. **Git utilities**: Git operations
   - Repository validation
   - Branch operations
   - Stashing and merging
   - Diff and comparison

3. **Branch utilities**: Branch lifecycle
   - Branch creation with naming conventions
   - Branch deletion (single and bulk)
   - Merge status checking
   - Post-merge cleanup

4. **Workspace utilities**: Workspace management
   - Workspace initialization
   - Archiving with metadata
   - Backup and restore
   - Complete workspace clearing
  - Workspace File Listing: `create_files_list(root_dir='.', output_path='.rdd-docs/workspace/files-list.json')` is a utility that recursively enumerates directories and files under the repository/workspace, excluding dot-folders and `venv` by default, and writes a JSON payload containing `type`, `name`, `relpath`, and `mtime` (ISO8601 UTC). It is exposed via the CLI action `python .rdd/scripts/rdd.py workspace list-files`.

5. **Requirements utilities**: Requirements handling
   - Format validation
   - Requirements merging
   - ID assignment for new requirements
   - Impact analysis

6. **Change utilities**: Change workflow
   - Change creation
   - Change tracking
   - Workflow orchestration
   - Completion and wrap-up

7. **Clarify utilities**: Clarification phase
   - Clarification initialization
   - Question logging
   - Clarification status tracking

8. **Prompt utilities**: Prompt management
   - Prompt completion marking
   - Execution logging
   - Status checking

9. **Config utilities**: Configuration management
   - Configuration file reading (get_rdd_config)
   - Configuration file writing (set_rdd_config)
   - Configuration path resolution (get_rdd_config_path)
   - Default branch detection with config priority

**Legacy Note**: Previous bash implementation (branch-utils.sh, change-utils.sh, etc.) has been archived.

