#!/usr/bin/env python3
"""
build.py
Build script for creating RDD framework releases
Creates a single cross-platform zip archive with installer
"""

import sys
import os
import re
import json
import shutil
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
import zipfile

# Color codes for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_success(msg: str):
    print(f"{Colors.GREEN}✓{Colors.NC} {msg}")

def print_error(msg: str):
    print(f"{Colors.RED}✗{Colors.NC} {msg}", file=sys.stderr)

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ{Colors.NC} {msg}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠{Colors.NC} {msg}")

def print_step(step: int, total: int, msg: str):
    print(f"{Colors.BLUE}[{step}/{total}]{Colors.NC} {msg}")

def exit_with_error(msg: str, code: int = 1):
    print_error(msg)
    sys.exit(code)

def extract_version(rdd_py_path: Path) -> str:
    """Extract version from rdd.py file"""
    print_info(f"Extracting version from {rdd_py_path}")
    
    if not rdd_py_path.exists():
        exit_with_error(f"File not found: {rdd_py_path}")
    
    content = rdd_py_path.read_text()
    match = re.search(r'RDD_VERSION\s*=\s*["\']([^"\']+)["\']', content)
    
    if not match:
        exit_with_error("Could not find RDD_VERSION in rdd.py")
    
    version = match.group(1)
    
    # Validate SemVer format
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        exit_with_error(f"Invalid version format: {version}. Expected SemVer (X.Y.Z)")
    
    print_success(f"Found version: {version}")
    return version

def create_build_dir(version: str, build_root: Path) -> Path:
    """Create clean build directory structure"""
    build_dir = build_root / f"rdd-v{version}"
    
    print_info(f"Creating build directory: {build_dir}")
    
    # Clean existing directory if present
    if build_dir.exists():
        print_warning(f"Removing existing build directory: {build_dir}")
        shutil.rmtree(build_dir)
    
    # Create directory structure
    build_dir.mkdir(parents=True, exist_ok=True)
    (build_dir / ".github" / "prompts").mkdir(parents=True, exist_ok=True)
    (build_dir / ".rdd" / "scripts").mkdir(parents=True, exist_ok=True)
    (build_dir / ".rdd" / "templates").mkdir(parents=True, exist_ok=True)
    (build_dir / ".vscode").mkdir(parents=True, exist_ok=True)
    
    print_success(f"Build directory created: {build_dir}")
    return build_dir

def copy_prompts(repo_root: Path, build_dir: Path):
    """Copy all prompt files to build directory"""
    print_info("Copying prompt files...")
    
    prompts_src = repo_root / ".github" / "prompts"
    prompts_dst = build_dir / ".github" / "prompts"
    
    if not prompts_src.exists():
        exit_with_error(f"Prompts directory not found: {prompts_src}")
    
    copied = 0
    for prompt_file in prompts_src.glob("*.prompt.md"):
        shutil.copy2(prompt_file, prompts_dst / prompt_file.name)
        copied += 1
    
    if copied == 0:
        exit_with_error(f"No prompt files found in {prompts_src}")
    
    print_success(f"Copied {copied} prompt file(s)")

def copy_scripts(repo_root: Path, build_dir: Path):
    """Copy RDD scripts to build directory"""
    print_info("Copying script files...")
    
    scripts_src = repo_root / ".rdd" / "scripts"
    scripts_dst = build_dir / ".rdd" / "scripts"
    
    scripts_to_copy = ["rdd.py", "rdd_utils.py"]
    
    for script_name in scripts_to_copy:
        script_path = scripts_src / script_name
        if not script_path.exists():
            exit_with_error(f"Required script not found: {script_path}")
        shutil.copy2(script_path, scripts_dst / script_name)
    
    print_success(f"Copied {len(scripts_to_copy)} script file(s)")

def copy_templates(repo_root: Path, build_dir: Path):
    """Copy all template files to build directory"""
    print_info("Copying template files...")
    
    templates_src = repo_root / ".rdd" / "templates"
    templates_dst = build_dir / ".rdd" / "templates"
    
    if not templates_src.exists():
        exit_with_error(f"Templates directory not found: {templates_src}")
    
    copied = 0
    for template_file in templates_src.iterdir():
        if template_file.is_file():
            shutil.copy2(template_file, templates_dst / template_file.name)
            copied += 1
    
    if copied == 0:
        exit_with_error(f"No template files found in {templates_src}")
    
    print_success(f"Copied {copied} template file(s)")

def copy_license(repo_root: Path, build_dir: Path):
    """Copy LICENSE file to build directory"""
    print_info("Copying LICENSE file...")
    
    license_src = repo_root / "LICENSE"
    
    if not license_src.exists():
        print_warning("LICENSE file not found - skipping")
        return
    
    shutil.copy2(license_src, build_dir / "LICENSE")
    print_success("Copied LICENSE file")

def copy_vscode_settings(repo_root: Path, build_dir: Path):
    """Copy VS Code settings template"""
    print_info("Copying VS Code settings template...")
    
    settings_src = repo_root / ".rdd" / "templates" / "settings.json"
    settings_dst = build_dir / ".vscode" / "settings.json"
    
    if not settings_src.exists():
        exit_with_error(f"Settings template not found: {settings_src}")
    
    shutil.copy2(settings_src, settings_dst)
    print_success("Copied VS Code settings template")

