# P01 Implementation: GitHub Release Process Design

## Task Summary
Design and analyze a comprehensive release process for the RDD framework GitHub repository, including builds, releases, naming conventions, scripts, automations, and CI/CD components.

## Current State Analysis

### Existing Infrastructure

#### Build System
- **Location**: `scripts/build.sh`
- **Current Capabilities**:
  - Creates platform-specific archives (Linux and Windows)
  - Extracts version from script files
  - Copies necessary files (.github/prompts, .rdd/templates, .rdd/scripts)
  - Note: Currently references bash scripts, but framework has migrated to Python
  - Includes bash-to-PowerShell conversion logic (now obsolete due to Python migration)

#### Version Management
- Version extracted from: `.rdd/scripts/rdd.sh` (legacy)
- Current approach: Hardcoded version string in scripts
- **Issue**: After Python migration, version should be extracted from `rdd.py`

#### Git Ignore Configuration
- Build artifacts excluded: `build/` directory
- Workspace excluded: `.rdd-docs/workspace/`

#### VS Code Settings
- Auto-approval configured for: `python .rdd/scripts/rdd.py`
- JSONL file associations configured
- Prompt file recommendations configured

### Project Requirements Context

#### Key Requirements from requirements.md
- **[FR-47]**: Python-Based Script Implementation
- **[FR-48]**: Cross-Platform Python Command (`python` not `python3`)
- **[FR-49]**: Python Command Installation Guidance
- **[TR-29]**: Python 3.7+ Requirement
- **[TR-30]**: Platform-Agnostic Python Command

#### Current Technology Stack
- **Python 3.7+**: Primary scripting language
- **Git 2.23+**: Version control
- **Cross-platform support**: Single Python codebase for Windows, Linux, macOS

### Framework Structure

#### Core Components to Include in Release
1. **Prompts**: `.github/prompts/rdd.*.prompt.md`
2. **Scripts**: `.rdd/scripts/rdd.py` and `.rdd/scripts/rdd_utils.py`
3. **Templates**: `.rdd/templates/*.md`
4. **VS Code Settings**: `.rdd/templates/settings.json`
5. **Documentation**: README.md, LICENSE
6. **Installation Script**: To be created

#### Files NOT to Include
- `.rdd-docs/` (except templates)
- `build/` directory
- `src/` directory (legacy platform-specific code)
- `__pycache__/` directories
- Test files (unless decided otherwise)

## Research: Best Practices for Python Tool Distribution

### Industry Standards Research

