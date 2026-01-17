// RDD Web Interface - Main JavaScript

// Global state
let sessionToken = null;
let currentPromptId = null;
let currentRegistry = null;
let currentEditingPrompt = null;
let currentPromptFolder = null;
let isViewOnlyMode = false;

// State persistence module
const StateManager = {
    // Keys for sessionStorage
    KEYS: {
        SECTION: 'rdd_current_section',
        FILE_VIEW: 'rdd_current_file_view'
    },
    
    // Save current section
    saveSection(sectionName) {
        try {
            sessionStorage.setItem(this.KEYS.SECTION, sectionName);
        } catch (e) {
            console.warn('Failed to save section state:', e);
        }
    },
    
    // Get saved section
    getSection() {
        try {
            return sessionStorage.getItem(this.KEYS.SECTION);
        } catch (e) {
            console.warn('Failed to get section state:', e);
            return null;
        }
    },
    
    // Save current file view (for active-prompt section)
    saveFileView(fileView) {
        try {
            sessionStorage.setItem(this.KEYS.FILE_VIEW, fileView);
        } catch (e) {
            console.warn('Failed to save file view state:', e);
        }
    },
    
    // Get saved file view
    getFileView() {
        try {
            return sessionStorage.getItem(this.KEYS.FILE_VIEW);
        } catch (e) {
            console.warn('Failed to get file view state:', e);
            return null;
        }
    },
    
    // Clear all saved state
    clearAll() {
        try {
            sessionStorage.removeItem(this.KEYS.SECTION);
            sessionStorage.removeItem(this.KEYS.FILE_VIEW);
        } catch (e) {
            console.warn('Failed to clear state:', e);
        }
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
async function initializeApp() {
    try {
        // Get session token
        const response = await fetch('/api/token');
        const data = await response.json();
        sessionToken = data.token;
        
        // Initialize snippet service
        if (typeof snippetService !== 'undefined') {
            snippetService.init(sessionToken);
        }
        
        // Load initial data
        await loadRegistry();
        await loadActivePrompt();
        // Start background refresh of active prompt statuses and mode buttons
        startActivePromptRefresh();
        
        // Setup help system
        setupExecutionModeTooltips();
        setupStatusFlagTooltips();
        initializeTooltips();
        
        // Restore previous section state if available
        const savedSection = StateManager.getSection();
        if (savedSection && savedSection !== 'active-prompt') {
            // Validate section exists before restoring
            const sectionElement = document.getElementById('section-' + savedSection);
            if (sectionElement) {
                // Navigate to saved section
                showSection(savedSection);
            } else {
                // Invalid section, clear state and stay on default (active-prompt)
                StateManager.saveSection('active-prompt');
            }
        } else {
            // Default to active-prompt and save initial state
            StateManager.saveSection('active-prompt');
        }
        
        showAlert('success', 'Application initialized successfully');
    } catch (error) {
        showAlert('danger', 'Failed to initialize application: ' + error.message);
    }
}

/**
 * Show/hide sections
 */
function showSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.style.display = 'none');
    
    // Remove active class from all nav links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));
    
    // Show selected section
    const targetSection = document.getElementById('section-' + sectionName);
    if (targetSection) {
        targetSection.style.display = 'block';
    }
    
    // Add active class to clicked nav link
    if (event && event.target) {
        event.target.classList.add('active');
    } else {
        // Find and activate the corresponding nav link when called programmatically
        const navLink = document.querySelector(`a[onclick*="showSection('${sectionName}')"]`);
        if (navLink) {
            navLink.classList.add('active');
        }
    }
    
    // Save current section state
    StateManager.saveSection(sectionName);
    
    // Load section-specific data
    if (sectionName === 'active-prompt') {
        loadActivePrompt();
    } else if (sectionName === 'config') {
        loadConfig();
    } else if (sectionName === 'workdir') {
        loadIterationStatus();
    } else if (sectionName === 'technical-design') {
        loadTechnicalDesign();
    } else if (sectionName === 'requirements') {
        loadRequirements();
    } else if (sectionName === 'help') {
        loadUserGuide();
    }
}

/**
 * Show alert message
 */
function showAlert(type, message, duration = 5000) {
    const alertContainer = document.getElementById('alert-container');
    const alertId = 'alert-' + Date.now();
    
    const alertHtml = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="bi bi-${getAlertIcon(type)}"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.innerHTML = alertHtml;
    
    // Auto-dismiss after specified duration
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, duration);
}

/**
 * Get icon for alert type
 */
function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle-fill',
        'danger': 'exclamation-triangle-fill',
        'warning': 'exclamation-circle-fill',
        'info': 'info-circle-fill'
    };
    return icons[type] || 'info-circle-fill';
}

/**
 * Execute an RDD action
 */
async function executeAction(domain, action, params = {}) {
    try {
        const response = await fetch('/api/action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                domain: domain,
                action: action,
                params: params
            })
        });
        
        const result = await response.json();
        return result;
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Load work iteration registry
 */
async function loadRegistry() {
    try {
        const response = await fetch('/api/registry');
        const result = await response.json();
        
        if (result.success) {
            currentRegistry = result.data;
            return currentRegistry;
        } else {
            console.error('Failed to load registry:', result.error);
            return null;
        }
    } catch (error) {
        console.error('Error loading registry:', error);
        return null;
    }
}

/**
 * Load prompts list
 */
async function loadPrompts() {
    const container = document.getElementById('prompts-table-container');
    container.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
    
    await loadRegistry();
    
    if (!currentRegistry || !currentRegistry.prompts) {
        container.innerHTML = '<p class="text-warning">No work iteration found. Please create one in the Prompts History section.</p>';
        return;
    }
    
    const prompts = currentRegistry.prompts;
    
    if (prompts.length === 0) {
        container.innerHTML = '<p class="text-muted">No prompts found. Create one using the button above.</p>';
        return;
    }
    
    // Build table
    let html = `
        <div class="table-responsive">
            <table class="table table-striped table-hover">
                <thead class="table-primary">
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>State</th>
                        <th>Executed</th>
                        <th>Analyze Mode</th>
                        <th>Plan Mode</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    prompts.forEach(prompt => {
        const promptId = prompt['prompt-id'];
        const title = prompt.title || prompt['prompt-title'] || '';
        const state = prompt.state || '';
        const analyzeEnabled = prompt['analyze-enabled'] || false;
        const planEnabled = prompt['plan-enabled'] || false;
        const executed = prompt['executed'] || false;
        
        const stateBadge = getStateBadge(state);
        
        // Executed badge
        const executedBadge = executed 
            ? '<span class="badge bg-success"><i class="bi bi-check-circle"></i> Yes</span>'
            : '<span class="badge bg-secondary">No</span>';
        
        // Determine if prompt is editable (active)
        const isEditable = (state === 'active');
        const buttonType = isEditable ? 'primary' : 'secondary';
        const buttonLabel = isEditable ? 'Edit' : 'View';
        const buttonIcon = isEditable ? 'pencil' : 'eye';
        
        // Analyze toggle (only for active prompts)
        let analyzeToggleHtml = '';
        if (state === 'active') {
            const toggleChecked = analyzeEnabled ? 'checked' : '';
            const toggleId = `analyze-toggle-${promptId}`;
            analyzeToggleHtml = `
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" id="${toggleId}" 
                           ${toggleChecked} onchange="toggleAnalyzeMode('${promptId}', this.checked)">
                    <label class="form-check-label" for="${toggleId}">
                        ${analyzeEnabled ? 'ON' : 'OFF'}
                    </label>
                </div>
            `;
        } else {
            analyzeToggleHtml = '<span class="text-muted">N/A</span>';
        }
        
        // Plan toggle (only for active prompts)
        let planToggleHtml = '';
        if (state === 'active') {
            const toggleChecked = planEnabled ? 'checked' : '';
            const toggleId = `plan-toggle-${promptId}`;
            planToggleHtml = `
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" id="${toggleId}" 
                           ${toggleChecked} onchange="togglePlanMode('${promptId}', this.checked)">
                    <label class="form-check-label" for="${toggleId}">
                        ${planEnabled ? 'ON' : 'OFF'}
                    </label>
                </div>
            `;
        } else {
            planToggleHtml = '<span class="text-muted">N/A</span>';
        }
        
        // Complete button (only for active prompts with executed=true)
        let completeButtonHtml = '';
        if (state === 'active') {
            const completeDisabled = !executed ? 'disabled' : '';
            const completeTitle = !executed ? 'Prompt must be executed first' : 'Complete this prompt';
            completeButtonHtml = `
                <button class="btn btn-sm btn-success" 
                        onclick="completePrompt('${promptId}')"
                        ${completeDisabled}
                        title="${completeTitle}">
                    <i class="bi bi-check-lg"></i> Complete
                </button>
            `;
        }
        
        html += `
            <tr>
                <td><code>${promptId}</code></td>
                <td>${escapeHtml(title)}</td>
                <td>${stateBadge}</td>
                <td>${executedBadge}</td>
                <td>${analyzeToggleHtml}</td>
                <td>${planToggleHtml}</td>
                <td>
                    <button class="btn btn-sm btn-${buttonType}" 
                            onclick="openPromptEditor('${promptId}', ${!isEditable})">
                        <i class="bi bi-${buttonIcon}"></i> ${buttonLabel}
                    </button>
                    <button class="btn btn-sm btn-primary" 
                            onclick="showSetStateModal('${promptId}', '${state}')">
                        <i class="bi bi-pencil"></i> Set State
                    </button>
                    ${completeButtonHtml}
                </td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = html;
}

/**
 * Get badge HTML for state
 */
function getStateBadge(state) {
    const badges = {
        'active': '<span class="badge bg-warning">Active</span>',
        'completed': '<span class="badge bg-success">Completed</span>'
    };
    return badges[state] || '<span class="badge bg-light text-dark">' + state + '</span>';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Show create prompt modal
 */
function showCreatePromptModal() {
    const modal = new bootstrap.Modal(document.getElementById('createPromptModal'));
    
    // Reset form
    document.getElementById('prompt-title').value = '';
    document.getElementById('prompt-state').value = 'active';
    
    modal.show();
}

/**
 * Create a new prompt
 */
async function createPrompt() {
    const title = document.getElementById('prompt-title').value.trim();
    const state = document.getElementById('prompt-state').value;
    
    if (!title) {
        showAlert('warning', 'Please enter a prompt title');
        return;
    }
    
    if (title.length > 80) {
        showAlert('warning', 'Prompt title must be 80 characters or less (currently ' + title.length + ' characters)');
        return;
    }
    
    const params = {
        title: title,
        state: state
    };
    
    const result = await executeAction('prompt', 'create', params);
    
    if (result.success) {
        showAlert('success', 'Prompt created successfully: ' + result.stdout.trim());
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('createPromptModal'));
        modal.hide();
        
        // Reload active prompt view
        await loadActivePrompt();
    } else {
        showAlert('danger', 'Failed to create prompt: ' + (result.error || result.stderr));
    }
}

/**
 * Show set state modal
 */
function showSetStateModal(promptId, currentState) {
    currentPromptId = promptId;
    
    const modal = new bootstrap.Modal(document.getElementById('setStateModal'));
    document.getElementById('set-state-prompt-id').textContent = promptId;
    document.getElementById('new-state').value = currentState;
    
    modal.show();
}

/**
 * Set prompt state
 */
async function setPromptState() {
    const newState = document.getElementById('new-state').value;
    
    const params = {
        'prompt-id': currentPromptId,
        'state': newState
    };
    
    const result = await executeAction('prompt', 'set_state', params);
    
    if (result.success) {
        showAlert('success', 'Prompt state updated successfully');
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('setStateModal'));
        modal.hide();
        
        // Reload active prompt view
        await loadActivePrompt();
    } else {
        showAlert('danger', 'Failed to set prompt state: ' + (result.error || result.stderr));
    }
}

/**
 * Load and display active prompt
 */
