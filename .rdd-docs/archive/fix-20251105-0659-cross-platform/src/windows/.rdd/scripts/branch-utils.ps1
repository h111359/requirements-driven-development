# branch-utils.ps1
# Branch management utility functions for RDD framework
# Provides branch creation, deletion, merge checking, and listing operations

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
if ($global:BRANCH_UTILS_LOADED) {
    return
}
$global:BRANCH_UTILS_LOADED = $true

# ============================================================================
# BRANCH CREATION
# ============================================================================

# Create a new branch with format validation
# Usage: New-Branch "enh|fix" "branch-name"
# Returns: $true on success, $false on failure
function New-Branch {
    param(
        [string]$BranchType,
        [string]$BranchName
    )
    
    if ([string]::IsNullOrEmpty($BranchType) -or [string]::IsNullOrEmpty($BranchName)) {
        Print-Error "Branch type and name are required"
        Write-Host "Usage: New-Branch <enh|fix> <branch_name>"
        return $false
    }
    
    # Validate branch type
    if ($BranchType -notmatch '^(enh|fix)$') {
        Print-Error "Invalid branch type: $BranchType"
        Print-Info "Valid types: enh, fix"
        return $false
    }
    
    # Validate branch name format (kebab-case, max 5 words)
    if (-not (Validate-Name $BranchName)) {
        return $false
    }
    
    # Generate branch ID with timestamp
    $dateTime = Get-Date -Format "yyyyMMdd-HHmm"
    $branchId = "${dateTime}-${BranchName}"
    $fullBranchName = "${BranchType}/${branchId}"
    
    # Check if branch already exists
    git show-ref --verify --quiet "refs/heads/$fullBranchName" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Print-Error "Branch '$fullBranchName' already exists"
        return $false
    }
    
    # Get default branch
    $defaultBranch = Get-DefaultBranch
    
    Print-Step "Creating new branch: $fullBranchName"
    
    # Switch to default branch and pull latest
    Print-Info "Switching to '$defaultBranch' and pulling latest changes..."
    git checkout $defaultBranch 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Print-Error "Failed to checkout '$defaultBranch'"
        return $false
    }
    
    git pull origin $defaultBranch 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Print-Warning "Failed to pull from origin (continuing anyway)"
    }
    
    # Create and checkout new branch
    Print-Info "Creating branch '$fullBranchName'..."
    git checkout -b $fullBranchName 2>&1
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Created and checked out branch: $fullBranchName"
        Write-Host ""
        Print-Info "Branch details:"
        Write-Host "  Type: $BranchType"
        Write-Host "  Name: $BranchName"
        Write-Host "  ID: $branchId"
        Write-Host "  Full: $fullBranchName"
        return $true
    }
    else {
        Print-Error "Failed to create branch"
        return $false
    }
}

# ============================================================================
# BRANCH DELETION
# ============================================================================

