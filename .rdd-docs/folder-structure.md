# 📁 Project Folder Structure

This document describes the organized structure of the project.

## 🧩 Root Layout

````markdown
# 📁 RDD Project Folder Structure

This document describes the organized structure of the Requirements-Driven Development framework.

## 🧩 Root Layout

```
repo-root/
├── .github/                      # GitHub workflows, prompts, Copilot instructions
│   ├── prompts/                  # Prompt templates for Copilot and RDD workflow
│   │   ├── rdd.execute.prompt.md
│   └── copilot-instructions.md   # Copilot agent behavioral guidelines
├── .rdd/                         # RDD framework internals
│   ├── scripts/                  # Python automation scripts
│   │   ├── rdd.py                # Main entry point for RDD commands
│   │   ├── rdd_utils.py          # Utility functions for all operations
│   │   ├── test_rdd_python.py    # Unit tests for Python implementation
│   │   ├── IMPLEMENTATION-SUMMARY.md  # Migration documentation
│   │   ├── README-PYTHON.md      # Python implementation guide
│   │   └── shell-to-python-mapping.md # Legacy bash to Python mapping
│   ├── templates/                # File templates for initialization
│   │   ├── copilot-prompts.md    # Stand-alone prompts template
│   │   ├── clarity-checklist.md  # Clarity checklist template
│   │   ├── design-checklist.md   # Design checklist template
│   │   ├── folder-structure.md   # Folder structure template
│   │   ├── questions-formatting.md  # Question formatting guidelines
│   │   ├── requirements-format.md   # Requirements format guidelines
│   └── user-guide.md             # Comprehensive user guide (installed during setup)
├── src/                          # Legacy platform-specific implementations (archived)
│   ├── linux/                    # Linux/macOS implementation
│   │   ├── .rdd/
│   │   │   ├── scripts/          # Bash scripts (.sh)
│   │   │   │   ├── rdd.sh        # Main entry point
│   │   │   │   ├── core-utils.sh
│   │   │   │   ├── git-utils.sh
│   │   │   │   ├── branch-utils.sh
│   │   │   │   ├── workspace-utils.sh
│   │   │   │   ├── requirements-utils.sh
│   │   │   │   ├── change-utils.sh
│   │   │   │   ├── clarify-utils.sh
│   │   │   │   └── prompt-utils.sh
│   │   │   ├── templates/        # Linux-specific templates
│   │   ├── .prompts/
│   │   │   └── prompts/          # Linux-specific prompts
│   │   └── ...
│   └── windows/                  # Windows implementation
│       ├── .rdd/
│       │   ├── scripts/          # PowerShell scripts (.ps1)
│       │   │   ├── rdd.ps1       # Main entry point
│       │   │   ├── core-utils.ps1
│       │   │   ├── git-utils.ps1
│       │   │   ├── branch-utils.ps1
│       │   │   ├── workspace-utils.ps1
│       │   │   ├── requirements-utils.ps1
│       │   │   ├── change-utils.ps1
│       │   │   ├── clarify-utils.ps1
│       │   │   └── prompt-utils.ps1
│       │   ├── templates/        # Windows-specific templates
│   │   ├── .prompts/
│       │   └── prompts/          # Windows-specific prompts
│       └── ...
├── .rdd-docs/                    # RDD documentation and workspace
│   ├── config.json               # Framework configuration (defaultBranch, version)
│   ├── workspace/                # Active development workspace
│   │   ├── .rdd.[fix|enh].[branch-name]  # Change config file (one per workspace)
│   │   ├── .rdd.copilot-prompts.md       # Stand-alone prompts checklist
│   │   ├── log.jsonl                      # Execution log
│   │   └── ...                            # Other workflow files (NOT change.md)
│   ├── archive/                  # Archived completed changes
│   │   └── [sanitized-branch-name]/      # One directory per archived change
│   │       ├── .archive-metadata          # Archive metadata (JSON)
│   │       └── ...                        # Archived workspace files
│   ├── requirements.md           # Main requirements document
│   ├── tech-spec.md              # Technical specifications
│   ├── data-model.md             # Data model and structures
│   ├── folder-structure.md       # This file
│   └── ...                       # Other project documentation
├── .vscode/                      # VS Code workspace settings
│   └── settings.json             # Editor config, auto-approvals, associations
├── build/                        # Generated build artifacts (ignored by Git)
│   ├── rdd-v{version}.zip        # Release archive (created by build.py)
│   └── rdd-v{version}.zip.sha256 # Checksum file for archive verification
├── scripts/                      # Build and release automation scripts
│   ├── build.py                  # Build script for creating releases
│   ├── install.py                # Python installer template
│   ├── install.sh                # Bash installer template
│   ├── install.ps1               # PowerShell installer template (deprecated)
│   ├── rdd.bat                   # Windows RDD launcher (installed to project root)
│   └── rdd.sh                    # Linux/macOS RDD launcher (installed to project root)
├── templates/                    # One-time seed templates (installed to .rdd-docs/)
│   ├── README.md                 # README template for build
│   ├── config.json               # Configuration seed template
│   ├── data-model.md             # Data model seed template
│   ├── requirements.md           # Requirements seed template
│   ├── tech-spec.md              # Technical spec seed template
│   ├── settings.json             # VS Code settings template
│   ├── user-guide.md             # Comprehensive user guide (copied to .rdd/ during install)
│   ├── install.sh                # Bash launcher template (Linux/macOS)
│   └── install.bat               # Batch launcher template (Windows)
├── README.md                     # Project overview and quick start
├── LICENSE                       # Project license
└── .gitignore                    # Git ignore rules
```

