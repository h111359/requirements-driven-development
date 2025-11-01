# Copilot Instructions

## Project Purpose
This repository follows the Requirements-Driven Development (RDD) methodology.  
Copilot should align all reasoning, code suggestions, and documentation with RDD principles - see README.md.

## Core Context Files
Before assisting with tasks, Copilot should understand and reference these files:

1. README.md — High-level overview, vision, and usage.
2. .rdd-docs/requirements.md — Functional and business requirements.
3. .rdd-docs/tech-spec.md — Technical architecture and implementation details.
4. .rdd-docs/folder-structure.md — Project organization and file structure.
5. .rdd-docs/data-model.md — Data structures and relationships.
6. .rdd-docs/version-control.md — Git branching strategies and commit conventions.

Copilot does not automatically read these files.  
Use commands like `@workspace summarize <path>` or `@workspace read <path>` in Copilot Chat when deeper context is needed.

## Behavioral Guidelines
1. Prioritize accuracy over speed. Base all reasoning on project documentation and RDD logic.  
2. If unsure about context, ask the user which document to consult.  
3. When writing code or documentation, ensure it aligns with the current RDD phase.  
4. Explain design choices using RDD vocabulary and reference the related section from .rdd-docs/* when applicable.
5. In case of unclarity or multiple choices - ask the user for guidance or chosing an option.


    