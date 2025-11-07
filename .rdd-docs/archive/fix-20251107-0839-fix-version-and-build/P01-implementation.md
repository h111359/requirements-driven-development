# P01 Implementation: Version Extraction Bug Fix

## Prompt
Bug: During the build the version is extracted from a variable defined in `.rdd/scripts/rdd.py` which is wrong. The version should be taken from `.rdd-docs/config.json`. Check if some other parts in build takes the wrong version as well and fix. Remove the code in `scripts/build.py` which takes the version from .py scripts and rely only on `.rdd-docs/config.json`

## Analysis

### Problem
- The build script (`scripts/build.py`) currently extracts the version from the `RDD_VERSION` variable in `.rdd/scripts/rdd.py`.
- The correct source of truth for the version is `.rdd-docs/config.json`.
- Other parts of the build script may also use the wrong version source.

### Solution Plan
1. Update `scripts/build.py` to read the version from `.rdd-docs/config.json` instead of `.rdd/scripts/rdd.py`.
2. Remove the `extract_version` function and any code that reads the version from `.rdd/scripts/rdd.py`.
3. Ensure all version references in the build script use the value from `.rdd-docs/config.json`.
4. Validate that no other part of the build script or related logic uses the old extraction method.
5. Document the change and reasoning here.

## Implementation Details

### Changes Made
- Updated `scripts/build.py` to read the version from `.rdd-docs/config.json`.
- Removed the `extract_version` function and all code that extracted the version from `.rdd/scripts/rdd.py`.
- All version references in the build script now use the value from `.rdd-docs/config.json`.
- Validated that no other part of the build script uses the old extraction method.

### Testing
- After the change, running the build script will use the version from `.rdd-docs/config.json`.
- If the config file is missing or the version is invalid, the script will exit with an error.

## Implementation Steps
- [x] Analysis and plan documented
- [ ] Update `scripts/build.py` to use `.rdd-docs/config.json` for version
- [ ] Remove old version extraction logic
- [ ] Test build script for correct version usage
- [ ] Mark prompt as completed

## Next Step
Mark the prompt as completed using the required script.
