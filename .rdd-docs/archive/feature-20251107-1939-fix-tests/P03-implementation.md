# P03 Implementation: Troubleshoot why the test is failing and fix it

## Prompt
Troubleshoot why the test is failing and fix it.

## Date
November 7, 2025

## Analysis

Starting investigation to identify which test is failing and why.

### Test Run Results

Command: `python scripts/run-tests.py`

**Failing Test:** `tests/build/test_build.py::TestFileCopying::test_copy_rdd_docs_seeds`

**Error:**
```
SystemExit: 1
Seed template not found: /tmp/tmp8l3r0nr_/rdd-project/templates/folder-structure.md
```

The test is failing because the `copy_rdd_docs_seeds` function in `scripts/build.py` is looking for seed templates in the `templates/` directory, but it cannot find `folder-structure.md`.

### Investigation Steps

1. Check the actual location of template files
2. Review the `copy_rdd_docs_seeds` function in `scripts/build.py`
3. Review the test setup to understand what's expected

### Root Cause

The `copy_rdd_docs_seeds` function in `scripts/build.py` (lines 180-186) expects these seed templates:
- config.json
- data-model.md
- requirements.md
- tech-spec.md
- **folder-structure.md**

However, the mock fixture in `tests/build/conftest.py` only creates the first 4 files, missing `folder-structure.md`.

### Solution

Add `folder-structure.md` to the mock fixture in `tests/build/conftest.py` to match what the build script expects.

## Implementation

### Changes Made

1. **Fixed `tests/build/conftest.py`**: Added the missing `folder-structure.md` file creation in the mock fixture:
   ```python
   (project_root / "templates" / "folder-structure.md").write_text("# Folder Structure")
   ```

2. **Enhanced `tests/build/test_build.py`**: Added assertion to verify `folder-structure.md` is copied:
   ```python
   assert (rdd_docs / "folder-structure.md").exists()
   ```

### Verification

Running tests to verify the fix...

Command: `python scripts/run-tests.py`

**Result:** ✓ All tests passed!

```
Total test suites: 3
Passed: 3
✓ All tests passed!
```

All 83 tests passed across all test suites:
- Python unit tests: 49 passed
- Build tests: 13 passed (including the previously failing test)
- Install tests: 21 passed

## Summary

The failing test `tests/build/test_build.py::TestFileCopying::test_copy_rdd_docs_seeds` was caused by a missing `folder-structure.md` file in the mock fixture. The build script expected this file to exist in the templates directory, but the test fixture only created 4 out of 5 required seed template files.

**Files Modified:**
1. `tests/build/conftest.py` - Added creation of `folder-structure.md` in mock fixture
2. `tests/build/test_build.py` - Added assertion to verify `folder-structure.md` is copied

The fix is complete and all tests now pass successfully.

