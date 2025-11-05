# change-utils.ps1
# Utility script for change workflow management in the RDD framework
# Orchestrates complete change creation and wrap-up workflows

# Prevent multiple sourcing
if ($global:CHANGE_UTILS_LOADED) {
    return
}
$global:CHANGE_UTILS_LOADED = $true

# Source dependencies
$script:SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $SCRIPT_DIR "core-utils.ps1")
. (Join-Path $SCRIPT_DIR "git-utils.ps1")
. (Join-Path $SCRIPT_DIR "branch-utils.ps1")
. (Join-Path $SCRIPT_DIR "workspace-utils.ps1")
. (Join-Path $SCRIPT_DIR "clarify-utils.ps1")

# Get repository root and paths
$script:REPO_ROOT = Get-RepoRoot
$script:WORKSPACE_DIR = "$REPO_ROOT/.rdd-docs/workspace"
$script:TEMPLATE_DIR = "$REPO_ROOT/.rdd/templates"

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHANGE CREATION WORKFLOW
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Create a new change with complete workflow
# Orchestrates: validation, ID generation, branch creation, workspace initialization
# Arguments:
#   $1 - change_name: The name of the change (kebab-case)
#   $2 - change_type: Type of change ('enh' or 'fix', default: 'enh')
# Returns: $true on success, $false on error
function New-Change {
    param(
        [string]$ChangeName,
        [string]$ChangeType = "enh"
    )
    
    # Validate required parameters
    if ([string]::IsNullOrEmpty($ChangeName)) {
        Print-Error "Change name is required"
        Write-Host "Usage: New-Change <change-name> [type]"
        Write-Host "  type: enh (default) or fix"
        return $false
    }
    
    # Validate change type
    if ($ChangeType -ne "enh" -and $ChangeType -ne "fix") {
        Print-Error "Invalid change type '$ChangeType'"
        Write-Host "Valid types: enh, fix"
        return $false
    }
    
    # Validate change name (kebab-case, max 5 words)
    if (-not (Validate-Name $ChangeName)) {
        return $false
    }
    
    # Generate change ID (YYYYMMDD-HHmm format)
    $dateTime = Get-Date -Format "yyyyMMdd-HHmm"
    $changeId = "${dateTime}-${ChangeName}"
    $branchName = "${ChangeType}/${changeId}"
    
    # Check if branch already exists
    if (Test-BranchExists $branchName "local") {
        Print-Error "Branch '$branchName' already exists"
        return $false
    }
    
    Print-Step "Creating change: $ChangeName ($ChangeType)"
    
    # Ensure .rdd-docs folder exists
    $rddDocsPath = "$script:REPO_ROOT/.rdd-docs"
    if (-not (Test-Path $rddDocsPath)) {
        New-Item -ItemType Directory -Path $rddDocsPath -Force | Out-Null
        Print-Success "Created .rdd-docs folder"
    }
    
    # Switch to main, pull latest, create new branch
    Print-Info "Switching to main branch..."
    $defaultBranch = Get-DefaultBranch
    git checkout $defaultBranch
    if ($LASTEXITCODE -ne 0) { return $false }
    
    Print-Info "Pulling latest changes..."
    git pull
    if ($LASTEXITCODE -ne 0) { return $false }
    
    Print-Info "Creating branch: $branchName"
    git checkout -b $branchName
    if ($LASTEXITCODE -ne 0) { return $false }
    Print-Success "Created and checked out branch: $branchName"
    
    # Initialize workspace
    Print-Info "Initializing workspace..."
    # Map 'enh' to 'change' for workspace initialization
    $workspaceType = if ($ChangeType -eq "enh") { "change" } else { $ChangeType }
    if (-not (Initialize-Workspace $workspaceType)) { return $false }
    
    # Initialize change tracking files
    Print-Info "Initializing change tracking..."
    if (-not (Initialize-ChangeTracking $changeId $branchName $ChangeType)) { return $false }
    
    # Create change configuration
    Print-Info "Creating change configuration..."
    if (-not (New-ChangeConfig $ChangeName $changeId $branchName $ChangeType)) { return $false }
    
    Write-Host ""
    Print-Success "Change workspace initialized successfully!"
    Write-Host "  - Branch: ${branchName}"
    Write-Host "  - Change ID: ${changeId}"
    Write-Host "  - Workspace: .rdd-docs/workspace/"
    Write-Host ""
    Print-Info "Next steps:"
    Write-Host "  1. Run clarification prompt: Use .github/prompts/rdd.02-clarify-requirements.prompt.md"
    
    return $true
}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHANGE TRACKING INITIALIZATION
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Initialize change tracking files
# Arguments:
#   $1 - change_id: The change ID (YYYYMMDD-HHmm-name format)
#   $2 - branch_name: The branch name (enh/fix/change-id)
#   $3 - change_type: Type of change ('enh' or 'fix')
# Returns: $true on success, $false on error
function Initialize-ChangeTracking {
    param(
        [string]$ChangeId,
        [string]$BranchName,
        [string]$ChangeType
    )
    
    # Validate parameters
    if ([string]::IsNullOrEmpty($ChangeId) -or [string]::IsNullOrEmpty($BranchName) -or [string]::IsNullOrEmpty($ChangeType)) {
        Print-Error "Missing required parameters for change tracking initialization"
        Write-Host "Usage: Initialize-ChangeTracking <change-id> <branch-name> <change-type>"
        return $false
    }
    
    return $true
}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHANGE CONFIGURATION
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Create change configuration file
# Writes .current-change JSON with all required fields
# Arguments:
#   $1 - change_name: The name of the change
#   $2 - change_id: The change ID (YYYYMMDD-HHmm-name format)
#   $3 - branch_name: The branch name (enh/fix/change-id)
#   $4 - change_type: Type of change ('enh' or 'fix')
# Returns: $true on success, $false on error
function New-ChangeConfig {
    param(
        [string]$ChangeName,
        [string]$ChangeId,
        [string]$BranchName,
        [string]$ChangeType
    )
    
    # Validate parameters
    if ([string]::IsNullOrEmpty($ChangeName) -or [string]::IsNullOrEmpty($ChangeId) -or 
        [string]::IsNullOrEmpty($BranchName) -or [string]::IsNullOrEmpty($ChangeType)) {
        Print-Error "Missing required parameters for change config"
        Write-Host "Usage: New-ChangeConfig <change-name> <change-id> <branch-name> <change-type>"
        return $false
    }
    
    # Create config file with new naming convention
    $timestamp = Get-Timestamp
    $configFilename = ".rdd.${ChangeType}.${BranchName -replace '/', '-'}"
    $configPath = Join-Path $script:WORKSPACE_DIR $configFilename
    
    $config = @{
        changeName = $ChangeName
        changeId = $ChangeId
        branchName = $BranchName
        changeType = $ChangeType
        startedAt = $timestamp
        phase = "init"
        status = "in-progress"
    } | ConvertTo-Json
    
    $config | Out-File -FilePath $configPath -Encoding utf8
    
    Print-Success "Created $configFilename config file"
    return $true
}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CHANGE WRAP-UP WORKFLOW
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Wrap up a change with complete workflow
# Orchestrates: archive, commit, push, PR creation
# Returns: $true on success, $false on error
function Complete-Change {
    $currentBranch = git branch --show-current
    
    # Validate we're on an enh/fix branch
    if ($currentBranch -notmatch '^(enh|fix)/') {
        Print-Error "Wrap-up can only be executed from an enh or fix branch"
        Print-Error "Current branch: $currentBranch"
        return $false
    }
    
    Print-Banner "CHANGE WRAP-UP WORKFLOW"
    
    # Check for uncommitted changes
    Print-Step "1. Checking for uncommitted changes"
    if (-not (Test-UncommittedChanges)) {
        return $false
    }
    Print-Success "No uncommitted changes found"
    Write-Host ""
    
    # Extract change type and name from branch
    $changeType = $currentBranch.Split('/')[0]
    $changeInfo = $currentBranch.Substring($changeType.Length + 1)
    
    # Display wrap-up plan
    Print-Info "This will perform the following actions:"
    Write-Host ""
    Write-Host "  1. Move workspace content to .rdd-docs/archive/${currentBranch -replace '/', '-'}"
    Write-Host "  2. Create commit with message: 'archive: moved workspace to archive'"
    Write-Host "  3. Push changes to remote branch"
    Write-Host ""
    
    # Ask for user confirmation
    if (-not (Confirm-Action "Proceed with wrap-up?")) {
        Print-Info "Wrap-up cancelled by user"
        return $true
    }
    Write-Host ""
    
    # Archive workspace
    Print-Step "2. Archiving workspace contents"
    $archiveRelative = Invoke-ArchiveWorkspace $currentBranch $false
    if (-not $archiveRelative) {
        Print-Error "Failed to archive workspace"
        return $false
    }
    Print-Success "Workspace archived to $archiveRelative"
    Write-Host ""
    
    # Create wrap-up commit
    Print-Step "3. Creating wrap-up commit"
    $commitMessage = "archive: moved workspace to archive"
    
    git add -A
    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) {
        Print-Warning "No changes staged for commit - skipping commit creation"
    }
    else {
        git commit -m $commitMessage
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Wrap-up commit created"
        }
        else {
            Print-Error "Failed to create wrap-up commit"
            return $false
        }
    }
    Write-Host ""
    
    # Push to remote
    Print-Step "4. Pushing branch to remote"
    if (Push-ToRemote $currentBranch) {
        Print-Success "Branch pushed to remote"
    }
    else {
        Print-Error "Failed to push branch to remote"
        return $false
    }
    
    # Display completion summary
    Write-Host ""
    Print-Banner "WRAP-UP COMPLETE"
    Write-Host ""
    Print-Success "Workspace archived to: $archiveRelative"
    Print-Success "Commit created with message: '$commitMessage'"
    Print-Success "Changes pushed to remote branch: $currentBranch"
    Write-Host ""
    Print-Info "Next Steps:"
    Write-Host "  1. Create a Pull Request on GitHub to merge your changes"
    Write-Host "  2. Review and complete the PR process"
    Write-Host "  3. After merge, you can delete the local and remote branches"
    Write-Host ""
    
    return $true
}

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

Export-ModuleMember -Function @(
    'New-Change',
    'Initialize-ChangeTracking',
    'New-ChangeConfig',
    'Complete-Change'
)

Debug-Print "change-utils.ps1 loaded successfully"
