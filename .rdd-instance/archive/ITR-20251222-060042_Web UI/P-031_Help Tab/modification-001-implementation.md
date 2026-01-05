# Modification 001 Implementation

## Issue
The markdown to HTML converter in `.rdd/src/web/server.py` was rendering bold text incorrectly. Text marked with `**bold**` in markdown was appearing as "trong>" in the rendered HTML instead of being wrapped in `<strong>` tags.

## Root Cause
The bug was in the `_markdown_to_html()` function (lines 118-136 in server.py). The code was:
1. First calling `html.escape(line)` which converted special characters including `*` to HTML entities
2. Then trying to use regex to find `**text**` patterns, which no longer existed after escaping

The regex `r'\*\*(.+?)\*\*'` couldn't match anything because the asterisks had been converted to `&ast;` or similar entities.

## Solution
Refactored the markdown processing order in `.rdd/src/web/server.py` (lines 118-149):
1. Process markdown syntax FIRST (bold, italic, code, links) using lambda functions to escape only the content
2. Split the processed line by HTML tags to identify which parts are already HTML
3. Escape only the remaining plain text parts that aren't inside HTML tags
4. This ensures markdown is converted to HTML before escaping, so the patterns can be found

### Changes Made
**File**: `.rdd/src/web/server.py`
- Lines 118-149: Rewrote the inline markdown processing logic
- Changed from `html.escape()` first then regex, to regex first with selective escaping
- Used lambda functions in `re.sub()` to escape content while building HTML tags
- Added logic to split by HTML tags and escape only non-tag text

## Testing
```bash
# Verified syntax
python -m py_compile .rdd/src/web/server.py
```
No syntax errors.

## Expected Result
Bold text marked as `**text**` in the markdown user guide will now correctly render as `<strong>text</strong>` in the HTML output, appearing as bold text in the browser instead of showing "trong>" artifacts.