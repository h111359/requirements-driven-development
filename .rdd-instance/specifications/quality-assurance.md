## Testing Infrastructure

### Test Organization

The framework includes a comprehensive testing suite organized by test type:

```
tests/
├── python/              # Python script tests (pytest)
│   ├── test_rdd_main.py       # Main entry point tests
│   ├── test_rdd_utils.py      # Utility function tests
│   ├── test_integration.py    # Integration tests
│   └── conftest.py            # Pytest fixtures
├── build/               # Build script tests
│   ├── test_build.py          # Build system tests
│   └── conftest.py            # Build fixtures
├── install/             # Installation tests
│   ├── test_install.py        # Installer tests
│   └── conftest.py            # Install fixtures
├── fixtures/            # Shared test fixtures
│   └── README.md              # Fixtures documentation
├── requirements.txt     # Test dependencies
└── README.md            # Testing documentation
```

### Test Frameworks

- **Python Tests**: pytest with pytest-cov for coverage reporting
- **Test Coverage**: 80+ tests covering all framework scripts
- **Pass Rate**: 100% (all Python tests passing)

### Test Isolation

All tests use isolation mechanisms to prevent corruption of existing code:
- **Temporary directories**: Each test creates and cleans up temp dirs
- **Mock git repositories**: Fresh git repos for each test
- **Subprocess mocking**: Git commands mocked where appropriate
- **No side effects**: Tests don't modify actual project files
- **Parallel safe**: Tests can run concurrently without conflicts

### Virtual Environment

The framework provides automated virtual environment setup for test execution:
- **Script**: `scripts/setup-test-env.py` creates `.venv/` directory
- **Smart handling**: Preserves existing environment, only updates packages
- **Test dependencies**: pytest, pytest-cov, pytest-mock, pytest-timeout, pytest-xdist
- **Build exclusion**: .venv/ excluded from release archives
- **CI/CD isolation**: GitHub Actions creates fresh environments per run

### Test Runner Scripts

The framework provides a unified Python-based test runner:

**Python Test Runner (scripts/run-tests.py)**:
- Cross-platform test execution (Windows, Linux, macOS)
- Color-coded output for readability
- Progress indicators
- Prerequisites checking
- Virtual environment activation
- Runs pytest for Python, build, and install tests
- Clear test summary with pass/fail counts
- Exit code reflects test success/failure

**Usage**:
```bash
python scripts/run-tests.py
```

### GitHub Actions CI/CD

Automated testing on push and pull requests:
- **Python version**: Python 3.9+ (expandable to matrix)
- **Test execution**: Uses `python scripts/run-tests.py` for unified cross-platform testing
- **Code coverage**: Coverage report generated during test run
- **Test summary**: Aggregated results with pass/fail status

### Test Coverage

**Current Coverage**:
- **rdd.py**: CLI routing, domain handlers, interactive menus
- **rdd_utils.py**: All utility functions (git, branch, workdir, config)
- **build.py**: Version extraction, archive creation, checksums
- **install.py**: Pre-flight checks, file operations, settings merge
- **run-tests.py**: Test runner, virtual environment activation, cross-platform execution