#### 1. Versioning Strategy - Semantic Versioning (SemVer)
**Standard**: MAJOR.MINOR.PATCH (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes
- **Pre-release**: alpha, beta, rc (e.g., 1.0.0-beta.1)

**Application to RDD**:
- Current version: 1.0.0 (from rdd.py)
- Should be centralized in one location
- Git tags should match release versions

**Sources**:
- [Semantic Versioning Specification](https://semver.org/)
- Python Packaging Guide recommendations

#### 2. Release Naming Convention
**Best Practice Pattern**: `<tool-name>-v<version>.<format>`
- Examples: `rdd-v1.0.0.zip`, `rdd-v1.2.3.tar.gz`
- No platform suffix needed for Python (cross-platform)
- Consider: `rdd-v1.0.0-installer.zip` for full release

**Application to RDD**:
- Single archive: `rdd-v<version>.zip`
- No need for separate Linux/Windows builds (Python is cross-platform)
- Archive contains installer script and all components

#### 3. Python Tool Distribution Methods

##### Option A: PyPI Package (pip installable)
**Pros**:
- Standard Python distribution method
- Simple installation: `pip install rdd-framework`
- Automatic dependency management
- Version management built-in

**Cons**:
- Requires package structure refactoring
- VS Code integration more complex
- Templates and prompts need special handling

##### Option B: Git Clone + Setup Script
**Pros**:
- Direct access to all files
- Easy to customize
- VS Code integration straightforward
- No packaging overhead

**Cons**:
- Manual updates required
- Users need git knowledge
- Harder to version control user installations

##### Option C: Zip Archive with Installer (RECOMMENDED for RDD)
**Pros**:
- Self-contained distribution
- No external dependencies (except Python)
- Works offline
- Easy to audit before installation
- VS Code integration preserved

**Cons**:
- Manual download required
- No automatic updates

**Why Recommended**: RDD is a development framework that integrates with VS Code and Git repositories. Users need full control over the installation location and configuration.

#### 4. Installation Script Best Practices

**Key Features for Python Installer**:
1. **Pre-flight checks**:
   - Python version verification (>= 3.7)
   - Git availability check
   - Target directory validation

2. **Interactive prompts**:
   - Installation directory
   - VS Code settings merge confirmation
   - PATH addition option

3. **File operations**:
   - Copy prompts to `.github/prompts/`
   - Copy RDD framework to `.rdd/`
   - Merge VS Code settings
   - Update .gitignore

4. **Post-installation**:
   - Verification test
   - Usage instructions
   - Next steps guidance

5. **Error handling**:
   - Rollback on failure
   - Clear error messages
   - Recovery suggestions

**Similar Tools Research**:
- **Poetry**: Uses curl | python installer
- **Pipx**: Self-contained installations
- **pre-commit**: Framework installation in git repos

#### 5. CI/CD for GitHub Releases

##### GitHub Actions Workflow Pattern
**Trigger Events**:
- Manual workflow dispatch
- Git tag push (e.g., `v1.0.0`)
- Release creation

**Build Steps**:
1. Checkout code
2. Set up Python
3. Run tests (if any)
4. Extract version from rdd.py
5. Create build archive
6. Generate checksums
7. Create/update GitHub Release
8. Upload archive as release asset

**Best Practices**:
- Automated release notes generation
- Changelog update automation
- Version validation
- Asset checksums for security

**Example Tools**:
- `actions/create-release`
- `softprops/action-gh-release`
- `marvinpinto/action-automatic-releases`

#### 6. Release Asset Structure

**Recommended Structure**:
```
rdd-v1.0.0.zip
├── install.py              # Installation script
├── README.md               # Installation instructions
├── LICENSE                 # License file
├── .github/
│   └── prompts/            # All prompt files
├── .rdd/
│   ├── scripts/
│   │   ├── rdd.py
│   │   └── rdd_utils.py
│   └── templates/          # All template files
└── .vscode/
    └── settings.json       # VS Code settings to merge
```

**Additional Files**:
- `CHANGELOG.md`: Version history
- `install.py`: Python installer script
- `uninstall.py`: Optional removal script
- `verify.py`: Installation verification

#### 7. Documentation in Release

**Essential Documentation**:
1. **README.md** in archive root:
   - Prerequisites (Python 3.7+, Git)
   - Quick start installation
   - Manual installation steps
   - Troubleshooting

2. **INSTALL.md** (detailed):
   - System requirements
   - Step-by-step installation
   - VS Code configuration
   - Verification steps
   - Uninstallation

3. **CHANGELOG.md**:
   - Version history
   - Breaking changes
   - New features
   - Bug fixes

### Security Considerations

1. **Checksum Verification**:
   - Generate SHA256 checksums for releases
   - Include checksums in release notes
   - Installer should verify integrity

2. **Code Signing**:
   - Consider GPG signing for releases
   - Verify installer authenticity

3. **Dependencies**:
   - Minimize external dependencies
   - Document all requirements
   - Pin versions if needed

## Proposed Solution Architecture

### Phase 1: Update Build System

#### Update build.sh
**Current issues**:
- References legacy bash scripts
- Creates separate Linux/Windows archives (no longer needed)
- Extracts version from wrong file

**Required changes**:
1. Extract version from `rdd.py` instead of `rdd.sh`
2. Create single cross-platform archive
3. Remove bash-to-PowerShell conversion
4. Add changelog generation
5. Generate checksums

#### New build.sh structure:
```bash
#!/bin/bash
# Extract version from rdd.py
# Create build/rdd-v<version>/ structure
# Copy files: prompts, scripts, templates, settings.json
# Create install.py from template
# Add README.md and LICENSE
# Create zip archive
# Generate SHA256 checksum
```

### Phase 2: Create Installation System

#### install.py Script
**Responsibilities**:
1. Verify Python version (>= 3.7)
2. Check git availability
3. Prompt for installation directory
4. Copy prompts to `.github/prompts/`
5. Copy `.rdd/` framework files
6. Merge `.vscode/settings.json`
7. Add `.rdd-docs/workspace/` to `.gitignore`
8. Run verification
9. Display success message with next steps

**Interactive prompts**:
- Target directory (default: current directory)
- VS Code settings merge confirmation
- .gitignore update confirmation

**Error handling**:
- Existing installation detection
- Permission issues
- Missing prerequisites
- Partial installation rollback

#### verify.py Script
**Checks**:
- All files copied correctly
- Python scripts executable
- VS Code settings merged
- .gitignore updated
- Test command: `python .rdd/scripts/rdd.py --version`

### Phase 3: GitHub Release Automation

#### .github/workflows/release.yml
**Workflow**:
```yaml
name: Create Release
on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      version:
        description: 'Release version (e.g., 1.0.0)'
        required: true

jobs:
  build-and-release:
    runs-on: ubuntu-latest
    steps:
      - Checkout code
      - Setup Python 3.10
      - Extract version
      - Run build.sh
      - Generate checksums
      - Create GitHub Release
      - Upload build artifact
      - Update release notes
```

**Automated release notes**:
- Extract from CHANGELOG.md
- Group by change type (Features, Fixes, Breaking Changes)
- Link to commits and PRs

### Phase 4: Version Management

#### Centralized Version
**Single source of truth**: `rdd.py`
```python
__version__ = "1.0.0"
RDD_VERSION = __version__
```

**Version checking**:
- `python .rdd/scripts/rdd.py --version`
- Display in all script outputs
- Logged in execution logs

#### Git Tags
**Convention**: `v<major>.<minor>.<patch>`
- Example: `v1.0.0`, `v1.2.3`
- Tags trigger release workflow
- Tags must match version in `rdd.py`

### Phase 5: Documentation

#### README.md in Release
**Content**:
- What is RDD
- System requirements
- Quick installation (using install.py)
- Manual installation steps
- Verification
- Getting started
- Troubleshooting

#### CHANGELOG.md
**Format**:
```markdown
# Changelog

## [1.0.0] - 2025-11-05
### Added
- Initial release
- Python-based cross-platform implementation
### Changed
- Migrated from bash to Python
### Removed
- Platform-specific scripts
```

## Implementation Checklist

### Immediate Tasks (Phase 1)
- [ ] Update `scripts/build.sh` to extract version from `rdd.py`
- [ ] Modify build.sh to create single cross-platform archive
- [ ] Remove bash-to-PowerShell conversion logic
- [ ] Add checksum generation to build.sh
- [ ] Test build.sh with current codebase

### Phase 2 Tasks
- [ ] Create `install.py` script with interactive prompts
- [ ] Create `verify.py` validation script
- [ ] Add installation README.md template
- [ ] Test installation on clean directory
- [ ] Test installation on existing project

### Phase 3 Tasks
- [ ] Create `.github/workflows/release.yml`
- [ ] Configure GitHub Actions secrets (if needed)
- [ ] Test workflow with test tag
- [ ] Document release process for maintainers

### Phase 4 Tasks
- [ ] Centralize version in `rdd.py`
- [ ] Add version command to rdd.py
- [ ] Create git tag naming convention documentation
- [ ] Update all scripts to use centralized version

### Phase 5 Tasks
- [ ] Create CHANGELOG.md
- [ ] Write installation README.md
- [ ] Create INSTALL.md (detailed)
- [ ] Update main README.md with installation instructions
- [ ] Add troubleshooting section

### Quality Assurance
- [ ] Test installation on Windows
- [ ] Test installation on macOS
- [ ] Test installation on Linux
- [ ] Verify VS Code settings merge
- [ ] Verify .gitignore updates
- [ ] Test uninstallation process
- [ ] Verify checksums
- [ ] Test release workflow end-to-end

## Recommended Next Steps

After this analysis is approved, create the following prompts:

1. **[P02] Update Build System**:
   - Modify scripts/build.sh for Python-based single archive
   - Add version extraction from rdd.py
   - Add checksum generation
   - Test build process

2. **[P03] Create Installation System**:
   - Implement install.py with all requirements
   - Implement verify.py
   - Create installation documentation
   - Test on all platforms

3. **[P04] GitHub Release Automation**:
   - Create GitHub Actions workflow
   - Configure release triggers
   - Test automated release process

4. **[P05] Version Management & Documentation**:
   - Centralize version management
   - Create CHANGELOG.md
   - Update all documentation
   - Create maintainer guide

## Conclusion

The proposed release process for the RDD framework follows industry best practices while being tailored to the unique needs of a development framework that integrates with VS Code and Git repositories. The key decision is to use a **zip archive with Python installer** approach rather than PyPI packaging, as it provides:

1. **Full control**: Users can audit and customize before installation
2. **Simplicity**: No external dependencies beyond Python and Git
3. **Flexibility**: Works in offline environments
4. **Integration**: Preserves VS Code and Git integration

The implementation is divided into 5 phases, allowing for incremental development and testing. The use of GitHub Actions for automated releases ensures consistency and reduces manual work.

The cross-platform nature of Python eliminates the need for separate Windows/Linux builds, simplifying the build process significantly compared to the current bash-based approach.
