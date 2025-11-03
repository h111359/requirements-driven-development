#!/bin/bash

# Script to delete merged branches both locally and remotely
# Uses interactive keyboard navigation for selection

set -o pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not a git repository${NC}"
    exit 1
fi

# Get the default branch (usually main or master)
DEFAULT_BRANCH=$(git remote show origin | grep 'HEAD branch' | cut -d' ' -f5)
if [ -z "$DEFAULT_BRANCH" ]; then
    DEFAULT_BRANCH="main"
fi

echo -e "${CYAN}${BOLD}=== Merged Branch Deletion Tool ===${NC}\n"
echo -e "Default branch: ${GREEN}${DEFAULT_BRANCH}${NC}\n"

# Fetch latest changes from remote
echo -e "${YELLOW}Fetching latest changes from remote...${NC}"
git fetch --prune origin

# Get list of local branches that are merged into the default branch
# Exclude the default branch itself and the current branch
echo -e "${YELLOW}Finding merged branches...${NC}\n"

# Get merged local branches
MERGED_BRANCHES=()
while IFS= read -r branch; do
    # Skip empty lines
    [ -z "$branch" ] && continue
    
    # Remove leading/trailing whitespace and asterisk for current branch
    branch=$(echo "$branch" | sed 's/^[* ]*//;s/[[:space:]]*$//')
    
    # Skip default branch
    [ "$branch" = "$DEFAULT_BRANCH" ] && continue
    
    # Check if branch exists remotely
    REMOTE_STATUS=""
    if git ls-remote --heads origin "$branch" | grep -q "$branch"; then
        REMOTE_STATUS=" ${CYAN}(remote)${NC}"
    else
        REMOTE_STATUS=" ${BLUE}(local only)${NC}"
    fi
    
    MERGED_BRANCHES+=("$branch|$REMOTE_STATUS")
done < <(git branch --merged "$DEFAULT_BRANCH")

if [ ${#MERGED_BRANCHES[@]} -eq 0 ]; then
    echo -e "${GREEN}No merged branches found!${NC}"
    exit 0
fi

echo -e "${BOLD}Found ${#MERGED_BRANCHES[@]} merged branch(es):${NC}\n"

# Interactive selection using checkboxes
declare -A SELECTED
CURRENT_INDEX=0
TOTAL_BRANCHES=${#MERGED_BRANCHES[@]}

# Initialize all as unselected
for i in "${!MERGED_BRANCHES[@]}"; do
    SELECTED[$i]=0
done

# Function to draw the menu
draw_menu() {
    clear
    echo -e "${CYAN}${BOLD}=== Select Branches to Delete ===${NC}\n"
    echo -e "Default branch: ${GREEN}${DEFAULT_BRANCH}${NC}\n"
    echo -e "${BOLD}Use ↑/↓ (or k/j) to navigate, SPACE to select/deselect, ENTER to confirm, 'a' to select all, 'n' to deselect all${NC}\n"
    
    for i in "${!MERGED_BRANCHES[@]}"; do
        IFS='|' read -r branch remote_info <<< "${MERGED_BRANCHES[$i]}"
        
        # Highlight current line
        if [ $i -eq $CURRENT_INDEX ]; then
            echo -n -e "${YELLOW}> "
        else
            echo -n "  "
        fi
        
        # Show checkbox
        if [ ${SELECTED[$i]} -eq 1 ]; then
            echo -n -e "[${GREEN}✓${NC}] "
        else
            echo -n "[ ] "
        fi
        
        # Show branch name and remote status
        echo -e "${branch}${remote_info}"
    done
    
    echo -e "\n${BOLD}Selected: ${GREEN}$(count_selected)${NC}/${TOTAL_BRANCHES}${NC}"
}

# Function to count selected items
count_selected() {
    local count=0
    for i in "${!SELECTED[@]}"; do
        [ ${SELECTED[$i]} -eq 1 ] && ((count++))
    done
    echo $count
}

# Function to read a single keypress
read_key() {
    local key
    # Read first character
    IFS= read -rsn1 key
    
    # If it's an escape sequence (arrow key)
    if [[ $key == $'\x1b' ]]; then
        # Read the next two characters
        IFS= read -rsn2 -t 0.1 rest
        key="${key}${rest}"
    fi
    
    echo "$key"
}

# Main selection loop
draw_menu

while true; do
    KEY=$(read_key)
    
    case "$KEY" in
        # Arrow up or 'k'
        $'\x1b[A'|'k')
            CURRENT_INDEX=$((CURRENT_INDEX - 1))
            if [ $CURRENT_INDEX -lt 0 ]; then
                CURRENT_INDEX=$((TOTAL_BRANCHES - 1))
            fi
            draw_menu
            ;;
        # Arrow down or 'j'
        $'\x1b[B'|'j')
            CURRENT_INDEX=$((CURRENT_INDEX + 1))
            if [ $CURRENT_INDEX -ge $TOTAL_BRANCHES ]; then
                CURRENT_INDEX=0
            fi
            draw_menu
            ;;
        # Spacebar - toggle selection
        ' ')
            if [ ${SELECTED[$CURRENT_INDEX]} -eq 1 ]; then
                SELECTED[$CURRENT_INDEX]=0
            else
                SELECTED[$CURRENT_INDEX]=1
            fi
            draw_menu
            ;;
        # 'a' - select all
        'a')
            for i in "${!SELECTED[@]}"; do
                SELECTED[$i]=1
            done
            draw_menu
            ;;
        # 'n' - deselect all
        'n')
            for i in "${!SELECTED[@]}"; do
                SELECTED[$i]=0
            done
            draw_menu
            ;;
        # Enter - confirm selection
        '')
            break
            ;;
        # 'q' - quit
        'q')
            echo -e "\n${YELLOW}Cancelled.${NC}"
            exit 0
            ;;
    esac
