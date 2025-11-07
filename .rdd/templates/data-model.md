# Kolko Ni Struva Product Data Model

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
