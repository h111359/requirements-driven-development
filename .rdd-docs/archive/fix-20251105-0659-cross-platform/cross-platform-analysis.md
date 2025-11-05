# Cross-Platform Script Execution Analysis

## Executive Summary

This document analyzes 5 different approaches to make the RDD framework prompts execute Python scripts properly on both Linux and Windows platforms. The analysis covers technical implementation, pros/cons, and recommendations for each approach.

**Current Challenge:** Prompt files in `.github/prompts/` use `python3 .rdd/scripts/rdd.py` which works on Linux/macOS but fails on Windows where `python` (not `python3`) is the standard command.

---

## Variant 1: Use Platform-Agnostic `python` Command

### Description
Replace all `python3` references with `python` in prompt files, as modern Python installations (3.3+) support `python` on all platforms.

### Implementation
**Change in prompt files:**
```bash
# Before
python3 .rdd/scripts/rdd.py change create enh

# After
python .rdd/scripts/rdd.py change create enh
```

### Pros
- ✅ **Simplest solution** - minimal changes required
- ✅ **Works on Windows** natively
- ✅ **Works on modern Linux/macOS** distributions
- ✅ **No wrapper scripts needed**
- ✅ **Direct, readable commands**
- ✅ **Easy to maintain**
- ✅ **No performance overhead**

### Cons
- ⚠️ **May fail on older Linux systems** where `python` points to Python 2.x
- ⚠️ **Requires user awareness** about Python version
- ⚠️ **Inconsistent with common Linux best practices** (using `python3` explicitly)

### Compatibility Assessment
- ✅ **Windows 10/11**: Excellent (standard)
- ✅ **Modern Linux (2020+)**: Excellent (most distros now make `python` point to Python 3)
- ⚠️ **Older Linux**: Moderate (may require manual symlink)
- ✅ **macOS**: Good (especially with Homebrew or official installer)

---

## Variant 2: Create Shell Wrapper Scripts

### Description
Create wrapper scripts that detect the platform and call the appropriate Python command.

### Implementation

**File: `.rdd/scripts/rdd-wrapper.sh`** (Linux/macOS)
```bash
#!/usr/bin/env bash
# RDD Wrapper for Linux/macOS
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python not found" >&2
    exit 1
fi

# Execute the RDD script
exec "$PYTHON_CMD" "$SCRIPT_DIR/rdd.py" "$@"
```

**File: `.rdd/scripts/rdd-wrapper.bat`** (Windows)
```batch
@echo off
REM RDD Wrapper for Windows
setlocal

REM Detect Python command
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
) else (
    where python3 >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=python3
    ) else (
        echo Error: Python not found >&2
        exit /b 1
    )
)

REM Execute the RDD script
%PYTHON_CMD% "%~dp0rdd.py" %*
```

**File: `.rdd/scripts/rdd-wrapper.ps1`** (PowerShell - Windows)
```powershell
#!/usr/bin/env pwsh
# RDD Wrapper for PowerShell
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Detect Python command
$PythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $PythonCmd = "python3"
} else {
    Write-Error "Error: Python not found"
    exit 1
}

# Execute the RDD script
& $PythonCmd "$ScriptDir/rdd.py" $args
```

**Usage in prompts:**
```bash
# Linux/macOS
.rdd/scripts/rdd-wrapper.sh change create enh

# Windows (cmd)
.rdd\scripts\rdd-wrapper.bat change create enh

# Windows (PowerShell)
.rdd/scripts/rdd-wrapper.ps1 change create enh
```

### Pros
- ✅ **Robust platform detection**
- ✅ **Handles multiple Python installations**
- ✅ **Falls back gracefully**
- ✅ **Consistent user experience**
- ✅ **Works on any Python 3.x setup**

### Cons
- ❌ **Requires multiple wrapper files** (3 files minimum)
- ❌ **More complex to maintain**
- ❌ **Still needs platform-specific commands in prompts**
- ❌ **Additional layer of indirection**
- ⚠️ **Execution policies may block scripts on Windows**
- ❌ **Not significantly better than Variant 1 for this use case**

---