def generate_readme(build_dir: Path, version: str):
    """Generate README.md with installation instructions"""
    print_info("Generating README.md...")
    
    readme_content = f"""# RDD Framework v{version}

Requirements-Driven Development (RDD) is a structured workflow automation framework that guides developers through requirement clarification, implementation, and documentation processes.

## System Requirements

- **Python 3.7+** 
  - Windows & macOS: Available by default with modern Python installations
  - Linux: Install `python-is-python3` package or create alias if `python` command is not available
- **Git 2.23+**
- **VS Code** (recommended)
- **GitHub Copilot** (optional but recommended)

### Python Command Setup

The RDD framework uses the `python` command (not `python3`) for cross-platform compatibility.

**Linux users**: If the `python` command is not available on your system, install it with:
```bash
sudo apt-get install python-is-python3  # Ubuntu/Debian
```
Or create an alias:
```bash
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc
```

## Installation

### Option 1: Interactive Installation (Recommended)

The interactive installer provides a visual menu to navigate and select your project directory.

#### Windows

1. **Extract this archive** to a temporary location (e.g., `C:\\Users\\YourName\\Downloads\\rdd-v{version}`)
2. **Open PowerShell** (right-click Start menu → Windows PowerShell)
3. **Navigate to extracted folder**:
   ```powershell
   cd C:\\Users\\YourName\\Downloads\\rdd-v{version}
   ```
4. **Run the interactive installer**:
   ```powershell
   .\\install.ps1
   ```
5. **Navigate with arrow keys** (↑/↓) to browse folders
6. **Press Enter** on a folder to enter it, or select `[SELECT THIS DIRECTORY]` to install here
7. **Confirm installation** when prompted

#### Linux/macOS

1. **Extract this archive** to a temporary location (e.g., `/tmp/rdd-v{version}`)
2. **Open terminal**
3. **Navigate to extracted folder**:
   ```bash
   cd /tmp/rdd-v{version}
   ```
4. **Make the installer executable**:
   ```bash
   chmod +x install.sh
   ```
5. **Run the interactive installer**:
   ```bash
   ./install.sh
   ```
6. **Navigate with arrow keys** (↑/↓) to browse folders
7. **Press Enter** on a folder to enter it, or select `[SELECT THIS DIRECTORY]` to install here
8. **Confirm installation** when prompted

### Option 2: Direct Python Installation

If you prefer to specify the path directly or the interactive installer doesn't work:

#### Windows
```powershell
cd C:\\path\\to\\your\\project
python C:\\Users\\YourName\\Downloads\\rdd-v{version}\\install.py
```

#### Linux/macOS
```bash
cd /path/to/your/project
python /tmp/rdd-v{version}/install.py
```

The installer will:
- Verify prerequisites
- Copy RDD framework files to your project
- Merge VS Code settings
- Update .gitignore

### Option 3: Manual Installation

If you prefer manual installation or the installers don't work:

#### Windows (PowerShell)
```powershell
# Copy prompts
Copy-Item -Recurse .github\\prompts C:\\path\\to\\your\\project\\.github\\

# Copy RDD framework
Copy-Item -Recurse .rdd C:\\path\\to\\your\\project\\

# Update .gitignore
Add-Content C:\\path\\to\\your\\project\\.gitignore ".rdd-docs/workspace/"
```

#### Linux/macOS (Bash)
```bash
# Copy prompts
cp -r .github/prompts /path/to/your/project/.github/

# Copy RDD framework
cp -r .rdd /path/to/your/project/

# Set executable permissions
chmod +x /path/to/your/project/.rdd/scripts/rdd.py

# Update .gitignore
echo ".rdd-docs/workspace/" >> /path/to/your/project/.gitignore
```

**Then manually merge VS Code settings**:
- Copy settings from `.vscode/settings.json` to your project's `.vscode/settings.json`
- Merge the arrays (don't replace existing settings)

## Verification

After installation, verify RDD is working:

#### Windows
```powershell
cd C:\\path\\to\\your\\project
python .rdd\\scripts\\rdd.py --version
```

#### Linux/macOS
```bash
cd /path/to/your/project
python .rdd/scripts/rdd.py --version
```

You should see: `RDD Framework v{version}`

## Getting Started

Initialize your first enhancement or fix:

#### Windows
```powershell
python .rdd\\scripts\\rdd.py change create enh my-first-feature
```

#### Linux/macOS
```bash
python .rdd/scripts/rdd.py change create enh my-first-feature
```

Then follow the RDD workflow prompts in VS Code with GitHub Copilot.

## Troubleshooting

### "python: command not found" (Linux)
Install the python-is-python3 package or create an alias (see System Requirements above).

### "Not a git repository"
RDD requires your project to be a Git repository. Initialize one with:
```bash
git init
```

### "Permission denied" (Linux/macOS)
Make the script executable:
```bash
chmod +x .rdd/scripts/rdd.py
```

### VS Code settings not taking effect
1. Restart VS Code
2. Check `.vscode/settings.json` was created/updated
3. Verify GitHub Copilot extension is installed

## Documentation

For more information, visit: https://github.com/h111359/requirements-driven-development

## License

See LICENSE file for details.
"""
    
    readme_path = build_dir / "README.md"
    readme_path.write_text(readme_content)
    print_success("Generated README.md")

