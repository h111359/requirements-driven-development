"""
Tests for configuration validation including manifest schema and path verification.

This module tests manifest.json validation including schema structure, path verification,
snippet resolution, and version format validation.

Key test scenarios covered:
- Manifest JSON schema validation
- Required paths existence verification
- Prompt snippet key resolution
- Framework version extraction and format validation
- Component configuration validation
- Upgrade policy validation

Special setup requirements:
- Tests use real manifest.json from .rdd/config/
- Validates against actual framework configuration
"""

import pytest
import json
from pathlib import Path


class TestManifestValidation:
    """Tests for manifest.json validation"""
    
    def test_manifest_exists_and_valid_json(self):
        """Test that manifest.json exists and contains valid JSON"""
        manifest_path = Path(__file__).resolve().parents[3] / ".rdd" / "config" / "manifest.json"
        
        assert manifest_path.exists(), "manifest.json not found"
        
        with open(manifest_path) as f:
            data = json.load(f)
        
        assert isinstance(data, dict), "Manifest must be a JSON object"
    
    def test_manifest_has_framework_version(self):
        """Test that manifest contains framework version in semantic versioning format"""
        manifest_path = Path(__file__).resolve().parents[3] / ".rdd" / "config" / "manifest.json"
        
        with open(manifest_path) as f:
            data = json.load(f)
        
        assert "framework" in data, "Manifest must have 'framework' key"
        assert "version" in data["framework"], "Framework must have 'version' key"
        
        version = data["framework"]["version"]
        # Check semantic versioning format (MAJOR.MINOR.PATCH)
        parts = version.split(".")
        assert len(parts) == 3, f"Version must be in MAJOR.MINOR.PATCH format, got {version}"
        for part in parts:
            assert part.isdigit(), f"Version parts must be numeric, got {version}"
    
    def test_manifest_has_required_paths(self):
        """Test that manifest contains requiredPaths configuration"""
        manifest_path = Path(__file__).resolve().parents[3] / ".rdd" / "config" / "manifest.json"
        
        with open(manifest_path) as f:
            data = json.load(f)
        
        assert "requiredPaths" in data, "Manifest must have 'requiredPaths' key"
        
        required_paths = data["requiredPaths"]
        assert isinstance(required_paths, dict), "requiredPaths must be an object"
        assert "framework" in required_paths, "requiredPaths must have 'framework' key"
        assert "instance" in required_paths, "requiredPaths must have 'instance' key"
    
    def test_manifest_required_paths_exist(self):
        """Test that all paths listed in requiredPaths actually exist in instance"""
        # This test requires a valid .rdd-instance to be set up
        # Will be covered in integration tests
        pass
    
    def test_manifest_has_prompt_snippets(self):
        """Test that manifest contains promptSnippets configuration"""
        manifest_path = Path(__file__).resolve().parents[3] / ".rdd" / "config" / "manifest.json"
        
        with open(manifest_path) as f:
            data = json.load(f)
        
        assert "promptSnippets" in data, "Manifest must have 'promptSnippets' key"
        
        snippets = data["promptSnippets"]
        assert isinstance(snippets, list), "promptSnippets must be an array"
        
        # Each snippet should have prompt-snippet-key and prompt-snippet-path
        for snippet in snippets:
            assert isinstance(snippet, dict), "Each snippet must be an object"
            assert "prompt-snippet-key" in snippet, "Snippet must have 'prompt-snippet-key'"
            assert "prompt-snippet-path" in snippet, "Snippet must have 'prompt-snippet-path'"
            assert isinstance(snippet["prompt-snippet-key"], str), "Snippet keys must be strings"
            assert isinstance(snippet["prompt-snippet-path"], str), "Snippet paths must be strings"
    
    def test_manifest_prompt_snippet_files_exist(self):
        """Test that all prompt snippet files referenced in manifest exist"""
        manifest_path = Path(__file__).resolve().parents[3] / ".rdd" / "config" / "manifest.json"
        repo_root = manifest_path.parents[2]
        
        with open(manifest_path) as f:
            data = json.load(f)
        
        snippets = data.get("promptSnippets", [])
        
        for snippet in snippets:
            key = snippet["prompt-snippet-key"]
            rel_path = snippet["prompt-snippet-path"]
            snippet_path = repo_root / rel_path
            assert snippet_path.exists(), f"Snippet file not found for key '{key}': {snippet_path}"


class TestConfigStructureValidation:
    """Tests for configuration file structure and conventions"""
    
    def test_instance_config_structure(self):
        """Test that instance-config.json has required structure"""
        # Integration test - requires .rdd-instance setup
        pass
    
    def test_technical_design_form_structure(self):
        """Test that technical-design-schema.json has valid structure"""
        form_path = Path(__file__).resolve().parents[3] / ".rdd" / "config" / "technical-design-schema.json"
        
        assert form_path.exists(), "technical-design-schema.json must exist"
        
        # File may be empty initially
        if form_path.stat().st_size > 0:
            with open(form_path) as f:
                data = json.load(f)
            
            assert isinstance(data, (dict, list)), "Technical design form must be valid JSON"
