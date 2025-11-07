# Shell Script Tests

Tests for Bash installation script (`install.sh`).

## Prerequisites

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install bats
```

### macOS
```bash
brew install bats-core
```

### Fedora/RHEL
```bash
sudo dnf install bats
```

## Running Tests

```bash
# Run all shell tests
bats tests/shell/test_install_sh.bats

# Run with verbose output
bats tests/shell/test_install_sh.bats --verbose

# Run specific test
bats tests/shell/test_install_sh.bats --filter "test_folder_navigation"
```

## Test Structure

The BATS tests verify:
- Interactive folder navigation
- Git repository validation
- Directory selection
- Error handling
- Cross-platform compatibility

## Limitations

- Interactive menu testing is limited
- Tests run in isolated temporary directories
- Some user interaction must be mocked

## References

- [BATS Documentation](https://bats-core.readthedocs.io/)
- [BATS GitHub](https://github.com/bats-core/bats-core)
