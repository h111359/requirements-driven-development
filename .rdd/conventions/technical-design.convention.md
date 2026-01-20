# Technical Design Convention

## Purpose

The Technical Design artifact stores structured architectural decisions for RDD framework projects. It is **optional** but **binding** when present.

**Key Principles**:
- Technical Design captures architectural choices, technology stack, deployment strategy, security, and operational decisions
- Only **explicitly answered** questions are stored (sparse storage model)
- **Python scripts enforce all modifications** - never edit the file directly
- Technical Design is optional: RDD execution flows continue if the file is empty or missing
- When present, RDD execution modes (clarify/analyze/plan/implement/modify) must comply with recorded decisions

## File Locations

### Schema (Framework-level)
- **Path**: `.rdd/config/technical-design-schema.json`
- **Description**: Machine-readable schema defining all available questions, categories, and conditional visibility rules
- **Format**: JSON with hierarchical structure (categories → questions)
- **Versioning**: No schema versioning; single authoritative schema

### Answers (Instance-level)
- **Path**: `.rdd-instance/specifications/technical-design.json`
- **Description**: Storage for answered questions only
- **Format**: JSON object keyed by `questionId`
- **Encoding**: UTF-8

## Schema Structure

The schema follows a **flattened model** where questions are direct children of categories:

```json
{
  "title": "Technical Design Questionnaire",
  "description": "Comprehensive architectural decision questionnaire",
  "categories": [
    {
      "id": "CategoryId",
      "label": "Category Display Name",
      "description": "Optional category description",
      "questions": [
        {
          "id": "QuestionId",
          "label": "Question text",
          "type": "radio|multiselect|text",
          "help": "Optional helper text",
          "options": [...],
          "placeholder": "...",
          "visibleWhen": [...],
          "allowOther": true
        }
      ]
    }
  ]
}
```

### Question Types

| Type | Description | Value Format | UI Element |
|------|-------------|--------------|------------|
| `radio` | Single choice from predefined options | String | Radio buttons |
| `multiselect` | Multiple choices from predefined options | Array of strings | Checkboxes |
| `text` | Free-form text input | String | Text input |

### Question Fields

- **id** (required): Unique stable identifier for the question (e.g., `"ProjectScale_OverallScaleCategory"`)
- **label** (required): Question text displayed to user
- **type** (required): Question type (radio, multiselect, text)
- **help** (optional): Helper text or example shown to user
- **options** (conditional): Array of option objects for radio/multiselect questions
  ```json
  "options": [
    {"id": "option-id", "label": "Option Label"}
  ]
  ```
- **placeholder** (optional): Placeholder text for text inputs
- **visibleWhen** (optional): Conditional visibility rules (see below)
- **allowOther** (optional): Boolean flag allowing custom text answer in addition to predefined options

### Conditional Visibility

Questions can be conditionally shown/hidden based on answers to other questions using **simple rule objects**:

```json
"visibleWhen": [
  {
    "questionId": "ProjectScale_OverallScaleCategory",
    "equals": "Enterprise-wide platform"
  }
]
```

**Evaluation Logic**:
- All rules in `visibleWhen` array must be satisfied (AND logic)
- Rule matches when the referenced question's current answer value equals the specified value
- For multiselect questions, rule matches if the specified value is present in the answer array
- Questions without `visibleWhen` are always visible

Multiple condition objects in visibleWhen array → AND logic

- ALL conditions must be satisfied for the question to be visible
  - Example: If visibleWhen has 2 rules, BOTH must be true

- Multiple values in the equals array → OR logic, The answer must match ANY ONE of the values. 
  - Example: "equals": ["Value A", "Value B"] means answer = "Value A" OR "Value B"

## Answers Storage Format

The answers file stores **only explicitly answered questions** as a JSON object keyed by `questionId`:

```json
{
  "ProjectScale_OverallScaleCategory": {
    "questionId": "ProjectScale_OverallScaleCategory",
    "type": "radio",
    "value": "Enterprise-wide platform",
    "answeredAt": "2026-01-17T14:30:00Z",
    "rationale": "Expected user base exceeds 10k across multiple regions"
  },
  "Frontend_Frameworks": {
    "questionId": "Frontend_Frameworks",
    "type": "multiselect",
    "value": ["react", "typescript"],
    "answeredAt": "2026-01-17T14:32:00Z"
  },
  "Backend_CustomStack": {
    "questionId": "Backend_CustomStack",
    "type": "text",
    "value": "Python FastAPI + PostgreSQL + Redis",
    "answeredAt": "2026-01-17T14:35:00Z",
    "rationale": "Matches team expertise and performance requirements"
  }
}
```

