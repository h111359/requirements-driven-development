## Files and Folders Structure

### Root Folder Structure

repo-root/
├── LICENSE                        # MIT License for the RDD framework
├── README.md                      # Main README with overview, installation instructions, usage guide and documentation for the RDD framework
├── build/                         # Build and release artifacts
├── researches/                    # Research and analysis documents
├── scripts/                       # Utility scripts for testing and environment setup
├── tech_design_schema_editor/     # Standalone web-based editor for technical design schema
└── tests/                         # Test suite for the RDD framework

**LICENSE**
- **Path**: `repo-root/LICENSE`
- **Type**: Text file
- **Description**: MIT License for the RDD framework

**README.md**
- **Path**: `repo-root/README.md`
- **Type**: Markdown
- **Description**: Main README with overview, installation instructions, usage guide and documentation for the RDD framework

---

### Build Folder Structure

repo-root/build/
├── build.py                           # Build script for creating RDD framework releases with cross-platform zip archive
├── create-release.prompt.md           # Prompt template for creating release notes from git history and branch information
├── rdd-v1.0.0.zip                     # Release package for version 1.0.0
├── rdd-v1.0.0.zip.sha256              # SHA256 checksum for version 1.0.0 release package
├── rdd-v1.0.1.zip                     # Release package for version 1.0.1
├── rdd-v1.0.1.zip.sha256              # SHA256 checksum for version 1.0.1 release package
├── rdd-v1.0.2.zip                     # Release package for version 1.0.2
├── rdd-v1.0.2.zip.sha256              # SHA256 checksum for version 1.0.2 release package
├── rdd-v1.0.3.zip                     # Release package for version 1.0.3
├── rdd-v1.0.3.zip.sha256              # SHA256 checksum for version 1.0.3 release package
├── rdd-v1.0.4.zip                     # Release package for version 1.0.4
├── rdd-v1.0.4.zip.sha256              # SHA256 checksum for version 1.0.4 release package
├── rdd-v1.1.0.zip                     # Release package for version 1.1.0
├── rdd-v1.1.0.zip.sha256              # SHA256 checksum for version 1.1.0 release package
├── rdd-v1.1.1.zip                     # Release package for version 1.1.1
├── rdd-v1.1.1.zip.sha256              # SHA256 checksum for version 1.1.1 release package
├── rdd-v1.1.2.zip                     # Release package for version 1.1.2
├── rdd-v1.1.2.zip.sha256              # SHA256 checksum for version 1.1.2 release package
├── release-notes-v1.0.1.md            # Release notes for version 1.0.1 including testing infrastructure and bug fixes
├── release-notes-v1.0.2.md            # Release notes for version 1.0.2
├── release-notes-v1.0.3.md            # Release notes for version 1.0.3
├── release-notes-v1.0.4.md            # Release notes for version 1.0.4
├── release-notes-v1.0.5.md            # Release notes for version 1.0.5
├── release-notes-v1.1.0.md            # Release notes for version 1.1.0
├── release-notes-v1.1.1.md            # Release notes for version 1.1.1
└── release-notes-v1.1.2.md            # Release notes for version 1.1.2

**build.py**
- **Path**: `repo-root/build/build.py`
- **Type**: Python script
- **Description**: Build script for creating RDD framework releases with cross-platform zip archive

**create-release.prompt.md**
- **Path**: `repo-root/build/create-release.prompt.md`
- **Type**: Markdown
- **Description**: Prompt template for creating release notes from git history and branch information

**Release Packages (rdd-v*.zip)**
- **Path**: `repo-root/build/rdd-v*.zip`
- **Type**: ZIP archives
- **Description**: Release packages for various versions of the RDD framework

**Release Checksums (rdd-v*.zip.sha256)**
- **Path**: `repo-root/build/rdd-v*.zip.sha256`
- **Type**: SHA256 checksum files
- **Description**: SHA256 checksums for verifying the integrity of release packages

