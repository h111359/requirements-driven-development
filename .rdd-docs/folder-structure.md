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
│   │   ├── rdd.01-initiate.prompt.md
│   │   ├── rdd.02-clarify-requirements.prompt.md
│   │   ├── rdd.06-execute.prompt.md
│   │   ├── rdd.07-update-docs.prompt.md
│   │   ├── rdd.08-wrap-up.prompt.md
│   │   ├── rdd.09-clean-up.prompt.md
│   │   ├── rdd.G1-update-backlog.prompt.md
│   │   ├── rdd.G2-detect-docs-changes.prompt.md
│   │   └── rdd.G4-update-from-main.prompt.md
│   └── copilot-instructions.md   # Copilot agent behavioral guidelines
├── .rdd/                         # RDD framework internals
│   ├── scripts/                  # Python automation scripts
│   │   ├── rdd.py                # Main entry point for RDD commands
│   │   ├── rdd_utils.py          # Utility functions for all operations
│   │   ├── test_rdd_python.py    # Unit tests for Python implementation
│   │   ├── IMPLEMENTATION-SUMMARY.md  # Migration documentation
│   │   ├── README-PYTHON.md      # Python implementation guide
│   │   └── shell-to-python-mapping.md # Legacy bash to Python mapping
│   └── templates/                # File templates for initialization
│       ├── copilot-prompts.md    # Stand-alone prompts template
│       ├── requirements.md       # Requirements document template
│       ├── tech-spec.md          # Technical specification template
│       ├── data-model.md         # Data model template
│       ├── folder-structure.md   # Folder structure template
│       └── ...                   # Other templates
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
│   └── build.py                  # Build script for creating releases
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

### 3. No Auto-Creation Policy
- Documentation files (`clarity-checklist.md`, `version-control.md`) are NOT automatically copied to workspace
- Template files are only copied when explicitly needed by workflow
- Workspace remains minimal with only essential working files
- **change.md template removed**: The `change.md` file is no longer created during workspace initialization

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
- Domain-based routing: `python .rdd/scripts/rdd.py <domain> <action> [options]`
- Replaces standalone scripts like ~~`fix-management.sh`~~ and ~~`rdd.sh`~~ (deprecated)
- Uses `python` (not `python3`) for cross-platform compatibility (Windows, Linux, macOS)

### 8. Build and Release System
- **Build script**: `scripts/build.py` creates release archives
- **Build artifacts**: Generated in `build/` directory (Git-ignored)
- **Release format**: Single cross-platform `rdd-v{version}.zip` archive
- **Archive contents**:
  - Framework files (.rdd/, .github/prompts/)
  - Installation scripts (install.py, install.sh, install.ps1)
  - Documentation (README.md with installation instructions, LICENSE)
  - VS Code settings template (.vscode/settings.json)
- **Verification**: SHA256 checksum file generated for each archive
- **Version source**: Extracted from `RDD_VERSION` constant in rdd.py

## 📝 RDD Workflow File Locations

### Prompts
All workflow prompts in: `.github/prompts/rdd.*.prompt.md`

### Scripts
Current implementation: `.rdd/scripts/rdd.py` and `.rdd/scripts/rdd_utils.py`  
Legacy bash scripts: Archived in workspace during Python migration

### Templates
All file templates in: `.rdd/templates/*.md`

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


