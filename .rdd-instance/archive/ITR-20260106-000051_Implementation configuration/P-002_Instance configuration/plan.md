# Implementation Plan for Instance Configuration

## Overview

This plan implements a new instance-level configuration system by creating `.rdd-instance/config/instance-config.json` to store the git-enabled setting, replacing the current location in `work-iteration-registry.json`. Based on questionnaire answers, this implementation will:
- Remove git-enabled completely from work-iteration-registry.json (Q1-A)
- Require re-seeding for existing instances without migration (Q2-C)
- Support only git-enabled configuration initially (Q3-A)
- Make the config folder mandatory in manifest validation (Q4-A)

## Implementation Steps

### Step 1: Create instance-config.json Schema and Default File

Create the new configuration file structure in `.rdd-instance/config/instance-config.json` with the following content:

```json
{
  "git-enabled": false
}
```

This will be the single source of truth for the git-enabled setting going forward.

### Step 2: Update rdd-instance_seed.py Script

Modify `.rdd/src/actions/rdd-instance_seed.py` to create the `.rdd-instance/config` folder and `instance-config.json` file during the seeding process. The script should:
- Create the `.rdd-instance/config` directory
- Write the default instance-config.json file with `{"git-enabled": false}`
- Ensure proper error handling if the folder/file cannot be created

### Step 3: Update Manifest to Require Config Folder

Modify `.rdd/config/manifest.json` to include the new mandatory items:
- Add `.rdd-instance/config/` folder as a mandatory directory
- Add `.rdd-instance/config/instance-config.json` as a mandatory file

This will ensure validation checks enforce the presence of the configuration file.

### Step 4: Update prompt_complete.py to Use New Configuration

Modify `.rdd/src/actions/prompt_complete.py` to:
- Remove reading git-enabled from `work-iteration-registry.json`
- Add logic to read git-enabled from `.rdd-instance/config/instance-config.json`
- Ensure proper error handling if the config file is missing or malformed
- Use the git-enabled value to determine whether to perform git commit operations

### Step 5: Update Web UI Workdir Page to Use New Configuration

Modify the Workdir page in the Web UI (likely in `.rdd/web-ui/` files) to:
- Remove any references to git-enabled in work-iteration-registry.json
- Read git-enabled from `.rdd-instance/config/instance-config.json` instead
- Display the configuration value appropriately in the UI
- Provide clear error messages if the config file is missing

### Step 6: Remove git-enabled from work-iteration-registry.json Schema

Since the questionnaire answer Q1-A specifies complete removal:
- Update the schema/structure expectations for work-iteration-registry.json to no longer include git-enabled
- Remove any initialization of git-enabled in scripts that create or modify the registry
- Ensure workdir_new_setup.py and similar scripts don't add this field

### Step 7: Update Validation and Error Messages

Add validation logic to detect missing `.rdd-instance/config/` folder or `instance-config.json` file:
- In manifest validation, provide clear error messages directing users to re-seed
- In Web UI startup/API endpoints, check for config existence and fail gracefully with instructions
- Error messages should state: "Instance configuration not found. Please re-run the seed script to create .rdd-instance/config/instance-config.json"

### Step 8: Update Files-and-Folders Specification

Add documentation for the new structure in `.rdd-instance/specifications/files-and-folders.md`:
- Document the `.rdd-instance/config/` folder
- Document the `instance-config.json` file with its purpose and schema
- Explain the git-enabled configuration key

### Step 9: Update Requirements (if needed)

Check if any new requirements need to be added to capture this architectural change:
- If needed, create a new technical requirement using: `python .rdd/src/actions/requirement_tr_create.py text="The framework shall store instance-level configuration in .rdd-instance/config/instance-config.json file"`
- If needed, create requirement for git-enabled: `python .rdd/src/actions/requirement_tr_create.py text="The framework shall read the git-enabled setting from .rdd-instance/config/instance-config.json to determine whether to perform git operations during prompt completion"`

These requirements would formalize the new configuration architecture.

### Step 10: Identify All Files That Currently Reference git-enabled in Registry

Before implementation, search the codebase for all references to git-enabled in work-iteration-registry.json:
- Search in Python scripts (`.rdd/src/actions/*.py`)
- Search in Web UI JavaScript files (`.rdd/web-ui/*.js` or similar)
- Search in any documentation files

This ensures no references are missed during the migration.

### Step 11: Update Each Identified File

For each file found in Step 10:
- Update to read from `.rdd-instance/config/instance-config.json` instead
- Remove imports or logic specific to reading from registry
- Add appropriate error handling for missing config file

### Step 12: Testing and Verification

After implementation:
- Test seed script creates config folder and file correctly
- Test manifest validation catches missing config
- Test prompt completion reads git-enabled from new location correctly
- Test Web UI displays and uses git-enabled from new location
- Verify error messages are clear and actionable

## Requirements Updates

The following requirements should be created during implementation (Step 9):

**New Technical Requirement TR-1:**
```
python .rdd/src/actions/requirement_tr_create.py text="The framework shall store instance-level configuration in .rdd-instance/config/instance-config.json file containing a git-enabled boolean flag"
```

**New Technical Requirement TR-2:**
```
python .rdd/src/actions/requirement_tr_create.py text="The framework shall read the git-enabled setting from .rdd-instance/config/instance-config.json to determine whether to perform git operations during prompt completion"
```

**New Technical Requirement TR-3:**
```
python .rdd/src/actions/requirement_tr_create.py text="The framework shall validate the presence of .rdd-instance/config/ folder and instance-config.json file during manifest validation and provide clear error messages directing users to re-seed if missing"
```

## Files to Be Modified

1. `.rdd/src/actions/rdd-instance_seed.py` - Add config folder and file creation
2. `.rdd/config/manifest.json` - Add config folder and file to mandatory items
3. `.rdd/src/actions/prompt_complete.py` - Read from new config location
4. `.rdd-instance/specifications/files-and-folders.md` - Document new structure
5. Web UI files (to be identified in Step 10) - Update to use new config
6. `.rdd/src/actions/workdir_new_setup.py` (if it exists) - Remove git-enabled initialization
7. Any other Python scripts identified in Step 10

## Success Criteria

- New instances created via seed script have `.rdd-instance/config/instance-config.json`
- Manifest validation enforces presence of config folder and file
- Prompt completion correctly reads git-enabled from new location
- Web UI Workdir page displays git configuration from new location
- No remaining references to git-enabled in work-iteration-registry.json
- Clear error messages guide users when config is missing
- Files and folders documentation is updated
- New technical requirements are added to requirements.md
