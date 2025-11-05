# git-utils.ps1
# Git operations utility functions for RDD framework
# Provides git-related operations used across all RDD scripts

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

# Prevent multiple sourcing
if ($global:GIT_UTILS_LOADED) {
    return
}
$global:GIT_UTILS_LOADED = $true

# ============================================================================
# GIT REPOSITORY CHECKS
# ============================================================================

# Check if we're in a git repository
# Usage: Test-GitRepo
# Returns: $true if in git repo, exits with error if not
function Test-GitRepo {
    try {
        git rev-parse --is-inside-work-tree 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Debug-Print "Git repository verified"
            return $true
        }
    }
    catch {}
    
    Print-Error "Not a git repository. Please run this from within a git repository."
    exit 1
}

# ============================================================================
# UNCOMMITTED CHANGES DETECTION
# ============================================================================

# Check for uncommitted changes (modified, staged, or untracked files)
# Usage: Test-UncommittedChanges
# Returns: $true if no changes, $false if changes exist
function Test-UncommittedChanges {
    $hasChanges = $false
    
    # Check for modified or staged files
    git diff-index --quiet HEAD -- 2>$null
    if ($LASTEXITCODE -ne 0) {
        $hasChanges = $true
    }
    
    # Check for untracked files
    $untrackedFiles = git ls-files --others --exclude-standard
    if ($untrackedFiles) {
        $hasChanges = $true
    }
    
    if ($hasChanges) {
        Print-Error "There are uncommitted changes in the repository."
        Print-Error "Please commit or stash your changes before proceeding."
        Write-Host ""
        Print-Info "Uncommitted changes:"
        git status --short
        return $false
    }
    
    Debug-Print "No uncommitted changes found"
    return $true
}

# ============================================================================
# BRANCH OPERATIONS
# ============================================================================

# Get the default branch name (main or master)
# Usage: Get-DefaultBranch
# Returns: "main" or "master" depending on what exists
function Get-DefaultBranch {
    $defaultBranch = "main"
    
    # Check if main branch exists
    git show-ref --verify --quiet "refs/heads/main" 2>$null
    if ($LASTEXITCODE -ne 0) {
        # Check if master branch exists
        git show-ref --verify --quiet "refs/heads/master" 2>$null
        if ($LASTEXITCODE -eq 0) {
            $defaultBranch = "master"
        }
    }
    
    return $defaultBranch
}

# Fetch latest changes from remote default branch
# Usage: Invoke-FetchMain
# Returns: $true on success, $false on failure
function Invoke-FetchMain {
    $defaultBranch = Get-DefaultBranch
    
    Print-Step "Fetching latest from origin/${defaultBranch}..."
    
    git fetch origin $defaultBranch --quiet 2>$null
    if ($LASTEXITCODE -eq 0) {
        Debug-Print "Successfully fetched origin/${defaultBranch}"
        return $true
    }
    else {
        Print-Warning "Failed to fetch from origin/${defaultBranch}"
        return $false
    }
}

# ============================================================================
# FILE COMPARISON AND DIFFS
# ============================================================================

# Compare current branch with main branch
# Usage: Compare-WithMain
# Returns: $true on success
function Compare-WithMain {
    Invoke-FetchMain | Out-Null
    
    $defaultBranch = Get-DefaultBranch
    $currentBranch = git branch --show-current
    
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host "  COMPARISON: ${currentBranch} vs ${defaultBranch}"
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host ""
    
    # Show commit differences
    Print-Step "Commit differences:"
    $commitCount = git rev-list --count "origin/${defaultBranch}..HEAD" 2>$null
    if (-not $commitCount) { $commitCount = "0" }
    Write-Host "  This branch is $commitCount commit(s) ahead of ${defaultBranch}"
    Write-Host ""
    
    if ([int]$commitCount -gt 0) {
        git log --oneline --graph --max-count=10 "origin/${defaultBranch}..HEAD"
        Write-Host ""
    }
    
    # Show file changes
    Print-Step "File changes:"
    Get-ModifiedFiles
    Write-Host ""
    
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return $true
}

