# Analysis: Prompt Snippets Adding in Prompt

## Copilot Review

### Brutally Honest Assessment

The request to add prompt snippet keys functionality is **well-conceived and addresses a real usability gap**. The current process requires users to manually type or remember the exact snippet keys like `[[[ROLE_SOLUTION_ARCHITECT]]]` which is error-prone and inefficient.

**Strengths of the Request:**
- Clear problem statement: users need to easily insert predefined prompt snippet keys
- Recognizes the need for three key features: viewing available snippets, seeing the prompt text, and placing snippets at chosen positions
- Acknowledges the existing manifest.json as the source of truth

**Weaknesses/Concerns:**
1. **Vague on implementation details** - "What are the possible approaches?" suggests uncertainty about technical direction
2. **Missing user workflow context** - Doesn't specify where this functionality should live (Web UI, CLI, both?)
3. **Scope ambiguity** - Should this be a simple picker or a more sophisticated editor with snippet support?
4. **No mention of testing or validation** - How will we ensure the snippet keys are valid and up-to-date?

**The Rough Reality:**
- This is a **medium-complexity feature** that will require UI/UX design, backend integration, and potentially frontend framework updates
- The current architecture already has a manifest.json with prompt snippets defined, which is good
- However, adding this to a web UI will require careful consideration of user experience - dropdown? autocomplete? modal? sidebar panel?
- **Risk:** Feature creep - users might want snippet preview, snippet editing, custom snippets, etc.
- **Technical debt consideration:** This adds another layer of indirection that must be maintained whenever prompt snippets change

## Best Practices

### Research Sources

#### 1. VS Code Snippet Implementation Patterns

**Source:** GitHub - microsoft/vscode repository  
**URL:** https://github.com/microsoft/vscode (examined snippet-related code)

**Key Findings:**
- **QuickPick Pattern**: VS Code uses a quick pick interface (`snippetPicker.ts`) for snippet selection
- **Autocomplete Integration**: Snippets appear in IntelliSense with `CompletionItemProvider`
- **Snippet Metadata**: Each snippet has label, description, prefix, and body
- **Enable/Disable Mechanism**: Users can show/hide snippets from IntelliSense
- **Categorization**: Snippets are grouped by source (User, Workspace, Extension)
- **Visual Hierarchy**: Separators distinguish different snippet groups

**Best Practices Identified:**
1. Use a searchable quick pick/dropdown for snippet selection
2. Show snippet metadata (description, source) in the UI
3. Provide keyboard shortcuts for common operations
4. Group snippets logically (by category or source)
5. Support filtering/search within the snippet list

#### 2. Stack Overflow - Template/Snippet UI Patterns

**Source:** StackOverflow questions on code snippets and templates  
**URL:** https://stackoverflow.com/questions/tagged/snippet

**Key Findings:**
- Users expect **autocomplete-style insertion** for snippets
- **Prefix-based triggering** is a common pattern (type prefix → snippet appears)
- **Multi-cursor support** can enhance snippet workflows
- **Snippet variables** (like $1, $2) are expected for cursor positioning
- **Discoverability is crucial** - users need to know what snippets are available

**Best Practices Identified:**
1. Provide visual feedback when snippet is available
2. Use familiar UI patterns (autocomplete, command palette)
3. Show snippet preview before insertion
4. Support keyboard-driven workflows
5. Make snippets discoverable without requiring memorization

#### 3. UX StackExchange - Template Insertion UI/UX

**Source:** UX StackExchange discussions on templates  
**URL:** https://ux.stackexchange.com/questions/tagged/templates

**Key Findings:**
- **Template pickers should be contextual** - show relevant templates based on current state
- **Preview before insert** is highly valued by users
- **Template vs. theme distinction** - users understand templates as content structures
- **Centralized editability** - users want to edit template definitions in one place
- **Tag-based systems** work well for categorizing templates

**Best Practices Identified:**
1. Provide context-aware snippet suggestions
2. Show live preview of snippet content
3. Allow users to manage snippets from a central location
4. Use clear visual indicators for template/snippet types
5. Support both mouse and keyboard interactions

### Synthesis of Best Practices

