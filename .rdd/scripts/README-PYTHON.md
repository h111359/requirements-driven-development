# RDD Python Scripts

Python implementation of the RDD (Requirements-Driven Development) framework scripts.

## Overview

This directory contains Python equivalents of all Bash scripts in the RDD framework, providing cross-platform compatibility while maintaining full functional parity with the Bash versions.

## Files

- **`rdd.py`** - Main entry point script (equivalent to `rdd.sh`)
- **`rdd_utils.py`** - Shared utility module with all helper functions
- **`shell-to-python-mapping.md`** - Comprehensive mapping and migration guide
- **`test_rdd_python.py`** - Test suite for Python implementation

## Requirements

- **Python 3.6 or later** (uses only standard library, no external dependencies)
- **Git** (for repository operations)

## Quick Start

### Check Installation

```bash
# Check Python version
python3 --version  # Should be 3.6+

# Test the script
python3 .rdd/scripts/rdd.py --version
```

### Basic Usage

```bash
# Show help
python3 .rdd/scripts/rdd.py --help

# Create a new change
python3 .rdd/scripts/rdd.py change create

# List branches
python3 .rdd/scripts/rdd.py branch list

# Compare with main
python3 .rdd/scripts/rdd.py git compare
```

### Make Executable (Optional)

```bash
# Make executable
chmod +x .rdd/scripts/rdd.py

# Run directly
./.rdd/scripts/rdd.py --help
```

## Command Reference

### Branch Operations

```bash
# Create a new branch
python3 rdd.py branch create enh my-enhancement
python3 rdd.py branch create fix my-bugfix

# Delete a branch
python3 rdd.py branch delete my-branch
python3 rdd.py branch delete my-branch --force

# List branches
python3 rdd.py branch list
python3 rdd.py branch list enh  # Filter by pattern
```

### Workspace Operations

```bash
# Initialize workspace
python3 rdd.py workspace init change
python3 rdd.py workspace init fix

# Archive workspace
python3 rdd.py workspace archive
python3 rdd.py workspace archive --keep  # Keep workspace after archiving

# Clear workspace
python3 rdd.py workspace clear
```

### Change Workflow

```bash
# Create a new change (interactive)
python3 rdd.py change create

# Create a fix (interactive)
python3 rdd.py change create fix

# Wrap up current change
python3 rdd.py change wrap-up
```

### Fix Workflow

```bash
# Initialize a fix
python3 rdd.py fix init my-bugfix

# Wrap up fix
python3 rdd.py fix wrap-up
```

### Git Operations

```bash
# Compare current branch with main
python3 rdd.py git compare

# List modified files
python3 rdd.py git modified-files

# Push current branch
python3 rdd.py git push
```

## Using in Custom Scripts

### Import Functions

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Add rdd scripts to path
sys.path.insert(0, str(Path(__file__).parent / '.rdd' / 'scripts'))

from rdd_utils import (
    print_success, print_error, print_info,
    validate_name, normalize_to_kebab_case,
    get_current_branch, get_default_branch
)

# Use the functions
print_success("Starting process")
branch = get_current_branch()
print_info(f"On branch: {branch}")

name = normalize_to_kebab_case("My Feature Name")
if validate_name(name):
    print_success(f"Valid name: {name}")
```

### Available Functions

See `rdd_utils.py` for complete documentation of available functions:

**Output Functions:**
- `print_success(message)` - Green checkmark message
- `print_error(message)` - Red X message  
- `print_warning(message)` - Yellow warning message
- `print_info(message)` - Blue info message
- `print_step(message)` - Cyan step message
- `print_banner(title, subtitle="")` - Formatted banner

**Validation Functions:**
- `validate_name(name)` - Validate kebab-case name
- `validate_branch_name(branch)` - Validate branch format
- `validate_file_exists(path, desc)` - Check file exists
- `validate_dir_exists(path, desc)` - Check directory exists

**String Functions:**
- `normalize_to_kebab_case(text)` - Convert to kebab-case

**Git Functions:**
- `check_git_repo()` - Verify git repository
- `get_current_branch()` - Get current branch name
- `get_default_branch()` - Get main/master branch
- `get_git_user()` - Get git user info
- `check_uncommitted_changes()` - Check for uncommitted changes
- `get_repo_root()` - Get repository root path

**Utility Functions:**
- `ensure_dir(path)` - Create directory if needed
- `get_timestamp()` - ISO 8601 timestamp
- `get_timestamp_filename()` - Filename-safe timestamp
- `confirm_action(prompt)` - User confirmation
- `debug_print(message)` - Debug logging (if DEBUG=1)

**Config Functions:**
- `get_config(key, file)` - Get config value
- `set_config(key, value, file)` - Set config value
- `find_change_config(dir)` - Find config file

## Testing

Run the test suite to validate functionality:

```bash
python3 .rdd/scripts/test_rdd_python.py
```

The test suite validates:
- Color output functions
- Validation functions
- String normalization
- Timestamp generation
- Git operations
- Directory operations
- Configuration management

## Platform Support

### Linux / macOS

Works natively, no special configuration needed.

```bash
python3 .rdd/scripts/rdd.py change create
```

### Windows

Works natively on Windows with Python 3.6+:

```cmd
python .rdd\scripts\rdd.py change create
```

**Note:** On Windows, use `python` instead of `python3` if Python 3 is your default.

### Color Support

- **Linux/macOS**: Works in all terminals
- **Windows**: Works in Windows Terminal, PowerShell, modern CMD
- **Fallback**: Colors degrade gracefully if not supported

## Migration from Bash

See [`shell-to-python-mapping.md`](./shell-to-python-mapping.md) for:
- Complete function mapping
- Migration guide for users
- Instructions for custom scripts
- GitHub Actions / CI/CD updates
- Platform-specific notes

## Troubleshooting

### ModuleNotFoundError

```bash
# Error: ModuleNotFoundError: No module named 'rdd_utils'
# Solution: Run from repository root or adjust PYTHONPATH
cd /path/to/repository
python3 .rdd/scripts/rdd.py --help
```

### Permission Denied

```bash
# Error: Permission denied
# Solution: Make script executable
chmod +x .rdd/scripts/rdd.py
```

### Python Version

```bash
# Error: Syntax errors or unexpected behavior
# Solution: Upgrade to Python 3.6+
python3 --version
```

## Debug Mode

Enable debug output by setting the `DEBUG` environment variable:

```bash
DEBUG=1 python3 .rdd/scripts/rdd.py change create
```

This will show:
- Debug print statements
- Stack traces on errors
- Additional diagnostic information

## Comparison with Bash

### Similarities

- ✅ Same command-line interface
- ✅ Same functionality and behavior
- ✅ Same output formatting
- ✅ Same error handling

### Differences

- Python uses `rdd_utils.py` module vs. multiple sourced `.sh` files
- Python implementation is more structured (classes, type hints)
- Slightly different error messages (but same content)
- Python may be faster for complex operations

## Contributing

When adding new features:

1. **Implement in `rdd.py` or `rdd_utils.py`** as appropriate
2. **Add tests** to `test_rdd_python.py`
3. **Update documentation** in this README
4. **Maintain compatibility** with Bash version
5. **Test on multiple platforms** (Linux, macOS, Windows)

## Support

For questions or issues:

- Check [`shell-to-python-mapping.md`](./shell-to-python-mapping.md)
- Review function docstrings in `rdd_utils.py`
- Use `--help` flag for command-specific help
- See main repository [README.md](../../README.md)

---

**Version**: 1.0.0  
**Python Requirement**: 3.6+  
**External Dependencies**: None (uses only Python standard library)