async function loadActivePrompt() {
    await loadRegistry();
    
    if (!currentRegistry || !currentRegistry.prompts) {
        showNoActivePrompt();
        return;
    }
    
    // Find active prompt
    const activePrompt = currentRegistry.prompts.find(p => p.state === 'active');
    
    if (!activePrompt) {
        showNoActivePrompt();
        return;
    }
    
    // Show active prompt content
    document.getElementById('no-active-prompt-message').style.display = 'none';
    document.getElementById('active-prompt-content').style.display = 'block';
    
    // Hide Archive Iteration button when active prompt exists
    const archiveBtn = document.getElementById('archive-iteration-btn');
    if (archiveBtn) {
        archiveBtn.style.display = 'none';
    }
    
    // Update title
    const promptId = activePrompt['prompt-id'];
    const title = activePrompt.title || activePrompt['prompt-title'] || '';
    document.getElementById('active-prompt-title').innerHTML = 
        `<span>Active Prompt: ${promptId}: ${escapeHtml(title)}</span>`;
    
    // Update iteration metadata in header
    updateIterationMetadata();
    
    // Update execution mode selector (button group) - always use registry value
    const currentMode = activePrompt['execution-mode'] || getSmartDefaultMode(activePrompt);
    previousExecutionMode = currentMode; // Initialize tracking
    const modeRadio = document.getElementById(`mode-${currentMode}`);
    if (modeRadio) {
        modeRadio.checked = true;
    }
    
    // Update complete button state
    const executed = activePrompt.executed || false;
    const completeBtn = document.getElementById('complete-prompt-btn');
    if (completeBtn) {
        completeBtn.disabled = !executed;
        completeBtn.title = executed ? 'Mark this prompt as completed' : 'Prompt must be executed first';
    }
    
    // Update add modification button state
    const implementationCompleted = activePrompt['implementation-completed'] || false;
    const addModificationBtn = document.getElementById('add-modification-btn');
    if (addModificationBtn) {
        addModificationBtn.disabled = !implementationCompleted;
        addModificationBtn.title = implementationCompleted ? 'Create a modification for small corrections' : 'Available after implementation completed';
    }
    
    // Update workflow status flags
    updateWorkflowFlags(activePrompt);
    
    // Update file button states based on workflow state
    updateFileButtonStates(activePrompt);
    
    // Load prompt files first - this sets currentPromptFolder needed by file views
    await loadActivePromptFiles(promptId);
    
    // NOW restore previous file view or default to Prompt
    // This happens after loadActivePromptFiles to ensure currentPromptFolder is set
    const savedFileView = StateManager.getFileView();
    if (savedFileView) {
        // Validate that the saved file view is available (button exists and is enabled)
        const fileButton = document.getElementById(`file-btn-${savedFileView}`);
        if (fileButton && !fileButton.disabled) {
            // Restore saved file view
            showFileView(savedFileView);
        } else {
            // Saved view not available, fall back to prompt
            showFileView('prompt');
        }
    } else {
        // No saved state, show default view
        showFileView('prompt');
    }
    
    // Load modifications if implementation is completed
    if (implementationCompleted) {
        await loadModifications();
    }
    
    // Re-initialize tooltips after content updates
    setupExecutionModeTooltips();
    setupStatusFlagTooltips();
    initializeTooltips();
}

/**
 * Show no active prompt message
 */
function showNoActivePrompt() {
    document.getElementById('no-active-prompt-message').style.display = 'block';
    document.getElementById('active-prompt-content').style.display = 'none';
    
    // Update iteration metadata even when no active prompt
    updateIterationMetadata();
    
    // Determine what buttons to show based on whether iteration exists
    const createIterationBtn = document.getElementById('create-iteration-btn-active');
    const createPromptBtn = document.getElementById('create-prompt-btn-active');
    const archiveBtn = document.getElementById('archive-iteration-btn');
    const messageText = document.getElementById('no-prompt-message-text');
    
    if (!currentRegistry) {
        // No iteration exists at all - show create iteration button only
        if (createIterationBtn) createIterationBtn.style.display = 'inline-block';
        if (createPromptBtn) createPromptBtn.style.display = 'none';
        if (archiveBtn) archiveBtn.style.display = 'none';
        if (messageText) messageText.textContent = 'No work iteration exists. Create one to get started.';
    } else {
        // Iteration exists but no active prompt - show create prompt and archive buttons
        if (createIterationBtn) createIterationBtn.style.display = 'none';
        if (createPromptBtn) createPromptBtn.style.display = 'inline-block';
        if (archiveBtn) archiveBtn.style.display = 'inline-block';
        if (messageText) messageText.textContent = 'No active prompt. Create a new prompt to continue working.';
    }
}

/**
 * Update iteration metadata display in Active Prompt header
 */
function updateIterationMetadata() {
    const metadataElement = document.getElementById('iteration-metadata');
    
    if (!metadataElement) {
        return;
    }
    
    if (!currentRegistry) {
        metadataElement.style.display = 'none';
        return;
    }
    
    const iterationId = currentRegistry['iteration-id'] || '';
    const iterationName = currentRegistry['iteration-name'] || '';
    
    if (iterationId && iterationName) {
        metadataElement.textContent = `Iteration: ${iterationName} (${iterationId})`;
        metadataElement.style.display = 'inline';
    } else {
        metadataElement.style.display = 'none';
    }
}

/**
 * Get smart default execution mode based on prompt state
 */
function getSmartDefaultMode(prompt) {
    const questionnaireGenerated = prompt['questionnaire-generated'] || false;
    const planGenerated = prompt['plan-generated'] || false;
    const implementationCompleted = prompt['implementation-completed'] || false;
    
    if (!questionnaireGenerated) {
        return 'clarify';
    } else if (!planGenerated) {
        return 'plan';
    } else if (!implementationCompleted) {
        return 'implement';
    } else {
        return 'no-action';
    }
}

/**
 * Update file button states for active prompt based on workflow state
 */
function updateFileButtonStates(prompt) {
    const questionnaireGenerated = prompt['questionnaire-generated'] || false;
    const planGenerated = prompt['plan-generated'] || false;
    const analysisGenerated = prompt['analysis-generated'] || false;
    const implementationCompleted = prompt['implementation-completed'] || false;
    const executed = prompt.executed || false;
    
    // Get file button elements
    const questionnaireBtn = document.getElementById('file-btn-questionnaire');
    const planBtn = document.getElementById('file-btn-plan');
    const analysisBtn = document.getElementById('file-btn-analysis');
    const implementationBtn = document.getElementById('file-btn-implementation');
    const modificationsBtn = document.getElementById('file-btn-modifications');
    
    // Get delete button elements
    const deleteQuestionnaireBtn = document.getElementById('delete-questionnaire-btn');
    const deletePlanBtn = document.getElementById('delete-plan-btn');
    const deleteAnalysisBtn = document.getElementById('delete-analysis-btn');
    
    // Prompt button: always enabled (no action needed)
    
    // Questionnaire button: enabled when questionnaire-generated=true
    if (questionnaireBtn) {
        questionnaireBtn.disabled = !questionnaireGenerated;
    }
    
    // Delete questionnaire button: enabled when questionnaire-generated=true
    if (deleteQuestionnaireBtn) {
        deleteQuestionnaireBtn.disabled = !questionnaireGenerated;
    }
    
    // Plan button: enabled when plan-generated=true
    if (planBtn) {
        planBtn.disabled = !planGenerated;
    }
    
    // Delete plan button: enabled when plan-generated=true
    if (deletePlanBtn) {
        deletePlanBtn.disabled = !planGenerated;
    }
    
    // Analysis button: enabled when analysis-generated=true
    if (analysisBtn) {
        analysisBtn.disabled = !analysisGenerated;
    }
    
    // Delete analysis button: enabled when analysis-generated=true
    if (deleteAnalysisBtn) {
        deleteAnalysisBtn.disabled = !analysisGenerated;
    }
    
    // Implementation button: enabled when implementation-completed=true
    if (implementationBtn) {
        implementationBtn.disabled = !implementationCompleted;
    }
    
    // Modifications button: enabled when executed=true
    if (modificationsBtn) {
        modificationsBtn.disabled = !executed;
    }
}

/**
 * Show specific file view and hide others
 */
function showFileView(fileType) {
    // Hide all file content views
    const allViews = document.querySelectorAll('.file-view-content');
    allViews.forEach(view => {
        view.style.display = 'none';
    });
    
    // Show selected view
    const targetView = document.getElementById(`content-${fileType}`);
    if (targetView) {
        targetView.style.display = 'block';
    }
    
    // Save current file view state
    StateManager.saveFileView(fileType);
    
    // Load content if needed
    if (fileType === 'questionnaire') {
        // Reload questionnaire to ensure it's current
        loadQuestionnaire();
    } else if (fileType === 'modifications') {
        // Reload modifications list
        loadModifications();
    }
}

/**
 * Update tab visibility for active prompt based on workflow state
 * @deprecated - Kept for backward compatibility but no longer used with new button-based UI
 */
function updateTabVisibility(prompt) {
    // This function is deprecated but kept for compatibility
    // The new UI uses updateFileButtonStates() instead
    updateFileButtonStates(prompt);
}

/**
 * Update workflow status flags for active prompt
 */
