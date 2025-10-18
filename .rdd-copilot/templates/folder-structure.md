# File and Folder Structure

> This template provides a standard project structure for web applications.

## Project Root
- `.github/`: GitHub-specific files (workflows, templates, etc.)
- `.rdd-docs/`: All project documentation
- `.vscode/` : Specific setpu for Visual Studio Code



## .rdd-docs/
Project documentation and planning
- `requirements.md`: Requirements specification file which represents the current state of the product
- `technical-specification.md`: Technical information like architecture, design, setup, etc.
- `folder-structure.md`: The current document describing the files and folders organization
- `change-requests` : Folder with individual change requests documentation (*.cr.md files)
- `templates/` : Documentation templates for requirements, technical specification, CRs, etc. (may be moved here from `.rdd-copilot/templates` during setup)
- For every CR, a dedicated log file (`cr-<cr id>-<cr-name>-log.md`) is created in the same folder as the CR file to record all rdd-copilot.* prompts and replies related to that CR.


## Customization
- Modify this structure based on your project's specific needs
- Add additional directories for frameworks, testing, build tools, etc.
- Maintain clear separation between source code, documentation, and configuration
