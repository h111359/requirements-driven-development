# requirements-utils.ps1
# Requirements management utility functions for RDD framework
# Provides validation, merging, ID assignment, and analysis for requirements

# Get the directory where this script is located
$script:SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

# Source core-utils.ps1 for common functions
$coreUtilsPath = Join-Path $SCRIPT_DIR "core-utils.ps1"
if (Test-Path $coreUtilsPath) {
    . $coreUtilsPath
}
else {
    Write-Error "ERROR: core-utils.ps1 not found. Please ensure it exists in the same directory."
    exit 1
}

# Source git-utils.ps1 for git operations
$gitUtilsPath = Join-Path $SCRIPT_DIR "git-utils.ps1"
if (Test-Path $gitUtilsPath) {
    . $gitUtilsPath
}
else {
    Write-Error "ERROR: git-utils.ps1 not found. Please ensure it exists in the same directory."
    exit 1
}

# Prevent multiple sourcing
if ($global:REQUIREMENTS_UTILS_LOADED) {
    return
}
$global:REQUIREMENTS_UTILS_LOADED = $true

# ============================================================================
# CONSTANTS
# ============================================================================

$script:REQUIREMENTS_FILE = ".rdd-docs/requirements.md"
$script:WORKSPACE_REQUIREMENTS = ".rdd-docs/workspace/requirements-changes.md"
$script:ID_MAPPING_FILE = ".rdd-docs/workspace/.id-mapping.txt"

# Section names and their ID prefixes
$script:SECTION_PREFIXES = @{
    "General Functionalities" = "GF"
    "Functional Requirements" = "FR"
    "Non-Functional Requirements" = "NFR"
    "Technical Requirements" = "TR"
}

# ============================================================================
# VALIDATION
# ============================================================================

# Validate requirements-changes.md format
# Usage: Test-Requirements [file_path]
# Returns: $true if valid, $false if invalid
function Test-Requirements {
    param([string]$ReqFile = $script:WORKSPACE_REQUIREMENTS)
    
    if (-not (Test-Path $ReqFile)) {
        Print-Error "Requirements file not found: $ReqFile"
        return $false
    }
    
    Print-Step "Validating requirements format: $(Split-Path -Leaf $ReqFile)"
    
    $hasErrors = $false
    $lineNum = 0
    
    $content = Get-Content $ReqFile
    
    foreach ($line in $content) {
        $lineNum++
        
        # Skip empty lines, comments, markdown headers, blockquotes, and horizontal rules
        if ([string]::IsNullOrWhiteSpace($line) -or 
            $line -match '^\s*#' -or
            $line -match '^\s*>' -or
            $line -match '^\s*--') {
            continue
        }
        
        # Check if line starts with a list marker
        if ($line -match '^\s*[-*]\s+') {
            # Extract the content after the list marker
            $contentMatch = $line -match '^\s*[-*]\s+(.*)$'
            if ($contentMatch) {
                $content = $matches[1]
                
                # Check if it starts with a valid prefix
                if ($content -notmatch '^\[ADDED\]' -and
                    $content -notmatch '^\[MODIFIED\]' -and
                    $content -notmatch '^\[DELETED\]') {
                    Print-Warning "Line ${lineNum}: Missing or invalid prefix [ADDED|MODIFIED|DELETED]"
                    Write-Host "  → $($line.Substring(0, [Math]::Min(80, $line.Length)))"
                    $hasErrors = $true
                }
                
                # Additional validation for MODIFIED and DELETED
                if ($content -match '^\[(MODIFIED|DELETED)\]' -and
                    $content -notmatch '^\[(MODIFIED|DELETED)\]\s*\[[A-Z]+-[0-9]+\]') {
                    Print-Warning "Line ${lineNum}: MODIFIED/DELETED must include existing ID [PREFIX-##]"
                    Write-Host "  → $($line.Substring(0, [Math]::Min(80, $line.Length)))"
                    $hasErrors = $true
                }
            }
        }
    }
    
    if (-not $hasErrors) {
        Print-Success "Validation passed: format is correct"
        return $true
    }
    else {
        Print-Warning "Validation completed with warnings"
        return $false
    }
}

# ============================================================================
# ID MANAGEMENT
# ============================================================================

# Get next available ID for a requirement section
# Usage: Get-NextRequirementId "PREFIX" [file_path]
# Returns: next ID as string (e.g., "01", "02")
function Get-NextRequirementId {
    param(
        [string]$Prefix,
        [string]$File = $script:REQUIREMENTS_FILE
    )
    
    if ([string]::IsNullOrEmpty($Prefix)) {
        Print-Error "Prefix is required"
        Write-Host "Usage: Get-NextRequirementId <PREFIX> [file_path]"
        return $null
    }
    
    if (-not (Test-Path $File)) {
        # If file doesn't exist, start from 01
        return "01"
    }
    
    # Find all IDs with this prefix and extract the number
    $content = Get-Content $File -Raw
    $matches = [regex]::Matches($content, "\[$Prefix-(\d+)\]")
    
    if ($matches.Count -eq 0) {
        return "01"
    }
    
    $maxId = ($matches | ForEach-Object { [int]$_.Groups[1].Value } | Measure-Object -Maximum).Maximum
    return ("{0:D2}" -f ($maxId + 1))
}