## ⚙️ Key Principles

### 1. Workspace Lifecycle
- **Initialization**: Workspace created when starting new enhancement/fix
- **Active Work**: Files added/modified during development
- **Archiving**: Complete workspace copied to archive directory
- **Cleanup**: All files removed from workspace after archiving

### 2. Config File Naming
- **Pattern**: `.rdd.[type].[branch-name]`
- **Type**: `fix` or `enh` 
- **Purpose**: Embeds change metadata directly in filename
- **Example**: `.rdd.fix.20251103-1257-prompt-08-bug-workspace-unclean`

### 4. Complete Workspace Clearing
- After archiving, ALL files are removed from workspace (not just a hardcoded list)
- Uses `find -mindepth 1 -delete` to ensure complete cleanup
- Prevents leftover files from interfering with next change

### 5. Archive Preservation
- Archives preserve complete workspace state at time of completion
- Named using sanitized branch name (slashes → hyphens)
- Include metadata file with timestamp, author, and commit info

### 6. Python-Based Implementation
- **Cross-platform**: Single Python codebase works on Windows, Linux, and macOS
- **Main script**: `rdd.py` with utilities in `rdd_utils.py`
- **Legacy archived**: Previous bash scripts moved to workspace archive during migration
- **No platform-specific scripts needed**: Python provides native cross-platform compatibility

### 7. Unified Command Interface
- All RDD operations accessible through `python .rdd/scripts/rdd.py`
- **Interactive menu (recommended)**: Run without arguments to access simplified 4-option workflow menu
- **CLI mode (advanced)**: Domain-based routing: `python .rdd/scripts/rdd.py <domain> <action> [options]`
- Domains include: change, branch, workspace, git, prompt, config
- Replaces standalone scripts like ~~`fix-management.sh`~~ and ~~`rdd.sh`~~ (deprecated)
- Uses `python` (not `python3`) for cross-platform compatibility (Windows, Linux, macOS)

### 8. Simplified Iteration Workflow (v1.0.3+)
- **Interactive menu system**: Numeric selection (no arrow keys) for reliability
- **4 core operations**: Create iteration, Update from default, Complete iteration, Delete merged branches
- **Safety checks**: Validates branch state and workspace emptiness before operations
- **Local-only mode support**: Skips remote operations when configured
- **Clear user feedback**: Informational messages guide users through each step
- **Legacy CLI access**: Advanced users can still use domain commands for scripting

### 9. Configuration Management
- **Configuration file**: `.rdd-docs/config.json` stores framework settings
- **Template location**: `templates/config.json` (seed template installed during build)
- **Version controlled**: Config shared across team in repository
- **CLI access**: `python .rdd/scripts/rdd.py config [show|get|set]`
- **Key settings**: defaultBranch, version, localOnly, timestamps
- **Interactive setup**: Branch selection and local-only mode prompts during initialization populate config
- **Local-only mode**: When `localOnly: true`, all remote git operations are automatically skipped

