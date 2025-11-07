## Step 4: Remove Legacy Scripts and Tests

Deleted files and directories:
- scripts/install.sh
- scripts/install.ps1
- scripts/run-tests.sh
- scripts/run-tests.ps1
- tests/shell/ (entire directory)
- tests/powershell/ (entire directory)

Updated tests:
- Removed build tests that asserted generation of install.sh and install.ps1
- Kept build tests for install.py generation intact
- Updated `tests/README.md` to reference `python scripts/run-tests.py` and removed shell/PowerShell guidance

## Step 5: Build Script Alignment

Adjusted `scripts/build.py` to:
- Stop generating install.sh and install.ps1
- Update step counts and success message contents
- Keep `install.py` generation as the only installer

## Step 6: Verification Plan

1) Configure Python env and run tests:
- Use `python setup-test-env.py` to prepare `.venv/`
- Run `python scripts/run-tests.py`

2) Sanity check installer:
- In a temp folder, run `python scripts/install.py` and cancel at prompt (pre-flight checks should pass)

## Notes on Functionality Parity

- Interactive folder navigation (arrow-key UI) from .sh/.ps1 is intentionally not migrated; `install.py` prompts for a path and validates git repo — sufficient for simplified install UX.
- All core checks and installation actions are implemented in `install.py`.

## Status

- Implementation complete; ready to run tests and mark prompt as completed.
# P01 Implementation: Simplify Installation Scripts

## Prompt Instructions

Scripts `scripts/install.ps1` and `scripts/install.sh` cause ton of issues. Remove them from everywhere - especially from tests here `tests`, from`README.md`. Simplify the instruction for installation in `README.md` so to be issued a Python command (specify for Linux and Windows), which to make the installation only running `scripts/install.py`. Check if there is usefull functionality in `scripts/install.ps1` and `scripts/install.sh` which is not in `scripts/install.py`. The test in `tests` should be changed so not to rely on `scripts/run-tests.ps1` and `scripts/run-tests.sh` but on a new script `scripts/run-tests.py`, which should replace the .ps1 and .sh run test scripts. The tests should test only `scripts/install.py`.

## Analysis

### Current State

Let me analyze the current state of the installation and test infrastructure:

1. **Installation Scripts**:
   - `scripts/install.py` - Python-based cross-platform installer
   - `scripts/install.sh` - Bash installer (to be removed)
   - `scripts/install.ps1` - PowerShell installer (to be removed)

2. **Test Runner Scripts**:
   - `scripts/run-tests.sh` - Bash test runner (to be replaced with Python)
   - `scripts/run-tests.ps1` - PowerShell test runner (to be replaced with Python)

3. **Test Files**:
   - `tests/shell/test_install_sh.bats` - Tests for bash installer
   - `tests/powershell/Install.Tests.ps1` - Tests for PowerShell installer
   - `tests/install/test_install.py` - Tests for Python installer

### Tasks to Complete

1. ✅ Read and compare functionality in all three installers
2. ✅ Ensure `scripts/install.py` has all necessary functionality
3. ✅ Create `scripts/run-tests.py` to replace shell/PowerShell test runners
4. ✅ Update tests to use only Python-based installation
5. ✅ Remove references to install.sh and install.ps1 from README.md
6. ✅ Remove install.sh and install.ps1 test files
7. ✅ Update all documentation to reference only Python-based installation

## Step 1: Compare Installer Functionality

### Analysis of install.py (Python Installer)
✅ **Complete functionality**:
- Python version check (3.7+)
- Git installation check
- Git repository validation
- Existing installation detection
- Target directory prompting
- Confirmation prompting
- Copy prompts to .github/prompts/
- Copy .rdd/ framework
- Copy .rdd-docs/ seed templates
- Merge VS Code settings intelligently
- Update .gitignore
- Installation verification

### Analysis of install.sh (Bash Installer)
**Additional functionality**:
- Interactive folder navigation with arrow keys
- Visual menu interface
- Folder browsing UI

**Core functionality**: Actually delegates to install.py after navigation!

### Analysis of install.ps1 (PowerShell Installer)
**Additional functionality**:
- Interactive folder navigation with arrow keys
- Visual menu interface (PowerShell version)
- Folder browsing UI

**Core functionality**: Also delegates to install.py after navigation!

### Conclusion
✅ **install.py contains ALL core installation functionality**
✅ **install.sh and install.ps1 only provide UI wrapper for directory selection**
✅ **No functionality loss if we remove shell/PowerShell wrappers**

The shell/PowerShell wrappers are **nice-to-have UI enhancements** but NOT essential. Users can:
1. Navigate to their target directory manually
2. Run `python install.py` directly
3. Provide directory path when prompted

### Decision
We will **remove install.sh and install.ps1** and document direct Python installation only.

## Step 2: Create run-tests.py

✅ Created `scripts/run-tests.py` with the following features:
- Cross-platform (Windows, Linux, macOS)
- Color-coded output
- Progress indicators
- Prerequisites checking
- Virtual environment activation
- Runs pytest for Python, build, and install tests
- Conditionally runs BATS (Linux/macOS) or Pester (Windows)
- Clear test summary with pass/fail counts

## Step 3: Remove References from README.md

Updating README.md to remove all references to install.sh and install.ps1...
