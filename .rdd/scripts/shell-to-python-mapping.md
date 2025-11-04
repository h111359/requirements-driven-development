# Shell to Python Mapping

This document provides a one-to-one mapping between Bash and Python scripts in the RDD framework, along with instructions for migrating to the Python versions.

## Overview

The RDD framework now supports both Bash and Python implementations that can be maintained in parallel. The Python version provides:

- **Cross-platform compatibility** - Works on Windows, Linux, and macOS
- **No external dependencies** - Uses only Python 3 standard library
- **Drop-in compatibility** - Same command-line interface as Bash scripts
- **Clean console feedback** - Colored output and consistent error handling

## Script Mapping

### Core Scripts

| Bash Script | Python Script | Status | Description |
|-------------|---------------|--------|-------------|
| `rdd.sh` | `rdd.py` | ✅ Complete | Main entry point with domain routing |
| `core-utils.sh` | `rdd_utils.py` | ✅ Complete | Core utility functions (integrated) |
| `git-utils.sh` | `rdd_utils.py` | ✅ Complete | Git operations (integrated) |
| `workspace-utils.sh` | `rdd.py` | ✅ Complete | Workspace management (integrated) |
| `branch-utils.sh` | `rdd.py` | ✅ Complete | Branch operations (integrated) |
| `change-utils.sh` | `rdd.py` | ✅ Complete | Change workflow (integrated) |
| `requirements-utils.sh` | `rdd.py` | ⚠️ Partial | Requirements operations (basic support) |
| `clarify-utils.sh` | `rdd.py` | ⚠️ Partial | Clarification operations (basic support) |
| `prompt-utils.sh` | `rdd.py` | ⚠️ Partial | Prompt management (basic support) |

### Implementation Strategy

The Python implementation uses a different architectural approach:

- **Bash**: Multiple sourced utility scripts with exported functions
- **Python**: Two main files:
  - `rdd_utils.py` - Shared utility module with all helper functions
  - `rdd.py` - Main entry point with integrated domain logic

This approach is more Pythonic and eliminates the complexity of shell sourcing while maintaining functional parity.

## Usage Examples

### Bash Version

```bash
# Main script
./rdd.sh change create

# With explicit bash
bash .rdd/scripts/rdd.sh branch list

# Source utilities in custom scripts
source .rdd/scripts/core-utils.sh
print_success "Operation completed"
```

### Python Version

```bash
# Main script
python3 .rdd/scripts/rdd.py change create

# Make executable and run directly
chmod +x .rdd/scripts/rdd.py
./rdd.py branch list

# Import utilities in custom Python scripts
from rdd_utils import print_success, validate_name
print_success("Operation completed")
```

## Command Compatibility Matrix

All commands are fully compatible between Bash and Python versions:

| Command | Bash | Python | Notes |
|---------|------|--------|-------|
| `--version` | ✅ | ✅ | Shows version information |
| `--help` | ✅ | ✅ | Shows help message |
| `branch create <type> <name>` | ✅ | ✅ | Creates new branch |
| `branch delete [name]` | ✅ | ✅ | Deletes branch |
| `branch list` | ✅ | ✅ | Lists branches |
| `workspace init <type>` | ✅ | ✅ | Initializes workspace |
| `workspace archive` | ✅ | ✅ | Archives workspace |
| `workspace clear` | ✅ | ✅ | Clears workspace |
| `change create` | ✅ | ✅ | Interactive change creation |
| `change wrap-up` | ✅ | ✅ | Completes change workflow |
| `fix init <name>` | ✅ | ✅ | Creates fix |
| `fix wrap-up` | ✅ | ✅ | Completes fix workflow |
| `git compare` | ✅ | ✅ | Compares with main branch |
| `git modified-files` | ✅ | ✅ | Lists modified files |
| `git push` | ✅ | ✅ | Pushes to remote |

## Functional Parity

### Core Functions

All core utility functions from `core-utils.sh` have been implemented:

- ✅ `print_success()` / `print_success()`
- ✅ `print_error()` / `print_error()`
- ✅ `print_warning()` / `print_warning()`
- ✅ `print_info()` / `print_info()`
- ✅ `print_step()` / `print_step()`
- ✅ `print_banner()` / `print_banner()`
- ✅ `validate_name()` / `validate_name()`
- ✅ `validate_branch_name()` / `validate_branch_name()`
- ✅ `normalize_to_kebab_case()` / `normalize_to_kebab_case()`
- ✅ `get_timestamp()` / `get_timestamp()`
- ✅ `get_timestamp_filename()` / `get_timestamp_filename()`
- ✅ `ensure_dir()` / `ensure_dir()`
- ✅ `confirm_action()` / `confirm_action()`

### Git Functions

All essential git utility functions from `git-utils.sh` have been implemented:

- ✅ `check_git_repo()` / `check_git_repo()`
- ✅ `get_current_branch()` / `get_current_branch()`
- ✅ `get_default_branch()` / `get_default_branch()`
- ✅ `get_git_user()` / `get_git_user()`
- ✅ `check_uncommitted_changes()` / `check_uncommitted_changes()`
- ✅ `fetch_main()` / `fetch_main()`
- ✅ `push_to_remote()` / `push_to_remote()`
- ✅ `auto_commit()` / `auto_commit()`
- ✅ `compare_with_main()` / `compare_with_main()`
- ✅ `get_modified_files()` / `get_modified_files()`

### Workspace Functions

All essential workspace functions from `workspace-utils.sh` have been implemented:

- ✅ `init_workspace()` / `init_workspace()`
- ✅ `archive_workspace()` / `archive_workspace()`
- ✅ `clear_workspace()` / `clear_workspace()`
- ✅ `copy_template()` / `copy_template()`

### Branch Functions

