# P02 Implementation

## Prompt
Modify `.github/workflows/tests.yml` to execute only `scripts/run-tests.py` and not .ps1 or .sh test scripts

## Context Gathering

### Current State Analysis
1. **Workflow file**: `.github/workflows/tests.yml` currently executes:
   - Linux job: `bash scripts/run-tests.sh`
   - Windows job: `.\scripts\run-tests.ps1`

2. **Available scripts**:
   - `scripts/run-tests.py` - Python cross-platform test runner (already exists)
   - `scripts/run-tests.sh` - Bash test runner (to be removed from workflow)
   - `scripts/run-tests.ps1` - PowerShell test runner (to be removed from workflow)

3. **Requirements context**:
   - From P01: Tests should rely on `scripts/run-tests.py` instead of .ps1 and .sh scripts
   - Framework uses Python for cross-platform compatibility
   - Command should be `python` (not `python3`) per TR-30

### Implementation Plan
1. Read current tests.yml file ✓
2. Replace `bash scripts/run-tests.sh` with `python scripts/run-tests.py` in Linux job ✓
3. Replace `.\scripts\run-tests.ps1` with `python scripts/run-tests.py` in Windows job ✓
4. Verify run-tests.py exists and is executable ✓
5. Update implementation documentation ✓

## Implementation Details

### Changes Made

#### File: `.github/workflows/tests.yml`

**Linux Job (all-tests-linux):**
- **Before:** `run: bash scripts/run-tests.sh`
- **After:** `run: python scripts/run-tests.py`
- **Removed:** `shell: powershell` directive (not needed for Python)

**Windows Job (all-tests-windows):**
- **Before:** `run: .\scripts\run-tests.ps1` with `shell: powershell`
- **After:** `run: python scripts/run-tests.py`
- **Removed:** `shell: powershell` directive (Python runs natively on Windows)

### Verification

1. **Script exists:** ✓ `scripts/run-tests.py` is present
2. **Cross-platform:** ✓ Python script supports both Windows and Linux
3. **Dependencies:** ✓ Script uses virtual environment from setup-test-env.py
4. **Test coverage:** ✓ Script runs all test suites (Python, build, install, platform-specific)

### Alignment with Requirements

- **FR-48 & TR-30:** Uses `python` command (not `python3`) for cross-platform compatibility
- **TR-47:** Framework uses Python for cross-platform test execution
- **P01 requirement:** Tests no longer rely on .ps1 or .sh scripts, only on run-tests.py

## Result

The workflow now executes only `scripts/run-tests.py` on both Linux and Windows platforms, providing a unified cross-platform test execution experience. The shell-specific scripts (run-tests.sh and run-tests.ps1) are no longer used by CI/CD.

