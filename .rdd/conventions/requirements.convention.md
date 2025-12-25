# Requirements Format Guide

This document describes the format for writing requirements in the RDD framework.


## File Structure

Requirements are organized into the following sections:

* Product Name - the official name of the product. The section should start with line - exactly `## Product Name`

* Product Overview - short description of the product. The section should start with line - exactly `## Product Overview`

* Definitions - labels and explanations of concepts used in this and other specifications. The section should start with line - exactly `## Definitions`

* User Requirements - statements from user point of view defining what is needed. No limitations how it should be achieved or technical terminology here. The section should start with line - exactly `## User Requirements`

* Technical Requirements - technical specifications, definitions how to be realized a part of the product. The section should start with line - exactly `## Technical Requirements`

Keep at least 3 empty lines between sections as separator. Tools MUST parse by headings (## ...) and requirement line pattern, not by blank-line counting; the 3-blank-line rule is style-only.


## Requirement Format

Each requirement follows this format:

```markdown
- [<Prefix>-<ID>] <Description>
```

### Components:

- **Prefix**: Section identifier (UR, TR)
- **ID**: The timestamp of creation of the requirement entry in format YYYYMMDD-HHmm whre YYYY is the year, MM - month, DD - day, HH - 24 format hour, mm - minutes. Example 20251224-0913
- **Description**: Detailed description of the requirement. Complete requirement statement using "shall" language


## Section Categories

### User Requirements (UR)
User perspective requirements. High-level capabilities and features of the system as well as specific behaviors and functions the system must perform. No technical constraints. No technical language.

**Examples:**

```markdown
- [UR-20251224-0901] The system shall allow users to upload files up to 100MB
- [UR-20251224-0902] The system shall export data in CSV format with UTF-8 encoding
```


### Technical Requirements (TR)
High-level principles for design of the system as well as technology stack and implementation specifications.

**Examples:**

```markdown
- [TR-20251224-0901] The system shall use Python 3.11 or higher
- [TR-20251224-0902] The framework shall use PostgreSQL 15+ as the database
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
- `[UR-20251224-0901] Max 100MB`
- `[UR-20251224-0902] Accept PDF, DOC, DOCX only`

❌ **Bad:**
- `[UR-20251224-0901] Max 100MB, PDF/DOC/DOCX only`

### 4. Avoid Implementation Details in UR

Implementation belongs in Technical Requirements (TR).

✅ **Good:**
- `[UR-20251224-0901] Export data in structured format`
- `[TR-20251224-0901] Use JSON serialization with UTF-8 encoding`

❌ **Bad:**
- `[UR-20251224-0901] Export data using JSON serialization`



## Best Practices

1. **Write complete sentences**: Full requirement statements
2. **Use definition labels**: Same terms throughout
3. **Avoid ambiguity**: Be precise and measurable
4. **Review for completeness**: Each requirement should be independently testable
5. **Requirement 


## Modification Markers

In `requirements.md`, use these prefixes:

### [DELETED]
Remove existing requirement (must include existing ID). Example:
```markdown
- [UR-20251224-0912] [DELETED] 
```
