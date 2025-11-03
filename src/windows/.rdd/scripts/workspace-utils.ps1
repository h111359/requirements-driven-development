# workspace-utils.ps1
# Workspace management utility functions for RDD framework
# Provides workspace initialization, archiving, backup/restore, and template management

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
if ($global:WORKSPACE_UTILS_LOADED) {
    return
}
$global:WORKSPACE_UTILS_LOADED = $true

# ============================================================================
# CONSTANTS AND CONFIGURATION
# ============================================================================

$script:WORKSPACE_DIR = ".rdd-docs/workspace"
$script:ARCHIVE_BASE_DIR = ".rdd-docs/archive"
$script:BACKUP_DIR = "$WORKSPACE_DIR/.backups"
$script:TEMPLATES_DIR = ".rdd/templates"

# ============================================================================
# WORKSPACE INITIALIZATION
# ============================================================================

# Initialize workspace with templates based on type (change or fix)
# Usage: Initialize-Workspace "change|fix"
# Returns: $true on success, $false on failure
function Initialize-Workspace {
    param([string]$WorkspaceType = "change")
    
    if ($WorkspaceType -notmatch '^(change|fix)$') {
        Print-Error "Invalid workspace type: $WorkspaceType"
        Print-Info "Valid types: change, fix"
        return $false
    }
    
    Print-Step "Initializing workspace for type: $WorkspaceType..."
    
    # Ensure workspace directory exists
    Ensure-Dir $script:WORKSPACE_DIR
    
    # Copy main template based on type
    if ($WorkspaceType -eq "fix") {
        Copy-Template "fix.md" "$script:WORKSPACE_DIR/fix.md"
    }
    
    # Copy copilot-prompts.md template to workspace with new name
    Copy-Template "copilot-prompts.md" "$script:WORKSPACE_DIR/.rdd.copilot-prompts.md"
    
    Print-Success "Workspace initialized successfully for $WorkspaceType"
    return $true
}

# ============================================================================
# WORKSPACE ARCHIVING
# ============================================================================

# Archive workspace to branch-specific folder
# Usage: Invoke-ArchiveWorkspace "branch_name" [keep_workspace]
# keep_workspace: $true to keep workspace after archiving, $false to remove (default: $false)
# Returns: relative path on success, $null on failure
function Invoke-ArchiveWorkspace {
    param(
        [string]$BranchName,
        [bool]$KeepWorkspace = $false
    )
    
    if ([string]::IsNullOrEmpty($BranchName)) {
        Print-Error "Branch name is required"
        Write-Host "Usage: Invoke-ArchiveWorkspace <branch_name> [keep_workspace]"
        return $null
    }
    
    # Check if workspace exists and has content
    if (-not (Test-Path $script:WORKSPACE_DIR)) {
        Print-Error "Workspace directory does not exist: $script:WORKSPACE_DIR"
        return $null
    }
    
    $workspaceContents = Get-ChildItem $script:WORKSPACE_DIR -ErrorAction SilentlyContinue
    if (-not $workspaceContents) {
        Print-Error "Workspace directory is empty: $script:WORKSPACE_DIR"
        return $null
    }
    
    # Create archive directory named after the branch
    # Remove any slashes and replace with hyphens
    $safeBranchName = $BranchName -replace '[/\\]', '-'
    $archiveDir = Join-Path $script:ARCHIVE_BASE_DIR $safeBranchName
    
    # Check if archive already exists
    if (Test-Path $archiveDir) {
        Print-Warning "Archive directory already exists: $archiveDir"
        if (-not (Confirm-Action "Overwrite existing archive?")) {
            Print-Info "Archive cancelled by user"
            return $null
        }
        Remove-Item -Path $archiveDir -Recurse -Force
    }
    
    # Create archive directory
    New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null
    
    # Copy all files from workspace to archive
    Copy-Item -Path "$script:WORKSPACE_DIR\*" -Destination $archiveDir -Recurse -Force
    
    # Create metadata file
    $gitUser = Get-GitUser
    $lastCommit = Get-LastCommitSha
    $lastMessage = Get-LastCommitMessage
    
    $metadata = @{
        archivedAt = Get-Timestamp
        branch = $BranchName
        archivedBy = $gitUser
        lastCommit = $lastCommit
        lastCommitMessage = $lastMessage
    } | ConvertTo-Json
    
    $metadata | Out-File -FilePath (Join-Path $archiveDir ".archive-metadata") -Encoding utf8
    
    Print-Success "Workspace archived to: $archiveDir"
    
    # Clean up workspace unless keep_workspace is true
    if (-not $KeepWorkspace) {
        Clear-WorkspaceForced
        Print-Info "Workspace directory cleared"
    }
    else {
        Print-Info "Workspace directory kept as requested"
    }
    
    return $archiveDir
}

# ============================================================================
# BACKUP AND RESTORE
# ============================================================================

