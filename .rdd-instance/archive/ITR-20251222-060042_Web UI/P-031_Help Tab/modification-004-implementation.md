# Modification 004 Implementation

## Issue
HTML entities were appearing in the rendered user guide. For example, "Web interface won't start" was displaying as "Web interface won&#x27;t start" with the apostrophe converted to the HTML entity `&#x27;`.

## Root Cause Analysis
The markdown processor was double-escaping text. Here's what was happening:

1. Markdown patterns (bold, italic, etc.) were matched using regex
2. The matched content was escaped using `html.escape()` inside lambda functions
3. After all markdown processing, the code split the result by HTML tags
4. Any text not inside tags was escaped AGAIN with `html.escape()`

So text like "won't" inside a header or paragraph would be:
1. First escaped in step 2: "won't" → "won't" (if inside markdown)
2. Then escaped again in step 4: "won't" → "won&#x27;t"

This double-escaping caused apostrophes and other special characters to show as HTML entities.

## Solution
Completely rewrote the markdown processing logic in `.rdd/src/web/server.py` (lines 113-161) using a single-pass approach:

1. **Created `process_markdown()` function** that processes the entire line in one pass:
   - Uses a combined regex pattern to find ALL markdown syntax (bold, italic, code, links)
   - Iterates through matches in order
   - For text BEFORE each match: escape it (plain text)
   - For text INSIDE each match: escape it and wrap in appropriate HTML tags
   - For text AFTER all matches: escape it (plain text)

2. **Key improvement**: Each piece of text is escaped exactly ONCE:
   - Plain text between markdown: escaped once
   - Content inside markdown tags: escaped once (when building the tag)
   - No post-processing escaping, so no double-escaping

### Changes Made
**File**: `.rdd/src/web/server.py`
- Lines 113-161: Completely rewrote inline markdown processing
- Removed the separate regex replacements for bold, italic, code, links
- Removed the tag-splitting post-processing step
- Added `process_markdown()` function with combined regex pattern
- Pattern: `r'(\*\*(.+?)\*\*)|(_(.+?)_)|(`(.+?)`)|(\[(.+?)\]\((.+?)\))'`
- Uses match groups to identify which markdown type was matched
- Processes text sequentially, escaping each piece exactly once

## Testing
```bash
python -m py_compile .rdd/src/web/server.py
```
No syntax errors.

## Expected Result
- Apostrophes, quotes, and other special characters display correctly as regular characters
- No HTML entities (like `&#x27;`, `&quot;`, `&amp;`) appear in the rendered text
- All markdown formatting (bold, italic, code, links) still works correctly
- Text is properly escaped to prevent XSS attacks, but only escaped once
- The user guide displays with natural, readable text throughout
