# clarify-utils.ps1
# Clarification management utility functions for RDD framework
# Provides initialization, logging, and template management for clarification phase

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

# Source workspace-utils.ps1 for workspace operations
$workspaceUtilsPath = Join-Path $SCRIPT_DIR "workspace-utils.ps1"
if (Test-Path $workspaceUtilsPath) {
    . $workspaceUtilsPath
}
else {
    Write-Error "ERROR: workspace-utils.ps1 not found. Please ensure it exists in the same directory."
    exit 1
}

# Prevent multiple sourcing
if ($global:CLARIFY_UTILS_LOADED) {
    return
}
$global:CLARIFY_UTILS_LOADED = $true

# ============================================================================
# CONSTANTS
# ============================================================================

$script:WORKSPACE_DIR = ".rdd-docs/workspace"
$script:CLARITY_TAXONOMY_SOURCE = ".rdd-docs/clarity-checklist.md"
$script:CLARITY_TAXONOMY_WORKSPACE = "$WORKSPACE_DIR/clarity-checklist.md"

# ============================================================================
# CLARIFICATION INITIALIZATION
# ============================================================================

# Initialize clarification phase in workspace
# Usage: Initialize-Clarification
# Returns: $true on success, $false on failure
function Initialize-Clarification {
    Print-Banner "INITIALIZE CLARIFICATION PHASE"
    Write-Host ""
    
    # Ensure workspace directory exists
    Ensure-Dir $script:WORKSPACE_DIR
    
    # Copy clarity-checklist.md
    if (-not (Copy-Taxonomy)) {
        Print-Warning "Failed to copy checklist, continuing anyway..."
    }
    Write-Host ""
     
    # Update phase in change config file if it exists
    $currentChangeFile = Find-ChangeConfig $script:WORKSPACE_DIR
    if ($currentChangeFile -and (Test-Path $currentChangeFile)) {
        try {
            $config = Get-Content $currentChangeFile -Raw | ConvertFrom-Json
            $config.phase = "clarify"
            $config | ConvertTo-Json | Set-Content $currentChangeFile -Encoding utf8
            Print-Success "Updated phase to 'clarify' in change config"
        }
        catch {
            Debug-Print "Failed to update phase in config"
        }
    }
    
    Write-Host ""
    Print-Success "Clarification phase initialized successfully"
    Write-Host ""
    Print-Info "Next steps:"
    Write-Host "  1. Review clarity-checklist.md for question categories"
    Write-Host "  2. Add questions to open-questions.md"
    Write-Host "  3. Log clarifications using Add-Clarification"
    
    return $true
}

# ============================================================================
# CLARIFICATION LOGGING
# ============================================================================

# Log a clarification Q&A entry to JSONL file
# Usage: Add-Clarification "question" "answer" [answered_by] [session_id]
# answered_by defaults to "user"
# session_id defaults to "clarify-YYYYMMDD-HHmm"
# Returns: $true on success, $false on failure
function Add-Clarification {
    param(
        [string]$Question,
        [string]$Answer,
        [string]$AnsweredBy = "user",
        [string]$SessionId = ""
    )
    
    if ([string]::IsNullOrEmpty($Question) -or [string]::IsNullOrEmpty($Answer)) {
        Print-Error "Question and answer are required"
        Write-Host "Usage: Add-Clarification <question> <answer> [answered_by] [session_id]"
        return $false
    }
    
    if ([string]::IsNullOrEmpty($SessionId)) {
        $SessionId = "clarify-$(Get-Date -Format 'yyyyMMdd-HHmm')"
    }
    
    $clarificationLog = Join-Path $script:WORKSPACE_DIR "log.jsonl"
    
    # Ensure workspace directory and log file exist
    Ensure-Dir $script:WORKSPACE_DIR
    if (-not (Test-Path $clarificationLog)) {
        New-Item -ItemType File -Path $clarificationLog -Force | Out-Null
    }
    
    # Create JSON entry
    $timestamp = Get-Timestamp
    $entry = @{
        timestamp = $timestamp
        question = $Question
        answer = $Answer
        answeredBy = $AnsweredBy
        sessionId = $SessionId
    } | ConvertTo-Json -Compress
    
    # Append to log file
    Add-Content -Path $clarificationLog -Value $entry -Encoding utf8
    
    Print-Success "Logged clarification entry"
    Debug-Print "Session: $SessionId, Answered by: $AnsweredBy"
    
    return $true
}

# ============================================================================
# TAXONOMY MANAGEMENT
# ============================================================================