# Create backup of workspace files with timestamp
# Usage: Backup-Workspace
# Returns: backup path on success, $null on failure
function Backup-Workspace {
    Print-Step "Creating backup of workspace files..."
    
    if (-not (Test-Path $script:WORKSPACE_DIR)) {
        Print-Error "Workspace directory does not exist: $script:WORKSPACE_DIR"
        return $null
    }
    
    # Create backup directory with timestamp
    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backupPath = Join-Path $script:BACKUP_DIR $timestamp
    New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
    
    # Backup key files
    $filesToBackup = @(
        "fix.md",
        "open-questions.md",
        "clarity-checklist.md"
    )
    
    # Add config files (.rdd.fix.* or .rdd.enh.*)
    $configFile = Find-ChangeConfig $script:WORKSPACE_DIR
    if ($configFile) {
        $filesToBackup += (Split-Path -Leaf $configFile)
    }
    
    $backedUpCount = 0
    foreach ($file in $filesToBackup) {
        $filePath = Join-Path $script:WORKSPACE_DIR $file
        if (Test-Path $filePath) {
            Copy-Item -Path $filePath -Destination $backupPath
            Debug-Print "Backed up $file"
            $backedUpCount++
        }
    }
    
    if ($backedUpCount -eq 0) {
        Print-Warning "No files found to backup"
        Remove-Item -Path $backupPath -Recurse -Force
        return $null
    }
    
    Print-Success "Backup created at $backupPath ($backedUpCount files)"
    return $backupPath
}

# Restore workspace from latest backup
# Usage: Restore-Workspace [backup_path]
# If backup_path not provided, uses latest backup
# Returns: $true on success, $false on failure
function Restore-Workspace {
    param([string]$BackupPath = "")
    
    # If no backup path provided, find latest
    if ([string]::IsNullOrEmpty($BackupPath)) {
        if (-not (Test-Path $script:BACKUP_DIR)) {
            Print-Error "No backups found in $script:BACKUP_DIR"
            return $false
        }
        
        $backups = Get-ChildItem $script:BACKUP_DIR -Directory | Sort-Object Name -Descending
        if (-not $backups) {
            Print-Error "No backups found in $script:BACKUP_DIR"
            return $false
        }
        
        # Get latest backup directory
        $latestBackup = $backups[0]
        $BackupPath = $latestBackup.FullName
        Print-Info "Using latest backup: $($latestBackup.Name)"
    }
    
    if (-not (Test-Path $BackupPath)) {
        Print-Error "Backup directory not found: $BackupPath"
        return $false
    }
    
    Print-Step "Restoring from backup: $(Split-Path -Leaf $BackupPath)"
    
    # Ensure workspace directory exists
    Ensure-Dir $script:WORKSPACE_DIR
    
    # Restore files
    $restoredCount = 0
    Get-ChildItem $BackupPath -File | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $script:WORKSPACE_DIR -Force
        Debug-Print "Restored $($_.Name)"
        $restoredCount++
    }
    
    if ($restoredCount -eq 0) {
        Print-Warning "No files found in backup to restore"
        return $false
    }
    
    Print-Success "Workspace restored from backup ($restoredCount files)"
    return $true
}

# ============================================================================
# WORKSPACE CLEARING
# ============================================================================

# Clear workspace with safety confirmation
# Usage: Clear-Workspace
# Returns: $true on success, $false if cancelled
function Clear-Workspace {
    Print-Warning "This will clear all workspace files."
    
    if ((Test-Path $script:WORKSPACE_DIR)) {
        $workspaceContents = Get-ChildItem $script:WORKSPACE_DIR -ErrorAction SilentlyContinue
        if ($workspaceContents) {
            Print-Info "Current workspace contains:"
            $workspaceContents | ForEach-Object { Write-Host "  - $($_.Name)" }
            Write-Host ""
        }
    }
    
    if (-not (Confirm-Action "Are you sure you want to clear the workspace?")) {
        Print-Info "Operation cancelled"
        return $false
    }
    
    Clear-WorkspaceForced
    return $true
}

# Clear workspace without confirmation (internal use)
# Usage: Clear-WorkspaceForced
# Returns: $true on success
function Clear-WorkspaceForced {
    if (-not (Test-Path $script:WORKSPACE_DIR)) {
        Debug-Print "Workspace directory does not exist"
        return $true
    }
    
    # Remove all files and subdirectories in workspace
    Get-ChildItem $script:WORKSPACE_DIR -Recurse | Remove-Item -Force -Recurse
    Debug-Print "Removed all contents from $script:WORKSPACE_DIR"
    
    # Remove backup directory if it exists
    if (Test-Path $script:BACKUP_DIR) {
        Remove-Item -Path $script:BACKUP_DIR -Recurse -Force
        Debug-Print "Removed backup directory"
    }
    
    Print-Success "Workspace cleared"
    return $true
}

