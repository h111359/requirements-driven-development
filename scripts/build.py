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

def read_script_template(script_path: Path, version: str) -> str:
    """Read a script template and substitute variables"""
    print_info(f"Reading script template: {script_path.name}")
    
    if not script_path.exists():
        exit_with_error(f"Script template not found: {script_path}")
    
    content = script_path.read_text()
    
    # Substitute version placeholder
    content = content.replace('{{VERSION}}', version)
    
    print_success(f"Loaded script template: {script_path.name}")
    return content

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
    (build_dir / ".rdd-docs").mkdir(parents=True, exist_ok=True)
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
    
    settings_src = repo_root / "templates" / "settings.json"
    settings_dst = build_dir / ".vscode" / "settings.json"
    
    if not settings_src.exists():
        exit_with_error(f"Settings template not found: {settings_src}")
    
    shutil.copy2(settings_src, settings_dst)
    print_success("Copied VS Code settings template")

def copy_rdd_docs_seeds(repo_root: Path, build_dir: Path):
    """Copy seed template files to .rdd-docs directory in build"""
    print_info("Copying seed templates to .rdd-docs...")
    
    templates_src = repo_root / "templates"
    rdd_docs_dst = build_dir / ".rdd-docs"
    
    # List of seed templates that should be copied to .rdd-docs during installation
    seed_templates = [
        "config.json",
        "data-model.md",
        "requirements.md",
        "tech-spec.md"
    ]
    
    if not templates_src.exists():
        exit_with_error(f"Templates directory not found: {templates_src}")
    
    copied = 0
    for template_name in seed_templates:
        template_path = templates_src / template_name
        if not template_path.exists():
            exit_with_error(f"Seed template not found: {template_path}")
        
        shutil.copy2(template_path, rdd_docs_dst / template_name)
        copied += 1
    
    print_success(f"Copied {copied} seed template(s) to .rdd-docs/")

def generate_readme(build_dir: Path, version: str, repo_root: Path):
    """Generate README.md from template with version substitution"""
    print_info("Generating README.md from template...")
    
    # Read template
    template_path = repo_root / "templates" / "README.md"
    
    if not template_path.exists():
        exit_with_error(f"README template not found: {template_path}")
    
    readme_content = template_path.read_text()
    
    # Substitute version placeholder
    readme_content = readme_content.replace('{{VERSION}}', version)
    
    # Write to build directory
    readme_path = build_dir / "README.md"
    readme_path.write_text(readme_content)
    
    print_success("Generated README.md from template")

def generate_installer(build_dir: Path, version: str, repo_root: Path):
    """Generate install.py script from template"""
    print_info("Generating install.py...")
    
    # Read template and substitute version
    template_path = repo_root / "scripts" / "install.py"
    installer_content = read_script_template(template_path, version)
    
    # Write to build directory
    installer_path = build_dir / "install.py"
    installer_path.write_text(installer_content)
    
    # Make executable on Unix systems
    if os.name != 'nt':
        installer_path.chmod(0o755)
    
    print_success("Generated install.py")

def generate_bash_installer(build_dir: Path, version: str, repo_root: Path):
    """Generate install.sh script from template"""
    print_info("Generating install.sh...")
    
    # Read template and substitute version
    template_path = repo_root / "scripts" / "install.sh"
    installer_content = read_script_template(template_path, version)
    
    # Write to build directory
    installer_path = build_dir / "install.sh"
    installer_path.write_text(installer_content)
    
    # Make executable on Unix systems
    if os.name != 'nt':
        installer_path.chmod(0o755)
    
    print_success("Generated install.sh")

def generate_powershell_installer(build_dir: Path, version: str, repo_root: Path):
    """Generate install.ps1 script from template"""
    print_info("Generating install.ps1...")
    
    # Read template and substitute version
    template_path = repo_root / "scripts" / "install.ps1"
    installer_content = read_script_template(template_path, version)
    
    # Write to build directory
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
        print_step(1, 11, "Extracting version")
        rdd_py = repo_root / ".rdd" / "scripts" / "rdd.py"
        version = extract_version(rdd_py)
        print()
        
        # Step 2: Create build directory
        print_step(2, 11, "Creating build directory")
        build_root = repo_root / "build"
        build_root.mkdir(exist_ok=True)
        build_dir = create_build_dir(version, build_root)
        print()
        
        # Step 3: Copy files
        print_step(3, 11, "Copying files")
        copy_prompts(repo_root, build_dir)
        copy_scripts(repo_root, build_dir)
        copy_templates(repo_root, build_dir)
        copy_license(repo_root, build_dir)
        copy_vscode_settings(repo_root, build_dir)
        copy_rdd_docs_seeds(repo_root, build_dir)
        print()
        
        # Step 4: Generate README
        print_step(4, 11, "Generating README.md")
        generate_readme(build_dir, version, repo_root)
        print()
        
        # Step 5: Generate Python installer
        print_step(5, 11, "Generating install.py")
        generate_installer(build_dir, version, repo_root)
        print()
        
        # Step 6: Generate Bash installer
        print_step(6, 11, "Generating install.sh")
        generate_bash_installer(build_dir, version, repo_root)
        print()
        
        # Step 7: Generate PowerShell installer
        print_step(7, 11, "Generating install.ps1")
        generate_powershell_installer(build_dir, version, repo_root)
        print()
        
        # Step 8: Create archive
        print_step(8, 11, "Creating archive")
        archive_path = create_archive(build_dir, build_root, version)
        print()
        
        # Step 9: Generate checksum
        print_step(9, 11, "Generating checksum")
        generate_checksum(archive_path)
        print()
        
        # Step 10: Cleanup
        print_step(10, 11, "Cleaning up")
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
