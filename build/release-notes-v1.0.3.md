# Release Notes - Version 1.0.3

**Release Date**: November 8, 2025

## Overview

This release introduces significant improvements to the user interface and build system, making the RDD framework more reliable and user-friendly. Key enhancements include a simplified numeric menu system and interactive version management during builds.

## Key Changes

### 1. Simplified Numeric Menu Navigation
- **Replaced** complex arrow-based menu navigation with simple numeric selection
- **Improved** reliability and consistency across all terminal types and platforms
- **Enhanced** user experience with clear numbered options
- Users now select options by entering numbers instead of navigating with arrow keys

### 2. Interactive Build Version Management
- **Added** interactive version increment prompt during build process
- **Automated** version updates in `.rdd-docs/config.json` when incrementing
- Users can now choose to:
  - Keep the current version and rebuild
  - Increment the patch version (last digit) automatically
- Version is now persistently stored and managed in config.json

### 3. Local-Only Mode Support
- **Introduced** `localOnly` configuration field in config.json
- **Enabled** repositories to operate without GitHub remote
- **Automated** remote operation skipping when local-only mode is active
- Users are prompted during installation to choose between GitHub remote mode and local-only mode

## Technical Improvements

### Menu System
- Simplified interaction model reduces complexity and potential errors
- Consistent behavior across Windows, Linux, and macOS
- Color-coded output for improved readability

### Build System
- Single source of truth for version in `.rdd-docs/config.json`
- Automatic config.json updates when version is incremented
- Clear user prompts with validation

### Configuration Management
- Added `localOnly` boolean field to config.json schema
- Enhanced installation process to configure local-only mode
- Remote operations intelligently skipped based on configuration

## Bug Fixes

- Fixed menu navigation issues that prevented proper option selection
- Resolved state corruption when returning to menu after command execution
- Improved terminal compatibility across different platforms

## Documentation Updates

- Updated requirements.md with new functional requirements (FR-75, FR-76, FR-77)
- Enhanced tech-spec.md with detailed menu system and build process documentation
- Documented localOnly field in data-model.md

## Migration Notes

No migration steps required. Existing installations will work seamlessly with the new release.

## Known Issues

None at this time.

## Next Steps

After installation:
1. Test the new numeric menu navigation: `python .rdd/scripts/rdd.py`
2. Try the interactive build process: `python scripts/build.py`
3. Configure local-only mode if needed: `python .rdd/scripts/rdd.py config set localOnly true`

---

For detailed installation instructions, see README.md in the release archive.
