"""
conftest.py
Pytest fixtures for build script tests
"""

import pytest
import tempfile
import shutil
import json
from pathlib import Path


@pytest.fixture
def temp_build_dir():
    """Create temporary build directory"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_rdd_project(temp_build_dir):
    """Create mock RDD project structure for build testing"""
    project_root = temp_build_dir / "rdd-project"
    project_root.mkdir()
    
    # Create directory structure
    (project_root / ".github" / "prompts").mkdir(parents=True)
    (project_root / ".rdd" / "scripts").mkdir(parents=True)
    (project_root / ".rdd" / "templates").mkdir(parents=True)
    (project_root / ".rdd-docs").mkdir(parents=True)
    (project_root / "scripts").mkdir(parents=True)
    (project_root / "templates").mkdir(parents=True)
    (project_root / "build").mkdir(parents=True)
    
    # Create config.json with version
    config = {
        "version": "1.0.0",
        "defaultBranch": "main",
        "created": "2025-01-01T00:00:00Z",
        "lastModified": "2025-01-01T00:00:00Z"
    }
    config_path = project_root / ".rdd-docs" / "config.json"
    config_path.write_text(json.dumps(config, indent=2))
    
    # Create mock prompts
    (project_root / ".github" / "prompts" / "test.prompt.md").write_text("# Test Prompt")
    
    # Create mock scripts
    (project_root / ".rdd" / "scripts" / "rdd.py").write_text('#!/usr/bin/env python3\nprint("rdd")')
    (project_root / ".rdd" / "scripts" / "rdd_utils.py").write_text('# Utils')
    
    # Create mock templates
    (project_root / ".rdd" / "templates" / "test.md").write_text("# Template")
    (project_root / "templates" / "config.json").write_text(json.dumps(config, indent=2))
    (project_root / "templates" / "settings.json").write_text('{}')
    (project_root / "templates" / "README.md").write_text("# RDD v{{VERSION}}")
    (project_root / "templates" / "data-model.md").write_text("# Data Model")
    (project_root / "templates" / "requirements.md").write_text("# Requirements")
    (project_root / "templates" / "tech-spec.md").write_text("# Tech Spec")
    (project_root / "templates" / "folder-structure.md").write_text("# Folder Structure")
    
    # Create LICENSE
    (project_root / "LICENSE").write_text("MIT License")
    
    # Create installer templates
    (project_root / "scripts" / "install.py").write_text(
        '#!/usr/bin/env python3\nVERSION = "{{VERSION}}"\nprint("Installer")'
    )
    (project_root / "scripts" / "install.sh").write_text(
        '#!/bin/bash\nVERSION="{{VERSION}}"\necho "Installer"'
    )
    (project_root / "scripts" / "install.ps1").write_text(
        '$VERSION = "{{VERSION}}"\nWrite-Host "Installer"'
    )
    
    yield project_root
