# Implementation Log - P-035: Split on prompts the release analysis

## Objective

Create a series of prompts based on the P-034 release automation analysis that can be executed in sequence by GitHub Copilot agents.

## Context Review

### Technical Design
The technical-design.json file is currently empty, so there are no specific technical constraints from the technical design for this task.

### Requirements
Reviewed requirements.md and found the following relevant requirements:
- **UR-0002**: Framework shall maintain a library of predefined framework prompt snippets and persist all composed prompts in Markdown files
- **UR-0005**: Framework shall provide a single prompt implementing the execute command
- **UR-0010**: Prompts shall call scripts for file and folder modifications rather than implementing logic directly

These requirements informed the structure of the prompts - they are detailed, executable instructions that reference scripts and follow best practices for RDD framework prompt construction.

### Files and Folders
Reviewed files-and-folders.md and found the build/ folder structure is highly relevant:
- `build/build.py` - Current build script that needs modification
- `build/release-notes-v*.md` - Release notes pattern
- `.rdd/config/manifest.json` - Version source location

### Prompt Registry
The prompt registry entry for P-034 contains detailed analysis of release automation approaches, phased rollout strategy, and specific implementation recommendations that formed the basis for creating the prompt series.

### Questionnaire Answers
The questionnaire.json had all questions answered:
- **Q1**: Selected Option A - Sequential prompts following phased rollout (Phase 1, Phase 2, Phase 3)
- **Q2**: Selected Option B - Detailed step-by-step instructions extracted from analysis
- **Q3**: Selected Option A - Each prompt includes testing and validation requirements
- **Q4**: Selected Option A - Explicit prerequisites listed at start of each prompt
- **Q5**: Selected Option C - No explicit rollback procedures in prompts

These answers guided the structure and content of the created prompts.

## Analysis Conducted

1. **Read P-034 Analysis**: Thoroughly reviewed the 881-line release automation analysis document
2. **Identified Phased Structure**: The analysis clearly outlined a three-phase approach:
   - Phase 1: Basic Automation (build.py CI support, basic workflow)
   - Phase 2: Enhanced Release Notes (RDD workdir analysis)
   - Phase 3: Advanced Features (version control, validation)
3. **Extracted Key Components**: Identified the main technical components:
   - build.py modifications for CI/CD
   - Version management scripts
   - Release notes generation
   - GitHub Actions workflow
   - Documentation
4. **Mapped to Sequential Prompts**: Based on questionnaire answer Q1, structured prompts sequentially following the phases

## Implementation Steps

### Step 1: Create Prompt Series Document

Created `release_prompts.md` with 7 sequential prompts:

**Prompt 1: Prepare build.py for CI/CD Integration**
- Modify existing build.py to support `--non-interactive` and `--version` arguments
- Maintain backward compatibility with manual execution
- Add comprehensive error handling for CI context
- Include testing procedures for both interactive and non-interactive modes

**Prompt 2: Create Version Management Helper Script**
- New file `build/version_manager.py`
- Functions for get, validate, parse, increment, update, and compare versions
- Command-line interface with subcommands
- JSON output support for CI integration
- Comprehensive error handling

**Prompt 3: Create Release Notes Generator Script**
- New file `build/generate_release_notes.py`
- Git operations (commits, tags, branches)
- RDD workdir analysis integration
- Commit categorization (features, fixes, docs, etc.)
- Markdown and JSON output formats

**Prompt 4: Create GitHub Actions Release Workflow (Phase 1)**
- Basic workflow: `.github/workflows/release.yml`
- Trigger on PR merge to main
- Automatic patch version increment
- Build artifacts and release notes generation
- GitHub release publishing

**Prompt 5: Enhance Release Workflow with Version Control Keywords (Phase 2)**
- Add keyword detection ([major], [minor], [version:X.Y.Z])
- PR description parsing
- Version validation
- PR comment with version increment preview
- Documentation and PR template

**Prompt 6: Add Validation and Safety Checks (Phase 3)**
- Tag conflict detection
- Build artifact verification
- SHA256 checksum validation
- Release notes validation
- Duplicate release check
- Workflow summary generation
- Cleanup on failure

**Prompt 7: Update Documentation and Create User Guide**
- Comprehensive release-process.md
- Updated README.md
- Troubleshooting guide
- Quick reference card
- User and contributor documentation

### Step 2: Structure Each Prompt

Each prompt follows a consistent structure based on questionnaire answers:

1. **Prerequisites** (Q4 - Explicit prerequisites)
   - Lists required completed prompts
   - Notes if it's the first prompt (no prerequisites)