function updateWorkflowFlags(prompt) {
    // Helper function to update a flag icon with semantic icons
    function updateFlag(flagId, isActive, inactiveIcon, activeIcon) {
        const flagElement = document.getElementById(flagId);
        if (flagElement) {
            const icon = flagElement.querySelector('i');
            if (icon) {
                if (isActive) {
                    icon.className = activeIcon + ' text-success';
                } else {
                    icon.className = inactiveIcon + ' text-secondary';
                }
            }
        }
    }
    
    // Update boolean flags with semantic icons
    updateFlag('flag-questionnaire-generated', 
        prompt['questionnaire-generated'] || false,
        'bi bi-question-circle',
        'bi bi-question-circle-fill');
    updateFlag('flag-questionnaire-answered', 
        prompt['questionnaire-answered'] || false,
        'bi bi-clipboard-check',
        'bi bi-clipboard-check-fill');
    updateFlag('flag-plan-generated', 
        prompt['plan-generated'] || false,
        'bi bi-file-earmark-text',
        'bi bi-file-earmark-text-fill');
    updateFlag('flag-analysis-generated', 
        prompt['analysis-generated'] || false,
        'bi bi-clipboard-data',
        'bi bi-clipboard-data-fill');
    updateFlag('flag-implementation-completed', 
        prompt['implementation-completed'] || false,
        'bi bi-file-code',
        'bi bi-file-code-fill');
    updateFlag('flag-executed', 
        prompt.executed || false,
        'bi bi-patch-check',
        'bi bi-patch-check-fill');
    
    // Update modifications count (only show when > 0)
    const modificationsCount = prompt['modifications-count'] || 0;
    const modificationsCountElement = document.getElementById('flag-modifications-count');
    const modificationsCountValue = document.getElementById('modifications-count-value');
    if (modificationsCountElement && modificationsCountValue) {
        if (modificationsCount > 0) {
            modificationsCountValue.textContent = modificationsCount;
            modificationsCountElement.style.display = 'inline';
        } else {
            modificationsCountElement.style.display = 'none';
        }
    }
    
    // Update current modification ID (only show when not null)
    const currentModificationId = prompt['current-modification-id'];
    const currentModificationElement = document.getElementById('flag-current-modification');
    const currentModificationValue = document.getElementById('current-modification-value');
    if (currentModificationElement && currentModificationValue) {
        if (currentModificationId !== null && currentModificationId !== undefined) {
            // Format with leading zeros (e.g., "001", "023")
            const formattedId = String(currentModificationId).padStart(3, '0');
            currentModificationValue.textContent = formattedId;
            currentModificationElement.style.display = 'inline';
        } else {
            currentModificationElement.style.display = 'none';
        }
    }
    
    // Re-initialize Bootstrap tooltips for the flag elements
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('.flag-icon[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        // Dispose existing tooltip instance if present to avoid multiple instances
        const existing = bootstrap.Tooltip.getInstance(tooltipTriggerEl);
        if (existing) {
            try { existing.dispose(); } catch (e) { /* ignore dispose errors */ }
        }
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// --- Active Prompt Background Refresh ---
let activePromptRefreshIntervalId = null;
let previousExecutionMode = null; // Track previous mode to detect changes

function isUserInteractingWithActivePrompt() {
    // If any modal is open, consider user interacting
    if (document.querySelector('.modal.show')) return true;

    // If any element inside active-prompt-content is focused (e.g., typing), suppress updates
    const activeContainer = document.getElementById('active-prompt-content');
    if (!activeContainer) return false;
    const activeEl = document.activeElement;
    if (!activeEl) return false;
    return activeContainer.contains(activeEl);
}

async function refreshActivePromptStatuses() {
    try {
        if (isUserInteractingWithActivePrompt()) return; // partial suppression per questionnaire

        const response = await fetch('/api/registry');
        const result = await response.json();

        if (!result || !result.success) return;

        const registry = result.data;
        if (!registry || !registry.prompts) return;

        const activePrompt = registry.prompts.find(p => p.state === 'active');
        if (!activePrompt) return;

        // Update flags (only updates the DOM for flags)
        updateWorkflowFlags(activePrompt);

        // Update file button states (view and delete buttons) in real-time
        updateFileButtonStates(activePrompt);

        // Update execution-mode radio/buttons only if value changed (hybrid approach per Q2-C)
        const currentMode = activePrompt['execution-mode'] || getSmartDefaultMode(activePrompt);
        if (currentMode !== previousExecutionMode) {
            previousExecutionMode = currentMode;
            
            // Try to set radio by id convention `mode-<mode>`
            const modeRadio = document.getElementById(`mode-${currentMode}`);
            if (modeRadio) {
                modeRadio.checked = true;
            } else {
                // Fallback: set inputs named execution-mode if present
                const radios = document.querySelectorAll('input[name="execution-mode"]');
                radios.forEach(r => r.checked = (r.id === `mode-${currentMode}` || r.value === currentMode));
            }
        }

        // Update complete button enabled state silently
        const executed = activePrompt.executed || false;
        const completeBtn = document.getElementById('complete-prompt-btn');
        if (completeBtn) {
            completeBtn.disabled = !executed;
            completeBtn.title = executed ? 'Mark this prompt as completed' : 'Prompt must be executed first';
        }
    } catch (err) {
        console.warn('Active prompt refresh failed:', err);
    }
}

function startActivePromptRefresh() {
    // Fixed 2s interval per questionnaire selection
    if (activePromptRefreshIntervalId) {
        clearInterval(activePromptRefreshIntervalId);
    }
    // Run immediately once, then every 2s
    refreshActivePromptStatuses();
    activePromptRefreshIntervalId = setInterval(refreshActivePromptStatuses, 2000);
}


/**
 * Update execution mode for active prompt
 */
async function updateExecutionMode(mode) {
    try {
        const response = await fetch('/api/action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                domain: 'prompt',
                action: 'set_execution_mode',
                params: {
                    mode: mode
                }
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Silent success - visual feedback from button state is sufficient
            await loadRegistry();
        } else {
            showAlert('danger', 'Failed to update execution mode: ' + (result.error || result.stderr));
        }
    } catch (error) {
        showAlert('danger', 'Failed to update execution mode: ' + error.message);
    }
}

/**
 * Delete execution mode file with confirmation dialog
 * @param {string} executionType - One of: 'questionnaire', 'analysis', 'plan'
 */
async function deleteExecutionModeFile(executionType) {
    // Map execution type to user-friendly names and script names
    const fileConfig = {
        'questionnaire': {
            displayName: 'Questionnaire',
            scriptAction: 'questionnaire_delete'
        },
        'analysis': {
            displayName: 'Analysis',
            scriptAction: 'analysis_delete'
        },
        'plan': {
            displayName: 'Plan',
            scriptAction: 'plan_delete'
        }
    };
    
    const config = fileConfig[executionType];
    if (!config) {
        showAlert('danger', `Invalid execution type: ${executionType}`);
        return;
    }
    
    // Show confirmation dialog
    const confirmMessage = `Are you sure you want to delete the ${config.displayName} file? This will reset the status as if the execution mode was never executed.`;
    
    if (!confirm(confirmMessage)) {
        return; // User cancelled
    }
    
    try {
        // Call the backend script to delete the file and reset flags
        const response = await fetch('/api/action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                domain: 'prompt',
                action: config.scriptAction,
                params: {}
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', `${config.displayName} file deleted successfully`);
            
            // Reload the registry to update UI state
            await loadRegistry();
            
            // If the deleted file was currently displayed, switch to prompt view
            const currentView = StateManager.getFileView();
            if (currentView === executionType) {
                showFileView('prompt');
            }
        } else {
            const errorMsg = result.error || result.stderr || 'Unknown error';
            showAlert('danger', `Failed to delete ${config.displayName} file: ${errorMsg}`);
        }
    } catch (error) {
        showAlert('danger', `Failed to delete ${config.displayName} file: ${error.message}`);
    }
}

/**
 * Load files for active prompt
 */
async function loadActivePromptFiles(promptId) {
    currentEditingPrompt = promptId;
    
    // Find the prompt folder
    try {
        const folderName = promptId + '_' + getFolderSuffix(promptId);
        currentPromptFolder = `workdir/${folderName}`;
        
        // Load all files
        await Promise.all([
            loadActivePromptFile('prompt.md'),
            loadActivePromptFile('plan.md'),
            loadActivePromptFile('analysis.md'),
            loadQuestionnaire(),
            loadActivePromptFile('implementation.md')
        ]);
        
        // Initialize snippet autocomplete for the prompt editor
        if (typeof initializeSnippetAutocomplete === 'function') {
            initializeSnippetAutocomplete();
        }
        
        // Setup auto-save for prompt.md
        setupPromptAutoSave();
    } catch (error) {
        console.error('Error loading prompt files:', error);
        showAlert('warning', 'Some prompt files could not be loaded');
    }
}

/**
 * Load a single file for active prompt
 */
async function loadActivePromptFile(filename) {
    const textareaId = `active-editor-${filename.replace('.md', '-md')}`;
    const textarea = document.getElementById(textareaId);
    
    if (!textarea) {
        console.warn(`Textarea not found for ${filename}`);
        return;
    }
    
    try {
        const filepath = `${currentPromptFolder}/${filename}`;
        const response = await fetch('/api/file/' + filepath + '?token=' + sessionToken);
        const result = await response.json();
        
        if (result.success) {
            textarea.value = result.content || '';
        } else {
            textarea.value = `# File not found\n\nThis file does not exist yet.`;
        }
    } catch (error) {
        console.error(`Error loading ${filename}:`, error);
        textarea.value = `# Error\n\nFailed to load file: ${error.message}`;
    }
}

/**
 * Save file for active prompt
 */
async function saveActivePromptFile(filename) {
    const textareaId = `active-editor-${filename.replace('.md', '-md')}`;
    const textarea = document.getElementById(textareaId);
    
    if (!textarea) {
        showAlert('danger', 'Textarea not found');
        return;
    }
    
    const content = textarea.value;
    
    // Validate snippet keys if saving prompt.md
    if (filename === 'prompt.md' && typeof snippetService !== 'undefined') {
        try {
            await snippetService.loadSnippets();
            const invalidKeys = snippetService.validateSnippetKeys(content);
            
            if (invalidKeys.length > 0) {
                const proceed = await showSnippetValidationDialog(invalidKeys);
                if (!proceed) {
                    return; // User chose to cancel save
                }
            }
        } catch (error) {
            console.warn('Snippet validation failed:', error);
            // Continue with save even if validation fails
        }
    }
    
    try {
        const filepath = `${currentPromptFolder}/${filename}`;
        const response = await fetch('/api/file/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                filepath: filepath,
                content: content
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', `${filename} saved successfully`);
        } else {
            showAlert('danger', `Failed to save ${filename}: ` + (result.error || 'Unknown error'));
        }
    } catch (error) {
        showAlert('danger', `Failed to save ${filename}: ` + error.message);
    }
}

/**
 * Auto-save state management
 */
let promptAutoSaveTimeout = null;
let promptSaveInProgress = false;
let promptLastSaveHash = null;
let promptValidationCache = { valid: true, invalidKeys: [] };

/**
 * Setup auto-save for prompt.md textarea
 */
function setupPromptAutoSave() {
    const textarea = document.getElementById('active-editor-prompt-md');
    if (!textarea) {
        console.warn('Prompt textarea not found for auto-save setup');
        return;
    }
    
    // Clear any existing listeners by cloning the element
    const newTextarea = textarea.cloneNode(true);
    textarea.parentNode.replaceChild(newTextarea, textarea);
    
    // Add input event for debounced auto-save
    newTextarea.addEventListener('input', function() {
        updatePromptSaveStatus('typing');
        triggerPromptAutoSave();
    });
    
    // Add blur event for immediate save on focus loss
    newTextarea.addEventListener('blur', function() {
        triggerPromptAutoSave(true); // Immediate save on blur
    });
    
    // Initialize save status
    updatePromptSaveStatus('saved');
    
    // Store initial content hash
    promptLastSaveHash = hashString(newTextarea.value);
}

/**
 * Trigger auto-save with debouncing
 */
function triggerPromptAutoSave(immediate = false) {
    // Clear existing timeout
    if (promptAutoSaveTimeout) {
        clearTimeout(promptAutoSaveTimeout);
        promptAutoSaveTimeout = null;
    }
    
    // If immediate, save right away
    if (immediate) {
        performPromptAutoSave();
    } else {
        // Debounce: wait 2 seconds after last keystroke
        promptAutoSaveTimeout = setTimeout(() => {
            performPromptAutoSave();
        }, 2000);
    }
}

/**
 * Perform the actual auto-save operation
 */
async function performPromptAutoSave() {
    if (promptSaveInProgress) {
        console.log('Save already in progress, skipping...');
        return;
    }
    
    const textarea = document.getElementById('active-editor-prompt-md');
    if (!textarea) {
        return;
    }
    
    const content = textarea.value;
    const contentHash = hashString(content);
    
    // Skip save if content hasn't changed
    if (contentHash === promptLastSaveHash) {
        console.log('Content unchanged, skipping save');
        return;
    }
    
    promptSaveInProgress = true;
    updatePromptSaveStatus('saving');
    
    try {
        // Run async validation (non-blocking)
        if (typeof snippetService !== 'undefined') {
            try {
                await snippetService.loadSnippets();
                const invalidKeys = snippetService.validateSnippetKeys(content);
                promptValidationCache = {
                    valid: invalidKeys.length === 0,
                    invalidKeys: invalidKeys
                };
            } catch (error) {
                console.warn('Snippet validation failed:', error);
                promptValidationCache = { valid: true, invalidKeys: [] };
            }
        }
        
        // Perform the save
        const filepath = `${currentPromptFolder}/prompt.md`;
        const response = await fetch('/api/file/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                filepath: filepath,
                content: content
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            promptLastSaveHash = contentHash;
            updatePromptSaveStatus('saved');
        } else {
            updatePromptSaveStatus('error', result.error || 'Unknown error');
        }
    } catch (error) {
        console.error('Auto-save failed:', error);
        updatePromptSaveStatus('error', error.message);
    } finally {
        promptSaveInProgress = false;
    }
}

/**
 * Update the save status indicator
 */
function updatePromptSaveStatus(status, errorMessage = '') {
    const statusElement = document.getElementById('prompt-save-status');
    if (!statusElement) {
        console.warn('Save status element not found');
        return;
    }
    
    const validationInfo = !promptValidationCache.valid 
        ? ` (${promptValidationCache.invalidKeys.length} invalid snippet${promptValidationCache.invalidKeys.length > 1 ? 's' : ''})`
        : '';
    
    switch (status) {
        case 'typing':
            statusElement.innerHTML = '<span class="text-muted"><i class="bi bi-pencil"></i> Editing...</span>';
            break;
        case 'saving':
            statusElement.innerHTML = '<span class="text-primary"><i class="bi bi-arrow-repeat spin"></i> Saving...</span>';
            break;
        case 'saved':
            if (promptValidationCache.valid) {
                statusElement.innerHTML = '<span class="text-success"><i class="bi bi-check-circle"></i> Saved</span>';
            } else {
                statusElement.innerHTML = `<span class="text-warning"><i class="bi bi-exclamation-triangle"></i> Saved${validationInfo}</span>`;
            }
            break;
        case 'error':
            statusElement.innerHTML = `<span class="text-danger"><i class="bi bi-x-circle"></i> Error: ${errorMessage} <a href="#" onclick="retryPromptSave(); return false;" class="text-decoration-underline">Retry</a></span>`;
            break;
    }
}

/**
 * Retry save on error
 */
function retryPromptSave() {
    performPromptAutoSave();
}

/**
 * Simple string hash function for change detection
 */
function hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32-bit integer
    }
    return hash;
}

/**
 * Load questionnaire (tries JSON first, then MD for legacy support)
 */
async function loadQuestionnaire() {
    const container = document.getElementById('questionnaire-container');
    
    if (!container) {
        console.warn('Questionnaire container not found');
        return;
    }
    
    try {
        // Try to load questionnaire.json first
        const jsonPath = `${currentPromptFolder}/questionnaire.json`;
        const jsonResponse = await fetch('/api/file/' + jsonPath + '?token=' + sessionToken);
        const jsonResult = await jsonResponse.json();
        
        if (jsonResult.success && jsonResult.data) {
            // Render JSON questionnaire (data is already parsed)
            renderQuestionnaireForm(jsonResult.data, jsonPath);
            
            // Update questionnaire-generated flag in registry
            await updateQuestionnaireGeneratedFlag(true);
            
            // Check if all questions are answered and update questionnaire-answered flag
            const allAnswered = jsonResult.data.questions.every(q => q['user-selection'] && q['user-selection'].type);
            await updateQuestionnaireAnsweredFlag(allAnswered);
            
            return;
        }
    } catch (error) {
        console.log('questionnaire.json not found or invalid, trying .md');
    }
    
    // Fall back to questionnaire.md (legacy)
    try {
        const mdPath = `${currentPromptFolder}/questionnaire.md`;
        const mdResponse = await fetch('/api/file/' + mdPath + '?token=' + sessionToken);
        const mdResult = await mdResponse.json();
        
        if (mdResult.success) {
            renderQuestionnaireLegacy(mdResult.content || '');
        } else {
            renderQuestionnaireNotFound();
        }
    } catch (error) {
        console.error('Error loading questionnaire:', error);
        renderQuestionnaireNotFound();
    }
}

/**
 * Render questionnaire form from JSON data
 */