# Get list of modified files compared to main branch
# Usage: Get-ModifiedFiles
# Returns: $true on success, prints modified files list
function Get-ModifiedFiles {
    $defaultBranch = Get-DefaultBranch
    $currentBranch = git branch --show-current
    
    Print-Info "Comparing ${currentBranch} with ${defaultBranch}..."
    Write-Host ""
    
    # Get list of modified files
    $modifiedFiles = git diff --name-only "origin/${defaultBranch}...HEAD" 2>$null
    
    if (-not $modifiedFiles) {
        Print-Warning "No files modified compared to ${defaultBranch}"
        return $true
    }
    
    Write-Host "Modified files:"
    $modifiedFiles | ForEach-Object {
        $file = $_
        $status = (git diff --name-status "origin/${defaultBranch}...HEAD" 2>$null | Select-String "^[AMDRC].*$file").ToString().Split()[0]
        switch ($status) {
            "A" { Write-Host "  + $file (added)" -ForegroundColor Green }
            "M" { Write-Host "  ~ $file (modified)" -ForegroundColor Yellow }
            "D" { Write-Host "  - $file (deleted)" -ForegroundColor Red }
            { $_ -match "R" } { Write-Host "  → $file (renamed)" -ForegroundColor Cyan }
            { $_ -match "C" } { Write-Host "  © $file (copied)" -ForegroundColor Cyan }
            default { Write-Host "  ? $file" -ForegroundColor Blue }
        }
    }
    
    Write-Host ""
    $fileCount = ($modifiedFiles | Measure-Object).Count
    Print-Success "Found $fileCount modified file(s)"
    
    return $true
}

# Get diff for a specific file compared to main branch
# Usage: Get-FileDiff "/path/to/file"
# Returns: $true on success, $false if file not found
function Get-FileDiff {
    param([string]$FilePath)
    
    if ([string]::IsNullOrEmpty($FilePath)) {
        Print-Error "File path is required"
        Write-Host "Usage: Get-FileDiff <file_path>"
        return $false
    }
    
    if (-not (Test-Path $FilePath)) {
        Print-Error "File not found: $FilePath"
        return $false
    }
    
    $defaultBranch = Get-DefaultBranch
    Print-Info "Showing changes in: $FilePath"
    Write-Host ""
    
    # Check if file exists in main branch
    git cat-file -e "origin/${defaultBranch}:${FilePath}" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Print-Warning "File is new (doesn't exist in ${defaultBranch})"
        Write-Host ""
        Write-Host "Full content:"
        Get-Content $FilePath
        return $true
    }
    
    # Show the diff
    git diff "origin/${defaultBranch}...HEAD" -- $FilePath
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Print-Success "Changes displayed for $FilePath"
    }
    
    return $true
}

# ============================================================================
# PUSH AND COMMIT OPERATIONS
# ============================================================================

# Push current branch to remote with upstream tracking
# Usage: Push-ToRemote [branch_name]
# If branch_name not provided, uses current branch
# Returns: $true on success, $false on failure
function Push-ToRemote {
    param([string]$BranchName = "")
    
    if ([string]::IsNullOrEmpty($BranchName)) {
        $BranchName = git branch --show-current
    }
    
    if ([string]::IsNullOrEmpty($BranchName)) {
        Print-Error "No branch name provided and could not determine current branch"
        return $false
    }
    
    Print-Info "Pushing branch '$BranchName' to remote..."
    
    git push -u origin $BranchName 2>&1
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Branch pushed to remote with upstream tracking"
        return $true
    }
    else {
        Print-Error "Failed to push branch to remote"
        return $false
    }
}

# Auto-commit all changes with a message
# Usage: Invoke-AutoCommit "commit message"
# Returns: 0 on success, 1 on failure, 2 if no changes to commit
function Invoke-AutoCommit {
    param([string]$Message)
    
    if ([string]::IsNullOrEmpty($Message)) {
        Print-Error "Commit message is required"
        Write-Host "Usage: Invoke-AutoCommit <message>"
        return 1
    }
    
    Print-Info "Staging changes..."
    git add -A
    
    # Check if there are changes to commit
    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) {
        Print-Warning "No changes to commit"
        return 2
    }
    
    Print-Info "Committing changes..."
    git commit -m $Message 2>&1
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Changes committed: $Message"
        return 0
    }
    else {
        Print-Error "Failed to commit changes"
        return 1
    }
}

# ============================================================================
# STASH OPERATIONS
# ============================================================================

