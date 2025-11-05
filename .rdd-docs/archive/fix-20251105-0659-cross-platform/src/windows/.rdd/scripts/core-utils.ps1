# core-utils.ps1
# Core utility functions for RDD framework
# Provides common utilities used across all RDD scripts
# All functions are exportable for use in other scripts

# Prevent multiple sourcing
if ($global:CORE_UTILS_LOADED) {
    return
}
$global:CORE_UTILS_LOADED = $true

# ============================================================================
# COLOR CODES AND OUTPUT FORMATTING
# ============================================================================

# Color codes for terminal output using .NET Console colors
$script:RED = [ConsoleColor]::Red
$script:GREEN = [ConsoleColor]::Green
$script:YELLOW = [ConsoleColor]::Yellow
$script:BLUE = [ConsoleColor]::Blue
$script:CYAN = [ConsoleColor]::Cyan

# ============================================================================
# COLORED OUTPUT FUNCTIONS
# ============================================================================

# Print success message with green checkmark
# Usage: Print-Success "Operation completed"
function Print-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

# Print error message with red X
# Usage: Print-Error "Operation failed"
function Print-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

# Print warning message with yellow warning symbol
# Usage: Print-Warning "This is a warning"
function Print-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

# Print info message with blue info symbol
# Usage: Print-Info "This is information"
function Print-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Blue
}

# Print step message with cyan arrow
# Usage: Print-Step "Starting process"
function Print-Step {
    param([string]$Message)
    Write-Host "▶ $Message" -ForegroundColor Cyan
}

# Print a formatted banner with custom title
# Usage: Print-Banner "TITLE" "Subtitle"
function Print-Banner {
    param(
        [string]$Title,
        [string]$Subtitle = ""
    )
    
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    
    # Calculate padding for centered title
    $titleLen = $Title.Length
    $totalWidth = 60
    $padding = [math]::Floor(($totalWidth - $titleLen) / 2)
    $paddingStr = " " * $padding
    
    Write-Host "║$paddingStr$Title$paddingStr║" -ForegroundColor Cyan
    
    if ($Subtitle) {
        $subtitleLen = $Subtitle.Length
        $subPadding = [math]::Floor(($totalWidth - $subtitleLen) / 2)
        $subPaddingStr = " " * $subPadding
        Write-Host "║$subPaddingStr$Subtitle$subPaddingStr║" -ForegroundColor Cyan
    }
    
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

# Validate name is in kebab-case format with max 5 words
# Usage: Validate-Name "my-enhancement-name"
# Returns: $true if valid, $false if invalid
function Validate-Name {
    param([string]$Name)
    
    # Check if name is empty
    if ([string]::IsNullOrEmpty($Name)) {
        Print-Error "Name cannot be empty"
        return $false
    }
    
    # Check kebab-case format (lowercase, hyphens only, no spaces)
    if ($Name -notmatch '^[a-z0-9]+(-[a-z0-9]+)*$') {
        Print-Error "Invalid name: '$Name'"
        Print-Error "Must be kebab-case (lowercase, hyphens only, no spaces)"
        Print-Error "Examples: my-enhancement, bug-fix, user-authentication"
        return $false
    }
    
    # Count words (split by hyphen)
    $wordCount = ($Name -split '-').Count
    if ($wordCount -gt 5) {
        Print-Error "Name too long: $wordCount words (maximum 5)"
        Print-Error "Use a shorter, more concise name"
        return $false
    }
    
    return $true
}

# Validate branch name format
# Usage: Validate-BranchName "enh/20231101-1234-my-enhancement"
# Returns: $true if valid, $false if invalid
function Validate-BranchName {
    param([string]$BranchName)
    
    # Check if branch name is empty
    if ([string]::IsNullOrEmpty($BranchName)) {
        Print-Error "Branch name cannot be empty"
        return $false
    }
    
    # Check format: {type}/{timestamp}-{name}
    if ($BranchName -notmatch '^(enh|fix)/[0-9]{8}-[0-9]{4}-.+$') {
        Print-Error "Invalid branch name format: '$BranchName'"
        Print-Error "Expected format: {enh|fix}/{YYYYMMDD-HHmm}-{name}"
        Print-Error "Example: enh/20231101-1234-my-enhancement"
        return $false
    }
    
    return $true
}

# Check if a file exists
# Usage: Validate-FileExists "/path/to/file"
# Returns: $true if exists, $false if not
function Validate-FileExists {
    param(
        [string]$FilePath,
        [string]$FileDescription = "File"
    )
    
    if ([string]::IsNullOrEmpty($FilePath)) {
        Print-Error "File path cannot be empty"
        return $false
    }
    
    if (-not (Test-Path $FilePath -PathType Leaf)) {
        Print-Error "$FileDescription not found: $FilePath"
        return $false
    }
    
    return $true
}

# Check if a directory exists
# Usage: Validate-DirExists "/path/to/dir"
# Returns: $true if exists, $false if not
function Validate-DirExists {
    param(
        [string]$DirPath,
        [string]$DirDescription = "Directory"
    )
    
    if ([string]::IsNullOrEmpty($DirPath)) {
        Print-Error "Directory path cannot be empty"
        return $false
    }
    
    if (-not (Test-Path $DirPath -PathType Container)) {
        Print-Error "$DirDescription not found: $DirPath"
        return $false
    }
    
    return $true
}

# ============================================================================
# CONFIGURATION FUNCTIONS
# ============================================================================

# Find the change config file in workspace
# Returns: path to config file or $null if not found
function Find-ChangeConfig {
    param([string]$WorkspaceDir = ".rdd-docs/workspace")
    
    # Look for .rdd.fix.* or .rdd.enh.* files
    $configFile = Get-ChildItem -Path $WorkspaceDir -Filter ".rdd.fix.*" -File -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $configFile) {
        $configFile = Get-ChildItem -Path $WorkspaceDir -Filter ".rdd.enh.*" -File -ErrorAction SilentlyContinue | Select-Object -First 1
    }
    
    if ($configFile) {
        return $configFile.FullName
    }
    
    return $null
}