### Answer Object Fields

- **questionId** (required): Question identifier matching schema
- **type** (required): Question type (must match schema)
- **value** (required): Answer value
  - Radio/text: String
  - Multiselect: Array of strings
- **answeredAt** (required): ISO 8601 timestamp in UTC when answer was recorded
- **rationale** (optional): Free-text explanation for the answer

### Upsert Semantics

- Setting an answer for an existing questionId **replaces** the previous answer entirely
- The `answeredAt` timestamp is updated on each modification
- Partial updates are not supported; provide complete answer object

## Python Action Scripts

**CRITICAL**: All modifications to `.rdd-instance/specifications/technical-design.json` must use these scripts. Direct file editing risks data corruption and format inconsistencies.

### Read Answers

```bash
python .rdd/src/actions/technical_design_read.py
```

**Output**: JSON object containing all answered questions (or empty object `{}`).

### Set/Update Answer

```bash
python .rdd/src/actions/technical_design_answer_set.py questionId=<id> type=<type> value=<value> [rationale=<text>]
```

**Parameters**:
- `questionId`: Question ID from schema (required)
- `type`: Question type - `radio`, `multiselect`, `text` (required)
- `value`: Answer value (required)
  - For multiselect: comma-separated list, e.g., `value="react,typescript"`
- `rationale`: Optional explanation for the answer

**Examples**:
```bash
# Set radio answer
python .rdd/src/actions/technical_design_answer_set.py questionId="ProjectScale_OverallScaleCategory" type="radio" value="Enterprise-wide platform"

# Set multiselect answer with rationale
python .rdd/src/actions/technical_design_answer_set.py questionId="Frontend_Frameworks" type="multiselect" value="react,typescript" rationale="Modern stack"

# Set text answer
python .rdd/src/actions/technical_design_answer_set.py questionId="Backend_CustomStack" type="text" value="FastAPI + PostgreSQL"
```

**Safety**:
- Validates questionId exists in schema
- Atomic write (temp file + rename) prevents corruption
- Auto-generates `answeredAt` timestamp

### Remove Answer

```bash
python .rdd/src/actions/technical_design_answer_remove.py questionId=<id>
```

**Example**:
```bash
python .rdd/src/actions/technical_design_answer_remove.py questionId="ProjectScale_OverallScaleCategory"
```

### Validate Answers

```bash
python .rdd/src/actions/technical_design_validate.py
```

**Checks**:
- All questionIds reference valid schema questions
- Answer types match schema question types
- Value types are correct (string for radio/text, array for multiselect)
- Required fields present

### Migrate Legacy Format

```bash
python .rdd/src/actions/technical_design_migrate.py [--dry-run]
```

**Features**:
- Detects legacy/old format automatically
- Creates timestamped backup before migration
- `--dry-run` shows what would be migrated without changes
- Safe to run multiple times (idempotent)

## RDD Execution Integration

### Reading Technical Design

All RDD execution modes read `.rdd-instance/specifications/technical-design.json` at the start (per `.rdd/prompt-snippets/execution.md` Step 4).

**Usage Pattern**:
```bash
# In prompts or execution steps
# Read technical design to inform decisions
python .rdd/src/actions/technical_design_read.py
```

### Compliance Requirements

When Technical Design contains answered questions:

- **Clarify Mode**: Generated questionnaires should respect architectural constraints (e.g., don't ask about cloud provider if already chosen)
- **Analyze Mode**: Analysis should consider recorded technology stack and deployment model
- **Plan Mode**: Plans should align with security, compliance, and operational choices
- **Implement Mode**: Implementation must comply with all technical design decisions

### Optional Nature

- Empty or missing Technical Design file does not block execution
- RDD flows proceed normally without Technical Design
- Prompts can explicitly override Technical Design (with justification)

## Web UI Integration

### Technical Design Page Requirements

- **Navigation**: Left sidebar for categories
- **Rendering**: Dynamic rendering from schema with questions displayed in a flat list
- **Search**: Full-text search across labels, options, help text
- **Filter**: By category, answered/unanswered status, question type
- **Editing**: Per-question widgets based on type (radio buttons, checkboxes, text inputs)
- **Conditional Visibility**: Questions appear/disappear based on `visibleWhen` rules evaluated in real-time
- **Save**: Calls Python scripts via Web UI backend API (never writes file directly)

### Web UI Backend Pattern

Following TR-0009 (REST-like JSON endpoints), the Web UI server provides:

```
GET  /api/technical-design/schema      - Read schema
GET  /api/technical-design/answers     - Read current answers
POST /api/technical-design/answer/set  - Set/update answer (calls technical_design_answer_set.py)
POST /api/technical-design/answer/remove - Remove answer (calls technical_design_answer_remove.py)
POST /api/technical-design/validate    - Validate answers (calls technical_design_validate.py)
POST /api/technical-design/migrate     - Trigger migration (calls technical_design_migrate.py)
```

Each endpoint invokes the corresponding Python action script via subprocess.

## Migration Strategy

### Detection

Migration runs automatically on Web UI startup when:
- File contains legacy format indicators:
  - `"sections"` key (old schema format mixed with answers)
  - `"schemaVersion"` key
  - Answer data in array format
- Current format: object keyed by questionId with `answeredAt` timestamps

### Migration Process

1. Backup original file: `technical-design.json.backup-<timestamp>`
2. Parse legacy format
3. Transform to new storage format (questionId-keyed object)
4. Validate migrated data
5. Write atomically

### Backwards Compatibility

- Migration is one-way (legacy → new)
- Original backup preserved for rollback
- No automatic migration of schema itself (only answers)

## Invariants

1. **Python scripts are the only write path** - Web UI, prompts, users must use scripts
2. **Only answered questions stored** - Empty/unanswered questions do not appear in file
3. **QuestionId uniqueness** - Each questionId appears at most once in answers
4. **Schema stability** - Question IDs should remain stable across schema updates
5. **UTF-8 encoding** - All JSON files use UTF-8
6. **Atomic writes** - All modifications use temp file + rename pattern

## Error Handling

Scripts provide structured JSON error messages:

```json
{
  "error": "Specific problem description",
  "details": "Technical details or exception message",
  "recovery": "Suggested remediation steps"
}
```

Example error scenarios:
- **Invalid questionId**: "Question ID not found in schema" → Check spelling and schema
- **Missing schema**: "Failed to load schema" → Ensure `.rdd/config/technical-design-schema.json` exists
- **JSON corruption**: "Invalid JSON" → Fix syntax or delete file to start fresh
- **Permission denied**: "Failed to save" → Check file permissions

## Examples

### Complete Workflow

1. **User opens Web UI Technical Design page**
2. **Backend calls migration script** (auto-detects format, migrates if needed)
3. **Frontend fetches schema and answers**:
   ```bash
   GET /api/technical-design/schema
   GET /api/technical-design/answers
   ```
4. **Frontend renders dynamic form** with conditional visibility
5. **User answers question** (radio button)
6. **Frontend calls set endpoint**:
   ```bash
   POST /api/technical-design/answer/set
   Body: { questionId: "...", type: "radio", value: "...", rationale: "..." }
   ```
7. **Backend invokes Python script**:
   ```bash
   python .rdd/src/actions/technical_design_answer_set.py questionId="..." type="..." value="..." rationale="..."
   ```
8. **Script validates, saves atomically, returns success**
9. **Frontend refreshes, shows updated state**

### CLI Usage

```bash
# Answer key architecture questions
python .rdd/src/actions/technical_design_answer_set.py questionId="CloudStrategy_DeploymentModel" type="radio" value="Public cloud only"

python .rdd/src/actions/technical_design_answer_set.py questionId="CloudStrategy_PrimaryProvider" type="radio" value="Azure" rationale="Enterprise standard"

python .rdd/src/actions/technical_design_answer_set.py questionId="Frontend_Frameworks" type="multiselect" value="react,typescript,webpack"

# Validate answers
python .rdd/src/actions/technical_design_validate.py

# View current answers
python .rdd/src/actions/technical_design_read.py

# Remove an answer
python .rdd/src/actions/technical_design_answer_remove.py questionId="Frontend_Frameworks"
```

## Maintenance

### Adding New Questions

1. Edit `.rdd/config/technical-design-schema.json`
2. Add question to appropriate category's questions array
3. Assign unique questionId
4. Define type, label, options, help text
5. Add `visibleWhen` rules if conditional
6. No migration needed (new questions simply unanswered)

### Removing/Deprecating Questions

1. Remove question from schema
2. Answers referencing removed questionId will fail validation
3. Use `technical_design_answer_remove.py` to clean up orphaned answers
4. Or let validation warnings inform manual cleanup

### Schema Evolution

- QuestionIds should be stable (avoid changing)
- Labels, help text, options can be updated freely
- Adding questions: safe, no migration
- Removing questions: requires cleanup of orphaned answers
- Renaming questionId: treat as remove + add (requires migration of answer data)


