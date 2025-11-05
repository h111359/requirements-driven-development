# Requirements Format Guide

This document describes the format for writing requirements in the RDD framework.

## File Structure

Requirements are organized into four main sections:

1. **General Functionalities** (GF)
2. **Functional Requirements** (FR)
3. **Non-Functional Requirements** (NFR)
4. **Technical Requirements** (TR)

## Requirement Format

Each requirement follows this format:

```markdown
- **[PREFIX-ID] Short Title**: Detailed description of the requirement
```

### Components:

- **Prefix**: Section identifier (GF, FR, NFR, or TR)
- **ID**: Sequential number (01, 02, 03, etc.)
- **Short Title**: Brief, descriptive name (2-5 words)
- **Description**: Complete requirement statement using "shall" language

### Examples:

```markdown
# General Functionalities

- **[GF-01] User Authentication**: The system shall provide OAuth2-based user authentication
- **[GF-02] Data Persistence**: The framework shall store all data in a local database

# Functional Requirements

- **[FR-01] File Upload**: The system shall allow users to upload files up to 100MB
- **[FR-02] Export to CSV**: The system shall export data in CSV format with UTF-8 encoding

# Non-Functional Requirements

- **[NFR-01] Response Time**: The system shall respond to user requests within 2 seconds
- **[NFR-02] Scalability**: The framework shall support up to 10,000 concurrent users

# Technical Requirements

- **[TR-01] Python Version**: The system shall use Python 3.11 or higher
- **[TR-02] Database Engine**: The framework shall use PostgreSQL 15+ as the database
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
- `[FR-01] File Size Limit: Max 100MB`
- `[FR-02] File Type Filter: Accept PDF, DOC, DOCX only`

❌ **Bad:**
- `[FR-01] File Upload: Max 100MB, PDF/DOC/DOCX only`

### 4. Avoid Implementation Details in FR/NFR

Implementation belongs in Technical Requirements (TR).

✅ **Good:**
- `[FR-01] Data Export: Export data in structured format`
- `[TR-01] Export Format: Use JSON serialization with UTF-8 encoding`

❌ **Bad:**
- `[FR-01] Data Export: Export data using JSON serialization`

## ID Assignment

### During Development (Workspace)

When adding new requirements in `requirements-changes.md`:

```markdown
- **[ADDED] User Authentication**: System shall require OAuth2 login
```

**Do NOT assign IDs manually** - they will be auto-assigned during wrap-up.

### During Wrap-Up

The wrap-up script automatically assigns IDs based on:
- The highest existing ID in each section
- Sequential numbering from that point

Example:
- Existing: GF-01, GF-02, GF-05 (GF-03, GF-04 removed)
- Next assigned: GF-06, GF-07, GF-08...

## Section Categories

### General Functionalities (GF)
High-level capabilities and features of the system.

**Examples:**
- User management
- Data import/export
- Reporting capabilities
- Integration features

### Functional Requirements (FR)
Specific behaviors and functions the system must perform.

**Examples:**
- Input validation rules
- Calculation algorithms
- Workflow steps
- Data transformations

### Non-Functional Requirements (NFR)
Quality attributes and constraints.

**Examples:**
- Performance (response time, throughput)
- Reliability (uptime, error rates)
- Usability (accessibility, user experience)
- Maintainability (code quality, documentation)

### Technical Requirements (TR)
Technology stack and implementation specifications.

**Examples:**
- Programming languages and versions
- Frameworks and libraries
- Database systems
- API specifications
- File formats and protocols

## Best Practices

1. **Start broad, get specific**: GF → FR → NFR → TR
2. **Keep titles concise**: 2-5 words maximum
3. **Write complete sentences**: Full requirement statements
4. **Use consistent terminology**: Same terms throughout
5. **Avoid ambiguity**: Be precise and measurable
6. **Review for completeness**: Each requirement should be independently testable

## Modification Markers

In `requirements-changes.md`, use these prefixes:

### [ADDED]
New requirement not in current requirements.md
```markdown
- **[ADDED] Feature Name**: Description
```

### [MODIFIED]
Change to existing requirement (must include existing ID)
```markdown
- **[MODIFIED] [FR-05] Feature Name**: New description
```

### [DELETED]
Remove existing requirement (must include existing ID and reason)
```markdown
- **[DELETED] [FR-12] Legacy Feature**: No longer needed after v2.0 migration
```

---

**Version:** 1.0  
**Last Updated:** 2025-10-31
