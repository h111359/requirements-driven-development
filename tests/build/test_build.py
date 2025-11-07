"""
test_build.py
Tests for build.py script
"""

import pytest
import sys
import os
import json
import zipfile
from pathlib import Path
from unittest.mock import patch, Mock

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

import build


class TestVersionExtraction:
    """Test version extraction from config.json"""
    
    def test_read_version_from_config(self, mock_rdd_project):
        """Test reading version from config.json"""
        os.chdir(mock_rdd_project)
        config_path = mock_rdd_project / ".rdd-docs" / "config.json"
        
        with open(config_path) as f:
            config = json.load(f)
        
        version = config.get("version")
        assert version == "1.0.0"
        assert isinstance(version, str)


class TestBuildDirCreation:
    """Test build directory creation"""
    
    def test_create_build_dir(self, mock_rdd_project):
        """Test creating build directory structure"""
        build_root = mock_rdd_project / "build"
        build_dir = build.create_build_dir("1.0.0", build_root)
        
        assert build_dir.exists()
        assert build_dir.name == "rdd-v1.0.0"
        assert (build_dir / ".github" / "prompts").exists()
        assert (build_dir / ".rdd" / "scripts").exists()
        assert (build_dir / ".rdd" / "templates").exists()
        assert (build_dir / ".rdd-docs").exists()
        assert (build_dir / ".vscode").exists()


class TestFileCopying:
    """Test file copying operations"""
    
    def test_copy_prompts(self, mock_rdd_project):
        """Test copying prompt files"""
        build_dir = build.create_build_dir("1.0.0", mock_rdd_project / "build")
        build.copy_prompts(mock_rdd_project, build_dir)
        
        prompts_dst = build_dir / ".github" / "prompts"
        assert (prompts_dst / "test.prompt.md").exists()
    
    def test_copy_scripts(self, mock_rdd_project):
        """Test copying script files"""
        build_dir = build.create_build_dir("1.0.0", mock_rdd_project / "build")
        build.copy_scripts(mock_rdd_project, build_dir)
        
        scripts_dst = build_dir / ".rdd" / "scripts"
        assert (scripts_dst / "rdd.py").exists()
        assert (scripts_dst / "rdd_utils.py").exists()
    
    def test_copy_templates(self, mock_rdd_project):
        """Test copying template files"""
        build_dir = build.create_build_dir("1.0.0", mock_rdd_project / "build")
        build.copy_templates(mock_rdd_project, build_dir)
        
        templates_dst = build_dir / ".rdd" / "templates"
        assert (templates_dst / "test.md").exists()
    
    def test_copy_vscode_settings(self, mock_rdd_project):
        """Test copying VS Code settings"""
        build_dir = build.create_build_dir("1.0.0", mock_rdd_project / "build")
        build.copy_vscode_settings(mock_rdd_project, build_dir)
        
        settings_file = build_dir / ".vscode" / "settings.json"
        assert settings_file.exists()
    
    def test_copy_rdd_docs_seeds(self, mock_rdd_project):
        """Test copying seed templates to .rdd-docs"""
        build_dir = build.create_build_dir("1.0.0", mock_rdd_project / "build")
        build.copy_rdd_docs_seeds(mock_rdd_project, build_dir)
        
        rdd_docs = build_dir / ".rdd-docs"
        assert (rdd_docs / "config.json").exists()
        assert (rdd_docs / "data-model.md").exists()
        assert (rdd_docs / "requirements.md").exists()
        assert (rdd_docs / "tech-spec.md").exists()


class TestTemplateGeneration:
    """Test template processing and generation"""
    
    def test_generate_readme(self, mock_rdd_project):
        """Test README generation with version substitution"""
        build_dir = build.create_build_dir("1.0.0", mock_rdd_project / "build")
        build.generate_readme(build_dir, "1.0.0", mock_rdd_project)
        
        readme = build_dir / "README.md"
        assert readme.exists()
        content = readme.read_text()
        assert "{{VERSION}}" not in content
        assert "1.0.0" in content
    
    def test_generate_installer(self, mock_rdd_project):
        """Test install.py generation"""
        build_dir = build.create_build_dir("1.0.0", mock_rdd_project / "build")
        build.generate_installer(build_dir, "1.0.0", mock_rdd_project)
        
        installer = build_dir / "install.py"
        assert installer.exists()
        content = installer.read_text()
        assert "{{VERSION}}" not in content
        assert "1.0.0" in content


class TestArchiveCreation:
    """Test ZIP archive creation"""
    
    def test_create_archive(self, mock_rdd_project):
        """Test creating ZIP archive"""
        build_dir = build.create_build_dir("1.0.0", mock_rdd_project / "build")
        
        # Add some files
        (build_dir / "test.txt").write_text("test")
        
        archive_path = build.create_archive(
            build_dir,
            mock_rdd_project / "build",
            "1.0.0"
        )
        
        assert archive_path.exists()
        assert archive_path.name == "rdd-v1.0.0.zip"
        
        # Verify archive contents
        with zipfile.ZipFile(archive_path, 'r') as zipf:
            files = zipf.namelist()
            assert any("test.txt" in f for f in files)


class TestChecksumGeneration:
    """Test checksum file generation"""
    
    def test_generate_checksum(self, mock_rdd_project):
        """Test SHA256 checksum generation"""
        build_dir = build.create_build_dir("1.0.0", mock_rdd_project / "build")
        (build_dir / "test.txt").write_text("test")
        
        archive_path = build.create_archive(
            build_dir,
            mock_rdd_project / "build",
            "1.0.0"
        )
        
        build.generate_checksum(archive_path)
        
        checksum_path = archive_path.parent / f"{archive_path.name}.sha256"
        assert checksum_path.exists()
        
        content = checksum_path.read_text()
        assert "rdd-v1.0.0.zip" in content
        assert len(content.split()[0]) == 64  # SHA256 is 64 hex chars


class TestOutputFunctions:
    """Test build script output functions"""
    
    def test_print_success(self, capsys):
        build.print_success("Test message")
        captured = capsys.readouterr()
        assert "Test message" in captured.out
        assert "✓" in captured.out
    
    def test_print_error(self, capsys):
        build.print_error("Error message")
        captured = capsys.readouterr()
        assert "Error message" in captured.err
        assert "✗" in captured.err
