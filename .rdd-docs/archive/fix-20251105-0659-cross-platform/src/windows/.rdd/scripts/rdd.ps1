# rdd.ps1
# Main wrapper script for RDD framework
# Provides domain-based routing to all utility scripts

# Version information
$script:RDD_VERSION = "1.0.0"

# Get the directory where this script is located
$script:SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

# Source all utility scripts
. (Join-Path $SCRIPT_DIR "core-utils.ps1")
. (Join-Path $SCRIPT_DIR "git-utils.ps1")
. (Join-Path $SCRIPT_DIR "workspace-utils.ps1")
. (Join-Path $SCRIPT_DIR "branch-utils.ps1")
. (Join-Path $SCRIPT_DIR "requirements-utils.ps1")
. (Join-Path $SCRIPT_DIR "clarify-utils.ps1")
. (Join-Path $SCRIPT_DIR "prompt-utils.ps1")
. (Join-Path $SCRIPT_DIR "change-utils.ps1")

# ============================================================================
# HELP SYSTEM
# ============================================================================

function Show-Version {
    Write-Host "RDD Framework v$script:RDD_VERSION"
}

function Show-MainHelp {
    Print-Banner "RDD Framework - Requirements-Driven Development"
    Write-Host ""
    Write-Host "Usage: .\rdd.ps1 <domain> <action> [options]"
    Write-Host ""
    Write-Host "Domains:"
    Write-Host "  branch        Branch management operations"
    Write-Host "  workspace     Workspace initialization and management"
    Write-Host "  requirements  Requirements validation and merging"
    Write-Host "  change        Change workflow management"
    Write-Host "  fix           Fix workflow management"
    Write-Host "  clarify       Clarification phase operations"
    Write-Host "  prompt        Stand-alone prompt management"
    Write-Host "  git           Git operations and comparisons"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  --help, -h    Show this help message"
    Write-Host "  --version, -v Show version information"
    Write-Host ""
    Write-Host "For domain-specific help, use: .\rdd.ps1 <domain> --help"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\rdd.ps1 change create my-enhancement enh"
    Write-Host "  .\rdd.ps1 branch delete my-branch"
    Write-Host "  .\rdd.ps1 requirements merge"
}

function Show-BranchHelp {
    Print-Banner "Branch Management"
    Write-Host ""
    Write-Host "Usage: .\rdd.ps1 branch <action> [options]"
    Write-Host ""
    Write-Host "Actions:"
    Write-Host "  create <type> <name>    Create new branch (type: enh|fix)"
    Write-Host "  delete [name] [-Force]  Delete branch (current if name omitted)"
    Write-Host "  delete-merged           Delete all merged branches"
    Write-Host "  cleanup [name]          Post-merge cleanup"
    Write-Host "  status <name>           Check merge status of branch"
    Write-Host "  list [filter]           List branches"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\rdd.ps1 branch create enh my-enhancement"
    Write-Host "  .\rdd.ps1 branch delete my-old-branch"
}

function Show-WorkspaceHelp {
    Print-Banner "Workspace Management"
    Write-Host ""
    Write-Host "Usage: .\rdd.ps1 workspace <action> [options]"
    Write-Host ""
    Write-Host "Actions:"
    Write-Host "  init <type>        Initialize workspace (type: change|fix)"
    Write-Host "  archive [-Keep]    Archive current workspace"
    Write-Host "  backup             Create backup of workspace"
    Write-Host "  restore            Restore from latest backup"
    Write-Host "  clear              Clear workspace with confirmation"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\rdd.ps1 workspace init change"
    Write-Host "  .\rdd.ps1 workspace archive -Keep"
}

function Show-RequirementsHelp {
    Print-Banner "Requirements Management"
    Write-Host ""
    Write-Host "Usage: .\rdd.ps1 requirements <action> [options]"
    Write-Host ""
    Write-Host "Actions:"
    Write-Host "  validate              Validate requirements-changes.md format"
    Write-Host "  merge [-DryRun]       Merge requirements changes"
    Write-Host "  preview               Preview requirements merge"
    Write-Host "  analyze               Analyze requirements impact"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\rdd.ps1 requirements validate"
    Write-Host "  .\rdd.ps1 requirements merge -DryRun"
}

