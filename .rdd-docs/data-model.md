# RDD Framework Data Model

## Configuration Files

### config.json

#### Description:
Framework-wide configuration file storing repository and workflow settings. Located in `.rdd-docs/config.json` and version-controlled with the repository.

#### Attributes:

  - version: 
    - Description: RDD framework version using semantic versioning
    - Mandatory: Yes
    - Data Type: String
    - Format: Semantic versioning (MAJOR.MINOR.PATCH)
    - Example: "1.0.0"

  - defaultBranch: 
    - Description: Name of the repository's default branch for change management
    - Mandatory: Yes
    - Data Type: String
    - Format: Valid git branch name
    - Data validation rules:
       - Must be a valid git branch name
       - Should exist in the repository
    - Example: "main", "dev", "master", "develop"

  - created:
    - Description: ISO 8601 timestamp of when the configuration was first created
    - Mandatory: Yes
    - Data Type: String
    - Format: ISO 8601 datetime with timezone (UTC)
    - Example: "2025-11-06T08:00:00Z"

  - lastModified:
    - Description: ISO 8601 timestamp of when the configuration was last updated
    - Mandatory: Yes
    - Data Type: String
    - Format: ISO 8601 datetime with timezone (UTC)
    - Example: "2025-11-06T10:30:00Z"

  - localOnly:
    - Description: Flag indicating whether the repository operates in local-only mode without GitHub remote
    - Mandatory: Yes
    - Data Type: Boolean
    - Format: true or false
    - Data validation rules:
       - Must be a boolean value
       - When true, all remote operations (fetch, push, pull) are skipped
       - When false (default), normal GitHub remote operations are performed
    - Example: false, true

#### Constraints

  - Primary-Key: N/A (single instance file)
  - Unique-Key: N/A

#### Example File:
```json
{
  "version": "1.0.0",
  "defaultBranch": "dev",
  "localOnly": false,
  "created": "2025-11-06T08:00:00Z",
  "lastModified": "2025-11-06T10:30:00Z"
}
```

#### Location:
- **File path**: `.rdd-docs/config.json`
- **Template**: `.rdd/templates/config.json`
- **Access functions**: 
  - `get_rdd_config(key, default)` - Read value
  - `set_rdd_config(key, value)` - Write value
  - `get_rdd_config_path()` - Get file path

#### Usage:
- Created during workspace initialization via interactive branch selection
- Updated via `python .rdd/scripts/rdd.py config set <key> <value>`
- Read by `get_default_branch()` function for branch management
- Displayed via `python .rdd/scripts/rdd.py config show`

## Entities

### <ENTITY-NAME>

#### Description:

<ENTITY-DESCRIPTION>

#### Attributes:

  - <ATTRIBUTE-NAME>: 
    - Description: <ATTRIBUTE-DESCRIPTION>
    - Mandatory: [Yes|No]    
    - Data Type: <DATA-TYPE>
    - Format: <DATA-FORMAT>
    - Data validation rules:
       - should contain `@`
    - Example: <DATA-EXAMPLE>

  - <ATTRIBUTE-NAME>: <ATTRIBUTE-DESCRIPTION>  

#### Constraints

  - Primary-Key: 
      - <ATTRIBUTE-NAME>
      - <ATTRIBUTE-NAME>
      - <ATTRIBUTE-NAME>

  - Unique-Key
      - <ATTRIBUTE-NAME>
      - <ATTRIBUTE-NAME>
      - <ATTRIBUTE-NAME>

## Relationships

### REL-<ENTITY-NAME>-<ENTITY-NAME>

- Cardinality: [1:1|M:1|1:M|M:M]
- Statement: [e.g "Each `Team` could have one or more `Employee`" or "Each `Employee` must belong to one and only one `Location`" ]
- Left Entity Attributes: 
      - <ATTRIBUTE-NAME>
      - <ATTRIBUTE-NAME>
- Right Entity Attributes: 
      - <ATTRIBUTE-NAME>
      - <ATTRIBUTE-NAME>


## Validation Rules

Examples:
- <ENTITY-NAME>: If data for a day is missing, script skips and logs a warning
- If entity reaches 10M rows - log a warning


## Physical Implementation

Description how the entities are realised - as tables in a database, files or other. Also here should be provided paths, connection strings or other which identifies the place of entity residence.

### Folder Structure Reference

## Data File Formats

### File <FILE-NAME>
- Location: `data/raw/`
- Format: [e.g. CSV (comma-separated values, UTF-8, quoted fields)]
- Header Row: [Yes|no]
- Fields:
    - <FIELD-NAME>
    - <FIELD-NAME>

- Example header:
```
"Населено място","Търговски обект","Наименование на продукта","Код на продукта","Категория","Цена на дребно","Цена в промоция"
```

- Example row:
```
"68134","МАГАЗИН МЛАДОСТ - СОФИЯ, ЖК МЛАДОСТ 2, БУЛ. АЛЕКСАНДЪР МАЛИНОВ 75","КРАВЕ МАСЛО 125 ГР ДИМИТЪР МАДЖАРОВ","040001","11","4.98",""
```

## Database Tables

### Table <TABLE-NAME>
- Schema: `<SCHEMA-NAME>`
- Storage Engine: [e.g. Azure SQL Database | PostgreSQL | Snowflake]
- Description: <TABLE-DESCRIPTION>
- Primary Key Columns:
  - <COLUMN-NAME>
  - <COLUMN-NAME>
- Foreign Keys:
  - `<FK-NAME>` → `<TARGET-SCHEMA>.<TARGET-TABLE>(<TARGET-COLUMN>)`
- Columns:
  - <COLUMN-NAME> (`<DATA-TYPE>`): <COLUMN-DESCRIPTION>
  - <COLUMN-NAME> (`<DATA-TYPE>`): <COLUMN-DESCRIPTION>
- Indexes:
  - `<INDEX-NAME>`: <COLUMN-LIST> [clustered|nonclustered|btree]
- Partitioning Strategy: [None | <COLUMN-NAME> | <RANGE>]
- Retention Policy: [e.g. Keep 36 months | Purge daily snapshots after 14 days]
- Example DDL:
```sql
CREATE TABLE <SCHEMA-NAME>.<TABLE-NAME> (
  <COLUMN-NAME> <DATA-TYPE> NOT NULL,
  <COLUMN-NAME> <DATA-TYPE>,
  CONSTRAINT <PK-NAME> PRIMARY KEY (<COLUMN-NAME>)
);
```
- Example row:
```
<VALUE-1>|<VALUE-2>|<VALUE-3>
```
