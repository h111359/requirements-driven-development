# 📁 Project Folder Structure

This document describes the organized structure of the project.

## 🧩 Root Layout

```
repo-root/
├── .github/                      # GitHub workflows, prompts, Copilot instructions
│   ├── prompts/                  # Prompt templates for Copilot and automation
│   └── copilot-instructions.md   # Copilot agent instructions
├── .venv/                        # Python virtual environment (local, ignored)
├── .vscode/                      # VS Code workspace settings
│   └── settings.json             # Editor config
├── build/                        # Generated build artifacts (ignored by Git)
├── data/                         # All data files (not committed)
├── docs/                         # Documentation
│   ├── changes/                  # Change logs and templates
│   │   └── template/             # Change log templates
│   ├── specifications/           # Technical specs
│   ├── user-guides/              # User documentation
│   ├── data-model.md             # Data model description
│   ├── file-structure.md         # This file
│   └── requirements.md           # Requirements document
├── logs/                         # ETL and audit logs
├── scripts/                      # Automation scripts (shell, PowerShell)
├── specs/                        # Implementation specs and plans
├── src/                          # Source code
│   ├── py/                       # Python code
│   │   ├── data/                 # Python data helpers
│   │   ├── kolko-ni-struva/      # Main Python package
│   │   │   ├── etl/              # ETL modules
│   │   │   ├── schemas/          # Schema definitions
│   │   └── logs/                 # Python log helpers
│   └── web/                      # Web app source
│       ├── assets/               # CSS, images, icons
│       ├── js/                   # JavaScript files
│       ├── templates/            # HTML templates
│       └── index.html            # Main HTML page
├── tests/                        # Automated tests
│   ├── fixtures/                 # Test fixtures/sample data
│   ├── tmp/                      # Temporary test outputs
├── input.md                      # Input/scratch file for prompts
├── netlify.toml                  # Netlify deployment config
├── pyproject.toml                # Python project metadata
├── README.md                     # Project overview
├── requirements.txt              # Python dependencies
├── .env.example                  # Example environment variables
├── .gitignore                    # Git ignore rules
```


## ⚙️ Key Principles

### 1. Source vs. Build Separation
- `src/` → editable code only  
- `build/` → generated artifacts (ignored by Git)  
- Netlify publishes from `build/web/`



## 📝 Adding New Files to the Project

When adding new files, follow this decision tree to place them in the correct location:

### Python Code
- **ETL modules** (data extraction, transformation, loading): `src/py/kolko-ni-struva/etl/`
- **Schema definitions** (validation models, data structures): `src/py/kolko-ni-struva/schemas/`
- **CLI commands**: Add to or extend `src/py/kolko-ni-struva/cli.py`
- **Utilities and helpers**: Create a `src/py/kolko-ni-struva/lib/` or `src/py/kolko-ni-struva/utils/` folder

### Web Files
- **HTML pages**: `src/web/` (e.g., `index.html`, `about.html`)
- **JavaScript**: `src/web/js/` (e.g., `script.js`, `chart.js`)
- **CSS, images, icons**: `src/web/assets/` (e.g., `style.css`, `logo.png`)
- **Templates** (if using templating): `src/web/templates/`

### Automation Scripts
- **Shell scripts** (`.sh`): `scripts/` (e.g., `build.sh`, `deploy.sh`)
- **PowerShell scripts** (`.ps1`): `scripts/` (e.g., `build.ps1`, `deploy.ps1`)
- Name scripts descriptively based on their function

### Tests
- **Test files**: `tests/` (e.g., `test_etl.py`, `test_schema_validation.py`)
- **Test fixtures** (sample data): `tests/fixtures/`
- **Temporary test outputs**: `tests/tmp/` (auto-ignored by Git)

### Documentation
- **User guides** (how to use the system): `docs/user-guides/`
- **Developer guides** (setup, contribution, coding standards): `docs/developer-guides/`
- **Requirements** (functional, technical, data): `docs/requirements/`
- **Specifications** (architecture, API, data models): `docs/specifications/`

### Configuration
- **Environment files**: Root (e.g., `.env`, `.env.example`)
- **Application configs**: `configs/` (e.g., `local.env`, `cloud.env`, `prod.env`)

### Data Files
- **Nomenclatures and reference data**: `data/` (e.g., `category-nomenclature.json`)
- **Raw downloaded data**: `data/raw/` (not committed to Git)
- **Interim/processed data**: `data/interim/`, `data/processed/` (not committed to Git)


