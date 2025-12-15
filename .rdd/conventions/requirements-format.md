# Requirements Format Guide

This document describes the format for writing requirements in the RDD framework.



## File Structure

Requirements are organized into four main sections:

## Product Name
## Product Overview
## Definitions, Acronyms, and Abbreviations
## Design principles
## General Functionalities
## Functional Requirements
## Non-Functional Requirements
## Technical Requirements

## Requirement Format

Each requirement follows this format:

```markdown
- [PREFIX-ID] Detailed description of the requirement
```

### Components:

- **Prefix**: Section identifier (DP, GF, FR, NFR, or TR)
- **ID**: Sequential number (001, 002, 003, etc.)
- **Description**: Complete requirement statement using "shall" language


## Section Categories

### Design principles (DP)
High-level principles for design of the system.

**Examples:**
- Modularity and separation of concerns
- Security by default and least privilege
- Scalability and performance-minded design
- Observability and operational transparency
- Resilience and fault tolerance
- Simplicity and maintainability
- Interoperability and adherence to standards
- Privacy and data protection by design
- Accessibility and inclusive design

```markdown
- [DP-001] The system shall follow a modular architecture with clear separation of concerns and well-defined interfaces
- [DP-002] The system shall adopt secure-by-default principles, enforcing least privilege and safe defaults
- [DP-003] The system shall be designed to scale horizontally and vertically without requiring major architectural changes
- [DP-004] The system shall be observable, providing structured logs, metrics, and distributed traces for debugging and monitoring
```

### General Functionalities (GF)
High-level capabilities and features of the system.

**Examples:**
- User management
- Data import/export
- Reporting capabilities
- Integration features

```markdown
- [GF-001] The system shall provide OAuth2-based user authentication
- [GF-002] The framework shall store all data in a local database
```

### Functional Requirements (FR)
Specific behaviors and functions the system must perform.

**Examples:**
- Input validation rules
- Calculation algorithms
- Workflow steps
- Data transformations

```markdown
- [FR-001] The system shall allow users to upload files up to 100MB
- [FR-002] The system shall export data in CSV format with UTF-8 encoding
```

### Non-Functional Requirements (NFR)
Quality attributes and constraints.

**Examples:**
- Performance (response time, throughput)
- Reliability (uptime, error rates)
- Usability (accessibility, user experience)
- Maintainability (code quality, documentation)

```markdown
- [NFR-001] The system shall respond to user requests within 2 seconds
- [NFR-002] The framework shall support up to 10,000 concurrent users
```

### Technical Requirements (TR)
Technology stack and implementation specifications.

**Examples:**
- Programming languages and versions
- Frameworks and libraries
- Database systems
- API specifications
- File formats and protocols

```markdown
- [TR-001] The system shall use Python 3.11 or higher
- [TR-002] The framework shall use PostgreSQL 15+ as the database
```



## Writing Guidelines

### 1. Use "Shall" Language

✅ **Good:** "The system shall validate user input"
❌ **Bad:** "The system should validate" or "The system validates"

### 2. Be Specific

✅ **Good:** "The system shall support CSV, JSON, and XML export formats"
❌ **Bad:** "The system shall support various formats"

### 3. One Requirement Per Line

✅ **Good:** 
- `[FR-001] Max 100MB`
- `[FR-002] Accept PDF, DOC, DOCX only`

❌ **Bad:**
- `[FR-001] Max 100MB, PDF/DOC/DOCX only`

### 4. Avoid Implementation Details in FR/NFR

Implementation belongs in Technical Requirements (TR).

✅ **Good:**
- `[FR-001] Export data in structured format`
- `[TR-001] Use JSON serialization with UTF-8 encoding`

❌ **Bad:**
- `[FR-001] Export data using JSON serialization`



## Best Practices

1. **Start broad, get specific**: GF → FR → NFR → TR
3. **Write complete sentences**: Full requirement statements
4. **Use consistent terminology**: Same terms throughout
5. **Avoid ambiguity**: Be precise and measurable
6. **Review for completeness**: Each requirement should be independently testable



## Modification Markers

In `requirements.md`, use these prefixes:

### [DELETED]
Remove existing requirement (must include existing ID). Example:
```markdown
- [FR-012] [DELETED] 
```
