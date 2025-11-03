# 📁 Project Folder Structure

[EDITED] This document describes the organized structure of the Requirements-Driven Development (RDD) framework repository.

## 🧩 Root Layout

```
requirements-driven-development/
├── .github/                      # GitHub workflows, prompts, Copilot instructions
│   ├── prompts/                  # [ADDED] Prompt templates for workflow phases
│   │   ├── rdd.01-initiate.prompt.md         # Change/fix initiation
│   │   ├── rdd.02-clarify-requirements.prompt.md  # Requirements clarification
│   │   ├── rdd.03-tech-design.prompt.md      # Technical design
│   │   ├── rdd.04-prompt-generator.prompt.md # Generate implementation prompts
│   │   ├── rdd.06-execute.prompt.md          # Execute stand-alone prompts
│   │   ├── rdd.G1-update-backlog.prompt.md   # Update backlog from GitHub
│   │   ├── rdd.G2-merge-requirements-changes.prompt.md # Merge requirements
│   │   └── rdd.G3-detect-requirements-changes.prompt.md # Detect changes
│   ├── ISSUE_TEMPLATE/           # [ADDED] GitHub issue templates
│   │   └── enhancement-template.md  # Enhancement issue template
│   └── copilot-instructions.md   # Copilot agent instructions
├── .rdd/                         # [ADDED] RDD framework core
│   ├── scripts/                  # [ADDED] Bash automation scripts
│   │   ├── rdd.sh                # Main entry point and router
│   │   ├── core-utils.sh         # Core utility functions
│   │   ├── git-utils.sh          # Git operations
│   │   ├── branch-utils.sh       # Branch management
│   │   ├── workspace-utils.sh    # Workspace operations
│   │   ├── change-utils.sh       # Change workflow
│   │   ├── clarify-utils.sh      # Clarification workflow
│   │   ├── requirements-utils.sh # Requirements operations
│   │   ├── prompt-utils.sh       # Prompt management
│   │   ├── pr-utils.sh           # Pull request operations
│   │   ├── fix-management.sh     # Fix workflow
│   │   ├── general.sh            # General operations
│   │   └── README.md             # Scripts documentation
│   └── templates/                # [ADDED] File templates
│       ├── change.md             # Enhancement change template
│       ├── fix.md                # Fix change template (placeholder)
│       ├── copilot-prompts.md    # Stand-alone prompts template
│       ├── clarity-checklist.md  # Requirements clarity checklist
│       ├── requirements-format.md # Requirements formatting guide
│       ├── questions-formatting.md # Question formatting standards
│       ├── requirements.md       # Requirements document template
│       ├── tech-spec.md          # Technical specification template
│       ├── folder-structure.md   # Folder structure template
│       ├── data-model.md         # Data model template
│       ├── version-control.md    # Version control template
│       ├── backlog.md            # Backlog tracking template
│       ├── design-checklist.md   # Design clarity checklist
│       └── settings.json         # VS Code settings template
├── .rdd-docs/                    # [ADDED] RDD documentation and workspace
│   ├── workspace/                # [ADDED] Active workspace (current branch work)
│   │   ├── change.md             # Current change details (enh)
│   │   ├── fix.md                # Current fix details (fix)
│   │   ├── copilot-prompts.md    # Stand-alone prompts tracking
│   │   ├── open-questions.md     # Clarification questions log
│   │   ├── requirements-changes.md # Requirements changes to merge
│   │   ├── clarity-checklist.md  # Copy of clarity taxonomy
│   │   ├── .current-change       # JSON config for active change
│   │   ├── .id-mapping.txt       # ID mapping after wrap-up
│   │   └── log.jsonl             # Prompt execution log
│   ├── archive/                  # [ADDED] Completed changes archive
│   │   ├── <change-id>/          # Individual change archives
│   │   │   ├── change.md / fix.md
│   │   │   ├── open-questions.md
│   │   │   ├── requirements-changes.md
│   │   │   ├── .id-mapping.txt
│   │   │   └── .archive-info     # Archive metadata (JSON)
│   │   └── fixes/                # Fix archives subdirectory
│   ├── requirements.md           # Main requirements (reflects latest from main)
│   ├── tech-spec.md              # Technical specification
│   ├── folder-structure.md       # This file
│   ├── data-model.md             # Data model description
│   ├── version-control.md        # Version control strategy
│   ├── clarity-checklist.md      # Clarity taxonomy checklist
│   └── backlog.md                # Backlog tracking
├── .vscode/                      # VS Code workspace settings
│   └── settings.json             # Editor config (auto-approval, prompts, etc.)
├── build/                        # [EDITED] Generated build artifacts (ignored by Git)
├── scripts/                      # [EDITED] User/project-specific automation scripts
│   ├── build.sh                  # Build script
│   └── delete-merged-branches.sh # Branch cleanup utility
├── LICENSE                       # [ADDED] MIT License
└── README.md                     # Project overview


## ⚙️ Key Principles

### 1. [ADDED] RDD Framework Isolation
- `.rdd/` → RDD framework core (scripts, templates)
- `.rdd-docs/` → RDD documentation and workspace
- `.github/prompts/` → Workflow prompts for Copilot
- User project files remain separate from RDD infrastructure

### 2. [ADDED] Workspace Lifecycle
- **Active**: `.rdd-docs/workspace/` contains files for current branch work
- **Archived**: Completed work moved to `.rdd-docs/archive/<change-id>/`
- **Empty on Main**: Workspace cleared when on main/master branch
- **Branch-Aligned**: Workspace content corresponds to active enh/fix branch

### 3. [ADDED] Template-Based Generation
- Templates in `.rdd/templates/` ensure consistency
- Workspace initialized by copying relevant templates
- All documentation follows standardized formats

### 4. [ADDED] Script Modularity
- Utility scripts organized by functional domain
- `rdd.sh` serves as main router and interactive menu
- Scripts source each other for code reuse
- All scripts executable and self-documented

## 📝 Adding New Files to the RDD Framework

### RDD Prompt Files
- **New workflow prompts**: `.github/prompts/rdd.<number>-<name>.prompt.md`
- **General utility prompts**: `.github/prompts/rdd.G<number>-<name>.prompt.md`
- Follow existing prompt structure (Role, Context, Rules, Steps, Output Files, Error Handling)

### RDD Script Files
- **Utility scripts**: `.rdd/scripts/<domain>-utils.sh` (e.g., `git-utils.sh`, `workspace-utils.sh`)
- **Specialized scripts**: `.rdd/scripts/<function>-<purpose>.sh` (e.g., `fix-management.sh`)
- Include proper header comments, source dependencies, export functions
- Make executable with `chmod +x`

### RDD Template Files
- **Document templates**: `.rdd/templates/<name>.md` (e.g., `change.md`, `requirements.md`)
- **Configuration templates**: `.rdd/templates/<name>.json` (e.g., `settings.json`)
- Use placeholders like `<PLACEHOLDER>` for user-replaceable content

### RDD Documentation
- **Core docs**: `.rdd-docs/<name>.md` (e.g., `requirements.md`, `tech-spec.md`)
- **Workspace files**: Generated dynamically, not committed on main branch
- **Archive files**: Historical record, committed after wrap-up

### User Project Files
- **Project source code**: `src/` or appropriate directory
- **Project scripts**: `scripts/` for build, deploy, etc.
- **Project docs**: `docs/` if separate from RDD docs
- Keep project files separate from `.rdd/` and `.rdd-docs/` to avoid conflicts
