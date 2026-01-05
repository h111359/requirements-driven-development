# Analysis for P-046: Requirements IDs

## Copilot Review

### Feasibility Assessment
The requested change is **highly feasible** and represents a significant improvement to the framework. The task involves:
1. Modifying the ID generation convention from timestamp-based (YYYYMMDD-HHmm) to sequential numeric format (UR-0001, TR-0001)
2. Updating the convention file to document the new format
3. Migrating all existing requirements to the new ID format

### Potential Risks and Challenges

**High Risk Areas:**
- **Breaking References**: Any external documentation, scripts, or tooling that references specific requirement IDs will break after migration
- **Git History**: Large-scale ID replacement will create a massive diff, making it harder to track actual requirement changes in git blame/history
- **Automation Dependencies**: Any automated scripts that parse or generate requirement IDs must be updated

**Medium Risk Areas:**
- **ID Collision During Migration**: If migration is interrupted, could result in duplicate IDs
- **Parsing Complexity**: Need to reliably extract highest ID from existing requirements to continue sequence
- **Category Assignment**: Some requirements might be miscategorized, affecting ID assignment

**Low Risk Areas:**
- **Convention File Update**: Straightforward documentation change
- **Format Validation**: New format is simpler to validate than timestamp format

### Impact on Existing Functionality

**Direct Impact:**
- All 528 lines of requirements.md will need modification
- Any scripts that generate requirements (if they exist) must be updated
- Web UI requirement display/editing may need adjustments
- Requirement addition workflows must implement new ID generation logic

**Indirect Impact:**
- Release notes and documentation mentioning specific requirement IDs become outdated
- Historical prompts referencing old IDs lose direct traceability
- Git commit messages with requirement IDs won't match current IDs

### Completeness of Prompt Description

**Missing Information:**
- No mention of updating requirement addition scripts/workflows to use new ID format
- Doesn't specify whether to update historical references in other files (prompts, release notes, etc.)
- Doesn't clarify how to handle [DELETED] requirements in the sequence counting
- No guidance on validation strategy after migration
- Unclear whether existing scripts rely on timestamp-based IDs

**Strengths:**
- Clear directive to update both convention and actual requirements
- User has answered detailed questionnaire covering key decisions
- Scope is well-defined and focused

## Best Practices

### Sequential Identifier Best Practices

Based on industry standards and common practices:

**1. Semantic Versioning and Traceability (ISO/IEC/IEEE 29148)**
- Requirements should have unique, stable identifiers
- Sequential numbering is preferred over timestamps for requirements
- IDs should be immutable once assigned
- Format should be consistent and machine-parseable

**2. Requirements Management Best Practices**
- **Prefix-based categorization**: UR/TR prefixes align with industry standards (User Requirements vs Technical Requirements)
- **Zero-padding**: Using fixed-width numbers (0001 vs 1) improves:
  - Visual alignment in documents
  - Lexicographic sorting
  - Professional appearance
  - Parsing reliability
- **Gap tolerance**: Allowing deleted requirements to keep their IDs maintains stability

**3. Migration Strategies**
- **Atomic migration**: All-at-once migration is preferred over gradual for consistency
- **Traceability mapping**: Creating old→new ID mapping aids transition (though user chose not to)
- **Validation**: Post-migration validation ensures no duplicates or gaps

**4. ID Generation Approaches**
- **File scanning**: Reading existing file to determine next ID is simpler and more robust than maintaining separate registry
- **Simplicity over optimization**: For typical requirement counts (< 1000), file scanning performance is negligible

## Samples from GitHub

### Example 1: Linux Kernel Requirements (Documentation/)
While the Linux kernel doesn't maintain a formal requirements.md, their Documentation/process/ files use similar sequential numbering for coding standards and process guidelines. They use simple numeric identifiers without padding.

### Example 2: OpenStack Requirements
OpenStack projects use sequential bug/story IDs in their tracking systems. Format is typically `#123456` without category prefixes, but the sequential approach matches this proposal.

