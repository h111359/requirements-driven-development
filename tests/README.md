# RDD Framework Test Suite

This directory contains comprehensive tests for the RDD framework.

## Quick Start

### 1. Set Up Virtual Environment

**Automated Setup (Recommended)**:
```bash
# Run from repository root
python setup-test-env.py
```

This will:
- Create `.venv/` virtual environment (or update if it exists)
- Install/update all test dependencies
- Preserve existing packages in the environment

**Manual Setup**:
```bash
# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r tests/requirements.txt
```

### 2. Activate Virtual Environment

**Before running any tests**, activate the virtual environment:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

When activated, your prompt will show `(.venv)`.

### 3. Run Tests

```bash
# Make sure virtual environment is activated!
pytest tests/python/

```bash
# Make sure virtual environment is activated!
pytest tests/python/

# Run with coverage
pytest tests/python/ --cov=.rdd/scripts --cov=scripts --cov-report=html

# Run specific test file
pytest tests/python/test_rdd_utils.py -v
```

## Directory Structure

- **`python/`** - Tests for Python scripts (`.rdd/scripts/` and `scripts/`)
- **`shell/`** - Tests for Bash scripts (`install.sh`)
- **`powershell/`** - Tests for PowerShell scripts (`install.ps1`)
- **`fixtures/`** - Shared test data and mock repositories

## Running Tests in Detail

### Python Tests

```bash
# Ensure virtual environment is activated first!
# source .venv/bin/activate

# Run all Python tests
pytest tests/python/

# Run with coverage
pytest tests/python/ --cov=.rdd/scripts --cov=scripts --cov-report=html
# Ubuntu/Debian: sudo apt-get install bats
# macOS: brew install bats-core

# Run shell tests
bats tests/shell/test_install_sh.bats
```

### PowerShell Tests (Windows)

```powershell
# Install Pester
Install-Module -Name Pester -Force -SkipPublisherCheck

# Run PowerShell tests
Invoke-Pester tests/powershell/Install.Tests.ps1
```

## CI/CD

Tests are automatically run via GitHub Actions on:
- Every push to `main` and `dev` branches
- Every pull request
- Both Linux and Windows environments

See `.github/workflows/tests.yml` for configuration.

## Test Coverage Goals

- **Unit tests**: > 80% code coverage
- **Integration tests**: Key workflows tested end-to-end
- **Cross-platform**: Tests run on both Linux and Windows

## Writing New Tests

### Python Tests

Follow pytest conventions:
- Test files: `test_*.py`
- Test functions: `def test_*():`
- Use fixtures from `conftest.py`
- Mock external dependencies (git, filesystem)

### Shell Tests

Follow BATS conventions:
- Test files: `*.bats`
- Test functions: `@test "description" { ... }`
- Use setup/teardown functions
- Mock commands when needed

### PowerShell Tests

Follow Pester conventions:
- Test files: `*.Tests.ps1`
- Describe/Context/It blocks
- Use BeforeAll/AfterAll
- Mock cmdlets when needed