function renderQuestionnaireForm(data, filepath) {
    const container = document.getElementById('questionnaire-container');
    
    if (!data.questions || data.questions.length === 0) {
        container.innerHTML = '<p class="text-muted">No questions available.</p>';
        return;
    }
    
    // Calculate completion stats
    const totalQuestions = data.questions.length;
    const answeredQuestions = data.questions.filter(q => q['user-selection'] && q['user-selection'].type).length;
    const completionPercent = Math.round((answeredQuestions / totalQuestions) * 100);
    
    // Find the first unanswered question to show by default
    let indexToShow = data.questions.findIndex(q => !(q['user-selection'] && q['user-selection'].type));
    if (indexToShow === -1) indexToShow = 0; // If all answered, show first
    
    let html = `
        <div class="row">
            <!-- Left Column: Context and Navigation -->
            <div class="col-md-4">
                <!-- Context section -->
                ${data.context ? `
                <div class="alert alert-info mb-3 py-2">
                    <h6 class="alert-heading mb-1"><i class="bi bi-info-circle"></i> Context</h6>
                    <p class="mb-0 small">${escapeHtml(data.context)}</p>
                </div>
                ` : ''}
                
                <!-- Progress -->
                <div class="mb-2">
                    <h6>Progress</h6>
                    <div class="progress mb-2" style="height: 20px;">
                        <div class="progress-bar ${completionPercent === 100 ? 'bg-success' : 'bg-warning'}" 
                             role="progressbar" style="width: ${completionPercent}%" 
                             aria-valuenow="${completionPercent}" aria-valuemin="0" aria-valuemax="100">
                            ${answeredQuestions}/${totalQuestions}
                        </div>
                    </div>
                </div>
                
                <!-- Question Navigation -->
                <div class="list-group" id="questionNavigation">
    `;
    
    data.questions.forEach((question, index) => {
        const questionId = question.id || `Q${index + 1}`;
        const isAnswered = question['user-selection'] && question['user-selection'].type;
        const isActive = index === indexToShow;
        
        html += `
            <a href="#" class="list-group-item list-group-item-action ${isActive ? 'active' : ''}" 
               data-question-index="${index}" data-question-id="${questionId}"
               onclick="showQuestion(event, ${index}, '${filepath}')">
                <div class="d-flex justify-content-between align-items-center">
                    <span class="small"><strong>${questionId}</strong></span>
                    ${isAnswered ? '<i class="bi bi-check-circle text-success"></i>' : '<i class="bi bi-clock text-warning"></i>'}
                </div>
                <div class="small text-truncate">${escapeHtml(question['question-text'] || '').substring(0, 50)}...</div>
            </a>
        `;
    });
    
    html += `
                </div>
            </div>
            
            <!-- Right Column: Current Question Details -->
            <div class="col-md-8">
                <div id="currentQuestionContainer">
                    ${renderQuestionDetail(data.questions[indexToShow], data.questions[indexToShow].id || `Q${indexToShow + 1}`, filepath)}
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
    
    // Store data globally for showQuestion function
    window.currentQuestionnaireData = data;
    window.currentQuestionnairePath = filepath;
}

/**
 * Show a specific question in the right panel
 */
function showQuestion(event, index, filepath) {
    event.preventDefault();
    
    const data = window.currentQuestionnaireData;
    if (!data || !data.questions || !data.questions[index]) return;
    
    const question = data.questions[index];
    const questionId = question.id || `Q${index + 1}`;
    
    // Update navigation active state
    document.querySelectorAll('#questionNavigation .list-group-item').forEach((item, i) => {
        if (i === index) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
    
    // Update question detail panel
    document.getElementById('currentQuestionContainer').innerHTML = 
        renderQuestionDetail(question, questionId, filepath);
}

/**
 * Render a single question detail with options
 */
function renderQuestionDetail(question, questionId, filepath) {
    let html = `
        <div class="question-title-sticky">
            <h5 class="mb-3"><strong>${questionId}:</strong> ${escapeHtml(question['question-text'] || '')}</h5>
        </div>
        <div class="question-content">
    `;
    
    // Recommendation alert - more compact
    if (question['recommended-option'] && question['recommendation-rationale']) {
        html += `
            <div class="alert alert-success py-2 mb-2" role="alert">
                <h6 class="alert-heading mb-1"><i class="bi bi-star-fill"></i> Recommended: Option ${question['recommended-option']}</h6>
                <p class="mb-0 small">${escapeHtml(question['recommendation-rationale'])}</p>
            </div>
        `;
    }
    
    // Options as radio buttons
    if (question.options && question.options.length > 0) {
        const userSelection = question['user-selection'] || { type: null, value: null };
        
        question.options.forEach(option => {
            const optionId = option.id || '';
            const isSelected = userSelection.type === 'predefined' && userSelection.value === optionId;
            const inputId = `${questionId}-option-${optionId}`;
            
            html += `
                <div class="form-check mb-2">
                    <input class="form-check-input" type="radio" name="${questionId}-options" 
                           id="${inputId}" value="${optionId}" ${isSelected ? 'checked' : ''}
                           onchange="saveQuestionnaireAnswer('${questionId}', 'predefined', '${optionId}', '${filepath}')">
                    <label class="form-check-label fw-bold" for="${inputId}">
                        ${optionId}. ${escapeHtml(option.label || '')}
                    </label>
                </div>
            `;
            
            // Pros and cons in a compact card
            if (option.pros || option.cons) {
                html += `
                    <div class="card mb-2 ms-4">
                        <div class="card-body py-2 px-3">
                            ${option.pros ? `
                                <div class="mb-1">
                                    <strong class="text-success small"><i class="bi bi-plus-circle"></i> Pros:</strong>
                                    <span class="ms-1 small">${escapeHtml(option.pros)}</span>
                                </div>
                            ` : ''}
                            ${option.cons ? `
                                <div class="${option.pros ? '' : 'mb-0'}">
                                    <strong class="text-danger small"><i class="bi bi-dash-circle"></i> Cons:</strong>
                                    <span class="ms-1 small">${escapeHtml(option.cons)}</span>
                                </div>
                            ` : ''}
                        </div>
                    </div>
                `;
            }
        });
    }
    
    // Custom answer field - more compact
    const userSelection = question['user-selection'] || { type: null, value: null };
    const customText = userSelection.type === 'custom' ? userSelection.value : '';
    
    html += `
        <div class="mt-2">
            <label class="form-label fw-bold small">Custom answer (if none of the above options fit):</label>
            <textarea class="form-control form-control-sm" id="${questionId}-custom-answer" rows="2" 
                      placeholder="Enter your custom answer here...">${escapeHtml(customText)}</textarea>
            <button class="btn btn-sm btn-primary mt-1" 
                    onclick="saveQuestionnaireCustomAnswer('${questionId}', '${filepath}')">
                <i class="bi bi-save"></i> Save Custom Answer
            </button>
        </div>
    </div>`;
    
    return html;
}

/**
 * Save questionnaire answer (predefined option)
 */
async function saveQuestionnaireAnswer(questionId, type, value, filepath) {
    try {
        // Load current questionnaire data
        const response = await fetch('/api/file/' + filepath + '?token=' + sessionToken);
        const result = await response.json();
        
        if (!result.success) {
            showAlert('danger', 'Failed to load questionnaire data');
            return;
        }
        
        // For JSON files, server returns parsed data in result.data
        const data = result.data;
        
        // Update the specific question's user-selection
        const question = data.questions.find(q => q.id === questionId);
        if (question) {
            question['user-selection'] = { type, value };
            
            // Save back to file
            const saveResponse = await fetch('/api/file/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    token: sessionToken,
                    filepath: filepath,
                    content: JSON.stringify(data, null, 2)
                })
            });
            
            const saveResult = await saveResponse.json();
            
            if (saveResult.success) {
                // Call validation script to check if all questions are answered
                await checkQuestionnaireComplete();
                
                // Update UI to show saved state
                showAlert('success', `Answer saved for ${questionId}`, 2000);
                // Reload questionnaire to update stats
                await loadQuestionnaire();
                // Reload active prompt to update badges
                await loadActivePrompt();
            } else {
                showAlert('danger', 'Failed to save answer: ' + (saveResult.error || 'Unknown error'));
            }
        }
    } catch (error) {
        console.error('Error saving answer:', error);
        showAlert('danger', 'Failed to save answer: ' + error.message);
    }
}

/**
 * Save questionnaire custom answer
 */
async function saveQuestionnaireCustomAnswer(questionId, filepath) {
    const textarea = document.getElementById(`${questionId}-custom-answer`);
    if (!textarea) return;
    
    const customText = textarea.value.trim();
    
    if (!customText) {
        showAlert('warning', 'Please enter a custom answer');
        return;
    }
    
    await saveQuestionnaireAnswer(questionId, 'custom', customText, filepath);
}

/**
 * Update questionnaire-generated flag in registry
 */
async function updateQuestionnaireGeneratedFlag(value) {
    try {
        const response = await fetch('/api/action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                domain: 'prompt',
                action: value ? 'questionnaire_generated_on' : 'questionnaire_generated_off',
                params: {}
            })
        });
        
        const result = await response.json();
        if (!result.success) {
            console.error('Failed to update questionnaire-generated flag:', result.error);
        }
    } catch (error) {
        console.error('Error updating questionnaire-generated flag:', error);
    }
}

/**
 * Check questionnaire completion and update flag via validation script
 */
async function checkQuestionnaireComplete() {
    try {
        const response = await fetch('/api/action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                domain: 'questionnaire',
                action: 'check_complete',
                params: {}
            })
        });
        
        const result = await response.json();
        if (!result.success) {
            console.error('Failed to check questionnaire completion:', result.error);
        }
    } catch (error) {
        console.error('Error checking questionnaire completion:', error);
    }
}

/**
 * Update questionnaire-answered flag in registry
 */
async function updateQuestionnaireAnsweredFlag(value) {
    try {
        const response = await fetch('/api/action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                domain: 'prompt',
                action: value ? 'questionnaire_answered_on' : 'questionnaire_answered_off',
                params: {}
            })
        });
        
        const result = await response.json();
        if (!result.success) {
            console.error('Failed to update questionnaire-answered flag:', result.error);
        }
    } catch (error) {
        console.error('Error updating questionnaire-answered flag:', error);
    }
}

/**
 * Render legacy markdown questionnaire (read-only)
 */
function renderQuestionnaireLegacy(content) {
    const container = document.getElementById('questionnaire-container');
    container.innerHTML = `
        <div class="alert alert-warning mb-3">
            <i class="bi bi-info-circle"></i> This is a legacy markdown questionnaire (read-only).
            New questionnaires use an interactive JSON format.
        </div>
        <div class="mb-3">
            <label class="form-label fw-bold">questionnaire.md</label>
            <textarea class="form-control font-monospace" rows="20" style="font-size: 14px;" readonly>${escapeHtml(content)}</textarea>
        </div>
    `;
}

/**
 * Render not found message
 */
function renderQuestionnaireNotFound() {
    const container = document.getElementById('questionnaire-container');
    container.innerHTML = `
        <div class="alert alert-info">
            <i class="bi bi-info-circle"></i> No questionnaire file found.
            Run analyze mode to generate questions.
        </div>
    `;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * View completed prompt (opens modal with read-only view)
 */
async function viewCompletedPrompt(promptId) {
    // Find prompt details from registry
    await loadRegistry();
    const prompt = currentRegistry.prompts.find(p => p['prompt-id'] === promptId);
    
    if (!prompt) {
        showAlert('danger', 'Prompt not found: ' + promptId);
        return;
    }
    
    const title = prompt.title || prompt['prompt-title'] || '';
    const promptFolder = `workdir/${promptId}_${title}`;
    
    // Update modal title
    document.getElementById('view-completed-prompt-title').textContent = 
        `View Prompt: ${promptId} - ${title}`;
    
    // Load all files into the modal
    const files = ['prompt.md', 'plan.md', 'questionnaire.md', 'implementation.md'];
    
    for (const file of files) {
        const filepath = `${promptFolder}/${file}`;
        const elementId = `view-editor-${file.replace('.', '-')}`;
        
        try {
            const encodedFilepath = encodeURIComponent(filepath);
            const response = await fetch('/api/file/' + encodedFilepath + '?token=' + sessionToken);
            const result = await response.json();
            
            const textarea = document.getElementById(elementId);
            if (textarea) {
                if (result.success) {
                    textarea.value = result.content || '';
                } else {
                    textarea.value = '';
                }
            }
        } catch (error) {
            console.error(`Error loading ${file}:`, error);
            const textarea = document.getElementById(elementId);
            if (textarea) {
                textarea.value = '';
            }
        }
    }
    
    // Load modifications if any
    await loadCompletedPromptModifications(promptId, promptFolder);
    
    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('viewCompletedPromptModal'));
    modal.show();
}

/**
 * Load modifications for a completed prompt
 */
async function loadCompletedPromptModifications(promptId, promptFolder) {
    const container = document.getElementById('view-modifications-list-container');
    
    await loadRegistry();
    const prompt = currentRegistry.prompts.find(p => p['prompt-id'] === promptId);
    
    if (!prompt) {
        container.innerHTML = '<p class="text-muted">No modifications.</p>';
        return;
    }
    
    const modificationsCount = prompt['modifications-count'] || 0;
    
    if (modificationsCount === 0) {
        container.innerHTML = '<p class="text-muted">No modifications.</p>';
        return;
    }
    
    let html = '<div class="list-group">';
    
    for (let i = 1; i <= modificationsCount; i++) {
        const modFile = `modification-${i}.md`;
        const modImplFile = `modification-${i}-implementation.md`;
        const filepath = `${promptFolder}/${modFile}`;
        
        try {
            const encodedFilepath = encodeURIComponent(filepath);
            const response = await fetch('/api/file/' + encodedFilepath + '?token=' + sessionToken);
            const result = await response.json();
            
            const content = result.success ? (result.content || 'No content') : 'File not found';
            const preview = content.substring(0, 200) + (content.length > 200 ? '...' : '');
            
            html += `
                <div class="list-group-item">
                    <h6 class="mb-1">Modification ${i}</h6>
                    <p class="mb-1 font-monospace small">${escapeHtml(preview)}</p>
                    <button class="btn btn-sm btn-outline-primary mt-2" 
                            onclick="viewModificationDetails('${promptFolder}', ${i})">
                        <i class="bi bi-eye"></i> View Details
                    </button>
                </div>
            `;
        } catch (error) {
            console.error(`Error loading modification ${i}:`, error);
        }
    }
    
    html += '</div>';
    container.innerHTML = html;
}

/**
 * View modification details (can be enhanced with a sub-modal if needed)
 */
async function viewModificationDetails(promptFolder, modId) {
    const modFile = `modification-${modId}.md`;
    const modImplFile = `modification-${modId}-implementation.md`;
    
    let details = `=== Modification ${modId} ===\n\n`;
    
    // Load modification description
    try {
        const filepath = `${promptFolder}/${modFile}`;
        const encodedFilepath = encodeURIComponent(filepath);
        const response = await fetch('/api/file/' + encodedFilepath + '?token=' + sessionToken);
        const result = await response.json();
        
        if (result.success) {
            details += `Description:\n${result.content}\n\n`;
        }
    } catch (error) {
        details += `Description: Error loading\n\n`;
    }
    
    // Load modification implementation
    try {
        const filepath = `${promptFolder}/${modImplFile}`;
        const encodedFilepath = encodeURIComponent(filepath);
        const response = await fetch('/api/file/' + encodedFilepath + '?token=' + sessionToken);
        const result = await response.json();
        
        if (result.success) {
            details += `Implementation:\n${result.content}\n`;
        }
    } catch (error) {
        details += `Implementation: Error loading\n`;
    }
    
    // Show in alert (can be enhanced with a better modal)
    alert(details);
}

/**
 * Get folder suffix from prompt in registry
 */
function getFolderSuffix(promptId) {
    if (!currentRegistry || !currentRegistry.prompts) {
        return '';
    }
    
    const prompt = currentRegistry.prompts.find(p => p['prompt-id'] === promptId);
    if (!prompt) {
        return '';
    }
    
    return prompt.title || prompt['prompt-title'] || '';
}

/**
 * Copy execute command text to clipboard
 */
async function copyExecuteCommand() {
    const textToCopy = "Follow the instructions in file `.rdd/prompt-snippets/execution.md`";
    const button = document.getElementById('copy-execute-cmd-btn');
    
    if (!button) {
        return;
    }
    
    try {
        // Copy to clipboard using the Clipboard API
        await navigator.clipboard.writeText(textToCopy);
        
        // Store original button content
        const originalHTML = button.innerHTML;
        
        // Change button to show "Copied!" with checkmark
        button.innerHTML = '<i class="bi bi-check-lg"></i> Copied!';
        button.disabled = true;
        
        // Revert button back to original after 2 seconds
        setTimeout(() => {
            button.innerHTML = originalHTML;
            button.disabled = false;
        }, 2000);
        
    } catch (error) {
        showAlert('danger', 'Failed to copy to clipboard: ' + error.message);
    }
}

/**
 * Complete the active prompt
 */
async function completeActivePrompt() {
    if (!currentRegistry || !currentRegistry.prompts) {
        showAlert('danger', 'No registry loaded');
        return;
    }
    
    const activePrompt = currentRegistry.prompts.find(p => p.state === 'active');
    if (!activePrompt) {
        showAlert('danger', 'No active prompt found');
        return;
    }
    
    const promptId = activePrompt['prompt-id'];
    
    if (!activePrompt.executed) {
        showAlert('warning', 'Prompt must be executed before it can be completed');
        return;
    }
    
    if (!confirm(`Are you sure you want to complete prompt ${promptId}?`)) {
        return;
    }
    
    const params = {
        'prompt-id': promptId
    };
    
    const result = await executeAction('prompt', 'complete', params);
    
    if (result.success) {
        showAlert('success', `Prompt ${promptId} completed successfully`);
        
        // Reload active prompt view
        await loadActivePrompt();
    } else {
        showAlert('danger', `Failed to complete prompt: ` + (result.error || result.stderr));
    }
}

/**
 * Toggle analyze mode for a prompt
 */
async function toggleAnalyzeMode(promptId, enabled) {
    const action = enabled ? 'analyze_on' : 'analyze_off';
    const params = {
        'prompt-id': promptId
    };
    
    const result = await executeAction('prompt', action, params);
    
    if (result.success) {
        showAlert('success', `Analyze mode ${enabled ? 'enabled' : 'disabled'} for prompt ${promptId}`);
        
        // Update the label next to the toggle
        const toggleId = `analyze-toggle-${promptId}`;
        const toggleElement = document.getElementById(toggleId);
        if (toggleElement) {
            const label = toggleElement.nextElementSibling;
            if (label) {
                label.textContent = enabled ? 'ON' : 'OFF';
            }
        }
        
        // Reload registry to ensure consistency
        await loadRegistry();
    } else {
        showAlert('danger', `Failed to ${enabled ? 'enable' : 'disable'} analyze mode: ` + (result.error || result.stderr));
        
        // Revert the toggle state
        const toggleId = `analyze-toggle-${promptId}`;
        const toggleElement = document.getElementById(toggleId);
        if (toggleElement) {
            toggleElement.checked = !enabled;
        }
    }
}

/**
 * Toggle plan mode for a prompt
 */
async function togglePlanMode(promptId, enabled) {
    const action = enabled ? 'plan_on' : 'plan_off';
    const params = {
        'prompt-id': promptId
    };
    
    const result = await executeAction('prompt', action, params);
    
    if (result.success) {
        showAlert('success', `Plan mode ${enabled ? 'enabled' : 'disabled'} for prompt ${promptId}`);
        
        // Update the label next to the toggle
        const toggleId = `plan-toggle-${promptId}`;
        const toggleElement = document.getElementById(toggleId);
        if (toggleElement) {
            const label = toggleElement.nextElementSibling;
            if (label) {
                label.textContent = enabled ? 'ON' : 'OFF';
            }
        }
        
        // Reload registry to ensure consistency (this will also update analyze toggle if it was auto-disabled)
        await loadRegistry();
    } else {
        showAlert('danger', `Failed to ${enabled ? 'enable' : 'disable'} plan mode: ` + (result.error || result.stderr));
        
        // Revert the toggle state
        const toggleId = `plan-toggle-${promptId}`;
        const toggleElement = document.getElementById(toggleId);
        if (toggleElement) {
            toggleElement.checked = !enabled;
        }
    }
}

/**
 * Complete a prompt
 */
async function completePrompt(promptId) {
    if (!confirm(`Are you sure you want to complete prompt ${promptId}?`)) {
        return;
    }
    
    const params = {
        'prompt-id': promptId
    };
    
    const result = await executeAction('prompt', 'complete', params);
    
    if (result.success) {
        showAlert('success', `Prompt ${promptId} completed successfully`);
        
        // Reload active prompt view
        await loadActivePrompt();
    } else {
        showAlert('danger', `Failed to complete prompt: ` + (result.error || result.stderr));
    }
}

/**
 * Show create work iteration modal
 */
function showCreateWorkIterationModal() {
    const modal = new bootstrap.Modal(document.getElementById('createWorkIterationModal'));
    
    // Reset form
    document.getElementById('modal-iteration-name').value = '';
    
    modal.show();
}

/**
 * Create new workdir
 */
async function createWorkdir() {
    const name = document.getElementById('modal-iteration-name').value.trim();
    
    if (!name) {
        showAlert('warning', 'Please enter an iteration name');
        return;
    }
    
    const result = await executeAction('workdir', 'new-setup', { name: name });
    
    if (result.success) {
        showAlert('success', 'Work iteration created successfully');
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('createWorkIterationModal'));
        modal.hide();
        
        // Reload data
        await loadRegistry();
        await loadIterationStatus();
        await loadActivePrompt();  // Refresh Active Prompt page to update button visibility
    } else {
        showAlert('danger', 'Failed to create work iteration: ' + (result.error || result.stderr));
    }
}

/**
 * Archive workdir
 */
async function archiveWorkdir() {
    if (!confirm('Are you sure you want to archive the current work iteration? This will clear the prompts history working directory.')) {
        return;
    }
    
    const result = await executeAction('workdir', 'archive', {});
    
    if (result.success) {
        showAlert('success', 'Work iteration archived successfully');
        
        // Reload data
        await loadRegistry();
        await loadIterationStatus();
        await loadActivePrompt();  // Refresh Active Prompt page to show create iteration button
    } else {
        showAlert('danger', 'Failed to archive work iteration: ' + (result.error || result.stderr));
    }
}

/**
 * Load iteration status
 */
async function loadIterationStatus() {
    // Load and display the registry
    await loadRegistry();
    
    const createSection = document.getElementById('create-iteration-section');
    const registrySection = document.getElementById('registry-section');
    const container = document.getElementById('registry-view-container');
    
    if (!currentRegistry) {
        // No iteration exists - do NOT show the create button in Prompts History
        // The Create Work Iteration control is intentionally available only
        // on the Active Prompt page per the active prompt instructions.
        createSection.style.display = 'none';
        registrySection.style.display = 'none';
        container.innerHTML = '<p class="text-muted">No work iteration exists. Create one on the Active Prompt page.</p>';
        return;
    }
    
    // Iteration exists - show registry
    createSection.style.display = 'none';
    registrySection.style.display = 'block';
    
    // Render registry view
    renderRegistryView(container, currentRegistry);
}

/**
 * Render the registry view
 */
function renderRegistryView(container, registry) {
    // Prompts table (iteration metadata removed - now shown in Active Prompt page header)
    let tableHtml = `
        <div class="table-responsive">
            <table class="table table-sm table-hover table-bordered">
                <thead class="table-light">
                    <tr>
                        <th style="width: 80px;">Prompt ID</th>
                        <th>Title</th>
                        <th style="width: 90px;">State</th>
                        <th style="width: 100px;">Exec Mode</th>
                        <th style="width: 50px;" title="Questionnaire Generated"><i class="bi bi-question-circle"></i> QG</th>
                        <th style="width: 50px;" title="Questionnaire Answered"><i class="bi bi-question-circle-fill"></i> QA</th>
                        <th style="width: 50px;" title="Plan Generated"><i class="bi bi-list-check"></i> Plan</th>
                        <th style="width: 50px;" title="Analysis Generated"><i class="bi bi-clipboard-data"></i> Anl</th>
                        <th style="width: 50px;" title="Implementation Completed"><i class="bi bi-code-square"></i> Impl</th>
                        <th style="width: 50px;" title="Executed"><i class="bi bi-play-circle"></i> Exec</th>
                        <th style="width: 90px;">Mod ID</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    if (registry.prompts && registry.prompts.length > 0) {
        registry.prompts.forEach(prompt => {
            const promptId = prompt['prompt-id'];
            const title = escapeHtml(prompt['prompt-title'] || prompt.title || '');
            const state = prompt.state || 'unknown';
            const executionMode = prompt['execution-mode'] || 'no-action';
            const modId = prompt['current-modification-id'] ? String(prompt['current-modification-id']).padStart(3, '0') : '-';
            
            // State badge
            const stateBadge = state === 'active' 
                ? '<span class="badge bg-success">Active</span>'
                : '<span class="badge bg-secondary">Completed</span>';
            
            // Execution mode badge
            const modeBadge = `<span class="badge bg-info">${escapeHtml(executionMode)}</span>`;
            
            // Boolean icons
            const checkIcon = '<i class="bi bi-check-circle-fill text-success" title="Yes"></i>';
            const xIcon = '<i class="bi bi-x-circle text-secondary" title="No"></i>';
            
            const qGenIcon = prompt['questionnaire-generated'] ? checkIcon : xIcon;
            const qAnsIcon = prompt['questionnaire-answered'] ? checkIcon : xIcon;
            const planIcon = prompt['plan-generated'] ? checkIcon : xIcon;
            const analysisIcon = prompt['analysis-generated'] ? checkIcon : xIcon;
            const implIcon = prompt['implementation-completed'] ? checkIcon : xIcon;
            const execIcon = prompt['executed'] ? checkIcon : xIcon;
            
            // Make title clickable for navigation
            const titleLink = `<a href="#" onclick="openPromptFromRegistry('${promptId}'); return false;" class="text-decoration-none prompt-title-link">${title}</a>`;
            
            tableHtml += `
                <tr>
                    <td><code>${promptId}</code></td>
                    <td>${titleLink}</td>
                    <td>${stateBadge}</td>
                    <td>${modeBadge}</td>
                    <td class="text-center">${qGenIcon}</td>
                    <td class="text-center">${qAnsIcon}</td>
                    <td class="text-center">${planIcon}</td>
                    <td class="text-center">${analysisIcon}</td>
                    <td class="text-center">${implIcon}</td>
                    <td class="text-center">${execIcon}</td>
                    <td class="text-center"><code>${modId}</code></td>
                </tr>
            `;
        });
    } else {
        tableHtml += `
            <tr>
                <td colspan="11" class="text-center text-muted">No prompts found in this iteration</td>
            </tr>
        `;
    }
    
    tableHtml += `
                </tbody>
            </table>
        </div>
    `;
    
    // Set only the table (metadata removed)
    container.innerHTML = tableHtml;
}