2. **Objective**
   - Clear statement of what the prompt accomplishes

3. **Detailed Steps** (Q2 - Detailed step-by-step instructions)
   - Numbered steps with specific actions
   - Code examples and command samples
   - File paths and exact implementations
   - Extracted directly from P-034 analysis

4. **Testing and Validation** (Q3 - Testing included in each prompt)
   - Comprehensive test procedures
   - Multiple test scenarios
   - Expected outcomes
   - Error case testing
   - Cross-platform verification where relevant

5. **Expected Deliverables**
   - Clear list of outputs

6. **Success Criteria**
   - Checkbox list of requirements for completion

Note: Rollback procedures were NOT included per Q5 answer (Option C selected).

### Step 3: Incorporate Analysis Details

- Extracted specific code examples from P-034 analysis
- Included version management logic (major.minor.patch incrementing)
- Incorporated git tagging strategies
- Added release notes generation best practices
- Included GitHub Actions workflow patterns
- Referenced RDD workdir analysis approach

### Step 4: Ensure Sequential Dependencies

Each prompt builds on previous ones:
- Prompt 1 → Enables Prompt 2, 3, 4 (provides CI-compatible build.py)
- Prompt 2 → Used by Prompts 4, 5, 6 (version management utilities)
- Prompt 3 → Used by Prompts 4, 6 (release notes generation)
- Prompt 4 → Enhanced by Prompts 5, 6 (basic workflow)
- Prompt 5 → Enhanced by Prompt 6 (version control)
- Prompt 6 → Documented by Prompt 7 (validation)
- Prompt 7 → Documents all previous prompts

## Key Decisions

1. **7 Prompts Total**: Balanced between granularity and manageability
   - Could have been 3 large prompts (too complex)
   - Could have been 15 small prompts (too fragmented)
   - 7 provides good balance for sequential execution

2. **Phase Alignment**: Prompts 1-4 = Phase 1, Prompt 5 = Phase 2, Prompts 6-7 = Phase 3
   - Matches the analysis's phased rollout approach
   - Allows stopping after any phase if needed

3. **Testing Emphasis**: Each prompt has extensive testing section
   - Aligns with questionnaire answer Q3 (Option A)
   - Ensures quality at each step
   - Prevents issues from compounding

4. **No Rollback Procedures**: Per questionnaire Q5 (Option C)
   - Keeps prompts focused on forward progress
   - Validation and testing catch issues early
   - Manual rollback procedures are in documentation (Prompt 7)

5. **Detailed Instructions**: Per questionnaire Q2 (Option B)
   - Extracted specific commands and code from analysis
   - Self-contained execution without needing to re-read analysis
   - Clear step numbers and code blocks

## Alignment with Requirements

The created prompts align with RDD framework requirements:

- **UR-0002**: Prompts are persisted in Markdown format (release_prompts.md)
- **UR-0005**: Each prompt can be executed via the standard execute command
- **UR-0010**: Prompts reference scripts (build.py, version_manager.py, generate_release_notes.py) rather than implementing logic inline

## Alignment with Analysis

The prompts directly implement the P-034 analysis recommendations:

1. **Version Management**: Prompts 2 and 5 implement the version increment strategy from Section 2
2. **Git Tagging**: Prompt 4 implements tagging strategy from Section 4
3. **Release Notes**: Prompt 3 implements best practices from Section 5, including RDD workdir analysis
4. **GitHub Actions**: Prompts 4, 5, 6 implement workflow design from Section 6
5. **Phased Rollout**: Prompts follow Phase 1 → Phase 2 → Phase 3 approach from Section 7
6. **Documentation**: Prompt 7 implements documentation recommendations from Section 8

## Output

Created file: `.rdd-instance/workdir/P-035_Split on prompts the release analysis/release_prompts.md`

The file contains:
- 7 sequential prompts
- Detailed step-by-step instructions for each
- Comprehensive testing procedures
- Clear prerequisites and success criteria
- Summary of the overall structure

Total document length: ~1,100 lines of detailed implementation instructions

## No Requirements Updates Needed

Reviewed the requirements.md file and determined that no new requirements need to be added. The existing requirements already cover:
- Prompt persistence and management (UR-0002)
- Execute command pattern (UR-0005)
- Script-based actions (UR-0010)

The implementation creates prompts for a release automation system, which is a development process improvement rather than a framework feature that would require new requirements.

## Completion

Implementation is complete. The release_prompts.md file is ready for use by GitHub Copilot agents to implement the release automation system in sequence.
