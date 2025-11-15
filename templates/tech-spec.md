# Technical Specification

> This is a template file. Replace with your project's technical requirements.

## System Overview
- [Provide high-level description of the system]
- [Define main components and their interactions]
- [Specify system boundaries and interfaces]

## Technology Stack
- [Specify programming languages, frameworks, and libraries]
- [Define browser/platform compatibility requirements]
- [List development tools and build systems]

## Architecture Patterns
- [Describe architectural patterns used (MVC, microservices, etc.)]
- [Explain design principles and patterns]
- [Document architectural decisions and rationale]

## Component Architecture
- [Detail major system components]
- [Define component responsibilities and interfaces]
- [Show component relationships and dependencies]

## Data Architecture
- [Describe data models and schemas]
- [Define data flow and storage patterns]
- [Specify data management strategies]

## Project Folder Structure
- [Root Layout] Example for root layout:
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
```
- [Adding New Files to the Project Principles] Example for adding new files principles:
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


## Deployment Architecture
- [Define deployment topology]
- [Specify infrastructure components]
- [Document scaling and availability strategies]

## Performance
- [Define response time and throughput requirements]
- [Specify resource usage limits]
- [Set scalability requirements]

## Security
- [Define authentication and authorization requirements]
- [Specify data protection and privacy requirements]
- [List compliance requirements]

## Infrastructure
- [Define hosting and deployment requirements]
- [Describe project folder structure and organization]
- [Specify database and storage requirements]
- [List third-party service dependencies]