### Example 3: Automotive SPICE (ASPICE) Requirement IDs
Format: `SWE.1-REQ-001`, `SWE.2-REQ-002`
- Shows category prefix (SWE.1, SWE.2)
- Uses 3-digit zero-padding
- Strictly sequential within categories
This closely mirrors the chosen approach.

### Example 4: NASA Software Requirements
NASA uses formats like `SRD-001`, `ICD-042`
- Document type prefix (SRD = Software Requirements Document)
- Zero-padded sequential numbers
- Typically 3-4 digit padding for large projects

### Common Patterns Observed:
- Prefix for categorization (UR/TR is good)
- Sequential numbering within categories
- Fixed-width padding (3-4 digits most common)
- Migration done atomically when needed
- Simple text file storage for traceability

## Proposals

### Alternative Implementation Strategies

**Option A: Full Migration with Mapping File (Rejected by User)**
Create a `requirement-id-mapping.json` file:
```json
{
  "UR-20251224-0901": "UR-0001",
  "UR-20251224-0902": "UR-0002"
}
```
**Pros**: External references can be updated programmatically, full traceability
**Cons**: Extra file to maintain, additional complexity
**Recommendation**: User chose not to do this (Q3 answer B), which is acceptable for internal-only requirements

**Option B: Hybrid Format During Transition (Rejected by User)**
Keep old IDs but add new IDs as comments:
```markdown
- [UR-0001] <!-- was: UR-20251224-0901 --> Description
```
**Pros**: Maintains reference to old IDs temporarily
**Cons**: Cluttered format, requires cleanup later
**Recommendation**: Not needed based on user's choice for clean migration

**Option C: Chosen Approach - Direct Migration**
- Scan requirements file
- Count requirements by category (UR/TR)
- Assign sequential IDs starting from 0001 in order of appearance
- Use 4-digit padding (per Q5 answer)
- No mapping file

**Pros**: Clean result, simple implementation, consistent format
**Cons**: Loses timestamp information, breaks external references
**Recommendation**: ✅ This aligns with user choices and is the right approach

### Suggested Requirement Modifications

Based on the prompt, the following requirements should be **added**:

**New User Requirements:**
```markdown
- [UR-XXXX] The framework shall use sequential numeric requirement identifiers with category prefixes (UR, TR) and 4-digit zero-padding to ensure unique, compact, and easily referenceable requirement IDs

- [UR-XXXX] The framework shall determine the next available requirement ID by scanning the existing requirements file to find the highest ID in each category, ensuring uniqueness without requiring separate state tracking
```

**New Technical Requirements:**
```markdown
- [TR-XXXX] Requirement IDs shall follow the format <PREFIX>-<NUMBER> where PREFIX is UR or TR and NUMBER is a 4-digit zero-padded sequential integer (e.g., UR-0001, TR-0042)

- [TR-XXXX] The requirements convention file shall specify the requirement ID format, padding rules, and uniqueness guarantees to ensure consistent ID generation across all framework operations

- [TR-XXXX] Requirement ID generation shall scan requirements.md using regex pattern `\[(UR|TR)-(\d+)\]` to extract existing IDs and calculate the next available ID per category
```

### Trade-offs Between Different Approaches

**4-digit vs 3-digit Padding:**
- User chose 4-digit (Q5 answer B)
- **Trade-off**: More verbose (UR-0001 vs UR-001) but future-proof
- **Assessment**: Reasonable choice for a framework meant to evolve
- **Recommendation**: Accept user's choice

**Scanning vs Registry File:**
- User chose scanning (Q2 answer C)
- **Trade-off**: Slightly slower (negligible) but more robust
- **Assessment**: Excellent choice - eliminates state synchronization issues
- **Recommendation**: Strongly support this choice

**Migration Timing:**
- User chose immediate full migration (Q3 answer B)
- **Trade-off**: Large one-time effort vs ongoing inconsistency
- **Assessment**: Right choice for internal tool with good git history
- **Recommendation**: Proceed with full migration

