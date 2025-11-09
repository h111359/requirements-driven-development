# P01 - User Guide Implementation

## Prompt Description
Create a file `templates/user-guide.md` which explains in detail how users should work with the RDD framework, including the different options and the process to be followed.

## Analysis Phase

### Files to Read
Reading the following files to understand the framework:
- README.md
- .rdd-docs/requirements.md
- .rdd/scripts/rdd.py
- .rdd/scripts/rdd_utils.py
- .github/prompts/rdd.06-execute.prompt.md
- .github/prompts/rdd.08-document.prompt.md

### Key Findings from Analysis

#### From README.md
- Framework provides structured documentation, guided workflows, AI optimization
- Installation via release archives with Python installer
- Quick Start: 0. Prerequisites → 1. Create iteration → 2. Define prompts → 3. Update docs → 4. Complete iteration
- Terminal menu options: Create/Update/Complete/Delete

#### From requirements.md
- Simplified iteration workflow with 4 options (FR-78)
- Safety checks for create/complete operations (FR-79, FR-80)
- Branch naming with kebab-case normalization (FR-81)
- Workspace initialization with only copilot-prompts.md (FR-82)
- Iteration completion includes archiving, committing, pushing (FR-83, FR-84, FR-85)
- Branch cleanup workflow for merged branches (FR-86, FR-87)
- Interactive menu with numeric navigation (FR-75)

#### From rdd.py
- Main menu loop with 4 options
- Create iteration: checks default branch, empty workspace, prompts for branch name
- Update from default: stashes changes, pulls, merges, restores stash
- Complete iteration: archives workspace, commits, pushes, returns to default branch
- Delete merged branches: interactive cleanup of merged branches

#### From rdd_utils.py
- Colored output functions for user feedback
- Git operations: branch management, stashing, merging
- Configuration management for defaultBranch, localOnly mode
- Prompt marking: mark_prompt_completed function

#### From prompts
- rdd.06-execute: Execute stand-alone prompts from workspace
- rdd.08-document: Update documentation after changes

### Workflow Understanding

The complete user workflow is:
1. **Setup**: Install RDD, configure, populate requirements/tech-spec
2. **Create Iteration**: From default branch with empty workspace
3. **Define Work**: Edit .rdd.copilot-prompts.md with prompts
4. **Execute Prompts**: Use `/rdd.06-execute P##` in Copilot chat
5. **Update (Optional)**: Sync with default branch changes via menu option
6. **Document**: Use `/rdd.08-document` to update docs
7. **Complete**: Archive, commit, push via menu option
8. **PR & Merge**: Create PR on GitHub, merge after review
9. **Cleanup**: Delete merged branches via menu option

## Implementation

Creating templates/user-guide.md with comprehensive user documentation...

## Changes Made

### 1. Created templates/user-guide.md
- **Location**: `/templates/user-guide.md`
- **Size**: Comprehensive 800+ line guide
- **Structure**:
  - Overview and key concepts
  - Prerequisites and installation
  - Complete workflow explanation
  - Terminal menu detailed guide (all 4 options)
  - Working with Copilot prompts
  - Complete workflow example (user profile feature)
  - Best practices (10 recommendations)
  - Troubleshooting (10 common issues with solutions)
  - Command reference appendix

### 2. Content Highlights
- **Workflow Cycle**: Visual diagram of RDD iteration cycle
- **Menu Options**: Detailed explanation of each menu option with prerequisites
- **Prompt Writing**: Guidelines for effective prompts with good/bad examples
- **Complete Example**: Step-by-step walkthrough of adding a user profile feature
- **Troubleshooting**: Solutions for 10 most common issues users face

### 3. Updated Install Scripts

#### Modified: scripts/install.py
**Function**: `copy_rdd_framework()`

**Changes**:
- Added code to copy `user-guide.md` from `templates/` to `.rdd/` during installation
- Added success/warning messages for user feedback
- Copies after the main .rdd directory is copied, ensuring user-guide.md is available in installed projects

**Location in file**: After line with `rdd_script.chmod(0o755)`

**Code added**:
```python
# Copy user-guide.md to .rdd directory
src_user_guide = source_dir / "templates" / "user-guide.md"
if src_user_guide.exists():
    dst_user_guide = dst_rdd / "user-guide.md"
    shutil.copy2(src_user_guide, dst_user_guide)
    print_info("  Copied user-guide.md to .rdd/")
else:
    print_warning("  user-guide.md not found in templates/")
```

**Result**: User guide is now automatically installed to `.rdd/user-guide.md` during framework installation, making it accessible to all users who install RDD.

### 4. Testing Plan
- Build release with updated install.py
- Test installation on clean project
- Verify user-guide.md appears in .rdd/ after installation
- Verify content is readable and properly formatted

### 5. Summary
✅ Created comprehensive user-guide.md (800+ lines)
✅ Updated install.py to copy user-guide.md during installation
✅ User guide will be accessible at `.rdd/user-guide.md` in all installations
✅ Prompt P01 completed successfully
