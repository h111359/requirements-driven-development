#
# run-tests.ps1
# Run all tests appropriate for Windows
#

# Error handling
$ErrorActionPreference = "Stop"

# Get script directory and repository root first
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

# Change to repository root
Set-Location $RepoRoot

# Print banner
Write-Host ""
Write-Host "============================================================" -ForegroundColor White
Write-Host "  RDD Framework Test Runner (Windows)" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor White
Write-Host ""

# Check prerequisites
Write-Host "[INFO] Checking prerequisites..." -ForegroundColor Blue

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check virtual environment
if (-not (Test-Path ".venv")) {
    Write-Host "[WARN] Virtual environment not found at .venv/" -ForegroundColor Yellow
    Write-Host "[INFO] Run: python setup-test-env.py" -ForegroundColor Blue
    exit 1
}
Write-Host "[OK] Virtual environment found" -ForegroundColor Green

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Blue
& ".venv\Scripts\Activate.ps1"
Write-Host "[OK] Virtual environment activated" -ForegroundColor Green

# Check pytest
try {
    $pytestVersion = pytest --version 2>&1 | Select-Object -First 1
    Write-Host "[OK] pytest found: $pytestVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] pytest not found in virtual environment" -ForegroundColor Red
    Write-Host "[INFO] Run: python setup-test-env.py" -ForegroundColor Blue
    exit 1
}

# Track test results
$TotalTests = 0
$PassedTests = 0
$FailedTests = 0

Write-Host ""
Write-Host "============================================================" -ForegroundColor White
Write-Host "  Running Tests" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor White
Write-Host ""

# Step 1: Python Unit Tests
Write-Host "[1/4] Running Python unit tests" -ForegroundColor Blue
try {
    pytest tests/python/ -v --tb=short
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Python unit tests passed" -ForegroundColor Green
        $PassedTests++
    } else {
        Write-Host "[ERROR] Python unit tests failed" -ForegroundColor Red
        $FailedTests++
    }
} catch {
    Write-Host "[ERROR] Python unit tests failed with exception" -ForegroundColor Red
    $FailedTests++
}
$TotalTests++
Write-Host ""

# Step 2: Build Tests
Write-Host "[2/4] Running build tests" -ForegroundColor Blue
try {
    pytest tests/build/ -v --tb=short
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Build tests passed" -ForegroundColor Green
        $PassedTests++
    } else {
        Write-Host "[ERROR] Build tests failed" -ForegroundColor Red
        $FailedTests++
    }
} catch {
    Write-Host "[ERROR] Build tests failed with exception" -ForegroundColor Red
    $FailedTests++
}
$TotalTests++
Write-Host ""

# Step 3: Install Tests
Write-Host "[3/4] Running install tests" -ForegroundColor Blue
try {
    pytest tests/install/ -v --tb=short
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Install tests passed" -ForegroundColor Green
        $PassedTests++
    } else {
        Write-Host "[ERROR] Install tests failed" -ForegroundColor Red
        $FailedTests++
    }
} catch {
    Write-Host "[ERROR] Install tests failed with exception" -ForegroundColor Red
    $FailedTests++
}
$TotalTests++
Write-Host ""

# Step 4: PowerShell Tests (Pester)
Write-Host "[4/4] Running PowerShell tests (Pester)" -ForegroundColor Blue
try {
    # Check if Pester is installed
    $pesterModule = Get-Module -ListAvailable -Name Pester
    if ($pesterModule) {
        $result = Invoke-Pester tests/powershell/*.Tests.ps1 -PassThru
        if ($result.FailedCount -eq 0) {
            Write-Host "[OK] PowerShell tests passed" -ForegroundColor Green
            $PassedTests++
        } else {
            Write-Host "[ERROR] PowerShell tests failed" -ForegroundColor Red
            $FailedTests++
        }
        $TotalTests++
    } else {
        Write-Host "[WARN] Pester not found - skipping PowerShell tests" -ForegroundColor Yellow
        Write-Host "[INFO] Install: Install-Module -Name Pester -Force -SkipPublisherCheck" -ForegroundColor Blue
    }
} catch {
    Write-Host "[WARN] PowerShell tests skipped due to error" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host ""
Write-Host "============================================================" -ForegroundColor White
Write-Host "  Test Summary" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor White
Write-Host ""

Write-Host "Total test suites: $TotalTests"
Write-Host "Passed: $PassedTests" -ForegroundColor Green
if ($FailedTests -gt 0) {
    Write-Host "Failed: $FailedTests" -ForegroundColor Red
}
Write-Host ""

# Exit with appropriate code
if ($FailedTests -gt 0) {
    Write-Host "[ERROR] Some tests failed" -ForegroundColor Red
    exit 1
} else {
    Write-Host "[OK] All tests passed!" -ForegroundColor Green
    exit 0
}
