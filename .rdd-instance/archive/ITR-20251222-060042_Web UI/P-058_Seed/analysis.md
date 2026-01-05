# Analysis: Seed Script for RDD Instance

## Copilot Review

### Feasibility Assessment
The requested seed script is **highly feasible** and represents a sound engineering practice. Creating an initialization script that validates and recreates missing mandatory files is a common pattern in framework initialization.

**Strengths of the request:**
- Clear scope: validate required paths and files from manifest.json
- Well-defined data sources: manifest.json contains all necessary configuration
- Convention-driven: files should be generated from convention files, ensuring consistency
- Idempotent design: script should check and do nothing if already seeded (explicitly stated)
- Integration point defined: web server should execute during initialization

**Potential Challenges:**
1. **Missing convention file**: The manifest.json references `.rdd/conventions/technical-design.convention.md` which does not exist. This will cause the script to fail during initialization unless handled gracefully.

2. **Complex file generation**: Some files have complex schemas (work-iteration-registry.json, prompts-registry.md) that require careful template generation to ensure validity.

3. **Validation complexity**: The prompt requests validation of generated files, but convention files are Markdown documents describing format rules, not machine-readable schemas. This makes automated validation challenging.

4. **Empty vs. initialized state**: technical-design.json currently exists but is empty. The script needs clear rules about when to recreate vs. preserve files.

5. **Error recovery**: The prompt doesn't specify what happens if seeding partially fails (e.g., some folders created but file generation fails).

### Impact on Existing Functionality
**Low to Medium impact:**

- **Web server**: Requires modification to call the seed script during initialization (before serving requests)
- **Existing initialization logic**: workdir_new_setup.py already initializes work-iteration-registry.json, so there's overlap that needs clarification
- **User experience**: Auto-seeding during web server startup improves developer experience by eliminating manual setup steps
- **Testing**: New script requires comprehensive tests to ensure it handles all edge cases correctly

**No breaking changes expected** if implemented correctly with proper safeguards.

### Completeness of Prompt
**Missing important details:**

1. **Convention file location**: What happens when a convention file (like technical-design.convention.md) doesn't exist?
2. **File content generation**: How to parse Markdown convention files and generate actual file content?
3. **Collision handling**: What if files exist but don't match conventions? Overwrite or preserve?
4. **Error handling specifics**: Should the web server fail to start if seeding fails?
5. **Archive folder**: Should the script create the archive folder structure mentioned in manifest.json?
6. **Git integration**: Should seeding be git-aware (e.g., avoid recreating gitignored files)?
7. **Logging verbosity**: How much detail should be logged during seeding?

The questionnaire answers provide some clarity (create recursively, skip existing files, fail on missing conventions, validate created files, detailed logging, idempotent), but these should ideally be in the prompt itself.

## Best Practices

Based on industry standards for initialization and seeding scripts, here are key best practices:

### 1. Idempotency
**Standard:** Initialization scripts should be safe to run multiple times without side effects.
- **Source:** HashiCorp's Terraform philosophy, Docker ENTRYPOINT patterns
- **Application:** Script should check existence before creating, never overwrite existing files
- **Questionnaire alignment:** Q6 confirms this is required

### 2. Fail-Fast Principle
**Standard:** Detect and report configuration errors as early as possible.
- **Source:** "Design by Contract" (Bertrand Meyer), Microsoft's Fail Fast principle
- **Application:** Validate manifest.json structure, verify all convention files exist before attempting creation
- **Questionnaire alignment:** Q3 recommends failing on missing convention files

### 3. Atomic Operations
**Standard:** Ensure operations complete fully or not at all.
- **Source:** Database ACID principles, filesystem transaction patterns
- **Application:** Use temporary files and atomic rename operations; if validation fails, don't leave partial state
- **Pattern:** Create files in temp location, validate all, then move to final location

### 4. Comprehensive Logging
**Standard:** Provide detailed logs for debugging while keeping normal output clean.
- **Source:** The Twelve-Factor App (Logs), Linux FHS logging conventions
- **Application:** Log all actions (created folders, skipped files, validation results) to help troubleshoot issues
- **Questionnaire alignment:** Q5 recommends detailed logging

### 5. Validation After Creation
**Standard:** Verify generated artifacts match expected schema/format.
- **Source:** TDD practices, Contract Testing patterns
- **Application:** After generating JSON files, parse them to verify validity; for Markdown, check basic structure
- **Questionnaire alignment:** Q4 recommends validating created files

### 6. Convention Over Configuration
**Standard:** Use sensible defaults to minimize configuration burden.
- **Source:** Ruby on Rails CoC principle, Spring Boot autoconfiguration
- **Application:** Manifest.json already provides conventions; script simply enforces them
- **Good fit:** The approach in the prompt aligns perfectly with this principle