## Variant 3: Python Script with Shebang + Make Executable

### Description
Make the Python script executable with proper shebang and call it directly without specifying Python interpreter.

### Implementation

**Modify `.rdd/scripts/rdd.py`:**
```python
#!/usr/bin/env python3
"""
rdd.py - Main wrapper script
"""
# ... rest of the file
```

**Make executable (Linux/macOS):**
```bash
chmod +x .rdd/scripts/rdd.py
```

**Create `.rdd/scripts/rdd.cmd` for Windows:**
```batch
@echo off
python "%~dp0rdd.py" %*
```

**Usage in prompts:**
```bash
# Linux/macOS
./.rdd/scripts/rdd.py change create enh

# Windows
.rdd\scripts\rdd.cmd change create enh
```

### Pros
- ✅ **Direct script execution on Linux/macOS**
- ✅ **No need to specify interpreter on Unix systems**
- ✅ **Clean, professional approach**
- ✅ **Follows Unix conventions**

### Cons
- ❌ **Doesn't work on Windows** (shebang ignored)
- ❌ **Still requires separate command for Windows**
- ❌ **Need to maintain `.cmd` wrapper**
- ⚠️ **May require `python3` to exist on the system**
- ❌ **Two different commands in prompts based on OS**

---

## Variant 4: GitHub Copilot's `mcp_pylance` Tool

### Description
Instead of running terminal commands, use GitHub Copilot's built-in `mcp_pylance_mcp_s_pylanceRunCodeSnippet` tool to execute Python code directly.

### Implementation

**Example in prompt file:**
Instead of:
```bash
python3 .rdd/scripts/rdd.py prompt mark-completed P01
```

Use in Copilot instructions:
```markdown
Execute the following Python code using the pylanceRunCodeSnippet tool:
```python
import sys
sys.path.insert(0, '.rdd/scripts')
from rdd import route_prompt
route_prompt(['mark-completed', 'P01'])
```

### Pros
- ✅ **Completely platform-agnostic**
- ✅ **No terminal command needed**
- ✅ **Works identically on all platforms**
- ✅ **Direct Python execution**
- ✅ **No command-line escaping issues**

### Cons
- ❌ **Only works within GitHub Copilot environment**
- ❌ **Cannot be run manually by users**
- ❌ **Verbose and complex prompt syntax**
- ❌ **Harder to debug**
- ❌ **Limited to Copilot Chat context**
- ❌ **Not suitable for documentation/user instructions**
- ❌ **Doesn't address the general use case**

---

## Variant 5: Environment Variable Configuration

### Description
Create a system where users set an environment variable for Python command, with automatic fallback detection.

### Implementation

**Modify `.rdd/scripts/rdd.py` to detect Python:**
```python
#!/usr/bin/env python3
import os
import sys
import shutil

def get_python_command():
    """Detect the appropriate Python command for this platform."""
    # Check environment variable first
    if 'RDD_PYTHON_CMD' in os.environ:
        return os.environ['RDD_PYTHON_CMD']
    
    # Auto-detect
    if shutil.which('python3'):
        return 'python3'
    elif shutil.which('python'):
        return 'python'
    else:
        return sys.executable  # Use the current Python interpreter
```

**Create `.rdd/scripts/run-rdd.sh` (cross-platform launcher):**
```bash
#!/usr/bin/env bash
# Cross-platform RDD launcher
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use environment variable or detect Python
PYTHON="${RDD_PYTHON_CMD:-}"

if [ -z "$PYTHON" ]; then
    if command -v python3 &> /dev/null; then
        PYTHON="python3"
    elif command -v python &> /dev/null; then
        PYTHON="python"
    else
        echo "Error: Python not found" >&2
        exit 1
    fi
fi

exec "$PYTHON" "$SCRIPT_DIR/rdd.py" "$@"
```

**User setup (optional):**
```bash
# Linux/macOS (.bashrc or .zshrc)
export RDD_PYTHON_CMD=python3