/**
 * Open prompt from registry (view prompt directly)
 */
function openPromptFromRegistry(promptId) {
    // Directly view the completed prompt
    viewCompletedPrompt(promptId);
}

/**
 * Open prompt editor
 */
async function openPromptEditor(promptId, viewOnly = false) {
    currentEditingPrompt = promptId;
    isViewOnlyMode = viewOnly;
    
    // Find prompt details from registry
    await loadRegistry();
    const prompt = currentRegistry.prompts.find(p => p['prompt-id'] === promptId);
    
    if (!prompt) {
        showAlert('danger', 'Prompt not found: ' + promptId);
        return;
    }
    
    const title = prompt.title || prompt['prompt-title'] || '';
    currentPromptFolder = `workdir/${promptId}_${title}`;
    
    // Update UI
    document.getElementById('editor-prompt-id').textContent = promptId;
    document.getElementById('editor-mode-label').textContent = viewOnly ? 'View' : 'Edit';
    
    // Show editor view, hide list view
    document.getElementById('prompts-list-view').style.display = 'none';
    document.getElementById('prompt-editor-view').style.display = 'block';
    
    // Load all files
    await loadPromptEditorFiles();
    
    // Disable/enable textareas and save buttons based on view mode
    updateEditorPermissions();
}

/**
 * Close prompt editor
 */
