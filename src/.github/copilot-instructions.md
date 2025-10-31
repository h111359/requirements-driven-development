# Concepts:

C01: `<cr-id>` is a placeholder representing a change request ID. It is a representation of a date and time following the format `YYYYMMDD-HHmm`, where YYYY is the four-digit year, MM is the two-digit month, DD is the two-digit day, HH is the two-digit hour in 24-hour format, and mm is the two-digit minutes. For example, a change request created on June 15, 2024, at 2:30 PM would have a `<cr-id>` of `20240615-1430`.

C02: `<cr-name>` is a placeholder representing a concise, hyphen-separated short name of the change request, sanitized to be lowercase, with unsupported characters removed, and spaces collapsed into single hyphens. The `<cr-name>` should not exceed 30 characters in length. For example, if the user provides the short name "Add User Authentication", the corresponding `<cr-name>` would be `add-user-authentication`.

# Rules:

R01:Lifecycle states (only these four values are valid; lowercase only):
1. **draft** – Initial state when the change request is created.
2. **clarified** – All clarifications are complete; ready for design.
3. **designed** – Design is finalized and implementation can begin.
4. **completed** – The change request has been fully implemented and closed. This is a final state; the state must not be changed any more. Further changes require a new change request.

Only these four states are permitted for any CR. No other states are allowed. States must be updated sequentially and are determined by the filename suffix.
States must be updated sequentially and are determined only by the filename suffix. Remove any State: field from CR files and instructions.

R02: Read and consider `.rdd-docs/requirements.md`, `.rdd-docs/README.md`, `.rdd-docs/technical-specification.md`, and `.rdd-docs/folder-structure.md`.


R03: Options Questions

Use this standardized format when presenting multiple options: concise, selectable choices in a compact ASCII box (A/B/C/...). Each descriptor ≤ 16 words.

Framed Question Template:
```

**Question**:  <Question text>?  

**Options:**
+--------------------------------------------------+
|  A) <Option A – brief descriptor>                |
|  B) <Option B – brief descriptor>                |
|  C) <Option C – brief descriptor>                |
|  D) <Option D – brief descriptor>                |
|  E) <Option E – brief descriptor>                |
|  F) <Option F – brief descriptor>                |
+--------------------------------------------------+
Reply: letter only (A–F).
```
Guidance:
- Omit unused trailing letters; stop at last needed option (e.g., D).
- Align vertical bars and pad lines for readability; box width matches longest line.
- For free-form follow-up, ask without the box and await user input.
- Act immediately on the selected option.
- Only reprint the box if the user's reply is invalid.

R04: Do **not** chain or stack multiple questions in one turn; wait for the answer.

R05  Keep every question line ≤ 120 characters.

R06: When the user should be asked for confirmation before proceeding, or everywhere else when the user should answer with simply yes or no, or confirm or not confirm or accept or not acceps (dual binary logic) use this standardized format:

```
**Please confirm to proceed: (Y/N)**
```

R07: Do not change anything outside the workspace - especially the python installation. Use only virtual environments inside the workspace if needed. Also so not change global git configurations, user settings, or any other global settings outside the workspace.

