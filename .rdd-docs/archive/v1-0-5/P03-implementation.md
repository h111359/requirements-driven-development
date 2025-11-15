# Implementation for P03: The file `templates/user-guide.md` is not included in the release while `scripts/build.py` is executed. Fix that.

## Analysis

### Problem
- The file `templates/user-guide.md` is not included in the release zip because the `copy_templates` function in `scripts/build.py` only copies files from `.rdd/templates`, not from the top-level `templates` directory where `user-guide.md` is located.
- The build process does not copy any files from `templates/` except for a few specific ones (e.g., README.md, settings.json) in other functions.

### Solution
- Update the build script to copy `user-guide.md` from `templates/` into the build directory.
- The most consistent location is to place it in the root of the build directory, similar to README.md, or in `.rdd-docs` if it is considered documentation.
- For clarity and discoverability, place it in the root of the build directory, as with README.md.
- Update the build script to copy `templates/user-guide.md` to `build_dir/user-guide.md` during the build process.
- Document this change here and in the folder structure documentation.

## Implementation Steps
1. Update `scripts/build.py` to copy `templates/user-guide.md` to the build directory root after generating README.md.
2. Add a print message for this step.
3. Update `.rdd-docs/folder-structure.md` to reflect the presence of `user-guide.md` in the release root.
4. (No requirements or data model changes needed.)

## Commands/Edits
- Edit `scripts/build.py` to add the copy step.
- Edit `.rdd-docs/folder-structure.md` to document the new file in the release structure.

## Next Steps
- Make the code and documentation changes.
- Mark the prompt as completed after all steps are done.