# Stash uncommitted changes
# Usage: Invoke-StashChanges
# Returns: $true on success, $false on failure
function Invoke-StashChanges {
    Print-Step "Stashing uncommitted changes..."
    
    # Check if there are any changes to stash
    git diff-index --quiet HEAD -- 2>$null
    $diffResult = $LASTEXITCODE
    $untrackedFiles = git ls-files --others --exclude-standard
    
    if ($diffResult -eq 0 -and -not $untrackedFiles) {
        Print-Info "No uncommitted changes to stash"
        return $true
    }
    
    # Create stash with timestamp
    $stashMessage = "RDD auto-stash $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    
    git stash push -u -m $stashMessage 2>&1
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Changes stashed successfully"
        Debug-Print "Stash message: $stashMessage"
        return $true
    }
    else {
        Print-Error "Failed to stash changes"
        return $false
    }
}

# Restore stashed changes
# Usage: Restore-StashedChanges
# Returns: 0 on success, 1 on failure, 2 if no stash found
function Restore-StashedChanges {
    Print-Step "Restoring stashed changes..."
    
    # Check if there are any RDD auto-stashes
    $stashList = git stash list | Select-String "RDD auto-stash"
    
    if (-not $stashList) {
        Print-Warning "No RDD auto-stash found"
        return 2
    }
    
    # Get the first RDD auto-stash index
    $stashIndex = ($stashList | Select-Object -First 1).LineNumber - 1
    
    # Pop the specific RDD auto-stash
    git stash pop "stash@{$stashIndex}" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Stashed changes restored successfully"
        return 0
    }
    else {
        Print-Error "Failed to restore stashed changes"
        Print-Warning "Changes are still in stash. Use 'git stash list' to see stashes and 'git stash pop' manually."
        return 1
    }
}

# ============================================================================
# MERGE AND SYNC OPERATIONS
# ============================================================================

# Pull latest changes from main branch
# Usage: Invoke-PullMain
# Returns: $true on success, $false on failure
function Invoke-PullMain {
    $defaultBranch = Get-DefaultBranch
    
    Print-Step "Pulling latest changes from origin/${defaultBranch}..."
    
    # First fetch from origin
    git fetch origin $defaultBranch --quiet 2>$null
    if ($LASTEXITCODE -ne 0) {
        Print-Error "Failed to fetch from origin/${defaultBranch}"
        return $false
    }
    
    # Check if local default branch exists
    git show-ref --verify --quiet "refs/heads/${defaultBranch}" 2>$null
    if ($LASTEXITCODE -ne 0) {
        # Local branch doesn't exist, create it from origin
        git branch $defaultBranch "origin/${defaultBranch}" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Created local ${defaultBranch} branch from origin"
            return $true
        }
        else {
            Print-Error "Failed to create local ${defaultBranch} branch"
            return $false
        }
    }
    
    # Try to update local main branch reference (fast-forward only)
    $currentBranch = Get-CurrentBranch
    if ($currentBranch -ne $defaultBranch) {
        # We're not on main, try to fast-forward the local main branch
        git fetch origin "${defaultBranch}:${defaultBranch}" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Updated local ${defaultBranch} branch"
            return $true
        }
        else {
            # Fast-forward failed, just ensure we have the latest from origin
            Print-Success "Fetched latest from origin/${defaultBranch}"
            Debug-Print "Could not fast-forward local ${defaultBranch} (may have local commits)"
            return $true
        }
    }
    else {
        # We're on main, do a regular pull
        git pull origin $defaultBranch 2>&1
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Successfully pulled latest ${defaultBranch}"
            return $true
        }
        else {
            Print-Error "Failed to pull from origin/${defaultBranch}"
            return $false
        }
    }
}

# Merge main into current branch
# Usage: Merge-MainIntoCurrent
# Returns: $true on success, $false on failure (including conflicts)
function Merge-MainIntoCurrent {
    $defaultBranch = Get-DefaultBranch
    $currentBranch = Get-CurrentBranch
    
    # Safety check: don't merge if we're on main
    if ($currentBranch -eq $defaultBranch) {
        Print-Error "Cannot merge ${defaultBranch} into itself"
        return $false
    }
    
    Print-Step "Merging ${defaultBranch} into ${currentBranch}..."
    
    # Attempt merge
    git merge $defaultBranch --no-edit 2>&1
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Successfully merged ${defaultBranch} into ${currentBranch}"
        return $true
    }
    else {
        # Check if it's a conflict
        $conflictedFiles = git ls-files -u | ForEach-Object { $_.Split("`t")[1] } | Sort-Object -Unique
        if ($conflictedFiles) {
            Print-Error "Merge conflicts detected!"
            Write-Host ""
            Print-Warning "Conflicts found in:"
            $conflictedFiles | ForEach-Object { Write-Host "  - $_" }
            Write-Host ""
            Print-Info "Please resolve conflicts manually:"
            Write-Host "  1. Edit conflicted files"
            Write-Host "  2. Stage resolved files: git add <file>"
            Write-Host "  3. Complete merge: git commit"
            Write-Host ""
            return $false
        }
        else {
            Print-Error "Merge failed for unknown reason"
            return $false
        }
    }
}

