#!/bin/bash

# core-utils.sh
# Core utility functions for RDD framework
# Provides common utilities used across all RDD scripts
# All functions are exportable for use in other scripts

# Prevent multiple sourcing
if [ -n "$CORE_UTILS_LOADED" ]; then
    return 0
fi
CORE_UTILS_LOADED=1

# ============================================================================
# COLOR CODES AND OUTPUT FORMATTING
# ============================================================================

# Color codes for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ============================================================================
# COLORED OUTPUT FUNCTIONS
# ============================================================================

# Print success message with green checkmark
# Usage: print_success "Operation completed"
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Print error message with red X
# Usage: print_error "Operation failed"
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Print warning message with yellow warning symbol
# Usage: print_warning "This is a warning"
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Print info message with blue info symbol
# Usage: print_info "This is information"
print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Print step message with cyan arrow
# Usage: print_step "Starting process"
print_step() {
    echo -e "${CYAN}▶${NC} $1"
}

# Print a formatted banner with custom title
# Usage: print_banner "TITLE" "Subtitle"
print_banner() {
    local title="$1"
    local subtitle="${2:-}"
    
    echo -e "${CYAN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════╗"
    
    # Calculate padding for centered title
    local title_len=${#title}
    local total_width=60
    local padding=$(( (total_width - title_len) / 2 ))
    local padding_str=$(printf '%*s' "$padding" '')
    
    echo "║${padding_str}${title}${padding_str}║"
    
    if [ -n "$subtitle" ]; then
        local subtitle_len=${#subtitle}
        local sub_padding=$(( (total_width - subtitle_len) / 2 ))
        local sub_padding_str=$(printf '%*s' "$sub_padding" '')
        echo "║${sub_padding_str}${subtitle}${sub_padding_str}║"
    fi
    
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

# Validate name is in kebab-case format with max 5 words
# Usage: validate_name "my-enhancement-name"
# Returns: 0 if valid, 1 if invalid
validate_name() {
    local name="$1"
    
    # Check if name is empty
    if [ -z "$name" ]; then
        print_error "Name cannot be empty"
        return 1
    fi
    
    # Check kebab-case format (lowercase, hyphens only, no spaces)
    if [[ ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
        print_error "Invalid name: '$name'"
        print_error "Must be kebab-case (lowercase, hyphens only, no spaces)"
        print_error "Examples: my-enhancement, bug-fix, user-authentication"
        return 1
    fi
    
    # Count words (split by hyphen)
    local word_count=$(echo "$name" | tr '-' '\n' | wc -l)
    if [ "$word_count" -gt 5 ]; then
        print_error "Name too long: $word_count words (maximum 5)"
        print_error "Use a shorter, more concise name"
        return 1
    fi
    
    return 0
}

# Validate branch name format
# Usage: validate_branch_name "enh/20231101-1234-my-enhancement"
# Returns: 0 if valid, 1 if invalid
validate_branch_name() {
    local branch_name="$1"
    
    # Check if branch name is empty
    if [ -z "$branch_name" ]; then
        print_error "Branch name cannot be empty"
        return 1
    fi
    
    # Check format: {type}/{timestamp}-{name}
    # Where type is enh or fix
    if [[ ! "$branch_name" =~ ^(enh|fix)/[0-9]{8}-[0-9]{4}-.+$ ]]; then
        print_error "Invalid branch name format: '$branch_name'"
        print_error "Expected format: {enh|fix}/{YYYYMMDD-HHmm}-{name}"
        print_error "Example: enh/20231101-1234-my-enhancement"
        return 1
    fi
    
    return 0
}

# Check if a file exists
# Usage: validate_file_exists "/path/to/file"
# Returns: 0 if exists, 1 if not
validate_file_exists() {
    local file_path="$1"
    local file_description="${2:-File}"
    
    if [ -z "$file_path" ]; then
        print_error "File path cannot be empty"
        return 1
    fi
    
    if [ ! -f "$file_path" ]; then
        print_error "$file_description not found: $file_path"
        return 1
    fi
    
    return 0
}

# Check if a directory exists
# Usage: validate_dir_exists "/path/to/dir"
# Returns: 0 if exists, 1 if not
validate_dir_exists() {
    local dir_path="$1"
    local dir_description="${2:-Directory}"
    
    if [ -z "$dir_path" ]; then
        print_error "Directory path cannot be empty"
        return 1
    fi
    
    if [ ! -d "$dir_path" ]; then
        print_error "$dir_description not found: $dir_path"
        return 1
    fi
    
    return 0
}

# ============================================================================
# CONFIGURATION FUNCTIONS
# ============================================================================

# Get configuration value from config file
# Usage: get_config "key" "/path/to/config.json"
# Returns: configuration value or empty string if not found
get_config() {
    local key="$1"
    local config_file="${2:-.rdd-docs/workspace/.current-change}"
    
    if [ ! -f "$config_file" ]; then
        return 1
    fi
    
    # Use jq if available for JSON files
    if command -v jq &> /dev/null && [[ "$config_file" == *.json ]]; then
        jq -r ".$key // empty" "$config_file" 2>/dev/null
    else
        # Fallback: simple grep for key-value pairs
        grep "\"$key\"" "$config_file" 2>/dev/null | sed 's/.*: *"\([^"]*\)".*/\1/' | head -n 1
    fi
}

# Set configuration value in config file
# Usage: set_config "key" "value" "/path/to/config.json"
# Returns: 0 if successful, 1 if failed
set_config() {
    local key="$1"
    local value="$2"
    local config_file="${3:-.rdd-docs/workspace/.current-change}"
    
    if [ -z "$key" ] || [ -z "$value" ]; then
        print_error "Key and value are required for set_config"
        return 1
    fi
    
    # Create config file if it doesn't exist
    if [ ! -f "$config_file" ]; then
        echo "{}" > "$config_file"
    fi
    
    # Use jq if available for JSON files
    if command -v jq &> /dev/null && [[ "$config_file" == *.json ]]; then
        local tmp_file=$(mktemp)
        jq --arg key "$key" --arg val "$value" '.[$key] = $val' "$config_file" > "$tmp_file"
        mv "$tmp_file" "$config_file"
    else
        print_warning "jq not available. Manual JSON editing required for: $key=$value"
        return 1
    fi
    
    return 0
}

# ============================================================================
# ERROR HANDLING UTILITIES
# ============================================================================

# Exit with error message
# Usage: exit_with_error "Error message"
exit_with_error() {
    print_error "$1"
    exit 1
}

# Check exit status and exit with error if non-zero
# Usage: check_status $? "Operation failed"
check_status() {
    local status=$1
    local error_msg="${2:-Command failed}"
    
    if [ $status -ne 0 ]; then
        exit_with_error "$error_msg"
    fi
}

# Confirm action with user
# Usage: confirm_action "Delete all files?"
# Returns: 0 if yes, 1 if no
confirm_action() {
    local prompt="$1"
    local response
    
    read -p "$(echo -e ${YELLOW}${prompt} [y/N]: ${NC})" -n 1 -r response
    echo
    
    if [[ $response =~ ^[Yy]$ ]]; then
        return 0
    else
        return 1
    fi
}

# ============================================================================
# HELP MESSAGE GENERATION
# ============================================================================

# Generate a formatted help section
# Usage: help_section "SECTION TITLE" "Description of section"
help_section() {
    local title="$1"
    local description="$2"
    
    echo -e "${CYAN}${BOLD}${title}${NC}"
    if [ -n "$description" ]; then
        echo "  $description"
    fi
    echo
}

# Generate a help command entry
# Usage: help_command "command-name" "Description of command" "command --option"
help_command() {
    local command="$1"
    local description="$2"
    local example="${3:-}"
    
    echo -e "  ${GREEN}${command}${NC}"
    echo "      $description"
    if [ -n "$example" ]; then
        echo -e "      ${BLUE}Example: $example${NC}"
    fi
    echo
}

# Generate a help option entry
# Usage: help_option "--option, -o" "Description of option"
help_option() {
    local option="$1"
    local description="$2"
    
    echo -e "  ${YELLOW}${option}${NC}"
    echo "      $description"
    echo
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

# Get repository root directory
# Returns: absolute path to git repository root
get_repo_root() {
    git rev-parse --show-toplevel 2>/dev/null || pwd
}

# Check if running in debug mode
# Returns: 0 if DEBUG=1, 1 otherwise
is_debug_mode() {
    [ "${DEBUG:-0}" = "1" ]
}

# Debug print (only prints if DEBUG=1)
# Usage: debug_print "Debug message"
debug_print() {
    if is_debug_mode; then
        echo -e "${CYAN}[DEBUG]${NC} $1" >&2
    fi
}

# Create directory if it doesn't exist
# Usage: ensure_dir "/path/to/dir"
ensure_dir() {
    local dir_path="$1"
    
    if [ ! -d "$dir_path" ]; then
        mkdir -p "$dir_path"
        debug_print "Created directory: $dir_path"
    fi
}

# Get timestamp in ISO 8601 format
# Returns: timestamp string (e.g., 2023-11-01T12:34:56Z)
get_timestamp() {
    date -u +%Y-%m-%dT%H:%M:%SZ
}

# Get timestamp for filenames (no special characters)
# Returns: timestamp string (e.g., 20231101-1234)
get_timestamp_filename() {
    date +%Y%m%d-%H%M
}

# Normalize text to kebab-case format
# Handles various inputs: "Add User Auth", "fix_login_bug", "update-README"
# Returns: kebab-case string or exits with error code 1
# Usage: normalized=$(normalize_to_kebab_case "Add User Auth")
normalize_to_kebab_case() {
    local input="$1"
    
    # Check if input is empty
    if [ -z "$input" ]; then
        return 1
    fi
    
    # Normalization steps:
    # 1. Convert to lowercase
    # 2. Replace underscores and spaces with hyphens
    # 3. Remove any characters that aren't lowercase letters, numbers, or hyphens
    # 4. Replace multiple consecutive hyphens with single hyphen
    # 5. Remove leading and trailing hyphens
    
    local normalized
    normalized=$(echo "$input" | \
        tr '[:upper:]' '[:lower:]' | \
        tr '_' '-' | \
        tr ' ' '-' | \
        sed 's/[^a-z0-9-]//g' | \
        sed 's/-\+/-/g' | \
        sed 's/^-//; s/-$//')
    
    # Check if result is empty (all characters were invalid)
    if [ -z "$normalized" ]; then
        return 1
    fi
    
    echo "$normalized"
    return 0
}

# ============================================================================
# EXPORT ALL FUNCTIONS
# ============================================================================

# Export all functions so they can be used by scripts that source this file
export -f print_success
export -f print_error
export -f print_warning
export -f print_info
export -f print_step
export -f print_banner
export -f validate_name
export -f validate_branch_name
export -f validate_file_exists
export -f validate_dir_exists
export -f get_config
export -f set_config
export -f exit_with_error
export -f check_status
export -f confirm_action
export -f help_section
export -f help_command
export -f help_option
export -f get_repo_root
export -f is_debug_mode
export -f debug_print
export -f ensure_dir
export -f get_timestamp
export -f get_timestamp_filename
export -f normalize_to_kebab_case

# Export color codes
export RED GREEN YELLOW BLUE CYAN BOLD NC

debug_print "core-utils.sh loaded successfully"