function Show-ChangeHelp {
    Print-Banner "Change Workflow"
    Write-Host ""
    Write-Host "Usage: .\rdd.ps1 change <action> [options]"
    Write-Host ""
    Write-Host "Actions:"
    Write-Host "  create [type]         Create new change (type: enh|fix)"
    Write-Host "  wrap-up               Complete change workflow"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\rdd.ps1 change create enh"
    Write-Host "  .\rdd.ps1 change wrap-up"
}

function Show-GitHelp {
    Print-Banner "Git Operations"
    Write-Host ""
    Write-Host "Usage: .\rdd.ps1 git <action> [options]"
    Write-Host ""
    Write-Host "Actions:"
    Write-Host "  compare           Compare current branch with main"
    Write-Host "  modified-files    List modified files"
    Write-Host "  file-diff <file>  Show diff for specific file"
    Write-Host "  push              Push current branch to remote"
    Write-Host "  update-from-main  Update current branch from main"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\rdd.ps1 git compare"
    Write-Host "  .\rdd.ps1 git update-from-main"
}

# ============================================================================
# DOMAIN ROUTING
# ============================================================================

function Invoke-BranchCommand {
    param([string[]]$Args)
    
    if ($Args.Length -eq 0) {
        Show-BranchHelp
        return
    }
    
    $action = $Args[0]
    
    switch ($action) {
        "create" {
            if ($Args.Length -lt 3) {
                Print-Error "Branch type and name required"
                Write-Host "Usage: .\rdd.ps1 branch create <type> <name>"
                return
            }
            New-Branch $Args[1] $Args[2]
        }
        "delete" {
            $force = $Args -contains "-Force"
            $branchName = $Args | Where-Object { $_ -ne "delete" -and $_ -ne "-Force" } | Select-Object -First 1
            Remove-Branch $branchName $force $false
        }
        "delete-merged" {
            Remove-MergedBranches
        }
        "cleanup" {
            $branchName = if ($Args.Length -gt 1) { $Args[1] } else { "" }
            Invoke-CleanupAfterMerge $branchName
        }
        "status" {
            if ($Args.Length -lt 2) {
                Print-Error "Branch name required"
                return
            }
            Test-MergeStatus $Args[1]
        }
        "list" {
            $filter = if ($Args.Length -gt 1) { $Args[1] } else { "local" }
            Get-Branches $filter
        }
        { $_ -in "--help", "-h" } {
            Show-BranchHelp
        }
        default {
            Print-Error "Unknown branch action: $action"
            Show-BranchHelp
        }
    }
}

function Invoke-WorkspaceCommand {
    param([string[]]$Args)
    
    if ($Args.Length -eq 0) {
        Show-WorkspaceHelp
        return
    }
    
    $action = $Args[0]
    
    switch ($action) {
        "init" {
            if ($Args.Length -lt 2) {
                Print-Error "Workspace type required (change|fix)"
                return
            }
            Initialize-Workspace $Args[1]
        }
        "archive" {
            $keep = $Args -contains "-Keep"
            $branchName = Get-CurrentBranch
            Invoke-ArchiveWorkspace $branchName $keep
        }
        "backup" {
            Backup-Workspace
        }
        "restore" {
            Restore-Workspace
        }
        "clear" {
            Clear-Workspace
        }
        { $_ -in "--help", "-h" } {
            Show-WorkspaceHelp
        }
        default {
            Print-Error "Unknown workspace action: $action"
            Show-WorkspaceHelp
        }
    }
}

function Invoke-RequirementsCommand {
    param([string[]]$Args)
    
    if ($Args.Length -eq 0) {
        Show-RequirementsHelp
        return
    }
    
    $action = $Args[0]
    
    switch ($action) {
        "validate" {
            Test-Requirements
        }
        "merge" {
            $dryRun = $Args -contains "-DryRun"
            Merge-Requirements $dryRun $true
        }
        "preview" {
            Show-RequirementsMergePreview
        }
        "analyze" {
            Get-RequirementsImpact
        }
        { $_ -in "--help", "-h" } {
            Show-RequirementsHelp
        }
        default {
            Print-Error "Unknown requirements action: $action"
            Show-RequirementsHelp
        }
    }
}