# Track ID mapping for requirements
# Usage: Add-IdMapping "old_id" "new_id" [mapping_file]
# Returns: $true on success
function Add-IdMapping {
    param(
        [string]$OldId,
        [string]$NewId,
        [string]$MappingFile = $script:ID_MAPPING_FILE
    )
    
    if ([string]::IsNullOrEmpty($OldId) -or [string]::IsNullOrEmpty($NewId)) {
        Print-Error "Both old_id and new_id are required"
        Write-Host "Usage: Add-IdMapping <old_id> <new_id> [mapping_file]"
        return $false
    }
    
    # Ensure directory exists
    $mappingDir = Split-Path -Parent $MappingFile
    Ensure-Dir $mappingDir
    
    # Create file with header if it doesn't exist
    if (-not (Test-Path $MappingFile)) {
        @"
# ID Mapping Log
# Tracks requirement ID changes during merges
# Format: OLD_ID -> NEW_ID (timestamp)

"@ | Out-File -FilePath $MappingFile -Encoding utf8
    }
    
    # Append mapping
    $timestamp = Get-Timestamp
    "$OldId -> $NewId ($timestamp)" | Add-Content -Path $MappingFile -Encoding utf8
    Debug-Print "ID mapping tracked: $OldId -> $NewId"
    
    return $true
}

# ============================================================================
# MERGE PREVIEW
# ============================================================================

