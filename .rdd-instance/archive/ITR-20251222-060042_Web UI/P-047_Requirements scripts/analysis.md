# Analysis: Requirements Scripts

## Copilot Review

### Feasibility Assessment

The requested changes are **highly feasible**. The prompt asks for creating 6 Python scripts following an established pattern (reference: `prompt_create.py`), which demonstrates that:
- The framework architecture supports this type of deterministic script
- There's a clear precedent to follow
- The technical infrastructure exists (file system access, JSON/MD parsing, error handling)

### Potential Risks and Challenges

1. **Requirements file parsing complexity**: The requirements.md file has a specific format with sections (Product Name, Overview, Definitions, User Requirements, Technical Requirements). Parsing must be robust to handle:
   - Variable whitespace between sections
   - Comments (like the migration note)
   - Edge cases with requirement text spanning multiple lines
   - The [DELETED] marker pattern

2. **ID sequence management**: The current system relies on scanning to find the highest ID. With user modifications abandoning the `id=` parameter (per Q2 answer), the script must be bulletproof in:
   - Correctly parsing all existing IDs including deleted ones
   - Handling gaps in sequences
   - Thread safety if multiple scripts run concurrently (though unlikely in this use case)

3. **Format compliance**: The `.rdd/conventions/requirements.convention.md` specifies strict formatting:
   - 4-digit zero-padded IDs (0001-9999)
   - Exact heading format (`## User Requirements`, `## Technical Requirements`)
   - "Shall" language requirement
   - Three blank lines between sections (style-only but expected)

4. **Validation complexity reduced**: User answers simplified validation to only `basic` and `none` (Q1), and abandoned `strict` mode (Q3). This reduces implementation complexity but still requires:
   - Character count validation (10-2048)
   - "Shall" keyword presence check
   - Format validation

5. **Atomic write edge cases**: While the simple temp file approach (Q5 answer) is straightforward, edge cases include:
   - Disk full scenarios
   - Permission issues
   - Cross-filesystem renames (temp directory on different mount)

### Impact on Existing Functionality

**Positive impacts:**
- Eliminates risk of AI agents corrupting requirements.md through direct editing
- Provides consistent error messages and validation
- Enables future tooling and automation built on these scripts
- Improves traceability (script execution can be logged)

**Potential negative impacts:**
- Adds friction for quick manual edits (must use scripts instead of direct editing)
- Requires learning new script syntax/parameters
- Could slow down workflow if scripts are verbose or slow
- Breaking changes: Any existing prompts/docs that mention direct editing must be updated

