#!/usr/bin/env python3
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

# Try to import tkinter for GUI folder selection
try:
    import tkinter as tk
    from tkinter import filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

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

def print_banner():
    print()
    print("=" * 60)
    print(f"  RDD Framework Installer v{{VERSION}}")
    print("=" * 60)
    print()

def print_installation_description():
    """Print a description of what the installer will do"""
    print()
    print("This installer will:")
    print("  • Copy RDD framework files (.rdd/ directory)")
    print("  • Copy GitHub prompts (.github/prompts/)")
    print("  • Copy seed templates to .rdd-docs/")
    print("  • Merge VS Code settings")
    print("  • Update .gitignore")
    print("  • Verify installation")
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
            f"Found: {current.major}.{current.minor}.{current.micro}\n"
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
            "Git is not installed or not in PATH\n"
            "Install Git: https://git-scm.com/downloads"
        )
        return False

def check_git_repo(target_dir: Path) -> bool:
    """Check if target directory is a Git repository"""
    print_info(f"Checking if {target_dir} is a Git repository...")
    
    git_dir = target_dir / ".git"
    if not git_dir.exists():
        exit_with_error(
            f"{target_dir} is not a Git repository\n"
            f"Initialize with: cd {target_dir} && git init"
        )
        return False
    
    print_success("Git repository confirmed")
    return True

def detect_existing_installation(target_dir: Path) -> bool:
    """Check if RDD is already installed"""
    print_info("Checking for existing RDD installation...")
    
    rdd_dir = target_dir / ".rdd"
    rdd_script = target_dir / ".rdd" / "scripts" / "rdd.py"
    prompts_dir = target_dir / ".github" / "prompts"
    rdd_docs_dir = target_dir / ".rdd-docs"
    
    has_scripts = rdd_script.exists()
    has_prompts = prompts_dir.exists() and any(prompts_dir.glob("rdd.*.prompt.md"))
    has_rdd_dir = rdd_dir.exists()
    has_docs = rdd_docs_dir.exists()
    
    if has_scripts or has_prompts or has_rdd_dir:
        print_warning("Existing RDD installation detected:")
        if has_rdd_dir:
            print(f"  • .rdd/ directory exists")
        if has_prompts:
            print(f"  • RDD prompt files found in .github/prompts/")
        if has_docs:
            print(f"  • .rdd-docs/ directory exists (contains your project data)")
        print()
        print_warning("Installation will OVERWRITE framework files but preserve .rdd-docs/ content")
        return True
    
    print_info("No existing installation found")
    return False

def get_target_directory_gui() -> Optional[Path]:
    """Use Tkinter GUI to select target directory"""
    if not TKINTER_AVAILABLE:
        return None
    
    try:
        # Create a hidden root window
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        # Show folder selection dialog
        print_info("Opening folder selection dialog...")
        folder_path = filedialog.askdirectory(
            title="Select Git Repository for RDD Installation",
            initialdir=Path.cwd()
        )
        
        root.destroy()
        
        if folder_path:
            return Path(folder_path).resolve()
        return None
    except Exception as e:
        print_warning(f"GUI folder picker failed: {e}")
        return None

def get_target_directory() -> Path:
    """Prompt user for target directory with GUI option"""
    default = Path.cwd()
    
    print()
    
    # Try GUI first if available
    if TKINTER_AVAILABLE:
        print("Choose installation method:")
        print("  1. Browse for folder (GUI)")
        print("  2. Enter path manually")
        print()
        choice = input("Enter choice (1 or 2, default: 1): ").strip()
        
        if choice == "" or choice == "1":
            gui_path = get_target_directory_gui()
            if gui_path:
                print_success(f"Selected: {gui_path}")
                return validate_target_directory(gui_path)
            else:
                print_info("No folder selected, falling back to manual entry")
    
    # Fallback to text input
    print(f"Enter target directory path (default: {default}):")
    response = input("> ").strip()
    
    if not response:
        target = default
    else:
        target = Path(response).expanduser().resolve()
    
    return validate_target_directory(target)

def validate_target_directory(target: Path) -> Path:
    """Validate that target is a valid directory"""
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
    
    # Remove all existing rdd.* prompts to ensure clean replacement
    removed = 0
    if dst_prompts.exists():
        for old_prompt in dst_prompts.glob("rdd.*.prompt.md"):
            old_prompt.unlink()
            removed += 1
    
    if removed > 0:
        print_info(f"Removed {removed} existing RDD prompt file(s)")
    
    # Copy new prompts
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
    
    # Copy user-guide.md to .rdd directory
    src_user_guide = source_dir / "user-guide.md"
    if src_user_guide.exists():
        dst_user_guide = dst_rdd / "user-guide.md"
        shutil.copy2(src_user_guide, dst_user_guide)
        print_info("  Copied user-guide.md to .rdd/")
    else:
        print_warning("  user-guide.md not found in root directory")
    
    # Copy RDD-Framework-User-Guide.pdf to .rdd directory
    src_pdf = source_dir / "RDD-Framework-User-Guide.pdf"
    if src_pdf.exists():
        dst_pdf = dst_rdd / "RDD-Framework-User-Guide.pdf"
        shutil.copy2(src_pdf, dst_pdf)
        print_info("  Copied RDD-Framework-User-Guide.pdf to .rdd/")
    else:
        print_warning("  RDD-Framework-User-Guide.pdf not found in root directory")
    
    print_success("Installed RDD framework")

