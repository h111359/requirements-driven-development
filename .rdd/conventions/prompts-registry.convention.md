## Purpose

`prompts-registry.md` is the canonical, repository-friendly registry of prompt texts for an RDD work iteration.

It must satisfy all of the following:
- Be human-readable and code-review friendly (Git).
- Be trivially machine-parseable (JavaScript/Python).
- Allow a JavaScript application to append new prompts safely.
- Allow a JavaScript application to print the exact prompt text by ID to the terminal.
- Allow Copilot (and humans) to locate the prompt text for a specific prompt ID with negligible risk of selecting the wrong text.

Operational execution state (e.g., active prompt, run status, questionnaire status/answers, runtime overrides) is stored in a separate JSON state file and MUST NOT be stored in `prompts-registry.md`.

---

## File invariants

1. The file is an ordered list of **prompt records**.
2. Each record is delimited by explicit sentinel lines:
   - Record start: `%%PROMPT <ID> "<TITLE>"`
   - Record end: `%%ENDPROMPT`
3. The prompt content is defined as the exact bytes between the record start line and record end line.
4. Prompt IDs MUST be unique within the file.


### Whitespace rules
- Sentinel lines MUST start at column 1 (no leading whitespace).
- Blank lines are allowed between elements.

---

## ID and Title rules

### ID
- Required.
- Format: `P-` followed by at least 3 digits, left-pad to 3 for <1000.
- Regex: `^P-[0-9]{3,}$`
- IDs are case-sensitive and MUST be treated as opaque identifiers.

### Title
- Required.
- Must be enclosed in double quotes on the start sentinel line.
- Titles are informational for humans and UIs; tools MUST NOT depend on title uniqueness.

---

## Parsing algorithm (normative)

Given a target ID `<ID>`, a parser MUST:

1. Scan the file linearly to find a line matching:
   - `%%PROMPT <ID> "<TITLE>"`
2. From the next line starts the prompt text 
4. Stop parsing the record at `%%ENDPROMPT`.
5. Return the captured lines as the prompt text.

Validation MUST fail if:
- The record start is found but:
  - `%%ENDPROMPT` is missing, or
  - another `%%PROMPT` appears before `%%ENDPROMPT` (nested/overlapping records).

---

## Editing rules (normative)

### Manual editing
- Humans may edit prompt text
- Humans MUST NOT change sentinel lines unless intentionally renaming an ID/title.

### Programmatic editing (JavaScript application)
To add a new prompt:
1. Append at the end of the file:
   - One blank line (optional)
   - `%%PROMPT <NEW_ID> "<TITLE>"`
   - Prompt text
   - `%%ENDPROMPT`
2. Ensure `<NEW_ID>` does not already exist (validate before write).
3. Preserve file line endings consistently (`\n` recommended).

To update an existing prompt:
- Locate record by ID using the parsing algorithm above.
- Replace only the content between record start line and record end line.
- Preserve sentinel lines and the overall record structure.

---

## Prohibited content / patterns (normative)

The following are NOT allowed:
- Using Markdown headings (`## ...`) as record boundaries.
- Using multiple fenced blocks inside a record.
- Including runtime state, active prompt selection, questionnaire answers, or execution logs.

---

## Example

%%PROMPT P-001 "Baseline problem statement"

You are a senior software architect.

Analyze the following problem and provide goals, constraints, and success criteria.

%%ENDPROMPT

%%PROMPT P-002 "Add architectural constraints"

Extend the previous response with repository-first, auditability, and incremental evolution constraints.
Focus on trade-offs and risks.

%%ENDPROMPT