## Prompt Modification

If I were writing this prompt, here's how I would structure it:

---

### Improved Prompt: Migrate Requirements to Sequential ID Format

**Context:**
The current requirements file uses timestamp-based IDs (format: `UR-YYYYMMDD-HHmm`), which creates collision risks when adding multiple requirements within the same minute and makes requirement counts non-obvious. This prompt implements migration to sequential numeric IDs based on approved questionnaire answers.

**Objectives:**
1. Update the requirements convention file to document sequential ID format
2. Implement ID generation logic by scanning existing requirements
3. Migrate all existing requirements to new ID format
4. Validate migration results

**Requirements:**
- ID Format: `<PREFIX>-<NUMBER>` where PREFIX ∈ {UR, TR} and NUMBER is 4-digit zero-padded (e.g., UR-0001, TR-0183)
- ID Generation: Scan requirements.md, extract max ID per category, increment by 1
- Migration Strategy: One-time full migration preserving requirement order
- Starting IDs: First UR = UR-0001, first TR = TR-0001 (sequential from actual count)

**Implementation Steps:**
1. **Update Convention File** (`.rdd/conventions/requirements.convention.md`)
   - Replace timestamp-based ID format documentation with sequential format
   - Specify 4-digit padding requirement
   - Document ID generation approach (file scanning)
   - Add regex pattern for ID extraction: `\[(UR|TR)-(\d{4})\]`

2. **Migrate Requirements File** (`.rdd-instance/specifications/requirements.md`)
   - Parse file section by section (Product Name, Overview, Definitions, UR, TR)
   - For each requirement line matching `- \[(UR|TR)-\d+-\d+\]`:
     - Track category (UR or TR)
     - Assign sequential ID starting from 0001 per category
     - Replace old ID with new ID: `- [UR-0042] Description...`
   - Handle [DELETED] requirements: keep their IDs but don't count in sequence
   - Preserve all other content exactly (descriptions, sections, formatting)

3. **Validation**
   - Verify no duplicate IDs exist
   - Confirm all requirements have valid format `[UR|TR-\d{4}]`
   - Count requirements: ensure last ID matches total count
   - Spot-check: first, middle, last requirements in each category

4. **Documentation**
   - Add comment in requirements.md header noting migration date
   - Update this implementation file with migration statistics (counts, etc.)

**Success Criteria:**
- Convention file accurately describes new ID format
- All requirements have sequential IDs with 4-digit padding
- No duplicate IDs exist
- Requirement order preserved from original file
- UR IDs: UR-0001 through UR-XXXX (where XXXX = current UR count)
- TR IDs: TR-0001 through TR-YYYY (where YYYY = current TR count)

**Files to Modify:**
- `.rdd/conventions/requirements.convention.md` - Update ID format specification
- `.rdd-instance/specifications/requirements.md` - Migrate all requirement IDs

**Out of Scope:**
- Updating references to old IDs in other files (prompts, release notes, etc.)
- Creating mapping file from old to new IDs
- Updating scripts or tools that might parse requirement IDs (to be handled separately)

**Notes:**
- This is a breaking change for any external ID references
- Git history will show large diff - this is expected and acceptable
- Migration is irreversible - ensure backup exists (git commit before executing)

---

### Key Improvements in Refined Prompt:

1. **Explicit Context**: Explains *why* the change is needed
2. **Clear Scope**: Defines what's in-scope and out-of-scope
3. **Step-by-Step Plan**: Breaks down implementation into logical phases
4. **Validation Criteria**: Specific checks to ensure success
5. **Success Metrics**: Quantifiable outcomes
6. **Risk Acknowledgment**: Notes about breaking changes and git history
7. **Structured Format**: Uses headers and lists for clarity
8. **Regex Specification**: Provides exact patterns for parsing
9. **Edge Cases**: Mentions [DELETED] requirements handling
10. **Verification Steps**: Built-in validation approach