### 10. Build and Release System
- **Build script**: `scripts/build.py` creates release archives
- **Build artifacts**: Generated in `build/` directory (Git-ignored)
- **Release format**: Single cross-platform `rdd-v{version}.zip` archive
- **Archive contents**:
  - Framework files (.rdd/, .github/prompts/)
  - Installation scripts:
    - install.py (from scripts/install.py - Python installer with GUI support)
    - install.sh (from templates/install.sh - Bash launcher for installer)
    - install.bat (from templates/install.bat - Batch launcher for installer)
  - RDD launcher scripts (installed to project root):
    - rdd.bat (from scripts/rdd.bat - Windows RDD menu launcher)
    - rdd.sh (from scripts/rdd.sh - Linux/macOS RDD menu launcher)
  - Documentation (README.md from templates/README.md, LICENSE)
  - VS Code settings template (.vscode/settings.json from templates/settings.json)
  - Seed templates (.rdd-docs/ with config.json, data-model.md, requirements.md, tech-spec.md from templates/)
- **Verification**: SHA256 checksum file generated for each archive
- **Version source**: Extracted from `.rdd-docs/config.json`
- **Template processing**: Reads templates from templates/ directory with {{VERSION}} placeholder substitution

## 📝 RDD Workflow File Locations

### Prompts
All workflow prompts in: `.github/prompts/rdd.*.prompt.md`

### Scripts
Current implementation: `.rdd/scripts/rdd.py` and `.rdd/scripts/rdd_utils.py`  
Legacy bash scripts: Archived in workspace during Python migration

### Templates
All file templates in: `.rdd/templates/*.md` (ongoing-use templates)
One-time seed templates in: `templates/` (installed once to `.rdd-docs/`)

### Active Work
Current workspace: `.rdd-docs/workspace/`

### Historical Record
Completed work: `.rdd-docs/archive/[branch-name]/`

### Main Documentation
Project docs: `.rdd-docs/*.md`
````


## ⚙️ Key Principles

### 1. Source vs. Build Separation
- `src/` → editable code only  
- `build/` → generated artifacts (ignored by Git)  
- Netlify publishes from `build/web/`



## 📝 Adding New Files to the Project

Use this template as a routing guide when introducing new files. Adjust folder names to match the conventions of your project.

### Python Code
- **ETL modules** (data extraction, transformation, loading): `src/py/<package-name>/etl/`
- **Schema definitions** (validation models, data structures): `src/py/<package-name>/schemas/`
- **CLI commands**: extend `src/py/<package-name>/cli.py` or add subcommands under `src/py/<package-name>/cli/`
- **Utilities and helpers**: group shared code under `src/py/<package-name>/lib/` or `src/py/<package-name>/utils/`

### Web Files
- **HTML pages**: `<web-root>/` (e.g., `index.html`, `about.html`)
- **JavaScript**: `<web-root>/js/` (e.g., `main.js`, `charts.js`)
- **CSS, images, icons**: `<web-root>/assets/` (e.g., `styles.css`, `logo.svg`)
- **Templates** (if using a templating engine): `<web-root>/templates/`

### Automation Scripts
- **Shell scripts** (`.sh`): `scripts/` (e.g., `build.sh`, `deploy.sh`)
- **PowerShell scripts** (`.ps1`): `scripts/` (e.g., `build.ps1`, `deploy.ps1`)
- Name scripts to reflect their purpose and environment

### Tests
- **Test files**: `tests/` (e.g., `test_etl.py`, `test_schema_validation.py`)
- **Test fixtures** (sample data/configuration): `tests/fixtures/`
- **Temporary test outputs**: `tests/tmp/` (auto-ignored by Git)

### Documentation
- **User guides** (how to use the system): `docs/user-guides/`
- **Developer guides** (setup, contribution standards): `docs/developer-guides/`
- **Requirements** (functional, technical, data): `docs/requirements/`
- **Specifications** (architecture, API, data models): `docs/specifications/`

### Configuration
- **Environment files**: repository root (e.g., `.env`, `.env.example`)
- **Application configs**: `configs/` (e.g., `local.env`, `cloud.env`, `prod.env`)

### Data Files
- **Reference and nomenclature data**: `data/` (e.g., `category-nomenclature.json`)
- **Raw ingested data**: `data/raw/` (typically excluded from version control)
- **Interim/processed data**: `data/interim/`, `data/processed/` (typically excluded from version control)