### 7. Separation of Concerns
**Standard:** Initialization logic should be separate from runtime logic.
- **Source:** SOLID principles (Single Responsibility)
- **Application:** Seed script should be standalone, callable from web server but also runnable independently for testing
- **Recommendation:** Make script usable via CLI, not just from web server

## Samples from GitHub

### 1. Django's `django-admin startproject`
**Repository:** django/django
**Approach:** 
- Uses template files with variable substitution
- Creates complete directory structure in one command
- Validates Python package names before creation
- Idempotent through existence checks

**Relevance:** Similar to RDD seed script - creates project structure from templates with validation.

### 2. Ruby on Rails `rails new`
**Repository:** rails/rails
**Approach:**
- Generates project scaffolding from templates
- Supports multiple template engines
- Allows customization through flags
- Creates git repository by default

**Relevance:** Comprehensive initialization that creates all necessary files and folders in correct structure.

### 3. Ansible's `setup` module
**Repository:** ansible/ansible
**Approach:**
- Idempotent by design - checks current state before making changes
- Detailed logging of all actions
- Fail-fast on critical errors
- Supports dry-run mode for safety

**Relevance:** Production-grade approach to system initialization with strong error handling.

### 4. Terraform's `init` command
**Repository:** hashicorp/terraform
**Approach:**
- Downloads required providers/modules
- Creates working directories
- Validates configuration before proceeding
- Safe to run multiple times
- Clear success/failure output

**Relevance:** Industry-standard initialization pattern with excellent error handling and user feedback.

### 5. Cookiecutter
**Repository:** cookiecutter/cookiecutter
**Approach:**
- Template-based project generation
- JSON/YAML configuration for templates
- Hooks for pre/post generation actions
- Extensive validation

**Relevance:** Similar template-based generation approach, could inform how to parse convention files.

**Common patterns across all:**
- Idempotent design
- Template-based generation
- Comprehensive validation
- Clear, actionable error messages
- Structured logging

## Proposals

### 1. Handle Missing Convention Files Gracefully
**Current approach:** Prompt suggests using convention files for generation.

**Problem:** technical-design.convention.md doesn't exist; this will cause immediate failure.

**Proposal:** Add fallback strategies to manifest.json:
```json
"requiredInstanceFiles": [
  {
    "path": ".rdd-instance/specifications/technical-design.json",
    "convention": ".rdd/conventions/technical-design.convention.md",
    "fallback": "empty-json-object"
  }
]
```

**Alternative:** Create the missing convention file as part of the seed work.

### 2. Add Template Files Instead of Convention Files
**Current approach:** Generate files by interpreting convention Markdown files.

**Problem:** Convention files describe format rules in English, making automated parsing complex and error-prone.

**Proposed change:**
- Add `.rdd/templates/` directory with actual template files
- Update manifest.json to reference templates instead of conventions:
```json
"requiredInstanceFiles": [
  {
    "path": ".rdd-instance/workdir/work-iteration-registry.json",
    "template": ".rdd/templates/work-iteration-registry.json.template"
  }
]
```
- Templates use simple variable substitution (e.g., `{{ITERATION_ID}}`)
- Keeps convention files for documentation, but uses templates for generation

**Benefits:**
- Much simpler implementation
- Higher reliability (copy template vs. parse English rules)
- Templates can be validated directly
- Clearer separation: conventions = documentation, templates = generation

### 3. Add Dry-Run and Repair Modes
**Current approach:** Simple create-if-missing logic.

**Proposal:** Add operation modes:
- `--check`: Validate only, report what's missing without making changes
- `--repair`: Recreate invalid/corrupted files (not just missing ones)
- `--force`: Overwrite even valid files (for testing/reset scenarios)

**Usage:**
```bash
python .rdd/src/actions/rdd-instance_seed.py --check
python .rdd/src/actions/rdd-instance_seed.py  # default: create missing only
python .rdd/src/actions/rdd-instance_seed.py --repair
```

### 4. Create Seed Script as Library + CLI
**Current approach:** Script to be called by web server.

**Proposal:** Structure as reusable module:
```python
# .rdd/src/lib/seeder.py
class InstanceSeeder:
    def check_required_paths(self) -> List[str]:
        """Returns list of missing paths."""
    
    def create_missing_files(self) -> Dict[str, bool]:
        """Creates missing files. Returns success status per file."""
    
    def validate_instance(self) -> List[str]:
        """Returns list of validation errors."""

# .rdd/src/actions/rdd-instance_seed.py (CLI wrapper)
# .rdd/src/web/server.py (calls seeder.create_missing_files())
```

**Benefits:**
- Testable in isolation
- Reusable from multiple contexts
- Easier to add features later

### 5. Progressive Validation Levels
**Current approach:** Q4 suggests validating all created files.

**Proposal:** Implement three validation levels:

1. **Structural validation** (always):
   - JSON files: verify valid JSON syntax
   - Markdown files: verify UTF-8 encoding
   - Folders: verify permissions

2. **Schema validation** (recommended):
   - JSON files: validate against JSON schema if available
   - Registry files: verify ID formats, required fields

3. **Content validation** (optional):
   - Cross-file consistency checks
   - Reference integrity (e.g., prompt IDs match across registries)

### 6. Add Requirement for Logging Framework
**Current requirement:** Uses print statements (based on other scripts).

**Proposal:** Add new technical requirement:
- [TR-XXXX] The framework shall use Python's logging module for all diagnostic output, with configurable log levels (DEBUG, INFO, WARNING, ERROR) to support both development and production use cases.

**Implementation:**
```python
import logging
logger = logging.getLogger(__name__)

logger.info("Created folder: %s", folder_path)
logger.warning("Skipped existing file: %s", file_path)
logger.error("Missing convention file: %s", convention_path)
```

**Benefits:**
- Standard Python practice
- Configurable verbosity
- Better integration with web server logging
- Structured log output

## Prompt Modification

Here's how I would rewrite this prompt for better clarity and completeness:

---

**Prompt: RDD Instance Initialization Script**

Create a script `.rdd/src/actions/rdd-instance_seed.py` that validates and initializes the RDD instance structure, ensuring all required files and folders exist with correct content.

**Functional Requirements:**

1. **Structure Validation:**
   - Read `requiredPaths.instance` from `.rdd/config/manifest.json`
   - Verify all required folders exist
   - Create missing folders recursively (like `mkdir -p`)

2. **File Initialization:**
   - Read `requiredInstanceFiles` from `.rdd/config/manifest.json`
   - For each required file that doesn't exist:
     - Locate the corresponding template file in `.rdd/templates/` (use basename of path + `.template` extension)
     - If template doesn't exist, fail with clear error message indicating which template is missing
     - Copy template content to target location
     - Perform basic validation (JSON syntax for .json files, UTF-8 encoding for .md files)

3. **Preservation Policy:**
   - NEVER overwrite or modify existing files
   - Script must be idempotent (safe to run repeatedly)
   - If a file already exists, skip it with info-level log message

4. **Error Handling:**
   - Fail fast if manifest.json is missing or malformed
   - Fail fast if any referenced template file is missing
   - Fail fast if file validation fails after creation
   - Provide specific error messages with remediation steps for all failures

5. **Logging:**
   - Use Python logging module with INFO level default
   - Log each folder creation with full path
   - Log each file creation with full path
   - Log each skipped file (already exists) with full path
   - Log validation results for created files
   - Print summary at end: X folders created, Y files created, Z files skipped

**Integration Requirements:**

1. **Web Server Integration:**
   - Modify `.rdd/src/web/server.py` main() function
   - Call seed script immediately after parsing arguments, before starting HTTP server
   - If seeding fails (non-zero exit code), abort server startup with error message
   - Log seed script output to console

2. **CLI Usage:**
   - Script should also be callable independently: `python .rdd/src/actions/rdd-instance_seed.py`
   - Support `--verbose` flag for DEBUG level logging
   - Return exit code 0 on success, 1 on failure

**Template Files to Create:**

Before implementing the seed script, create template files in `.rdd/templates/`:

1. `work-iteration-registry.json.template` - minimal valid work iteration registry
2. `prompts-registry.md.template` - empty prompts registry with header
3. `files-and-folders.md.template` - empty file structure document
4. `requirements.md.template` - requirements file header with Product Name/Overview placeholders
5. `technical-design.json.template` - empty JSON object `{}`

**Testing Requirements:**

Create tests in `build/tests/python/test_seed.py` that verify:
- Creates missing folders and files
- Skips existing files without modification
- Validates JSON syntax of created files
- Fails gracefully on missing templates
- Produces expected log output
- Is truly idempotent (running twice produces same result)

**Notes:**
- This script implements the "convention over configuration" principle
- Templates represent the minimal valid content for each file type
- Users can customize files after seeding; script preserves customizations on subsequent runs
- Seed script should complete in <100ms for typical case (all files exist)

---

**Why This Is Better:**

1. **More specific:** Defines exact template file approach vs. vague "convention files"
2. **Clearer scope:** Explicitly lists which templates to create
3. **Better error handling:** Specifies exactly when to fail and what messages to show
4. **Integration clarity:** Specifies exact integration point in web server
5. **Testability:** Includes specific test requirements
6. **Prerequisites:** Makes clear that templates must exist before script can work
7. **Performance expectations:** Sets clear performance goal
8. **Preserves original intent:** Still idempotent, still runs on web server init, still validates
9. **Actionable:** Developer knows exactly what to build without interpretation needed
10. **Complete:** No ambiguity about missing convention files or generation logic