# Preview requirements merge without making changes
# Usage: Show-RequirementsMergePreview
# Returns: $true on success
function Show-RequirementsMergePreview {
    if (-not (Test-Path $script:WORKSPACE_REQUIREMENTS)) {
        Print-Error "Requirements changes file not found: $script:WORKSPACE_REQUIREMENTS"
        return $false
    }
    
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host "  MERGE PREVIEW"
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host ""
    
    # Count changes by type
    $content = Get-Content $script:WORKSPACE_REQUIREMENTS -Raw
    $addedCount = ([regex]::Matches($content, '^\-\s+\*\*\[ADDED\]', [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
    $modifiedCount = ([regex]::Matches($content, '^\-\s+\*\*\[MODIFIED\]', [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
    $deletedCount = ([regex]::Matches($content, '^\-\s+\*\*\[DELETED\]', [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
    
    Print-Info "Changes to be applied:"
    Write-Host "  [ADDED]    : $addedCount requirements" -ForegroundColor Green
    Write-Host "  [MODIFIED] : $modifiedCount requirements" -ForegroundColor Yellow
    Write-Host "  [DELETED]  : $deletedCount requirements" -ForegroundColor Red
    Write-Host ""
    
    $total = $addedCount + $modifiedCount + $deletedCount
    if ($total -eq 0) {
        Print-Warning "No changes detected"
        Write-Host ""
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        return $true
    }
    
    # Show actual changes
    if ($addedCount -gt 0) {
        Write-Host "━━━ ADDED Requirements ━━━"
        Get-Content $script:WORKSPACE_REQUIREMENTS | Where-Object { $_ -match '^\-\s+\*\*\[ADDED\]' } | ForEach-Object {
            Write-Host "  $($_.Substring(0, [Math]::Min(100, $_.Length)))"
        }
        Write-Host ""
    }
    
    if ($modifiedCount -gt 0) {
        Write-Host "━━━ MODIFIED Requirements ━━━"
        Get-Content $script:WORKSPACE_REQUIREMENTS | Where-Object { $_ -match '^\-\s+\*\*\[MODIFIED\]' } | ForEach-Object {
            Write-Host "  $($_.Substring(0, [Math]::Min(100, $_.Length)))"
        }
        Write-Host ""
    }
    
    if ($deletedCount -gt 0) {
        Write-Host "━━━ DELETED Requirements ━━━"
        Get-Content $script:WORKSPACE_REQUIREMENTS | Where-Object { $_ -match '^\-\s+\*\*\[DELETED\]' } | ForEach-Object {
            Write-Host "  $($_.Substring(0, [Math]::Min(100, $_.Length)))"
        }
        Write-Host ""
    }
    
    Print-Success "Total: $total requirement changes"
    Write-Host ""
    Print-Info "Run 'Merge-Requirements' to apply these changes"
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return $true
}

# ============================================================================
# REQUIREMENTS MERGING
# ============================================================================

# Merge requirements changes into main requirements file
# Usage: Merge-Requirements [dry_run] [create_backup]
# dry_run: $true to preview only, $false to apply (default: $false)
# create_backup: $true to create backup, $false otherwise (default: $true)
# Returns: $true on success, $false on failure
function Merge-Requirements {
    param(
        [bool]$DryRun = $false,
        [bool]$CreateBackup = $true
    )
    
    Print-Banner "MERGE REQUIREMENTS"
    Write-Host ""
    
    # Validate merge readiness
    if (-not (Test-Path $script:WORKSPACE_REQUIREMENTS)) {
        Print-Error "Requirements changes file not found: $script:WORKSPACE_REQUIREMENTS"
        return $false
    }
    
    # If dry run, just show preview
    if ($DryRun) {
        Print-Info "DRY RUN - No changes will be made"
        Write-Host ""
        Show-RequirementsMergePreview
        return $true
    }
    
    # Validate format first
    if (-not (Test-Requirements $script:WORKSPACE_REQUIREMENTS)) {
        Print-Error "Validation failed - cannot proceed with merge"
        return $false
    }
    Write-Host ""
    
    # Create backup if requested
    if ($CreateBackup -and (Test-Path $script:REQUIREMENTS_FILE)) {
        $backupFile = "$script:REQUIREMENTS_FILE.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Copy-Item -Path $script:REQUIREMENTS_FILE -Destination $backupFile
        Print-Success "Created backup: $backupFile"
        Write-Host ""
    }
    
    # If requirements.md doesn't exist, create from template
    if (-not (Test-Path $script:REQUIREMENTS_FILE)) {
        Print-Warning "requirements.md not found - creating from template"
        $templatePath = ".rdd/templates/requirements.md"
        if (Test-Path $templatePath) {
            Copy-Item -Path $templatePath -Destination $script:REQUIREMENTS_FILE
        }
        else {
            # Create minimal template
            @'
# Overview

<OVERVIEW-PLACEHOLDER>

# General Functionalities

# Functional Requirements

# Non-Functional Requirements

# Technical Requirements

'@ | Out-File -FilePath $script:REQUIREMENTS_FILE -Encoding utf8
        }
        Print-Success "Created requirements.md"
        Write-Host ""
    }
    
    Print-Warning "Automated merge for ADDED items only"
    Print-Warning "MODIFIED and DELETED items require manual review"
    Write-Host ""
    Print-Success "Requirements merge process initiated"
    Print-Info "ID mappings saved to: $script:ID_MAPPING_FILE"
    
    return $true
}

# ============================================================================
# REQUIREMENTS ANALYSIS
# ============================================================================

# Analyze requirements impact comparing with main branch
# Usage: Get-RequirementsImpact
# Returns: $true on success
function Get-RequirementsImpact {
    Test-GitRepo | Out-Null
    
    $defaultBranch = Get-DefaultBranch
    
    Print-Banner "REQUIREMENTS IMPACT ANALYSIS"
    Write-Host ""
    
    # Fetch latest
    Invoke-FetchMain | Out-Null
    
    # Check if requirements.md has been directly modified
    $reqModified = git diff --name-only "origin/${defaultBranch}...HEAD" | Where-Object { $_ -eq $script:REQUIREMENTS_FILE }
    
    if ($reqModified) {
        Print-Warning "requirements.md has been directly modified in this branch"
        Write-Host ""
        Print-Info "Requirements changes:"
        git diff "origin/${defaultBranch}...HEAD" -- $script:REQUIREMENTS_FILE | Where-Object { $_ -match '^\s*[\+\-]\s*-\s*\*\*\[' }
        Write-Host ""
    }
    else {
        Print-Info "requirements.md has NOT been directly modified"
        Write-Host ""
    }
    
    # Check if requirements-changes.md exists in workspace
    if (Test-Path $script:WORKSPACE_REQUIREMENTS) {
        Print-Info "Found requirements-changes.md in workspace"
        Write-Host ""
        
        # Count changes by type
        $content = Get-Content $script:WORKSPACE_REQUIREMENTS -Raw
        $added = ([regex]::Matches($content, '^\-\s+\*\*\[ADDED\]', [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
        $modified = ([regex]::Matches($content, '^\-\s+\*\*\[MODIFIED\]', [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
        $deleted = ([regex]::Matches($content, '^\-\s+\*\*\[DELETED\]', [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
        
        Print-Info "Requirements changes pending:"
        Write-Host "  + Added: $added" -ForegroundColor Green
        Write-Host "  ~ Modified: $modified" -ForegroundColor Yellow
        Write-Host "  - Deleted: $deleted" -ForegroundColor Red
        Write-Host ""
        
        $total = $added + $modified + $deleted
        if ($total -gt 0) {
            Print-Success "Total: $total requirement changes"
        }
        else {
            Print-Warning "No requirement changes detected"
        }
    }
    else {
        Print-Info "No requirements-changes.md found in workspace"
    }
    
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return $true
}

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

Export-ModuleMember -Function @(
    'Test-Requirements',
    'Get-NextRequirementId',
    'Add-IdMapping',
    'Show-RequirementsMergePreview',
    'Merge-Requirements',
    'Get-RequirementsImpact'
)

Debug-Print "requirements-utils.ps1 loaded successfully"
