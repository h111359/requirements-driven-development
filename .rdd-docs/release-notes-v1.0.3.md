git pull origin main
# RDD Framework v1.0.3 - Summary

**Release Date:** November 8, 2025

Version 1.0.3 simplifies the RDD framework with a new 4-step workflow: create iteration, update from default, complete iteration, and delete merged branches. The menu system is now numeric (no arrow keys/curses), making it more reliable and user-friendly.

Local-only mode is supported via the `localOnly` config option, allowing use without a GitHub remote. All remote operations are skipped in this mode. Function names now use "default branch" terminology for flexibility.

The build script prompts for version management and updates config.json automatically. Unused logging and menu code have been removed for clarity and maintainability.

All tests have been updated for the new workflow, with 61 tests and ~87% coverage. CI/CD now passes on GitHub Actions. Safety checks prevent common mistakes (e.g., committing to default branch, mixing work).

Migration: Existing users should add `localOnly` to config.json and learn the new menu. CLI commands remain available. No changes needed for existing branches or archives.

Key files changed: rdd.py, rdd_utils.py, build.py, install.py, test files. Performance is unchanged. No known issues.

For questions or issues, see GitHub Issues or `.rdd-docs/` documentation.

**Thank you for using RDD Framework v1.0.3!**