# Windows (PowerShell profile)
$env:RDD_PYTHON_CMD = "python"
```

**Usage in prompts:**
```bash
.rdd/scripts/run-rdd.sh change create enh  # Works on both platforms
```

### Pros
- ✅ **User-customizable**
- ✅ **Automatic fallback detection**
- ✅ **Works with unusual Python setups**
- ✅ **Single command in prompts**
- ✅ **Flexible for different environments**

### Cons
- ❌ **Requires additional launcher script**
- ⚠️ **Users must set environment variable for best experience**
- ⚠️ **Bash script may not work on Windows without Git Bash/WSL**
- ❌ **More complex initial setup**
- ❌ **Documentation overhead**

---

## Comparison Matrix

| Criterion | Variant 1 (python) | Variant 2 (Wrappers) | Variant 3 (Shebang) | Variant 4 (Copilot Tool) | Variant 5 (Env Var) |
|-----------|-------------------|---------------------|--------------------|-----------------------|-------------------|
| **Simplicity** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Cross-platform** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Maintainability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **User-friendly** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| **Robustness** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Documentation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

---

## Final Recommendation

### 🏆 **Recommended: Variant 1 (Use `python` command)**

**Rationale:**
1. **Modern Python installations support `python` command across platforms** - PEP 394 was updated in 2020 to allow `python` to point to Python 3
2. **Simplest implementation** - just replace `python3` with `python` in prompt files
3. **Works natively on Windows** - the primary concern
4. **Minimal maintenance burden**
5. **Best user experience** - no wrapper scripts, no configuration needed

**Implementation Steps:**
1. Update all prompt files in `.github/prompts/` to use `python` instead of `python3`
2. Update the shebang in `.rdd/scripts/rdd.py` to `#!/usr/bin/env python3` (Linux/macOS will still use python3, Windows ignores shebang)
3. Document the Python 3 requirement in README.md
4. Add a troubleshooting section for users with older systems

**Fallback Plan:**
If users encounter issues on older Linux systems where `python` points to Python 2, they can:
- Create an alias: `alias python=python3`
- Create a symlink: `sudo ln -s /usr/bin/python3 /usr/local/bin/python`
- Manually replace `python` with `python3` in their local copy

### 🥈 **Alternative: Variant 5 (Environment Variable)**

If the project requires maximum flexibility and robustness (e.g., supporting legacy systems, custom Python installations), Variant 5 is the second-best choice. However, it adds complexity without significant benefit for most users.

---

## Migration Path

### Step 1: Update Prompt Files
Replace all occurrences of `python3` with `python` in these files:
- `.github/prompts/rdd.01-initiate.prompt.md`
- `.github/prompts/rdd.06-execute.prompt.md`
- `.github/prompts/rdd.08-wrap-up.prompt.md`
- `.github/prompts/rdd.09-clean-up.prompt.md`
- `.github/prompts/rdd.G4-update-from-main.prompt.md`

### Step 2: Update Documentation
Add to README.md:
```markdown
## Requirements
- Python 3.7 or higher
- Git 2.23 or higher

Note: The `python` command must point to Python 3.x. On older Linux systems, 
you may need to create an alias or symlink if `python` points to Python 2.x.
```

### Step 3: Test on Both Platforms
- Test on Linux (Ubuntu 20.04+, Fedora 35+)
- Test on macOS (Big Sur+)
- Test on Windows 10/11

---

## Appendix: Command Examples

### Current State (Linux-specific)
```bash
python3 .rdd/scripts/rdd.py change create enh
python3 .rdd/scripts/rdd.py prompt mark-completed P01
python3 .rdd/scripts/rdd.py branch cleanup
```

### After Migration (Cross-platform)
```bash
python .rdd/scripts/rdd.py change create enh
python .rdd/scripts/rdd.py prompt mark-completed P01
python .rdd/scripts/rdd.py branch cleanup
```

---

## Conclusion

**Variant 1** (using `python` instead of `python3`) is the optimal solution for the RDD framework. It balances simplicity, cross-platform compatibility, and maintainability while addressing the core issue of Windows compatibility without introducing unnecessary complexity.

The migration is straightforward, low-risk, and can be completed in a single update cycle. Edge cases (older Linux systems) are rare in modern development environments and can be easily addressed through documentation and simple workarounds.

