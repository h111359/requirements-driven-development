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
│   │   └── rdd.08-wrap-up.prompt.md
│   └── copilot-instructions.md   # Copilot agent behavioral guidelines
├── .rdd/                         # RDD framework internals
│   ├── scripts/                  # Automation scripts for RDD workflows
│   │   ├── rdd.sh                # Main entry point for RDD commands
│   │   ├── change-utils.sh       # Change/fix creation and management
│   │   ├── workspace-utils.sh    # Workspace initialization and archiving
│   │   ├── prompt-utils.sh       # Prompt execution helpers
│   │   ├── git-utils.sh          # Git operations
│   │   ├── core-utils.sh         # Common utility functions
│   │   └── ...                   # Other utility scripts
│   └── templates/                # File templates for initialization
│       ├── fix.md                # Fix template
│       ├── copilot-prompts.md    # Stand-alone prompts template
│       ├── requirements.md       # Requirements document template
│       ├── tech-spec.md          # Technical specification template
│       ├── data-model.md         # Data model template
│       ├── folder-structure.md   # Folder structure template
│       └── ...                   # Other templates
├── .rdd-docs/                    # RDD documentation and workspace
│   ├── workspace/                # Active development workspace
│   │   ├── .rdd.[fix|enh].[branch-name]  # Change config file (one per workspace)
│   │   ├── .rdd.copilot-prompts.md       # Stand-alone prompts checklist
│   │   ├── log.jsonl                      # Execution log
│   │   └── ...                            # Other workflow files
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
├── scripts/                      # Project-specific automation scripts
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

### 4. Complete Workspace Clearing
- After archiving, ALL files are removed from workspace (not just a hardcoded list)
- Uses `find -mindepth 1 -delete` to ensure complete cleanup
- Prevents leftover files from interfering with next change

### 5. Archive Preservation
- Archives preserve complete workspace state at time of completion
- Named using sanitized branch name (slashes → hyphens)
- Include metadata file with timestamp, author, and commit info

## 📝 RDD Workflow File Locations

### Prompts
All workflow prompts in: `.github/prompts/rdd.*.prompt.md`

### Scripts
All automation in: `.rdd/scripts/*.sh`

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