**Release Notes (release-notes-v*.md)**
- **Path**: `repo-root/build/release-notes-v*.md`
- **Type**: Markdown
- **Description**: Release notes documenting changes, enhancements, and fixes for each version

---

### Researches Folder Structure

repo-root/researches/
├── 20251228-1300-build-folder-gitignored/    # Research on gitignoring build folder
│   └── advantages-disadvantages.md           # Analysis of advantages and disadvantages of gitignoring the build folder
└── 20251228-1537-plan-further-work/          # Planning documentation
    └── plan.md                               # Detailed development plan for further work on the RDD framework

**advantages-disadvantages.md**
- **Path**: `repo-root/researches/20251228-1300-build-folder-gitignored/advantages-disadvantages.md`
- **Type**: Markdown
- **Description**: Analysis of advantages and disadvantages of gitignoring the build folder

**plan.md**
- **Path**: `repo-root/researches/20251228-1537-plan-further-work/plan.md`
- **Type**: Markdown
- **Description**: Detailed development plan for further work on the RDD framework

---

### Tech Design Schema Editor Folder Structure

repo-root/tech_design_schema_editor/
├── server.py                      # Python HTTP server with REST API for schema file operations
├── index.html                     # Main HTML page with two-panel layout (tree navigation + editor)
├── run_editor.sh                  # Launcher script for Linux/Mac - starts server and opens browser
├── run_editor.bat                 # Launcher script for Windows - starts server and opens browser
├── README.md                      # Comprehensive documentation with usage guide, schema structure, and validation rules
├── static/
│   ├── style.css                  # Stylesheet extracted and adapted from RDD Web UI
│   └── app.js                     # JavaScript application for schema editing and validation
└── backups/                       # Directory for automatic schema backups (created by server)

**server.py**
- **Path**: `repo-root/tech_design_schema_editor/server.py`
- **Type**: Python script
- **Description**: Python HTTP server with REST API for schema file operations including load, save with validation, backup creation, and atomic file writes

**index.html**
- **Path**: `repo-root/tech_design_schema_editor/index.html`
- **Type**: HTML
- **Description**: Main HTML page with two-panel layout featuring tree navigation sidebar and form-based editor panel

**run_editor.sh**
- **Path**: `repo-root/tech_design_schema_editor/run_editor.sh`
- **Type**: Bash script
- **Description**: Launcher script for Linux/Mac that starts the server and automatically opens the browser

**run_editor.bat**
- **Path**: `repo-root/tech_design_schema_editor/run_editor.bat`
- **Type**: Batch script
- **Description**: Launcher script for Windows that starts the server and opens the browser

**README.md**
- **Path**: `repo-root/tech_design_schema_editor/README.md`
- **Type**: Markdown
- **Description**: Comprehensive documentation including quick start guide, usage instructions, schema structure, validation rules, and troubleshooting

**static/style.css**
- **Path**: `repo-root/tech_design_schema_editor/static/style.css`
- **Type**: CSS
- **Description**: Stylesheet extracted and adapted from RDD Web UI for consistent look and feel with editor-specific components

**static/app.js**
- **Path**: `repo-root/tech_design_schema_editor/static/app.js`
- **Type**: JavaScript
- **Description**: Client application implementing schema loading, tree rendering, CRUD operations, validation, and status management

