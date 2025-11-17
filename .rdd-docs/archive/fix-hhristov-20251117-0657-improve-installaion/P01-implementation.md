# P01 Implementation

## Prompt Text

During the build, the script `build/build.py` should copy the file `.rdd/about.json` in the `.rdd` of the release. During installation, if in the repo is installed previous version of the RDD framework, the installation script `scripts/install.py` should create a folder `.rdd-docs/archive/installation_<version>` and should move there the obsolete files `.rdd-docs/data-model.md` and `.rdd-docs/folder-structure.md` and should inform the user to merge by themselves if important information is left in these files.

## Context from Requirements

**Relevant Requirements**:
- **[FR-98]**: The framework shall maintain all technical documentation in a single tech-spec.md file, with Data Architecture and Project Folder Structure as dedicated sections within tech-spec.md rather than separate files
- This requirement implies that `data-model.md` and `folder-structure.md` are obsolete files from older versions

**Related Technical Specifications**:
- Build process copies various files to release archives (.rdd/, .github/prompts/, templates, etc.)
- Installer handles upgrade scenarios and merges settings
- Archive functionality exists for preserving old content

## Context from Tech-Spec

**Build Process (build.py)**:
- Currently copies framework files, prompts, scripts, templates, LICENSE, settings
- Does NOT currently copy `.rdd/about.json` to the release `.rdd/` directory
- Creates archives with structure preserving original file organization

**Installation Process (install.py)**:
- Handles existing installation detection
- Overwrites framework files but preserves .rdd-docs/ content
- Does NOT currently handle archiving obsolete files from previous versions
- No version-based upgrade logic for obsolete files

## Implementation Plan

### Part 1: Build Process Changes

**Objective**: Copy `.rdd/about.json` to the release `.rdd/` directory during build

**Steps**:
1. Add a new function `copy_about_json()` in `build/build.py`
2. Call this function in the main build process after copying other `.rdd/` content
3. Verify the file is included in the release archive

### Part 2: Installation Process Changes

**Objective**: Archive obsolete files during installation if upgrading from previous version

**Steps**:
1. Detect if obsolete files exist (`data-model.md`, `folder-structure.md`)
2. If they exist:
   a. Detect installed framework version from existing `.rdd/about.json`
   b. Create archive directory `.rdd-docs/archive/installation_<version>/`
   c. Move obsolete files to archive
   d. Display informational message to user
3. Continue with normal installation

**Implementation Details**:
- New function: `archive_obsolete_files(target_dir: Path) -> None`
- Check for files: `.rdd-docs/data-model.md`, `.rdd-docs/folder-structure.md`
- Read version from existing `.rdd/about.json` if present
- Create archive with format: `.rdd-docs/archive/installation_{version}/`
- Use `shutil.move()` to relocate files
- Print clear message about what was archived and why

## Execution Steps

### Step 1: Modify build.py to copy about.json ✓

**Changes Made**:

1. Added new function `copy_about_json(repo_root: Path, build_dir: Path)`:
   - Copies `.rdd/about.json` from repo root to build `.rdd/` directory
   - Validates source file exists
   - Uses `shutil.copy2()` to preserve metadata
   - Provides clear console output

2. Updated main build process:
   - Added call to `copy_about_json()` in Step 3 after `copy_scripts()`
   - Ensures about.json is included in release archives

**File Modified**: `build/build.py`

**Lines Added**: 
- Function definition at line ~151 (after `copy_scripts()`)
- Function call at line ~431 (in main build process Step 3)

### Step 2: Modify install.py to archive obsolete files ✓

**Changes Made**:

1. Added new function `archive_obsolete_files(target_dir: Path)`:
   - Checks for obsolete files: `data-model.md`, `folder-structure.md`
   - Reads version from existing `.rdd/about.json` if present
   - Creates archive directory: `.rdd-docs/archive/installation_{version}/`
   - Moves obsolete files to archive using `shutil.move()`
   - Displays informational message about:
     - What was archived and where
     - That files are replaced by tech-spec.md sections
     - User should manually merge important information

2. Updated main installation flow:
   - Added call to `archive_obsolete_files(target_dir)` at the beginning of installation
   - Executes before copying new framework files
   - Ensures obsolete files are preserved before overwrite

**File Modified**: `scripts/install.py`

**Lines Added**:
- Function definition at line ~118 (after `detect_existing_installation()`)
- Function call at line ~461 (in main try block, before copy_prompts())

**Key Features**:
- Graceful handling if version cannot be read (uses "unknown")
- Only archives files that exist
- Creates archive directory with proper structure
- Clear user communication about what happened and what to do

### Step 3: Test the changes ✓

**Test 1: Build Process - about.json Copy**

Command:
```bash
python build/build.py
```

Results:
- ✓ Build completed successfully
- ✓ Console output shows "Copied about.json"
- ✓ Archive verification shows `rdd-v1.1.2/.rdd/about.json` is included
- ✓ File size: 24 bytes (JSON with version field)

**Test 2: Installer - Obsolete Files Archiving**

Setup:
- Created test git repository at `/tmp/rdd-install-test/test-repo`
- Created mock previous installation with:
  - `.rdd/about.json` containing version "1.0.0"
  - `.rdd-docs/data-model.md` with content
  - `.rdd-docs/folder-structure.md` with content

Command:
```bash
cd /tmp/rdd-install-test/rdd-v1.1.2
python install.py
# Target: /tmp/rdd-install-test/test-repo
```

Results:
- ✓ Installer detected existing RDD installation
- ✓ Archived 2 obsolete files to `.rdd-docs/archive/installation_1.0.0/`
- ✓ Files preserved with original content
- ✓ Files removed from main `.rdd-docs/` directory
- ✓ Clear user message displayed about:
  - What was archived and where
  - Mapping to new tech-spec.md sections
  - Instructions to manually merge if needed
- ✓ Installation completed successfully

Verification:
```bash
ls -la /tmp/rdd-install-test/test-repo/.rdd-docs/archive/installation_1.0.0/
# Shows: data-model.md, folder-structure.md

ls -la /tmp/rdd-install-test/test-repo/.rdd-docs/
# Shows: archive/, config.json, requirements.md, tech-spec.md
# (No data-model.md or folder-structure.md)
```

**Both implementations are working correctly!**

### Step 4: Update requirements.md ✓

Added new functional requirements:
- **[FR-123]**: Framework Version Distribution - Build process copies .rdd/about.json to release
- **[FR-124]**: Obsolete File Archiving During Upgrade - Installer archives obsolete files from previous versions
- **[FR-125]**: Obsolete File Notification - Installer informs users about archived files

### Step 5: Update tech-spec.md ✓

Updated sections:
- **Build Process Steps**: Added "about.json" to step 5 (Copy framework files)
- **Installation System - Obsolete file archiving**: Added new section documenting the upgrade scenario handling with obsolete file detection, archiving, and user notifications

### Step 6: Mark prompt as completed ✓

Executed:
```bash
python .rdd/scripts/rdd.py prompt mark-completed P01
```

Result: ✓ Prompt P01 marked as completed in work-iteration-prompts.md

## Summary

All tasks from prompt P01 have been successfully completed:

1. ✓ Build process now copies `.rdd/about.json` to release archives
2. ✓ Installer now archives obsolete files during upgrades
3. ✓ Both implementations tested and verified working
4. ✓ Requirements.md updated with 3 new FR entries
5. ✓ Tech-spec.md updated with implementation details
6. ✓ Prompt marked as completed

The framework now properly handles version information distribution and legacy file migration during upgrades.