**For Prompt Snippet Insertion UI:**
1. **Primary Interface**: Command palette or autocomplete-style picker
2. **Secondary Interface**: Dedicated snippet panel/sidebar for browsing
3. **Key Features:**
   - Search/filter by snippet key or description
   - Show snippet content preview
   - Categorize by role type or function
   - Keyboard shortcuts for insertion
   - Visual indicators for snippet boundaries in text
4. **User Experience:**
   - Minimal friction: 2-3 clicks maximum to insert
   - Progressive disclosure: basic list → detailed preview → insert
   - Discoverability: prominently feature snippet functionality

## Samples from GitHub

### How Other Projects Solve Similar Problems

#### VS Code Snippet System

**Repository:** microsoft/vscode  
**Approach:** Multi-layered snippet support

**Key Implementation Details:**
- **SnippetPicker**: Quick pick interface with search and categorization
- **CompletionProvider**: Autocomplete integration in editors
- **Snippet Files**: JSON-based snippet definitions with metadata
- **Services Layer**: `ISnippetsService` manages snippet lifecycle
- **UI Components**: Quick pick, completion widget, snippet editor

**Code Pattern Example:**
```typescript
// Picker pattern
async function pickSnippet(accessor: ServicesAccessor, 
                          languageIdOrSnippets: string | Snippet[]): Promise<Snippet | undefined> {
  const snippetService = accessor.get(ISnippetsService);
  const quickInputService = accessor.get(IQuickInputService);
  
  // Create categorized picks with metadata
  const picks = snippets.map(snippet => ({
    label: snippet.prefix || snippet.name,
    detail: snippet.description || snippet.body,
    snippet
  }));
  
  // Show quick pick with search
  const picker = quickInputService.createQuickPick();
  picker.items = makeSnippetPicks();
  picker.matchOnDetail = true;
  
  // Return selected snippet
  return await picker.selectedItems[0]?.snippet;
}
```

**Lessons Learned:**
- Separate data layer (service) from UI layer (picker)
- Use existing UI primitives (quick pick)
- Provide rich metadata in picker
- Support both programmatic and interactive insertion

#### Notion-like Template Systems

**Approach:** Inline template picker with preview

**Key Features:**
- Type `/` to trigger template menu
- Fuzzy search through templates
- Hover preview shows template content
- Click or Enter to insert
- Recently used templates at top

**Applicability to RDD:**
- Inline `/snippet` command could trigger picker
- Show prompt snippet keys with descriptions
- Preview shows actual snippet content from file
- Insert at cursor position

#### JetBrains Live Templates

**Approach:** Context-aware template suggestions

**Key Features:**
- Templates appear in code completion
- Customizable by language/context
- Tab to expand template
- Tab stops for parameterization
- Template preview in documentation popup

**Applicability to RDD:**
- Could integrate snippet picker into prompt editor
- Show snippet preview on hover
- Allow tab expansion if prefix matches

## Proposals

### Proposed Changes to Requirements

#### 1. **Clarify User Context and Interface**

**Current Gap:** The prompt doesn't specify *where* users will add snippets (Web UI text editor, CLI, both).

**Proposed Requirement Addition:**
- Primary interface: Web UI prompt editor
- Secondary interface: CLI command for snippet insertion
- Both should use the same underlying snippet service

#### 2. **Define Specific Features**

**Proposed Feature Set:**
1. **Snippet Browser Panel** (Web UI)
   - Sidebar panel listing all available snippets
   - Search/filter functionality
   - Categorized by snippet type (ROLE, ANALYZE, etc.)
   - Preview pane showing snippet content

2. **Inline Snippet Insertion** (Web UI)
   - Slash command `/snippet` triggers quick picker
   - Autocomplete shows matching snippets as user types `[[[`
   - Click to insert at cursor position

3. **Snippet Management View** (Web UI)
   - Read-only view of snippet definitions
   - Shows file path and content
   - Link to manifest.json for reference

4. **CLI Snippet Support**
   - `rdd snippet list` - show available snippets
   - `rdd snippet view <key>` - show snippet content
   - `rdd snippet insert <key>` - add to prompt file

#### 3. **Add Validation Requirements**

