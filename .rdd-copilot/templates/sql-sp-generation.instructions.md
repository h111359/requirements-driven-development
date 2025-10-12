---
description: 'Guidelines for generating SQL statements and stored procedures'
applyTo: '**/*.sql'
---

# SQL Development

## Database schema generation
- all table names should be in singular form
- all column names should be in singular form
- all tables should have a primary key column named `id`
- all tables should have a column named `created_at` to store the creation timestamp
- all tables should have a column named `updated_at` to store the last update timestamp

## Database schema design
- all tables should have a primary key constraint
- all foreign key constraints should have a name
- all foreign key constraints should be defined inline
- all foreign key constraints should have `ON DELETE CASCADE` option
- evaluate use of `ON UPDATE CASCADE` per criteria (default: omit unless justified; see Foreign Key Update/Delete Strategy)
- all foreign key constraints should reference the primary key of the parent table

## Foreign Key Update/Delete Strategy
**Default Policy:** Do NOT automatically apply `ON UPDATE CASCADE`. Prefer immutable surrogate primary keys (IDENTITY / UUID). Key updates should be exceptional.

### When to Use `ON UPDATE CASCADE`
- Natural key used as parent PK and legitimate business renames occur.
- Controlled maintenance operation requiring propagation of re-key changes.
- Consolidation / merge workflows (e.g., merging duplicate domain entities) where continuity must be preserved.

### When to Avoid `ON UPDATE CASCADE`
- Surrogate PKs (identity/UUID) that never change.
- High‑volume child tables where cascade could lock large ranges or escalate contention.
- Distributed / replicated environments where cascading updates may create replication lag.
- Audit / compliance domains needing explicit, traceable re-key scripts.

### Preferred Alternatives
- Use immutable surrogate PK; keep mutable business identifiers in separate columns.
- Perform explicit staged re-key scripts with audit logging.
- Use staging tables for consolidation before applying changes.

### Risk Checklist (all must be true before enabling)
1. Key updates are infrequent (<1% of rows monthly).
2. Estimated affected rows analyzed (EXPLAIN / plan review).
3. No deep cascade chain (>2 levels) or circular references.
4. Audit/compliance allows silent propagation.
5. Replication / CDC impact assessed and acceptable.

### Example Comparison
Bad (overuse):
```
FOREIGN KEY (customer_id) REFERENCES customers(id)
	ON UPDATE CASCADE ON DELETE CASCADE
```
Good (stable surrogate, only delete cascades):
```
FOREIGN KEY (customer_id) REFERENCES customers(id)
	ON DELETE CASCADE
```
Natural key scenario (justified update cascade):
```
FOREIGN KEY (country_code) REFERENCES countries(code)
	ON UPDATE CASCADE
```

## SQL Coding Style
- use uppercase for SQL keywords (SELECT, FROM, WHERE)
- use consistent indentation for nested queries and conditions
- include comments to explain complex logic
- break long queries into multiple lines for readability
- organize clauses consistently (SELECT, FROM, JOIN, WHERE, GROUP BY, HAVING, ORDER BY)

## SQL Query Structure
- use explicit column names in SELECT statements instead of SELECT *
- qualify column names with table name or alias when using multiple tables
- limit the use of subqueries when joins can be used instead
- include LIMIT/TOP clauses to restrict result sets
- use appropriate indexing for frequently queried columns
- avoid using functions on indexed columns in WHERE clauses

## Stored Procedure Naming Conventions
- prefix stored procedure names with 'usp_'
- use PascalCase for stored procedure names
- use descriptive names that indicate purpose (e.g., usp_GetCustomerOrders)
- include plural noun when returning multiple records (e.g., usp_GetProducts)
- include singular noun when returning single record (e.g., usp_GetProduct)

## Parameter Handling
- prefix parameters with '@'
- use camelCase for parameter names
- provide default values for optional parameters
- validate parameter values before use
- document parameters with comments
- arrange parameters consistently (required first, optional later)


## Stored Procedure Structure
- include header comment block with description, parameters, and return values
- return standardized error codes/messages
- return result sets with consistent column order
- use OUTPUT parameters for returning status information
- prefix temporary tables with 'tmp_'


## SQL Security Best Practices
- parameterize all queries to prevent SQL injection
- use prepared statements when executing dynamic SQL
- avoid embedding credentials in SQL scripts
- implement proper error handling without exposing system details
- avoid using dynamic SQL within stored procedures

## Transaction Management
- explicitly begin and commit transactions
- use appropriate isolation levels based on requirements
- avoid long-running transactions that lock tables
- use batch processing for large data operations
- include SET NOCOUNT ON for stored procedures that modify data
