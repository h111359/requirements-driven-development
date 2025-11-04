#!/usr/bin/env python3
"""
Test script to validate Python RDD implementation
Tests core functionality and compares with expected behavior
"""

import sys
import os
from pathlib import Path

# Add script dir to path
SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SCRIPT_DIR))

from rdd_utils import *

def test_color_output():
    """Test colored output functions"""
    print("\n=== Testing Color Output ===")
    print_success("Success message test")
    print_error("Error message test")
    print_warning("Warning message test")
    print_info("Info message test")
    print_step("Step message test")
    print_banner("Test Banner", "Subtitle")
    return True

def test_validation():
    """Test validation functions"""
    print("\n=== Testing Validation Functions ===")
    
    # Test valid names
    assert validate_name("my-test") == True
    assert validate_name("bug-fix") == True
    assert validate_name("user-authentication") == True
    print_success("Valid names passed")
    
    # Test invalid names (these should fail silently in validation)
    assert validate_name("Invalid Name") == False
    assert validate_name("") == False
    print_success("Invalid names rejected correctly")
    
    # Test branch name validation
    assert validate_branch_name("enh/20231101-1234-my-test") == True
    assert validate_branch_name("fix/20231101-1234-bug-fix") == True
    assert validate_branch_name("invalid") == False
    print_success("Branch name validation passed")
    
    return True

def test_normalization():
    """Test string normalization"""
    print("\n=== Testing String Normalization ===")
    
    assert normalize_to_kebab_case("Add User Auth") == "add-user-auth"
    assert normalize_to_kebab_case("fix_login_bug") == "fix-login-bug"
    assert normalize_to_kebab_case("UPDATE-README") == "update-readme"
    assert normalize_to_kebab_case("  spaces  around  ") == "spaces-around"
    print_success("Normalization tests passed")
    
    return True

def test_timestamps():
    """Test timestamp functions"""
    print("\n=== Testing Timestamp Functions ===")
    
    ts = get_timestamp()
    print(f"ISO timestamp: {ts}")
    assert "T" in ts and "Z" in ts
    
    ts_file = get_timestamp_filename()
    print(f"Filename timestamp: {ts_file}")
    assert "-" in ts_file and len(ts_file) == 13  # YYYYMMDD-HHMM
    
    print_success("Timestamp tests passed")
    return True

def test_git_functions():
    """Test git utility functions"""
    print("\n=== Testing Git Functions ===")
    
    # These require being in a git repo
    try:
        check_git_repo()
        print_success("Git repository check passed")
        
        branch = get_current_branch()
        print(f"Current branch: {branch}")
        assert branch != ""
        
        default = get_default_branch()
        print(f"Default branch: {default}")
        assert default in ["main", "master"]
        
        user = get_git_user()
        print(f"Git user: {user}")
        assert "@" in user or "<" in user
        
        print_success("Git function tests passed")
        return True
    except SystemExit:
        print_warning("Not in a git repository, skipping git tests")
        return True

def test_directory_functions():
    """Test directory utility functions"""
    print("\n=== Testing Directory Functions ===")
    
    # Test ensure_dir
    test_dir = "/tmp/rdd-test-dir"
    if os.path.exists(test_dir):
        os.rmdir(test_dir)
    
    ensure_dir(test_dir)
    assert os.path.exists(test_dir)
    assert os.path.isdir(test_dir)
    
    # Cleanup
    os.rmdir(test_dir)
    print_success("Directory function tests passed")
    
    return True

def test_config_functions():
    """Test configuration functions"""
    print("\n=== Testing Config Functions ===")
    
    # Create a test config file
    test_config = "/tmp/test-config.json"
    
    # Test set_config
    result = set_config("testKey", "testValue", test_config)
    assert result == True
    assert os.path.exists(test_config)
    
    # Test get_config
    value = get_config("testKey", test_config)
    assert value == "testValue"
    
    # Cleanup
    if os.path.exists(test_config):
        os.remove(test_config)
    
    print_success("Config function tests passed")
    return True

def main():
    """Run all tests"""
    print_banner("RDD Python Implementation Tests", "Validating Functionality")
    
    tests = [
        ("Color Output", test_color_output),
        ("Validation", test_validation),
        ("Normalization", test_normalization),
        ("Timestamps", test_timestamps),
        ("Git Functions", test_git_functions),
        ("Directory Functions", test_directory_functions),
        ("Config Functions", test_config_functions),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print_error(f"{name} test failed")
        except AssertionError as e:
            failed += 1
            print_error(f"{name} test failed: {e}")
        except Exception as e:
            failed += 1
            print_error(f"{name} test error: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")
    
    if failed == 0:
        print_success("All tests passed!")
        return 0
    else:
        print_error(f"{failed} test(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
