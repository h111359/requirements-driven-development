#
# run-tests.ps1
# Run all tests appropriate for Windows
#

# Print functions must be defined before ErrorActionPreference to ensure they're available
function Global:Print-Header {
    param([string]$Message)
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor White
    Write-Host "  $Message" -ForegroundColor White
    Write-Host "============================================================" -ForegroundColor White
    Write-Host ""
}

function Global:Print-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Global:Print-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Global:Print-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Blue
}

function Global:Print-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Global:Print-Step {
    param(
        [int]$Current,
        [int]$Total,
        [string]$Message
    )
    Write-Host "[$Current/$Total] $Message" -ForegroundColor Blue
}

# Error handling - set AFTER functions are defined
$ErrorActionPreference = "Stop"

# Get script directory and repository root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

# Change to repository root
Set-Location $RepoRoot

# Print banner
Print-Header "RDD Framework Test Runner (Windows)"

# Check prerequisites
Print-Info "Checking prerequisites..."

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Print-Success "Python found: $pythonVersion"
} catch {
    Print-Error "Python is not installed or not in PATH"
    exit 1
}

# Check virtual environment
if (-not (Test-Path ".venv")) {
    Print-Warning "Virtual environment not found at .venv/"
    Print-Info "Run: python setup-test-env.py"
    exit 1
}
Print-Success "Virtual environment found"

# Activate virtual environment
Print-Info "Activating virtual environment..."
& ".venv\Scripts\Activate.ps1"
Print-Success "Virtual environment activated"

# Check pytest
try {
    $pytestVersion = pytest --version 2>&1 | Select-Object -First 1
    Print-Success "pytest found: $pytestVersion"
} catch {
    Print-Error "pytest not found in virtual environment"
    Print-Info "Run: python setup-test-env.py"
    exit 1
}

# Track test results
$TotalTests = 0
$PassedTests = 0
$FailedTests = 0

Write-Host ""
Print-Header "Running Tests"

# Step 1: Python Unit Tests
Print-Step 1 4 "Running Python unit tests"
try {
    pytest tests/python/ -v --tb=short
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Python unit tests passed"
        $PassedTests++
    } else {
        Print-Error "Python unit tests failed"
        $FailedTests++
    }
} catch {
    Print-Error "Python unit tests failed with exception"
    $FailedTests++
}
$TotalTests++
Write-Host ""

# Step 2: Build Tests
Print-Step 2 4 "Running build tests"
try {
    pytest tests/build/ -v --tb=short
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Build tests passed"
        $PassedTests++
    } else {
        Print-Error "Build tests failed"
        $FailedTests++
    }
} catch {
    Print-Error "Build tests failed with exception"
    $FailedTests++
}
$TotalTests++
Write-Host ""

# Step 3: Install Tests
Print-Step 3 4 "Running install tests"
try {
    pytest tests/install/ -v --tb=short
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Install tests passed"
        $PassedTests++
    } else {
        Print-Error "Install tests failed"
        $FailedTests++
    }
} catch {
    Print-Error "Install tests failed with exception"
    $FailedTests++
}
$TotalTests++
Write-Host ""

# Step 4: PowerShell Tests (Pester)
Print-Step 4 4 "Running PowerShell tests (Pester)"
try {
    # Check if Pester is installed
    $pesterModule = Get-Module -ListAvailable -Name Pester
    if ($pesterModule) {
        $result = Invoke-Pester tests/powershell/*.Tests.ps1 -PassThru
        if ($result.FailedCount -eq 0) {
            Print-Success "PowerShell tests passed"
            $PassedTests++
        } else {
            Print-Error "PowerShell tests failed"
            $FailedTests++
        }
        $TotalTests++
    } else {
        Print-Warning "Pester not found - skipping PowerShell tests"
        Print-Info "Install: Install-Module -Name Pester -Force -SkipPublisherCheck"
    }
} catch {
    Print-Warning "PowerShell tests skipped due to error"
}
Write-Host ""

# Summary
Print-Header "Test Summary"

Write-Host "Total test suites: $TotalTests"
Write-Host "Passed: $PassedTests" -ForegroundColor Green
if ($FailedTests -gt 0) {
    Write-Host "Failed: $FailedTests" -ForegroundColor Red
}
Write-Host ""

# Exit with appropriate code
if ($FailedTests -gt 0) {
    Print-Error "Some tests failed"
    exit 1
} else {
    Print-Success "All tests passed!"
    exit 0
}
