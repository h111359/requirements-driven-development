"""
End-to-end integration tests validating complete prompt lifecycle workflows.

This module tests complete prompt workflows from creation through completion including
questionnaire, plan, analysis, and implementation phases using real filesystem operations
in temporary directories.

Key test scenarios covered:
- Complete prompt workflow: Create → Questionnaire → Plan → Implement → Complete
- Modification workflow: Complete prompt → Create modification → Execute → Complete
- Multiple prompts workflow: Create multiple → Single active constraint → Complete in sequence
- State transitions and flag management throughout lifecycle

Special setup requirements:
- Uses temp_rdd_instance fixture for isolated testing
- Executes real action scripts via subprocess
- Validates actual file creation and JSON updates
- Tests run with real .rdd-instance-test/ directory
"""

import pytest
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
ACTIONS_DIR = REPO_ROOT / ".rdd" / "src" / "actions"


class TestCompletePromptWorkflow:
    """Tests for complete prompt lifecycle from creation to completion"""
    
    def test_full_prompt_lifecycle(self, temp_rdd_instance):
        """Test complete workflow: create → clarify → analyze → plan → implement → complete"""
        instance_dir = temp_rdd_instance
        workdir = instance_dir / "workdir"
        registry_file = workdir / "work-iteration-registry.json"
        
        # Change to repo root for script execution
        original_cwd = Path.cwd()
        import os
        os.chdir(REPO_ROOT)
        
        try:
            # Step 1: Create a prompt
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_create.py"), "title=Integration Test Prompt"],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            
            assert result.returncode == 0, f"prompt_create failed: {result.stderr}"
            prompt_id = result.stdout.strip()
            assert prompt_id == "P-001"
            
            # Verify registry updated
            with open(registry_file) as f:
                registry = json.load(f)
            
            assert len(registry["prompts"]) == 1
            prompt = registry["prompts"][0]
            assert prompt["prompt-id"] == "P-001"
            assert prompt["state"] == "active"
            assert prompt["execution-mode"] == "no-action"
            
            # Verify prompt folder created
            prompt_folder = workdir / "P-001_Integration_Test_Prompt"
            assert prompt_folder.exists()
            assert (prompt_folder / "prompt.md").exists()
            
            # Step 2: Generate questionnaire (simulate by setting flag)
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_questionnaire_generated_on.py")],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result.returncode == 0
            
            # Create a sample questionnaire file
            questionnaire_data = {
                "context": "Test context",
                "questions": [
                    {
                        "id": "Q1",
                        "question-text": "Test question?",
                        "options": [
                            {"id": "A", "label": "Option A", "pros": "Good", "cons": "None"}
                        ],
                        "recommended-option": "A",
                        "recommendation-rationale": "Best choice",
                        "user-selection": {"type": "predefined", "value": "A"}
                    }
                ]
            }
            questionnaire_file = prompt_folder / "questionnaire.json"
            with open(questionnaire_file, "w") as f:
                json.dump(questionnaire_data, f, indent=2)
            
            # Mark questionnaire as answered
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "questionnaire_check_complete.py")],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result.returncode == 0
            
            # Step 3: Generate analysis (simulate)
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_analysis_generated_on.py")],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result.returncode == 0
            
            # Create analysis file
            analysis_file = prompt_folder / "analysis.md"
            analysis_file.write_text("# Analysis\n\nAnalysis content here.")
            
            # Step 4: Generate plan (simulate)
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_plan_generated_on.py")],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result.returncode == 0
            
            # Create plan file
            plan_file = prompt_folder / "plan.md"
            plan_file.write_text("# Plan\n\n## Step 1\nDo something.")
            
            # Step 5: Mark implementation completed
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_implementation_completed_on.py")],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result.returncode == 0
            
            # Create implementation file
            impl_file = prompt_folder / "implementation.md"
            impl_file.write_text("# Implementation\n\nImplementation log.")
            
            # Step 6: Mark as executed
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_set_executed_on.py")],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result.returncode == 0
            
            # Verify all flags are set
            with open(registry_file) as f:
                registry = json.load(f)
            
            prompt = registry["prompts"][0]
            assert prompt["questionnaire-generated"] == True
            assert prompt["questionnaire-answered"] == True
            assert prompt["analysis-generated"] == True
            assert prompt["plan-generated"] == True
            assert prompt["implementation-completed"] == True
            assert prompt["executed"] == True
            
            # Step 7: Complete the prompt
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_set_state.py"), "state=completed"],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result.returncode == 0
            
            # Verify final state
            with open(registry_file) as f:
                registry = json.load(f)
            
            prompt = registry["prompts"][0]
            assert prompt["state"] == "completed"
            
        finally:
            os.chdir(original_cwd)
    
    def test_create_multiple_prompts_enforces_single_active(self, temp_rdd_instance):
        """Test that only one prompt can be active at a time"""
        instance_dir = temp_rdd_instance
        workdir = instance_dir / "workdir"
        
        original_cwd = Path.cwd()
        import os
        os.chdir(REPO_ROOT)
        
        try:
            # Create first prompt (active by default)
            result1 = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_create.py"), "title=First Prompt"],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result1.returncode == 0
            
            # Try to create second active prompt - should fail
            result2 = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_create.py"), "title=Second Prompt", "state=active"],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result2.returncode != 0
            assert "Only one prompt" in result2.stderr or "already active" in result2.stderr
            
        finally:
            os.chdir(original_cwd)


class TestModificationWorkflow:
    """Tests for modification workflow on completed prompts"""
    
    def test_modification_lifecycle(self, temp_rdd_instance):
        """Test complete modification workflow"""
        instance_dir = temp_rdd_instance
        workdir = instance_dir / "workdir"
        
        original_cwd = Path.cwd()
        import os
        os.chdir(REPO_ROOT)
        
        try:
            # Create and complete a prompt first
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_create.py"), "title=Test Prompt"],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result.returncode == 0
            prompt_id = result.stdout.strip()
            
            # Mark implementation completed
            subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_implementation_completed_on.py")],
                capture_output=True,
                cwd=str(REPO_ROOT)
            )
            
            # Create modification
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "modification_create.py"), 
                 f"prompt-id={prompt_id}", "description=Fix a bug"],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result.returncode == 0
            
            # Verify modification file created
            prompt_folder = workdir / "P-001_Test_Prompt"
            modification_file = prompt_folder / "modification-001.md"
            assert modification_file.exists()
            
            # Complete modification
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "modification_complete.py")],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result.returncode == 0
            
        finally:
            os.chdir(original_cwd)


class TestStateTransitions:
    """Tests for prompt state transitions"""
    
    def test_bidirectional_state_transitions(self, temp_rdd_instance):
        """Test that prompts can transition between active and completed freely"""
        instance_dir = temp_rdd_instance
        
        original_cwd = Path.cwd()
        import os
        os.chdir(REPO_ROOT)
        
        try:
            # Create prompt (active by default)
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_create.py"), "title=Test Prompt"],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result.returncode == 0
            prompt_id = result.stdout.strip()
            
            # Transition to completed
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_set_state.py"), 
                 "state=completed", f"prompt-id={prompt_id}"],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result.returncode == 0
            
            # Transition back to active
            result = subprocess.run(
                [sys.executable, str(ACTIONS_DIR / "prompt_set_state.py"), 
                 "state=active", f"prompt-id={prompt_id}"],
                capture_output=True,
                text=True,
                cwd=str(REPO_ROOT)
            )
            assert result.returncode == 0
            
        finally:
            os.chdir(original_cwd)
