# prompt-utils.ps1
# Utility script for prompt management in the RDD framework
# Handles marking prompts as completed and logging execution details

# Prevent multiple sourcing
if ($global:PROMPT_UTILS_LOADED) {
    return
}
$global:PROMPT_UTILS_LOADED = $true

# Source dependencies
$script:SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$coreUtilsPath = Join-Path $SCRIPT_DIR "core-utils.ps1"
if (Test-Path $coreUtilsPath) {
    . $coreUtilsPath
}

# Get repository root and workspace directory
$script:REPO_ROOT = Get-RepoRoot
$script:WORKSPACE_DIR = "$REPO_ROOT/.rdd-docs/workspace"

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT COMPLETION FUNCTIONS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Mark a stand-alone prompt as completed in .rdd.copilot-prompts.md
# Changes checkbox from "- [ ]" to "- [x]"
# Arguments:
#   $1 - prompt_id: The ID of the prompt (e.g., P001, P002)
#   $2 - journal_file: Path to .rdd.copilot-prompts.md (optional)
# Returns: $true on success, $false on error
function Set-PromptCompleted {
    param(
        [string]$PromptId,
        [string]$JournalFile = "$script:WORKSPACE_DIR/.rdd.copilot-prompts.md"
    )
    
    # Validate prompt ID is provided
    if ([string]::IsNullOrEmpty($PromptId)) {
        Print-Error "Prompt ID is required"
        Write-Host "Usage: Set-PromptCompleted <prompt-id> [journal-file]"
        return $false
    }
    
    # Check if journal file exists
    if (-not (Test-Path $JournalFile)) {
        Print-Error ".rdd.copilot-prompts.md not found at: $JournalFile"
        return $false
    }
    
    # Read file content
    $content = Get-Content $JournalFile -Raw
    
    # Check if the prompt exists and is not already completed
    if ($content -match "^\s*-\s*\[\s*\]\s*\[$PromptId\]") {
        # Mark the prompt as completed
        $content = $content -replace "(?m)^(\s*-\s*)\[\s*\](\s*\[\s*$PromptId\s*\])", '${1}[x]${2}'
        Set-Content -Path $JournalFile -Value $content -Encoding utf8
        Print-Success "Marked prompt $PromptId as completed"
        return $true
    }
    elseif ($content -match "^\s*-\s*\[x\]\s*\[$PromptId\]") {
        Print-Warning "Prompt $PromptId is already marked as completed"
        return $true
    }
    else {
        Print-Error "Prompt $PromptId not found in .rdd.copilot-prompts.md"
        return $false
    }
}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT EXECUTION LOGGING
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Log prompt execution details to log.jsonl
# Creates a structured JSONL entry with timestamp, promptId, executionDetails, sessionId
# Arguments:
#   $1 - prompt_id: The ID of the executed prompt
#   $2 - execution_details: Full content describing what was executed
#   $3 - session_id: Optional session identifier
# Returns: $true on success, $false on error
function Add-PromptExecution {
    param(
        [string]$PromptId,
        [string]$ExecutionDetails,
        [string]$SessionId = ""
    )
    
    if ([string]::IsNullOrEmpty($SessionId)) {
        $SessionId = "exec-$(Get-Date -Format 'yyyyMMdd-HHmm')"
    }
    
    $logFile = "$script:WORKSPACE_DIR/log.jsonl"
    
    # Validate required parameters
    if ([string]::IsNullOrEmpty($PromptId)) {
        Print-Error "Prompt ID is required for logging"
        Write-Host "Usage: Add-PromptExecution <prompt-id> <execution-details> [session-id]"
        return $false
    }
    
    if ([string]::IsNullOrEmpty($ExecutionDetails)) {
        Print-Error "Execution details are required for logging"
        Write-Host "Usage: Add-PromptExecution <prompt-id> <execution-details> [session-id]"
        return $false
    }
    
    # Ensure workspace directory exists
    Ensure-Dir $script:WORKSPACE_DIR
    
    # Create log file if it doesn't exist
    if (-not (Test-Path $logFile)) {
        New-Item -ItemType File -Path $logFile -Force | Out-Null
        Print-Success "Created log file: $logFile"
    }
    
    # Create JSON line entry
    $timestamp = Get-Timestamp
    $entry = @{
        timestamp = $timestamp
        promptId = $PromptId
        executionDetails = $ExecutionDetails
        sessionId = $SessionId
    } | ConvertTo-Json -Compress
    
    Add-Content -Path $logFile -Value $entry -Encoding utf8
    
    Print-Success "Logged execution details for prompt $PromptId to $logFile"
    return $true
}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT LISTING AND FILTERING
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# List prompts from .rdd.copilot-prompts.md filtered by status
# Arguments:
#   $1 - status: Filter by status ('unchecked', 'checked', 'all')
#   $2 - journal_file: Path to .rdd.copilot-prompts.md (optional)
# Returns: $true on success, $false on error
function Get-Prompts {
    param(
        [string]$Status = "all",
        [string]$JournalFile = "$script:WORKSPACE_DIR/.rdd.copilot-prompts.md"
    )
    
    # Validate status parameter
    if ($Status -notmatch '^(unchecked|checked|all)$') {
        Print-Error "Invalid status filter: '$Status'"
        Write-Host "Valid options: unchecked, checked, all"
        return $false
    }
    
    # Check if journal file exists
    if (-not (Test-Path $JournalFile)) {
        Print-Error ".rdd.copilot-prompts.md not found at: $JournalFile"
        return $false
    }
    
    # Print header
    Print-Banner "PROMPTS LIST ($Status)"
    
    # Read and filter content
    $content = Get-Content $JournalFile
    
    # Filter and display based on status
    switch ($Status) {
        "unchecked" {
            $content | Where-Object { $_ -match '^\s*-\s*\[\s*\]\s*\[P[0-9]+\]' } | ForEach-Object {
                if ($_ -match '\[P([0-9]+)\]\s*(.*)') {
                    $promptId = "P$($matches[1])"
                    $promptTitle = $matches[2].Trim().Substring(0, [Math]::Min(80, $matches[2].Trim().Length))
                    Write-Host "  ☐ [$promptId] $promptTitle"
                }
            }
        }
        "checked" {
            $content | Where-Object { $_ -match '^\s*-\s*\[x\]\s*\[P[0-9]+\]' } | ForEach-Object {
                if ($_ -match '\[P([0-9]+)\]\s*(.*)') {
                    $promptId = "P$($matches[1])"
                    $promptTitle = $matches[2].Trim().Substring(0, [Math]::Min(80, $matches[2].Trim().Length))
                    Write-Host "  ☑ [$promptId] $promptTitle"
                }
            }
        }
        "all" {
            $content | Where-Object { $_ -match '^\s*-\s*\[[x ]\]\s*\[P[0-9]+\]' } | ForEach-Object {
                if ($_ -match '\[P([0-9]+)\]\s*(.*)') {
                    $promptId = "P$($matches[1])"
                    $promptTitle = $matches[2].Trim().Substring(0, [Math]::Min(80, $matches[2].Trim().Length))
                    $checkbox = if ($_ -match '\[x\]') { "☑" } else { "☐" }
                    Write-Host "  $checkbox [$promptId] $promptTitle"
                }
            }
        }
    }
    
    # Print summary
    $totalCount = ($content | Where-Object { $_ -match '^\s*-\s*\[[x ]\]\s*\[P[0-9]+\]' } | Measure-Object).Count
    $checkedCount = ($content | Where-Object { $_ -match '^\s*-\s*\[x\]\s*\[P[0-9]+\]' } | Measure-Object).Count
    $uncheckedCount = $totalCount - $checkedCount
    
    Write-Host ""
    Print-Info "Summary: $checkedCount completed, $uncheckedCount pending, $totalCount total"
    
    return $true
}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROMPT VALIDATION
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Validate prompt status in copilot-prompts.md
# Checks if a prompt exists and returns its status
# Arguments:
#   $1 - prompt_id: The ID of the prompt to check
#   $2 - journal_file: Path to copilot-prompts.md (optional)
# Returns: 0 if unchecked, 1 if checked, 2 if not found, 3 if file not found
function Test-PromptStatus {
    param(
        [string]$PromptId,
        [string]$JournalFile = "$script:WORKSPACE_DIR/.rdd.copilot-prompts.md"
    )
    
    # Validate prompt ID is provided
    if ([string]::IsNullOrEmpty($PromptId)) {
        Print-Error "Prompt ID is required"
        Write-Host "Usage: Test-PromptStatus <prompt-id> [journal-file]"
        return 3
    }
    
    # Check if journal file exists
    if (-not (Test-Path $JournalFile)) {
        Print-Error "copilot-prompts.md not found at: $JournalFile"
        return 3
    }
    
    # Read content
    $content = Get-Content $JournalFile -Raw
    
    # Check if prompt exists and get its status
    if ($content -match "^\s*-\s*\[\s*\]\s*\[$PromptId\]") {
        Print-Info "Prompt $PromptId exists and is unchecked (pending)"
        return 0
    }
    elseif ($content -match "^\s*-\s*\[x\]\s*\[$PromptId\]") {
        Print-Info "Prompt $PromptId exists and is checked (completed)"
        return 1
    }
    else {
        Print-Warning "Prompt $PromptId not found in copilot-prompts.md"
        return 2
    }
}

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

Export-ModuleMember -Function @(
    'Set-PromptCompleted',
    'Add-PromptExecution',
    'Get-Prompts',
    'Test-PromptStatus'
)

Debug-Print "prompt-utils.ps1 loaded successfully"
