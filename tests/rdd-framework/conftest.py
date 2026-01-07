"""
Shared pytest fixtures and configuration for RDD framework tests.

This module provides common fixtures used across all RDD framework test modules including:
- Temporary RDD instance setup with required directory structure
- Mock registry utilities for testing prompt workflows
- Sample prompt creation helpers
- Mock requirements file for requirement tests
- Cleanup utilities to ensure test isolation

Special setup requirements:
- Tests use shared .rdd-instance-test/ directory cleaned before each test
- Fixtures support both unit tests (with mocking) and integration tests (with real files)
"""

import pytest
import json
import os
import shutil
from pathlib import Path
from datetime import datetime


@pytest.fixture
def temp_rdd_instance(tmp_path):
    """
    Creates a temporary .rdd-instance-test/ directory with required RDD structure.
    
    This fixture sets up a minimal RDD instance suitable for integration testing
    with real filesystem operations. The structure includes:
    - workdir/ with work-iteration-registry.json
    - specifications/ folder
    - config/ folder with instance-config.json
    
    Args:
        tmp_path: pytest's built-in temporary directory fixture
        
    Returns:
        Path: Path to the temporary .rdd-instance-test directory
        
    Yields:
        Path: The temporary instance directory, cleaned up after test completion
    """
    # Create base structure
    instance_dir = tmp_path / ".rdd-instance-test"
    instance_dir.mkdir()
    
    # Create subdirectories
    workdir = instance_dir / "workdir"
    workdir.mkdir()
    
    specs_dir = instance_dir / "specifications"
    specs_dir.mkdir()
    
    config_dir = instance_dir / "config"
    config_dir.mkdir()
    
    archive_dir = instance_dir / "archive"
    archive_dir.mkdir()
    
    # Create initial work-iteration-registry.json
    registry_file = workdir / "work-iteration-registry.json"
    initial_registry = {
        "iteration-id": "ITR-TEST-001",
        "iteration-name": "Test Iteration",
        "prompt-id-sequence-next-value": 1,
        "prompts": []
    }
    registry_file.write_text(json.dumps(initial_registry, indent=4))
    
    # Create instance-config.json
    config_file = config_dir / "instance-config.json"
    instance_config = {
        "git-enabled": False
    }
    config_file.write_text(json.dumps(instance_config, indent=4))
    
    # Create empty requirements.md
    requirements_file = specs_dir / "requirements.md"
    requirements_file.write_text("## Product Name\n\nTest Product\n\n## User Requirements\n\n")
    
    yield instance_dir
    
    # Cleanup is handled automatically by tmp_path


@pytest.fixture
def mock_registry():
    """
    Provides a mock work-iteration-registry.json with configurable prompts.
    
    Returns a factory function that creates registry dictionaries with various
    prompt states for testing different scenarios.
    
    Returns:
        callable: Factory function that accepts prompt configurations and returns registry dict
    """
    def _create_registry(prompts=None, iteration_id="ITR-TEST-001", iteration_name="Test", next_id=1):
        """
        Factory function to create mock registry with custom prompts.
        
        Args:
            prompts: List of prompt dictionaries (default: empty list)
            iteration_id: Iteration ID string
            iteration_name: Iteration name string
            next_id: Next prompt ID sequence value
            
        Returns:
            dict: Complete registry dictionary
        """
        if prompts is None:
            prompts = []
        
        return {
            "iteration-id": iteration_id,
            "iteration-name": iteration_name,
            "prompt-id-sequence-next-value": next_id,
            "prompts": prompts
        }
    
    return _create_registry


@pytest.fixture
def sample_prompt():
    """
    Provides a sample prompt dictionary with realistic field values.
    
    Returns a factory function that creates prompt dictionaries for testing
    with customizable fields.
    
    Returns:
        callable: Factory function that returns prompt dict with specified overrides
    """
    def _create_prompt(prompt_id="P-001", title="Test Prompt", state="active", **kwargs):
        """
        Factory function to create sample prompt with defaults.
        
        Args:
            prompt_id: Prompt identifier (default: "P-001")
            title: Prompt title (default: "Test Prompt")
            state: Prompt state (default: "active")
            **kwargs: Additional fields to override defaults
            
        Returns:
            dict: Complete prompt dictionary
        """
        prompt = {
            "prompt-id": prompt_id,
            "prompt-title": title,
            "state": state,
            "questionnaire-generated": False,
            "questionnaire-answered": False,
            "plan-generated": False,
            "analysis-generated": False,
            "implementation-completed": False,
            "execution-mode": "no-action",
            "executed": False
        }
        prompt.update(kwargs)
        return prompt
    
    return _create_prompt


