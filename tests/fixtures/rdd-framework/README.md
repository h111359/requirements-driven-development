# RDD Framework Test Fixtures

This directory contains test fixtures for RDD framework tests organized with realistic but minimal data sets.

## Purpose

Test fixtures provide sample data for testing framework components without requiring full production setups. They enable:

- Isolated testing with known data states
- Reproducible test scenarios
- Fast test execution without complex setup

## Structure

### sample-registry.json
Sample work-iteration-registry.json with varied prompt states:
- One completed prompt with full workflow (questionnaire, plan, implementation)
- One active prompt in clarify mode (questionnaire generated but not answered)
- One completed prompt with minimal workflow (no artifacts)

Used for testing:
- Registry parsing and validation
- Prompt state queries
- Workflow flag checking

### sample-requirements.md
Sample requirements.md file with both UR and TR requirements:
- 3 User Requirements (UR-0001 through UR-0003)
- 3 Technical Requirements (TR-0001 through TR-0003)

Used for testing:
- Requirement ID parsing
- Auto-increment logic
- File format preservation
- CRUD operations

### sample-manifest.json
Valid manifest configuration for validation tests with:
- Framework metadata (name, version)
- RDD instance configuration (required paths and files)
- Prompt snippet mappings

Used for testing:
- Manifest schema validation
- Path verification logic
- Snippet resolution
- Version extraction

## Usage Guidelines

1. **Minimal data**: Fixtures include only essential data for testing
2. **Realistic structure**: Follow actual production file formats
3. **No sensitive data**: All data is generic and safe for version control
4. **Documented purpose**: Each fixture's purpose is documented above
5. **Maintenance**: Update fixtures when framework structure changes

## Test Coverage

These fixtures support testing of:
- Action scripts (prompt management, requirements, workflow)
- Configuration validation
- Integration workflows
- Registry operations
- File format compliance