# Delete a branch locally and remotely with safety checks
# Usage: Remove-Branch "branch_name" [force] [skip_checks]
# force: $true to force delete (bypass merge check), $false otherwise (default: $false)
# skip_checks: $true to skip uncommitted changes check, $false otherwise (default: $false)
# Returns: $true on success, $false on failure
function Remove-Branch {
    param(
        [string]$BranchName,
        [bool]$Force = $false,
        [bool]$SkipChecks = $false
    )
    
    if ([string]::IsNullOrEmpty($BranchName)) {
        Print-Error "Branch name is required"
        Write-Host "Usage: Remove-Branch <branch_name> [force] [skip_checks]"
        return $false
    }
    
    # Check if we're in a git repository
    Test-GitRepo | Out-Null
    
    # Check for uncommitted changes unless skipped
    if (-not $SkipChecks) {
        Print-Info "Checking for uncommitted changes..."
        if (-not (Test-UncommittedChanges)) {
            Print-Error "Please commit or stash changes before deleting branch"
            return $false
        }
        Write-Host ""
    }
    
    # Check if branch exists locally
    git show-ref --verify --quiet "refs/heads/$BranchName" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Print-Error "Local branch '$BranchName' does not exist"
        return $false
    }
    
    # Check if branch is merged (unless force delete)
    if (-not $Force) {
        Print-Info "Checking if branch is merged..."
        $mergeStatus = Test-MergeStatus $BranchName
        
        if ($mergeStatus -eq 1) {
            Print-Warning "Branch is not merged into default branch"
            if (-not (Confirm-Action "Delete anyway? (This will use force delete)")) {
                Print-Info "Deletion cancelled"
                return $false
            }
            $Force = $true
        }
        elseif ($mergeStatus -gt 1) {
            Print-Error "Failed to check merge status"
            return $false
        }
        Write-Host ""
    }
    
    # Get default branch to switch to
    $defaultBranch = Get-DefaultBranch
    
    # Switch to default branch
    Print-Info "Switching to branch '$defaultBranch'..."
    git checkout $defaultBranch 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Print-Error "Failed to checkout '$defaultBranch'"
        return $false
    }
    Write-Host ""
    
    # Delete local branch
    Print-Info "Deleting local branch '$BranchName'..."
    if ($Force) {
        git branch -D $BranchName 2>&1
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Local branch force-deleted"
        }
        else {
            Print-Error "Failed to delete local branch"
            return $false
        }
    }
    else {
        git branch -d $BranchName 2>&1
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Local branch deleted"
        }
        else {
            Print-Error "Failed to delete local branch (not fully merged)"
            return $false
        }
    }
    Write-Host ""
    
    # Check if remote branch exists and delete
    $remoteBranches = git ls-remote --heads origin $BranchName 2>$null
    if ($remoteBranches -match $BranchName) {
        Print-Info "Deleting remote branch 'origin/$BranchName'..."
        git push origin --delete $BranchName 2>&1
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Remote branch deleted"
        }
        else {
            Print-Warning "Failed to delete remote branch (check permissions)"
            return $false
        }
    }
    else {
        Print-Info "Remote branch does not exist (or was already deleted)"
    }
    
    Write-Host ""
    Print-Success "Branch '$BranchName' deleted successfully"
    return $true
}

# ============================================================================
# BATCH BRANCH DELETION
# ============================================================================

# Delete all merged branches with confirmation
# Usage: Remove-MergedBranches
# Returns: $true on success, $false on failure
function Remove-MergedBranches {
    Test-GitRepo | Out-Null
    
    $defaultBranch = Get-DefaultBranch
    
    Print-Banner "DELETE MERGED BRANCHES"
    Write-Host ""
    
    # Fetch latest changes
    Print-Info "Fetching latest changes from remote..."
    git fetch --all 2>&1 | Out-Null
    Write-Host ""
    
    # Update local default branch
    Print-Info "Updating local '$defaultBranch' to match remote..."
    git checkout $defaultBranch 2>&1 | Out-Null
    git pull origin $defaultBranch 2>&1 | Out-Null
    Print-Success "Local '$defaultBranch' updated"
    Write-Host ""
    
    # Get list of remote branches merged into default branch
    Print-Info "Finding branches merged into '$defaultBranch'..."
    $mergedRemoteBranches = git branch -r --merged "origin/$defaultBranch" 2>$null |
        Where-Object { $_ -notmatch "origin/$defaultBranch" -and $_ -notmatch 'origin/HEAD' } |
        ForEach-Object { $_.Trim() }
    
    $mergedLocalBranches = git branch --merged $defaultBranch 2>$null |
        Where-Object { $_ -notmatch "^\*" -and $_ -notmatch "^\s*${defaultBranch}$" -and $_ -notmatch "^\s*HEAD$" } |
        ForEach-Object { $_.Trim() }
    
    # Check if there are any branches to delete
    if (-not $mergedRemoteBranches -and -not $mergedLocalBranches) {
        Print-Info "No merged branches found"
        return $true
    }
    
    # Display branches to be deleted
    if ($mergedRemoteBranches) {
        Write-Host ""
        Print-Info "Remote branches to delete:"
        $mergedRemoteBranches | ForEach-Object { Write-Host "  - $_" }
    }
    
    if ($mergedLocalBranches) {
        Write-Host ""
        Print-Info "Local branches to delete:"
        $mergedLocalBranches | ForEach-Object { Write-Host "  - $_" }
    }
    
    Write-Host ""
    
    # Count branches
    $remoteCount = if ($mergedRemoteBranches) { ($mergedRemoteBranches | Measure-Object).Count } else { 0 }
    $localCount = if ($mergedLocalBranches) { ($mergedLocalBranches | Measure-Object).Count } else { 0 }
    $totalCount = $remoteCount + $localCount
    
    Print-Warning "Total branches to delete: $totalCount ($remoteCount remote, $localCount local)"
    Write-Host ""
    
    # Ask for confirmation
    if (-not (Confirm-Action "Delete all these branches?")) {
        Print-Info "Deletion cancelled"
        return $true
    }
    
    Write-Host ""
    
    # Delete remote branches
    if ($mergedRemoteBranches) {
        Print-Step "Deleting remote branches..."
        $mergedRemoteBranches | ForEach-Object {
            $branch = $_ -replace '^origin/', ''
            Print-Info "Deleting origin/$branch..."
            git push origin --delete $branch 2>&1
            if ($LASTEXITCODE -eq 0) {
                Print-Success "Deleted origin/$branch"
            }
            else {
                Print-Error "Failed to delete origin/$branch"
            }
        }
        Write-Host ""
    }
    
    # Delete local branches
    if ($mergedLocalBranches) {
        Print-Step "Deleting local branches..."
        $mergedLocalBranches | ForEach-Object {
            $branch = $_
            Print-Info "Deleting $branch..."
            git branch -d $branch 2>&1
            if ($LASTEXITCODE -eq 0) {
                Print-Success "Deleted $branch"
            }
            else {
                Print-Error "Failed to delete $branch"
            }
        }
        Write-Host ""
    }
    
    Print-Success "Branch cleanup completed"
    return $true
}

