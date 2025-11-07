#!/usr/bin/env python3
"""
setup-test-env.py
Setup script for RDD test environment
Creates or updates virtual environment and installs test dependencies
"""

import sys
import os
import subprocess
from pathlib import Path

# Ensure UTF-8 encoding on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def print_banner():
    """Print script banner"""
    print()
    print("=" * 60)
    print("  RDD Test Environment Setup")
    print("=" * 60)
    print()

def print_success(msg: str):
    """Print success message"""
    print(f"✓ {msg}")

def print_info(msg: str):
    """Print info message"""
    print(f"ℹ {msg}")

def print_error(msg: str):
    """Print error message"""
    print(f"✗ {msg}", file=sys.stderr)

def run_command(cmd: list, cwd=None, capture_output=True):
    """Run a command and return success status"""
    try:
        if capture_output:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return True, result.stdout
        else:
            subprocess.run(cmd, cwd=cwd, check=True)
            return True, ""
    except subprocess.CalledProcessError as e:
        return False, e.stderr if capture_output else str(e)

def check_python_version():
    """Check Python version is 3.7+"""
    if sys.version_info < (3, 7):
        print_error(f"Python 3.7+ required. Current: {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected")
    return True

def create_or_update_venv(venv_path: Path):
    """Create virtual environment or verify existing one"""
    if venv_path.exists():
        print_info(f"Virtual environment already exists at {venv_path}")
        print_info("Will update packages without recreating...")
        return True
    
    print_info(f"Creating virtual environment at {venv_path}...")
    success, output = run_command([sys.executable, "-m", "venv", str(venv_path)])
    
    if not success:
        print_error(f"Failed to create virtual environment:\n{output}")
        return False
    
    print_success("Virtual environment created")
    return True

def get_venv_python(venv_path: Path) -> Path:
    """Get path to Python executable in virtual environment"""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "python.exe"
    else:
        return venv_path / "bin" / "python"

def get_venv_pip(venv_path: Path) -> Path:
    """Get path to pip executable in virtual environment"""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "pip.exe"
    else:
        return venv_path / "bin" / "pip"

def upgrade_pip(venv_path: Path):
    """Upgrade pip in virtual environment"""
    print_info("Upgrading pip...")
    pip_exe = get_venv_pip(venv_path)
    
    success, output = run_command([str(pip_exe), "install", "--upgrade", "pip"])
    
    if not success:
        print_error(f"Failed to upgrade pip:\n{output}")
        return False
    
    print_success("pip upgraded")
    return True

def install_requirements(venv_path: Path, requirements_file: Path):
    """Install or update requirements in virtual environment"""
    if not requirements_file.exists():
        print_error(f"Requirements file not found: {requirements_file}")
        return False
    
    print_info("Installing/updating test dependencies...")
    pip_exe = get_venv_pip(venv_path)
    
    # Use --upgrade to update existing packages without disrupting others
    success, output = run_command([
        str(pip_exe), "install", "--upgrade", "-r", str(requirements_file)
    ])
    
    if not success:
        print_error(f"Failed to install dependencies:\n{output}")
        return False
    
    print_success("Test dependencies installed/updated")
    return True

def show_activation_instructions(venv_path: Path):
    """Display instructions for activating the virtual environment"""
    print()
    print("=" * 60)
    print("Setup completed successfully!")
    print("=" * 60)
    print()
    print("To activate the virtual environment:")
    
    if sys.platform == "win32":
        print(f"  {venv_path}\\Scripts\\activate          (Command Prompt)")
        print(f"  {venv_path}\\Scripts\\Activate.ps1      (PowerShell)")
    else:
        print(f"  source {venv_path}/bin/activate")
    
    print()
    print("To run tests:")
    print("  pytest tests/python/")
    print()
    print("To deactivate:")
    print("  deactivate")
    print()

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Get paths
    repo_root = Path(__file__).parent
    venv_path = repo_root / ".venv"
    requirements_file = repo_root / "tests" / "requirements.txt"
    
    print()
    print(f"Repository root: {repo_root}")
    print(f"Virtual environment: {venv_path}")
    print(f"Requirements file: {requirements_file}")
    print()
    
    # Create or verify virtual environment
    if not create_or_update_venv(venv_path):
        return 1
    
    # Upgrade pip
    if not upgrade_pip(venv_path):
        return 1
    
    # Install/update requirements
    if not install_requirements(venv_path, requirements_file):
        return 1
    
    # Show activation instructions
    show_activation_instructions(venv_path)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