**Proposed Addition:**
- Validate snippet keys against manifest.json
- Show warning if snippet key in prompt text doesn't exist in manifest
- Auto-update snippet list when manifest.json changes
- Provide migration path if snippet keys are renamed

#### 4. **Consider Future Extensibility**

**Proposed Consideration:**
- Design with custom user snippets in mind (future feature)
- Allow snippet parameters/placeholders (like `[[[ROLE {role_name}]]]`)
- Support snippet composition (snippets that include other snippets)

### Different Implementation Options

#### Option A: Simple Dropdown Menu

**Description:** Add a dropdown menu to the prompt editor with all snippet keys.

**Pros:**
- Simplest to implement
- Familiar UI pattern
- Low learning curve

**Cons:**
- Doesn't show snippet content
- Poor discoverability for large snippet lists
- No search functionality

**Implementation Effort:** Low (1-2 days)

#### Option B: Command Palette Integration

**Description:** Add snippet insertion to existing command palette or create dedicated snippet palette.

**Pros:**
- Keyboard-driven workflow
- Searchable
- Consistent with modern editor patterns
- Can show snippet descriptions

**Cons:**
- Requires keyboard shortcut learning
- May not be discoverable to new users
- Doesn't show preview of snippet content

**Implementation Effort:** Medium (3-5 days)

#### Option C: Rich Snippet Panel (Recommended)

**Description:** Dedicated sidebar panel with snippet browser, search, and preview.

**Pros:**
- **Best discoverability**
- Shows full snippet content
- Searchable and filterable
- Can categorize snippets
- Supports future features (custom snippets)

**Cons:**
- Higher implementation complexity
- Takes up screen space
- Requires more UI/UX design

**Implementation Effort:** High (5-7 days)

#### Option D: Hybrid Approach (Most Practical)

**Description:** Combine inline autocomplete + quick picker + snippet panel.

**Components:**
1. **Autocomplete**: Typing `[[[` triggers snippet suggestions
2. **Quick Picker**: Keyboard shortcut (Ctrl+K S) opens snippet picker
3. **Snippet Panel**: Optional sidebar for browsing (can be collapsed)

**Pros:**
- **Serves different user preferences**
- Autocomplete for power users
- Picker for keyboard-driven workflow
- Panel for exploration and learning
- Highest flexibility

**Cons:**
- Most complex to implement
- Requires coordination between components
- More code to maintain

**Implementation Effort:** High (7-10 days)

**Recommendation:** Start with Option D but implement incrementally:
1. Phase 1: Quick Picker (3-5 days)
2. Phase 2: Autocomplete integration (2-3 days)
3. Phase 3: Snippet Panel (3-5 days)

## Prompt Modification

### How I Would Write This Prompt

If I were writing this prompt to be clearer and more actionable, here's what I would write:

---

**Title:** Add Prompt Snippet Insertion UI to Web Interface

**Role Context:** [[[ROLE_SOFTWARE_DEVELOPER]]]

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

---

### Key Improvements in This Version:

1. **Specific role assignment** - Uses SOFTWARE_DEVELOPER instead of SOLUTION_ARCHITECT (more appropriate for implementation)
2. **Clearer requirements structure** - Prioritized list with specific features
3. **Technical constraints spelled out** - Mentions manifest.json, framework, API needs
4. **Acceptance criteria defined** - Measurable success metrics
5. **Scope boundaries** - Explicitly states what's out of scope
6. **Reference implementation** - Points to real-world example to learn from
7. **Phased approach implied** - Priorities allow for incremental implementation
8. **No analysis prompt needed** - This is an implementation prompt, not a design exploration

### Why This Is Better:

- **Actionable** - Developer knows exactly what to build
- **Bounded** - Clear scope prevents feature creep
- **Prioritized** - Can deliver MVP quickly, iterate later
- **Context-rich** - Explains the "why" behind the feature
- **Testable** - Acceptance criteria enable verification
- **Reference-aware** - Points to proven patterns

The original prompt was exploratory ("What are the possible approaches?"), which is appropriate for the ANALYZE phase with SOLUTION_ARCHITECT role. But for actual implementation, the prompt should be specific and directive, which is what this revised version provides.