# ============================================================================
# POST-MERGE CLEANUP
# ============================================================================

# Clean up after a branch has been merged
# Switches to default branch, fetches and pulls latest, deletes the specified merged branch
# Usage: Invoke-CleanupAfterMerge [branch_name]
# If branch_name not provided, prompts user to enter it
# Returns: $true on success, $false on failure
function Invoke-CleanupAfterMerge {
    param([string]$BranchName = "")
    
    Test-GitRepo | Out-Null
    
    Print-Banner "POST-MERGE CLEANUP"
    Write-Host ""
    
    # Get default branch
    $defaultBranch = Get-DefaultBranch
    $currentBranch = Get-CurrentBranch
    
    # If no branch name provided, prompt for it or use current branch
    if ([string]::IsNullOrEmpty($BranchName)) {
        # If we're not on the default branch, offer to delete current branch
        if ($currentBranch -ne $defaultBranch) {
            Print-Info "Current branch: $currentBranch"
            if (Confirm-Action "Delete current branch after cleanup?") {
                $BranchName = $currentBranch
            }
            else {
                $BranchName = Read-Host "Enter branch name to delete (or press Enter to skip)"
                if ([string]::IsNullOrEmpty($BranchName)) {
                    Print-Info "No branch specified for deletion"
                }
            }
        }
        else {
            $BranchName = Read-Host "Enter branch name to delete (or press Enter to skip)"
            if ([string]::IsNullOrEmpty($BranchName)) {
                Print-Info "No branch specified for deletion"
            }
        }
    }
    
    # Switch to default branch
    Print-Step "1. Switching to '$defaultBranch' branch"
    if ($currentBranch -ne $defaultBranch) {
        git checkout $defaultBranch 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Print-Error "Failed to checkout '$defaultBranch'"
            return $false
        }
        Print-Success "Switched to '$defaultBranch'"
    }
    else {
        Print-Info "Already on '$defaultBranch'"
    }
    Write-Host ""
    
    # Fetch latest changes
    Print-Step "2. Fetching latest changes from remote"
    git fetch origin 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Print-Warning "Failed to fetch from remote"
    }
    else {
        Print-Success "Fetched latest changes"
    }
    Write-Host ""
    
    # Pull latest changes for default branch
    Print-Step "3. Pulling latest changes for '$defaultBranch'"
    git pull origin $defaultBranch 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Print-Warning "Failed to pull latest changes"
    }
    else {
        Print-Success "Pulled latest changes"
    }
    Write-Host ""
    
    # Delete the branch if specified
    if (-not [string]::IsNullOrEmpty($BranchName)) {
        Print-Step "4. Deleting branch '$BranchName'"
        
        # Check if branch exists locally
        git show-ref --verify --quiet "refs/heads/$BranchName" 2>$null
        if ($LASTEXITCODE -eq 0) {
            # Delete local branch
            git branch -d $BranchName 2>&1
            if ($LASTEXITCODE -eq 0) {
                Print-Success "Local branch deleted"
            }
            else {
                Print-Warning "Branch not fully merged, use --force if needed"
                if (Confirm-Action "Force delete local branch?") {
                    git branch -D $BranchName 2>&1
                    if ($LASTEXITCODE -eq 0) {
                        Print-Success "Local branch force-deleted"
                    }
                    else {
                        Print-Error "Failed to delete local branch"
                    }
                }
            }
        }
        else {
            Print-Info "Local branch does not exist (already deleted)"
        }
        
        # Check and delete remote branch
        $remoteBranches = git ls-remote --heads origin $BranchName 2>$null
        if ($remoteBranches -match $BranchName) {
            Print-Info "Deleting remote branch 'origin/$BranchName'..."
            git push origin --delete $BranchName 2>&1
            if ($LASTEXITCODE -eq 0) {
                Print-Success "Remote branch deleted"
            }
            else {
                Print-Warning "Failed to delete remote branch (may require permissions)"
            }
        }
        else {
            Print-Info "Remote branch does not exist (already deleted)"
        }
        Write-Host ""
    }
    
    Print-Banner "CLEANUP COMPLETE"
    Write-Host ""
    Print-Success "You are now on '$defaultBranch' with latest changes"
    if (-not [string]::IsNullOrEmpty($BranchName)) {
        Print-Success "Branch '$BranchName' has been cleaned up"
    }
    Write-Host ""
    
    return $true
}

