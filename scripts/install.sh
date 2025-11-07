#!/usr/bin/env bash
"""
install.sh
RDD Framework Interactive Installer for Linux/macOS
Provides visual folder navigation for installation directory selection
"""

set -e

# Version from build
VERSION="{{VERSION}}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Current navigation state
CURRENT_DIR=""
SELECTED_INDEX=0

# Print colored messages
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_banner() {
    clear
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║      RDD Framework Interactive Installer v${VERSION}           ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check Python
    if ! command -v python &> /dev/null; then
        print_error "Python is not installed or not in PATH"
        print_error "Install Python 3.7+ from: https://www.python.org/downloads/"
        exit 1
    fi
    
    # Check Python version
    python_version=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    print_success "Python ${python_version} detected"
    
    # Check Git
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed or not in PATH"
        print_error "Install Git from: https://git-scm.com/downloads"
        exit 1
    fi
    
    git_version=$(git --version)
    print_success "${git_version} detected"
    
    echo ""
}

# Navigate folders with visual menu
navigate_folders() {
    local start_dir="$1"
    CURRENT_DIR="$(cd "$start_dir" && pwd)"
    SELECTED_INDEX=0
    
    while true; do
        # Get list of directories
        local dirs=()
        
        # Add parent directory option if not at root
        if [ "$CURRENT_DIR" != "/" ]; then
            dirs+=("..")
        fi
        
        # Add "select this" option
        dirs+=(".")
        
        # Add subdirectories (only directories, sorted)
        while IFS= read -r dir; do
            if [ -d "$CURRENT_DIR/$dir" ] && [ "$dir" != "." ] && [ "$dir" != ".." ]; then
                dirs+=("$dir")
            fi
        done < <(ls -1 "$CURRENT_DIR" 2>/dev/null | sort)
        
        # Ensure selected index is in bounds
        if [ $SELECTED_INDEX -lt 0 ]; then
            SELECTED_INDEX=0
        fi
        if [ $SELECTED_INDEX -ge ${#dirs[@]} ]; then
            SELECTED_INDEX=$((${#dirs[@]} - 1))
        fi
        
        # Draw menu
        draw_menu "${dirs[@]}"
        
        # Get user input
        read -rsn1 key
        
        case "$key" in
            $'\e')  # Escape sequence (arrow keys)
                read -rsn2 key  # Read the rest of the escape sequence
                case "$key" in
                    '[A')  # Up arrow
                        SELECTED_INDEX=$((SELECTED_INDEX - 1))
                        if [ $SELECTED_INDEX -lt 0 ]; then
                            SELECTED_INDEX=0
                        fi
                        ;;
                    '[B')  # Down arrow
                        SELECTED_INDEX=$((SELECTED_INDEX + 1))
                        if [ $SELECTED_INDEX -ge ${#dirs[@]} ]; then
                            SELECTED_INDEX=$((${#dirs[@]} - 1))
                        fi
                        ;;
                esac
                ;;
            '')  # Enter key
                local selected="${dirs[$SELECTED_INDEX]}"
                if [ "$selected" = ".." ]; then
                    # Go to parent directory
                    CURRENT_DIR="$(cd "$CURRENT_DIR/.." && pwd)"
                    SELECTED_INDEX=0
                elif [ "$selected" = "." ]; then
                    # Select current directory
                    return 0
                else
                    # Enter subdirectory
                    CURRENT_DIR="$(cd "$CURRENT_DIR/$selected" && pwd)"
                    SELECTED_INDEX=0
                fi
                ;;
            'q'|'Q')  # Quit
                echo ""
                print_info "Installation cancelled by user"
                exit 0
                ;;
        esac
    done
}

# Draw the navigation menu
draw_menu() {
    local dirs=("$@")
    clear
    print_banner
    
    echo -e "${CYAN}${BOLD}Select Installation Directory${NC}"
    echo ""
    echo -e "${BOLD}Current:${NC} ${CURRENT_DIR}"
    echo ""
    echo "┌────────────────────────────────────────────────────────────┐"
    
    local index=0
    for dir in "${dirs[@]}"; do
        local display_name
        if [ "$dir" = ".." ]; then
            display_name="[..] Parent Directory"
        elif [ "$dir" = "." ]; then
            display_name="[SELECT THIS DIRECTORY]"
        else
            display_name="$dir/"
        fi
        
        if [ $index -eq $SELECTED_INDEX ]; then
            echo -e "│ ${GREEN}▶${NC} ${BOLD}${display_name}${NC}"
        else
            echo -e "│   ${display_name}"
        fi
        
        index=$((index + 1))
    done
    
    echo "└────────────────────────────────────────────────────────────┘"
    echo ""
    echo -e "${CYAN}Use ${BOLD}↑↓${NC}${CYAN} arrow keys to navigate, ${BOLD}Enter${NC}${CYAN} to select, ${BOLD}Q${NC}${CYAN} to quit${NC}"
}

# Validate git repository
validate_git_repo() {
    local target_dir="$1"
    
    print_info "Checking if $target_dir is a Git repository..."
    
    if [ ! -d "$target_dir/.git" ]; then
        echo ""
        print_error "Selected directory is not a Git repository"
        print_info "Initialize with: cd $target_dir && git init"
        echo ""
        read -p "Press Enter to continue..."
        return 1
    fi
    
    print_success "Git repository confirmed"
    return 0
}

# Confirm installation
confirm_installation() {
    local target_dir="$1"
    
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                    Installation Summary                    ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "${BOLD}Target Directory:${NC} ${target_dir}"
    echo -e "${BOLD}RDD Version:${NC} v${VERSION}"
    echo ""
    
    # Check for existing installation
    if [ -f "$target_dir/.rdd/scripts/rdd.py" ]; then
        print_warning "Existing RDD installation detected - will be OVERWRITTEN"
        echo ""
    fi
    
    read -p "$(echo -e ${BOLD}Proceed with installation? [y/N]:${NC} )" -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installation cancelled by user"
        exit 0
    fi
}

# Run Python installer
run_python_installer() {
    local source_dir="$1"
    local target_dir="$2"
    
    echo ""
    print_info "Running Python installer..."
    echo ""
    
    cd "$target_dir"
    python "$source_dir/install.py" <<EOF


EOF
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo ""
        echo "╔════════════════════════════════════════════════════════════╗"
        echo "║              Installation Completed Successfully!          ║"
        echo "╚════════════════════════════════════════════════════════════╝"
        echo ""
        print_success "RDD Framework v${VERSION} installed to: ${target_dir}"
        echo ""
        echo -e "${BOLD}Next steps:${NC}"
        echo "  1. Restart VS Code"
        echo "  2. Create your first change:"
        echo -e "     ${CYAN}cd ${target_dir}${NC}"
        echo -e "     ${CYAN}python .rdd/scripts/rdd.py change create enh my-feature${NC}"
        echo ""
        echo "Documentation: https://github.com/h111359/requirements-driven-development"
        echo ""
    else
        echo ""
        print_error "Installation failed with exit code: $exit_code"
        exit $exit_code
    fi
}

# Main execution
main() {
    # Get source directory (where this script is located)
    SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Prerequisites check
    check_prerequisites
    
    # Navigate to select installation directory
    print_info "Starting folder navigation..."
    print_info "Navigate with arrow keys, press Enter to select"
    echo ""
    sleep 2
    
    navigate_folders "$(pwd)"
    
    TARGET_DIR="$CURRENT_DIR"
    
    # Validate git repository
    while ! validate_git_repo "$TARGET_DIR"; do
        echo ""
        read -p "$(echo -e ${BOLD}Try selecting a different directory? [Y/n]:${NC} )" -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            print_info "Installation cancelled by user"
            exit 0
        fi
        
        navigate_folders "$TARGET_DIR"
        TARGET_DIR="$CURRENT_DIR"
    done
    
    # Confirm installation
    confirm_installation "$TARGET_DIR"
    
    # Run Python installer
    run_python_installer "$SOURCE_DIR" "$TARGET_DIR"
}

# Run main function
main