def generate_installer(build_dir: Path, version: str):
    """Generate install.py script"""
    print_info("Generating install.py...")
    
    installer_content = '''#!/usr/bin/env python3
"""
install.py
RDD Framework Installer
Installs RDD framework into a target Git repository
"""

import sys
import os
import json
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

# Minimum Python version
MIN_PYTHON_VERSION = (3, 7)

# Color codes for output
class Colors:
    RED = '\\033[0;31m'
    GREEN = '\\033[0;32m'
    YELLOW = '\\033[0;33m'
    BLUE = '\\033[0;34m'
    NC = '\\033[0m'  # No Color

def print_success(msg: str):
    print(f"{Colors.GREEN}✓{Colors.NC} {msg}")

def print_error(msg: str):
    print(f"{Colors.RED}✗{Colors.NC} {msg}", file=sys.stderr)

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ{Colors.NC} {msg}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠{Colors.NC} {msg}")

def print_banner():
    print()
    print("=" * 60)
    print(f"  RDD Framework Installer v''' + version + '''")
    print("=" * 60)
    print()

def exit_with_error(msg: str, code: int = 1):
    print_error(msg)
    sys.exit(code)

def check_python_version():
    """Verify Python version is 3.7+"""
    print_info("Checking Python version...")
    
    current = sys.version_info
    if current < MIN_PYTHON_VERSION:
        exit_with_error(
            f"Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+ required. "
            f"Found: {current.major}.{current.minor}.{current.micro}\\n"
            f"Please upgrade Python: https://www.python.org/downloads/"
        )
    
    print_success(f"Python {current.major}.{current.minor}.{current.micro} detected")

def check_git_installed() -> bool:
    """Check if Git is installed"""
    print_info("Checking for Git...")
    
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        print_success(f"{version} detected")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        exit_with_error(
            "Git is not installed or not in PATH\\n"
            "Install Git: https://git-scm.com/downloads"
        )
        return False

def check_git_repo(target_dir: Path) -> bool:
    """Check if target directory is a Git repository"""
    print_info(f"Checking if {target_dir} is a Git repository...")
    
    git_dir = target_dir / ".git"
    if not git_dir.exists():
        exit_with_error(
            f"{target_dir} is not a Git repository\\n"
            f"Initialize with: cd {target_dir} && git init"
        )
        return False
    
    print_success("Git repository confirmed")
    return True

def detect_existing_installation(target_dir: Path) -> bool:
    """Check if RDD is already installed"""
    print_info("Checking for existing RDD installation...")
    
    rdd_script = target_dir / ".rdd" / "scripts" / "rdd.py"
    prompts_dir = target_dir / ".github" / "prompts"
    
    has_scripts = rdd_script.exists()
    has_prompts = prompts_dir.exists() and any(prompts_dir.glob("rdd.*.prompt.md"))
    
    if has_scripts or has_prompts:
        print_warning("Existing RDD installation detected")
        return True
    
    print_info("No existing installation found")
    return False

def get_target_directory() -> Path:
    """Prompt user for target directory"""
    default = Path.cwd()
    
    print()
    print(f"Target directory (default: {default}):")
    response = input("> ").strip()
    
    if not response:
        target = default
    else:
        target = Path(response).expanduser().resolve()
    
    if not target.exists():
        exit_with_error(f"Directory does not exist: {target}")
    
    if not target.is_dir():
        exit_with_error(f"Not a directory: {target}")
    
    return target

def confirm_installation(target_dir: Path, is_upgrade: bool) -> bool:
    """Get user confirmation to proceed"""
    print()
    if is_upgrade:
        print_warning("This will OVERWRITE the existing RDD installation.")
    
    print(f"Install RDD Framework to: {target_dir}")
    print("Proceed? (y/N):")
    response = input("> ").strip().lower()
    
    return response in ['y', 'yes']

def copy_prompts(source_dir: Path, target_dir: Path):
    """Copy prompt files to target"""
    print_info("Installing prompts...")
    
    src_prompts = source_dir / ".github" / "prompts"
    dst_prompts = target_dir / ".github" / "prompts"
    
    dst_prompts.mkdir(parents=True, exist_ok=True)
    
    copied = 0
    for prompt_file in src_prompts.glob("*.prompt.md"):
        shutil.copy2(prompt_file, dst_prompts / prompt_file.name)
        copied += 1
    
    print_success(f"Installed {copied} prompt file(s)")

def copy_rdd_framework(source_dir: Path, target_dir: Path):
    """Copy .rdd directory to target"""
    print_info("Installing RDD framework...")
    
    src_rdd = source_dir / ".rdd"
    dst_rdd = target_dir / ".rdd"
    
    # Remove existing installation
    if dst_rdd.exists():
        shutil.rmtree(dst_rdd)
    
    shutil.copytree(src_rdd, dst_rdd)
    
    # Set executable permissions on rdd.py (Unix)
    if os.name != 'nt':  # Not Windows
        rdd_script = dst_rdd / "scripts" / "rdd.py"
        rdd_script.chmod(0o755)
    
    print_success("Installed RDD framework")

def merge_vscode_settings(source_dir: Path, target_dir: Path):
    """Merge VS Code settings with existing settings"""
    print_info("Merging VS Code settings...")
    
    src_settings = source_dir / ".vscode" / "settings.json"
    dst_settings = target_dir / ".vscode" / "settings.json"
    
    # Load source settings
    try:
        with open(src_settings, 'r') as f:
            # Remove comments for JSON parsing
            content = f.read()
            # Simple comment removal (not perfect but works for this case)
            lines = [line.split('//')[0].rstrip() for line in content.split('\\n')]
            clean_content = '\\n'.join(lines)
            source_data = json.loads(clean_content)
    except Exception as e:
        print_warning(f"Could not load source settings: {e}")
        return
    
    # Load existing settings or create empty
    if dst_settings.exists():
        try:
            with open(dst_settings, 'r') as f:
                target_data = json.load(f)
        except Exception as e:
            print_warning(f"Could not load existing settings: {e}")
            target_data = {}
    else:
        target_data = {}
        dst_settings.parent.mkdir(parents=True, exist_ok=True)
    
    # Merge settings
    merged = merge_settings(source_data, target_data)
    
    # Write merged settings
    try:
        with open(dst_settings, 'w') as f:
            json.dump(merged, f, indent=2)
        print_success("Merged VS Code settings")
    except Exception as e:
        print_warning(f"Could not write settings: {e}")

def merge_settings(source: Dict[str, Any], target: Dict[str, Any]) -> Dict[str, Any]:
    """Merge source settings into target settings"""
    merged = target.copy()
    
    # Arrays: append unique values
    array_keys = ['chat.promptFilesRecommendations', 'chat.tools.terminal.autoApprove']
    for key in array_keys:
        if key in source:
            if isinstance(source[key], dict):
                # Handle object format (new format)
                merged.setdefault(key, {})
                merged[key].update(source[key])
            elif isinstance(source[key], list):
                # Handle array format (old format)
                existing = set(merged.get(key, []))
                new_items = source[key]
                merged[key] = list(existing) + [
                    item for item in new_items if item not in existing
                ]
    
    # Object: merge keys
    if 'files.associations' in source:
        merged.setdefault('files.associations', {})
        merged['files.associations'].update(source['files.associations'])
    
    # Array: replace (RDD requires specific values)
    if 'editor.rulers' in source:
        merged['editor.rulers'] = source['editor.rulers']
    
    return merged

def update_gitignore(target_dir: Path):
    """Update .gitignore to exclude workspace"""
    print_info("Updating .gitignore...")
    
    gitignore_path = target_dir / ".gitignore"
    workspace_entry = ".rdd-docs/workspace/"
    
    # Read existing or create empty
    if gitignore_path.exists():
        lines = gitignore_path.read_text().splitlines()
    else:
        lines = []
    
    # Check if already present
    patterns = [
        '.rdd-docs/workspace/',
        '.rdd-docs/workspace',
        '.rdd-docs/workspace/*',
    ]
    
    for line in lines:
        if any(pattern in line for pattern in patterns):
            print_info(".gitignore already contains workspace exclusion")
            return
    
    # Add entry
    if lines and lines[-1].strip():  # Add blank line if needed
        lines.append('')
    lines.append('# RDD framework workspace (auto-generated)')
    lines.append(workspace_entry)
    
    # Write back
    gitignore_path.write_text('\\n'.join(lines) + '\\n')
    print_success("Updated .gitignore")

def verify_installation(target_dir: Path) -> bool:
    """Verify installation completed successfully"""
    print_info("Verifying installation...")
    
    # Check key files exist
    checks = [
        target_dir / ".rdd" / "scripts" / "rdd.py",
        target_dir / ".rdd" / "scripts" / "rdd_utils.py",
        target_dir / ".github" / "prompts",
    ]
    
    for path in checks:
        if not path.exists():
            print_error(f"Missing: {path}")
            return False
    
    # Test RDD command
    try:
        result = subprocess.run(
            ["python", str(target_dir / ".rdd" / "scripts" / "rdd.py"), "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        version_output = result.stdout.strip()
        print_success(f"RDD command verified: {version_output}")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"RDD command test failed: {e}")
        return False

def main():
    """Main installation flow"""
    print_banner()
    
    # Get source directory (where this script is located)
    source_dir = Path(__file__).parent.absolute()
    
    # Pre-flight checks
    check_python_version()
    check_git_installed()
    
    # Get target directory
    target_dir = get_target_directory()
    check_git_repo(target_dir)
    
    # Check for existing installation
    is_upgrade = detect_existing_installation(target_dir)
    
    # Get confirmation
    if not confirm_installation(target_dir, is_upgrade):
        print_info("Installation cancelled by user")
        sys.exit(0)
    
    print()
    print("Installing...")
    print()
    
    try:
        # Install files
        copy_prompts(source_dir, target_dir)
        copy_rdd_framework(source_dir, target_dir)
        merge_vscode_settings(source_dir, target_dir)
        update_gitignore(target_dir)
        
        # Verify
        if not verify_installation(target_dir):
            exit_with_error("Installation verification failed")
        
        # Success
        print()
        print("=" * 60)
        print_success("RDD Framework installed successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  1. Restart VS Code")
        print("  2. Create your first change:")
        print(f"     cd {target_dir}")
        print("     python .rdd/scripts/rdd.py change create enh my-feature")
        print()
        print("Documentation: https://github.com/h111359/requirements-driven-development")
        print()
        
    except Exception as e:
        exit_with_error(f"Installation failed: {e}")

if __name__ == "__main__":
    main()
'''
    
    installer_path = build_dir / "install.py"
    installer_path.write_text(installer_content)
    
    # Make executable on Unix systems
    if os.name != 'nt':
        installer_path.chmod(0o755)
    
    print_success("Generated install.py")

