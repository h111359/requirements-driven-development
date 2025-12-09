# Files and Folders Structure

## Root layout:

repo-root/
├── .github/                      # GitHub workflows, prompts, Copilot instructions
│   ├── prompts/                  # Prompt templates for Copilot and automation
│   └── copilot-instructions.md   # Copilot agent instructions
├── .venv/                        # Python virtual environment (local, ignored)
├── .vscode/                      # VS Code workspace settings
│   └── settings.json             # Editor config
├── build/                        # Generated build artifacts (ignored by Git)
├── data/                         # All data files (not committed)

## Adding New Files to the Project Principles:

<>
```
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
```
