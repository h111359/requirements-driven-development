## Files and Folders Structure

repo-root/
├── .github/                      # GitHub workflows, prompts, Copilot instructions
│   ├── prompts/                  # Prompt templates for Copilot and RDD workflow
│   │   ├── rdd.execute.prompt.md
│   └── copilot-instructions.md   # Copilot agent behavioral guidelines
├── .rdd/                         # RDD framework internals
│   ├── about.json                # Framework version information
│   ├── scripts/                  # Python automation scripts
│   │   ├── rdd.py                # Main entry point for RDD commands
│   │   ├── rdd_utils.py          # Utility functions for all operations
│   ├── templates/                # File templates for initialization
│   │   ├── work-iteration-prompts.md    # Stand-alone prompts template
│   │   ├── user-story.md         # User story template
│   │   ├── clarity-checklist.md  # Clarity checklist template
│   │   ├── design-checklist.md   # Design checklist template
│   │   ├── questions-formatting.md  # Question formatting guidelines
│   │   ├── requirements-format.md   # Requirements format guidelines
├── .rdd-instance/                    # RDD documentation and workspace
│   ├── config.json               # Framework configuration (defaultBranch, localOnly, timestamps)
│   ├── work-iteration-prompts.md # Stand-alone prompts checklist (top level, backed up to workspace on iteration complete)
│   ├── user-story.md             # User story definition (top level, backed up to workspace on iteration complete)
│   ├── workspace/                # Active development workspace
│   │   ├── .rdd.[fix|enh].[branch-name]  # Change config file (one per workspace)
│   │   ├── log.jsonl                      # Execution log
│   │   └── ...                            # Other workflow files (work-iteration-prompts.md, user-story.md backed up here during completion)
│   ├── archive/                  # Archived completed changes
│   │   └── [sanitized-branch-name]/      # One directory per archived change
│   │       ├── .archive-metadata          # Archive metadata (JSON)
│   │       └── ...                        # Archived workspace files
│   ├── requirements.md           # Main requirements document
│   └── ...                       # Other project documentation
├── .vscode/                      # VS Code workspace settings
│   └── settings.json             # Editor config, auto-approvals, associations
├── build/                        # Build directory with build script and artifacts
│   ├── build.py                  # Build script for creating releases
│   ├── rdd-v{version}.zip        # Release archive (created by build.py)
│   └── rdd-v{version}.zip.sha256 # Checksum file for archive verification
├── scripts/                      # Release and automation scripts
│   ├── install.py                # Python installer template
│   ├── install.sh                # Bash installer template
│   ├── install.ps1               # PowerShell installer template (deprecated)
│   ├── rdd.bat                   # Windows RDD launcher (installed to project root)
│   ├── rdd.sh                    # Linux/macOS RDD launcher (installed to project root)
│   ├── run-tests.py              # Test runner script
│   └── setup-test-env.py         # Virtual environment setup for testing
├── templates/                    # One-time seed templates (installed to .rdd-instance/)
│   ├── README.md                 # README template for build
│   ├── config.json               # Configuration seed template
│   ├── requirements.md           # Requirements seed template
│   ├── settings.json             # VS Code settings template
│   ├── user-guide.md             # Comprehensive user guide (copied to .rdd/ during install)
│   ├── install.sh                # Bash launcher template (Linux/macOS)
│   └── install.bat               # Batch launcher template (Windows)
├── tests/                        # Comprehensive testing suite
│   ├── python/                   # Python script tests (pytest)
│   ├── build/                    # Build script tests
│   ├── install/                  # Installation tests
│   ├── fixtures/                 # Shared test fixtures
│   ├── requirements.txt          # Test dependencies
│   └── README.md                 # Testing documentation
├── README.md                     # Project overview and quick start
├── user-guide.md                 # Comprehensive user guide (included in release root)
├── LICENSE                       # Project license
└── .gitignore                    # Git ignore rules


## System Files

### about.json

**Description**: Framework version information file. Located in `.rdd/about.json` and version-controlled with the repository.

**Attributes**:

- **version**: 
  - Description: RDD framework version using semantic versioning
  - Mandatory: Yes
  - Data Type: String
  - Format: Semantic versioning (MAJOR.MINOR.PATCH)
  - Example: "1.1.1"

**Example File**:
```json
{
  "version": "1.1.1"
}
```

**Location**:
- File path: `.rdd/about.json`
- Read by: `get_framework_version()` in rdd.py
- Updated by: `update_about_version()` in build.py

**Usage**:
- Read when displaying framework version (`python .rdd/scripts/rdd.py --version`)
- Updated during build process when user increments version
- Single source of truth for framework version



### config.json

**Description**: Framework-wide configuration file storing repository and workflow settings. Located in `.rdd-instance/config.json` and version-controlled with the repository. Note: Version information is stored separately in `.rdd/about.json`.

**Attributes**:

- **defaultBranch**: 
  - Description: Name of the repository's default branch for change management
  - Mandatory: Yes
  - Data Type: String
  - Format: Valid git branch name
  - Data validation rules: Must be a valid git branch name; Should exist in the repository
  - Example: "main", "dev", "master", "develop"

- **created**:
  - Description: ISO 8601 timestamp of when the configuration was first created
  - Mandatory: Yes
  - Data Type: String
  - Format: ISO 8601 datetime with timezone (UTC)
  - Example: "2025-11-06T08:00:00Z"

- **lastModified**:
  - Description: ISO 8601 timestamp of when the configuration was last updated
  - Mandatory: Yes
  - Data Type: String
  - Format: ISO 8601 datetime with timezone (UTC)
  - Example: "2025-11-06T10:30:00Z"

- **localOnly**:
  - Description: Flag indicating whether the repository operates in local-only mode without GitHub remote
  - Mandatory: Yes
  - Data Type: Boolean
  - Format: true or false
  - Data validation rules: Must be a boolean value; When true, all remote operations (fetch, push, pull) are skipped; When false (default), normal GitHub remote operations are performed
  - Example: false, true

**Example File**:
```json
{
  "defaultBranch": "dev",
  "localOnly": false,
  "created": "2025-11-06T08:00:00Z",
  "lastModified": "2025-11-06T10:30:00Z"
}
```

**Location**:
- File path: `.rdd-instance/config.json`
- Template: `.rdd/templates/config.json`
- Access functions: `get_rdd_config(key, default)`, `set_rdd_config(key, value)`, `get_rdd_config_path()`

**Usage**:
- Created during workspace initialization via interactive branch selection
- Updated via `python .rdd/scripts/rdd.py config set <key> <value>`
- Read by `get_default_branch()` function for branch management
- Displayed via `python .rdd/scripts/rdd.py config show`