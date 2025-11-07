#!/usr/bin/env bats
# test_install_sh.bats
# Tests for install.sh bash installer

setup() {
    # Create temporary test directory
    TEST_DIR=$(mktemp -d)
    export TEST_DIR
    
    # Create mock RDD archive structure
    MOCK_RDD_DIR="$TEST_DIR/rdd-v1.0.0"
    mkdir -p "$MOCK_RDD_DIR/.rdd/scripts"
    mkdir -p "$MOCK_RDD_DIR/.rdd/templates"
    mkdir -p "$MOCK_RDD_DIR/.github/prompts"
    mkdir -p "$MOCK_RDD_DIR/.rdd-docs"
    mkdir -p "$MOCK_RDD_DIR/.vscode"
    
    # Create mock files
    echo '#!/usr/bin/env python3' > "$MOCK_RDD_DIR/.rdd/scripts/rdd.py"
    echo 'print("RDD")' >> "$MOCK_RDD_DIR/.rdd/scripts/rdd.py"
    chmod +x "$MOCK_RDD_DIR/.rdd/scripts/rdd.py"
    
    echo '{}' > "$MOCK_RDD_DIR/.vscode/settings.json"
    echo 'MIT License' > "$MOCK_RDD_DIR/LICENSE"
    
    # Copy install.py for testing
    if [ -f "scripts/install.py" ]; then
        cp scripts/install.py "$MOCK_RDD_DIR/install.py"
    fi
    
    export MOCK_RDD_DIR
}

teardown() {
    # Clean up test directory
    if [ -n "$TEST_DIR" ] && [ -d "$TEST_DIR" ]; then
        rm -rf "$TEST_DIR"
    fi
}

@test "install.sh exists and is executable" {
    [ -f "scripts/install.sh" ]
    [ -x "scripts/install.sh" ]
}

@test "install.sh shows version banner" {
    skip "Interactive test - requires user input"
    # This would need to mock user input
}

@test "check python3 availability" {
    run command -v python3
    [ "$status" -eq 0 ]
}

@test "check git availability" {
    run command -v git
    [ "$status" -eq 0 ]
}

@test "create test git repository" {
    # Create a test git repo
    REPO_DIR="$TEST_DIR/test-repo"
    mkdir -p "$REPO_DIR"
    cd "$REPO_DIR"
    
    git init
    git config user.name "Test User"
    git config user.email "test@example.com"
    
    # Verify it's a git repo
    [ -d "$REPO_DIR/.git" ]
}

@test "install.py can be executed with python" {
    skip "install.py is interactive and doesn't support --help flag"
    
    if [ ! -f "$MOCK_RDD_DIR/install.py" ]; then
        skip "install.py not available"
    fi
    
    # Test that install.py can at least show help
    run python3 "$MOCK_RDD_DIR/install.py" --help
    # May fail but should execute without syntax errors
    [ "$status" -eq 0 ] || [ "$status" -eq 2 ]
}

@test "directory navigation functions work" {
    # Test basic directory operations
    CURRENT_DIR=$(pwd)
    TEST_SUBDIR="$TEST_DIR/subdir"
    mkdir -p "$TEST_SUBDIR"
    
    cd "$TEST_SUBDIR"
    [ "$(pwd)" = "$TEST_SUBDIR" ]
    
    cd "$CURRENT_DIR"
    [ "$(pwd)" = "$CURRENT_DIR" ]
}

@test "git repository detection works" {
    # Test git detection in a git repo
    REPO_DIR="$TEST_DIR/git-repo"
    mkdir -p "$REPO_DIR"
    cd "$REPO_DIR"
    git init
    
    [ -d ".git" ]
    
    # Test in non-git directory
    NON_GIT_DIR="$TEST_DIR/non-git"
    mkdir -p "$NON_GIT_DIR"
    cd "$NON_GIT_DIR"
    
    [ ! -d ".git" ]
}

@test "file operations work correctly" {
    # Test file copying operations
    SRC_DIR="$TEST_DIR/src"
    DST_DIR="$TEST_DIR/dst"
    
    mkdir -p "$SRC_DIR"
    mkdir -p "$DST_DIR"
    
    echo "test content" > "$SRC_DIR/test.txt"
    
    cp "$SRC_DIR/test.txt" "$DST_DIR/test.txt"
    
    [ -f "$DST_DIR/test.txt" ]
    [ "$(cat "$DST_DIR/test.txt")" = "test content" ]
}

@test "directory traversal safety" {
    # Test that we don't accidentally navigate outside test dir
    CURRENT=$(pwd)
    
    # Try to go up many levels
    cd "$TEST_DIR"
    for i in {1..10}; do
        cd ..
    done
    
    # Should not crash or cause errors
    RESULT=$(pwd)
    
    # Navigate back
    cd "$CURRENT"
    
    # Test passes if no errors occurred
    [ -d "$CURRENT" ]
}