# Update current branch from main (full workflow)
# Usage: Update-FromMain
# Returns: $true on success, $false on failure
function Update-FromMain {
    $defaultBranch = Get-DefaultBranch
    $currentBranch = Get-CurrentBranch
    
    Print-Banner "Update Branch from ${defaultBranch}"
    Write-Host ""
    Print-Info "Current branch: ${currentBranch}"
    Print-Info "Target: ${defaultBranch}"
    Write-Host ""
    
    # Safety check: don't run on main
    if ($currentBranch -eq $defaultBranch) {
        Print-Error "Cannot update ${defaultBranch} from itself"
        Print-Info "This command is meant to update feature branches with latest ${defaultBranch}"
        return $false
    }
    
    # Step 1: Stash changes
    if (-not (Invoke-StashChanges)) {
        Print-Error "Failed to stash changes. Aborting."
        return $false
    }
    
    # Step 2: Pull latest main
    if (-not (Invoke-PullMain)) {
        Print-Error "Failed to pull latest ${defaultBranch}. Aborting."
        # Try to restore stash
        $restoreResult = Restore-StashedChanges
        if ($restoreResult -ne 0) {
            Print-Error "Also failed to restore stashed changes"
            Print-Warning "Your changes are safely in the stash. Run 'git stash list' to see them."
        }
        return $false
    }
    
    # Step 3: Merge main into current branch
    if (-not (Merge-MainIntoCurrent)) {
        Print-Error "Merge failed. Please resolve conflicts manually."
        Print-Warning "Your changes are still stashed. After resolving conflicts:"
        Write-Host "  1. Complete the merge: git commit"
        Write-Host "  2. Restore your changes: git stash pop"
        return $false
    }
    
    # Step 4: Restore stashed changes
    $restoreResult = Restore-StashedChanges
    
    if ($restoreResult -eq 0) {
        Write-Host ""
        Print-Banner "Update Complete"
        Print-Success "Branch updated from ${defaultBranch}"
        Print-Success "Local changes restored (uncommitted)"
        return $true
    }
    elseif ($restoreResult -eq 2) {
        Write-Host ""
        Print-Banner "Update Complete"
        Print-Success "Branch updated from ${defaultBranch}"
        Print-Info "No stashed changes to restore"
        return $true
    }
    else {
        Write-Host ""
        Print-Warning "Update complete but failed to restore stash"
        Print-Info "Your changes are still in stash. Restore manually with:"
        Write-Host "  git stash pop"
        return $false
    }
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

# Get current branch name
# Usage: Get-CurrentBranch
# Returns: current branch name
function Get-CurrentBranch {
    return git branch --show-current
}

# Get git user information
# Usage: Get-GitUser
# Returns: "Name <email>"
function Get-GitUser {
    $name = git config user.name
    $email = git config user.email
    return "$name <$email>"
}

# Get last commit SHA
# Usage: Get-LastCommitSha
# Returns: commit SHA
function Get-LastCommitSha {
    return git rev-parse HEAD
}

# Get last commit message (first line only)
# Usage: Get-LastCommitMessage
# Returns: commit message
function Get-LastCommitMessage {
    return (git log -1 --pretty=%B | Select-Object -First 1)
}

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

Export-ModuleMember -Function @(
    'Test-GitRepo',
    'Test-UncommittedChanges',
    'Get-DefaultBranch',
    'Invoke-FetchMain',
    'Compare-WithMain',
    'Get-ModifiedFiles',
    'Get-FileDiff',
    'Push-ToRemote',
    'Invoke-AutoCommit',
    'Invoke-StashChanges',
    'Restore-StashedChanges',
    'Invoke-PullMain',
    'Merge-MainIntoCurrent',
    'Update-FromMain',
    'Get-CurrentBranch',
    'Get-GitUser',
    'Get-LastCommitSha',
    'Get-LastCommitMessage'
)

Debug-Print "git-utils.ps1 loaded successfully"