# ============================================================================
# TEMPLATE MANAGEMENT
# ============================================================================

# Copy template file to destination with validation
# Usage: Copy-Template "template_name" "destination_path"
# Returns: $true on success, $false on failure
function Copy-Template {
    param(
        [string]$TemplateName,
        [string]$Destination
    )
    
    if ([string]::IsNullOrEmpty($TemplateName) -or [string]::IsNullOrEmpty($Destination)) {
        Print-Error "Template name and destination are required"
        Write-Host "Usage: Copy-Template <template_name> <destination>"
        return $false
    }
    
    $templatePath = Join-Path $script:TEMPLATES_DIR $TemplateName
    
    # Validate template exists
    if (-not (Test-Path $templatePath)) {
        Print-Error "Template not found: $templatePath"
        return $false
    }
    
    # Create destination directory if needed
    $destDir = Split-Path -Parent $Destination
    Ensure-Dir $destDir
    
    # Check if destination already exists
    if (Test-Path $Destination) {
        Print-Warning "Destination file already exists: $Destination"
        if (-not (Confirm-Action "Overwrite existing file?")) {
            Print-Info "Copy cancelled by user"
            return $false
        }
    }
    
    # Copy template
    Copy-Item -Path $templatePath -Destination $Destination -Force
    Print-Success "Copied template $TemplateName to $Destination"
    return $true
}

# ============================================================================
# WORKSPACE INSPECTION
# ============================================================================

# Check if workspace exists and has content
# Usage: Test-WorkspaceExists
# Returns: $true if workspace exists with content, $false otherwise
function Test-WorkspaceExists {
    if (-not (Test-Path $script:WORKSPACE_DIR)) {
        Print-Error "Workspace directory does not exist: $script:WORKSPACE_DIR"
        return $false
    }
    
    $workspaceContents = Get-ChildItem $script:WORKSPACE_DIR -ErrorAction SilentlyContinue
    if (-not $workspaceContents) {
        Print-Error "Workspace directory is empty: $script:WORKSPACE_DIR"
        return $false
    }
    
    Debug-Print "Workspace directory found with content"
    return $true
}

# List workspace files
# Usage: Get-WorkspaceFiles
# Returns: $true on success
function Get-WorkspaceFiles {
    if (-not (Test-WorkspaceExists)) {
        return $false
    }
    
    Print-Info "Workspace files:"
    Get-ChildItem $script:WORKSPACE_DIR -File | ForEach-Object {
        $size = "{0:N2} KB" -f ($_.Length / 1KB)
        Write-Host "  - $($_.Name) ($size)"
    }
    
    return $true
}

# Get workspace status
# Usage: Get-WorkspaceStatus
# Returns: $true on success
function Get-WorkspaceStatus {
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host "  WORKSPACE STATUS"
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host ""
    
    if (Test-Path $script:WORKSPACE_DIR) {
        Print-Success "Workspace directory exists: $script:WORKSPACE_DIR"
        
        $fileCount = (Get-ChildItem $script:WORKSPACE_DIR -File -ErrorAction SilentlyContinue | Measure-Object).Count
        Print-Info "Files in workspace: $fileCount"
        
        if ($fileCount -gt 0) {
            Write-Host ""
            Get-WorkspaceFiles | Out-Null
        }
        
        # Check for current change config
        $configFile = Find-ChangeConfig $script:WORKSPACE_DIR
        if ($configFile -and (Test-Path $configFile)) {
            Write-Host ""
            Print-Info "Current change configuration:"
            $config = Get-Content $configFile -Raw | ConvertFrom-Json
            $config | ConvertTo-Json | Write-Host
        }
    }
    else {
        Print-Warning "Workspace directory does not exist: $script:WORKSPACE_DIR"
    }
    
    # Check for backups
    if (Test-Path $script:BACKUP_DIR) {
        $backupCount = (Get-ChildItem $script:BACKUP_DIR -Directory -ErrorAction SilentlyContinue | Measure-Object).Count
        if ($backupCount -gt 0) {
            Write-Host ""
            Print-Info "Backups available: $backupCount"
            $latestBackup = Get-ChildItem $script:BACKUP_DIR -Directory | Sort-Object Name -Descending | Select-Object -First 1
            Print-Info "Latest backup: $($latestBackup.Name)"
        }
    }
    
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return $true
}

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

Export-ModuleMember -Function @(
    'Initialize-Workspace',
    'Invoke-ArchiveWorkspace',
    'Backup-Workspace',
    'Restore-Workspace',
    'Clear-Workspace',
    'Clear-WorkspaceForced',
    'Copy-Template',
    'Test-WorkspaceExists',
    'Get-WorkspaceFiles',
    'Get-WorkspaceStatus'
)

Debug-Print "workspace-utils.ps1 loaded successfully"