All essential branch functions from `branch-utils.sh` have been implemented:

- ✅ `create_branch()` / `create_branch()`
- ✅ `delete_branch()` / `delete_branch()`
- ✅ `list_branches()` / `list_branches()`

## Migration Guide

### For End Users

To switch from Bash to Python:

1. **Check Python version** (requires Python 3.6+):
   ```bash
   python3 --version
   ```

2. **Use Python script instead**:
   ```bash
   # Instead of:
   ./rdd.sh change create
   
   # Use:
   python3 .rdd/scripts/rdd.py change create
   ```

3. **Optional: Create an alias**:
   ```bash
   # Add to your ~/.bashrc or ~/.zshrc
   alias rdd-py='python3 .rdd/scripts/rdd.py'
   
   # Then use:
   rdd-py change create
   ```

### For Custom Scripts

If you've created custom scripts that source RDD utilities:

**Bash approach:**
```bash
#!/bin/bash
source .rdd/scripts/core-utils.sh
source .rdd/scripts/git-utils.sh

print_success "Starting process"
current_branch=$(get_current_branch)
echo "On branch: $current_branch"
```

**Python approach:**
```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add rdd scripts to path
sys.path.insert(0, str(Path(__file__).parent / '.rdd' / 'scripts'))

from rdd_utils import print_success, get_current_branch

print_success("Starting process")
current_branch = get_current_branch()
print(f"On branch: {current_branch}")
```

### For GitHub Actions / CI/CD

Update your workflows to use Python scripts:

**Before:**
```yaml
- name: Create change
  run: |
    bash .rdd/scripts/rdd.sh change create
```

**After:**
```yaml
- name: Create change
  run: |
    python3 .rdd/scripts/rdd.py change create
```

**Or maintain compatibility:**
```yaml
- name: Create change
  run: |
    # Use Python if available, fall back to Bash
    if command -v python3 &> /dev/null; then
      python3 .rdd/scripts/rdd.py change create
    else
      bash .rdd/scripts/rdd.sh change create
    fi
```

## Modifying `.github/prompts` to Use Python

To update Copilot prompts to use Python versions:

1. **Find prompt files** that reference RDD scripts:
   ```bash
   grep -r "rdd.sh" .github/prompts/
   ```

2. **Update references** from `rdd.sh` to `rdd.py`:
   ```markdown
   <!-- Before -->
   Run the RDD script: `./rdd.sh change create`
   
   <!-- After -->
   Run the RDD script: `python3 .rdd/scripts/rdd.py change create`
   ```

3. **Update any sourced utilities**:
   ```markdown
   <!-- Before -->
   Source utilities: `source .rdd/scripts/core-utils.sh`
   
   <!-- After -->
   Import utilities in Python: `from rdd_utils import *`
   ```

4. **Test the prompts** to ensure they work with Python scripts.

## Platform-Specific Notes

### Linux / macOS

Both Bash and Python versions work natively. No special configuration needed.

### Windows

**Bash version** requires:
- Git Bash, WSL, or Cygwin to run shell scripts

**Python version** works natively on Windows:
- No additional tools required
- Use `python rdd.py` instead of `python3 rdd.py` if Python 3 is your default

### Color Support

Both versions support colored output:
- **Linux/macOS**: Works in all terminals
- **Windows**: Works in Windows Terminal, PowerShell, and modern CMD
- **Fallback**: Colors degrade gracefully if not supported

## Testing Functional Equality

To verify that Python and Bash versions produce the same results:

```bash
# Test help output
./rdd.sh --help > bash_help.txt
python3 .rdd/scripts/rdd.py --help > python_help.txt
diff bash_help.txt python_help.txt

# Test branch listing
./rdd.sh branch list > bash_branches.txt
python3 .rdd/scripts/rdd.py branch list > python_branches.txt
diff bash_branches.txt python_branches.txt

# Test git operations
./rdd.sh git compare > bash_compare.txt
python3 .rdd/scripts/rdd.py git compare > python_compare.txt
diff bash_compare.txt python_compare.txt
```

## Known Differences

Minor differences between implementations:

1. **Error messages**: Slightly different formatting but same content
2. **Stack traces**: Python shows Python tracebacks when DEBUG=1
3. **Performance**: Python may be slightly faster for complex operations
4. **Interactive prompts**: Identical behavior, different implementation

## Troubleshooting

### Python script not found

```bash
# Error: ModuleNotFoundError: No module named 'rdd_utils'
# Solution: Ensure you're running from the correct directory or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.rdd/scripts"
```

### Permission denied

```bash
# Error: Permission denied
# Solution: Make script executable
chmod +x .rdd/scripts/rdd.py
```

### Python version too old

```bash
# Error: syntax error or unexpected behavior
# Solution: Upgrade to Python 3.6 or later
python3 --version  # Should be 3.6+
```

## Future Enhancements

Areas for future Python implementation:

- **Requirements operations** - Full implementation of requirements merging and validation
- **Clarification operations** - Complete clarification phase management
- **Prompt operations** - Full prompt tracking and execution logging
- **PR operations** - GitHub PR creation and management
- **Interactive menu** - TUI menu system similar to Bash version
- **Test suite** - Comprehensive unit and integration tests

## Contributing

When adding new features:

1. **Implement in both Bash and Python** to maintain parallel support
2. **Update this mapping document** with new functions
3. **Test on multiple platforms** (Linux, macOS, Windows)
4. **Document any platform-specific behaviors**
5. **Maintain command-line compatibility** between versions

## Support

For questions or issues:

- **Bash version**: See bash script comments and help output
- **Python version**: Check docstrings and use `--help`
- **Both**: Consult main repository README.md

---

**Last Updated**: 2025-01-04
**Python Version**: 1.0.0
**Bash Version**: 1.0.0