@pytest.fixture
def mock_requirements_file():
    """
    Provides mock requirements.md content for requirement tests.
    
    Returns a factory function that creates requirements file content with
    various existing requirements for testing ID generation and CRUD operations.
    
    Returns:
        callable: Factory function that returns requirements content string
    """
    def _create_requirements(ur_count=0, tr_count=0):
        """
        Factory function to create requirements file content.
        
        Args:
            ur_count: Number of existing UR requirements
            tr_count: Number of existing TR requirements
            
        Returns:
            str: Complete requirements.md content
        """
        content = "## Product Name\n\nTest Product\n\n## User Requirements\n\n"
        
        for i in range(1, ur_count + 1):
            content += f"- [UR-{i:04d}] Sample user requirement {i}\n\n"
        
        content += "\n## Technical Requirements\n\n"
        
        for i in range(1, tr_count + 1):
            content += f"- [TR-{i:04d}] Sample technical requirement {i}\n\n"
        
        return content
    
    return _create_requirements


@pytest.fixture
def clean_test_instance():
    """
    Ensures .rdd-instance-test/ is cleaned before each test.
    
    This fixture is useful for integration tests that need to start with
    a completely clean state. It removes any existing .rdd-instance-test/
    directory in the current working directory.
    
    Yields:
        None: Cleanup happens before test execution
    """
    test_instance_path = Path(".rdd-instance-test")
    
    # Clean before test
    if test_instance_path.exists():
        shutil.rmtree(test_instance_path)
    
    yield
    
    # Clean after test
    if test_instance_path.exists():
        shutil.rmtree(test_instance_path)


@pytest.fixture
def mock_prompt_folder(tmp_path):
    """
    Creates a mock prompt folder with prompt.md and other artifacts.
    
    Useful for testing action scripts that operate on prompt folders.
    
    Args:
        tmp_path: pytest's built-in temporary directory fixture
        
    Returns:
        callable: Factory function that creates prompt folder and returns path
    """
    def _create_prompt_folder(prompt_id="P-001", title="Test", include_files=None):
        """
        Factory function to create prompt folder with artifacts.
        
        Args:
            prompt_id: Prompt ID
            title: Prompt title
            include_files: List of files to create ('prompt', 'questionnaire', 'plan', 
                          'analysis', 'implementation')
            
        Returns:
            Path: Path to created prompt folder
        """
        if include_files is None:
            include_files = ['prompt']
        
        folder_name = f"{prompt_id}_{title.replace(' ', '_')}"
        prompt_folder = tmp_path / "workdir" / folder_name
        prompt_folder.mkdir(parents=True)
        
        # Create requested files
        if 'prompt' in include_files:
            (prompt_folder / "prompt.md").write_text("# Test Prompt\n\nContent here.")
        
        if 'questionnaire' in include_files:
            questionnaire_data = {
                "context": "Test context",
                "questions": []
            }
            (prompt_folder / "questionnaire.json").write_text(json.dumps(questionnaire_data, indent=2))
        
        if 'plan' in include_files:
            (prompt_folder / "plan.md").write_text("# Implementation Plan\n\nSteps here.")
        
        if 'analysis' in include_files:
            (prompt_folder / "analysis.md").write_text("# Analysis\n\nAnalysis here.")
        
        if 'implementation' in include_files:
            (prompt_folder / "implementation.md").write_text("# Implementation Log\n\nLog here.")
        
        return prompt_folder
    
    return _create_prompt_folder


@pytest.fixture
def captured_timestamp():
    """
    Provides a fixed timestamp for testing timestamp-dependent operations.
    
    Returns:
        str: ISO8601 formatted timestamp
    """
    return "2026-01-07T10:30:00"
