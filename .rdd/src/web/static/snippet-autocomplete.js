// Snippet Autocomplete Component - Modal-based snippet picker

class SnippetAutocomplete {
    constructor(textareaId, snippetService) {
        this.textarea = document.getElementById(textareaId);
        this.snippetService = snippetService;
        this.modal = null;
        this.modalInstance = null;
        this.selectedSnippet = null;
        this.filteredSnippets = [];
        this.cursorPositionBeforeModal = 0;
        this.triggerSequence = '[[[';
        this.debounceTimer = null;
        
        if (this.textarea) {
            this.init();
        }
    }

    /**
     * Initialize the autocomplete component
     */
    init() {
        // Get modal element
        this.modal = document.getElementById('snippetPickerModal');
        if (!this.modal) {
            console.error('Snippet picker modal not found');
            return;
        }
        
        this.modalInstance = new bootstrap.Modal(this.modal);
        
        // Add event listeners for textarea
        this.textarea.addEventListener('input', (e) => this.onInput(e));
        
        // Add event listeners for modal elements
        const searchInput = document.getElementById('snippet-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.onSearch(e));
        }
        
        const insertBtn = document.getElementById('insert-snippet-btn');
        if (insertBtn) {
            insertBtn.addEventListener('click', () => this.insertSelectedSnippet());
        }
        
        // Reset on modal close
        this.modal.addEventListener('hidden.bs.modal', () => this.onModalClose());
    }

    /**
     * Handle input events with debouncing to detect [[[
     */
    onInput(e) {
        clearTimeout(this.debounceTimer);
        
        this.debounceTimer = setTimeout(() => {
            this.checkTrigger();
        }, 150);
    }

    /**
     * Check if trigger sequence was typed
     */
    checkTrigger() {
        const cursorPos = this.textarea.selectionStart;
        const textBeforeCursor = this.textarea.value.substring(0, cursorPos);
        
        // Find the last occurrence of the trigger sequence before cursor
        const lastTriggerIndex = textBeforeCursor.lastIndexOf(this.triggerSequence);
        
        if (lastTriggerIndex === -1) {
            return;
        }
        
        // Check if there's text after the trigger
        const textAfterTrigger = textBeforeCursor.substring(lastTriggerIndex + this.triggerSequence.length);
        
        // Don't show if already closed with ]]]
        if (textBeforeCursor.includes(']]]', lastTriggerIndex)) {
            const closingIndex = textBeforeCursor.indexOf(']]]', lastTriggerIndex);
            if (closingIndex < cursorPos) {
                return;
            }
        }
        
        // Only trigger if [[[  was just typed (within last few characters)
        if (cursorPos - lastTriggerIndex === 3) {
            this.showModal('');
        }
    }

    /**
     * Show the modal snippet picker
     * @param {string} initialQuery - Initial search query
     */
    async showModal(initialQuery = '') {
        try {
            // Save cursor position
            this.cursorPositionBeforeModal = this.textarea.selectionStart;
            
            // Load snippets
            await this.snippetService.loadSnippets();
            this.filteredSnippets = this.snippetService.searchSnippets(initialQuery);
            
            // Set search input
            const searchInput = document.getElementById('snippet-search');
            if (searchInput) {
                searchInput.value = initialQuery;
            }
            
            // Render snippet list
            this.renderSnippetList();
            
            // Show modal
            this.modalInstance.show();
            
            // Focus search input
            setTimeout(() => {
                if (searchInput) {
                    searchInput.focus();
                }
            }, 300);
        } catch (error) {
            console.error('Error showing snippet modal:', error);
        }
    }

    /**
     * Handle search input
     */
    onSearch(e) {
        const query = e.target.value;
        this.filteredSnippets = this.snippetService.searchSnippets(query);
        this.renderSnippetList();
    }

    /**
     * Render the snippet list in modal
     */
    renderSnippetList() {
        const container = document.getElementById('snippet-list-modal');
        if (!container) return;
        
        container.innerHTML = '';
        
        if (this.filteredSnippets.length === 0) {
            container.innerHTML = '<p class="text-muted text-center p-3">No snippets found</p>';
            document.getElementById('insert-snippet-btn').disabled = true;
            return;
        }
        
        this.filteredSnippets.forEach((snippet, index) => {
            const item = document.createElement('div');
            item.className = 'snippet-modal-item p-3 border-bottom';
            item.style.cursor = 'pointer';
            item.dataset.index = index;
            
            const keyText = snippet.key.replace('[[[', '').replace(']]]', '');
            const description = snippet.description || '';
            
            item.innerHTML = `
                <div class="fw-bold text-primary font-monospace" style="font-size: 0.9rem;">${keyText}</div>
                <div class="text-muted small">${description}</div>
            `;
            
            // Click to select and show preview
            item.addEventListener('click', () => this.selectSnippet(index));
            
            // Double-click to insert immediately
            item.addEventListener('dblclick', () => {
                this.selectSnippet(index);
                this.insertSelectedSnippet();
            });
            
            container.appendChild(item);
        });
    }

