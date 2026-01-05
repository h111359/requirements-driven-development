"""
test_seed.py
Test suite for rdd-instance_seed.py script
"""

import pytest
import json
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_repo(tmp_path):
    """Create a temporary repository structure with minimal RDD framework"""
    repo = tmp_path / "test-repo"
    repo.mkdir()
    
    # Create .rdd structure
    rdd_dir = repo / ".rdd"
    (rdd_dir / "config").mkdir(parents=True)
    (rdd_dir / "src" / "actions").mkdir(parents=True)
    (rdd_dir / "conventions").mkdir(parents=True)
    
    # Copy the seed script to the test repo
    seed_script_source = Path(__file__).resolve().parents[2] / ".rdd" / "src" / "actions" / "rdd-instance_seed.py"
    seed_script_dest = rdd_dir / "src" / "actions" / "rdd-instance_seed.py"
    if seed_script_source.exists():
        shutil.copy(seed_script_source, seed_script_dest)
    
    yield repo
    
    # Cleanup is automatic with tmp_path


@pytest.fixture
def minimal_manifest(temp_repo):
    """Create a minimal valid manifest.json"""
    manifest_data = {
        "requiredPaths": {
            "instance": [
                ".rdd-instance/specifications",
                ".rdd-instance/workdir",
                ".rdd-instance/archive"
            ]
        },
        "requiredInstanceFiles": [
            {
                "path": ".rdd-instance/specifications/requirements.md",
                "convention": ".rdd/conventions/requirements.convention.md"
            },
            {
                "path": ".rdd-instance/specifications/technical-design.json",
                "convention": ".rdd/conventions/technical-design.convention.md"
            },
            {
                "path": ".rdd-instance/specifications/files-and-folders.md",
                "convention": ".rdd/conventions/files-and-folders.convention.md"
            }
        ]
    }
    
    manifest_path = temp_repo / ".rdd" / "config" / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest_data, f, indent=2)
    
    # Create convention files (they just need to exist)
    for file_entry in manifest_data["requiredInstanceFiles"]:
        conv_path = temp_repo / file_entry["convention"]
        conv_path.parent.mkdir(parents=True, exist_ok=True)
        conv_path.write_text("# Convention file\n")
    
    return manifest_path


def run_seed_script(repo_path, verbose=False):
    """Helper function to run the seed script"""
    seed_script = repo_path / ".rdd" / "src" / "actions" / "rdd-instance_seed.py"
    cmd = [sys.executable, str(seed_script)]
    if verbose:
        cmd.append("--verbose")
    
    result = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    return result


def test_creates_missing_folders(temp_repo, minimal_manifest):
    """Verify the script creates missing required folders"""
    # Ensure folders don't exist
    assert not (temp_repo / ".rdd-instance" / "specifications").exists()
    assert not (temp_repo / ".rdd-instance" / "workdir").exists()
    
    # Run seed script
    result = run_seed_script(temp_repo)
    
    # Check exit code
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    
    # Verify folders were created
    assert (temp_repo / ".rdd-instance" / "specifications").exists()
    assert (temp_repo / ".rdd-instance" / "workdir").exists()
    assert (temp_repo / ".rdd-instance" / "archive").exists()
    
    # Check output mentions folder creation
    assert "folders created" in result.stdout.lower()


def test_creates_missing_files(temp_repo, minimal_manifest):
    """Verify the script creates missing required files with valid content"""
    # Ensure files don't exist
    req_file = temp_repo / ".rdd-instance" / "specifications" / "requirements.md"
    tech_file = temp_repo / ".rdd-instance" / "specifications" / "technical-design.json"
    
    # Run seed script
    result = run_seed_script(temp_repo)
    
    # Check exit code
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    
    # Verify files were created
    assert req_file.exists()
    assert tech_file.exists()
    
    # Verify content is valid
    req_content = req_file.read_text()
    assert "Product Name" in req_content
    assert "User Requirements" in req_content
    
    # Verify JSON is valid
    tech_content = tech_file.read_text()
    json.loads(tech_content)  # Should not raise exception
    
    # Check output mentions file creation
    assert "files created" in result.stdout.lower()


def test_skips_existing_files(temp_repo, minimal_manifest):
    """Verify the script does not overwrite existing files"""
    # Create a file with custom content
    req_file = temp_repo / ".rdd-instance" / "specifications" / "requirements.md"
    req_file.parent.mkdir(parents=True, exist_ok=True)
    custom_content = "# My Custom Requirements\n\nDo not overwrite this!"
    req_file.write_text(custom_content)
    
    # Run seed script
    result = run_seed_script(temp_repo)
    
    # Check exit code
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    
    # Verify content was preserved
    assert req_file.read_text() == custom_content
    
    # Check output mentions skipped files
    assert "skipped" in result.stdout.lower()


