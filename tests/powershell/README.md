# PowerShell Script Tests

Tests for PowerShell installation script (`install.ps1`).

## Prerequisites

### Windows
```powershell
# Install Pester
Install-Module -Name Pester -Force -SkipPublisherCheck

# Update Pester to latest version
Update-Module -Name Pester
```

### Check Pester Installation
```powershell
Get-Module -ListAvailable Pester
```

## Running Tests

```powershell
# Run all PowerShell tests
Invoke-Pester tests/powershell/Install.Tests.ps1

# Run with detailed output
Invoke-Pester tests/powershell/Install.Tests.ps1 -Output Detailed

# Run specific test
Invoke-Pester tests/powershell/Install.Tests.ps1 -TestName "Install.ps1 exists"

# Generate code coverage
Invoke-Pester tests/powershell/Install.Tests.ps1 -CodeCoverage scripts/install.ps1
```

## Test Structure

The Pester tests verify:
- Interactive folder navigation
- Git repository validation
- Directory selection  
- Error handling
- Windows-specific functionality

## Test Isolation

- Tests run in isolated temporary directories
- Mock objects used for external dependencies
- No modifications to actual installation

## Limitations

- Interactive menu testing requires mocking
- Some Windows-specific features may not translate to Linux
- User input simulation has constraints

## References

- [Pester Documentation](https://pester.dev/)
- [Pester GitHub](https://github.com/pester/Pester)
- [PowerShell Testing Guide](https://docs.microsoft.com/en-us/powershell/scripting/dev-cross-plat/writing-portable-modules)