function Invoke-ChangeCommand {
    param([string[]]$Args)
    
    if ($Args.Length -eq 0) {
        Show-ChangeHelp
        return
    }
    
    $action = $Args[0]
    
    switch ($action) {
        "create" {
            # Interactive creation
            Write-Host ""
            Write-Host "─── RDD-COPILOT ───"
            Write-Host " Prompt: Create Change"
            Write-Host " Description:"
            Write-Host " > Create a new Change folder with timestamped naming,"
            Write-Host " > branch setup, and template initialization."
            Write-Host ""
            Write-Host " User Action:"
            Write-Host " > Provide a short description and name for the change."
            Write-Host "───────────────"
            Write-Host ""
            
            $changeName = Read-Host "Enter change name (will be normalized to kebab-case)"
            if ([string]::IsNullOrEmpty($changeName)) {
                Print-Error "Change name cannot be empty"
                return
            }
            
            $normalizedName = Normalize-ToKebabCase $changeName
            if (-not $normalizedName) {
                Print-Error "Unable to normalize name"
                return
            }
            
            Print-Success "Normalized name: $normalizedName"
            $confirm = Read-Host "Use this name? (y/n)"
            if ($confirm -notmatch '^[Yy]') {
                Print-Info "Operation cancelled"
                return
            }
            
            $changeType = if ($Args.Length -gt 1) { $Args[1] } else { "enh" }
            New-Change $normalizedName $changeType
        }
        "wrap-up" {
            Complete-Change
        }
        { $_ -in "--help", "-h" } {
            Show-ChangeHelp
        }
        default {
            Print-Error "Unknown change action: $action"
            Show-ChangeHelp
        }
    }
}

function Invoke-GitCommand {
    param([string[]]$Args)
    
    if ($Args.Length -eq 0) {
        Show-GitHelp
        return
    }
    
    $action = $Args[0]
    
    switch ($action) {
        "compare" {
            Compare-WithMain
        }
        "modified-files" {
            Get-ModifiedFiles
        }
        "file-diff" {
            if ($Args.Length -lt 2) {
                Print-Error "File path required"
                return
            }
            Get-FileDiff $Args[1]
        }
        "push" {
            $branchName = Get-CurrentBranch
            Push-ToRemote $branchName
        }
        "update-from-main" {
            Update-FromMain
        }
        { $_ -in "--help", "-h" } {
            Show-GitHelp
        }
        default {
            Print-Error "Unknown git action: $action"
            Show-GitHelp
        }
    }
}

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

function Main {
    param([string[]]$Args)
    
    # Handle no arguments
    if ($Args.Length -eq 0) {
        Show-MainHelp
        return
    }
    
    # Handle global options
    if ($Args[0] -in "--version", "-v") {
        Show-Version
        return
    }
    
    if ($Args[0] -in "--help", "-h") {
        Show-MainHelp
        return
    }
    
    # Route to domain handler
    $domain = $Args[0]
    $domainArgs = $Args[1..($Args.Length-1)]
    
    switch ($domain) {
        "branch" {
            Invoke-BranchCommand $domainArgs
        }
        "workspace" {
            Invoke-WorkspaceCommand $domainArgs
        }
        "requirements" {
            Invoke-RequirementsCommand $domainArgs
        }
        "change" {
            Invoke-ChangeCommand $domainArgs
        }
        "git" {
            Invoke-GitCommand $domainArgs
        }
        default {
            Print-Error "Unknown domain: $domain"
            Write-Host ""
            Write-Host "Available domains: branch, workspace, requirements, change, git"
            Write-Host ""
            Write-Host "Use '.\rdd.ps1 --help' for more information"
        }
    }
}

# Run main function with all arguments
Main $args
