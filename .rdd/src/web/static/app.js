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
        
        // Load initial data
        await loadRegistry();
        await loadPrompts();
        
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
    if (sectionName === 'workdir') {
        loadIterationStatus();
    }
}

/**
 * Show alert message
 */
function showAlert(type, message) {
    const alertContainer = document.getElementById('alert-container');
    const alertId = 'alert-' + Date.now();
    
    const alertHtml = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="bi bi-${getAlertIcon(type)}"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.innerHTML = alertHtml;
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
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
                        <th>Type</th>
                        <th>State</th>
                        <th>Executed</th>
                        <th>Parent ID</th>
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
        const type = prompt.type || '';
        const state = prompt.state || '';
        const parentId = prompt['parent-id'] || '-';
        const analyzeEnabled = prompt['analyze-enabled'] || false;
        const planEnabled = prompt['plan-enabled'] || false;
        const executed = prompt['executed'] || false;
        
        const stateBadge = getStateBadge(state);
        const typeBadge = getTypeBadge(type);
        
        // Executed badge
        const executedBadge = executed 
            ? '<span class="badge bg-success"><i class="bi bi-check-circle"></i> Yes</span>'
            : '<span class="badge bg-secondary">No</span>';
        
        // Determine if prompt is editable (draft, planned, in-progress)
        const isEditable = (state === 'draft' || state === 'planned' || state === 'in-progress');
        const buttonType = isEditable ? 'primary' : 'secondary';
        const buttonLabel = isEditable ? 'Edit' : 'View';
        const buttonIcon = isEditable ? 'pencil' : 'eye';
        
        // Analyze toggle (only for non-completed prompts)
        let analyzeToggleHtml = '';
        if (state !== 'completed') {
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
        
        // Plan toggle (only for non-completed prompts)
        let planToggleHtml = '';
        if (state !== 'completed') {
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
        
        // Complete button (only for in-progress prompts with executed=true)
        let completeButtonHtml = '';
        if (state === 'in-progress') {
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
                <td>${typeBadge}</td>
                <td>${stateBadge}</td>
                <td>${executedBadge}</td>
                <td>${parentId === null ? '-' : '<code>' + parentId + '</code>'}</td>
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
        'draft': '<span class="badge bg-secondary">Draft</span>',
        'planned': '<span class="badge bg-info">Planned</span>',
        'in-progress': '<span class="badge bg-primary">In Progress</span>',
        'completed': '<span class="badge bg-success">Completed</span>'
    };
    return badges[state] || '<span class="badge bg-light text-dark">' + state + '</span>';
}

/**
 * Get badge HTML for type
 */
function getTypeBadge(type) {
    const badges = {
        'main': '<span class="badge bg-primary">Main</span>',
        'modification': '<span class="badge bg-warning text-dark">Modification</span>'
    };
    return badges[type] || '<span class="badge bg-light text-dark">' + type + '</span>';
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
    document.getElementById('prompt-type').value = 'main';
    document.getElementById('prompt-state').value = 'draft';
    document.getElementById('prompt-parent-id').value = '';
    
    modal.show();
}

/**
 * Create a new prompt
 */
async function createPrompt() {
    const title = document.getElementById('prompt-title').value.trim();
    const type = document.getElementById('prompt-type').value;
    const state = document.getElementById('prompt-state').value;
    const parentId = document.getElementById('prompt-parent-id').value.trim();
    
    if (!title) {
        showAlert('warning', 'Please enter a prompt title');
        return;
    }
    
    const params = {
        title: title,
        type: type,
        state: state
    };
    
    if (parentId) {
        params['parent-id'] = parentId;
    }
    
    const result = await executeAction('prompt', 'create', params);
    
    if (result.success) {
        showAlert('success', 'Prompt created successfully: ' + result.stdout.trim());
        
        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('createPromptModal'));
        modal.hide();
        
        // Reload prompts
        await loadPrompts();
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
        
        // Reload prompts
        await loadPrompts();
    } else {
        showAlert('danger', 'Failed to set prompt state: ' + (result.error || result.stderr));
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
        
        // Reload prompts list
        await loadPrompts();
    } else {
        showAlert('danger', `Failed to complete prompt: ` + (result.error || result.stderr));
    }
}

/**
 * Create new workdir
 */
async function createWorkdir() {
    const name = document.getElementById('iteration-name').value.trim();
    
    if (!name) {
        showAlert('warning', 'Please enter an iteration name');
        return;
    }
    
    const result = await executeAction('workdir', 'new-setup', { name: name });
    
    if (result.success) {
        showAlert('success', 'Work iteration created successfully');
        document.getElementById('iteration-name').value = '';
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
    const container = document.getElementById('iteration-status');
    container.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div>';
    
    await loadRegistry();
    
    if (!currentRegistry) {
        container.innerHTML = '<p class="text-warning">No work iteration registry found.</p>';
        return;
    }
    
    const html = `
        <dl class="row mb-0">
            <dt class="col-sm-3">Iteration ID:</dt>
            <dd class="col-sm-9"><code>${currentRegistry['iteration-id']}</code></dd>
            
            <dt class="col-sm-3">Iteration Name:</dt>
            <dd class="col-sm-9">${escapeHtml(currentRegistry['iteration-name'])}</dd>
            
            <dt class="col-sm-3">Total Prompts:</dt>
            <dd class="col-sm-9">${currentRegistry.prompts ? currentRegistry.prompts.length : 0}</dd>
            
            <dt class="col-sm-3">Next Prompt ID:</dt>
            <dd class="col-sm-9"><code>P-${String(currentRegistry['prompt-id-sequence-next-value']).padStart(3, '0')}</code></dd>
        </dl>
    `;
    
    container.innerHTML = html;
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