function closePromptEditor() {
    // Show list view, hide editor view
    document.getElementById('prompts-list-view').style.display = 'block';
    document.getElementById('prompt-editor-view').style.display = 'none';
    
    // Clear editor state
    currentEditingPrompt = null;
    currentPromptFolder = null;
    isViewOnlyMode = false;
    
    // Reload prompts list
    loadPrompts();
}

/**
 * Load all prompt editor files
 */
async function loadPromptEditorFiles() {
    const files = ['prompt.md', 'plan.md', 'questionnaire.md', 'implementation.md'];
    
    for (const file of files) {
        await loadPromptEditorFile(file);
    }
}

/**
 * Load a single prompt editor file
 */
async function loadPromptEditorFile(filename) {
    const filepath = `${currentPromptFolder}/${filename}`;
    const elementId = `editor-${filename.replace('.', '-')}`;
    
    try {
        // URL-encode the filepath to handle spaces and special characters
        const encodedFilepath = encodeURIComponent(filepath);
        const response = await fetch('/api/file/' + encodedFilepath + '?token=' + sessionToken);
        const result = await response.json();
        
        const textarea = document.getElementById(elementId);
        if (textarea) {
            if (result.success) {
                textarea.value = result.content || '';
            } else {
                // File might not exist yet
                textarea.value = '';
                console.log(`File ${filename} not found or empty`);
            }
        }
    } catch (error) {
        console.error(`Error loading ${filename}:`, error);
        const textarea = document.getElementById(elementId);
        if (textarea) {
            textarea.value = '';
        }
    }
}

/**
 * Save a prompt file
 */
async function savePromptFile(filename) {
    if (isViewOnlyMode) {
        showAlert('warning', 'Cannot save in view-only mode');
        return;
    }
    
    const elementId = `editor-${filename.replace('.', '-')}`;
    const content = document.getElementById(elementId).value;
    const filepath = `${currentPromptFolder}/${filename}`;
    
    try {
        const response = await fetch('/api/file/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                filepath: filepath,
                content: content
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', `${filename} saved successfully`);
        } else {
            showAlert('danger', `Failed to save ${filename}: ${result.error}`);
        }
    } catch (error) {
        showAlert('danger', `Error saving ${filename}: ${error.message}`);
    }
}

/**
 * Update editor permissions based on view mode
 */
function updateEditorPermissions() {
    const textareaIds = ['editor-prompt-md', 'editor-plan-md', 'editor-questionnaire-md'];
    const saveButtonIds = ['save-prompt-btn', 'save-plan-btn', 'save-questionnaire-btn'];
    
    textareaIds.forEach(id => {
        const textarea = document.getElementById(id);
        if (textarea) {
            textarea.readOnly = isViewOnlyMode;
        }
    });
    
    saveButtonIds.forEach(id => {
        const button = document.getElementById(id);
        if (button) {
            button.disabled = isViewOnlyMode;
            if (isViewOnlyMode) {
                button.classList.remove('btn-success');
                button.classList.add('btn-secondary');
            } else {
                button.classList.remove('btn-secondary');
                button.classList.add('btn-success');
            }
        }
    });
}

/**
 * Shutdown the server
 */
async function shutdownServer() {
    if (!confirm('Are you sure you want to shutdown the RDD Web Server?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/shutdown', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', 'Server is shutting down. You can close this window.');
            // Disable all UI elements after shutdown
            document.body.innerHTML = '<div class="container mt-5 text-center"><h2>Server Shutdown</h2><p>The RDD Web Server has been shut down. You can close this window.</p></div>';
        } else {
            showAlert('danger', `Failed to shutdown server: ${result.error}`);
        }
    } catch (error) {
        // Server likely already shut down, which is expected
        showAlert('success', 'Server shutdown initiated. You can close this window.');
        setTimeout(() => {
            document.body.innerHTML = '<div class="container mt-5 text-center"><h2>Server Shutdown</h2><p>The RDD Web Server has been shut down. You can close this window.</p></div>';
        }, 1000);
    }
}
/**
 * Show add modification modal
 */
function showAddModificationModal() {
    document.getElementById('modification-description').value = '';
    const modal = new bootstrap.Modal(document.getElementById('addModificationModal'));
    modal.show();
}

/**
 * Create a new modification
 */
async function createModification() {
    const description = document.getElementById('modification-description').value.trim();
    
    if (!description) {
        showAlert('warning', 'Please enter a modification description');
        return;
    }
    
    try {
        const response = await fetch('/api/modification/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                description: description
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', 'Modification created successfully');
            // Immediately set execution mode to modification
            await updateExecutionMode('modification');
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('addModificationModal'));
            modal.hide();
            // Reload active prompt to update modifications list
            await loadActivePrompt();
            await loadModifications();
        } else {
            showAlert('danger', `Failed to create modification: ${result.error}`);
        }
    } catch (error) {
        showAlert('danger', `Error creating modification: ${error.message}`);
    }
}

/**
 * Load modifications list
 */
async function loadModifications() {
    try {
        const response = await fetch('/api/modification/list', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayModificationsList(result.modifications || []);
        } else {
            console.error('Failed to load modifications:', result.error);
        }
    } catch (error) {
        console.error('Error loading modifications:', error);
    }
}

/**
 * Display modifications list
 */
function displayModificationsList(modifications) {
    const container = document.getElementById('modifications-list-container');
    
    if (!modifications || modifications.length === 0) {
        container.innerHTML = '<p class="text-muted">No modifications yet.</p>';
        return;
    }
    
    let html = '<div class="list-group">';
    
    modifications.forEach(mod => {
        const statusBadge = mod.status === 'completed' 
            ? '<span class="badge bg-success">Completed</span>' 
            : '<span class="badge bg-warning">In Progress</span>';
        
        const created = new Date(mod.created).toLocaleString();
        const completed = mod.completed ? new Date(mod.completed).toLocaleString() : 'N/A';
        
        // Add edit button for in-progress modifications
        const editButton = mod.status !== 'completed' 
            ? `<button class="btn btn-sm btn-outline-primary" onclick="editModification('${mod['modification-id']}', \`${escapeHtml(mod.description || '').replace(/`/g, '\`')}\`)">
                   <i class="bi bi-pencil"></i> Edit
               </button>` 
            : '';
        
        // Add view implementation button for all modifications
        const viewImplButton = `<button class="btn btn-sm btn-outline-secondary" onclick="viewModificationImplementation('${mod['modification-id']}')" title="View implementation log">
                   <i class="bi bi-file-earmark-text"></i> View Implementation
               </button>`;
        
        html += `
            <div class="list-group-item">
                <div class="d-flex w-100 justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="mb-0">Modification ${mod['modification-id']}</h6>
                            ${statusBadge}
                        </div>
                        <p class="mb-1" id="mod-desc-${mod['modification-id']}">${escapeHtml(mod.description || 'No description')}</p>
                        <small class="text-muted">
                            Created: ${created} | Completed: ${completed}
                        </small>
                    </div>
                    <div class="ms-2 d-flex gap-1">
                        ${viewImplButton}
                        ${editButton}
                    </div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}
/**
 * View modification implementation log
 */
async function viewModificationImplementation(modificationId) {
    const filepath = `${currentPromptFolder}/modification-${modificationId}-implementation.md`;
    const encodedFilepath = encodeURIComponent(filepath);
    
    // Set modal title
    document.getElementById('view-modification-impl-title').textContent = `Modification ${modificationId} - Implementation Log`;
    
    // Load implementation file
    try {
        const response = await fetch('/api/file/' + encodedFilepath + '?token=' + sessionToken);
        const result = await response.json();
        
        const contentArea = document.getElementById('view-modification-impl-content');
        
        if (result.success) {
            const content = result.content || '';
            if (content.trim() === '') {
                contentArea.value = 'No implementation log recorded yet.';
            } else {
                contentArea.value = content;
            }
        } else {
            contentArea.value = 'Implementation log file not found or could not be loaded.';
        }
    } catch (error) {
        console.error('Error loading modification implementation:', error);
        document.getElementById('view-modification-impl-content').value = 'Error loading implementation log: ' + error.message;
    }
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('viewModificationImplementationModal'));
    modal.show();
}

/**
 * Edit a modification description
 */
function editModification(modificationId, currentDescription) {
    const descElement = document.getElementById(`mod-desc-${modificationId}`);
    if (!descElement) return;
    
    // Create textarea for editing
    descElement.innerHTML = `
        <textarea class="form-control mb-2" id="edit-mod-${modificationId}" rows="3">${currentDescription}</textarea>
        <button class="btn btn-sm btn-success me-1" onclick="saveModificationEdit('${modificationId}')">
            <i class="bi bi-check-lg"></i> Save
        </button>
        <button class="btn btn-sm btn-secondary" onclick="cancelModificationEdit('${modificationId}', \`${escapeHtml(currentDescription).replace(/`/g, '\\`')}\`)">
            <i class="bi bi-x-lg"></i> Cancel
        </button>
    `;
    
    // Focus on textarea
    document.getElementById(`edit-mod-${modificationId}`).focus();
}

/**
 * Save modification edit
 */
async function saveModificationEdit(modificationId) {
    const textarea = document.getElementById(`edit-mod-${modificationId}`);
    if (!textarea) return;
    
    const newDescription = textarea.value.trim();
    if (!newDescription) {
        showAlert('warning', 'Description cannot be empty');
        return;
    }
    
    try {
        const response = await fetch('/api/modification/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                modificationId: modificationId,
                description: newDescription
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', 'Modification updated successfully');
            await loadModifications();
        } else {
            showAlert('danger', `Failed to update modification: ${result.error}`);
        }
    } catch (error) {
        showAlert('danger', `Error updating modification: ${error.message}`);
    }
}

/**
 * Cancel modification edit
 */
function cancelModificationEdit(modificationId, originalDescription) {
    const descElement = document.getElementById(`mod-desc-${modificationId}`);
    if (!descElement) return;
    
    descElement.innerHTML = escapeHtml(originalDescription);
}

/**
 * Show snippet validation dialog with invalid keys
 * @param {Array<string>} invalidKeys - Array of invalid snippet keys
 * @returns {Promise<boolean>} True if user wants to save anyway, false to cancel
 */
function showSnippetValidationDialog(invalidKeys) {
    return new Promise((resolve) => {
        const invalidKeysList = invalidKeys.map(key => `<code>${escapeHtml(key)}</code>`).join('<br>');
        
        const modalHtml = `
            <div class="modal fade" id="snippetValidationModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header bg-warning">
                            <h5 class="modal-title">
                                <i class="bi bi-exclamation-triangle"></i> Invalid Snippet Keys Found
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p>The following snippet keys in your prompt are not defined in manifest.json:</p>
                            <div class="alert alert-warning">
                                ${invalidKeysList}
                            </div>
                            <p>Do you want to:</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="fixManuallyBtn">
                                <i class="bi bi-pencil"></i> Fix Manually
                            </button>
                            <button type="button" class="btn btn-warning" id="saveAnywayBtn">
                                <i class="bi bi-save"></i> Save Anyway
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing modal if any
        const existingModal = document.getElementById('snippetValidationModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Add modal to body
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        const modalElement = document.getElementById('snippetValidationModal');
        const modal = new bootstrap.Modal(modalElement);
        
        // Handle button clicks
        document.getElementById('saveAnywayBtn').addEventListener('click', () => {
            modal.hide();
            resolve(true);
        });
        
        document.getElementById('fixManuallyBtn').addEventListener('click', () => {
            modal.hide();
            resolve(false);
        });
        
        // Handle modal close (X button or backdrop)
        modalElement.addEventListener('hidden.bs.modal', () => {
            modalElement.remove();
        });
        
        modal.show();
    });
}

