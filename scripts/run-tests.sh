#!/bin/bash
#
# run-tests.sh
# Run all tests appropriate for Linux/macOS
#

set -e  # Exit on error

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo ""
    echo "============================================================"
    echo "  $1"
    echo "============================================================"
    echo ""
}

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

print_step() {
    echo -e "${BLUE}[$1/$2]${NC} $3"
}

# Get script directory and repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to repository root
cd "$REPO_ROOT"

# Print banner
print_header "RDD Framework Test Runner (Linux)"

# Check prerequisites
print_info "Checking prerequisites..."

# Check Python
if ! command -v python &> /dev/null; then
    print_error "Python is not installed or not in PATH"
    exit 1
fi
print_success "Python found: $(python --version)"

# Check virtual environment
if [ ! -d ".venv" ]; then
    print_warning "Virtual environment not found at .venv/"
    print_info "Run: python setup-test-env.py"
    exit 1
fi
print_success "Virtual environment found"

# Activate virtual environment
print_info "Activating virtual environment..."
source .venv/bin/activate
print_success "Virtual environment activated"

# Check pytest
if ! command -v pytest &> /dev/null; then
    print_error "pytest not found in virtual environment"
    print_info "Run: python setup-test-env.py"
    exit 1
fi
print_success "pytest found: $(pytest --version | head -1)"

# Track test results
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

echo ""
print_header "Running Tests"

# Step 1: Python Unit Tests
print_step 1 4 "Running Python unit tests"
if pytest tests/python/ -v --tb=short; then
    print_success "Python unit tests passed"
    ((PASSED_TESTS++))
else
    print_error "Python unit tests failed"
    ((FAILED_TESTS++))
fi
((TOTAL_TESTS++))
echo ""

# Step 2: Build Tests
print_step 2 4 "Running build tests"
if pytest tests/build/ -v --tb=short; then
    print_success "Build tests passed"
    ((PASSED_TESTS++))
else
    print_error "Build tests failed"
    ((FAILED_TESTS++))
fi
((TOTAL_TESTS++))
echo ""

# Step 3: Install Tests
print_step 3 4 "Running install tests"
if pytest tests/install/ -v --tb=short; then
    print_success "Install tests passed"
    ((PASSED_TESTS++))
else
    print_error "Install tests failed"
    ((FAILED_TESTS++))
fi
((TOTAL_TESTS++))
echo ""

# Step 4: Shell Tests (BATS)
print_step 4 4 "Running shell tests (BATS)"
if command -v bats &> /dev/null; then
    if bats tests/shell/*.bats; then
        print_success "Shell tests passed"
        ((PASSED_TESTS++))
    else
        print_error "Shell tests failed"
        ((FAILED_TESTS++))
    fi
    ((TOTAL_TESTS++))
else
    print_warning "BATS not found - skipping shell tests"
    print_info "Install: sudo apt-get install bats (Ubuntu/Debian)"
    print_info "Install: brew install bats-core (macOS)"
fi
echo ""

# Summary
print_header "Test Summary"

echo "Total test suites: $TOTAL_TESTS"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
if [ $FAILED_TESTS -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED_TESTS${NC}"
fi
echo ""

# Exit with appropriate code
if [ $FAILED_TESTS -gt 0 ]; then
    print_error "Some tests failed"
    exit 1
else
    print_success "All tests passed!"
    exit 0
fi
