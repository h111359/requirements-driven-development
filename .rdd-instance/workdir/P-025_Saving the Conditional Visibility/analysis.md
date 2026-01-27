# Copilot Review

The prompt is currently a placeholder ("TBD"), so there is no explicit description of the expected behavior for saving conditional visibility rules in the Technical Design Schema Editor, leaving key details (trigger points, data format, validation rules, UI affordances, and legacy handling) unspecified; this uncertainty risks implementing a fix that diverges from prior conditional-visibility UX changes (P-023/P-024) and may not address the underlying persistence issue, especially given the many schema/editor iterations and flattened schema shape.

# Best Practices

- GOV.UK Design System – Conditionally revealing form questions: https://design-system.service.gov.uk/components/checkboxes/#conditionally-revealing-content — Keep conditional reveals simple, only reveal related questions, and be mindful of assistive technology notifications; complex conditional flows should be broken into simpler steps.
- W3C WAI Forms Notifications: https://www.w3.org/WAI/tutorials/forms/notifications/ — Provide clear inline feedback and accessible status updates (e.g., live regions, concise error copy) when dynamic form state changes; ensure users are informed when content appears/disappears.

# Proposals

- Clarify the desired persistence workflow: when a user edits conditional visibility (e.g., rule builder fields), define when saving should occur (auto-save on change vs. explicit save) and the expected validation (e.g., require questionId, operator, value; guard against missing referenced question/options).
- Align data format with prior prompts: confirm whether `visibleWhen` is stored as structured JSON array with questionId/operator/value (per P-023/P-024) and whether legacy string expressions still need to be accepted and migrated.
- Define UX signals: specify success/error feedback for save attempts (toast/status banner, inline errors near rule rows) and accessibility cues (aria-live updates) to match best-practice guidance.
- Identify regression surface: list all code paths that touch conditional visibility (schema editor rule builder, tech design page rendering, backend validators) to ensure the “saving” issue is fixed end-to-end rather than only in UI.

# Prompt Modification

A clearer prompt could be:

> The Technical Design Schema Editor’s conditional visibility rule builder is not persisting changes. Investigate and fix saving of `visibleWhen` rules so edits in the rule builder are written to `.rdd/config/technical-design-schema.json` using the structured array format `{questionId, operator, value}`. Ensure validation rejects missing/invalid question references or option values, provide clear user feedback (success/error), and preserve backward compatibility with legacy string rules. Describe tests covering add/edit/delete of rules, autosave behavior, and reload correctness.