done

# Get list of selected branches
BRANCHES_TO_DELETE=()
for i in "${!MERGED_BRANCHES[@]}"; do
    if [ ${SELECTED[$i]} -eq 1 ]; then
        IFS='|' read -r branch remote_info <<< "${MERGED_BRANCHES[$i]}"
        BRANCHES_TO_DELETE+=("$branch")
    fi
done

# Check if any branches were selected
if [ ${#BRANCHES_TO_DELETE[@]} -eq 0 ]; then
    echo -e "\n${YELLOW}No branches selected. Exiting.${NC}"
    exit 0
fi

# Confirm deletion
clear
echo -e "${CYAN}${BOLD}=== Confirmation ===${NC}\n"
echo -e "${BOLD}You are about to delete the following branches:${NC}\n"

for branch in "${BRANCHES_TO_DELETE[@]}"; do
    # Check if branch exists remotely
    if git ls-remote --heads origin "$branch" | grep -q "$branch"; then
        echo -e "  ${RED}✗${NC} ${branch} ${CYAN}(local + remote)${NC}"
    else
        echo -e "  ${RED}✗${NC} ${branch} ${BLUE}(local only)${NC}"
    fi
done

echo -e "\n${BOLD}${RED}This action cannot be undone!${NC}"
echo -n -e "\n${BOLD}Continue? (yes/no): ${NC}"
read -r CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}Cancelled.${NC}"
    exit 0
fi

# Delete branches
echo -e "\n${YELLOW}Deleting branches...${NC}\n"

for branch in "${BRANCHES_TO_DELETE[@]}"; do
    echo -e "${BOLD}Processing: ${branch}${NC}"
    
    # Delete local branch
    if git show-ref --verify --quiet "refs/heads/$branch"; then
        if git branch -d "$branch" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} Deleted local branch"
        else
            # Force delete if normal delete fails
            echo -e "  ${YELLOW}! Branch not fully merged, force deleting...${NC}"
            git branch -D "$branch"
            echo -e "  ${GREEN}✓${NC} Force deleted local branch"
        fi
    else
        echo -e "  ${BLUE}ℹ${NC} Local branch not found (already deleted?)"
    fi
    
    # Delete remote branch
    if git ls-remote --heads origin "$branch" | grep -q "$branch"; then
        if git push origin --delete "$branch" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} Deleted remote branch"
        else
            echo -e "  ${RED}✗${NC} Failed to delete remote branch (check permissions)"
        fi
    else
        echo -e "  ${BLUE}ℹ${NC} Remote branch not found (already deleted?)"
    fi
    
    echo ""
done

echo -e "${GREEN}${BOLD}Done!${NC}"
echo -e "${CYAN}Deleted ${#BRANCHES_TO_DELETE[@]} branch(es).${NC}"
