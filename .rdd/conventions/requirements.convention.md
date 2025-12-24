# Requirements Format Guide

This document describes the format for writing requirements in the RDD framework.


## File Structure

Requirements are organized into the following sections:

* Product Name - the official name of the product

* Product Overview - short description of the product

* Definitions, Acronyms, and Abbreviations - all important and used further terms, acronyms, etc.

* User Requirements

* Technical Requirements



## Requirement Format

Each requirement follows this format:

```markdown
- [<Prefix>-<ID>] <Description>
```

### Components:

- **Prefix**: Section identifier (UR, TR)
- **ID**: Sequential number (001, 002, 003, etc.)
- **Description**: Detailed description of the requirement. Complete requirement statement using "shall" language


## Section Categories

### User Requirements (UR)
User perspective requirements. High-level capabilities and features of the system as well as specific behaviors and functions the system must perform. No technical constraints. No technical language.

**Examples:**

```markdown
- [UR-001] The system shall allow users to upload files up to 100MB
- [UR-002] The system shall export data in CSV format with UTF-8 encoding
```


### Technical Requirements (TR)
High-level principles for design of the system as well as technology stack and implementation specifications.

**Examples:**

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
- `[UR-001] Max 100MB`
- `[UR-002] Accept PDF, DOC, DOCX only`

❌ **Bad:**
- `[UR-001] Max 100MB, PDF/DOC/DOCX only`

### 4. Avoid Implementation Details in FR/NFR

Implementation belongs in Technical Requirements (TR).

✅ **Good:**
- `[UR-001] Export data in structured format`
- `[TR-001] Use JSON serialization with UTF-8 encoding`

❌ **Bad:**
- `[UR-001] Export data using JSON serialization`



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
- [UR-012] [DELETED] 
```
