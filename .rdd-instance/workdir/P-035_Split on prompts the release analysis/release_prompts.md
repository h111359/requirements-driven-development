# Release Automation Implementation Prompts

This document contains a series of prompts for implementing the release automation system based on the analysis in P-034. These prompts should be executed in sequence by GitHub Copilot agents.

---

## Prompt 1: Prepare build.py for CI/CD Integration

**Prerequisites:**
- None (first prompt in sequence)

**Objective:**
Modify the existing `build/build.py` script to support non-interactive execution for CI/CD pipelines while maintaining backward compatibility with manual execution.

**Detailed Steps:**

1. **Read the current build.py implementation**
   - Analyze the existing script at `build/build.py`
   - Identify all interactive prompts and user input points
   - Document current version reading mechanism from `.rdd/config/manifest.json`

2. **Add command-line argument parsing**
   - Import `argparse` module at the top of the script
   - Create an argument parser with the following arguments:
     - `--version`: Specific version to build (e.g., "2.1.0")
     - `--non-interactive`: Flag to enable non-interactive mode for CI
   - Place argument parsing at the start of the `main()` function

3. **Implement non-interactive mode logic**
   - When `--non-interactive` is set:
     - Require `--version` argument (exit with error if missing)
     - Skip all user prompts
     - Use provided version directly
     - Automatically resolve any file conflicts (prefer overwrite)
     - Exit with non-zero code on any errors
   - When interactive (default):
     - Preserve all existing interactive behavior
     - Keep current user prompts and confirmations

4. **Update version handling**
   - Extract version reading into a separate function `get_current_version()`
   - Extract version validation into a function `validate_version(version_string)`
   - Ensure version format validation (major.minor.patch)

5. **Enhance error handling**
   - Add clear error messages for CI context
   - Ensure all errors print to stderr
   - Return appropriate exit codes:
     - 0 for success
     - 1 for general errors
     - 2 for validation errors

6. **Update file operations**
   - Ensure all file paths use os.path.join for cross-platform compatibility
   - Verify zip creation works correctly in both modes
   - Verify SHA256 checksum generation works in both modes

**Testing and Validation:**

1. **Test interactive mode (existing behavior)**
   ```bash
   # Should work exactly as before
   python build/build.py
   ```
   - Verify all prompts appear
   - Verify user can select version
   - Verify artifacts are created correctly

2. **Test non-interactive mode**
   ```bash
   # Should succeed
   python build/build.py --version 2.1.0 --non-interactive
   
   # Should fail with clear error
   python build/build.py --non-interactive
   
   # Should fail with validation error
   python build/build.py --version invalid --non-interactive
   ```
   - Verify no prompts appear
   - Verify build completes successfully
   - Verify artifacts are created:
     - `build/rdd-v2.1.0.zip` exists
     - `build/rdd-v2.1.0.zip.sha256` exists
   - Verify exit codes are correct

3. **Test version validation**
   ```bash
   # Valid versions
   python build/build.py --version 1.0.0 --non-interactive
   python build/build.py --version 10.20.30 --non-interactive
   
   # Invalid versions (should fail)
   python build/build.py --version 1.0 --non-interactive
   python build/build.py --version v1.0.0 --non-interactive
   python build/build.py --version abc --non-interactive
   ```

4. **Cross-platform verification**
   - Test on Linux (if available)
   - Test on Windows (if available)
   - Verify file paths work correctly

**Expected Deliverables:**
- Modified `build/build.py` with CI support
- Backward compatible with existing manual workflow
- Clear error messages for CI context
- Successfully creates artifacts in both modes

**Success Criteria:**
- [ ] Script accepts `--version` and `--non-interactive` arguments
- [ ] Non-interactive mode completes without any user input
- [ ] Interactive mode works exactly as before
- [ ] Build artifacts are created correctly in both modes
- [ ] Version validation works correctly
- [ ] Error handling provides clear messages
- [ ] Exit codes are appropriate for CI/CD pipelines

---

## Prompt 2: Create Version Management Helper Script

**Prerequisites:**
- Prompt 1 completed (build.py supports CI mode)

**Objective:**
Create a Python helper script that handles version reading, incrementing, and updating in `.rdd/config/manifest.json`. This script will be used by the GitHub Actions workflow.

**Detailed Steps:**

1. **Create the version management script**
   - Create new file: `build/version_manager.py`
   - Add standard Python script header with description
   - Import required modules: `json`, `sys`, `argparse`, `re`

2. **Implement version reading function**
   ```python
   def get_current_version():
       """Read current version from manifest.json"""
       # Read .rdd/config/manifest.json
       # Extract framework.version field
       # Return version string
   ```

3. **Implement version validation function**
   ```python
   def validate_version(version):
       """Validate version string format (major.minor.patch)"""
       # Use regex to validate format: \d+\.\d+\.\d+
       # Return True if valid, False otherwise
   ```

4. **Implement version parsing function**
   ```python
   def parse_version(version):
       """Parse version string into major, minor, patch integers"""
       # Split version by '.'
       # Convert to integers
       # Return tuple (major, minor, patch)
   ```

5. **Implement version increment function**
   ```python
   def increment_version(version, increment_type='patch'):
       """Increment version based on type (major, minor, or patch)"""
       # Parse current version
       # Increment based on type:
       #   major: X.0.0 (X+1)
       #   minor: X.Y.0 (Y+1)
       #   patch: X.Y.Z (Z+1)
       # Return new version string
   ```

6. **Implement version update function**
   ```python
   def update_manifest_version(new_version):
       """Update version in manifest.json"""
       # Read manifest.json
       # Update framework.version field
       # Write back with proper formatting (indent=2)
       # Preserve other fields unchanged
   ```

7. **Implement version comparison function**
   ```python
   def compare_versions(version1, version2):
       """Compare two versions, return -1, 0, or 1"""
       # Parse both versions
       # Compare major, then minor, then patch
       # Return comparison result
   ```