def test_validates_json_files(temp_repo, minimal_manifest):
    """Verify JSON files are validated after creation"""
    # Run seed script
    result = run_seed_script(temp_repo, verbose=True)
    
    # Check exit code
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    
    # Verify technical-design.json is valid
    tech_file = temp_repo / ".rdd-instance" / "specifications" / "technical-design.json"
    assert tech_file.exists()
    
    content = tech_file.read_text()
    data = json.loads(content)  # Should not raise exception
    assert isinstance(data, dict)


def test_idempotent_behavior(temp_repo, minimal_manifest):
    """Verify running the script twice produces the same result (idempotent)"""
    # Run seed script first time
    result1 = run_seed_script(temp_repo)
    assert result1.returncode == 0
    
    # Record file modification times
    req_file = temp_repo / ".rdd-instance" / "specifications" / "requirements.md"
    tech_file = temp_repo / ".rdd-instance" / "specifications" / "technical-design.json"
    
    req_mtime1 = req_file.stat().st_mtime
    tech_mtime1 = tech_file.stat().st_mtime
    
    req_content1 = req_file.read_text()
    tech_content1 = tech_file.read_text()
    
    # Run seed script second time
    result2 = run_seed_script(temp_repo)
    assert result2.returncode == 0
    
    # Verify files were not modified
    assert req_file.stat().st_mtime == req_mtime1
    assert tech_file.stat().st_mtime == tech_mtime1
    
    assert req_file.read_text() == req_content1
    assert tech_file.read_text() == tech_content1
    
    # Second run should report all files as skipped (0 created, 3 skipped)
    assert "0 files created" in result2.stdout
    assert "3 files skipped" in result2.stdout


def test_expected_log_output(temp_repo, minimal_manifest):
    """Verify the script produces expected INFO level log messages"""
    # Run seed script
    result = run_seed_script(temp_repo)
    
    # Check exit code
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    
    # Verify output format
    output = result.stdout
    
    # Should have summary line
    assert "Seed complete:" in output
    assert "folders created" in output
    assert "files created" in output
    assert "files skipped" in output


def test_fails_on_missing_manifest(temp_repo):
    """Verify the script fails with exit code 1 when manifest.json is missing"""
    # Don't create manifest.json (skip minimal_manifest fixture)
    
    # Create convention files so those don't cause failure
    (temp_repo / ".rdd" / "conventions").mkdir(parents=True, exist_ok=True)
    (temp_repo / ".rdd" / "conventions" / "requirements.convention.md").write_text("# Convention\n")
    
    # Run seed script
    result = run_seed_script(temp_repo)
    
    # Check exit code is 1
    assert result.returncode == 1
    
    # Check error message mentions manifest
    output = result.stdout + result.stderr
    assert "manifest" in output.lower()


def test_fails_on_malformed_manifest(temp_repo):
    """Verify the script fails with exit code 1 when manifest.json is malformed"""
    # Create malformed manifest
    manifest_path = temp_repo / ".rdd" / "config" / "manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text("{ invalid json ]")
    
    # Run seed script
    result = run_seed_script(temp_repo)
    
    # Check exit code is 1
    assert result.returncode == 1
    
    # Check error message mentions malformed/syntax
    output = result.stdout + result.stderr
    assert "malformed" in output.lower() or "json" in output.lower()


def test_fails_on_missing_convention_file(temp_repo, minimal_manifest):
    """Verify the script fails with exit code 1 when a referenced convention file is missing"""
    # Delete one convention file
    conv_file = temp_repo / ".rdd" / "conventions" / "requirements.convention.md"
    conv_file.unlink()
    
    # Run seed script
    result = run_seed_script(temp_repo)
    
    # Check exit code is 1
    assert result.returncode == 1
    
    # Check error message mentions convention file
    output = result.stdout + result.stderr
    assert "convention" in output.lower()


def test_verbose_flag(temp_repo, minimal_manifest):
    """Verify the --verbose flag enables DEBUG level logging"""
    # Run with verbose flag
    result = run_seed_script(temp_repo, verbose=True)
    
    # Check exit code
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    
    # Check for DEBUG level messages
    output = result.stdout + result.stderr
    assert "DEBUG:" in output


def test_performance_with_existing_files(temp_repo, minimal_manifest):
    """Verify script completes quickly when all files exist (target: <100ms)"""
    import time
    
    # First run to create all files
    result = run_seed_script(temp_repo)
    assert result.returncode == 0
    
    # Second run with all files existing - measure time
    start_time = time.time()
    result = run_seed_script(temp_repo)
    elapsed_time = time.time() - start_time
    
    assert result.returncode == 0
    
    # Should complete in reasonable time (allowing generous margin for CI/slow systems)
    # Target is <100ms, but allow up to 2 seconds for test reliability
    assert elapsed_time < 2.0, f"Script took {elapsed_time:.3f}s (target: <0.1s, max allowed: 2s)"
