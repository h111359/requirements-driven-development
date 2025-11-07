# P02 Implementation: Remove RDD_VERSION Variable

## Prompt Description
In `.rdd/scripts/rdd.py` is defined variable RDD_VERSION. In the future, when new versions are created, this variable will become obsolete if forgotten to be modified. In order not to cause confusion - it needs to be removed. Check if it is used at all and if not - remove it.

## Analysis

### Current State
The `RDD_VERSION` variable is defined in `.rdd/scripts/rdd.py` at line 49:
```python
# Version information
RDD_VERSION = "1.0.0"
```

### Usage Analysis

**1. Used in rdd.py itself:**
- Line 1203: `show_version()` function displays the version:
  ```python
  def show_version() -> None:
      """Show version information."""
      print(f"RDD Framework v{RDD_VERSION} (Python)")
  ```

**2. No longer used in build.py:**
According to P01 implementation, the build script was already fixed to read version from `.rdd-docs/config.json` instead of `RDD_VERSION`. The build script now reads:
```python
# Step 1: Extract version from .rdd-docs/config.json
config_path = repo_root / ".rdd-docs" / "config.json"
with open(config_path, "r") as f:
    config = json.load(f)
version = config.get("version")
```

**3. Documentation references:**
- `.rdd-docs/tech-spec.md` line 272
- `.rdd-docs/folder-structure.md` line 172
- `.rdd-docs/requirements.md` line 142 (requirement TR-33)

These documentation references describe the old behavior and need to be updated.

### Conclusion
The `RDD_VERSION` variable is **only used once** in `rdd.py` itself (in the `show_version()` function). It is no longer used by the build system after P01 fixes. It is obsolete and should be:
1. Removed from `rdd.py`
2. Replaced with a function that reads version from `.rdd-docs/config.json`
3. Documentation references should be updated

## Implementation Plan

### Step 1: Create version reading function
Add a new function to read version from config.json in `rdd.py`

### Step 2: Update show_version() function
Replace `RDD_VERSION` usage with the new config reading function

### Step 3: Remove RDD_VERSION variable
Delete the variable definition

### Step 4: Update documentation
Update references in documentation files

## Implementation Details

### Changes to .rdd/scripts/rdd.py

1. **Add new function to read version from config:**
```python
def get_framework_version() -> str:
    """Get framework version from config.json"""
    config_path = get_rdd_config_path()
    if os.path.isfile(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get("version", "unknown")
        except Exception:
            pass
    return "unknown"
```

2. **Update show_version() function:**
```python
def show_version() -> None:
    """Show version information."""
    version = get_framework_version()
    print(f"RDD Framework v{version} (Python)")
```

3. **Remove RDD_VERSION variable:**
Delete lines 48-49:
```python
# Version information
RDD_VERSION = "1.0.0"
```

### Changes to documentation files

1. **Update .rdd-docs/tech-spec.md**
2. **Update .rdd-docs/folder-structure.md**
3. **Update .rdd-docs/requirements.md** (requirement TR-33)

## Execution Log

### Status: Completed ✅

#### Step 1: Added version reading function
Created `get_framework_version()` function in `rdd.py` that reads version from `.rdd-docs/config.json`:
```python
def get_framework_version() -> str:
    """Get framework version from config.json"""
    config_path = get_rdd_config_path()
    if os.path.isfile(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get("version", "unknown")
        except Exception:
            pass
    return "unknown"
```

#### Step 2: Updated show_version() function
Modified `show_version()` to use the new function instead of `RDD_VERSION`:
```python
def show_version() -> None:
    """Show version information."""
    version = get_framework_version()
    print(f"RDD Framework v{version} (Python)")
```

#### Step 3: Removed RDD_VERSION variable
Deleted the obsolete variable definition from `rdd.py` (lines 48-49)

#### Step 4: Updated documentation
Updated references in:
- `.rdd-docs/tech-spec.md` - Build script version management section
- `.rdd-docs/folder-structure.md` - Build artifacts version source
- `.rdd-docs/requirements.md` - Requirement TR-33

#### Verification
Tested the version command:
```bash
python .rdd/scripts/rdd.py --version
# Output: RDD Framework v1.0.1 (Python)
```
✅ Successfully reads version from config.json (showing 1.0.1)

## Summary

The `RDD_VERSION` variable has been successfully removed from `rdd.py`. The framework now:
- Reads version from `.rdd-docs/config.json` (single source of truth)
- Has no hardcoded version in Python code
- Returns "unknown" as graceful fallback if config is missing
- All documentation updated to reflect the new behavior

This eliminates the risk of forgotten version updates and ensures consistency across the framework.

