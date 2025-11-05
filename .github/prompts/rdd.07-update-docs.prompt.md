````prompt
# RDD: Update Documentation

## Purpose
Update project documentation to reflect changes made during the current fix/enhancement work.

## Context
Changes have been documented in `.rdd-docs/workspace/.rdd.copilot-prompts.md`. This prompt ensures all main documentation files reflect those changes accurately.

## Instructions

**S01: Analyze Changes**

1. Read `.rdd-docs/workspace/.rdd.copilot-prompts.md` to identify completed prompts (marked with `[x]`)
2. For each completed prompt, extract:
   - What was changed (files, functions, behavior)
   - What was added (new files, features)
   - What was removed (deleted files, deprecated features)

**S02: Gather Context**

Read the following to understand current implementation:
- All files in `.github/prompts/` - understand workflow prompts
- All files in `.rdd/scripts/` - understand Python script implementation (`rdd.py` and `rdd_utils.py`)
- All files in `.rdd/templates/` - understand template structure

**S03: Identify Documentation Updates**

Determine which documentation sections need updates:
- **Requirements changes**: New/modified/deleted requirements → `.rdd-docs/requirements.md`
- **Technical changes**: Architecture, scripts, file structure → `.rdd-docs/tech-spec.md`
- **Folder structure changes**: New/moved/deleted files → `.rdd-docs/folder-structure.md`
- **Data model changes**: Config files, data structures → `.rdd-docs/data-model.md`

**S04: Update Requirements.md**

For `.rdd-docs/requirements.md`:

1. **Adding new requirements**:
   - Find the highest ID in the target section (GF/FR/NFR/TR)
   - Add new requirement with next sequential ID
   - Format: `- **[ID] Title**: Description`

2. **Modifying existing requirements**:
   - Locate requirement by ID
   - Update description while preserving ID and structure
   - Keep format: `- **[ID] Title**: Description`

3. **Deleting requirements**:
   - **DO NOT delete the requirement line**
   - Replace content with: `- **[ID] [DELETED]`
   - This preserves ID sequence and shows audit trail

**S05: Update Tech-Spec.md**

For `.rdd-docs/tech-spec.md`:

1. Update relevant sections (System Overview, Architecture, etc.)
2. Add new sections if needed
3. Preserve existing structure and section hierarchy
4. Use clear, technical language

**S06: Update Folder-Structure.md**

For `.rdd-docs/folder-structure.md`:

1. Update the ASCII tree structure if files/folders changed
2. Add descriptions for new directories
3. Update "Key Principles" if workflow changed
4. Maintain consistent formatting with existing structure

**S07: Update Data-Model.md**

For `.rdd-docs/data-model.md`:

1. Document new config file structures (e.g., `.rdd.[fix|enh].<branch-name>`)
2. Update JSON schemas if changed
3. Document file naming conventions
4. Preserve existing model documentation

**S08: Validate Updates**

Before completing:
1. Verify all ID sequences are continuous (no gaps unless intentional deletions)
2. Ensure deleted requirements show `[DELETED]` marker
3. Check that cross-references between docs are updated
4. Confirm formatting consistency with existing content

## Important Guidelines

- **Preserve ID sequences**: Never renumber existing requirement IDs
- **Mark deletions**: Use `[DELETED]` instead of removing lines
- **Maintain structure**: Keep section hierarchy and formatting
- **Be precise**: Only update what changed, don't rewrite unnecessarily
- **Sequential IDs**: When adding requirements, continue from highest existing ID in that section
- **Cross-reference check**: If a requirement references another by ID, ensure the reference is still valid

## Example: Handling Deletions

❌ **Wrong** - Deleting the line:
```markdown
- **[FR-11] Old Feature**: Description of old feature
- **[FR-12] Next Feature**: Description
```

✅ **Correct** - Marking as deleted:
```markdown
- **[FR-11] [DELETED]
- **[FR-12] Next Feature**: Description
```

## Example: Adding Requirements

If highest FR is [FR-41], add new requirements as:
```markdown
- **[FR-42] New Feature Name**: Description of new feature
- **[FR-43] Another Feature**: Description of another feature
```     