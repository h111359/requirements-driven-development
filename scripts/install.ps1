<#
.SYNOPSIS
    RDD Framework Interactive Installer for Windows
.DESCRIPTION
    Provides visual folder navigation for installation directory selection
.NOTES
    Version: {{VERSION}}
#>

$ErrorActionPreference = 'Stop'
$VERSION = "{{VERSION}}"

# Current navigation state
$script:CurrentDir = ""
$script:SelectedIndex = 0

# Print colored messages
function Write-Success {
    param([string]$Message)
    Write-Host "✓ " -ForegroundColor Green -NoNewline
    Write-Host $Message
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "✗ " -ForegroundColor Red -NoNewline
    Write-Host $Message
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ " -ForegroundColor Blue -NoNewline
    Write-Host $Message
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ " -ForegroundColor Yellow -NoNewline
    Write-Host $Message
}

function Write-Banner {
    Clear-Host
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗"
    Write-Host "║      RDD Framework Interactive Installer v$VERSION           ║"
    Write-Host "╚════════════════════════════════════════════════════════════╝"
    Write-Host ""
}

# Check prerequisites
function Test-Prerequisites {
    Write-Info "Checking prerequisites..."
    
    # Check Python
    try {
        $pythonVersion = & python --version 2>&1
        if ($LASTEXITCODE -ne 0) { throw }
        Write-Success "Python detected: $pythonVersion"
    }
    catch {
        Write-ErrorMsg "Python is not installed or not in PATH"
        Write-ErrorMsg "Install Python 3.7+ from: https://www.python.org/downloads/"
        exit 1
    }
    
    # Check Git
    try {
        $gitVersion = & git --version 2>&1
        if ($LASTEXITCODE -ne 0) { throw }
        Write-Success "$gitVersion detected"
    }
    catch {
        Write-ErrorMsg "Git is not installed or not in PATH"
        Write-ErrorMsg "Install Git from: https://git-scm.com/downloads/"
        exit 1
    }
    
    Write-Host ""
}

# Navigate folders with visual menu
function Start-FolderNavigation {
    param([string]$StartDir)
    
    $script:CurrentDir = (Resolve-Path $StartDir).Path
    $script:SelectedIndex = 0
    
    while ($true) {
        # Get list of directories
        $dirs = @()
        
        # Add parent directory option if not at root
        $parent = Split-Path -Parent $script:CurrentDir
        if ($parent) {
            $dirs += ".."
        }
        
        # Add "select this" option
        $dirs += "."
        
        # Add subdirectories (only directories, sorted)
        try {
            $subdirs = Get-ChildItem -Path $script:CurrentDir -Directory -ErrorAction SilentlyContinue | 
                       Sort-Object Name | 
                       Select-Object -ExpandProperty Name
            if ($subdirs) {
                $dirs += $subdirs
            }
        }
        catch {
            # Ignore errors (permission denied, etc.)
        }
        
        # Ensure selected index is in bounds
        if ($script:SelectedIndex -lt 0) {
            $script:SelectedIndex = 0
        }
        if ($script:SelectedIndex -ge $dirs.Count) {
            $script:SelectedIndex = $dirs.Count - 1
        }
        
        # Draw menu
        Show-Menu -Dirs $dirs
        
        # Get user input
        $key = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        
        switch ($key.VirtualKeyCode) {
            38 {  # Up arrow
                $script:SelectedIndex--
                if ($script:SelectedIndex -lt 0) {
                    $script:SelectedIndex = 0
                }
            }
            40 {  # Down arrow
                $script:SelectedIndex++
                if ($script:SelectedIndex -ge $dirs.Count) {
                    $script:SelectedIndex = $dirs.Count - 1
                }
            }
            13 {  # Enter
                $selected = $dirs[$script:SelectedIndex]
                if ($selected -eq "..") {
                    # Go to parent directory
                    $parent = Split-Path -Parent $script:CurrentDir
                    if ($parent) {
                        $script:CurrentDir = $parent
                        $script:SelectedIndex = 0
                    }
                }
                elseif ($selected -eq ".") {
                    # Select current directory
                    return $script:CurrentDir
                }
                else {
                    # Enter subdirectory
                    $script:CurrentDir = Join-Path $script:CurrentDir $selected
                    $script:SelectedIndex = 0
                }
            }
            81 {  # Q key
                Write-Host ""
                Write-Info "Installation cancelled by user"
                exit 0
            }
        }
    }
}