    /**
     * Select a snippet and show preview
     * @param {number} index - Index of snippet in filtered list
     */
    selectSnippet(index) {
        this.selectedSnippet = this.filteredSnippets[index];
        
        // Update UI - highlight selected item
        const items = document.querySelectorAll('.snippet-modal-item');
        items.forEach((item, i) => {
            if (i === index) {
                item.style.backgroundColor = '#e7f3ff';
                item.style.borderLeft = '4px solid #0d6efd';
            } else {
                item.style.backgroundColor = '';
                item.style.borderLeft = '';
            }
        });
        
        // Show preview
        this.showPreview(this.selectedSnippet);
        
        // Enable insert button
        document.getElementById('insert-snippet-btn').disabled = false;
    }

    /**
     * Show preview of selected snippet
     * @param {Object} snippet - Snippet object
     */
    showPreview(snippet) {
        const container = document.getElementById('snippet-preview-modal');
        if (!container) return;
        
        container.innerHTML = `
            <div class="p-3 bg-light border-bottom">
                <div class="fw-bold font-monospace text-primary">${snippet.key}</div>
                <div class="text-muted small">${snippet.path}</div>
            </div>
            <div class="p-3">
                <pre class="mb-0" style="white-space: pre-wrap; font-size: 0.85rem;">${snippet.content || 'No content'}</pre>
            </div>
        `;
    }

    /**
     * Insert the selected snippet at cursor position
     */
    insertSelectedSnippet() {
        if (!this.selectedSnippet) {
            return;
        }
        
        const snippet = this.selectedSnippet;
        const cursorPos = this.cursorPositionBeforeModal;
        const textBeforeCursor = this.textarea.value.substring(0, cursorPos);
        const textAfterCursor = this.textarea.value.substring(cursorPos);
        
        // Find if there's a [[[  before cursor that we should replace
        const lastTriggerIndex = textBeforeCursor.lastIndexOf(this.triggerSequence);
        
        let newTextBefore;
        if (lastTriggerIndex !== -1 && cursorPos - lastTriggerIndex <= 20) {
            // Replace the [[[ and any text after it with the snippet key
            newTextBefore = textBeforeCursor.substring(0, lastTriggerIndex) + snippet.key;
        } else {
            // Just insert at cursor position
            newTextBefore = textBeforeCursor + snippet.key;
        }
        
        const newValue = newTextBefore + textAfterCursor;
        
        // Update textarea
        this.textarea.value = newValue;
        
        // Set cursor position after inserted snippet
        const newCursorPos = newTextBefore.length;
        this.textarea.setSelectionRange(newCursorPos, newCursorPos);
        
        // Trigger input event
        this.textarea.dispatchEvent(new Event('input', { bubbles: true }));
        
        // Close modal
        this.modalInstance.hide();
        
        // Focus back on textarea
        this.textarea.focus();
    }

    /**
     * Handle modal close
     */
    onModalClose() {
        this.selectedSnippet = null;
        this.filteredSnippets = [];
        
        // Clear search
        const searchInput = document.getElementById('snippet-search');
        if (searchInput) {
            searchInput.value = '';
        }
        
        // Clear preview
        const previewContainer = document.getElementById('snippet-preview-modal');
        if (previewContainer) {
            previewContainer.innerHTML = `
                <div class="p-3 bg-light border-bottom">
                    <strong>Preview</strong>
                </div>
                <div class="p-3">
                    <p class="text-muted">Select a snippet to preview</p>
                </div>
            `;
        }
        
        // Disable insert button
        document.getElementById('insert-snippet-btn').disabled = true;
    }

    /**
     * Manually trigger the modal
     */
    trigger() {
        // Save current cursor position
        this.cursorPositionBeforeModal = this.textarea.selectionStart;
        
        // Clear any pending debounce
        clearTimeout(this.debounceTimer);
        
        // Show modal without inserting [[[
        this.showModal('');
    }
}

// Global instance - will be initialized when prompt editor is loaded
let promptSnippetAutocomplete = null;

/**
 * Initialize snippet autocomplete for the prompt editor
 */
function initializeSnippetAutocomplete() {
    if (promptSnippetAutocomplete) {
        return;
    }
    
    const textarea = document.getElementById('active-editor-prompt-md');
    if (textarea && snippetService) {
        promptSnippetAutocomplete = new SnippetAutocomplete('active-editor-prompt-md', snippetService);
        console.log('Snippet autocomplete initialized');
    }
}

