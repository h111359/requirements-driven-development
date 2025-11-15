# P05 Implementation

## Prompt Text

During installation when running the script install.py should remove all rdd.* prompts first, before installing (copying in `.github/prompts`) the rdd. prompts from the installation. Aim is to be replaced all prompts starting with "rdd." as there could be some left from previous releases.

## Context Analysis

### Relevant Requirements from requirements.md

The installation system is documented with the following requirements:

- **[FR-53]**: Python-Based Installer - provides cross-platform Python installer (install.py) that automates installation, settings merging, and .gitignore updates
- **[FR-54]**: Installation Verification - verifies prerequisites, validates target is Git repository
- **[NFR-20]**: Simplified Installation Process - straightforward process using Python (install.py)

### Current Implementation (install.py)

The current `copy_prompts` function at line ~230 in install.py:

```python
def copy_prompts(source_dir: Path, target_dir: Path):
    """Copy prompt files to target"""
    print_info("Installing prompts...")
    
    src_prompts = source_dir / ".github" / "prompts"
    dst_prompts = target_dir / ".github" / "prompts"
    
    dst_prompts.mkdir(parents=True, exist_ok=True)
    
    copied = 0
    for prompt_file in src_prompts.glob("*.prompt.md"):
        shutil.copy2(prompt_file, dst_prompts / prompt_file.name)
        copied += 1
    
    print_success(f"Installed {copied} prompt file(s)")
```

**Issue**: This function does NOT remove existing `rdd.*` prompt files before copying new ones. If a previous installation had prompt files that are no longer part of the framework, they would remain.

### Technical Specification

From tech-spec.md:
- Prompts location: `.github/prompts/` (TR-12)
- Naming pattern for RDD prompts: `rdd.*.prompt.md`

### Solution

The prompt requests that all existing `rdd.*` prompts be removed before installing new ones. This ensures a clean replacement of all RDD prompt files.

## Implementation Plan

1. **Modify `copy_prompts` function** in `scripts/install.py`:
   - Before copying new prompts, remove all existing files matching pattern `rdd.*.prompt.md` in target `.github/prompts/` directory
   - Add informational message about cleanup
   - Then proceed with copying as before

2. **Update requirements.md**: Add requirement for prompt cleanup during installation

3. **Update tech-spec.md**: Document the prompt cleanup behavior

4. **Create and run the file listing script** as per instructions

5. **Mark prompt as completed** using the script

## Implementation Details

### Step 1: Modified `copy_prompts` function in scripts/install.py

Changed the function to remove all existing `rdd.*.prompt.md` files before copying new ones:

```python
def copy_prompts(source_dir: Path, target_dir: Path):
    """Copy prompt files to target"""
    print_info("Installing prompts...")
    
    src_prompts = source_dir / ".github" / "prompts"
    dst_prompts = target_dir / ".github" / "prompts"
    
    dst_prompts.mkdir(parents=True, exist_ok=True)
    
    # Remove all existing rdd.* prompts to ensure clean replacement
    removed = 0
    if dst_prompts.exists():
        for old_prompt in dst_prompts.glob("rdd.*.prompt.md"):
            old_prompt.unlink()
            removed += 1
    
    if removed > 0:
        print_info(f"Removed {removed} existing RDD prompt file(s)")
    
    # Copy new prompts
    copied = 0
    for prompt_file in src_prompts.glob("*.prompt.md"):
        shutil.copy2(prompt_file, dst_prompts / prompt_file.name)
        copied += 1
    
    print_success(f"Installed {copied} prompt file(s)")
```

**Key changes**:
- Added removal step before copying
- Uses `glob("rdd.*.prompt.md")` to match all RDD prompt files
- Unlinks (deletes) each matching file
- Reports number of removed files to user
- Then proceeds with normal copy operation

This ensures that obsolete prompt files from previous releases are removed before installing new ones.

### Step 2: Updated requirements.md

Added new requirement **[FR-99]**: "Prompt Cleanup During Installation - The installer shall remove all existing RDD prompt files (matching pattern rdd.*.prompt.md) from .github/prompts/ before installing new prompt files to ensure clean replacement and removal of obsolete prompts from previous releases"

### Step 3: Updated tech-spec.md

Modified the "Automated file operations" section under "Python Installation (install.py)" to document that the installer removes all existing `rdd.*.prompt.md` files before copying new ones.

### Step 4: Created and executed list-files.py

Created script `.rdd-docs/workspace/list-files.py` which:
- Recursively scans all files and folders in the workspace root
- Excludes directories starting with "."
- Records relative path, type (file/folder), and last modification time
- Outputs results to `.rdd-docs/workspace/files-list.md`

Executed the script successfully:
```bash
python .rdd-docs/workspace/list-files.py
```
Output: "✓ File list written to: .rdd-docs/workspace/files-list.md - Total items: 80"

### Step 5: Created files-analysis.md

Created `.rdd-docs/workspace/files-analysis.md` with:
- Summary of all project directories and their contents
- Description of file types and purposes
- Identification of recent changes (files modified today)
- Notes about generated/cache files excluded from version control

### Step 6: Verified Project Folder Structure in tech-spec.md

Reviewed the "## Project Folder Structure" section in `.rdd-docs/tech-spec.md`. The structure documentation is comprehensive, accurate, and up-to-date with the actual project layout. No updates needed.

## Summary of Changes

1. **Modified scripts/install.py**: Added cleanup of existing `rdd.*.prompt.md` files before installing new prompts
2. **Updated requirements.md**: Added requirement [FR-99] for prompt cleanup during installation
3. **Updated tech-spec.md**: Documented prompt cleanup behavior in installation section
4. **Created workspace scripts**: list-files.py for file inventory
5. **Created workspace documentation**: files-list.md and files-analysis.md for project structure analysis

All changes implement the requirement from prompt P05 to ensure clean replacement of RDD prompt files during installation.

## Completion

Prompt P05 has been successfully completed and marked as done using:
```bash
python .rdd/scripts/rdd.py prompt mark-completed P05
```

The checkbox in `.rdd-docs/workspace/.rdd.copilot-prompts.md` has been updated from `- [ ]` to `- [x]` for P05.