def generate_bash_installer(build_dir: Path, version: str):
    """Generate install.sh interactive installer script for Linux/macOS"""
    print_info("Generating install.sh...")
    
    installer_content = '''#!/usr/bin/env bash
"""
install.sh
RDD Framework Interactive Installer for Linux/macOS
Provides visual folder navigation for installation directory selection
"""

set -e

# Version from build
VERSION="''' + version + '''"

# Colors
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[0;33m'
BLUE='\\033[0;34m'
CYAN='\\033[0;36m'
BOLD='\\033[1m'
NC='\\033[0m' # No Color

# Current navigation state
CURRENT_DIR=""
SELECTED_INDEX=0

# Print colored messages
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_banner() {
    clear
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║      RDD Framework Interactive Installer v${VERSION}           ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check Python
    if ! command -v python &> /dev/null; then
        print_error "Python is not installed or not in PATH"
        print_error "Install Python 3.7+ from: https://www.python.org/downloads/"
        exit 1
    fi
    
    # Check Python version
    python_version=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    print_success "Python ${python_version} detected"
    
    # Check Git
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed or not in PATH"
        print_error "Install Git from: https://git-scm.com/downloads"
        exit 1
    fi
    
    git_version=$(git --version)
    print_success "${git_version} detected"
    
    echo ""
}

# Navigate folders with visual menu
navigate_folders() {
    local start_dir="$1"
    CURRENT_DIR="$(cd "$start_dir" && pwd)"
    SELECTED_INDEX=0
    
    while true; do
        # Get list of directories
        local dirs=()
        
        # Add parent directory option if not at root
        if [ "$CURRENT_DIR" != "/" ]; then
            dirs+=("..")
        fi
        
        # Add "select this" option
        dirs+=(".")
        
        # Add subdirectories (only directories, sorted)
        while IFS= read -r dir; do
            if [ -d "$CURRENT_DIR/$dir" ] && [ "$dir" != "." ] && [ "$dir" != ".." ]; then
                dirs+=("$dir")
            fi
        done < <(ls -1 "$CURRENT_DIR" 2>/dev/null | sort)
        
        # Ensure selected index is in bounds
        if [ $SELECTED_INDEX -lt 0 ]; then
            SELECTED_INDEX=0
        fi
        if [ $SELECTED_INDEX -ge ${#dirs[@]} ]; then
            SELECTED_INDEX=$((${#dirs[@]} - 1))
        fi
        
        # Draw menu
        draw_menu "${dirs[@]}"
        
        # Get user input
        read -rsn1 key
        
        case "$key" in
            $'\\e')  # Escape sequence (arrow keys)
                read -rsn2 key  # Read the rest of the escape sequence
                case "$key" in
                    '[A')  # Up arrow
                        SELECTED_INDEX=$((SELECTED_INDEX - 1))
                        if [ $SELECTED_INDEX -lt 0 ]; then
                            SELECTED_INDEX=0
                        fi
                        ;;
                    '[B')  # Down arrow
                        SELECTED_INDEX=$((SELECTED_INDEX + 1))
                        if [ $SELECTED_INDEX -ge ${#dirs[@]} ]; then
                            SELECTED_INDEX=$((${#dirs[@]} - 1))
                        fi
                        ;;
                esac
                ;;
            '')  # Enter key
                local selected="${dirs[$SELECTED_INDEX]}"
                if [ "$selected" = ".." ]; then
                    # Go to parent directory
                    CURRENT_DIR="$(cd "$CURRENT_DIR/.." && pwd)"
                    SELECTED_INDEX=0
                elif [ "$selected" = "." ]; then
                    # Select current directory
                    return 0
                else
                    # Enter subdirectory
                    CURRENT_DIR="$(cd "$CURRENT_DIR/$selected" && pwd)"
                    SELECTED_INDEX=0
                fi
                ;;
            'q'|'Q')  # Quit
                echo ""
                print_info "Installation cancelled by user"
                exit 0
                ;;
        esac
    done
}

# Draw the navigation menu
draw_menu() {
    local dirs=("$@")
    clear
    print_banner
    
    echo -e "${CYAN}${BOLD}Select Installation Directory${NC}"
    echo ""
    echo -e "${BOLD}Current:${NC} ${CURRENT_DIR}"
    echo ""
    echo "┌────────────────────────────────────────────────────────────┐"
    
    local index=0
    for dir in "${dirs[@]}"; do
        local display_name
        if [ "$dir" = ".." ]; then
            display_name="[..] Parent Directory"
        elif [ "$dir" = "." ]; then
            display_name="[SELECT THIS DIRECTORY]"
        else
            display_name="$dir/"
        fi
        
        if [ $index -eq $SELECTED_INDEX ]; then
            echo -e "│ ${GREEN}▶${NC} ${BOLD}${display_name}${NC}"
        else
            echo -e "│   ${display_name}"
        fi
        
        index=$((index + 1))
    done
    
    echo "└────────────────────────────────────────────────────────────┘"
    echo ""
    echo -e "${CYAN}Use ${BOLD}↑↓${NC}${CYAN} arrow keys to navigate, ${BOLD}Enter${NC}${CYAN} to select, ${BOLD}Q${NC}${CYAN} to quit${NC}"
}

# Validate git repository
validate_git_repo() {
    local target_dir="$1"
    
    print_info "Checking if $target_dir is a Git repository..."
    
    if [ ! -d "$target_dir/.git" ]; then
        echo ""
        print_error "Selected directory is not a Git repository"
        print_info "Initialize with: cd $target_dir && git init"
        echo ""
        read -p "Press Enter to continue..."
        return 1
    fi
    
    print_success "Git repository confirmed"
    return 0
}

# Confirm installation
confirm_installation() {
    local target_dir="$1"
    
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                    Installation Summary                    ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "${BOLD}Target Directory:${NC} ${target_dir}"
    echo -e "${BOLD}RDD Version:${NC} v${VERSION}"
    echo ""
    
    # Check for existing installation
    if [ -f "$target_dir/.rdd/scripts/rdd.py" ]; then
        print_warning "Existing RDD installation detected - will be OVERWRITTEN"
        echo ""
    fi
    
    read -p "$(echo -e ${BOLD}Proceed with installation? [y/N]:${NC} )" -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installation cancelled by user"
        exit 0
    fi
}

# Run Python installer
run_python_installer() {
    local source_dir="$1"
    local target_dir="$2"
    
    echo ""
    print_info "Running Python installer..."
    echo ""
    
    cd "$target_dir"
    python "$source_dir/install.py" <<EOF


EOF
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo ""
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║              Installation Completed Successfully!          ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
        print_success "RDD Framework v${VERSION} installed to: ${target_dir}"
        echo ""
        echo -e "${BOLD}Next steps:${NC}"
        echo "  1. Restart VS Code"
        echo "  2. Create your first change:"
        echo -e "     ${CYAN}cd ${target_dir}${NC}"
        echo -e "     ${CYAN}python .rdd/scripts/rdd.py change create enh my-feature${NC}"
        echo ""
        echo "Documentation: https://github.com/h111359/requirements-driven-development"
        echo ""
    else
        echo ""
        print_error "Installation failed with exit code: $exit_code"
        exit $exit_code
    fi
}

# Main execution
main() {
    # Get source directory (where this script is located)
    SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Prerequisites check
    check_prerequisites
    
    # Navigate to select installation directory
    print_info "Starting folder navigation..."
    print_info "Navigate with arrow keys, press Enter to select"
    echo ""
    sleep 2
    
    navigate_folders "$(pwd)"
    
    TARGET_DIR="$CURRENT_DIR"
    
    # Validate git repository
    while ! validate_git_repo "$TARGET_DIR"; do
        echo ""
        read -p "$(echo -e ${BOLD}Try selecting a different directory? [Y/n]:${NC} )" -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            print_info "Installation cancelled by user"
            exit 0
        fi
        
        navigate_folders "$TARGET_DIR"
        TARGET_DIR="$CURRENT_DIR"
    done
    
    # Confirm installation
    confirm_installation "$TARGET_DIR"
    
    # Run Python installer
    run_python_installer "$SOURCE_DIR" "$TARGET_DIR"
}

# Run main function
main
'''
    
    installer_path = build_dir / "install.sh"
    installer_path.write_text(installer_content)
    
    # Make executable on Unix systems
    if os.name != 'nt':
        installer_path.chmod(0o755)
    
    print_success("Generated install.sh")

