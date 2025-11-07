# Test Fixtures

This directory contains shared test data and fixtures for RDD framework tests.

## Contents

- **`sample_repo/`** - Sample git repository structure for testing
- **`test_configs/`** - Test configuration files
- **`mock_data/`** - Mock data for testing (requirements, changes, etc.)

## Usage

Fixtures are automatically loaded by pytest through the `conftest.py` files in each test directory.

## Adding New Fixtures

1. Create fixture data in appropriate subdirectory
2. Add fixture function in relevant `conftest.py`
3. Document fixture purpose and usage

## Isolation

All fixtures should:
- Use temporary directories
- Clean up after themselves
- Not modify actual project files
- Be idempotent (can run multiple times)