/**
 * Insert snippet from toolbar button
 */
function insertSnippetFromButton() {
    if (typeof promptSnippetAutocomplete !== 'undefined' && promptSnippetAutocomplete) {
        promptSnippetAutocomplete.trigger();
    } else {
        showAlert('warning', 'Snippet autocomplete not initialized. Type [[[ to insert snippets.');
    }
}

/**
 * Load requirements content for the Requirements tab
 */
async function loadRequirements() {
    const textarea = document.getElementById('requirements-content');
    
    try {
        const response = await fetch('/api/file/specifications/requirements.md?token=' + sessionToken);
        const result = await response.json();
        
        if (result.success) {
            textarea.value = result.content || '';
        } else {
            showAlert('danger', 'Failed to load requirements: ' + result.error);
        }
    } catch (error) {
        showAlert('danger', 'Error loading requirements: ' + error.message);
    }
}

/**
 * Save requirements content
 */
async function saveRequirements() {
    const content = document.getElementById('requirements-content').value;
    
    try {
        const response = await fetch('/api/file/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                filepath: 'specifications/requirements.md',
                content: content
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', 'Requirements saved successfully');
        } else {
            showAlert('danger', 'Failed to save requirements: ' + result.error);
        }
    } catch (error) {
        showAlert('danger', 'Error saving requirements: ' + error.message);
    }
}

/**
 * Load configuration
 */
async function loadConfig() {
    try {
        const response = await fetch('/api/config?token=' + sessionToken);
        const result = await response.json();
        
        if (result.success) {
            const gitEnabled = result.data['git-enabled'] || false;
            document.getElementById('git-enabled-toggle').checked = gitEnabled;
        } else {
            showAlert('danger', 'Failed to load configuration: ' + result.error);
        }
    } catch (error) {
        showAlert('danger', 'Error loading configuration: ' + error.message);
    }
}

/**
 * Save git-enabled configuration
 */
async function saveGitEnabled() {
    const gitEnabled = document.getElementById('git-enabled-toggle').checked;
    
    try {
        const response = await fetch('/api/config/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                gitEnabled: gitEnabled
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', 'Configuration saved successfully');
        } else {
            showAlert('danger', 'Failed to save configuration: ' + result.error);
        }
    } catch (error) {
        showAlert('danger', 'Error saving configuration: ' + error.message);
    }
}

/**
 * Technical Design Data
 */
let techDesignSchema = null;
let techDesignAnswers = {};
let techDesignCurrentCategory = null;

/**
 * Load technical design content
 */
async function loadTechnicalDesign() {
    // Show loading state
    document.getElementById('tech-design-loading').style.display = 'block';
    document.getElementById('tech-design-no-category').style.display = 'none';
    document.getElementById('tech-design-questions').style.display = 'none';
    
    try {
        // Load schema
        const schemaResponse = await fetch('/api/technical-design/schema');
        const schemaResult = await schemaResponse.json();
        
        if (!schemaResult.success) {
            showAlert('danger', 'Failed to load technical design schema: ' + schemaResult.error);
            return;
        }
        
        techDesignSchema = schemaResult.schema;
        
        // Load answers
        const answersResponse = await fetch('/api/technical-design/answers');
        const answersResult = await answersResponse.json();
        
        if (answersResult.success) {
            techDesignAnswers = answersResult.answers || {};
        }
        
        // Render category list
        renderCategoryList();
        
        // Hide loading, show no category message
        document.getElementById('tech-design-loading').style.display = 'none';
        document.getElementById('tech-design-no-category').style.display = 'block';
        
        // Set up search and filter handlers
        setupTechnicalDesignFilters();
        
    } catch (error) {
        showAlert('danger', 'Error loading technical design: ' + error.message);
        document.getElementById('tech-design-loading').style.display = 'none';
    }
}

/**
 * Render category list in sidebar
 */
function renderCategoryList() {
    const categoryList = document.getElementById('category-list');
    categoryList.innerHTML = '';
    
    techDesignSchema.categories.forEach((category, index) => {
        const answeredCount = countAnsweredInCategory(category);
        const totalCount = countQuestionsInCategory(category);
        
        const item = document.createElement('a');
        item.href = '#';
        item.className = 'list-group-item list-group-item-action';
        item.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <span>${category.label}</span>
                <span class="badge bg-secondary">${answeredCount}/${totalCount}</span>
            </div>
        `;
        item.onclick = (e) => {
            e.preventDefault();
            selectCategory(category.id);
        };
        
        categoryList.appendChild(item);
    });
}

/**
 * Count answered questions in a category
 */
function countAnsweredInCategory(category) {
    let count = 0;
    category.groups.forEach(group => {
        group.questions.forEach(question => {
            if (techDesignAnswers[question.id]) {
                count++;
            }
        });
    });
    return count;
}

/**
 * Count total questions in a category
 */
function countQuestionsInCategory(category) {
    let count = 0;
    category.groups.forEach(group => {
        count += group.questions.length;
    });
    return count;
}

/**
 * Select a category and render its questions
 */
function selectCategory(categoryId) {
    techDesignCurrentCategory = categoryId;
    
    // Update active state in sidebar
    const items = document.querySelectorAll('#category-list .list-group-item');
    items.forEach(item => item.classList.remove('active'));
    
    const activeIndex = techDesignSchema.categories.findIndex(c => c.id === categoryId);
    if (activeIndex >= 0) {
        items[activeIndex].classList.add('active');
    }
    
    // Render questions for this category
    renderCategoryQuestions(categoryId);
    
    // Show questions container
    document.getElementById('tech-design-no-category').style.display = 'none';
    document.getElementById('tech-design-questions').style.display = 'block';
}

/**
 * Render questions for a category
 */
function renderCategoryQuestions(categoryId) {
    const category = techDesignSchema.categories.find(c => c.id === categoryId);
    if (!category) return;
    
    const accordion = document.getElementById('tech-design-accordion');
    accordion.innerHTML = '';
    
    category.groups.forEach((group, groupIndex) => {
        const groupId = `group-${categoryId}-${groupIndex}`;
        
        const groupDiv = document.createElement('div');
        groupDiv.className = 'accordion-item';
        
        const headerDiv = document.createElement('h2');
        headerDiv.className = 'accordion-header';
        headerDiv.id = `heading-${groupId}`;
        
        const button = document.createElement('button');
        button.className = 'accordion-button' + (groupIndex !== 0 ? ' collapsed' : '');
        button.type = 'button';
        button.setAttribute('data-bs-toggle', 'collapse');
        button.setAttribute('data-bs-target', `#collapse-${groupId}`);
        button.textContent = group.label;
        
        headerDiv.appendChild(button);
        groupDiv.appendChild(headerDiv);
        
        const collapseDiv = document.createElement('div');
        collapseDiv.id = `collapse-${groupId}`;
        collapseDiv.className = 'accordion-collapse collapse' + (groupIndex === 0 ? ' show' : '');
        collapseDiv.setAttribute('data-bs-parent', '#tech-design-accordion');
        
        const bodyDiv = document.createElement('div');
        bodyDiv.className = 'accordion-body';
        
        // Render questions in this group
        group.questions.forEach(question => {
            if (isQuestionVisible(question)) {
                bodyDiv.appendChild(renderQuestion(question));
            }
        });
        
        collapseDiv.appendChild(bodyDiv);
        groupDiv.appendChild(collapseDiv);
        
        accordion.appendChild(groupDiv);
    });
}

/**
 * Check if a question should be visible based on visibleWhen rules
 */
function isQuestionVisible(question) {
    if (!question.visibleWhen || question.visibleWhen.length === 0) {
        return true;
    }
    
    // All rules must be satisfied (AND logic)
    for (const rule of question.visibleWhen) {
        const dependentAnswer = techDesignAnswers[rule.questionId];
        if (!dependentAnswer) {
            return false;
        }
        
        const value = dependentAnswer.value;
        if (Array.isArray(value)) {
            // Multiselect: check if equals value is in array
            if (!value.includes(rule.equals)) {
                return false;
            }
        } else {
            // Radio/text: check exact match
            if (value !== rule.equals) {
                return false;
            }
        }
    }
    
    return true;
}

/**
 * Render a single question
 */
function renderQuestion(question) {
    const questionDiv = document.createElement('div');
    questionDiv.className = 'mb-4 p-3 border rounded';
    questionDiv.setAttribute('data-question-id', question.id);
    
    // Question label
    const label = document.createElement('div');
    label.className = 'fw-bold mb-2';
    label.textContent = question.label;
    questionDiv.appendChild(label);
    
    // Help text
    if (question.help) {
        const help = document.createElement('div');
        help.className = 'text-muted small mb-2';
        help.textContent = question.help;
        questionDiv.appendChild(help);
    }
    
    // Current answer display
    const currentAnswer = techDesignAnswers[question.id];
    if (currentAnswer) {
        const answerDisplay = document.createElement('div');
        answerDisplay.className = 'alert alert-success small py-2 mb-2';
        answerDisplay.innerHTML = `<strong>Current answer:</strong> ${formatAnswerValue(currentAnswer.value)}`;
        questionDiv.appendChild(answerDisplay);
    }
    
    // Question input based on type
    if (question.type === 'radio' && question.options) {
        const optionsDiv = document.createElement('div');
        question.options.forEach(option => {
            const radioDiv = document.createElement('div');
            radioDiv.className = 'form-check';
            
            const input = document.createElement('input');
            input.type = 'radio';
            input.className = 'form-check-input';
            input.name = question.id;
            input.value = option.id;
            input.id = `${question.id}-${option.id}`;
            if (currentAnswer && currentAnswer.value === option.id) {
                input.checked = true;
            }
            input.onchange = () => saveQuestionAnswer(question, option.id);
            
            const labelEl = document.createElement('label');
            labelEl.className = 'form-check-label';
            labelEl.htmlFor = input.id;
            labelEl.textContent = option.label;
            
            radioDiv.appendChild(input);
            radioDiv.appendChild(labelEl);
            optionsDiv.appendChild(radioDiv);
        });
        questionDiv.appendChild(optionsDiv);
    } else if (question.type === 'multiselect' && question.options) {
        const optionsDiv = document.createElement('div');
        question.options.forEach(option => {
            const checkDiv = document.createElement('div');
            checkDiv.className = 'form-check';
            
            const input = document.createElement('input');
            input.type = 'checkbox';
            input.className = 'form-check-input';
            input.value = option.id;
            input.id = `${question.id}-${option.id}`;
            if (currentAnswer && Array.isArray(currentAnswer.value) && currentAnswer.value.includes(option.id)) {
                input.checked = true;
            }
            input.onchange = () => saveMultiselectAnswer(question);
            
            const labelEl = document.createElement('label');
            labelEl.className = 'form-check-label';
            labelEl.htmlFor = input.id;
            labelEl.textContent = option.label;
            
            checkDiv.appendChild(input);
            checkDiv.appendChild(labelEl);
            optionsDiv.appendChild(checkDiv);
        });
        questionDiv.appendChild(optionsDiv);
    } else if (question.type === 'text') {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'form-control';
        input.placeholder = question.placeholder || '';
        input.value = currentAnswer ? currentAnswer.value : '';
        input.onblur = () => saveQuestionAnswer(question, input.value);
        questionDiv.appendChild(input);
    }
    
    // Clear answer button
    if (currentAnswer) {
        const clearBtn = document.createElement('button');
        clearBtn.className = 'btn btn-sm btn-outline-danger mt-2';
        clearBtn.innerHTML = '<i class="bi bi-x-circle"></i> Clear Answer';
        clearBtn.onclick = () => clearQuestionAnswer(question);
        questionDiv.appendChild(clearBtn);
    }
    
    return questionDiv;
}

/**
 * Format answer value for display
 */
function formatAnswerValue(value) {
    if (Array.isArray(value)) {
        return value.join(', ');
    }
    return value;
}

/**
 * Save question answer
 */
async function saveQuestionAnswer(question, value) {
    try {
        const response = await fetch('/api/technical-design/answer/set', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                questionId: question.id,
                type: question.type,
                value: value
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Reload answers and re-render
            await reloadTechnicalDesignAnswers();
            showAlert('success', 'Answer saved', 2000);
        } else {
            showAlert('danger', 'Failed to save answer: ' + (result.error || 'Unknown error'));
        }
    } catch (error) {
        showAlert('danger', 'Error saving answer: ' + error.message);
    }
}

/**
 * Save multiselect answer
 */
async function saveMultiselectAnswer(question) {
    const checkboxes = document.querySelectorAll(`input[id^="${question.id}-"]:checked`);
    const values = Array.from(checkboxes).map(cb => cb.value);
    
    if (values.length === 0) {
        // No values selected - remove answer
        await clearQuestionAnswer(question);
    } else {
        await saveQuestionAnswer(question, values);
    }
}