def generate_powershell_installer(build_dir: Path, version: str):
    """Generate install.ps1 interactive installer script for Windows"""
    print_info("Generating install.ps1...")
    
    installer_content = '''<#
.SYNOPSIS
    RDD Framework Interactive Installer for Windows
.DESCRIPTION
    Provides visual folder navigation for installation directory selection
.NOTES
    Version: ''' + version + '''
#>

$ErrorActionPreference = 'Stop'
$VERSION = "''' + version + '''"

# Current navigation state
$script:CurrentDir = ""
$script:SelectedIndex = 0

# Print colored messages
function Write-Success {
    param([string]$Message)
    Write-Host "✓ " -ForegroundColor Green -NoNewline
    Write-Host $Message
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "✗ " -ForegroundColor Red -NoNewline
    Write-Host $Message
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ " -ForegroundColor Blue -NoNewline
    Write-Host $Message
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ " -ForegroundColor Yellow -NoNewline
    Write-Host $Message
}

function Write-Banner {
    Clear-Host
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗"
    Write-Host "║      RDD Framework Interactive Installer v$VERSION           ║"
    Write-Host "╚════════════════════════════════════════════════════════════╝"
    Write-Host ""
}

# Check prerequisites
function Test-Prerequisites {
    Write-Info "Checking prerequisites..."
    
    # Check Python
    try {
        $pythonVersion = & python --version 2>&1
        if ($LASTEXITCODE -ne 0) { throw }
        Write-Success "Python detected: $pythonVersion"
    }
    catch {
        Write-ErrorMsg "Python is not installed or not in PATH"
        Write-ErrorMsg "Install Python 3.7+ from: https://www.python.org/downloads/"
        exit 1
    }
    
    # Check Git
    try {
        $gitVersion = & git --version 2>&1
        if ($LASTEXITCODE -ne 0) { throw }
        Write-Success "$gitVersion detected"
    }
    catch {
        Write-ErrorMsg "Git is not installed or not in PATH"
        Write-ErrorMsg "Install Git from: https://git-scm.com/downloads/"
        exit 1
    }
    
    Write-Host ""
}

# Navigate folders with visual menu
function Start-FolderNavigation {
    param([string]$StartDir)
    
    $script:CurrentDir = (Resolve-Path $StartDir).Path
    $script:SelectedIndex = 0
    
    while ($true) {
        # Get list of directories
        $dirs = @()
        
        # Add parent directory option if not at root
        $parent = Split-Path -Parent $script:CurrentDir
        if ($parent) {
            $dirs += ".."
        }
        
        # Add "select this" option
        $dirs += "."
        
        # Add subdirectories (only directories, sorted)
        try {
            $subdirs = Get-ChildItem -Path $script:CurrentDir -Directory -ErrorAction SilentlyContinue | 
                       Sort-Object Name | 
                       Select-Object -ExpandProperty Name
            if ($subdirs) {
                $dirs += $subdirs
            }
        }
        catch {
            # Ignore errors (permission denied, etc.)
        }
        
        # Ensure selected index is in bounds
        if ($script:SelectedIndex -lt 0) {
            $script:SelectedIndex = 0
        }
        if ($script:SelectedIndex -ge $dirs.Count) {
            $script:SelectedIndex = $dirs.Count - 1
        }
        
        # Draw menu
        Show-Menu -Dirs $dirs
        
        # Get user input
        $key = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        
        switch ($key.VirtualKeyCode) {
            38 {  # Up arrow
                $script:SelectedIndex--
                if ($script:SelectedIndex -lt 0) {
                    $script:SelectedIndex = 0
                }
            }
            40 {  # Down arrow
                $script:SelectedIndex++
                if ($script:SelectedIndex -ge $dirs.Count) {
                    $script:SelectedIndex = $dirs.Count - 1
                }
            }
            13 {  # Enter
                $selected = $dirs[$script:SelectedIndex]
                if ($selected -eq "..") {
                    # Go to parent directory
                    $parent = Split-Path -Parent $script:CurrentDir
                    if ($parent) {
                        $script:CurrentDir = $parent
                        $script:SelectedIndex = 0
                    }
                }
                elseif ($selected -eq ".") {
                    # Select current directory
                    return $script:CurrentDir
                }
                else {
                    # Enter subdirectory
                    $script:CurrentDir = Join-Path $script:CurrentDir $selected
                    $script:SelectedIndex = 0
                }
            }
            81 {  # Q key
                Write-Host ""
                Write-Info "Installation cancelled by user"
                exit 0
            }
        }
    }
}

# Draw the navigation menu
function Show-Menu {
    param([array]$Dirs)
    
    Clear-Host
    Write-Banner
    
    Write-Host "Select Installation Directory" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Current: " -NoNewline
    Write-Host $script:CurrentDir -ForegroundColor White
    Write-Host ""
    Write-Host "┌────────────────────────────────────────────────────────────┐"
    
    $index = 0
    foreach ($dir in $Dirs) {
        $displayName = if ($dir -eq "..") {
            "[..] Parent Directory"
        }
        elseif ($dir -eq ".") {
            "[SELECT THIS DIRECTORY]"
        }
        else {
            "$dir\"
        }
        
        if ($index -eq $script:SelectedIndex) {
            Write-Host "│ " -NoNewline
            Write-Host "▶ " -ForegroundColor Green -NoNewline
            Write-Host $displayName -ForegroundColor White
        }
        else {
            Write-Host "│   $displayName"
        }
        
        $index++
    }
    
    Write-Host "└────────────────────────────────────────────────────────────┘"
    Write-Host ""
    Write-Host "Use " -ForegroundColor Cyan -NoNewline
    Write-Host "↑↓" -ForegroundColor White -NoNewline
    Write-Host " arrow keys to navigate, " -ForegroundColor Cyan -NoNewline
    Write-Host "Enter" -ForegroundColor White -NoNewline
    Write-Host " to select, " -ForegroundColor Cyan -NoNewline
    Write-Host "Q" -ForegroundColor White -NoNewline
    Write-Host " to quit" -ForegroundColor Cyan
}

# Validate git repository
function Test-GitRepository {
    param([string]$TargetDir)
    
    Write-Info "Checking if $TargetDir is a Git repository..."
    
    $gitDir = Join-Path $TargetDir ".git"
    if (-not (Test-Path $gitDir)) {
        Write-Host ""
        Write-ErrorMsg "Selected directory is not a Git repository"
        Write-Info "Initialize with: cd $TargetDir; git init"
        Write-Host ""
        Read-Host "Press Enter to continue"
        return $false
    }
    
    Write-Success "Git repository confirmed"
    return $true
}

# Confirm installation
function Confirm-Installation {
    param([string]$TargetDir)
    
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗"
    Write-Host "║                    Installation Summary                    ║"
    Write-Host "╚════════════════════════════════════════════════════════════╝"
    Write-Host ""
    Write-Host "Target Directory: " -NoNewline
    Write-Host $TargetDir -ForegroundColor White
    Write-Host "RDD Version: " -NoNewline
    Write-Host "v$VERSION" -ForegroundColor White
    Write-Host ""
    
    # Check for existing installation
    $existingRdd = Join-Path $TargetDir ".rdd\\scripts\\rdd.py"
    if (Test-Path $existingRdd) {
        Write-Warning "Existing RDD installation detected - will be OVERWRITTEN"
        Write-Host ""
    }
    
    $response = Read-Host "Proceed with installation? [y/N]"
    
    if ($response -notmatch '^[Yy]$') {
        Write-Info "Installation cancelled by user"
        exit 0
    }
}

# Run Python installer
function Invoke-PythonInstaller {
    param(
        [string]$SourceDir,
        [string]$TargetDir
    )
    
    Write-Host ""
    Write-Info "Running Python installer..."
    Write-Host ""
    
    Set-Location $TargetDir
    
    # Run Python installer with input redirection
    $installerPath = Join-Path $SourceDir "install.py"
    $inputData = "`n`n"  # Two enters for default target directory
    $inputData | & python $installerPath
    
    $exitCode = $LASTEXITCODE
    
    if ($exitCode -eq 0) {
        Write-Host ""
        Write-Host "╔════════════════════════════════════════════════════════════╗"
        Write-Host "║              Installation Completed Successfully!          ║"
        Write-Host "╚════════════════════════════════════════════════════════════╝"
        Write-Host ""
        Write-Success "RDD Framework v$VERSION installed to: $TargetDir"
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor White
        Write-Host "  1. Restart VS Code"
        Write-Host "  2. Create your first change:"
        Write-Host "     cd $TargetDir" -ForegroundColor Cyan
        Write-Host "     python .rdd\\scripts\\rdd.py change create enh my-feature" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Documentation: https://github.com/h111359/requirements-driven-development"
        Write-Host ""
    }
    else {
        Write-Host ""
        Write-ErrorMsg "Installation failed with exit code: $exitCode"
        exit $exitCode
    }
}

# Main execution
function Main {
    # Get source directory (where this script is located)
    $sourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    
    # Prerequisites check
    Test-Prerequisites
    
    # Navigate to select installation directory
    Write-Info "Starting folder navigation..."
    Write-Info "Navigate with arrow keys, press Enter to select"
    Write-Host ""
    Start-Sleep -Seconds 2
    
    $targetDir = Start-FolderNavigation -StartDir (Get-Location).Path
    
    # Validate git repository
    while (-not (Test-GitRepository -TargetDir $targetDir)) {
        Write-Host ""
        $response = Read-Host "Try selecting a different directory? [Y/n]"
        
        if ($response -match '^[Nn]$') {
            Write-Info "Installation cancelled by user"
            exit 0
        }
        
        $targetDir = Start-FolderNavigation -StartDir $targetDir
    }
    
    # Confirm installation
    Confirm-Installation -TargetDir $targetDir
    
    # Run Python installer
    Invoke-PythonInstaller -SourceDir $sourceDir -TargetDir $targetDir
}

# Run main function
Main
'''
    
    installer_path = build_dir / "install.ps1"
    installer_path.write_text(installer_content)
    
    print_success("Generated install.ps1")