# Get configuration value from config file
# Usage: Get-Config "key" "/path/to/config.json"
# Returns: configuration value or $null if not found
function Get-Config {
    param(
        [string]$Key,
        [string]$ConfigFile = ""
    )
    
    # If no config file specified, try to find it
    if ([string]::IsNullOrEmpty($ConfigFile)) {
        $ConfigFile = Find-ChangeConfig ".rdd-docs/workspace"
        if (-not $ConfigFile) {
            return $null
        }
    }
    
    if (-not (Test-Path $ConfigFile)) {
        return $null
    }
    
    try {
        $config = Get-Content $ConfigFile -Raw | ConvertFrom-Json
        return $config.$Key
    }
    catch {
        return $null
    }
}

# Set configuration value in config file
# Usage: Set-Config "key" "value" "/path/to/config.json"
# Returns: $true if successful, $false if failed
function Set-Config {
    param(
        [string]$Key,
        [string]$Value,
        [string]$ConfigFile = ""
    )
    
    if ([string]::IsNullOrEmpty($Key) -or [string]::IsNullOrEmpty($Value)) {
        Print-Error "Key and value are required for Set-Config"
        return $false
    }
    
    # If no config file specified, try to find it
    if ([string]::IsNullOrEmpty($ConfigFile)) {
        $ConfigFile = Find-ChangeConfig ".rdd-docs/workspace"
        if (-not $ConfigFile) {
            Print-Error "No change config file found"
            return $false
        }
    }
    
    # Create config file if it doesn't exist
    if (-not (Test-Path $ConfigFile)) {
        "{}" | Out-File -FilePath $ConfigFile -Encoding utf8
    }
    
    try {
        $config = Get-Content $ConfigFile -Raw | ConvertFrom-Json
        $config | Add-Member -MemberType NoteProperty -Name $Key -Value $Value -Force
        $config | ConvertTo-Json | Set-Content $ConfigFile -Encoding utf8
        return $true
    }
    catch {
        Print-Warning "Failed to update config: $_"
        return $false
    }
}

# ============================================================================
# ERROR HANDLING UTILITIES
# ============================================================================

# Exit with error message
# Usage: Exit-WithError "Error message"
function Exit-WithError {
    param([string]$Message)
    Print-Error $Message
    exit 1
}

# Check exit status and exit with error if non-zero
# Usage: Check-Status $LASTEXITCODE "Operation failed"
function Check-Status {
    param(
        [int]$Status,
        [string]$ErrorMsg = "Command failed"
    )
    
    if ($Status -ne 0) {
        Exit-WithError $ErrorMsg
    }
}

# Confirm action with user
# Usage: Confirm-Action "Delete all files?"
# Returns: $true if yes, $false if no
function Confirm-Action {
    param([string]$Prompt)
    
    $response = Read-Host "$Prompt [y/N]"
    return $response -match '^[Yy]$'
}

