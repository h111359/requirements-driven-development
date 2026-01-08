# Implementation Plan for P-046: Requirements IDs

## Overview
This plan implements the migration from timestamp-based requirement IDs to sequential numeric IDs with 4-digit padding, based on the questionnaire answers and analysis completed. The plan covers updating the convention file, migrating all existing requirements, and ensuring compliance with framework requirements.

## Step 1: Update Requirements Convention File

**File:** `.rdd/conventions/requirements.convention.md`

**Actions:**
- Replace the current ID format specification that describes timestamp-based IDs (YYYYMMDD-HHmm) with the new sequential numeric format
- Update the "Requirement Format" section to specify: `[<Prefix>-<Number>]` where Number is a 4-digit zero-padded sequential integer
- Modify the ID component description from timestamp format to: "4-digit zero-padded sequential number starting from 0001 (e.g., 0001, 0042, 0183, 1247)"
- Add documentation for ID generation approach: "The next available ID is determined by scanning the requirements file to find the highest existing ID in each category (UR, TR) and incrementing by 1"
- Update all examples throughout the convention file to use the new format (e.g., `UR-0001` instead of `UR-20251224-0901`)
- Add a regex pattern for ID validation: `\[(UR|TR)-(\d{4})\]`
- Document the 4-digit padding requirement and its rationale (supports up to 9999 requirements per category, ensures consistent visual alignment)

**Rationale:** The convention file serves as the authoritative reference for requirement formatting and must be updated before migrating the actual requirements to ensure consistency.

## Step 2: Count Existing Requirements by Category

**File:** `.rdd-instance/specifications/requirements.md`

**Actions:**
- Parse the requirements file section by section (Product Name, Product Overview, Definitions, User Requirements, Technical Requirements)
- Identify all requirement lines matching the pattern `- \[(UR|TR)-[0-9]{8}-[0-9]{4}\]` (current timestamp format)
- Count requirements in each category:
  - Count all lines starting with `- [UR-` in the User Requirements section (excluding [DELETED] entries from the count)
  - Count all lines starting with `- [TR-` in the Technical Requirements section (excluding [DELETED] entries from the count)
- Record the counts to determine the ID range (UR-0001 through UR-XXXX and TR-0001 through TR-YYYY)

**Rationale:** Understanding the total count ensures proper sequential assignment and validates the migration is complete.

## Step 3: Migrate User Requirements IDs

**File:** `.rdd-instance/specifications/requirements.md`

**Actions:**
- Process the "## User Requirements" section
- For each requirement line matching `- \[UR-[0-9]{8}-[0-9]{4}\]`:
  - Assign sequential ID starting from UR-0001
  - Replace the old ID with new format: `- [UR-0001]`, `- [UR-0002]`, etc.
  - Increment counter for next requirement
  - Preserve the entire description text after the ID exactly as-is
- For [DELETED] requirements:
  - Replace old ID with new sequential ID
  - Keep the [DELETED] marker in the description
  - Do NOT skip the sequence number (deleted requirements keep their sequence position)
- Maintain exact formatting, indentation, and line breaks
- Do not modify any other content in the section

**Example transformation:**
```
OLD: - [UR-20251224-0901] The framework shall define RDD...
NEW: - [UR-0001] The framework shall define RDD...

OLD: - [UR-20251229-1841] [DELETED]
NEW: - [UR-0086] [DELETED]
```

**Rationale:** Sequential processing ensures each requirement gets a unique, consecutive ID while preserving the original order and content.

## Step 4: Migrate Technical Requirements IDs

**File:** `.rdd-instance/specifications/requirements.md`

**Actions:**
- Process the "## Technical Requirements" section
- For each requirement line matching `- \[TR-[0-9]{8}-[0-9]{4}\]`:
  - Assign sequential ID starting from TR-0001
  - Replace the old ID with new format: `- [TR-0001]`, `- [TR-0002]`, etc.
  - Increment counter for next requirement
  - Preserve the entire description text after the ID exactly as-is
- For [DELETED] requirements:
  - Replace old ID with new sequential ID
  - Keep the [DELETED] marker in the description
  - Do NOT skip the sequence number
- Maintain exact formatting, indentation, and line breaks
- Do not modify any other content in the section

**Rationale:** Technical requirements follow the same migration pattern as user requirements but with separate TR prefix and independent sequence.

## Step 5: Validate Migration Results

**Actions:**
- Scan the migrated requirements.md file
- Verify all requirement IDs match the new format pattern: `\[(UR|TR)-\d{4}\]`
- Check for duplicate IDs within each category
- Confirm sequential numbering with no gaps (except intentionally for deleted items which still hold their sequence position)
- Verify the last ID in each category matches the total count:
  - If there are 178 UR entries, last should be UR-0178
  - If there are 45 TR entries, last should be TR-0045
- Spot-check random requirements to ensure descriptions were not altered
- Verify no old timestamp-format IDs remain

**Success Criteria:**
- Zero duplicate IDs
- All IDs match format `[UR|TR-\d{4}]`
- Sequential numbering verified
- No content changes except IDs

**Rationale:** Validation ensures migration integrity and catches any parsing or replacement errors.

## Step 6: Update Requirements File with New Requirements