def create_archive(build_dir: Path, build_root: Path, version: str) -> Path:
    """Create zip archive from build directory"""
    print_info("Creating zip archive...")
    
    archive_name = f"rdd-v{version}.zip"
    archive_path = build_root / archive_name
    
    # Remove existing archive
    if archive_path.exists():
        archive_path.unlink()
    
    # Create zip file
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in build_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(build_dir.parent)
                zipf.write(file_path, arcname)
    
    # Get file size
    size_mb = archive_path.stat().st_size / (1024 * 1024)
    
    print_success(f"Created archive: {archive_path} ({size_mb:.2f} MB)")
    return archive_path

def generate_checksum(archive_path: Path):
    """Generate SHA256 checksum file"""
    print_info("Generating SHA256 checksum...")
    
    # Calculate checksum
    sha256 = hashlib.sha256()
    with open(archive_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    
    checksum = sha256.hexdigest()
    
    # Write checksum file
    checksum_path = archive_path.parent / f"{archive_path.name}.sha256"
    checksum_path.write_text(f"{checksum}  {archive_path.name}\n")
    
    print_success(f"Generated checksum: {checksum_path}")
    print_info(f"SHA256: {checksum}")

def cleanup_staging(build_dir: Path):
    """Remove staging directory"""
    print_info("Cleaning up staging directory...")
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print_success("Staging directory removed")

def main():
    """Main build process"""
    print()
    print("=" * 60)
    print("  RDD Framework Build Script")
    print("=" * 60)
    print()
    
    # Get repository root
    script_dir = Path(__file__).parent.absolute()
    repo_root = script_dir.parent
    
    print_info(f"Repository root: {repo_root}")
    
    # Build process
    try:
        # Step 1: Extract version
        print_step(1, 8, "Extracting version")
        rdd_py = repo_root / ".rdd" / "scripts" / "rdd.py"
        version = extract_version(rdd_py)
        print()
        
        # Step 2: Create build directory
        print_step(2, 8, "Creating build directory")
        build_root = repo_root / "build"
        build_root.mkdir(exist_ok=True)
        build_dir = create_build_dir(version, build_root)
        print()
        
        # Step 3: Copy files
        print_step(3, 8, "Copying files")
        copy_prompts(repo_root, build_dir)
        copy_scripts(repo_root, build_dir)
        copy_templates(repo_root, build_dir)
        copy_license(repo_root, build_dir)
        copy_vscode_settings(repo_root, build_dir)
        print()
        
        # Step 4: Generate README
        print_step(4, 10, "Generating README.md")
        generate_readme(build_dir, version)
        print()
        
        # Step 5: Generate Python installer
        print_step(5, 10, "Generating install.py")
        generate_installer(build_dir, version)
        print()
        
        # Step 6: Generate Bash installer
        print_step(6, 10, "Generating install.sh")
        generate_bash_installer(build_dir, version)
        print()
        
        # Step 7: Generate PowerShell installer
        print_step(7, 10, "Generating install.ps1")
        generate_powershell_installer(build_dir, version)
        print()
        
        # Step 8: Create archive
        print_step(8, 10, "Creating archive")
        archive_path = create_archive(build_dir, build_root, version)
        print()
        
        # Step 9: Generate checksum
        print_step(9, 10, "Generating checksum")
        generate_checksum(archive_path)
        print()
        
        # Step 10: Cleanup
        print_step(10, 10, "Cleaning up")
        cleanup_staging(build_dir)
        print()
        
        # Success summary
        print("=" * 60)
        print_success(f"Build completed successfully!")
        print("=" * 60)
        print()
        print(f"Version:     {version}")
        print(f"Archive:     {archive_path}")
        print(f"Checksum:    {archive_path}.sha256")
        print()
        print("Contents:")
        print("  - README.md (Windows & Linux instructions)")
        print("  - install.py (Python installer)")
        print("  - install.sh (Interactive Bash installer)")
        print("  - install.ps1 (Interactive PowerShell installer)")
        print()
        print("Next steps:")
        print("  1. Test the interactive installers:")
        print()
        print("     Linux/macOS:")
        print(f"       unzip {archive_path} -d /tmp/rdd-test")
        print(f"       cd /tmp/rdd-test/rdd-v{version}")
        print(f"       chmod +x install.sh")
        print(f"       ./install.sh")
        print()
        print("     Windows:")
        print(f"       Expand-Archive {archive_path} -DestinationPath C:\\Temp\\rdd-test")
        print(f"       cd C:\\Temp\\rdd-test\\rdd-v{version}")
        print(f"       .\\install.ps1")
        print()
        print("  2. Create GitHub release:")
        print(f"     - Tag: v{version}")
        print(f"     - Attach: {archive_path}")
        print(f"     - Attach: {archive_path}.sha256")
        print()
        
    except KeyboardInterrupt:
        print()
        print_warning("Build cancelled by user")
        sys.exit(130)
    except Exception as e:
        print()
        exit_with_error(f"Build failed: {e}")

if __name__ == "__main__":
    main()