# ============================================================================
# MERGE STATUS CHECKING
# ============================================================================

# Check if a branch is merged into the base branch
# Usage: Test-MergeStatus "branch_name" ["base_branch"]
# Returns: 0 if merged, 1 if not merged, 2+ for errors
function Test-MergeStatus {
    param(
        [string]$BranchName,
        [string]$BaseBranch = ""
    )
    
    if ([string]::IsNullOrEmpty($BranchName)) {
        Print-Error "Branch name is required"
        Write-Host "Usage: Test-MergeStatus <branch_name> [base_branch]"
        return 2
    }
    
    if ([string]::IsNullOrEmpty($BaseBranch)) {
        $BaseBranch = Get-DefaultBranch
    }
    
    # Check if branch exists
    git show-ref --verify --quiet "refs/heads/$BranchName" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Print-Error "Branch '$BranchName' does not exist"
        return 3
    }
    
    $currentBranch = Get-CurrentBranch
    
    # Fetch latest from remote
    Debug-Print "Fetching latest changes from remote..."
    git fetch origin 2>&1 | Out-Null
    
    # Check if base branch exists
    git show-ref --verify --quiet "refs/heads/$BaseBranch" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Print-Error "Base branch '$BaseBranch' not found"
        return 4
    }
    
    # Update local base branch to match remote
    Debug-Print "Updating local '$BaseBranch' branch..."
    git checkout $BaseBranch 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Print-Error "Failed to checkout '$BaseBranch'"
        return 5
    }
    
    git pull origin $BaseBranch 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Print-Error "Failed to pull latest changes for '$BaseBranch'"
        return 6
    }
    
    # Return to original branch
    git checkout $currentBranch 2>&1 | Out-Null
    Debug-Print "Local '$BaseBranch' updated from remote"
    
    # Check if branch is merged using git branch --merged
    $mergedBranches = git branch --merged $BaseBranch
    if ($mergedBranches -match "^\*?\s*${BranchName}$") {
        Print-Success "Branch '$BranchName' is merged into '$BaseBranch'"
        return 0
    }
    else {
        Print-Warning "Branch '$BranchName' is NOT merged into '$BaseBranch'"
        return 1
    }
}

# ============================================================================
# BRANCH LISTING
# ============================================================================