**backups/**
- **Path**: `repo-root/tech_design_schema_editor/backups/`
- **Type**: Directory
- **Description**: Directory for automatic timestamped schema backups created before each save operation

---

### Scripts Folder Structure

repo-root/scripts/
├── run-tests.py                   # Cross-platform test runner for RDD Framework that runs all platform-appropriate tests
└── setup-test-env.py              # Setup script for creating or updating RDD test environment and installing test dependencies

**run-tests.py**
- **Path**: `repo-root/scripts/run-tests.py`
- **Type**: Python script
- **Description**: Cross-platform test runner for RDD Framework that runs all platform-appropriate tests

**setup-test-env.py**
- **Path**: `repo-root/scripts/setup-test-env.py`
- **Type**: Python script
- **Description**: Setup script for creating or updating RDD test environment and installing test dependencies

---

### Tests Folder Structure

repo-root/tests/
├── requirements.txt               # RDD Framework test dependencies including pytest and code quality tools
├── test-spec.md                   # Comprehensive test specification for the RDD framework test suite
├── build/                         # Build script tests
├── fixtures/                      # Shared test data and fixtures
├── install/                       # Installation tests
└── python/                        # Python code tests

**requirements.txt**
- **Path**: `repo-root/tests/requirements.txt`
- **Type**: Text file
- **Description**: RDD Framework test dependencies including pytest and code quality tools

**test-spec.md**
- **Path**: `repo-root/tests/test-spec.md`
- **Type**: Markdown
- **Description**: Comprehensive test specification for the RDD framework test suite

---

### Tests - Build Folder Structure

repo-root/tests/build/
├── conftest.py                    # Pytest fixtures for build script tests
└── test_build.py                  # Tests for build.py script including version extraction and package creation

**conftest.py**
- **Path**: `repo-root/tests/build/conftest.py`
- **Type**: Python script
- **Description**: Pytest fixtures for build script tests

**test_build.py**
- **Path**: `repo-root/tests/build/test_build.py`
- **Type**: Python script
- **Description**: Tests for build.py script including version extraction and package creation

---

### Tests - Fixtures Folder Structure

repo-root/tests/fixtures/
└── README.md                      # Documentation for test fixtures and shared test data

**README.md**
- **Path**: `repo-root/tests/fixtures/README.md`
- **Type**: Markdown
- **Description**: Documentation for test fixtures and shared test data

---

### Tests - Install Folder Structure

repo-root/tests/install/
├── conftest.py                    # Pytest fixtures for install script tests
└── test_install.py                # Tests for install.py script including pre-flight checks and installation process

**conftest.py**
- **Path**: `repo-root/tests/install/conftest.py`
- **Type**: Python script
- **Description**: Pytest fixtures for install script tests

**test_install.py**
- **Path**: `repo-root/tests/install/test_install.py`
- **Type**: Python script
- **Description**: Tests for install.py script including pre-flight checks and installation process

---

### Tests - Python Folder Structure

repo-root/tests/python/
├── conftest.py                    # Pytest configuration and shared fixtures for RDD framework tests
├── test_integration.py            # Integration tests for RDD workflow including end-to-end scenarios
├── test_rdd_main.py               # Unit tests for rdd.py main entry point and CLI interface
├── test_rdd_utils.py              # Unit tests for rdd_utils.py utility functions
└── test_seed.py                   # Test suite for rdd-instance_seed.py script including seed data validation

**conftest.py**
- **Path**: `repo-root/tests/python/conftest.py`
- **Type**: Python script
- **Description**: Pytest configuration and shared fixtures for RDD framework tests

**test_integration.py**
- **Path**: `repo-root/tests/python/test_integration.py`
- **Type**: Python script
- **Description**: Integration tests for RDD workflow including end-to-end scenarios

**test_rdd_main.py**
- **Path**: `repo-root/tests/python/test_rdd_main.py`
- **Type**: Python script
- **Description**: Unit tests for rdd.py main entry point and CLI interface

**test_rdd_utils.py**
- **Path**: `repo-root/tests/python/test_rdd_utils.py`
- **Type**: Python script
- **Description**: Unit tests for rdd_utils.py utility functions

**test_seed.py**
- **Path**: `repo-root/tests/python/test_seed.py`
- **Type**: Python script
- **Description**: Test suite for rdd-instance_seed.py script including seed data validation

**GitHub-Copilot-Expert.md**
- **Path**: `repo-root/prompts/GitHub-Copilot-Expert.md`
- **Type**: Markdown
- **Description**: Expert prompt engineering template for GitHub Copilot with best practices

---

### Researches Folder Structure

repo-root/researches/
├── 20251228-1300-build-folder-gitignored/
│   └── advantages-disadvantages.md    # Analysis of advantages and disadvantages of gitignoring the build folder
└── 20251228-1537-plan-further-work/
    └── plan.md                        # Detailed development plan for further work on the RDD framework

**20251228-1300-build-folder-gitignored/advantages-disadvantages.md**
- **Path**: `repo-root/researches/20251228-1300-build-folder-gitignored/advantages-disadvantages.md`
- **Type**: Markdown
- **Description**: Analysis of advantages and disadvantages of gitignoring the build folder

**20251228-1537-plan-further-work/plan.md**
- **Path**: `repo-root/researches/20251228-1537-plan-further-work/plan.md`
- **Type**: Markdown
- **Description**: Detailed development plan for further work on the RDD framework

---

### Scripts Folder Structure

repo-root/scripts/
├── run-tests.py                   # Cross-platform test runner for RDD Framework that runs all platform-appropriate tests
└── setup-test-env.py              # Setup script for creating or updating RDD test environment and installing test dependencies

**run-tests.py**
- **Path**: `repo-root/scripts/run-tests.py`
- **Type**: Python script
- **Description**: Cross-platform test runner for RDD Framework that runs all platform-appropriate tests

**setup-test-env.py**
- **Path**: `repo-root/scripts/setup-test-env.py`
- **Type**: Python script
- **Description**: Setup script for creating or updating RDD test environment and installing test dependencies

---

### Tests - Python Folder - Seed Script Tests

**test_seed.py**
- **Path**: `repo-root/tests/python/test_seed.py`
- **Type**: Python test script
- **Description**: Test suite for rdd-instance_seed.py script, verifying folder creation, file initialization, validation, idempotency, and error handling

---

### RDD Instance - Archive Folder Structure

.rdd-instance/archive/
├── <iteration-id>_<iteration-name>.zip    # Compressed archive of completed work iterations

**Archive Zip Files**
- **Path**: `.rdd-instance/archive/<iteration-id>_<iteration-name>.zip`
- **Type**: ZIP archive
- **Description**: Compressed archive of a completed work iteration's workdir content. Created when archiving an iteration via the workdir_archive.py script. Contains the complete state of the workdir folder including all prompts, plans, questionnaires, implementations, and the work iteration registry. Archives are stored as zip files (not directories) to reduce disk space usage and prevent Windows path length issues caused by deeply nested directory structures.
- **Naming Convention**: `<iteration-id>_<iteration-name>.zip` where iteration-id follows format `ITR-YYYYMMDD-HHmmss` and iteration-name is the user-provided iteration name.
- **Contents**: Complete copy of `.rdd-instance/workdir/` folder structure at the time of archiving, including:
  - `work-iteration-registry.json` - Registry state at archive time
  - `prompts-registry.md` - Prompts history up to archive time
  - `<prompt-id>_<prompt-title>/` folders - All prompt working folders with their artifacts
- **Access**: To access archived content, extract the zip file to a temporary location.

---

### RDD Instance - Config Folder Structure

.rdd-instance/config/
└── instance-config.json           # Instance-level configuration file containing git-enabled flag and other instance settings

**instance-config.json**
- **Path**: `.rdd-instance/config/instance-config.json`
- **Type**: JSON configuration file
- **Description**: Instance-level configuration for the RDD framework. Contains the git-enabled boolean flag that controls whether git commit operations are performed during prompt completion. Default value is false. This configuration is separate from the work iteration registry to provide consistent behavior across all iterations in an instance.
- **Schema**: `{"git-enabled": boolean}`
- **Default**: `{"git-enabled": false}`

---

### RDD Framework - Actions Folder

**.rdd/src/actions/rdd-instance_seed.py**
- **Path**: `repo-root/.rdd/src/actions/rdd-instance_seed.py`
- **Type**: Python script
- **Description**: Validates and initializes RDD instance structure by creating missing folders and files based on manifest.json configuration. Idempotent and safe for repeated execution. Executed automatically during web server startup.
