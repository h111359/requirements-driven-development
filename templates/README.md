# RDD Framework v{{VERSION}}

Requirements-Driven Development (RDD) is a structured workflow automation framework that guides developers through requirement clarification, implementation, and documentation processes.

## System Requirements

- **Python 3.7+** 
- **Git 2.23+**
- **VS Code**
- **GitHub Copilot**


## Installation

1. **Download the latest release** from [GitHub Releases](https://github.com/h111359/requirements-driven-development/releases)
   - Download `rdd-v{version}.zip`
   - Verify with `rdd-v{version}.zip.sha256` (optional)

2. **Extract the archive**
   Extract the archive in a folder

3. **Run the install scripts**
   
   - For Linux - run install.sh
   - For Windows - run install.bat

4. **Choose target folder**
   Follow the instructions to install RDD in the desired destination

The installer automatically:
- Verifies Python 3.7+ and Git are installed
- Checks the target is a Git repository
- Detects and warns about existing RDD installations
- Copies framework files (.rdd/, .github/prompts/, .rdd-docs/ templates)
- Merges VS Code settings intelligently
- Updates .gitignore
- Verifies successful installation


## Documentation

For more information, visit: https://github.com/h111359/requirements-driven-development

## License

See LICENSE file for details.