/**
 * Clear question answer
 */
async function clearQuestionAnswer(question) {
    try {
        const response = await fetch('/api/technical-design/answer/remove', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                questionId: question.id
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Reload answers and re-render
            await reloadTechnicalDesignAnswers();
            showAlert('success', 'Answer cleared', 2000);
        } else {
            showAlert('danger', 'Failed to clear answer: ' + (result.error || 'Unknown error'));
        }
    } catch (error) {
        showAlert('danger', 'Error clearing answer: ' + error.message);
    }
}

/**
 * Reload technical design answers and re-render current category
 */
async function reloadTechnicalDesignAnswers() {
    try {
        const response = await fetch('/api/technical-design/answers');
        const result = await response.json();
        
        if (result.success) {
            techDesignAnswers = result.answers || {};
            
            // Re-render category list to update counters
            renderCategoryList();
            
            // Re-render current category if one is selected
            if (techDesignCurrentCategory) {
                renderCategoryQuestions(techDesignCurrentCategory);
                // Restore active state
                const activeIndex = techDesignSchema.categories.findIndex(c => c.id === techDesignCurrentCategory);
                const items = document.querySelectorAll('#category-list .list-group-item');
                items.forEach(item => item.classList.remove('active'));
                if (activeIndex >= 0) {
                    items[activeIndex].classList.add('active');
                }
            }
        }
    } catch (error) {
        console.error('Error reloading answers:', error);
    }
}

/**
 * Set up search and filter handlers
 */
function setupTechnicalDesignFilters() {
    const searchInput = document.getElementById('tech-design-search');
    const filterStatus = document.getElementById('tech-design-filter-status');
    
    searchInput.addEventListener('input', applyTechnicalDesignFilters);
    filterStatus.addEventListener('change', applyTechnicalDesignFilters);
}

/**
 * Apply filters to questions
 */
function applyTechnicalDesignFilters() {
    const searchTerm = document.getElementById('tech-design-search').value.toLowerCase();
    const filterStatus = document.getElementById('tech-design-filter-status').value;
    
    const questions = document.querySelectorAll('[data-question-id]');
    
    questions.forEach(questionDiv => {
        const questionId = questionDiv.getAttribute('data-question-id');
        const question = findQuestionById(questionId);
        
        if (!question) {
            questionDiv.style.display = 'none';
            return;
        }
        
        let show = true;
        
        // Apply search filter
        if (searchTerm) {
            const searchableText = [
                question.label,
                question.help || '',
                ...(question.options || []).map(o => o.label)
            ].join(' ').toLowerCase();
            
            if (!searchableText.includes(searchTerm)) {
                show = false;
            }
        }
        
        // Apply status filter
        if (filterStatus) {
            const isAnswered = !!techDesignAnswers[questionId];
            if (filterStatus === 'answered' && !isAnswered) {
                show = false;
            } else if (filterStatus === 'unanswered' && isAnswered) {
                show = false;
            }
        }
        
        questionDiv.style.display = show ? 'block' : 'none';
    });
}

/**
 * Find a question by ID across all categories
 */
function findQuestionById(questionId) {
    for (const category of techDesignSchema.categories) {
        for (const group of category.groups) {
            for (const question of group.questions) {
                if (question.id === questionId) {
                    return question;
                }
            }
        }
    }
    return null;
}

/**
 * Save technical design content (legacy - kept for compatibility)
 */
async function saveTechnicalDesign() {
    // This function is replaced by the new dynamic UI
    // Kept for backwards compatibility but shows a message
    showAlert('info', 'Technical Design now uses a dynamic form. Use the category navigation to answer questions.');
}

/**
 * Load and display the user guide in the Help section
 */
async function loadUserGuide() {
    const container = document.getElementById('help-content-container');
    
    try {
        // Show loading state
        container.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-secondary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3">Loading user guide...</p>
            </div>
        `;
        
        const response = await fetch('/api/help/user-guide');
        const data = await response.json();
        
        if (!response.ok || !data.success) {
            throw new Error(data.error || 'Failed to load user guide');
        }
        
        // Display the rendered HTML
        container.innerHTML = `<div class="user-guide-content">${data.html}</div>`;
        
    } catch (error) {
        console.error('Error loading user guide:', error);
        container.innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-exclamation-triangle"></i>
                <strong>Error loading user guide:</strong> ${error.message}
                <p class="mt-2 mb-0">
                    <small>Please ensure the user guide file exists at .rdd/docs/user-guide.md</small>
                </p>
            </div>
        `;
    }
}

// ============================================================================
// HELP SYSTEM - Tooltips and Context-Sensitive Help
// ============================================================================

/**
 * Help content constants for tooltips and modals
 */
const HELP_CONTENT = {
    // Execution mode tooltips
    executionModes: {
        clarify: {
            title: "Clarify Mode",
            description: "Generate questions to resolve ambiguities in the prompt. Use when the prompt lacks specific details like file paths, behavior descriptions, or design decisions. Produces questionnaire.json with questions for you to answer."
        },
        analyze: {
            title: "Analyze Mode", 
            description: "Analyze the prompt to identify requirements, constraints, and technical considerations. Use before planning or implementation to ensure thorough understanding. Produces analysis.md with detailed findings."
        },
        plan: {
            title: "Plan Mode",
            description: "Generate a detailed step-by-step implementation plan without executing it. Use when you want to review the approach before implementation. Produces plan.md with specific execution steps."
        },
        implement: {
            title: "Implement Mode",
            description: "Execute the full implementation of the prompt including code changes and file updates. Use when you're ready to apply changes to your codebase. Produces implementation.md with detailed change log."
        },
        modification: {
            title: "Modification Mode",
            description: "Create a small correction or enhancement to a completed prompt. Use for minor fixes without creating a full new prompt. Produces modification-XXX.md and modification-XXX-implementation.md files."
        }
    },
    
    // Status flag tooltips
    statusFlags: {
        questionnaireGenerated: {
            label: "Questionnaire Generated",
            explanation: "A questionnaire file (questionnaire.json) has been created with clarification questions",
            trigger: "Set when Clarify mode execution completes successfully"
        },
        questionnaireAnswered: {
            label: "Questionnaire Answered",
            explanation: "All questions in the questionnaire have been answered by the user",
            trigger: "Set when the user provides answers to all questionnaire questions via the Web UI"
        },
        analysisGenerated: {
            label: "Analysis Generated",
            explanation: "An analysis file (analysis.md) has been created with detailed prompt analysis",
            trigger: "Set when Analyze mode execution completes successfully"
        },
        planGenerated: {
            label: "Plan Generated",
            explanation: "An implementation plan file (plan.md) has been created with step-by-step instructions",
            trigger: "Set when Plan mode execution completes successfully"
        },
        implementationCompleted: {
            label: "Implementation Completed",
            explanation: "The prompt implementation has finished and an implementation log has been created",
            trigger: "Set when Implement mode execution completes successfully"
        },
        executed: {
            label: "Executed",
            explanation: "The prompt has been executed at least once (any execution mode)",
            trigger: "Set when any execution mode completes, tracking that work has been done on this prompt"
        },
        modificationsCount: {
            label: "Modifications Count",
            explanation: "Number of modifications created for this prompt",
            trigger: "Incremented each time a new modification is created"
        },
        currentModification: {
            label: "Current Modification ID",
            explanation: "The ID of the modification currently being worked on",
            trigger: "Set when a modification is created, cleared when modification completes"
        }
    },
    
    // Page-level help content
    pages: {
        activePrompt: {
            title: "Active Prompt - Help",
            purpose: "The Active Prompt page is your primary workspace for developing a single prompt through its lifecycle from clarification to implementation.",
            workflows: [
                "<strong>Clarify → Analyze → Plan → Implement:</strong> Standard workflow for complex prompts requiring clarification and planning",
                "<strong>Quick Implementation:</strong> Skip directly to Implement mode for straightforward prompts",
                "<strong>Modifications:</strong> After completing a prompt, use modifications for small corrections without creating a new prompt"
            ],
            userGuideLink: "/README.md"
        },
        promptsHistory: {
            title: "Prompts History - Help",
            purpose: "View and manage all prompts in the current work iteration, including their states, execution modes, and workflow progress.",
            workflows: [
                "<strong>Review Progress:</strong> See which prompts are active, completed, or in progress",
                "<strong>Track Workflow:</strong> Monitor questionnaire, analysis, plan, and implementation flags for each prompt",
                "<strong>Iteration Management:</strong> View iteration metadata and archive completed iterations"
            ],
            userGuideLink: "/README.md"
        },
        technicalDesign: {
            title: "Technical Design - Help",
            purpose: "Define and document architectural decisions, technology choices, and design constraints for your project in a structured format.",
            workflows: [
                "<strong>Interactive Form:</strong> Answer configuration questions that adapt based on your previous choices",
                "<strong>JSON Export:</strong> Technical design is stored as JSON for programmatic access during implementation"
            ],
            userGuideLink: "/README.md"
        },
        requirements: {
            title: "Requirements - Help",
            purpose: "Manage user requirements (UR) and technical requirements (TR) that define what your system should do and how it should be built.",
            workflows: [
                "<strong>View Requirements:</strong> Browse all requirements with their IDs, text, and status",
                "<strong>Traceability:</strong> Requirements are automatically updated during prompt implementation",
                "<strong>Historical Record:</strong> Requirements file maintains complete history of project specifications"
            ],
            userGuideLink: "/README.md"
        }
    }
};

/**
 * Initialize all tooltips on the page
 * Should be called after DOM content is loaded and after dynamic content updates
 */
function initializeTooltips() {
    // Dispose of existing tooltips to avoid duplicates
    const existingTooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    existingTooltips.forEach(element => {
        const tooltip = bootstrap.Tooltip.getInstance(element);
        if (tooltip) {
            tooltip.dispose();
        }
    });
    
    // Initialize all tooltips with configuration for touch devices
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(element => {
        new bootstrap.Tooltip(element, {
            trigger: 'hover focus', // Works on both desktop (hover) and touch (focus on tap)
            boundary: 'window',
            placement: 'auto'
        });
    });
}

/**
 * Setup execution mode tooltips
 * Adds tooltips to the execution mode radio buttons
 */
function setupExecutionModeTooltips() {
    const modes = ['clarify', 'analyze', 'plan', 'implement', 'modification'];
    
    modes.forEach(mode => {
        const modeElement = document.getElementById(`mode-${mode}`);
        const labelElement = document.querySelector(`label[for="mode-${mode}"]`);
        
        if (labelElement && HELP_CONTENT.executionModes[mode]) {
            const content = HELP_CONTENT.executionModes[mode];
            labelElement.setAttribute('data-bs-toggle', 'tooltip');
            labelElement.setAttribute('data-bs-placement', 'top');
            labelElement.setAttribute('title', content.description);
            labelElement.style.cursor = 'help';
        }
    });
}

/**
 * Setup enhanced status flag tooltips
 * Updates existing status flag tooltips with detailed information
 */
function setupStatusFlagTooltips() {
    const flagMappings = {
        'flag-questionnaire-generated': 'questionnaireGenerated',
        'flag-questionnaire-answered': 'questionnaireAnswered',
        'flag-analysis-generated': 'analysisGenerated',
        'flag-plan-generated': 'planGenerated',
        'flag-implementation-completed': 'implementationCompleted',
        'flag-executed': 'executed',
        'flag-modifications-count': 'modificationsCount',
        'flag-current-modification': 'currentModification'
    };
    
    Object.entries(flagMappings).forEach(([elementId, contentKey]) => {
        const element = document.getElementById(elementId);
        if (element && HELP_CONTENT.statusFlags[contentKey]) {
            const content = HELP_CONTENT.statusFlags[contentKey];
            const tooltipText = `${content.label}: ${content.explanation}. ${content.trigger}`;
            element.setAttribute('data-bs-toggle', 'tooltip');
            element.setAttribute('data-bs-placement', 'top');
            element.setAttribute('title', tooltipText);
        }
    });
}

/**
 * Show page-level help modal
 */
function showPageHelp(pageName) {
    const helpContent = HELP_CONTENT.pages[pageName];
    if (!helpContent) {
        console.error('No help content found for page:', pageName);
        return;
    }
    
    // Create modal HTML
    const modalHtml = `
        <div class="modal fade" id="pageHelpModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">
                            <i class="bi bi-question-circle"></i> ${helpContent.title}
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <h6 class="text-primary">Purpose</h6>
                            <p class="text-muted">${helpContent.purpose}</p>
                        </div>
                        <div class="mb-3">
                            <h6 class="text-primary">Key Workflows</h6>
                            <ul>
                                ${helpContent.workflows.map(w => `<li>${w}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="mt-4">
                            <a href="${helpContent.userGuideLink}" target="_blank" class="btn btn-outline-primary btn-sm">
                                <i class="bi bi-book"></i> View Full User Guide
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if present
    const existingModal = document.getElementById('pageHelpModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('pageHelpModal'));
    modal.show();
    
    // Clean up modal after it's hidden
    document.getElementById('pageHelpModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}
