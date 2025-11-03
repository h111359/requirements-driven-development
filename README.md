# Requirements-Driven Development (RDD)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/h111359/requirements-driven-development)](https://github.com/h111359/requirements-driven-development/releases)
[![Build Status](https://img.shields.io/github/actions/workflow/status/h111359/requirements-driven-development/ci.yml?branch=main)](https://github.com/h111359/requirements-driven-development/actions)

A structured methodology and framework for software development with GitHub Copilot, emphasizing clear requirements documentation, systematic change management, and maintainable codebases.

## Overview

Requirements-Driven Development (RDD) is a methodology that combines traditional requirements engineering principles with modern AI-assisted development practices. It provides a systematic approach to manage requirements, technical specifications, and changes throughout the software development lifecycle.

## Features

- **Structured Documentation**: Organized approach to maintain requirements, technical specifications, and architectural decisions
- **Change Management**: Systematic tracking of changes from inception to archive
- **Clarity Checklist**: Standardized framework for requirement clarification and refinement
- **Version Control Integration**: Git-based workflow aligned with development processes
- **AI-Assisted Development**: Optimized for use with GitHub Copilot and similar AI tools

## Installation

```bash
<TO-BE-DEFINED>
```

## Usage

### Quick Start

```bash
<TO-BE-DEFINED>
```

### Project Structure

The RDD methodology organizes project documentation in the `.rdd-docs/` directory:

```
.rdd-docs/
├── requirements.md          # Project requirements
├── tech-spec.md            # Technical specifications
├── folder-structure.md     # Repository structure documentation
├── data-model.md           # Data model documentation
├── version-control.md      # Version control strategy
├── clarity-checklist.md     # Requirements clarification checklist
├── workspace/              # Current active work
└── archive/               # Historical changes
    ├── <change-name>/     # Archived change directories
    └── fixes/            # Bug fixes archive
```

### Core Workflow

1. **Document Requirements**: Define clear requirements in `requirements.md`
2. **Technical Design**: Document architecture and design in `tech-spec.md`
3. **Archive Completed Work**: Move completed changes to `archive/`
4. **Maintain Documentation**: Keep all documentation synchronized with code changes

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch following the naming convention: `feat/YYYYMMDD-HHMM-description`
3. Document your changes following the RDD methodology
4. Submit a pull request with clear description

For detailed contribution guidelines: <TO-BE-DEFINED>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Author**: Hristo M. Hristov
- **Email**: h111359@gmail.com
- **Project Link**: [https://github.com/h111359/requirements-driven-development](https://github.com/h111359/requirements-driven-development)

## Acknowledgments

Inspiration from Spec-Kit and OpenSpec projects.
