*Role Context:** [[[ROLE_SOFTWARE_DEVELOPER]]]

**Background:**
The RDD framework uses prompt snippet keys (e.g., `[[[ROLE_SOLUTION_ARCHITECT]]]`, `[[[ANALYZE]]]`) to include reusable prompt instructions. These keys are defined in `.rdd/config/manifest.json` under the `promptSnippets` array. Currently, users must manually type these keys, which is error-prone and requires memorizing the exact syntax.

**Requirements:**

1. **Snippet Quick Picker** (Priority: HIGH)
   - Add a quick picker/dropdown UI component to the prompt editor in the Web UI
   - Display all available prompt snippet keys from manifest.json
   - Show snippet descriptions/paths alongside keys
   - Support search/filter within the snippet list
   - Insert selected snippet key at current cursor position
   - Accessible via keyboard shortcut (e.g., Ctrl+K, S) and toolbar button

2. **Snippet Preview** (Priority: MEDIUM)
   - Show preview of snippet file content when hovering over a snippet in the picker
   - Display file path and snippet description
   - Highlight syntax in preview (if applicable)

3. **Snippet Validation** (Priority: MEDIUM)
   - Validate snippet keys in prompt text against manifest.json
   - Show warning indicators for invalid/outdated snippet keys
   - Provide quick fix to update or remove invalid keys

4. **Future Considerations** (Priority: LOW)
   - Design with autocomplete integration in mind
   - Consider sidebar panel for snippet browsing
   - Plan for custom user snippets (not in this iteration)

**Technical Constraints:**
- Must read snippet definitions from `.rdd/config/manifest.json`
- Should update dynamically if manifest changes
- Web UI is built with [specify framework: React/Vue/etc.] - ensure compatibility
- Backend API may need new endpoint to serve snippet data

**Acceptance Criteria:**
- User can open snippet picker from prompt editor
- Picker shows all snippet keys with descriptions
- Selecting a snippet inserts the key (e.g., `[[[ROLE_SOLUTION_ARCHITECT]]]`) at cursor
- Picker supports keyboard navigation and search
- No performance impact on prompt editor load time
- Unit tests for snippet service and picker component

**Out of Scope:**
- Editing snippet definitions (read-only for now)
- Custom user snippets
- Snippet parameterization
- CLI integration (future iteration)

**Reference Implementation:**
Review VS Code's snippet picker implementation for UX patterns: [microsoft/vscode/src/vs/workbench/contrib/snippets/browser/snippetPicker.ts](https://github.com/microsoft/vscode/tree/main/src/vs/workbench/contrib/snippets/browser/snippetPicker.ts)