"""
conftest.py
Pytest fixtures for install script tests
"""

import pytest
import tempfile
import shutil
import json
from pathlib import Path
import subprocess


@pytest.fixture
def temp_install_dir():
    """Create temporary installation directory"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_git_repo_for_install(temp_install_dir):
    """Create mock git repository for installation testing"""
    repo_dir = temp_install_dir / "target-repo"
    repo_dir.mkdir()
    
    # Initialize git repo
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True, capture_output=True)
    
    # Create initial commit
    readme = repo_dir / "README.md"
    readme.write_text("# Target Repository")
    subprocess.run(["git", "add", "README.md"], cwd=repo_dir, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_dir, check=True, capture_output=True)
    
    yield repo_dir


@pytest.fixture
def mock_rdd_archive(temp_install_dir):
    """Create mock RDD archive structure"""
    archive_dir = temp_install_dir / "rdd-v1.0.0"
    archive_dir.mkdir()
    
    # Create directory structure
    (archive_dir / ".github" / "prompts").mkdir(parents=True)
    (archive_dir / ".rdd" / "scripts").mkdir(parents=True)
    (archive_dir / ".rdd" / "templates").mkdir(parents=True)
    (archive_dir / ".rdd-docs").mkdir(parents=True)
    (archive_dir / ".vscode").mkdir(parents=True)
    
    # Create mock files
    (archive_dir / ".rdd" / "scripts" / "rdd.py").write_text('#!/usr/bin/env python3\nprint("RDD")')
    (archive_dir / ".rdd" / "scripts" / "rdd_utils.py").write_text('# Utils')
    (archive_dir / ".rdd" / "templates" / "test.md").write_text('# Template')
    (archive_dir / ".github" / "prompts" / "test.prompt.md").write_text('# Prompt')
    
    # Create seed templates in .rdd-docs
    config = {
        "version": "1.0.0",
        "defaultBranch": "main",
        "created": "2025-01-01T00:00:00Z",
        "lastModified": "2025-01-01T00:00:00Z"
    }
    (archive_dir / ".rdd-docs" / "config.json").write_text(json.dumps(config, indent=2))
    (archive_dir / ".rdd-docs" / "requirements.md").write_text('# Requirements')
    (archive_dir / ".rdd-docs" / "tech-spec.md").write_text('# Tech Spec')
    (archive_dir / ".rdd-docs" / "data-model.md").write_text('# Data Model')
    
    # VS Code settings
    settings = {
        "chat.promptFilesRecommendations": [],
        "chat.tools.terminal.autoApprove": [],
        "files.associations": {},
        "editor.rulers": [80, 120]
    }
    (archive_dir / ".vscode" / "settings.json").write_text(json.dumps(settings, indent=2))
    
    # LICENSE
    (archive_dir / "LICENSE").write_text("MIT License")
    
    yield archive_dir
