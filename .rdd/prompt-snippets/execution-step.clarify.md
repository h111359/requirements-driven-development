## Definitions

See the definitions in `.rdd/prompt-snippets/execution.md`


## Instructions - Follow these steps exactly:

1. Before generating any questions, review the already-loaded context from execution.md:
   - [ACTIVE-PROMPT]
   - [REQUIREMENTS]
   - [TECHNICAL-DESIGN]
   - [FILES-AND-FOLDERS]
   - [WI-REGISTRY]
   Generate questions ONLY when a decision is required for implementation and the answer cannot be derived from these sources.

2. Identify ambiguous or underspecified parts of [ACTIVE-PROMPT] that have multiple plausible interpretations which would lead to materially different implementation/design outcomes. For each such ambiguity, generate ONE multiple-choice question with up to 5 mutually exclusive, realistic options.

3. Create or update the questionnaire JSON file:
   - The questionnaire must be a JSON file named `questionnaire.json` in the [ACTIVE-PROMPT-FOLDER].
   - Follow the JSON schema in `.rdd/conventions/questionnaire-json-schema.md`.
   - Include root-level `context` and a `questions` array.
   - For each question include: `id`, `question-text`, `options` (with `pros`/`cons`), `recommended-option`, `recommendation-rationale`, and `user-selection`.
   - Initialize all `user-selection` fields as `{"type": null, "value": null}`.

4. Idempotency and duplication rules:
   - If `questionnaire.json` does NOT exist: create it and write all generated questions.
   - If `questionnaire.json` already exists:
     - Do NOT modify existing question objects (including their options, recommendations, or existing `user-selection`).
     - You MAY append new questions ONLY if they are not duplicates of existing ones.
     - Treat questions as duplicates if their normalized `question-text` matches an existing question’s normalized `question-text` (case-insensitive, trimmed whitespace).


## Execution Step Rules

- Do not generate questions for which answers are already found in the context files.
- Always follow the conventions defined in [QUESTIONNAIRE-CONVENTION].