# Draw the navigation menu
function Show-Menu {
    param([array]$Dirs)
    
    Clear-Host
    Write-Banner
    
    Write-Host "Select Installation Directory" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Current: " -NoNewline
    Write-Host $script:CurrentDir -ForegroundColor White
    Write-Host ""
    Write-Host "┌────────────────────────────────────────────────────────────┐"
    
    $index = 0
    foreach ($dir in $Dirs) {
        $displayName = if ($dir -eq "..") {
            "[..] Parent Directory"
        }
        elseif ($dir -eq ".") {
            "[SELECT THIS DIRECTORY]"
        }
        else {
            "$dir\"
        }
        
        if ($index -eq $script:SelectedIndex) {
            Write-Host "│ " -NoNewline
            Write-Host "▶ " -ForegroundColor Green -NoNewline
            Write-Host $displayName -ForegroundColor White
        }
        else {
            Write-Host "│   $displayName"
        }
        
        $index++
    }
    
    Write-Host "└────────────────────────────────────────────────────────────┘"
    Write-Host ""
    Write-Host "Use " -ForegroundColor Cyan -NoNewline
    Write-Host "↑↓" -ForegroundColor White -NoNewline
    Write-Host " arrow keys to navigate, " -ForegroundColor Cyan -NoNewline
    Write-Host "Enter" -ForegroundColor White -NoNewline
    Write-Host " to select, " -ForegroundColor Cyan -NoNewline
    Write-Host "Q" -ForegroundColor White -NoNewline
    Write-Host " to quit" -ForegroundColor Cyan
}

# Validate git repository
function Test-GitRepository {
    param([string]$TargetDir)
    
    Write-Info "Checking if $TargetDir is a Git repository..."
    
    $gitDir = Join-Path $TargetDir ".git"
    if (-not (Test-Path $gitDir)) {
        Write-Host ""
        Write-ErrorMsg "Selected directory is not a Git repository"
        Write-Info "Initialize with: cd $TargetDir; git init"
        Write-Host ""
        Read-Host "Press Enter to continue"
        return $false
    }
    
    Write-Success "Git repository confirmed"
    return $true
}

# Confirm installation
function Confirm-Installation {
    param([string]$TargetDir)
    
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗"
    Write-Host "║                    Installation Summary                    ║"
    Write-Host "╚════════════════════════════════════════════════════════════╝"
    Write-Host ""
    Write-Host "Target Directory: " -NoNewline
    Write-Host $TargetDir -ForegroundColor White
    Write-Host "RDD Version: " -NoNewline
    Write-Host "v$VERSION" -ForegroundColor White
    Write-Host ""
    
    # Check for existing installation
    $existingRdd = Join-Path $TargetDir ".rdd\scripts\rdd.py"
    if (Test-Path $existingRdd) {
        Write-Warning "Existing RDD installation detected - will be OVERWRITTEN"
        Write-Host ""
    }
    
    $response = Read-Host "Proceed with installation? [y/N]"
    
    if ($response -notmatch '^[Yy]$') {
        Write-Info "Installation cancelled by user"
        exit 0
    }
}

# Run Python installer
function Invoke-PythonInstaller {
    param(
        [string]$SourceDir,
        [string]$TargetDir
    )
    
    Write-Host ""
    Write-Info "Running Python installer..."
    Write-Host ""
    
    Set-Location $TargetDir
    
    # Run Python installer with input redirection
    $installerPath = Join-Path $SourceDir "install.py"
    $inputData = "`n`n"  # Two enters for default target directory
    $inputData | & python $installerPath
    
    $exitCode = $LASTEXITCODE
    
    if ($exitCode -eq 0) {
        Write-Host ""
        Write-Host "╔════════════════════════════════════════════════════════════╗"
        Write-Host "║              Installation Completed Successfully!          ║"
        Write-Host "╚════════════════════════════════════════════════════════════╝"
        Write-Host ""
        Write-Success "RDD Framework v$VERSION installed to: $TargetDir"
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor White
        Write-Host "  1. Restart VS Code"
        Write-Host "  2. Create your first change:"
        Write-Host "     cd $TargetDir" -ForegroundColor Cyan
        Write-Host "     python .rdd\scripts\rdd.py change create enh my-feature" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Documentation: https://github.com/h111359/requirements-driven-development"
        Write-Host ""
    }
    else {
        Write-Host ""
        Write-ErrorMsg "Installation failed with exit code: $exitCode"
        exit $exitCode
    }
}

# Main execution
function Main {
    # Get source directory (where this script is located)
    $sourceDir = $PSScriptRoot
    
    # Prerequisites check
    Test-Prerequisites
    
    # Navigate to select installation directory
    Write-Info "Starting folder navigation..."
    Write-Info "Navigate with arrow keys, press Enter to select"
    Write-Host ""
    Start-Sleep -Seconds 2
    
    $targetDir = Start-FolderNavigation -StartDir (Get-Location).Path
    
    # Validate git repository
    while (-not (Test-GitRepository -TargetDir $targetDir)) {
        Write-Host ""
        $response = Read-Host "Try selecting a different directory? [Y/n]"
        
        if ($response -match '^[Nn]$') {
            Write-Info "Installation cancelled by user"
            exit 0
        }
        
        $targetDir = Start-FolderNavigation -StartDir $targetDir
    }
    
    # Confirm installation
    Confirm-Installation -TargetDir $targetDir
    
    # Run Python installer
    Invoke-PythonInstaller -SourceDir $sourceDir -TargetDir $targetDir
}

# Run main function
Main
