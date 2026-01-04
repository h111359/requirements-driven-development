// RDD Web Interface - Main JavaScript

// Global state
let sessionToken = null;
let currentPromptId = null;
let currentRegistry = null;
let currentEditingPrompt = null;
let currentPromptFolder = null;
let isViewOnlyMode = false;

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
    event.target.classList.add('active');
    
    // Load section-specific data
    if (sectionName === 'prompts-history') {
        loadPromptsHistory();
    } else if (sectionName === 'active-prompt') {
        loadActivePrompt();
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
        container.innerHTML = '<p class="text-warning">No work iteration found. Please create one in the Workdir section.</p>';
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
        
        // Reload prompts history
        await loadPromptsHistory();
        // Also reload active prompt page if it exists
        const activeSection = document.getElementById('section-active-prompt');
        if (activeSection && activeSection.style.display !== 'none') {
            await loadActivePrompt();
        }
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
        
        // Reload both views
        await loadPromptsHistory();
        await loadActivePrompt();
    } else {
        showAlert('danger', 'Failed to set prompt state: ' + (result.error || result.stderr));
    }
}

/**
 * Load and display prompts history (completed prompts only)
 */
async function loadPromptsHistory() {
    const container = document.getElementById('prompts-history-table-container');
    container.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
    
    await loadRegistry();
    
    if (!currentRegistry || !currentRegistry.prompts) {
        container.innerHTML = '<p class="text-warning">No work iteration found. Please create one in the Workdir section.</p>';
        return;
    }
    
    // Filter to completed prompts only
    const completedPrompts = currentRegistry.prompts.filter(p => p.state === 'completed');
    
    if (completedPrompts.length === 0) {
        container.innerHTML = '<p class="text-muted">No completed prompts found.</p>';
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
                        <th>Questionnaire</th>
                        <th>Plan</th>
                        <th>Implementation</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    completedPrompts.forEach(prompt => {
        const promptId = prompt['prompt-id'];
        const title = prompt.title || prompt['prompt-title'] || '';
        
        // Status badges
        const questionnaireGenerated = prompt['questionnaire-generated'] || false;
        const questionnaireAnswered = prompt['questionnaire-answered'] || false;
        const planGenerated = prompt['plan-generated'] || false;
        const implementationCompleted = prompt['implementation-completed'] || false;
        
        // Questionnaire status: Green if answered, Gray if not generated
        let questionnaireBadge = '';
        if (!questionnaireGenerated) {
            questionnaireBadge = '<span class="badge bg-secondary"><i class="bi bi-dash-circle"></i> Not Generated</span>';
        } else if (questionnaireAnswered) {
            questionnaireBadge = '<span class="badge bg-success"><i class="bi bi-check-circle"></i> Answered</span>';
        } else {
            questionnaireBadge = '<span class="badge bg-warning"><i class="bi bi-clock-history"></i> Generated</span>';
        }
        
        // Plan status
        const planBadge = planGenerated 
            ? '<span class="badge bg-success"><i class="bi bi-check-circle"></i> Generated</span>'
            : '<span class="badge bg-secondary"><i class="bi bi-dash-circle"></i> Not Generated</span>';
        
        // Implementation status
        const implementationBadge = implementationCompleted
            ? '<span class="badge bg-success"><i class="bi bi-check-circle"></i> Completed</span>'
            : '<span class="badge bg-secondary"><i class="bi bi-dash-circle"></i> Not Completed</span>';
        
        html += `
            <tr>
                <td><code>${promptId}</code></td>
                <td>${escapeHtml(title)}</td>
                <td>${questionnaireBadge}</td>
                <td>${planBadge}</td>
                <td>${implementationBadge}</td>
                <td>
                    <button class="btn btn-sm btn-primary" 
                            onclick="viewCompletedPrompt('${promptId}')">
                        <i class="bi bi-eye"></i> View
                    </button>
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
    
    // Update title
    const promptId = activePrompt['prompt-id'];
    const title = activePrompt.title || activePrompt['prompt-title'] || '';
    document.getElementById('active-prompt-title').innerHTML = 
        `<i class="bi bi-journal-check me-2"></i><span>${promptId}: ${escapeHtml(title)}</span>`;
    
    // Update execution mode selector (button group)
    const currentMode = activePrompt['execution-mode'] || getSmartDefaultMode(activePrompt);
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
    
    // Update tab visibility based on workflow state
    updateTabVisibility(activePrompt);
    
    // Load prompt files
    await loadActivePromptFiles(promptId);
    
    // Load modifications if implementation is completed
    if (implementationCompleted) {
        await loadModifications();
    }
}

/**
 * Show no active prompt message
 */
function showNoActivePrompt() {
    document.getElementById('no-active-prompt-message').style.display = 'block';
    document.getElementById('active-prompt-content').style.display = 'none';
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
 * Update tab visibility for active prompt based on workflow state
 */
function updateTabVisibility(prompt) {
    const questionnaireGenerated = prompt['questionnaire-generated'] || false;
    const planGenerated = prompt['plan-generated'] || false;
    const analysisGenerated = prompt['analysis-generated'] || false;
    const implementationCompleted = prompt['implementation-completed'] || false;
    const executed = prompt.executed || false;
    
    // Get tab elements (li elements containing the tab buttons)
    const questionnaireTabLi = document.querySelector('#active-questionnaire-tab').closest('li.nav-item');
    const planTabLi = document.querySelector('#active-plan-tab').closest('li.nav-item');
    const analysisTabLi = document.querySelector('#active-analysis-tab').closest('li.nav-item');
    const implementationTabLi = document.querySelector('#active-implementation-tab').closest('li.nav-item');
    const modificationsTabLi = document.querySelector('#active-modifications-tab').closest('li.nav-item');
    
    // Prompt tab: always visible (no action needed)
    
    // Questionnaire tab: visible when questionnaire-generated=true
    if (questionnaireTabLi) {
        questionnaireTabLi.style.display = questionnaireGenerated ? '' : 'none';
    }
    
    // Plan tab: visible when plan-generated=true
    if (planTabLi) {
        planTabLi.style.display = planGenerated ? '' : 'none';
    }
    
    // Analysis tab: visible when analysis-generated=true
    if (analysisTabLi) {
        analysisTabLi.style.display = analysisGenerated ? '' : 'none';
    }
    
    // Implementation tab: visible when implementation-completed=true
    if (implementationTabLi) {
        implementationTabLi.style.display = implementationCompleted ? '' : 'none';
    }
    
    // Modifications tab: visible when executed=true
    if (modificationsTabLi) {
        modificationsTabLi.style.display = executed ? '' : 'none';
    }
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
        'bi bi-square',
        'bi bi-check-square-fill');
    updateFlag('flag-plan-generated', 
        prompt['plan-generated'] || false,
        'bi bi-journal-text',
        'bi bi-journal-check');
    updateFlag('flag-analysis-generated', 
        prompt['analysis-generated'] || false,
        'bi bi-clipboard-data',
        'bi bi-clipboard-check');
    updateFlag('flag-implementation-completed', 
        prompt['implementation-completed'] || false,
        'bi bi-code-slash',
        'bi bi-check-circle-fill');
    updateFlag('flag-executed', 
        prompt.executed || false,
        'bi bi-play-circle',
        'bi bi-play-circle-fill');
    
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
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
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
        
        // Reload both views
        await loadPromptsHistory();
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
        
        // Reload both views
        await loadPromptsHistory();
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
        
        await loadIterationStatus();
        await loadRegistry();
    } else {
        showAlert('danger', 'Failed to create work iteration: ' + (result.error || result.stderr));
    }
}

/**
 * Archive workdir
 */
async function archiveWorkdir() {
    if (!confirm('Are you sure you want to archive the current work iteration? This will clear the workdir.')) {
        return;
    }
    
    const result = await executeAction('workdir', 'archive', {});
    
    if (result.success) {
        showAlert('success', 'Work iteration archived successfully');
        await loadIterationStatus();
        await loadRegistry();
    } else {
        showAlert('danger', 'Failed to archive work iteration: ' + (result.error || result.stderr));
    }
}

/**
 * Load iteration status
 */
async function loadIterationStatus() {
    // Update compact status header
    await loadRegistry();
    
    if (!currentRegistry) {
        document.getElementById('status-iteration-id').textContent = 'No iteration';
        document.getElementById('status-iteration-name').textContent = '';
        document.getElementById('status-total-prompts').textContent = '';
        document.getElementById('status-next-prompt-id').textContent = '';
        return;
    }
    
    document.getElementById('status-iteration-id').innerHTML = `<strong>ID:</strong> <code>${currentRegistry['iteration-id']}</code>`;
    document.getElementById('status-iteration-name').innerHTML = `<strong>Name:</strong> ${escapeHtml(currentRegistry['iteration-name'])}`;
    document.getElementById('status-total-prompts').innerHTML = `<strong>Prompts:</strong> ${currentRegistry.prompts ? currentRegistry.prompts.length : 0}`;
    document.getElementById('status-next-prompt-id').innerHTML = `<strong>Next ID:</strong> <code>P-${String(currentRegistry['prompt-id-sequence-next-value']).padStart(3, '0')}</code>`;
}

/**
 * Load file
 */
async function loadFile() {
    const filepath = document.getElementById('file-path').value.trim();
    
    if (!filepath) {
        showAlert('warning', 'Please enter a file path');
        return;
    }
    
    try {
        const response = await fetch('/api/file/' + filepath + '?token=' + sessionToken);
        const result = await response.json();
        
        if (result.success) {
            let content;
            if (result.data) {
                // JSON file
                content = JSON.stringify(result.data, null, 2);
            } else {
                // Text file
                content = result.content;
            }
            
            document.getElementById('file-content').value = content;
            document.getElementById('file-editor-container').style.display = 'block';
            showAlert('success', 'File loaded successfully');
        } else {
            showAlert('danger', 'Failed to load file: ' + result.error);
        }
    } catch (error) {
        showAlert('danger', 'Error loading file: ' + error.message);
    }
}

/**
 * Load file (quick access)
 */
function loadFileQuick(filepath) {
    document.getElementById('file-path').value = filepath;
    loadFile();
}

/**
 * Save file
 */
async function saveFile() {
    const filepath = document.getElementById('file-path').value.trim();
    const content = document.getElementById('file-content').value;
    
    if (!filepath) {
        showAlert('warning', 'Please enter a file path');
        return;
    }
    
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
            showAlert('success', 'File saved successfully');
        } else {
            showAlert('danger', 'Failed to save file: ' + result.error);
        }
    } catch (error) {
        showAlert('danger', 'Error saving file: ' + error.message);
    }
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
 * Load technical design content
 */
async function loadTechnicalDesign() {
    const textarea = document.getElementById('technical-design-content');
    
    try {
        const response = await fetch('/api/file/specifications/technical-design.json?token=' + sessionToken);
        const result = await response.json();
        
        if (result.success) {
            textarea.value = result.content || '';
        } else {
            showAlert('danger', 'Failed to load technical design: ' + result.error);
        }
    } catch (error) {
        showAlert('danger', 'Error loading technical design: ' + error.message);
    }
}

/**
 * Save technical design content
 */
async function saveTechnicalDesign() {
    const content = document.getElementById('technical-design-content').value;
    
    try {
        const response = await fetch('/api/file/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                token: sessionToken,
                filepath: 'specifications/technical-design.json',
                content: content
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('success', 'Technical design saved successfully');
        } else {
            showAlert('danger', 'Failed to save technical design: ' + result.error);
        }
    } catch (error) {
        showAlert('danger', 'Error saving technical design: ' + error.message);
    }
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