def install_launcher_script(source_dir: Path, target_dir: Path):
    """Copy appropriate launcher script (rdd.bat or rdd.sh) to target root"""
    print_info("Installing RDD launcher script...")
    
    # Detect OS and select appropriate launcher
    if os.name == 'nt':  # Windows
        launcher_name = "rdd.bat"
    else:  # Linux, macOS, etc.
        launcher_name = "rdd.sh"
    
    src_launcher = source_dir / launcher_name
    dst_launcher = target_dir / launcher_name
    
    if not src_launcher.exists():
        print_warning(f"Launcher script not found: {src_launcher}")
        return
    
    # Copy launcher to target root
    shutil.copy2(src_launcher, dst_launcher)
    
    # Set executable permissions (Unix only)
    if os.name != 'nt':
        dst_launcher.chmod(0o755)
        print_success(f"Installed {launcher_name} (executable)")
    else:
        print_success(f"Installed {launcher_name}")
    
    # Provide usage hint
    if os.name == 'nt':
        print_info(f"  Usage: Double-click {launcher_name} or run from terminal")
    else:
        print_info(f"  Usage: ./{launcher_name} or double-click from file manager")

def ask_local_only_mode() -> bool:
    """Ask user if they want to use local-only mode (no GitHub remote)"""
    print()
    print("=" * 60)
    print("  Repository Mode Configuration")
    print("=" * 60)
    print()
    print("Will you be using GitHub remote for this repository?")
    print()
    print("  • Yes (default): Normal mode with GitHub push/pull/fetch")
    print("  • No: Local-only mode (no remote operations)")
    print()
    print("Use GitHub remote? (Y/n):")
    response = input("> ").strip().lower()
    
    # Default to Yes (not local-only)
    # Local-only is true only if user explicitly says no
    return response in ['n', 'no']


def copy_rdd_docs_seeds(source_dir: Path, target_dir: Path, local_only: bool = False):
    """Copy seed template files from .rdd-docs in source to target"""
    print_info("Installing .rdd-docs seed templates...")
    
    src_rdd_docs = source_dir / ".rdd-docs" 
    dst_rdd_docs = target_dir / ".rdd-docs"
    
    # Create .rdd-docs directory if it doesn't exist
    dst_rdd_docs.mkdir(parents=True, exist_ok=True)
    
    # List of seed files to copy
    seed_files = ["config.json", "requirements.md", "tech-spec.md"]
    
    copied = 0
    for seed_file in seed_files:
        src_file = src_rdd_docs / seed_file
        dst_file = dst_rdd_docs / seed_file
        
        # Skip if destination already exists (don't overwrite user's work)
        if dst_file.exists():
            print_info(f"  Skipping {seed_file} (already exists)")
            continue
        
        if src_file.exists():
            shutil.copy2(src_file, dst_file)
            copied += 1
            
            # If this is config.json, update it with localOnly setting
            if seed_file == "config.json":
                try:
                    with open(dst_file, 'r') as f:
                        config_data = json.load(f)
                    
                    config_data['localOnly'] = local_only
                    
                    with open(dst_file, 'w') as f:
                        json.dump(config_data, f, indent=2)
                    
                    mode_str = "local-only" if local_only else "GitHub remote"
                    print_info(f"  Configured for {mode_str} mode")
                except Exception as e:
                    print_warning(f"  Could not update config.json: {e}")
    
    print_success(f"Installed {copied} seed template(s)")


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
            lines = [line.split('//')[0].rstrip() for line in content.split('\n')]
            clean_content = '\n'.join(lines)
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
    gitignore_path.write_text('\n'.join(lines) + '\n')
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
    
    # Show what the installer will do
    print_installation_description()
    
    # Get target directory
    target_dir = get_target_directory()
    check_git_repo(target_dir)
    
    # Check for existing installation
    is_upgrade = detect_existing_installation(target_dir)
    
    # Get confirmation
    if not confirm_installation(target_dir, is_upgrade):
        print_info("Installation cancelled by user")
        sys.exit(0)
    
    # Ask about local-only mode
    local_only = ask_local_only_mode()
    
    print()
    print("Installing...")
    print()
    
    try:
        # Install files
        copy_prompts(source_dir, target_dir)
        copy_rdd_framework(source_dir, target_dir)
        install_launcher_script(source_dir, target_dir)
        copy_rdd_docs_seeds(source_dir, target_dir, local_only)
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
        print("  2. Create your first work itteration:")
        print(f"     cd {target_dir}")
        print("     python .rdd/scripts/rdd.py ")
        print()
        print("Documentation: https://github.com/h111359/requirements-driven-development")
        print()
        
    except Exception as e:
        exit_with_error(f"Installation failed: {e}")

if __name__ == "__main__":
    main()