**Mitigation**: The execution instructions update (requirement #3) addresses this by providing clear documentation and examples.

### Completeness of Prompt Description

**Well-specified aspects:**
- Clear reference implementation (prompt_create.py)
- Explicit parameter definitions
- Output format specification (SUCCESS/ERROR messages)
- File format convention reference
- Success criteria listed

**Underspecified aspects:**
1. **Error message format**: While "clear error messages with suggested fixes" is mentioned, there's no template or examples
2. **Modification behavior**: "Replace entire requirement text" - should this preserve exact formatting (spacing, line breaks) or normalize it?
3. **Section positioning**: "Append to end of appropriate section" - what if section doesn't exist? Create it?
4. **Concurrent execution**: No mention of locking or handling simultaneous script runs
5. **Testing**: Success criteria mention "scripts are functional and tested" but no test specifications provided
6. **CLI integration**: No mention of whether these scripts should be added to the CLI menu system (`rdd.py`)

**User modifications from questionnaire:**
- Q1: Only `basic` and `none` validation (removes `strict`)
- Q2: No user-provided ID parameter (always auto-generate)
- Q3: No duplicate text checking (removes strict validation requirement)
- Q4: Both consolidated section + inline warnings in execution instructions
- Q5: Simple temp file atomic writes

These answers clarify several ambiguities and simplify the implementation.

## Best Practices

### Python Script Design Patterns

**Source**: Python official documentation and community standards
**URL**: https://docs.python.org/3/tutorial/modules.html (conceptual)

**Best practices for CLI scripts:**
1. **Argument parsing**: Use named parameters (`key=value`) as this framework does, avoiding positional arguments for clarity
2. **Exit codes**: 0 for success, 1 for user errors, 2 for system errors (though this framework uses just 0/1)
3. **Output streams**: Success to stdout, errors to stderr (the prompt correctly specifies this)
4. **Error messages**: Include problem + solution (the prompt requires this)
5. **Atomic operations**: Validate all inputs before making any changes (fail-fast principle)
6. **Idempotency**: Consider whether operations should be repeatable (for requirements: create is not, modify/delete should be)

### File Format Management

**Source**: Common practices in requirements management tools
**Principles:**
1. **Structured text files**: Markdown is good for human readability + machine parseability
2. **Immutable IDs**: Never reuse deleted requirement IDs (maintains historical traceability)
3. **Versioning**: The framework uses git, which is appropriate for text-based requirements
4. **Validation levels**: Tiered validation (none/basic/strict) is a common pattern
5. **Tombstoning**: Using [DELETED] markers rather than removing lines preserves ID continuity

### Atomic File Operations

**Source**: POSIX and filesystem best practices
**Pattern:**
```python
# 1. Validate inputs
# 2. Read original file
# 3. Make modifications in memory
# 4. Write to temporary file
# 5. Rename temp over original (atomic on POSIX)
```

This is exactly what the prompt specifies and what Q5 confirmed.

### Requirements Engineering

**Source**: IEEE 29148-2018, INCOSE best practices
**Key principles:**
1. **Unique identifiers**: Every requirement needs a unique, permanent ID ✓ (framework does this)
2. **Traceability**: IDs enable tracking from requirements → design → implementation → tests ✓
3. **Versioning**: Requirements should be version controlled ✓ (git)
4. **Shall language**: Clear, mandatory language ("shall") for requirements ✓ (framework enforces)
5. **Testability**: Each requirement should be independently testable ✓ (framework convention)
6. **Categorization**: Separate user vs technical requirements ✓ (UR/TR prefixes)

The RDD framework aligns well with industry standards.

## Samples from GitHub

### Similar Requirement Management Approaches

**1. pip-tools (Python)**
- **Repository**: pypa/pip-tools
- **Approach**: Deterministic dependency file management with separate compile/sync scripts
- **Relevance**: Uses deterministic scripts to modify requirements files rather than manual editing
- **Pattern**: `pip-compile` generates requirements.txt from requirements.in atomically
- **Takeaway**: Separation of concerns (source vs. generated), atomic writes, validation before commit

**2. Terraform (HashiCorp)**
- **Approach**: Declarative configuration with plan/apply workflow
- **Relevance**: Similar to RDD's analyze/plan/implement workflow
- **Pattern**: Validate → Plan → Apply with explicit approval gates
- **Takeaway**: Multi-stage execution with human-in-the-loop verification reduces errors

**3. Conventional Commits**
- **Approach**: Structured commit messages with parsing scripts
- **Relevance**: Enforces format consistency through tooling rather than documentation alone
- **Pattern**: git hooks validate format before commit
- **Takeaway**: Automation catches format errors immediately, prevents bad data from entering the system

**4. Sphinx/ReStructuredText Documentation Systems**
- **Approach**: Structured text with parsers that enforce format
- **Relevance**: Similar to requirements.md structure with sections and formatting rules
- **Pattern**: Build-time validation fails on format errors
- **Takeaway**: Parser strictness forces adherence to format conventions

**5. mkdocs-material (Python)**
- **Repository**: squidfunk/mkdocs-material
- **Approach**: Configuration through YAML with schema validation
- **Relevance**: Clear separation of content vs. tooling, validation at build time
- **Takeaway**: Schema-driven validation is more robust than manual checks

### Common Pattern Across Examples

All successful implementations:
- **Fail fast**: Validate before modifying
- **Atomic operations**: All-or-nothing changes
- **Clear errors**: Specific problem + suggested fix
- **Automation**: Scripts enforce rules humans forget
- **Separation**: Source of truth (scripts/schemas) separate from generated content

## Proposals

### Alternative Implementation Strategies

**Option A: Continue with Python scripts (as specified)**
- **Pros**: Matches framework pattern, no new dependencies, full control
- **Cons**: Manual parser implementation, ongoing maintenance
- **Recommendation**: ✓ This is the right choice given framework constraints

**Option B: Use a requirements parser library**
- **Example**: Custom markdown parser or YAML alternative
- **Pros**: More robust parsing, better error messages
- **Cons**: Adds dependency, might not match existing format perfectly
- **Recommendation**: ✗ Not worth the dependency for this simple format

**Option C: Convert requirements.md to structured format (JSON/YAML)**
- **Pros**: Machine-readable, easier parsing, schema validation
- **Cons**: Major breaking change, loses human readability, lots of migration work
- **Recommendation**: ✗ Too disruptive, markdown is working fine

### Suggested Requirement Modifications

**1. Simplify validation parameter (already addressed by user)**
User chose to remove `strict` validation and only keep `basic`/`none`. This is good - simpler is better.

**2. Consider adding a `requirement_list.py` script**
Not in the prompt, but would be useful:
```bash
python .rdd/src/actions/requirement_list.py [category=UR|TR]
```
Output: Table of all requirements with ID, type, text preview, status

**3. Add `requirement_validate.py` for pre-commit checks**
Could validate entire requirements.md file without modifying it:
```bash
python .rdd/src/actions/requirement_validate.py
```
Output: List of format violations, duplicate checks, etc.

**4. Consider requirement metadata**
Future enhancement: Track creation date, last modified, author, status (draft/approved/implemented)
This could go in a separate `requirements-metadata.json` file

### Trade-offs

**ID auto-generation (user's Q2 decision)**
- **User chose**: Always auto-generate, no manual ID override
- **Trade-off**: Simplifies implementation ✓, but reduces flexibility ✗
- **Impact**: Cannot fix sequence gaps or reuse deleted IDs
- **Mitigation**: Keep it simple for now, can add `id=` parameter later if needed

**Validation levels (user's Q1 & Q3 decisions)**
- **User chose**: Only `basic` and `none`, no `strict`
- **Trade-off**: Simpler code ✓, but less protection against bad requirements ✗
- **Impact**: Users can create duplicate or poor-quality requirements
- **Mitigation**: Documentation and code review processes should catch issues

**Atomic writes (user's Q5 decision)**
- **User chose**: Simple temp file approach
- **Trade-off**: Simple implementation ✓, but no rollback capability ✗
- **Impact**: If something goes wrong after write, manual recovery needed
- **Mitigation**: Git provides version control safety net

## Prompt Modification

### Refined Prompt Version

**Context**: The RDD framework currently allows direct editing of `.rdd-instance/specifications/requirements.md`, creating risks of format corruption and ID conflicts. We need to enforce script-based modifications using deterministic Python scripts following the existing framework pattern (`prompt_create.py`).

**Objective**: Create requirement management scripts and update execution instructions to mandate their use.

**Scope**:
1. Create 6 Python scripts in `.rdd/src/actions/`:
   - `requirement_ur_create.py` - Create User Requirement
   - `requirement_ur_modify.py` - Modify User Requirement  
   - `requirement_ur_delete.py` - Delete User Requirement
   - `requirement_tr_create.py` - Create Technical Requirement
   - `requirement_tr_modify.py` - Modify Technical Requirement
   - `requirement_tr_delete.py` - Delete Technical Requirement

2. Update execution instruction files to prohibit direct requirements.md editing

**Script Specifications**:

*Common behavior (all scripts):*
- **ID management**: Auto-generate next sequential ID (no manual override)
- **Validation**: Support `validation=basic` (default) or `validation=none`
  - Basic: Check 10-2048 chars, contains "shall", valid format
  - None: Skip validation (for special cases)
- **Output**: Print `SUCCESS: <action> <requirement-id>` to stdout, errors to stderr
- **Exit codes**: 0 for success, 1 for failure
- **Atomic writes**: Write to temp file, validate, then rename over original
- **Format compliance**: Follow `.rdd/conventions/requirements.convention.md`
- **Error messages**: Include specific problem + suggested fix

*Create scripts:*
- **Parameters**: `text="<requirement text>"`, `validation=basic|none` (optional)
- **Behavior**: 
  - Parse requirements.md to find highest existing ID for category
  - Generate next ID (e.g., UR-0143 → UR-0144)
  - Validate text (if validation=basic)
  - Append to end of appropriate section (## User Requirements or ## Technical Requirements)
  - Ensure proper formatting with markdown list item prefix `- [ID] text`

*Modify scripts:*
- **Parameters**: `id="<requirement-id>"`, `text="<new complete text>"`, `validation=basic|none` (optional)
- **Behavior**:
  - Find requirement by ID
  - Replace entire requirement text (keeping ID)
  - Validate new text (if validation=basic)
  - Preserve file structure and other requirements

*Delete scripts:*
- **Parameters**: `id="<requirement-id>"`
- **Behavior**:
  - Find requirement by ID
  - Replace text with `[DELETED]` marker (keep ID line)
  - Format: `- [UR-0123] [DELETED]`

**Validation Logic (basic mode)**:
```python
def validate_requirement_text(text: str) -> None:
    text = text.strip()
    if len(text) < 10:
        raise ValueError("Requirement text too short (minimum 10 characters)")
    if len(text) > 2048:
        raise ValueError("Requirement text too long (maximum 2048 characters)")
    if "shall" not in text.lower():
        raise ValueError("Requirement must contain 'shall' keyword")
```

**Error Handling Examples**:
```python
# ID not found
"ERROR: Requirement UR-0123 not found in requirements.md. Run 'python .rdd/src/actions/requirement_list.py' to see all IDs."

# Validation failure  
"ERROR: Requirement text must contain 'shall' keyword. Example: 'The system shall validate user input.' Use validation=none to skip this check."

# File permission error
"ERROR: Cannot write to requirements.md (permission denied). Check file permissions or run with appropriate privileges."
```

**Execution Instructions Updates**:

*File: `.rdd/prompt-snippets/execution.md`*
- Add new section "Requirements Management Rules" near top:
  ```markdown
  ## Requirements Management Rules
  
  **CRITICAL**: Never edit `.rdd-instance/specifications/requirements.md` directly.
  Always use requirement management scripts:
  - Create: `python .rdd/src/actions/requirement_ur_create.py text="..."`
  - Modify: `python .rdd/src/actions/requirement_ur_modify.py id="UR-0123" text="..."`
  - Delete: `python .rdd/src/actions/requirement_ur_delete.py id="UR-0123"`
  
  Replace `ur` with `tr` for Technical Requirements.
  ```

- Add inline reminder in step 10 (Update requirements):
  ```markdown
  10. Update [REQUIREMENTS] if needed using requirement scripts (never edit file directly).
  ```

*File: `.rdd/prompt-snippets/execution-step.implementation.md`*
- Add examples section showing script usage:
  ```markdown
  ## Examples: Adding Requirements During Implementation
  
  # Create new user requirement
  python .rdd/src/actions/requirement_ur_create.py text="The system shall provide export functionality"
  
  # Modify existing requirement
  python .rdd/src/actions/requirement_tr_modify.py id="TR-0042" text="The framework shall use Python 3.11 or higher"
  
  # Mark requirement as deleted
  python .rdd/src/actions/requirement_ur_delete.py id="UR-0088"
  ```

**Success Criteria**:
1. All 6 scripts execute successfully and handle errors gracefully
2. Scripts correctly parse requirements.md and maintain format
3. ID generation is deterministic and sequential
4. Validation catches format violations
5. Execution instructions clearly prohibit direct editing
6. Scripts tested with: valid inputs, invalid inputs, edge cases (empty file, missing sections)

**Testing Checklist**:
- [ ] Create UR with basic validation
- [ ] Create TR with validation=none
- [ ] Modify existing requirement
- [ ] Delete requirement (verify [DELETED] marker)
- [ ] Validation catches: short text, no "shall", too long
- [ ] Error messages are helpful
- [ ] Concurrent execution doesn't corrupt file (manual test)
- [ ] Works with empty requirements.md (should fail gracefully or create sections)

**Implementation Notes**:
- Reference `prompt_create.py` for code structure and patterns
- Use regex pattern from requirements convention: `\[(UR|TR)-(\d{4})\]`
- Consider requirements.md sections structure (headers are `## User Requirements`, etc.)
- Handle the migration note comment block gracefully
- Test with current requirements.md file (544 lines, mix of regular and [DELETED] requirements)

### Improvements in Refined Version

1. **Explicit validation logic**: Code example shows exact validation rules
2. **Error message examples**: Shows what good error messages look like
3. **Testing checklist**: Makes success criteria more concrete and testable
4. **Implementation notes**: Provides specific guidance on edge cases
5. **File structure**: Clearer organization with explicit sections for each aspect
6. **Examples**: Shows actual command syntax for common operations
7. **Scope clarity**: Explicitly lists what's included and what's not
8. **Success criteria**: More specific and measurable
9. **Incorporates user decisions**: Integrates questionnaire answers (no strict validation, auto-ID only, etc.)
10. **Less ambiguity**: Removes underspecified aspects identified in Copilot Review section
