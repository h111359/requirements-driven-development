## Files and Folders Structure

### Root Folder Structure

repo-root/
├── LICENSE                        # MIT License for the RDD framework
├── README.md                      # Main README with overview, installation instructions and usage guide for the RDD framework
├── build/                         # Build and release artifacts
├── prompts/                       # Prompt engineering templates
├── researches/                    # Research and analysis documents
└── scripts/                       # Utility scripts for testing and environment setup

**LICENSE**
- **Path**: `repo-root/LICENSE`
- **Type**: Text file
- **Description**: MIT License for the RDD framework

**README.md**
- **Path**: `repo-root/README.md`
- **Type**: Markdown
- **Description**: Main README with overview, installation instructions and usage guide for the RDD framework

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
├── release-notes-v1.1.2.md            # Release notes for version 1.1.2
├── scripts/                           # Test runner scripts
└── tests/                             # Test suite

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

### Build Scripts Folder Structure

repo-root/build/scripts/
└── run-tests.py                   # Cross-platform test runner for RDD Framework that runs all platform-appropriate tests

**run-tests.py**
- **Path**: `repo-root/build/scripts/run-tests.py`
- **Type**: Python script
- **Description**: Cross-platform test runner for RDD Framework that runs all platform-appropriate tests

---

### Build Tests Folder Structure

repo-root/build/tests/
├── requirements.txt               # RDD Framework test dependencies including pytest and code quality tools
├── test-spec.md                   # Comprehensive test specification for the RDD framework test suite
├── build/                         # Build script tests
├── fixtures/                      # Shared test data and fixtures
├── install/                       # Installation tests
└── python/                        # Python code tests

**requirements.txt**
- **Path**: `repo-root/build/tests/requirements.txt`
- **Type**: Text file
- **Description**: RDD Framework test dependencies including pytest and code quality tools

**test-spec.md**
- **Path**: `repo-root/build/tests/test-spec.md`
- **Type**: Markdown
- **Description**: Comprehensive test specification for the RDD framework test suite

---

### Build Tests - Build Folder Structure

repo-root/build/tests/build/
├── conftest.py                    # Pytest fixtures for build script tests
└── test_build.py                  # Tests for build.py script including version extraction and package creation

**conftest.py**
- **Path**: `repo-root/build/tests/build/conftest.py`
- **Type**: Python script
- **Description**: Pytest fixtures for build script tests

**test_build.py**
- **Path**: `repo-root/build/tests/build/test_build.py`
- **Type**: Python script
- **Description**: Tests for build.py script including version extraction and package creation

---

### Build Tests - Fixtures Folder Structure

repo-root/build/tests/fixtures/
└── README.md                      # Documentation for test fixtures and shared test data

**README.md**
- **Path**: `repo-root/build/tests/fixtures/README.md`
- **Type**: Markdown
- **Description**: Documentation for test fixtures and shared test data

---

### Build Tests - Install Folder Structure

repo-root/build/tests/install/
├── conftest.py                    # Pytest fixtures for install script tests
└── test_install.py                # Tests for install.py script including pre-flight checks and installation process

**conftest.py**
- **Path**: `repo-root/build/tests/install/conftest.py`
- **Type**: Python script
- **Description**: Pytest fixtures for install script tests

**test_install.py**
- **Path**: `repo-root/build/tests/install/test_install.py`
- **Type**: Python script
- **Description**: Tests for install.py script including pre-flight checks and installation process

---

### Build Tests - Python Folder Structure

repo-root/build/tests/python/
├── conftest.py                    # Pytest configuration and shared fixtures for RDD framework tests
├── test_integration.py            # Integration tests for RDD workflow including end-to-end scenarios
├── test_rdd_main.py               # Unit tests for rdd.py main entry point and CLI interface
└── test_rdd_utils.py              # Unit tests for rdd_utils.py utility functions

**conftest.py**
- **Path**: `repo-root/build/tests/python/conftest.py`
- **Type**: Python script
- **Description**: Pytest configuration and shared fixtures for RDD framework tests

**test_integration.py**
- **Path**: `repo-root/build/tests/python/test_integration.py`
- **Type**: Python script
- **Description**: Integration tests for RDD workflow including end-to-end scenarios

**test_rdd_main.py**
- **Path**: `repo-root/build/tests/python/test_rdd_main.py`
- **Type**: Python script
- **Description**: Unit tests for rdd.py main entry point and CLI interface

**test_rdd_utils.py**
- **Path**: `repo-root/build/tests/python/test_rdd_utils.py`
- **Type**: Python script
- **Description**: Unit tests for rdd_utils.py utility functions

---

### Prompts Folder Structure

repo-root/prompts/
└── GitHub-Copilot-Expert.md       # Expert prompt engineering template for GitHub Copilot with best practices

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
