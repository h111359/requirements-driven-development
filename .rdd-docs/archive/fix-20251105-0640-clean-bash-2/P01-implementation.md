# P01 Implementation: Clean Up Unused Bash Scripts

## Task
Check all .sh scripts in `.rdd/scripts` if they are used in some of the prompts in `.github/prompts` or in some of the .py scripts in `.rdd/scripts`. If not - move them to `.rdd-docs/workspace`.

## Step 1: Identify all .sh scripts in .rdd/scripts

Bash scripts found in `.rdd/scripts/`:
- branch-utils.sh
- change-utils.sh
- clarify-utils.sh
- core-utils.sh
- git-utils.sh
- prompt-utils.sh
- rdd.sh
- requirements-utils.sh
- workspace-utils.sh

## Step 2: Check usage in prompts and Python scripts

**Usage in prompts (`.github/prompts/`):**
- Only `rdd.sh` is referenced (indirectly via `python3 .rdd/scripts/rdd.py`)
- Python version is used: `python3 .rdd/scripts/rdd.py`

**Usage in Python scripts:**
- `rdd.py` mentions `rdd.sh` in a comment only (as reference, not execution)

**Usage in `rdd.sh`:**
The main `rdd.sh` script sources ALL utility scripts:
```bash
source "$SCRIPT_DIR/core-utils.sh"
source "$SCRIPT_DIR/git-utils.sh"
source "$SCRIPT_DIR/workspace-utils.sh"
source "$SCRIPT_DIR/branch-utils.sh"
source "$SCRIPT_DIR/requirements-utils.sh"
source "$SCRIPT_DIR/clarify-utils.sh"
source "$SCRIPT_DIR/prompt-utils.sh"
source "$SCRIPT_DIR/change-utils.sh"
```

## Step 3: Analysis

**Conclusion:** 
All bash scripts in `.rdd/scripts/` are USED:
- `rdd.sh` - Main entry point (referenced in old prompts, but now replaced by Python)
- All utility scripts (branch-utils.sh, change-utils.sh, etc.) - Sourced by `rdd.sh`

However, based on the current state:
- The project has migrated to Python (`rdd.py`)
- All prompts now use `python3 .rdd/scripts/rdd.py` instead of bash scripts
- The bash scripts appear to be **legacy** code that's been replaced by Python implementation

## Step 4: Decision

Since ALL bash scripts are interconnected (rdd.sh sources the utilities), and the entire bash implementation has been replaced by Python (`rdd.py` and `rdd_utils.py`), we should NOT move individual scripts.

**User chose option B:** Move ALL bash scripts together to a legacy archive location

## Step 5: Execute Move

Created directory and moved all bash scripts:

```bash
mkdir -p .rdd-docs/workspace/legacy-bash-scripts
mv .rdd/scripts/*.sh .rdd-docs/workspace/legacy-bash-scripts/
```

**Scripts moved (9 files):**
- branch-utils.sh
- change-utils.sh
- clarify-utils.sh
- core-utils.sh
- git-utils.sh
- prompt-utils.sh
- rdd.sh
- requirements-utils.sh
- workspace-utils.sh

**Remaining in `.rdd/scripts/`:**
- rdd.py (Python implementation)
- rdd_utils.py (Python utilities)
- test_rdd_python.py (Tests)
- IMPLEMENTATION-SUMMARY.md
- README-PYTHON.md
- shell-to-python-mapping.md

## Result

✓ All legacy bash scripts successfully moved to `.rdd-docs/workspace/legacy-bash-scripts/`
✓ `.rdd/scripts/` now contains only Python implementation files
✓ Clean separation between current (Python) and legacy (Bash) implementations

## Documentation Updates

All documentation has been updated to reflect the Python migration:

### requirements.md
- **[TR-06]** Modified: Updated to reflect Python implementation (legacy bash archived)
- **[TR-07]** Modified: Changed to generic error handling language
- **[TR-08]** Modified: Noted jq was for legacy bash, Python uses native json module
- **[FR-13]** Marked as [DELETED] (referenced bash script)
- **[FR-14]** Marked as [DELETED] (referenced bash script)
- **[FR-44]** Marked as [DELETED] (referenced bash scripts rdd.sh/rdd.ps1)
- **[FR-47]** Added: Python-Based Script Implementation requirement

### tech-spec.md
- Updated **Technology Stack** section to reflect Python as primary language
- Updated **Command Routing Pattern** to show `python3 .rdd/scripts/rdd.py` commands
- Updated **Main Entry Point** to reference `rdd.py` instead of bash/PowerShell
- Updated **Utility Scripts** section to document Python implementation
- Replaced **Cross-Platform Implementation** section noting Python provides native compatibility
- Updated **Deployment Architecture** for Python installation
- Updated **Migration Notes** with bash script archival and Python migration details
- Updated **Deprecated Components** to include all bash and PowerShell scripts

### folder-structure.md
- Updated `.rdd/scripts/` listing to show only Python files (rdd.py, rdd_utils.py, tests, docs)
- Marked `src/` directory as "Legacy platform-specific implementations (archived)"
- Updated **Key Principle #6** to document Python-based implementation
- Updated **Key Principle #7** to show Python command syntax
- Updated **RDD Workflow File Locations** to reference Python scripts

### data-model.md
- Replaced **Platform-Specific Implementations** section with **Implementation** section
- Documented current Python implementation
- Documented legacy bash scripts as archived
- Listed all 9 archived bash script files
