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

    # REMOVED: extract_version function. Version is now read from .rdd-docs/config.json

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
    
    if not settings_dst.exists():
        shutil.copy2(settings_src, settings_dst)
        print_success("Copied VS Code settings template")
    else:
        print_info(f"VS Code settings already exists at {settings_dst}, skipping copy.")
        

def copy_rdd_docs_seeds(repo_root: Path, build_dir: Path):
    """Copy seed template files to .rdd-docs directory in build"""
    print_info("Copying seed templates to .rdd-docs...")
    
    templates_src = repo_root / "templates"
    rdd_docs_dst = build_dir / ".rdd-docs"
    
    # List of seed templates that should be copied to .rdd-docs during installation
    seed_templates = [
        "config.json",
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

def copy_user_guide(build_dir: Path, repo_root: Path):
    """Copy user-guide.md from templates to build directory root"""
    print_info("Copying user-guide.md to build directory root...")
    user_guide_src = repo_root / "templates" / "user-guide.md"
    user_guide_dst = build_dir / "user-guide.md"
    if not user_guide_src.exists():
        print_warning(f"user-guide.md not found at {user_guide_src}, skipping copy.")
        return
    shutil.copy2(user_guide_src, user_guide_dst)
    print_success("Copied user-guide.md to build directory root")

def copy_user_guide_pdf(build_dir: Path, repo_root: Path):
    """Copy RDD-Framework-User-Guide.pdf from templates to build directory root"""
    print_info("Copying RDD-Framework-User-Guide.pdf to build directory root...")
    pdf_src = repo_root / "templates" / "RDD-Framework-User-Guide.pdf"
    pdf_dst = build_dir / "RDD-Framework-User-Guide.pdf"
    if not pdf_src.exists():
        print_warning(f"RDD-Framework-User-Guide.pdf not found at {pdf_src}, skipping copy.")
        return
    shutil.copy2(pdf_src, pdf_dst)
    print_success("Copied RDD-Framework-User-Guide.pdf to build directory root")

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
    """Generate install.sh launcher script from template"""
    print_info("Generating install.sh launcher...")
    
    # Read template and substitute version
    template_path = repo_root / "templates" / "install.sh"
    installer_content = read_script_template(template_path, version)
    
    # Write to build directory
    installer_path = build_dir / "install.sh"
    installer_path.write_text(installer_content)
    
    # Make executable on Unix systems
    if os.name != 'nt':
        installer_path.chmod(0o755)
    
    print_success("Generated install.sh launcher")

def generate_batch_installer(build_dir: Path, version: str, repo_root: Path):
    """Generate install.bat launcher script from template"""
    print_info("Generating install.bat launcher...")
    
    # Read template and substitute version
    template_path = repo_root / "templates" / "install.bat"
    installer_content = read_script_template(template_path, version)
    
    # Write to build directory
    installer_path = build_dir / "install.bat"
    installer_path.write_text(installer_content)
    
    print_success("Generated install.bat launcher")

def copy_rdd_launcher_scripts(build_dir: Path, repo_root: Path):
    """Copy RDD launcher scripts (rdd.bat and rdd.sh) to build directory"""
    print_info("Copying RDD launcher scripts...")
    
    scripts_src = repo_root / "scripts"
    
    launchers = ["rdd.bat", "rdd.sh"]
    copied = 0
    
    for launcher_name in launchers:
        launcher_src = scripts_src / launcher_name
        launcher_dst = build_dir / launcher_name
        
        if not launcher_src.exists():
            print_warning(f"Launcher script not found: {launcher_src}")
            continue
        
        shutil.copy2(launcher_src, launcher_dst)
        
        # Make rdd.sh executable on Unix systems
        if launcher_name == "rdd.sh" and os.name != 'nt':
            launcher_dst.chmod(0o755)
        
        copied += 1
    
    if copied == 0:
        print_warning("No launcher scripts copied")
    else:
        print_success(f"Copied {copied} RDD launcher script(s)")

def generate_powershell_installer(build_dir: Path, version: str, repo_root: Path):
    """Generate install.ps1 script from template (DEPRECATED - replaced by install.bat)"""
    print_info("Generating install.ps1...")
    
    # Read template and substitute version
    template_path = repo_root / "templates" / "install.ps1"
    if not template_path.exists():
        print_warning("install.ps1 template not found, skipping")
        return
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

def increment_patch_version(version: str) -> str:
    """Increment the patch version (last digit) of a semantic version string"""
    parts = version.split('.')
    if len(parts) != 3:
        exit_with_error(f"Invalid version format: {version}")
    
    try:
        major = int(parts[0])
        minor = int(parts[1])
        patch = int(parts[2])
    except ValueError:
        exit_with_error(f"Invalid version format: {version}")
    
    new_version = f"{major}.{minor}.{patch + 1}"
    return new_version

def update_config_version(config_path: Path, new_version: str):
    """Update version in config.json and set lastModified timestamp"""
    print_info(f"Updating config.json with version {new_version}")
    
    if not config_path.exists():
        exit_with_error(f"Config file not found: {config_path}")
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    config["version"] = new_version
    
    # Update lastModified with current timestamp in ISO format
    from datetime import datetime, timezone
    config["lastModified"] = datetime.now(timezone.utc).isoformat()
    
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print_success(f"Updated config.json: version → {new_version}")

def prompt_version_selection(current_version: str) -> str:
    """
    Prompt user to choose version: keep current or increment patch.
    Returns the selected version string.
    """
    print()
    print("=" * 60)
    print("  Version Selection")
    print("=" * 60)
    print()
    print(f"Current version: {Colors.BLUE}{current_version}{Colors.NC}")
    print()
    
    # Calculate what the incremented version would be
    incremented = increment_patch_version(current_version)
    print(f"Options:")
    print(f"  1. Keep current version ({current_version})")
    print(f"  2. Increment patch version ({incremented})")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1 or 2): ").strip()
            
            if choice == '1':
                print_info(f"Using current version: {current_version}")
                return current_version
            elif choice == '2':
                print_info(f"Incrementing to version: {incremented}")
                return incremented
            else:
                print_warning("Invalid choice. Please enter 1 or 2.")
        except (KeyboardInterrupt, EOFError):
            print()
            print_warning("Version selection cancelled")
            sys.exit(130)

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
        # Step 1: Extract version from .rdd-docs/config.json and prompt for version selection
        print_step(1, 9, "Version selection")
        config_path = repo_root / ".rdd-docs" / "config.json"
        if not config_path.exists():
            exit_with_error(f"Config file not found: {config_path}")
        with open(config_path, "r") as f:
            config = json.load(f)
        current_version = config.get("version")
        if not current_version or not re.match(r'^\d+\.\d+\.\d+$', current_version):
            exit_with_error(f"Invalid or missing version in config.json: {current_version}")
        print_success(f"Found current version: {current_version}")

        # Prompt user for version selection
        selected_version = prompt_version_selection(current_version)

        # Update config.json if version changed
        if selected_version != current_version:
            update_config_version(config_path, selected_version)

        version = selected_version
        print()

        # Step 2: Create build directory
        print_step(2, 9, "Creating build directory")
        build_root = repo_root / "build"
        build_root.mkdir(exist_ok=True)
        build_dir = create_build_dir(version, build_root)
        print()

        # Step 3: Copy files
        print_step(3, 9, "Copying files")
        copy_prompts(repo_root, build_dir)
        copy_scripts(repo_root, build_dir)
        copy_templates(repo_root, build_dir)
        copy_license(repo_root, build_dir)
        copy_vscode_settings(repo_root, build_dir)
        copy_rdd_docs_seeds(repo_root, build_dir)
        print()

        # Step 4: Generate README and copy user-guide
        print_step(4, 9, "Generating README.md and copying user-guide.md")
        generate_readme(build_dir, version, repo_root)
        copy_user_guide(build_dir, repo_root)
        copy_user_guide_pdf(build_dir, repo_root)
        print()

        # Step 5: Generate installers
        print_step(5, 9, "Generating installers")
        generate_installer(build_dir, version, repo_root)
        generate_bash_installer(build_dir, version, repo_root)
        generate_batch_installer(build_dir, version, repo_root)
        copy_rdd_launcher_scripts(build_dir, repo_root)
        print()

        # Step 6: Create archive
        print_step(6, 9, "Creating archive")
        archive_path = create_archive(build_dir, build_root, version)
        print()

        # Step 7: Generate checksum
        print_step(7, 9, "Generating checksum")
        generate_checksum(archive_path)
        print()

        # Step 8: Cleanup
        print_step(8, 9, "Cleaning up")
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
        print("  - README.md (Installation instructions)")
        print("  - user-guide.md (Comprehensive user guide)")
        print("  - install.py (Python installer)")
        print("  - install.sh (Linux/macOS installer launcher)")
        print("  - install.bat (Windows installer launcher)")
        print("  - rdd.sh (Linux/macOS RDD launcher)")
        print("  - rdd.bat (Windows RDD launcher)")
        print()
        print("Next steps:")
        print("  1. Test installer:")
        print(f"     Linux/macOS: unzip {archive_path} -d /tmp/rdd-test && cd /tmp/rdd-test/rdd-v{version} && ./install.sh")
        print(f"     Windows: Extract archive, navigate to folder, double-click install.bat")
        print("  2. Or test direct Python installer:")
        print(f"     python install.py")
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
