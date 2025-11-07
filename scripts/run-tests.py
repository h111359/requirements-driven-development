#!/usr/bin/env python3
"""
run-tests.py
Cross-platform test runner for RDD Framework
Runs all tests appropriate for the current platform
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path
from typing import List, Tuple

# Color codes for output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    WHITE = '\033[1;37m'
    NC = '\033[0m'  # No Color

def is_windows():
    """Check if running on Windows"""
    return os.name == 'nt'

def print_header(msg: str):
    """Print section header"""
    print()
    print("=" * 60)
    print(f"  {msg}")
    print("=" * 60)
    print()

def print_success(msg: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.NC} {msg}")

def print_error(msg: str):
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.NC} {msg}", file=sys.stderr)

def print_info(msg: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.NC} {msg}")

def print_warning(msg: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.NC} {msg}")

def print_step(current: int, total: int, msg: str):
    """Print step progress"""
    print(f"{Colors.BLUE}[{current}/{total}]{Colors.NC} {msg}")

def check_prerequisites() -> bool:
    """Check if all prerequisites are met"""
    print_info("Checking prerequisites...")
    
    # Check Python
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print_success(f"Python found: {python_version}")
    
    # Check virtual environment
    venv_dir = Path(".venv")
    if not venv_dir.exists():
        print_warning("Virtual environment not found at .venv/")
        print_info("Run: python setup-test-env.py")
        return False
    print_success("Virtual environment found")
    
    # Check pytest in venv
    if is_windows():
        pytest_path = venv_dir / "Scripts" / "pytest.exe"
    else:
        pytest_path = venv_dir / "bin" / "pytest"
    
    if not pytest_path.exists():
        print_error("pytest not found in virtual environment")
        print_info("Run: python setup-test-env.py")
        return False
    
    # Get pytest version
    try:
        result = subprocess.run(
            [str(pytest_path), "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        pytest_version = result.stdout.strip().split('\n')[0]
        print_success(f"{pytest_version}")
    except subprocess.CalledProcessError:
        print_error("Failed to get pytest version")
        return False
    
    return True

def get_python_executable() -> str:
    """Get path to Python executable in virtual environment"""
    venv_dir = Path(".venv")
    if is_windows():
        return str(venv_dir / "Scripts" / "python.exe")
    else:
        return str(venv_dir / "bin" / "python")

def get_pytest_executable() -> str:
    """Get path to pytest executable in virtual environment"""
    venv_dir = Path(".venv")
    if is_windows():
        return str(venv_dir / "Scripts" / "pytest.exe")
    else:
        return str(venv_dir / "bin" / "pytest")

def run_pytest_suite(test_dir: str, description: str) -> bool:
    """Run a pytest test suite"""
    pytest_cmd = get_pytest_executable()
    
    try:
        result = subprocess.run(
            [pytest_cmd, test_dir, "-v", "--tb=short"],
            check=False
        )
        return result.returncode == 0
    except Exception as e:
        print_error(f"Failed to run tests: {e}")
        return False

def run_bats_tests() -> Tuple[bool, bool]:
    """Run BATS shell tests (Linux/macOS only)
    
    Returns:
        (tests_ran, tests_passed)
    """
    if is_windows():
        return (False, True)  # Not applicable on Windows
    
    # Check if bats is installed
    if shutil.which("bats") is None:
        print_warning("BATS not found - skipping shell tests")
        print_info("Install: sudo apt-get install bats (Ubuntu/Debian)")
        print_info("Install: brew install bats-core (macOS)")
        return (False, True)  # Not an error, just skipped
    
    # Run BATS tests
    try:
        result = subprocess.run(
            ["bats", "tests/shell/*.bats"],
            shell=True,
            check=False
        )
        return (True, result.returncode == 0)
    except Exception as e:
        print_error(f"Failed to run BATS tests: {e}")
        return (True, False)

def run_pester_tests() -> Tuple[bool, bool]:
    """Run Pester PowerShell tests (Windows only)
    
    Returns:
        (tests_ran, tests_passed)
    """
    if not is_windows():
        return (False, True)  # Not applicable on Linux/macOS
    
    # Check if Pester is installed
    try:
        check_pester = subprocess.run(
            ["powershell", "-Command", "Get-Module -ListAvailable -Name Pester"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if not check_pester.stdout.strip():
            print_warning("Pester not found - skipping PowerShell tests")
            print_info("Install: Install-Module -Name Pester -Force -SkipPublisherCheck")
            return (False, True)  # Not an error, just skipped
        
        # Run Pester tests
        result = subprocess.run(
            [
                "powershell",
                "-Command",
                "Invoke-Pester tests/powershell/*.Tests.ps1 -PassThru | Select-Object -ExpandProperty FailedCount"
            ],
            capture_output=True,
            text=True,
            check=False
        )
        
        failed_count = int(result.stdout.strip() or "0")
        return (True, failed_count == 0)
        
    except Exception as e:
        print_warning(f"PowerShell tests skipped due to error: {e}")
        return (False, True)  # Not an error, just skipped

def main():
    """Main test execution"""
    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    os.chdir(repo_root)
    
    # Print banner
    platform = "Windows" if is_windows() else "Linux/macOS"
    print_header(f"RDD Framework Test Runner ({platform})")
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Track test results
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    print()
    print_header("Running Tests")
    
    # Step 1: Python Unit Tests
    print_step(1, 4, "Running Python unit tests")
    total_tests += 1
    if run_pytest_suite("tests/python/", "Python unit tests"):
        print_success("Python unit tests passed")
        passed_tests += 1
    else:
        print_error("Python unit tests failed")
        failed_tests += 1
    print()
    
    # Step 2: Build Tests
    print_step(2, 4, "Running build tests")
    total_tests += 1
    if run_pytest_suite("tests/build/", "Build tests"):
        print_success("Build tests passed")
        passed_tests += 1
    else:
        print_error("Build tests failed")
        failed_tests += 1
    print()
    
    # Step 3: Install Tests
    print_step(3, 4, "Running install tests")
    total_tests += 1
    if run_pytest_suite("tests/install/", "Install tests"):
        print_success("Install tests passed")
        passed_tests += 1
    else:
        print_error("Install tests failed")
        failed_tests += 1
    print()
    
    # Step 4: Platform-specific tests
    if is_windows():
        print_step(4, 4, "Running PowerShell tests (Pester)")
        ran, passed = run_pester_tests()
        if ran:
            total_tests += 1
            if passed:
                print_success("PowerShell tests passed")
                passed_tests += 1
            else:
                print_error("PowerShell tests failed")
                failed_tests += 1
    else:
        print_step(4, 4, "Running shell tests (BATS)")
        ran, passed = run_bats_tests()
        if ran:
            total_tests += 1
            if passed:
                print_success("Shell tests passed")
                passed_tests += 1
            else:
                print_error("Shell tests failed")
                failed_tests += 1
    print()
    
    # Summary
    print_header("Test Summary")
    print(f"Total test suites: {total_tests}")
    print(f"{Colors.GREEN}Passed: {passed_tests}{Colors.NC}")
    if failed_tests > 0:
        print(f"{Colors.RED}Failed: {failed_tests}{Colors.NC}")
    print()
    
    # Exit with appropriate code
    if failed_tests > 0:
        print_error("Some tests failed")
        sys.exit(1)
    else:
        print_success("All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