# Copy clarity-checklist.md from .rdd-docs to workspace
# Usage: Copy-Taxonomy
# Returns: $true on success, $false on failure
function Copy-Taxonomy {
    if (-not (Test-Path $script:CLARITY_TAXONOMY_SOURCE)) {
        Print-Error "clarity-checklist.md not found: $script:CLARITY_TAXONOMY_SOURCE"
        Print-Info "Please ensure the taxonomy file exists in .rdd-docs/"
        return $false
    }
    
    Ensure-Dir $script:WORKSPACE_DIR
    
    # Check if already exists
    if (Test-Path $script:CLARITY_TAXONOMY_WORKSPACE) {
        Print-Warning "clarity-checklist.md already exists in workspace"
        if (-not (Confirm-Action "Overwrite existing taxonomy?")) {
            Print-Info "Copy cancelled"
            return $true
        }
    }
    
    Copy-Item -Path $script:CLARITY_TAXONOMY_SOURCE -Destination $script:CLARITY_TAXONOMY_WORKSPACE -Force
    Print-Success "Copied clarity-checklist.md to workspace"
    
    return $true
}

# ============================================================================
# CLARIFICATION INSPECTION
# ============================================================================

# Display clarification log entries
# Usage: Show-Clarifications [session_id]
# If session_id provided, filters by that session
# Returns: $true on success
function Show-Clarifications {
    param([string]$SessionId = "")
    
    $clarificationLog = Join-Path $script:WORKSPACE_DIR "log.jsonl"
    
    if (-not (Test-Path $clarificationLog)) {
        Print-Warning "No clarification log found"
        return $true
    }
    
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host "  CLARIFICATION LOG"
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host ""
    
    $entries = Get-Content $clarificationLog | ForEach-Object {
        $_ | ConvertFrom-Json
    }
    
    if (-not [string]::IsNullOrEmpty($SessionId)) {
        Print-Info "Filtering by session: $SessionId"
        Write-Host ""
        $entries = $entries | Where-Object { $_.sessionId -eq $SessionId }
    }
    
    foreach ($entry in $entries) {
        Write-Host "[$($entry.timestamp)] $($entry.answeredBy)"
        Write-Host "  Q: $($entry.question)"
        Write-Host "  A: $($entry.answer)"
        Write-Host ""
    }
    
    $entryCount = ($entries | Measure-Object).Count
    Print-Info "Total entries: $entryCount"
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return $true
}

# Count clarification entries
# Usage: Get-ClarificationCount [session_id]
# Returns: count
function Get-ClarificationCount {
    param([string]$SessionId = "")
    
    $clarificationLog = Join-Path $script:WORKSPACE_DIR "log.jsonl"
    
    if (-not (Test-Path $clarificationLog)) {
        return 0
    }
    
    $entries = Get-Content $clarificationLog | ForEach-Object {
        $_ | ConvertFrom-Json
    }
    
    if (-not [string]::IsNullOrEmpty($SessionId)) {
        $entries = $entries | Where-Object { $_.sessionId -eq $SessionId }
    }
    
    return ($entries | Measure-Object).Count
}

# Get clarification status summary
# Usage: Get-ClarificationStatus
# Returns: $true on success
function Get-ClarificationStatus {
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host "  CLARIFICATION STATUS"
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host ""
    
    $clarificationLog = Join-Path $script:WORKSPACE_DIR "log.jsonl"
    
    # Check if clarification log exists
    if (Test-Path $clarificationLog) {
        $entryCount = Get-ClarificationCount
        Print-Success "Clarification log exists"
        Print-Info "Total entries: $entryCount"
    }
    else {
        Print-Warning "Clarification log not found"
    }
    Write-Host ""
    
    # Check if open-questions.md exists
    $openQuestionsPath = Join-Path $script:WORKSPACE_DIR "open-questions.md"
    if (Test-Path $openQuestionsPath) {
        Print-Success "open-questions.md exists"
        
        # Count question statuses
        $content = Get-Content $openQuestionsPath -Raw
        $openCount = ([regex]::Matches($content, '^\-\s*\[\s*\]')).Count
        $partialCount = ([regex]::Matches($content, '^\-\s*\[\?\]')).Count
        $answeredCount = ([regex]::Matches($content, '^\-\s*\[x\]')).Count
        
        Print-Info "Questions status:"
        Write-Host "  [ ] Open: $openCount"
        Write-Host "  [?] Partial: $partialCount"
        Write-Host "  [x] Answered: $answeredCount"
    }
    else {
        Print-Warning "open-questions.md not found"
    }
    Write-Host ""
    
    # Check if taxonomy exists
    if (Test-Path $script:CLARITY_TAXONOMY_WORKSPACE) {
        Print-Success "clarity-checklist.md available in workspace"
    }
    else {
        Print-Warning "clarity-checklist.md not found in workspace"
    }
    
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    return $true
}

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

Export-ModuleMember -Function @(
    'Initialize-Clarification',
    'Add-Clarification',
    'Copy-Taxonomy',
    'Show-Clarifications',
    'Get-ClarificationCount',
    'Get-ClarificationStatus'
)

Debug-Print "clarify-utils.ps1 loaded successfully"