8. **Create command-line interface**
   - Add argparse with subcommands:
     - `get`: Print current version
     - `increment`: Increment and print new version (don't update file)
     - `update`: Update manifest.json with new version
     - `validate`: Validate a version string
     - `compare`: Compare two versions
   - Each subcommand should have appropriate arguments
   - Add `--dry-run` flag for testing

9. **Add error handling**
   - Handle file not found errors
   - Handle JSON parsing errors
   - Handle invalid version formats
   - Print clear error messages to stderr
   - Use appropriate exit codes

10. **Add output formatting**
    - Support `--json` flag for JSON output (for CI parsing)
    - Default to human-readable output
    - Ensure consistent output format

**Testing and Validation:**

1. **Test get command**
   ```bash
   python build/version_manager.py get
   # Should print: 2.1.0 (or current version)
   
   python build/version_manager.py get --json
   # Should print: {"version": "2.1.0"}
   ```

2. **Test increment command**
   ```bash
   python build/version_manager.py increment --type patch
   # Should print: 2.1.1
   
   python build/version_manager.py increment --type minor
   # Should print: 2.2.0
   
   python build/version_manager.py increment --type major
   # Should print: 3.0.0
   ```

3. **Test validate command**
   ```bash
   python build/version_manager.py validate 1.2.3
   # Should exit 0 (valid)
   
   python build/version_manager.py validate invalid
   # Should exit 1 (invalid)
   ```

4. **Test update command with dry-run**
   ```bash
   python build/version_manager.py update 2.1.1 --dry-run
   # Should show what would change without modifying file
   ```

5. **Test update command (actual)**
   ```bash
   # Save current manifest
   cp .rdd/config/manifest.json .rdd/config/manifest.json.backup
   
   # Update version
   python build/version_manager.py update 2.1.1
   
   # Verify update
   python build/version_manager.py get
   # Should print: 2.1.1
   
   # Verify JSON integrity
   python -m json.tool .rdd/config/manifest.json > /dev/null
   
   # Restore backup
   mv .rdd/config/manifest.json.backup .rdd/config/manifest.json
   ```

6. **Test compare command**
   ```bash
   python build/version_manager.py compare 1.0.0 2.0.0
   # Should print: 1.0.0 < 2.0.0
   
   python build/version_manager.py compare 2.1.0 2.1.0
   # Should print: 2.1.0 = 2.1.0
   ```

7. **Test error handling**
   ```bash
   # Test with non-existent manifest
   python build/version_manager.py --manifest /nonexistent/path.json get
   # Should print clear error and exit with code 1
   
   # Test with invalid JSON
   # (create temporary invalid JSON file and test)
   ```

**Expected Deliverables:**
- New file `build/version_manager.py` with full functionality
- Command-line interface with subcommands
- Comprehensive error handling
- Support for both human and machine-readable output

**Success Criteria:**
- [ ] Can read current version from manifest.json
- [ ] Can validate version string format
- [ ] Can increment version (major, minor, patch)
- [ ] Can update manifest.json with new version
- [ ] Can compare two versions
- [ ] All commands work correctly
- [ ] Error handling is comprehensive
- [ ] Exit codes are appropriate
- [ ] JSON output mode works for CI integration
- [ ] Dry-run mode prevents accidental changes

---

## Prompt 3: Create Release Notes Generator Script

**Prerequisites:**
- Prompt 1 completed (build.py supports CI mode)
- Prompt 2 completed (version_manager.py exists)

**Objective:**
Create a Python script that generates release notes by analyzing git commits, merged branches, and RDD workdir content. This script will be used by the GitHub Actions workflow.

**Detailed Steps:**

1. **Create the release notes generator script**
   - Create new file: `build/generate_release_notes.py`
   - Add standard Python script header
   - Import required modules: `subprocess`, `re`, `json`, `os`, `sys`, `argparse`, `datetime`

2. **Implement git operations helpers**
   ```python
   def run_git_command(command):
       """Execute git command and return output"""
       # Run subprocess with shell=True
       # Capture stdout and stderr
       # Return output or raise error
   
   def get_last_tag():
       """Get the most recent git tag"""
       # Run: git describe --tags --abbrev=0
       # Handle case when no tags exist
       # Return tag name or None
   
   def get_commits_since(since_ref='HEAD'):
       """Get commit messages since reference"""
       # Run: git log {since_ref}..HEAD --oneline --no-merges
       # Parse output into list of commits
       # Return list of tuples (hash, message)
   
   def get_merged_branches(since_ref='HEAD'):
       """Get branches merged since reference"""
       # Run: git log {since_ref}..HEAD --merges --pretty=format:"%s"
       # Extract branch names from merge messages
       # Return list of branch names
   ```

3. **Implement RDD workdir analysis**
   ```python
   def get_changed_prompts(since_ref='HEAD'):
       """Get prompts that changed since reference"""
       # Run: git diff --name-only {since_ref}..HEAD .rdd-instance/workdir/
       # Parse output to extract prompt IDs and titles
       # Use regex: P-(\d+)_(.+?)/
       # Return list of tuples (prompt_id, prompt_title)
   
   def read_prompt_implementation(prompt_id, prompt_title):
       """Read implementation details for a prompt"""
       # Construct path: .rdd-instance/workdir/P-{id}_{title}/implementation.md
       # Read file if exists
       # Extract key sections (summary, changes made, etc.)
       # Return dictionary with implementation details
   
   def read_prompt_metadata(prompt_id, prompt_title):
       """Read prompt metadata from prompt.md and questionnaire.json"""
       # Read prompt.md for original request
       # Read questionnaire.json if exists for decisions
       # Return dictionary with metadata
   ```

4. **Implement release notes formatting**
   ```python
   def format_release_notes(version, data):
       """Format release notes in markdown"""
       # Create markdown structure:
       # - Header with version
       # - Summary section
       # - Features and Enhancements (from prompts)
       # - Bug Fixes (from commits with "fix" keyword)
       # - Prompts Completed (from RDD workdir)
       # - Commits (detailed list)
       # - Branch Information
       # Return formatted markdown string
   ```

5. **Implement main generation function**
   ```python
   def generate_release_notes(version, since_ref=None, output_file=None):
       """Main function to generate release notes"""
       # Determine since_ref (last tag if not specified)
       # Gather all data:
       #   - Get commits
       #   - Get merged branches
       #   - Get changed prompts
       #   - Read implementation details
       # Format release notes
       # Write to output file or stdout
       # Return formatted notes
   ```

6. **Create command-line interface**
   ```python
   # Add argparse:
   #   --version: Version for the release (required)
   #   --since: Reference point (commit/tag) to compare from
   #   --output: Output file path (default: build/release-notes-v{version}.md)
   #   --format: Output format (markdown or json)
   #   --include-commits: Include detailed commit list (default: true)
   #   --include-prompts: Include RDD prompt details (default: true)
   ```

7. **Add categorization logic**
   ```python
   def categorize_commits(commits):
       """Categorize commits by type"""
       # Categories:
       #   - Features (feat:, add, implement)
       #   - Bug Fixes (fix:, bug, resolve)
       #   - Documentation (docs:, documentation)
       #   - Refactoring (refactor:, cleanup)
       #   - Other
       # Return dictionary of categorized commits
   ```

8. **Add error handling**
   - Handle git command failures
   - Handle missing directories/files
   - Handle invalid version formats
   - Print clear error messages
   - Use appropriate exit codes

9. **Add summary generation**
   ```python
   def generate_summary(data):
       """Generate a brief summary of the release"""
       # Count features, fixes, prompts completed
       # Create one-sentence summary
       # Return summary string
   ```

**Testing and Validation:**

1. **Test with no previous tag (first release)**
   ```bash
   python build/generate_release_notes.py --version 1.0.0
   # Should generate notes for all commits
   # Should handle "no previous tag" gracefully
   ```

2. **Test with specific since reference**
   ```bash
   # Using a tag
   python build/generate_release_notes.py --version 2.2.0 --since v2.1.0
   
   # Using a commit hash
   python build/generate_release_notes.py --version 2.2.0 --since abc123
   ```

3. **Test output file creation**
   ```bash
   python build/generate_release_notes.py --version 2.2.0 --output test-notes.md
   
   # Verify file created
   ls -l test-notes.md
   
   # Verify content is valid markdown
   cat test-notes.md
   
   # Cleanup
   rm test-notes.md
   ```

4. **Test with different formats**
   ```bash
   # Markdown (default)
   python build/generate_release_notes.py --version 2.2.0 --format markdown
   
   # JSON (for machine parsing)
   python build/generate_release_notes.py --version 2.2.0 --format json
   # Verify valid JSON output
   python build/generate_release_notes.py --version 2.2.0 --format json | python -m json.tool
   ```

5. **Test commit categorization**
   ```bash
   # Generate notes and verify categories are present
   python build/generate_release_notes.py --version 2.2.0
   # Should show sections for Features, Bug Fixes, etc.
   ```

6. **Test RDD workdir integration**
   ```bash
   # Generate notes and verify prompt information is included
   python build/generate_release_notes.py --version 2.2.0 --include-prompts
   # Should show completed prompts with titles
   ```

7. **Test error handling**
   ```bash
   # Invalid git repository
   cd /tmp && python /path/to/generate_release_notes.py --version 1.0.0
   # Should fail with clear error message
   
   # Invalid version format
   python build/generate_release_notes.py --version invalid
   # Should fail with validation error
   
   # Non-existent since reference
   python build/generate_release_notes.py --version 2.2.0 --since nonexistent
   # Should fail with clear error message
   ```

8. **Integration test with actual repository state**
   ```bash
   # Generate notes for current state
   python build/generate_release_notes.py --version 2.2.0
   
   # Verify output contains:
   # - Release header
   # - Summary section
   # - Commit list
   # - Prompt information (if any prompts completed)
   # - Properly formatted markdown
   ```

**Expected Deliverables:**
- New file `build/generate_release_notes.py` with full functionality
- Support for git commit analysis
- Support for RDD workdir analysis
- Markdown and JSON output formats
- Comprehensive error handling

**Success Criteria:**
- [ ] Can analyze git commits between references
- [ ] Can extract merged branch information
- [ ] Can analyze RDD workdir changes
- [ ] Can categorize commits by type
- [ ] Generates well-formatted markdown release notes
- [ ] Supports JSON output for machine parsing
- [ ] Handles edge cases (no tags, no prompts, etc.)
- [ ] Error messages are clear and helpful
- [ ] Works with current repository structure

---

## Prompt 4: Create GitHub Actions Release Workflow (Phase 1 - Basic)

**Prerequisites:**
- Prompt 1 completed (build.py supports CI mode)
- Prompt 2 completed (version_manager.py exists)
- Prompt 3 completed (generate_release_notes.py exists)

**Objective:**
Create a GitHub Actions workflow that automatically creates releases when PRs are merged to main. This is Phase 1 implementation with basic functionality: automatic patch version increment, artifact creation, and release publishing.

**Detailed Steps:**

1. **Create the workflow file**
   - Create new file: `.github/workflows/release.yml`
   - Add workflow metadata (name, description)

2. **Define workflow trigger**
   ```yaml
   name: Create Release
   
   on:
     pull_request:
       types: [closed]
       branches: [main]
   ```

3. **Define permissions**
   ```yaml
   permissions:
     contents: write  # Required for creating releases, tags, and pushing commits
   ```

4. **Create main job with conditional execution**
   ```yaml
   jobs:
     create-release:
       # Only run if PR was actually merged (not just closed)
       if: github.event.pull_request.merged == true
       runs-on: ubuntu-latest
   ```

5. **Add checkout step**
   ```yaml
   steps:
     - name: Checkout repository
       uses: actions/checkout@v4
       with:
         fetch-depth: 0  # Full history needed for git operations
         token: ${{ secrets.GITHUB_TOKEN }}
   ```

6. **Add Python setup step**
   ```yaml
     - name: Set up Python
       uses: actions/setup-python@v5
       with:
         python-version: '3.9'
   ```

7. **Add version determination step**
   ```yaml
     - name: Get current version and calculate new version
       id: version
       run: |
         # Get current version
         CURRENT_VERSION=$(python build/version_manager.py get)
         echo "current=$CURRENT_VERSION" >> $GITHUB_OUTPUT
         
         # For Phase 1, always increment patch version
         NEW_VERSION=$(python build/version_manager.py increment --type patch)
         echo "new=$NEW_VERSION" >> $GITHUB_OUTPUT
         
         echo "Current version: $CURRENT_VERSION"
         echo "New version: $NEW_VERSION"
   ```

8. **Add manifest update step**
   ```yaml
     - name: Update manifest.json with new version
       run: |
         python build/version_manager.py update ${{ steps.version.outputs.new }}
         echo "Updated manifest.json to version ${{ steps.version.outputs.new }}"
   ```

9. **Add build artifacts step**
   ```yaml
     - name: Build release artifacts
       run: |
         python build/build.py --version ${{ steps.version.outputs.new }} --non-interactive
         
         # Verify artifacts were created
         if [ ! -f "build/rdd-v${{ steps.version.outputs.new }}.zip" ]; then
           echo "Error: Build artifact not created"
           exit 1
         fi
         
         if [ ! -f "build/rdd-v${{ steps.version.outputs.new }}.zip.sha256" ]; then
           echo "Error: SHA256 checksum not created"
           exit 1
         fi
         
         echo "Build artifacts created successfully"
   ```

10. **Add release notes generation step**
    ```yaml
      - name: Generate release notes
        run: |
          python build/generate_release_notes.py \
            --version ${{ steps.version.outputs.new }} \
            --output build/release-notes-v${{ steps.version.outputs.new }}.md
          
          echo "Release notes generated"
    ```

11. **Add commit and push step**
    ```yaml
      - name: Commit version bump and release notes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          
          git add .rdd/config/manifest.json
          git add build/release-notes-v${{ steps.version.outputs.new }}.md
          
          git commit -m "chore: bump version to ${{ steps.version.outputs.new }} [skip ci]"
          git push
    ```

12. **Add tag creation step**
    ```yaml
      - name: Create and push git tag
        run: |
          git tag -a "v${{ steps.version.outputs.new }}" \
            -m "Release v${{ steps.version.outputs.new }}"
          git push origin "v${{ steps.version.outputs.new }}"
          
          echo "Created tag v${{ steps.version.outputs.new }}"
    ```

13. **Add GitHub release creation step**
    ```yaml
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          tag_name: v${{ steps.version.outputs.new }}
          name: Release v${{ steps.version.outputs.new }}
          body_path: build/release-notes-v${{ steps.version.outputs.new }}.md
          files: |
            build/rdd-v${{ steps.version.outputs.new }}.zip
            build/rdd-v${{ steps.version.outputs.new }}.zip.sha256
            build/release-notes-v${{ steps.version.outputs.new }}.md
          draft: false
          prerelease: false
    ```

14. **Add error summary step**
    ```yaml
      - name: Report success
        if: success()
        run: |
          echo "✅ Release v${{ steps.version.outputs.new }} created successfully"
          echo "📦 Tag: v${{ steps.version.outputs.new }}"
          echo "🔗 Release URL: https://github.com/${{ github.repository }}/releases/tag/v${{ steps.version.outputs.new }}"
      
      - name: Report failure
        if: failure()
        run: |
          echo "❌ Release creation failed"
          echo "Please check the logs above for details"
    ```

**Testing and Validation:**

1. **Validate workflow syntax**
   ```bash
   # Use GitHub CLI or online validator
   # Ensure YAML is valid
   cat .github/workflows/release.yml
   ```

2. **Test on a feature branch first (dry run)**
   - Create a test workflow file: `.github/workflows/release-test.yml`
   - Modify trigger to use a test branch:
     ```yaml
     on:
       pull_request:
         types: [closed]
         branches: [test-release]
     ```
   - Create test branch and test PR
   - Verify workflow runs without errors

3. **Manual validation checklist before enabling on main**
   - [ ] Workflow file syntax is valid
   - [ ] All prerequisite scripts exist and work
   - [ ] Git permissions are correct
   - [ ] GitHub token has necessary permissions
   - [ ] Build artifacts are created correctly
   - [ ] Release notes are generated correctly

4. **Enable workflow on main branch**
   - Ensure `.github/workflows/release.yml` has correct trigger:
     ```yaml
     branches: [main]
     ```
   - Commit and push workflow file

5. **Test with an actual PR to main**
   - Create a small test PR from dev to main
   - Merge the PR
   - Monitor workflow execution in GitHub Actions tab
   - Verify:
     - [ ] Workflow triggers on PR merge
     - [ ] Version is incremented correctly
     - [ ] Manifest.json is updated
     - [ ] Build artifacts are created
     - [ ] Release notes are generated
     - [ ] Commit is pushed back to main
     - [ ] Git tag is created
     - [ ] GitHub release is published
     - [ ] Release has correct artifacts attached

6. **Verify release artifacts**
   - Navigate to GitHub Releases page
   - Check latest release contains:
     - [ ] Correct version number
     - [ ] Release notes with proper formatting
     - [ ] rdd-v{version}.zip file
     - [ ] rdd-v{version}.zip.sha256 file
     - [ ] release-notes-v{version}.md file

7. **Verify git state after release**
   ```bash
   # Pull latest changes
   git pull origin main
   
   # Check version in manifest
   python build/version_manager.py get
   # Should show new version
   
   # Check latest tag
   git describe --tags
   # Should show new tag
   
   # Check release notes file exists
   ls build/release-notes-v*.md
   ```

8. **Test error scenarios (optional but recommended)**
   - Test with build failure (temporarily break build.py)
   - Test with invalid version format
   - Test with git conflict
   - Verify workflow fails gracefully with clear error messages

**Expected Deliverables:**
- New file `.github/workflows/release.yml`
- Fully automated release process on PR merge to main
- Automatic patch version increment
- Build artifacts attached to releases
- Release notes generation

**Success Criteria:**
- [ ] Workflow file is created and valid
- [ ] Workflow triggers only on PR merge to main
- [ ] Workflow has correct permissions
- [ ] Version is automatically incremented (patch)
- [ ] Manifest.json is updated in repository
- [ ] Build artifacts are created successfully
- [ ] Release notes are generated and included
- [ ] Git tag is created and pushed
- [ ] GitHub release is published with all artifacts
- [ ] Process completes end-to-end without manual intervention
- [ ] Error messages are clear if workflow fails

---

## Prompt 5: Enhance Release Workflow with Version Control Keywords (Phase 2)

**Prerequisites:**
- Prompt 1 completed (build.py supports CI mode)
- Prompt 2 completed (version_manager.py exists)
- Prompt 3 completed (generate_release_notes.py exists)
- Prompt 4 completed (basic release workflow exists)

**Objective:**
Enhance the GitHub Actions release workflow to support manual version increment control via PR description keywords. Allow developers to specify major or minor version increments instead of always incrementing patch version.

**Detailed Steps:**

1. **Update the version determination step in workflow**
   - Edit `.github/workflows/release.yml`
   - Locate the "Get current version and calculate new version" step
   - Replace the simple patch increment with keyword detection logic

2. **Implement keyword detection**
   ```yaml
     - name: Determine version increment type
       id: version
       run: |
         # Get current version
         CURRENT_VERSION=$(python build/version_manager.py get)
         echo "current=$CURRENT_VERSION" >> $GITHUB_OUTPUT
         
         # Get PR description
         PR_BODY="${{ github.event.pull_request.body }}"
         PR_TITLE="${{ github.event.pull_request.title }}"
         
         # Detect version increment keyword
         # Priority: explicit version > major > minor > patch (default)
         INCREMENT_TYPE="patch"
         
         # Check for explicit version: [version:X.Y.Z]
         if echo "$PR_BODY" | grep -qE '\[version:[0-9]+\.[0-9]+\.[0-9]+\]'; then
           EXPLICIT_VERSION=$(echo "$PR_BODY" | grep -oE '\[version:[0-9]+\.[0-9]+\.[0-9]+\]' | sed 's/\[version://; s/\]//')
           echo "increment=explicit" >> $GITHUB_OUTPUT
           echo "new=$EXPLICIT_VERSION" >> $GITHUB_OUTPUT
           echo "Version explicitly set to: $EXPLICIT_VERSION"
         # Check for [major] keyword
         elif echo "$PR_BODY $PR_TITLE" | grep -qiE '\[major\]'; then
           INCREMENT_TYPE="major"
           NEW_VERSION=$(python build/version_manager.py increment --type major)
           echo "increment=major" >> $GITHUB_OUTPUT
           echo "new=$NEW_VERSION" >> $GITHUB_OUTPUT
           echo "Major version increment: $CURRENT_VERSION -> $NEW_VERSION"
         # Check for [minor] keyword
         elif echo "$PR_BODY $PR_TITLE" | grep -qiE '\[minor\]'; then
           INCREMENT_TYPE="minor"
           NEW_VERSION=$(python build/version_manager.py increment --type minor)
           echo "increment=minor" >> $GITHUB_OUTPUT
           echo "new=$NEW_VERSION" >> $GITHUB_OUTPUT
           echo "Minor version increment: $CURRENT_VERSION -> $NEW_VERSION"
         # Default to patch
         else
           INCREMENT_TYPE="patch"
           NEW_VERSION=$(python build/version_manager.py increment --type patch)
           echo "increment=patch" >> $GITHUB_OUTPUT
           echo "new=$NEW_VERSION" >> $GITHUB_OUTPUT
           echo "Patch version increment: $CURRENT_VERSION -> $NEW_VERSION"
         fi
   ```

3. **Add version validation step**
   ```yaml
     - name: Validate new version
       run: |
         # Validate version format
         if ! python build/version_manager.py validate ${{ steps.version.outputs.new }}; then
           echo "Error: Invalid version format: ${{ steps.version.outputs.new }}"
           exit 1
         fi
         
         # Check that new version is greater than current version
         CURRENT="${{ steps.version.outputs.current }}"
         NEW="${{ steps.version.outputs.new }}"
         
         if [ "$CURRENT" = "$NEW" ]; then
           echo "Error: New version ($NEW) is the same as current version ($CURRENT)"
           exit 1
         fi
         
         # Use version_manager to compare
         python build/version_manager.py compare "$CURRENT" "$NEW"
   ```

4. **Add PR comment step for version preview**
   ```yaml
     - name: Add comment to PR with version info
       uses: actions/github-script@v7
       if: success()
       with:
         script: |
           const currentVersion = '${{ steps.version.outputs.current }}';
           const newVersion = '${{ steps.version.outputs.new }}';
           const incrementType = '${{ steps.version.outputs.increment }}';
           
           const comment = `## 🚀 Release Automation
           
           Version will be updated:
           - **Current**: \`${currentVersion}\`
           - **New**: \`${newVersion}\`
           - **Increment Type**: \`${incrementType}\`
           
           Release will be created automatically after merge.`;
           
           github.rest.issues.createComment({
             owner: context.repo.owner,
             repo: context.repo.repo,
             issue_number: context.issue.number,
             body: comment
           });
   ```

5. **Update documentation**
   - Create or update `docs/release-process.md` (or add section to README.md)
   - Document the keyword system:
     ```markdown
     ## Version Control Keywords
     
     Control the version increment by including keywords in your PR description:
     
     - **[patch]** (default): Increment patch version (X.Y.Z -> X.Y.Z+1)
       - Use for bug fixes and small changes
       - Example: 2.1.0 -> 2.1.1
     
     - **[minor]**: Increment minor version (X.Y.Z -> X.Y+1.0)
       - Use for new features (backward compatible)
       - Example: 2.1.0 -> 2.2.0
     
     - **[major]**: Increment major version (X.Y.Z -> X+1.0.0)
       - Use for breaking changes
       - Example: 2.1.0 -> 3.0.0
     
     - **[version:X.Y.Z]**: Set explicit version
       - Use for special cases (hotfixes, etc.)
       - Example: [version:2.1.5]
     
     ### Examples
     
     PR Description with minor increment:
     ```
     This PR adds a new feature for CSV export.
     
     [minor]
     ```
     
     PR Description with explicit version:
     ```
     Hotfix for critical issue.
     
     [version:2.1.3]
     ```
     ```

6. **Create PR template**
   - Create `.github/PULL_REQUEST_TEMPLATE.md` if it doesn't exist
   - Add version control reminder:
     ```markdown
     ## Description
     [Describe your changes]
     
     ## Version Increment (for main branch PRs)
     Add one of the following keywords to control version increment:
     - [ ] [patch] - Bug fixes, small changes (default)
     - [ ] [minor] - New features (backward compatible)
     - [ ] [major] - Breaking changes
     - [ ] [version:X.Y.Z] - Explicit version
     ```

**Testing and Validation:**

1. **Test patch increment (default behavior)**
   ```bash
   # Create test PR to main without any keyword
   # Verify workflow increments patch version
   # Current: 2.1.0 -> Expected: 2.1.1
   ```

2. **Test minor increment**
   ```bash
   # Create test PR to main with [minor] in description
   # Verify workflow increments minor version
   # Current: 2.1.0 -> Expected: 2.2.0
   ```

3. **Test major increment**
   ```bash
   # Create test PR to main with [major] in description
   # Verify workflow increments major version
   # Current: 2.1.0 -> Expected: 3.0.0
   ```

4. **Test explicit version**
   ```bash
   # Create test PR to main with [version:2.5.0] in description
   # Verify workflow uses explicit version
   # Current: 2.1.0 -> Expected: 2.5.0
   ```

5. **Test keyword in PR title**
   ```bash
   # Create test PR with [minor] in title instead of body
   # Verify workflow detects it correctly
   ```

6. **Test invalid explicit version**
   ```bash
   # Create test PR with [version:invalid] in description
   # Verify workflow fails with clear error message
   ```

7. **Test version comparison validation**
   ```bash
   # Create test PR with [version:2.0.0] (lower than current)
   # Verify workflow fails with error about version not being greater
   ```

8. **Verify PR comment appears**
   - Create a test PR
   - Check that automated comment appears showing version increment plan
   - Verify comment has correct current and new versions
   - Verify increment type is displayed correctly

9. **Test edge cases**
   - Multiple keywords in description (first one wins)
   - Case sensitivity ([MAJOR] vs [major])
   - Keywords in code blocks (should be ignored)

**Expected Deliverables:**
- Enhanced `.github/workflows/release.yml` with keyword detection
- Documentation of version control keywords
- PR template with version increment options
- Version validation logic

**Success Criteria:**
- [ ] Default behavior (no keyword) increments patch version
- [ ] [minor] keyword increments minor version correctly
- [ ] [major] keyword increments major version correctly
- [ ] [version:X.Y.Z] sets explicit version correctly
- [ ] Keywords work in both PR title and description
- [ ] Invalid versions are rejected with clear errors
- [ ] Version comparison validates new > current
- [ ] PR comment shows version increment plan
- [ ] Documentation is clear and comprehensive
- [ ] PR template guides users on version control

---

## Prompt 6: Add Validation and Safety Checks to Release Workflow (Phase 3)

**Prerequisites:**
- Prompt 1 completed (build.py supports CI mode)
- Prompt 2 completed (version_manager.py exists)
- Prompt 3 completed (generate_release_notes.py exists)
- Prompt 4 completed (basic release workflow exists)
- Prompt 5 completed (version control keywords implemented)

**Objective:**
Add comprehensive validation and safety checks to the release workflow to prevent common errors and ensure release quality. This includes tag conflict detection, artifact verification, and pre-release validation.

**Detailed Steps:**

1. **Add tag conflict detection step**
   - Edit `.github/workflows/release.yml`
   - Add new step after version determination:
   ```yaml
     - name: Check for tag conflicts
       run: |
         NEW_VERSION="${{ steps.version.outputs.new }}"
         TAG_NAME="v${NEW_VERSION}"
         
         # Check if tag already exists locally
         if git rev-parse "$TAG_NAME" >/dev/null 2>&1; then
           echo "Error: Tag $TAG_NAME already exists locally"
           exit 1
         fi
         
         # Check if tag exists on remote
         if git ls-remote --tags origin | grep -q "refs/tags/$TAG_NAME$"; then
           echo "Error: Tag $TAG_NAME already exists on remote"
           echo "This usually means a release for version $NEW_VERSION already exists"
           exit 1
         fi
         
         echo "✓ Tag $TAG_NAME is available"
   ```

2. **Add build artifact verification step**
   - Add new step after build artifacts step:
   ```yaml
     - name: Verify build artifacts
       run: |
         NEW_VERSION="${{ steps.version.outputs.new }}"
         ZIP_FILE="build/rdd-v${NEW_VERSION}.zip"
         SHA_FILE="build/rdd-v${NEW_VERSION}.zip.sha256"
         
         echo "Verifying artifacts for version $NEW_VERSION..."
         
         # Check zip file exists
         if [ ! -f "$ZIP_FILE" ]; then
           echo "Error: ZIP artifact not found: $ZIP_FILE"
           exit 1
         fi
         
         # Check sha256 file exists
         if [ ! -f "$SHA_FILE" ]; then
           echo "Error: SHA256 checksum not found: $SHA_FILE"
           exit 1
         fi
         
         # Verify zip file is not empty
         ZIP_SIZE=$(stat -f%z "$ZIP_FILE" 2>/dev/null || stat -c%s "$ZIP_FILE")
         if [ "$ZIP_SIZE" -lt 1000 ]; then
           echo "Error: ZIP file is too small (${ZIP_SIZE} bytes), likely corrupted"
           exit 1
         fi
         
         # Verify zip file integrity
         if ! unzip -t "$ZIP_FILE" >/dev/null; then
           echo "Error: ZIP file is corrupted or invalid"
           exit 1
         fi
         
         # Verify SHA256 checksum matches
         cd build
         if ! sha256sum -c "rdd-v${NEW_VERSION}.zip.sha256"; then
           echo "Error: SHA256 checksum verification failed"
           exit 1
         fi
         cd ..
         
         # Verify zip contains expected files
         if ! unzip -l "$ZIP_FILE" | grep -q ".rdd/"; then
           echo "Error: ZIP file doesn't contain .rdd/ directory"
           exit 1
         fi
         
         if ! unzip -l "$ZIP_FILE" | grep -q "README.md"; then
           echo "Error: ZIP file doesn't contain README.md"
           exit 1
         fi
         
         echo "✓ All artifacts verified successfully"
         echo "  - ZIP size: ${ZIP_SIZE} bytes"
         echo "  - SHA256: verified"
         echo "  - ZIP integrity: valid"
         echo "  - Required files: present"
   ```

3. **Add release notes validation step**
   - Add new step after release notes generation:
   ```yaml
     - name: Validate release notes
       run: |
         NEW_VERSION="${{ steps.version.outputs.new }}"
         NOTES_FILE="build/release-notes-v${NEW_VERSION}.md"
         
         echo "Validating release notes..."
         
         # Check file exists
         if [ ! -f "$NOTES_FILE" ]; then
           echo "Error: Release notes not found: $NOTES_FILE"
           exit 1
         fi
         
         # Check file is not empty
         if [ ! -s "$NOTES_FILE" ]; then
           echo "Error: Release notes file is empty"
           exit 1
         fi
         
         # Check file contains version number
         if ! grep -q "$NEW_VERSION" "$NOTES_FILE"; then
           echo "Error: Release notes don't contain version $NEW_VERSION"
           exit 1
         fi
         
         # Check file has proper markdown structure
         if ! grep -q "^#" "$NOTES_FILE"; then
           echo "Warning: Release notes missing markdown headers"
         fi
         
         # Count number of lines
         LINE_COUNT=$(wc -l < "$NOTES_FILE")
         echo "✓ Release notes validated successfully"
         echo "  - File size: $(stat -f%z "$NOTES_FILE" 2>/dev/null || stat -c%s "$NOTES_FILE") bytes"
         echo "  - Lines: $LINE_COUNT"
   ```

4. **Add pre-commit validation step**
   - Add new step before committing version bump:
   ```yaml
     - name: Pre-commit validation
       run: |
         echo "Running pre-commit validation..."
         
         # Check that manifest.json is valid JSON
         if ! python -m json.tool .rdd/config/manifest.json > /dev/null; then
           echo "Error: manifest.json is not valid JSON"
           exit 1
         fi
         
         # Verify version in manifest matches expected
         MANIFEST_VERSION=$(python build/version_manager.py get)
         EXPECTED_VERSION="${{ steps.version.outputs.new }}"
         
         if [ "$MANIFEST_VERSION" != "$EXPECTED_VERSION" ]; then
           echo "Error: Version mismatch"
           echo "  Manifest: $MANIFEST_VERSION"
           echo "  Expected: $EXPECTED_VERSION"
           exit 1
         fi
         
         # Check for uncommitted changes (other than what we expect)
         EXPECTED_CHANGES=".rdd/config/manifest.json build/release-notes-v${EXPECTED_VERSION}.md"
         
         echo "✓ Pre-commit validation passed"
   ```

5. **Add duplicate release check**
   - Add new step before creating GitHub release:
   ```yaml
     - name: Check for duplicate releases
       run: |
         NEW_VERSION="${{ steps.version.outputs.new }}"
         
         # Check if release already exists on GitHub
         if gh release view "v${NEW_VERSION}" >/dev/null 2>&1; then
           echo "Error: Release v${NEW_VERSION} already exists on GitHub"
           echo "Please delete the existing release or use a different version"
           exit 1
         fi
         
         echo "✓ No duplicate release found"
       env:
         GH_TOKEN: ${{ github.token }}
   ```

6. **Add workflow summary step**
   - Add new step at the end of workflow (before success/failure reports):
   ```yaml
     - name: Generate workflow summary
       if: always()
       run: |
         cat >> $GITHUB_STEP_SUMMARY << 'EOF'
         ## Release Workflow Summary
         
         | Item | Value |
         |------|-------|
         | **Current Version** | `${{ steps.version.outputs.current }}` |
         | **New Version** | `${{ steps.version.outputs.new }}` |
         | **Increment Type** | `${{ steps.version.outputs.increment }}` |
         | **Tag** | `v${{ steps.version.outputs.new }}` |
         | **PR** | #${{ github.event.pull_request.number }} |
         | **Branch** | `${{ github.event.pull_request.head.ref }}` |
         
         ### Validation Checks
         - ✅ Tag availability verified
         - ✅ Build artifacts created
         - ✅ Artifact integrity verified
         - ✅ Release notes generated
         - ✅ Manifest.json updated
         - ✅ Version validated
         
         ### Generated Artifacts
         - `build/rdd-v${{ steps.version.outputs.new }}.zip`
         - `build/rdd-v${{ steps.version.outputs.new }}.zip.sha256`
         - `build/release-notes-v${{ steps.version.outputs.new }}.md`
         EOF
   ```

7. **Add cleanup on failure**
   - Add new step that runs only on failure:
   ```yaml
     - name: Cleanup on failure
       if: failure()
       run: |
         NEW_VERSION="${{ steps.version.outputs.new }}"
         
         echo "Cleaning up after failed release attempt..."
         
         # Remove build artifacts
         rm -f "build/rdd-v${NEW_VERSION}.zip" || true
         rm -f "build/rdd-v${NEW_VERSION}.zip.sha256" || true
         rm -f "build/release-notes-v${NEW_VERSION}.md" || true
         
         # Note: We don't revert manifest.json changes as they haven't been pushed yet
         
         echo "✓ Cleanup completed"
   ```

8. **Update documentation**
   - Update `docs/release-process.md` with validation information:
     ```markdown
     ## Validation Checks
     
     The release workflow performs the following validation checks:
     
     1. **Tag Conflict Detection**: Ensures the version tag doesn't already exist
     2. **Build Artifact Verification**: Validates ZIP integrity and content
     3. **SHA256 Checksum Verification**: Ensures checksum matches artifact
     4. **Release Notes Validation**: Checks notes are generated correctly
     5. **Manifest Validation**: Ensures manifest.json is valid JSON with correct version
     6. **Duplicate Release Check**: Prevents creating duplicate GitHub releases
     
     If any check fails, the workflow will stop and roll back changes.
     ```

**Testing and Validation:**

1. **Test tag conflict detection**
   ```bash
   # Create a tag manually
   git tag v9.9.9
   git push origin v9.9.9
   
   # Create PR with [version:9.9.9] and merge
   # Verify workflow fails with tag conflict error
   
   # Cleanup
   git tag -d v9.9.9
   git push --delete origin v9.9.9
   ```

2. **Test with corrupted build artifact**
   ```bash
   # Temporarily modify build.py to create invalid zip
   # Verify workflow fails at artifact verification step
   # Restore build.py
   ```

3. **Test with empty release notes**
   ```bash
   # Temporarily modify generate_release_notes.py to create empty file
   # Verify workflow fails at release notes validation
   # Restore generate_release_notes.py
   ```

4. **Test manifest validation**
   ```bash
   # Temporarily break manifest.json format (invalid JSON)
   # Verify workflow fails at pre-commit validation
   # Restore manifest.json
   ```

5. **Test duplicate release check**
   ```bash
   # Create a release manually with version v9.9.8
   # Create PR with [version:9.9.8] and merge
   # Verify workflow fails with duplicate release error
   # Delete manual release
   ```

6. **Test normal successful flow**
   ```bash
   # Create a normal PR and merge
   # Verify all validation checks pass
   # Verify workflow summary is generated correctly
   ```

7. **Verify workflow summary**
   - Check GitHub Actions run page
   - Verify summary section shows:
     - Version information
     - Validation checklist
     - Generated artifacts list

8. **Test cleanup on failure**
   - Trigger a workflow that fails (e.g., tag conflict)
   - Verify build artifacts are cleaned up
   - Verify no uncommitted changes remain

**Expected Deliverables:**
- Enhanced `.github/workflows/release.yml` with comprehensive validation
- Tag conflict detection
- Build artifact verification
- Release notes validation
- Cleanup on failure
- Updated documentation

**Success Criteria:**
- [ ] Tag conflict detection prevents duplicate tags
- [ ] Build artifact verification catches corrupted builds
- [ ] SHA256 checksum is verified correctly
- [ ] Release notes validation ensures quality notes
- [ ] Manifest.json validation prevents invalid JSON
- [ ] Duplicate release check prevents conflicts
- [ ] Workflow summary provides clear information
- [ ] Cleanup on failure removes partial artifacts
- [ ] All validation checks work correctly
- [ ] Documentation is updated with validation info

---

## Prompt 7: Update Documentation and Create User Guide

**Prerequisites:**
- Prompt 1 completed (build.py supports CI mode)
- Prompt 2 completed (version_manager.py exists)
- Prompt 3 completed (generate_release_notes.py exists)
- Prompt 4 completed (basic release workflow exists)
- Prompt 5 completed (version control keywords implemented)
- Prompt 6 completed (validation and safety checks added)

**Objective:**
Create comprehensive documentation for the automated release system, including user guides, troubleshooting information, and maintenance procedures.

**Detailed Steps:**

1. **Create main release process documentation**
   - Create new file: `docs/release-process.md`
   - Structure:
     ```markdown
     # Release Process Documentation
     
     ## Overview
     [Explain automated release system]
     
     ## How It Works
     [Explain trigger, workflow steps, outputs]
     
     ## Version Control
     [Explain version increment keywords]
     
     ## Creating a Release
     [Step-by-step guide for developers]
     
     ## Validation Checks
     [List all validation checks]
     
     ## Troubleshooting
     [Common issues and solutions]
     
     ## Manual Override
     [How to create manual release if needed]
     ```

2. **Write overview section**
   ```markdown
   ## Overview
   
   The RDD Framework uses an automated release system that creates new releases
   whenever a pull request is merged to the `main` branch. This system:
   
   - Automatically determines version increments
   - Builds release artifacts
   - Generates release notes from commits and RDD workdir
   - Creates git tags
   - Publishes GitHub releases
   
   The entire process is fully automated and requires no manual intervention.
   ```

3. **Write "How It Works" section**
   ```markdown
   ## How It Works
   
   ### Trigger
   The release workflow is triggered when a pull request is closed AND merged to `main`.
   
   ### Workflow Steps
   
   1. **Version Determination**: Analyzes PR description for version keywords
   2. **Version Validation**: Ensures version is valid and not duplicate
   3. **Manifest Update**: Updates version in `.rdd/config/manifest.json`
   4. **Build Artifacts**: Runs `build.py` to create release package
   5. **Artifact Verification**: Validates ZIP integrity and checksum
   6. **Release Notes**: Generates notes from git history and RDD workdir
   7. **Commit Changes**: Commits manifest and release notes to main
   8. **Tag Creation**: Creates and pushes git tag
   9. **GitHub Release**: Publishes release with artifacts
   
   ### Outputs
   
   After successful completion, the workflow creates:
   
   - Git tag: `v{version}`
   - GitHub Release with:
     - Release notes
     - `rdd-v{version}.zip` - Framework package
     - `rdd-v{version}.zip.sha256` - Checksum file
     - `release-notes-v{version}.md` - Release notes file
   - Repository commit with updated manifest and release notes
   ```

4. **Write "Version Control" section**
   ```markdown
   ## Version Control
   
   ### Version Increment Keywords
   
   Control the version increment by adding a keyword to your PR description:
   
   | Keyword | Effect | Example | Use Case |
   |---------|--------|---------|----------|
   | (none) | Patch increment | 2.1.0 → 2.1.1 | Bug fixes, small changes |
   | `[minor]` | Minor increment | 2.1.0 → 2.2.0 | New features (backward compatible) |
   | `[major]` | Major increment | 2.1.0 → 3.0.0 | Breaking changes |
   | `[version:X.Y.Z]` | Explicit version | 2.1.0 → X.Y.Z | Special cases, hotfixes |
   
   ### Examples
   
   **Patch increment (default)**:
   ```
   PR Description:
   Fix bug in build script that caused validation errors.
   ```
   Result: Version increments from 2.1.0 to 2.1.1
   
   **Minor increment**:
   ```
   PR Description:
   Add new CSV export feature to the framework.
   
   [minor]
   ```
   Result: Version increments from 2.1.0 to 2.2.0
   
   **Major increment**:
   ```
   PR Description:
   Restructure API - breaking changes to prompt format.
   
   [major]
   ```
   Result: Version increments from 2.1.0 to 3.0.0
   
   **Explicit version**:
   ```
   PR Description:
   Critical hotfix for production issue.
   
   [version:2.1.5]
   ```
   Result: Version set to 2.1.5
   
   ### Best Practices
   
   - Use patch increment for bug fixes and minor improvements
   - Use minor increment for new features that don't break compatibility
   - Use major increment for breaking changes or major architectural changes
   - Use explicit version sparingly, only for special situations
   - Keywords can appear anywhere in PR title or description
   - Only one keyword will be used (priority: explicit > major > minor > patch)
   ```

5. **Write "Creating a Release" section**
   ```markdown
   ## Creating a Release
   
   ### Step-by-Step Guide
   
   1. **Prepare Your Changes**
      - Complete your work in a feature branch
      - Merge feature branch to `dev` branch
      - Test thoroughly in `dev`
   
   2. **Create PR from dev to main**
      ```bash
      # From dev branch
      git checkout dev
      git pull origin dev
      
      # Create PR via GitHub UI or gh CLI
      gh pr create --base main --head dev --title "Release X.Y.Z"
      ```
   
   3. **Add Version Keyword to PR**
      - Edit PR description
      - Add appropriate keyword ([minor], [major], or [version:X.Y.Z])
      - If no keyword, patch version will be used
   
   4. **Review PR**
      - Review changes in PR
      - Check automated comment showing version increment plan
      - Ensure all CI checks pass
   
   5. **Merge PR**
      - Click "Merge pull request"
      - Release workflow will start automatically
   
   6. **Monitor Workflow**
      - Go to Actions tab in GitHub
      - Watch "Create Release" workflow execution
      - Check for any errors
   
   7. **Verify Release**
      - Navigate to Releases page
      - Verify new release is published
      - Check artifacts are attached
      - Review release notes
   
   ### What to Expect
   
   - Workflow takes approximately 2-5 minutes to complete
   - You'll receive GitHub notification when release is published
   - Version in `main` branch will be updated
   - Git tag will be created
   - Release notes will be generated automatically
   
   ### Checklist
   
   Before merging PR to main:
   - [ ] All features are tested and working
   - [ ] CI/CD checks pass
   - [ ] Appropriate version keyword is in PR description
   - [ ] Breaking changes are documented (if [major])
   - [ ] Release notes will be meaningful
   ```

6. **Write "Validation Checks" section**
   ```markdown
   ## Validation Checks
   
   The release workflow performs multiple validation checks to ensure quality:
   
   ### 1. Tag Conflict Detection
   - **What**: Checks if version tag already exists
   - **Why**: Prevents duplicate releases and version conflicts
   - **Failure**: Workflow stops if tag exists
   - **Fix**: Use different version or delete old tag
   
   ### 2. Build Artifact Verification
   - **What**: Validates ZIP file integrity and content
   - **Why**: Ensures release package is not corrupted
   - **Checks**:
     - ZIP file exists and is not empty
     - ZIP file can be extracted without errors
     - ZIP contains `.rdd/` directory
     - ZIP contains `README.md`
   - **Failure**: Workflow stops if verification fails
   - **Fix**: Check build.py script for issues
   
   ### 3. SHA256 Checksum Verification
   - **What**: Verifies checksum matches artifact
   - **Why**: Ensures artifact integrity and authenticity
   - **Failure**: Workflow stops if checksum doesn't match
   - **Fix**: Check build.py checksum generation
   
   ### 4. Release Notes Validation
   - **What**: Checks release notes are generated properly
   - **Why**: Ensures meaningful release documentation
   - **Checks**:
     - File exists and is not empty
     - Contains version number
     - Has markdown structure
   - **Failure**: Workflow stops if validation fails
   - **Fix**: Check generate_release_notes.py script
   
   ### 5. Manifest Validation
   - **What**: Validates manifest.json format and version
   - **Why**: Ensures manifest is valid JSON with correct version
   - **Checks**:
     - Valid JSON format
     - Version matches expected version
   - **Failure**: Workflow stops if manifest is invalid
   - **Fix**: Check version_manager.py script
   
   ### 6. Duplicate Release Check
   - **What**: Checks if GitHub release already exists
   - **Why**: Prevents duplicate releases
   - **Failure**: Workflow stops if release exists
   - **Fix**: Delete existing release or use different version
   ```

7. **Write "Troubleshooting" section**
   ```markdown
   ## Troubleshooting
   
   ### Common Issues
   
   #### Issue: Workflow doesn't trigger
   
   **Symptoms**: No workflow run after merging PR
   
   **Possible Causes**:
   - PR was closed without merging
   - PR was merged to wrong branch (not main)
   - Workflow file has syntax errors
   
   **Solutions**:
   1. Check PR was actually merged (not just closed)
   2. Verify PR was merged to `main` branch
   3. Check `.github/workflows/release.yml` syntax
   4. Check GitHub Actions is enabled for repository
   
   #### Issue: Tag conflict error
   
   **Symptoms**: Workflow fails with "Tag already exists"
   
   **Solutions**:
   ```bash
   # Check existing tags
   git tag -l
   
   # Delete local tag
   git tag -d v2.1.0
   
   # Delete remote tag
   git push --delete origin v2.1.0
   
   # Re-run workflow
   ```
   
   #### Issue: Build artifact verification fails
   
   **Symptoms**: Workflow fails at "Verify build artifacts" step
   
   **Possible Causes**:
   - build.py script has errors
   - Disk space issues
   - Permission issues
   
   **Solutions**:
   1. Test build locally:
      ```bash
      python build/build.py --version 2.1.0 --non-interactive
      ```
   2. Check build.py error messages
   3. Verify required files are being included in ZIP
   
   #### Issue: Version not incrementing correctly
   
   **Symptoms**: Wrong version number in release
   
   **Possible Causes**:
   - Wrong keyword in PR description
   - manifest.json not updated
   
   **Solutions**:
   1. Check PR description for correct keyword
   2. Verify version_manager.py is working:
      ```bash
      python build/version_manager.py get
      python build/version_manager.py increment --type minor
      ```
   
   #### Issue: Release notes are empty or incorrect
   
   **Symptoms**: Release notes missing information
   
   **Solutions**:
   1. Test release notes generation locally:
      ```bash
      python build/generate_release_notes.py --version 2.1.0
      ```
   2. Check git commit history
   3. Verify RDD workdir has implementation files
   
   ### Emergency Procedures
   
   #### Delete a Failed Release
   
   ```bash
   # Using GitHub CLI
   gh release delete v2.1.0 --yes
   
   # Delete the tag
   git push --delete origin v2.1.0
   git tag -d v2.1.0
   
   # Revert manifest.json if needed
   git revert <commit-hash>
   git push origin main
   ```
   
   #### Create Manual Release (if automation fails)
   
   ```bash
   # 1. Update version manually
   python build/version_manager.py update 2.1.0
   
   # 2. Build artifacts
   python build/build.py --version 2.1.0 --non-interactive
   
   # 3. Generate release notes
   python build/generate_release_notes.py --version 2.1.0
   
   # 4. Create tag
   git add .rdd/config/manifest.json build/release-notes-v2.1.0.md
   git commit -m "chore: bump version to 2.1.0"
   git tag -a v2.1.0 -m "Release v2.1.0"
   git push origin main --tags
   
   # 5. Create GitHub release manually via web UI
   # Upload artifacts from build/ folder
   ```
   ```

8. **Update main README.md**
   - Add section about automated releases:
   ```markdown
   ## Releases
   
   The RDD Framework uses automated releases. When a PR is merged to `main`,
   a new release is automatically created.
   
   ### For Users
   
   Download the latest release from the
   [Releases page](https://github.com/your-org/repo/releases).
   
   Each release includes:
   - Framework package (rdd-vX.Y.Z.zip)
   - SHA256 checksum file
   - Detailed release notes
   
   ### For Contributors
   
   See [Release Process Documentation](docs/release-process.md) for details on:
   - How releases are created
   - Version control keywords
   - Troubleshooting
   
   ### Version Control
   
   Control version increments by adding keywords to your PR description:
   - No keyword = patch increment (2.1.0 → 2.1.1)
   - `[minor]` = minor increment (2.1.0 → 2.2.0)
   - `[major]` = major increment (2.1.0 → 3.0.0)
   - `[version:X.Y.Z]` = explicit version
   ```

9. **Create quick reference card**
   - Create file: `docs/release-quick-reference.md`
   - Include:
     - Common commands
     - Version keywords
     - Troubleshooting quick fixes
     - Emergency contacts/procedures

**Testing and Validation:**

1. **Review documentation for accuracy**
   - Read through all documentation
   - Verify all commands are correct
   - Check all links work
   - Ensure examples are up-to-date

2. **Test all commands in documentation**
   ```bash
   # Test each command example
   python build/version_manager.py get
   python build/version_manager.py increment --type minor
   python build/generate_release_notes.py --version 2.1.0
   etc.
   ```

3. **Validate markdown formatting**
   ```bash
   # Use markdown linter or preview
   # Check that all markdown renders correctly
   ```

4. **Test troubleshooting procedures**
   - Follow each troubleshooting step
   - Verify solutions work as described
   - Update if anything is incorrect

5. **Peer review**
   - Have another developer review documentation
   - Check for clarity and completeness
   - Gather feedback on usefulness

**Expected Deliverables:**
- Comprehensive `docs/release-process.md`
- Updated `README.md` with release information
- Quick reference guide
- All documentation tested and validated

**Success Criteria:**
- [ ] Documentation covers all aspects of release system
- [ ] Examples are clear and working
- [ ] Troubleshooting section covers common issues
- [ ] Quick reference provides fast access to key information
- [ ] README.md is updated with release information
- [ ] All commands in documentation work correctly
- [ ] Documentation is clear for both users and contributors
- [ ] Links and formatting are correct

---

## Summary

This series of 7 prompts implements the complete release automation system following the phased approach outlined in the P-034 analysis:

**Phase 1 (Prompts 1-4): Basic Automation**
- Non-interactive build.py
- Version management utilities
- Release notes generation
- Basic GitHub Actions workflow

**Phase 2 (Prompt 5): Enhanced Version Control**
- Keyword-based version increment control
- Flexible versioning options

**Phase 3 (Prompts 6-7): Advanced Features**
- Comprehensive validation and safety checks
- Complete documentation and user guides

Each prompt includes:
- Clear prerequisites
- Detailed step-by-step instructions
- Comprehensive testing and validation procedures
- Success criteria

The prompts should be executed in order to build up the complete release automation system incrementally.
