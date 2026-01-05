"""
conftest.py
Pytest configuration and shared fixtures for RDD framework tests
"""

import pytest
import os
import sys
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import Mock, patch
import subprocess


@pytest.fixture
def temp_dir():
    """Create a temporary directory that's cleaned up after the test"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_git_repo(temp_dir):
    """Create a mock git repository"""
    # Initialize git repo with main as default branch
    subprocess.run(["git", "init", "-b", "main"], cwd=temp_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_dir, check=True, capture_output=True)
    
    # Create initial commit
    readme = temp_dir / "README.md"
    readme.write_text("# Test Repository")
    subprocess.run(["git", "add", "README.md"], cwd=temp_dir, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=temp_dir, check=True, capture_output=True)
    
    yield temp_dir


@pytest.fixture
def rdd_workspace(mock_git_repo):
    """Create a mock RDD workspace structure"""
    repo = mock_git_repo
    
    # Create RDD directories
    (repo / ".rdd" / "scripts").mkdir(parents=True)
    (repo / ".rdd" / "templates").mkdir(parents=True)
    (repo / ".github" / "prompts").mkdir(parents=True)
    (repo / ".rdd-docs" / "workspace").mkdir(parents=True)
    (repo / ".rdd-docs" / "archive").mkdir(parents=True)
    
    # Create config.json (version moved to about.json)
    config = {
        "defaultBranch": "main",
        "created": "2025-01-01T00:00:00Z",
        "lastModified": "2025-01-01T00:00:00Z"
    }
    config_path = repo / ".rdd-docs" / "config.json"
    config_path.write_text(json.dumps(config, indent=2))
    
    # Create about.json with version
    about = {
        "version": "1.0.0"
    }
    about_path = repo / ".rdd" / "about.json"
    about_path.write_text(json.dumps(about, indent=2))
    
    # Create basic documentation files
    (repo / ".rdd-docs" / "requirements.md").write_text("# Requirements\n")
    (repo / ".rdd-docs" / "tech-spec.md").write_text("# Technical Specification\n\n## Data Architecture\n\n## Project Folder Structure\n")
    
    yield repo


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run for git commands"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(
            returncode=0,
            stdout="",
            stderr=""
        )
        yield mock_run


@pytest.fixture
def sample_change_config():
    """Sample change configuration"""
    return {
        "type": "fix",
        "name": "test-fix",
        "branch": "fix/test-fix",
        "created": "2025-11-07T10:00:00Z",
        "author": "test@example.com"
    }


@pytest.fixture
def sample_requirements_changes():
    """Sample requirements changes content"""
    return """## General Functionalities

- [ADDED] [GF-NEW] New Feature: Description of new functionality

## Functional Requirements

- [MODIFIED] [FR-01] Updated Requirement: Updated description
- [DELETED] [FR-02] Removed Requirement: Reason for removal

## Non-Functional Requirements

- [ADDED] [NFR-NEW] Performance: New performance requirement
"""


@pytest.fixture
def mock_curses():
    """Mock curses for menu testing"""
    with patch('curses.wrapper') as mock_wrapper:
        mock_wrapper.side_effect = lambda func, *args: func(Mock(), *args)
        yield mock_wrapper


@pytest.fixture(autouse=True)
def reset_sys_path():
    """Reset sys.path after each test"""
    original_path = list(sys.path)
    yield
    sys.path[:] = original_path


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow"
    )
    config.addinivalue_line(
        "markers", "requires_git: mark test as requiring git"
    )
