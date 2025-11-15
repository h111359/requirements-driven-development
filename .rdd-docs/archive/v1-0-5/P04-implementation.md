# P04 Implementation: Consolidate folder-structure.md and data-model.md into tech-spec.md

## Task Description
The files `.rdd-docs/folder-structure.md` and `.rdd-docs/data-model.md` should not exist as files anymore, but the information should be part of `.rdd-docs/tech-spec.md` and should be maintained up to date after each prompt there. All references to these files should be replaced with references to sections in tech-spec.md.

## Implementation Steps

### Step 1: Analyze Current State
Reading current files:
- `.rdd-docs/folder-structure.md` - Contains project folder structure documentation
- `.rdd-docs/data-model.md` - Contains data model and configuration schemas
- `.rdd-docs/tech-spec.md` - Current technical specification
- `templates/tech-spec.md` - Template file (already modified manually per requirements)

The template already has placeholders for:
- "## Project Folder Structure" section
- "## Data Architecture" section

### Step 2: Files to Update
According to the prompt, need to update references in:
- .github/prompts/rdd.execute.prompt.md
- .rdd/scripts/rdd.py
- .rdd-docs/requirements.md
- .rdd-docs/tech-spec.md
- scripts/build.py
- scripts/install.py
- templates/user-guide.md
- tests/build/conftest.py
- tests/build/test_build.py
- tests/python/conftest.py

### Step 3: Execution Plan
1. Update `.rdd-docs/tech-spec.md` to include content from folder-structure.md and data-model.md
2. Update all references in the files listed above
3. Update documentation files (requirements.md, tech-spec.md)
4. The actual deletion of folder-structure.md and data-model.md will be handled after all references are updated

## Detailed Execution

### ✅ Step 1: Update tech-spec.md
**Status**: Completed

Updated `.rdd-docs/tech-spec.md` to include:
- Added "## Data Architecture" section with complete config.json schema from data-model.md
- Replaced simple folder structure with complete detailed structure from folder-structure.md
- Added key principles from folder-structure.md
- Sections now at lines 685-940 (approximately)

### ✅ Step 2: Update References in Files
**Status**: Completed

Updated all references in:
- ✅ .github/prompts/rdd.execute.prompt.md - Updated context reading and documentation update steps
- ✅ .rdd-docs/requirements.md - Updated FR-63 and TR-50 to remove data-model.md and folder-structure.md
- ✅ scripts/build.py - Removed data-model.md and folder-structure.md from seed_templates list
- ✅ scripts/install.py - Removed data-model.md and folder-structure.md from seed_files list
- ✅ templates/user-guide.md - Updated all references to point to tech-spec.md sections
- ✅ tests/build/conftest.py - Updated to create only tech-spec.md with sections
- ✅ tests/build/test_build.py - Removed assertions for data-model.md and folder-structure.md
- ✅ tests/python/conftest.py - Updated to create only tech-spec.md with sections

Note: .rdd/scripts/rdd.py had no references to these files.

### ✅ Step 3: Handle Template Files
**Status**: Completed

Deleted obsolete files:
- ✅ templates/data-model.md - Removed (content now in templates/tech-spec.md)
- ✅ templates/folder-structure.md - Removed (content now in templates/tech-spec.md)
- ✅ .rdd-docs/data-model.md - Removed (content now in .rdd-docs/tech-spec.md)
- ✅ .rdd-docs/folder-structure.md - Removed (content now in .rdd-docs/tech-spec.md)

Command used: `rm <file-paths>`

### ✅ Step 4: Update Documentation
**Status**: Completed

Updated documentation files:
- ✅ .rdd-docs/requirements.md - Added FR-98 to document the consolidation change
- ✅ .rdd-docs/tech-spec.md - Already updated in Step 1 with Data Architecture and Project Folder Structure sections

## Summary

Successfully completed P04 prompt execution:

1. **Consolidated documentation**: Merged content from folder-structure.md and data-model.md into tech-spec.md as dedicated sections
2. **Updated all references**: Modified 10+ files to reference tech-spec.md sections instead of separate files
3. **Removed obsolete files**: Deleted data-model.md and folder-structure.md from both templates/ and .rdd-docs/ directories
4. **Updated requirements**: Added FR-98 to document this architectural change
5. **Updated tests**: Modified test fixtures to match new structure

All references now point to:
- "## Data Architecture" section in tech-spec.md (instead of data-model.md)
- "## Project Folder Structure" section in tech-spec.md (instead of folder-structure.md)

Files modified:
- .github/prompts/rdd.execute.prompt.md
- .rdd-docs/requirements.md
- .rdd-docs/tech-spec.md
- scripts/build.py
- scripts/install.py
- templates/user-guide.md
- tests/build/conftest.py
- tests/build/test_build.py
- tests/python/conftest.py

Files deleted:
- templates/data-model.md
- templates/folder-structure.md
- .rdd-docs/data-model.md
- .rdd-docs/folder-structure.md