# List branches with optional filtering
# Usage: Get-Branches [filter]
# filter: "local", "remote", "merged", "unmerged", "all" (default: "local")
# Returns: $true on success
function Get-Branches {
    param([string]$Filter = "local")
    
    Test-GitRepo | Out-Null
    
    $defaultBranch = Get-DefaultBranch
    
    switch ($Filter) {
        "local" {
            Print-Info "Local branches:"
            git branch --list | ForEach-Object { Write-Host "  $_" }
        }
        "remote" {
            Print-Info "Remote branches:"
            git branch -r | ForEach-Object { Write-Host "  $_" }
        }
        "merged" {
            Print-Info "Branches merged into '$defaultBranch':"
            git branch --merged $defaultBranch | ForEach-Object { Write-Host "  $_" }
        }
        "unmerged" {
            Print-Info "Branches NOT merged into '$defaultBranch':"
            git branch --no-merged $defaultBranch | ForEach-Object { Write-Host "  $_" }
        }
        "all" {
            Print-Info "All branches (local and remote):"
            git branch -a | ForEach-Object { Write-Host "  $_" }
        }
        default {
            Print-Error "Invalid filter: $Filter"
            Print-Info "Valid filters: local, remote, merged, unmerged, all"
            return $false
        }
    }
    
    return $true
}

# ============================================================================
# BRANCH INSPECTION
# ============================================================================

# Get information about a specific branch
# Usage: Get-BranchInfo "branch_name"
# Returns: $true on success, $false on failure
function Get-BranchInfo {
    param([string]$BranchName)
    
    if ([string]::IsNullOrEmpty($BranchName)) {
        Print-Error "Branch name is required"
        Write-Host "Usage: Get-BranchInfo <branch_name>"
        return $false
    }
    
    # Check if branch exists
    git show-ref --verify --quiet "refs/heads/$BranchName" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Print-Error "Branch '$BranchName' does not exist"
        return $false
    }
    
    $defaultBranch = Get-DefaultBranch
    
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host "  BRANCH INFO: $BranchName"
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host ""
    
    # Last commit on branch
    Print-Info "Last commit:"
    git log -1 --pretty=format:"  %h - %s (%cr) <%an>" $BranchName
    Write-Host ""
    Write-Host ""
    
    # Commit count ahead/behind default branch
    $ahead = git rev-list --count "origin/${defaultBranch}..${BranchName}" 2>$null
    if (-not $ahead) { $ahead = "0" }
    $behind = git rev-list --count "${BranchName}..origin/${defaultBranch}" 2>$null
    if (-not $behind) { $behind = "0" }
    Print-Info "Compared to '$defaultBranch':"
    Write-Host "  Ahead: $ahead commit(s)"
    Write-Host "  Behind: $behind commit(s)"
    Write-Host ""
    
    # Merge status
    Print-Info "Merge status:"
    $mergedBranches = git branch --merged $defaultBranch
    if ($mergedBranches -match "^\*?\s*${BranchName}$") {
        Write-Host "  ✓ Merged into '$defaultBranch'"
    }
    else {
        Write-Host "  ✗ Not merged into '$defaultBranch'"
    }
    Write-Host ""
    
    # Remote tracking
    $remoteBranch = git rev-parse --abbrev-ref "${BranchName}@{upstream}" 2>$null
    Print-Info "Remote tracking:"
    if ($remoteBranch) {
        Write-Host "  Tracking: $remoteBranch"
    }
    else {
        Write-Host "  No remote tracking configured"
    }
    
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return $true
}

# Check if branch exists (local or remote)
# Usage: Test-BranchExists "branch_name" ["local|remote|any"]
# Returns: $true if exists, $false if not
function Test-BranchExists {
    param(
        [string]$BranchName,
        [string]$Location = "any"
    )
    
    if ([string]::IsNullOrEmpty($BranchName)) {
        return $false
    }
    
    switch ($Location) {
        "local" {
            git show-ref --verify --quiet "refs/heads/$BranchName" 2>$null
            return ($LASTEXITCODE -eq 0)
        }
        "remote" {
            $remoteBranches = git ls-remote --heads origin $BranchName 2>$null
            return ($remoteBranches -match $BranchName)
        }
        "any" {
            git show-ref --verify --quiet "refs/heads/$BranchName" 2>$null
            if ($LASTEXITCODE -eq 0) {
                return $true
            }
            $remoteBranches = git ls-remote --heads origin $BranchName 2>$null
            return ($remoteBranches -match $BranchName)
        }
        default {
            Print-Error "Invalid location: $Location"
            return $false
        }
    }
}

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

Export-ModuleMember -Function @(
    'New-Branch',
    'Remove-Branch',
    'Remove-MergedBranches',
    'Invoke-CleanupAfterMerge',
    'Test-MergeStatus',
    'Get-Branches',
    'Get-BranchInfo',
    'Test-BranchExists'
)

Debug-Print "branch-utils.ps1 loaded successfully"