**File:** `.rdd-instance/specifications/requirements.md`

**Actions:**
Add the following new requirements to document the sequential ID approach:

**New User Requirements (to be added in User Requirements section):**

```markdown
- [UR-XXXX] The framework shall use sequential numeric requirement identifiers with category prefixes (UR, TR) and 4-digit zero-padding to ensure unique, compact, and easily referenceable requirement IDs

- [UR-XXXX] The framework shall determine the next available requirement ID by scanning the existing requirements file to find the highest ID in each category, ensuring uniqueness without requiring separate state tracking
```

**New Technical Requirements (to be added in Technical Requirements section):**

```markdown
- [TR-XXXX] Requirement IDs shall follow the format <PREFIX>-<NUMBER> where PREFIX is UR or TR and NUMBER is a 4-digit zero-padded sequential integer (e.g., UR-0001, TR-0042)

- [TR-XXXX] The requirements convention file shall specify the requirement ID format, padding rules, and uniqueness guarantees to ensure consistent ID generation across all framework operations

- [TR-XXXX] Requirement ID generation shall scan requirements.md using regex pattern `\[(UR|TR)-(\d{4})\]` to extract existing IDs and calculate the next available ID per category
```

Where XXXX is the next sequential number after the last migrated ID in each respective category.

**Rationale:** These requirements formally document the new ID system and generation approach, ensuring future compliance and providing reference for anyone working with requirements.

## Step 7: Add Migration Note to Requirements File

**File:** `.rdd-instance/specifications/requirements.md`

**Actions:**
- Add a comment near the top of the file (after Product Name but before Product Overview) documenting the migration
- Format as a Markdown comment or note section
- Include migration date: January 4, 2026
- Note the change from timestamp-based to sequential IDs
- Mention that git history preserves old IDs for traceability

**Example text:**
```markdown
<!-- 
Migration Note: On January 4, 2026, requirement IDs were migrated from timestamp-based 
format (UR-YYYYMMDD-HHmm) to sequential numeric format (UR-0001, TR-0001). 
Git history preserves original IDs for traceability.
-->
```

**Rationale:** Future readers will understand the ID format change and know where to find historical IDs if needed.

## Step 8: Verify Compliance with Framework Requirements

**Actions:**
Review the following framework requirements to ensure the plan fulfills them:

- **[UR-20251224-0903]**: "The framework shall load, apply, and update `requirements file` automatically during each prompt execution"
  - ✅ Covered: This plan updates the requirements file as part of prompt execution
  
- **[UR-20251224-0912]**: "The framework must maintain a `requirements file` and automatically update it after each prompt execution"
  - ✅ Covered: Step 6 adds new requirements documenting the ID system

- **No requirement deletion allowed per execution.md**: "Never delete already added requirements rows"
  - ✅ Covered: Migration preserves all requirements, only changes IDs, maintains [DELETED] markers

- **Convention compliance**: "Maintain existing structure and formatting of requirements.md - it should be accordingly the convention in requirements.convention.md"
  - ✅ Covered: Steps 1-4 update convention first, then migrate to match it

- **Requirement format**: "Each requirement follows this format: - [<Prefix>-<ID>] <Description>"
  - ✅ Covered: New format maintains this structure with improved ID format

**Rationale:** Ensures the plan aligns with all framework requirements and policies.

## Step 9: Document Implementation Statistics

**Actions:**
In the implementation.md file (during execution phase), record:
- Total number of UR requirements migrated
- Total number of TR requirements migrated
- Number of [DELETED] requirements encountered
- ID range for each category (e.g., UR-0001 to UR-0178)
- Any issues or edge cases encountered
- Validation results (duplicate check, format check, sequence check)

**Rationale:** Provides traceability and documentation of the migration process for future reference.

## Execution Sequence Summary

1. Update convention file with new ID format specification
2. Count existing requirements to determine migration scope
3. Migrate all User Requirements IDs sequentially
4. Migrate all Technical Requirements IDs sequentially
5. Validate migration integrity and completeness
6. Add new requirements documenting the ID system
7. Add migration note for future reference
8. Verify framework requirements compliance
9. Document migration statistics in implementation file

## Files Modified

- `.rdd/conventions/requirements.convention.md` - ID format specification updated
- `.rdd-instance/specifications/requirements.md` - All requirement IDs migrated + new requirements added

## Out of Scope

The following items are explicitly out of scope for this prompt:
- Updating references to old requirement IDs in other files (prompts, release notes, historical documents)
- Creating a mapping file from old IDs to new IDs
- Modifying scripts that parse or generate requirement IDs (to be handled in future prompts if needed)
- Updating git commit messages that reference old requirement IDs

## Success Criteria

- ✅ Convention file documents sequential 4-digit format with examples
- ✅ All requirements have format `[UR|TR-\d{4}]`
- ✅ No duplicate IDs exist
- ✅ Sequential numbering verified (UR-0001, UR-0002... TR-0001, TR-0002...)
- ✅ Last ID matches total count per category
- ✅ No requirement descriptions modified (except ID portion)
- ✅ New requirements added documenting the ID system
- ✅ Migration note added to requirements file
- ✅ All framework requirements observed
