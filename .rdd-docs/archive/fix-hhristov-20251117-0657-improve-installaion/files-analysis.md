# Project Files Analysis

Generated: 2025-11-17

## Summary

This analysis covers the key files and folders in the RDD Framework project based on the files-list.md scan.

## Key Folders and Files

### Root Level
- **LICENSE**: Project license file
- **README.md**: Main project documentation and quick start guide
- **rdd.sh**: Linux/macOS launcher script for RDD framework (installed to project root during installation)
- **user-guide.md**: Comprehensive user guide with workflow instructions

### .github/
GitHub-specific configuration and workflows
- **ISSUE_TEMPLATE/enhancement-template.md**: Issue template for enhancements
- **prompts/**: GitHub Copilot prompt files
  - `rdd.analyse-and-plan.prompt.md`: Prompt for analyzing user stories and generating execution plans
  - `rdd.execute.prompt.md`: Prompt for executing work iteration prompts
  - `rdd.update.prompt.md`: Prompt for updating documentation
- **workflows/**: GitHub Actions CI/CD workflows
  - `main-pr-restriction.yml`: Workflow to restrict direct PRs to main branch
  - `tests.yml`: Automated testing workflow

### .rdd/
RDD Framework core files (framework internals)
- **about.json**: Framework version information (v1.1.2 currently)
- **scripts/**: Python automation scripts
  - `rdd.py`: Main entry point for RDD commands with domain routing
  - `rdd_utils.py`: Utility functions for all RDD operations
- **templates/**: File templates for workspace initialization
  - `clarity-checklist.md`: Checklist for requirement clarity assessment
  - `design-checklist.md`: Design considerations checklist
  - `questions-formatting.md`: Guidelines for formatting questions to users
  - `requirements-format.md`: Format specification for requirements
  - `user-story.md`: User story template with state tracking
  - `work-iteration-prompts.md`: Template for stand-alone prompts checklist

### .rdd-docs/
Project documentation and workspace (user-specific content)
- **config.json**: Framework configuration (default branch, local-only mode, timestamps)
- **requirements.md**: Main requirements document with GF/FR/NFR/TR sections
- **tech-spec.md**: Technical specification with architecture, data model, and folder structure
- **user-story.md**: Current user story being worked on (top level, backed up during completion)
- **work-iteration-prompts.md**: Current work iteration prompts checklist (top level, backed up during completion)
- **archive/**: Archived completed work iterations
  - Multiple feature/fix branches archived as ZIP files or directories
  - `fix-hh-20251116-1016-build-improving/`: Most recent archived work
- **workspace/**: Active development workspace
  - `P01-implementation.md`: Implementation details for prompt P01
  - `files-analysis.md`: This file
  - `files-list.md`: Generated list of all project files
  - `list-files.py`: Script to generate files list

### .vscode/
VS Code workspace settings
- **settings.json**: Editor configuration, auto-approvals, file associations for RDD

### build/
Build system and release artifacts
- **build.py**: Python script for creating release archives with version conflict detection
- **create-release.prompt.md**: Prompt for release creation workflow
- **rdd-v*.zip**: Release archives for different versions
- **rdd-v*.zip.sha256**: SHA256 checksums for release archives
- **release-notes-v*.md**: Release notes for each version
- **scripts/run-tests.py**: Test runner script
- **tests/**: Test suite for build process
  - Build tests, installation tests, Python tests
  - Test fixtures and configurations

### scripts/
Installer and launcher scripts
- **install.py**: Python installer (template for build process)
- **rdd.bat**: Windows launcher script
- **rdd.sh**: Linux/macOS launcher script  
- **run-tests.py**: Python-based test runner for all test types
- **setup-test-env.py**: Script to setup virtual environment for testing

### templates/
One-time seed templates (installed to .rdd-docs/ during installation)
- **README.md**: README template for releases
- **config.json**: Configuration file seed template
- **requirements.md**: Requirements document seed template
- **tech-spec.md**: Technical specification seed template
- **settings.json**: VS Code settings template
- **user-guide.md**: User guide (also copied to build root)
- **RDD-Framework-User-Guide.pdf**: User guide in PDF format
- **RDD-Framework-User-Guide.pptx**: User guide source presentation
- **install.sh**: Bash installer launcher template
- **install.bat**: Batch installer launcher template

### tests/
Comprehensive test suite
- **python/**: Python unit tests and integration tests
  - `test_rdd_main.py`: Tests for main entry point
  - `test_rdd_utils.py`: Tests for utility functions
  - `test_integration.py`: Integration tests
- **build/**: Build process tests
  - `test_build.py`: Tests for build script
- **install/**: Installation process tests
  - `test_install.py`: Tests for installer
- **fixtures/**: Shared test fixtures
- **requirements.txt**: Test dependencies (pytest, pytest-cov, etc.)

## Recent Changes

### Prompt P01

The following changes were made as part of P01 implementation:

### Build Process (build/build.py)
- Added `copy_about_json()` function to copy `.rdd/about.json` to release .rdd/ directory
- Updated build process to include about.json in release archives

### Installation Process (scripts/install.py)
- Added `archive_obsolete_files()` function to handle upgrade scenarios
- Detects and archives obsolete files (`data-model.md`, `folder-structure.md`) from previous RDD versions
- Creates archive at `.rdd-docs/archive/installation_<version>/`
- Displays informational message about archived files and migration to tech-spec.md sections

### Documentation
- Updated requirements.md with FR-123, FR-124, FR-125
- Updated tech-spec.md Build Process Steps and Installer documentation sections

### Prompt P02

The following changes were made as part of P02 implementation:

### Build Process (build/build.py)
- Added `check_existing_build_artifacts()` function to detect existing zip and sha256 files
- Added `prompt_version_conflict_resolution()` function to handle conflicts with three options:
  1. Stop build process
  2. Increment patch version (with confirmation)
  3. Overwrite existing files (with confirmation)
- Modified `main()` function to check for conflicts before version selection
- Moved `build_root` creation earlier to support conflict detection
- Build process now prevents accidental overwrites of existing releases

### Documentation
- Updated requirements.md with FR-126, FR-127, FR-128
- Updated tech-spec.md Build Script description and Build Process Steps
