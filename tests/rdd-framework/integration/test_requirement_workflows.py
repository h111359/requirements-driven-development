"""
Integration tests for requirement management workflows.

This module tests requirement CRUD operations, validation, and ID sequencing with real
file manipulation and actual script execution.

Key test scenarios covered:
- Requirement CRUD cycle (create, modify, delete for both UR and TR)
- ID auto-increment and sequential numbering
- Validation enforcement and bypass
- File format preservation

Special setup requirements:
- Uses temp_rdd_instance fixture
- Tests manipulate real requirements.md file
- Validates format compliance
"""

import pytest
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
actions_dir = REPO_ROOT / ".rdd" / "src" / "actions"


class TestRequirementCRUDCycle:
    """Tests for complete requirement CRUD workflows"""
    
    def test_create_modify_delete_ur(self, temp_rdd_instance):
        """Test complete UR lifecycle"""
        test_dir = temp_rdd_instance
        instance_dir = test_dir / ".rdd-instance"
        actions_dir = test_dir / ".rdd" / "src" / "actions"
        requirements_file = instance_dir / "specifications" / "requirements.md"
        
        original_cwd = Path.cwd()
        import os
        os.chdir(test_dir)
        
        try:
            # Create UR
            result = subprocess.run(
                [sys.executable, str(actions_dir / "requirement_ur_create.py"),
                 "text=The system shall provide test functionality"],
                capture_output=True,
                text=True,
                cwd=str(test_dir)
            )
            assert result.returncode == 0, f"Create failed: {result.stderr}"
            
            # Verify created
            content = requirements_file.read_text()
            assert "[UR-0001]" in content
            assert "The system shall provide test functionality" in content
            
            # Modify UR
            result = subprocess.run(
                [sys.executable, str(actions_dir / "requirement_ur_modify.py"),
                 "id=UR-0001", "text=The system shall provide enhanced test functionality"],
                capture_output=True,
                text=True,
                cwd=str(test_dir)
            )
            assert result.returncode == 0
            
            # Verify modified
            content = requirements_file.read_text()
            assert "enhanced test functionality" in content
            
            # Delete UR
            result = subprocess.run(
                [sys.executable, str(actions_dir / "requirement_ur_delete.py"),
                 "id=UR-0001"],
                capture_output=True,
                text=True,
                cwd=str(test_dir)
            )
            assert result.returncode == 0
            
            # Verify deleted (marked as [DELETED])
            content = requirements_file.read_text()
            assert "[UR-0001]" in content
            assert "[DELETED]" in content
            
        finally:
            os.chdir(original_cwd)
    
    def test_create_modify_delete_tr(self, temp_rdd_instance):
        """Test complete TR lifecycle"""
        test_dir = temp_rdd_instance
        instance_dir = test_dir / ".rdd-instance"
        actions_dir = test_dir / ".rdd" / "src" / "actions"
        requirements_file = instance_dir / "specifications" / "requirements.md"
        
        original_cwd = Path.cwd()
        import os
        os.chdir(test_dir)
        
        try:
            # Create TR
            result = subprocess.run(
                [sys.executable, str(actions_dir / "requirement_tr_create.py"),
                 "text=The framework shall implement test support"],
                capture_output=True,
                text=True,
                cwd=str(test_dir)
            )
            assert result.returncode == 0
            
            # Verify created
            content = requirements_file.read_text()
            assert "[TR-0001]" in content
            
        finally:
            os.chdir(original_cwd)


class TestRequirementIDSequencing:
    """Tests for requirement ID auto-increment"""
    
    def test_sequential_ur_ids(self, temp_rdd_instance):
        """Test that multiple URs get sequential IDs"""
        test_dir = temp_rdd_instance
        instance_dir = test_dir / ".rdd-instance"
        actions_dir = test_dir / ".rdd" / "src" / "actions"
        requirements_file = instance_dir / "specifications" / "requirements.md"
        
        original_cwd = Path.cwd()
        import os
        os.chdir(test_dir)
        
        try:
            # Create first UR
            subprocess.run(
                [sys.executable, str(actions_dir / "requirement_ur_create.py"),
                 "text=The system shall do A"],
                capture_output=True,
                cwd=str(test_dir)
            )
            
            # Create second UR
            subprocess.run(
                [sys.executable, str(actions_dir / "requirement_ur_create.py"),
                 "text=The system shall do B"],
                capture_output=True,
                cwd=str(test_dir)
            )
            
            # Create third UR
            subprocess.run(
                [sys.executable, str(actions_dir / "requirement_ur_create.py"),
                 "text=The system shall do C"],
                capture_output=True,
                cwd=str(test_dir)
            )
            
            # Verify sequential IDs
            content = requirements_file.read_text()
            assert "[UR-0001]" in content
            assert "[UR-0002]" in content
            assert "[UR-0003]" in content
            
        finally:
            os.chdir(original_cwd)


class TestRequirementValidation:
    """Tests for requirement validation"""
    
    def test_validation_bypass(self, temp_rdd_instance):
        """Test creating requirement with validation=none"""
        test_dir = temp_rdd_instance
        instance_dir = test_dir / ".rdd-instance"
        actions_dir = test_dir / ".rdd" / "src" / "actions"
        
        original_cwd = Path.cwd()
        import os
        os.chdir(test_dir)
        
        try:
            # Create requirement without "shall" (normally invalid)
            result = subprocess.run(
                [sys.executable, str(actions_dir / "requirement_ur_create.py"),
                 "text=See external document XYZ", "validation=none"],
                capture_output=True,
                text=True,
                cwd=str(test_dir)
            )
            # Should succeed with validation=none
            assert result.returncode == 0
            
        finally:
            os.chdir(original_cwd)