# ============================================================================
# HELP MESSAGE GENERATION
# ============================================================================

# Generate a formatted help section
# Usage: Help-Section "SECTION TITLE" "Description of section"
function Help-Section {
    param(
        [string]$Title,
        [string]$Description = ""
    )
    
    Write-Host $Title -ForegroundColor Cyan
    if ($Description) {
        Write-Host "  $Description"
    }
    Write-Host ""
}

# Generate a help command entry
# Usage: Help-Command "command-name" "Description of command" "command --option"
function Help-Command {
    param(
        [string]$Command,
        [string]$Description,
        [string]$Example = ""
    )
    
    Write-Host "  $Command" -ForegroundColor Green
    Write-Host "      $Description"
    if ($Example) {
        Write-Host "      Example: $Example" -ForegroundColor Blue
    }
    Write-Host ""
}

# Generate a help option entry
# Usage: Help-Option "--option, -o" "Description of option"
function Help-Option {
    param(
        [string]$Option,
        [string]$Description
    )
    
    Write-Host "  $Option" -ForegroundColor Yellow
    Write-Host "      $Description"
    Write-Host ""
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

# Get repository root directory
# Returns: absolute path to git repository root
function Get-RepoRoot {
    try {
        $root = git rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -eq 0) {
            return $root
        }
    }
    catch {}
    return $PWD.Path
}

# Check if running in debug mode
# Returns: $true if DEBUG env var is set, $false otherwise
function Test-DebugMode {
    return $env:DEBUG -eq "1"
}

# Debug print (only prints if DEBUG=1)
# Usage: Debug-Print "Debug message"
function Debug-Print {
    param([string]$Message)
    if (Test-DebugMode) {
        Write-Host "[DEBUG] $Message" -ForegroundColor Cyan
    }
}

# Create directory if it doesn't exist
# Usage: Ensure-Dir "/path/to/dir"
function Ensure-Dir {
    param([string]$DirPath)
    
    if (-not (Test-Path $DirPath)) {
        New-Item -ItemType Directory -Path $DirPath -Force | Out-Null
        Debug-Print "Created directory: $DirPath"
    }
}

# Get timestamp in ISO 8601 format
# Returns: timestamp string (e.g., 2023-11-01T12:34:56Z)
function Get-Timestamp {
    return (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
}

# Get timestamp for filenames (no special characters)
# Returns: timestamp string (e.g., 20231101-1234)
function Get-TimestampFilename {
    return Get-Date -Format "yyyyMMdd-HHmm"
}

# Normalize text to kebab-case format
# Handles various inputs: "Add User Auth", "fix_login_bug", "update-README"
# Returns: kebab-case string or $null
# Usage: $normalized = Normalize-ToKebabCase "Add User Auth"
function Normalize-ToKebabCase {
    param([string]$Input)
    
    # Check if input is empty
    if ([string]::IsNullOrEmpty($Input)) {
        return $null
    }
    
    # Normalization steps:
    # 1. Convert to lowercase
    # 2. Replace underscores and spaces with hyphens
    # 3. Remove any characters that aren't lowercase letters, numbers, or hyphens
    # 4. Replace multiple consecutive hyphens with single hyphen
    # 5. Remove leading and trailing hyphens
    
    $normalized = $Input.ToLower()
    $normalized = $normalized -replace '[_\s]', '-'
    $normalized = $normalized -replace '[^a-z0-9-]', ''
    $normalized = $normalized -replace '-+', '-'
    $normalized = $normalized.Trim('-')
    
    # Check if result is empty
    if ([string]::IsNullOrEmpty($normalized)) {
        return $null
    }
    
    return $normalized
}

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

Export-ModuleMember -Function @(
    'Print-Success',
    'Print-Error',
    'Print-Warning',
    'Print-Info',
    'Print-Step',
    'Print-Banner',
    'Validate-Name',
    'Validate-BranchName',
    'Validate-FileExists',
    'Validate-DirExists',
    'Find-ChangeConfig',
    'Get-Config',
    'Set-Config',
    'Exit-WithError',
    'Check-Status',
    'Confirm-Action',
    'Help-Section',
    'Help-Command',
    'Help-Option',
    'Get-RepoRoot',
    'Test-DebugMode',
    'Debug-Print',
    'Ensure-Dir',
    'Get-Timestamp',
    'Get-TimestampFilename',
    'Normalize-ToKebabCase'
)

Debug-Print "core-utils.ps1 loaded successfully"
