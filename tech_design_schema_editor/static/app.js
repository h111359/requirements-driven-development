/**
 * Technical Design Schema Editor - Client Application
 * 
 * Manages loading, editing, and saving the technical design schema.
 */

// Global state
let schema = null;
let currentView = 'welcome'; // 'welcome', 'category', 'question'
let currentCategory = null;
let currentQuestion = null;
let isModified = false;
let isSaving = false;
let expandedCategories = new Set();
let selectedItem = null; // Track selected item for keyboard shortcuts: {type: 'category'|'question'|'option', data: {...}}

// DOM elements
const elements = {};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initElements();
    attachEventListeners();
    attachKeyboardShortcuts();
    loadSchema();
});

/**
 * Array reordering helper functions
 */
function moveItemUp(array, index) {
    if (index <= 0 || index >= array.length) return false;
    [array[index - 1], array[index]] = [array[index], array[index - 1]];
    return true;
}

function moveItemDown(array, index) {
    if (index < 0 || index >= array.length - 1) return false;
    [array[index], array[index + 1]] = [array[index + 1], array[index]];
    return true;
}

/**
 * Cache DOM elements for faster access
 */
function initElements() {
    // Navigation buttons
    elements.btnValidate = document.getElementById('btnValidate');
    elements.btnBackup = document.getElementById('btnBackup');
    
    // Sidebar
    elements.searchInput = document.getElementById('searchInput');
    elements.btnAddCategory = document.getElementById('btnAddCategory');
    elements.btnExpandAll = document.getElementById('btnExpandAll');
    elements.treeContainer = document.getElementById('treeContainer');
    
    // Editor views
    elements.welcomeScreen = document.getElementById('welcomeScreen');
    elements.categoryEditor = document.getElementById('categoryEditor');
    elements.questionEditor = document.getElementById('questionEditor');
    
    // Category form
    elements.categoryForm = document.getElementById('categoryForm');
    elements.categoryId = document.getElementById('categoryId');
    elements.categoryLabel = document.getElementById('categoryLabel');
    elements.categoryDescription = document.getElementById('categoryDescription');
    elements.btnAddQuestion = document.getElementById('btnAddQuestion');
    elements.btnDeleteCategory = document.getElementById('btnDeleteCategory');
    
    // Question form
    elements.questionForm = document.getElementById('questionForm');
    elements.questionId = document.getElementById('questionId');
    elements.questionLabel = document.getElementById('questionLabel');
    elements.questionType = document.getElementById('questionType');
    elements.questionHelp = document.getElementById('questionHelp');
    elements.questionVisibleWhen = document.getElementById('questionVisibleWhen');
    elements.optionsGroup = document.getElementById('optionsGroup');
    elements.optionsList = document.getElementById('optionsList');
    elements.btnAddOption = document.getElementById('btnAddOption');
    elements.allowOtherGroup = document.getElementById('allowOtherGroup');
    elements.questionAllowOther = document.getElementById('questionAllowOther');
    elements.questionOtherPlaceholder = document.getElementById('questionOtherPlaceholder');
    elements.btnDeleteQuestion = document.getElementById('btnDeleteQuestion');
    
    // Status bar
    elements.statusMessage = document.getElementById('statusMessage');
    elements.statusCategories = document.getElementById('statusCategories');
    elements.statusQuestions = document.getElementById('statusQuestions');
    elements.statusModified = document.getElementById('statusModified');
}

/**
 * Attach event listeners to UI elements
 */
function attachEventListeners() {
    // Navigation buttons
    elements.btnValidate.addEventListener('click', validateSchema);
    elements.btnBackup.addEventListener('click', createBackup);
    
    // Sidebar
    elements.searchInput.addEventListener('input', handleSearch);
    elements.btnAddCategory.addEventListener('click', addNewCategory);
    elements.btnExpandAll.addEventListener('click', toggleExpandAll);
    
    // Category form
    elements.categoryForm.addEventListener('submit', saveCategoryChanges);
    elements.btnAddQuestion.addEventListener('click', addNewQuestion);
    elements.btnDeleteCategory.addEventListener('click', deleteCategory);
    
    // Category field updates on blur (validate and save)
    elements.categoryId.addEventListener('blur', updateCategoryId);
    elements.categoryLabel.addEventListener('blur', updateCategoryLabel);
    elements.categoryDescription.addEventListener('blur', updateCategoryDescription);
    
    // Question form
    elements.questionForm.addEventListener('submit', saveQuestionChanges);
    elements.questionType.addEventListener('change', handleQuestionTypeChange);
    elements.btnAddOption.addEventListener('click', addNewOption);
    elements.btnDeleteQuestion.addEventListener('click', deleteQuestion);
    
    // Question field updates on blur (validate and save)
    elements.questionId.addEventListener('blur', updateQuestionId);
    elements.questionLabel.addEventListener('blur', updateQuestionLabel);
    elements.questionType.addEventListener('blur', updateQuestionType);
    elements.questionHelp.addEventListener('blur', updateQuestionHelp);
    elements.questionVisibleWhen.addEventListener('blur', updateQuestionVisibleWhen);
    elements.questionAllowOther.addEventListener('change', updateQuestionAllowOther);
    elements.questionOtherPlaceholder.addEventListener('blur', updateQuestionOtherPlaceholder);
    
    // Condition builder event listeners
    const btnToggleVisibleWhenMode = document.getElementById('btnToggleVisibleWhenMode');
    const btnAddCondition = document.getElementById('btnAddCondition');
    const btnConvertLegacy = document.getElementById('btnConvertLegacy');
    if (btnToggleVisibleWhenMode) btnToggleVisibleWhenMode.addEventListener('click', toggleVisibleWhenMode);
    if (btnAddCondition) btnAddCondition.addEventListener('click', addConditionRow);
    if (btnConvertLegacy) btnConvertLegacy.addEventListener('click', convertLegacyExpressionToBuilder);
}

/**
 * Attach global keyboard shortcuts
 */
function attachKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Alt+Up or Alt+Down for reordering
        if (e.altKey && (e.code === 'ArrowUp' || e.code === 'ArrowDown')) {
            e.preventDefault();
            
            const direction = e.code === 'ArrowUp' ? 'up' : 'down';
            
            // Determine what to move based on current view
            if (currentView === 'category' && currentCategory !== null) {
                // Move current category
                const catIndex = currentCategory;
                if (direction === 'up') {
                    if (moveItemUp(schema.categories, catIndex)) {
                        currentCategory = catIndex - 1;
                        setModified(true);
                        renderTree();
                        showCategoryEditor(currentCategory);
                    }
                } else {
                    if (moveItemDown(schema.categories, catIndex)) {
                        currentCategory = catIndex + 1;
                        setModified(true);
                        renderTree();
                        showCategoryEditor(currentCategory);
                    }
                }
            } else if (currentView === 'question' && currentCategory !== null && currentQuestion !== null) {
                // Move current question
                const qIndex = currentQuestion;
                const questions = schema.categories[currentCategory].questions;
                if (direction === 'up') {
                    if (moveItemUp(questions, qIndex)) {
                        currentQuestion = qIndex - 1;
                        setModified(true);
                        renderTree();
                        showQuestionEditor(currentCategory, currentQuestion);
                    }
                } else {
                    if (moveItemDown(questions, qIndex)) {
                        currentQuestion = qIndex + 1;
                        setModified(true);
                        renderTree();
                        showQuestionEditor(currentCategory, currentQuestion);
                    }
                }
            }
        }
    });
}

/**
 * Load schema from server
 */
async function loadSchema() {
    try {
        showStatus('Loading schema...', 'info');
        
        const response = await fetch('/api/schema');
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to load schema');
        }
        
        schema = data.schema;
        isModified = false;
        
        renderTree();
        updateStatusBar();
        showStatus('Schema loaded successfully', 'success');
        
    } catch (error) {
        console.error('Error loading schema:', error);
        showStatus(`Error: ${error.message}`, 'error');
    }
}

/**
 * Save schema to server
 */
async function saveSchema() {
    // Auto-save handles all saves now
    await autoSave();
}

/**
 * Validate schema without saving
 */
async function validateSchema() {
    try {
        showStatus('Validating schema...', 'info');
        
        const response = await fetch('/api/validate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ schema })
        });
        
        const data = await response.json();
        
        if (data.valid) {
            showStatus('✓ Schema is valid!', 'success');
        } else {
            showValidationErrors(data.errors);
            showStatus(`✗ Validation failed: ${data.errors.length} error(s)`, 'error');
        }
        
    } catch (error) {
        console.error('Error validating schema:', error);
        showStatus(`Error: ${error.message}`, 'error');
    }
}

/**
 * Create backup
 */
async function createBackup() {
    try {
        showStatus('Creating backup...', 'info');
        
        const response = await fetch('/api/backup', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to create backup');
        }
        
        // Show validation warnings if present
        if (data.warnings && data.warnings.length > 0) {
            console.warn('Backup created with validation warnings:', data.warnings);
            showValidationErrors(data.warnings);
        }
        
        showStatus(data.message, data.warnings ? 'warning' : 'success');
        
    } catch (error) {
        console.error('Error creating backup:', error);
        showStatus(`Error: ${error.message}`, 'error');
    }
}

/**
 * Render the category/question tree in the sidebar
 */
function renderTree() {
    if (!schema || !schema.categories) {
        elements.treeContainer.innerHTML = '<div class="empty-state"><p>No schema loaded</p></div>';
        return;
    }
    
    const searchTerm = elements.searchInput.value.toLowerCase();
    let html = '';
    
    schema.categories.forEach((category, catIndex) => {
        const questions = category.questions || [];
        const isExpanded = expandedCategories.has(category.id);
        const isActive = currentView === 'category' && currentCategory === catIndex;
        
        // Filter questions by search term
        const visibleQuestions = searchTerm ? 
            questions.filter(q => 
                (q.label || '').toLowerCase().includes(searchTerm) ||
                (q.id || '').toLowerCase().includes(searchTerm)
            ) : questions;
        
        // Skip category if search doesn't match and no questions match
        if (searchTerm && visibleQuestions.length === 0 && 
            !(category.label || '').toLowerCase().includes(searchTerm)) {
            return;
        }
        
        html += `
            <div class="tree-category">
                <div class="tree-category-header ${isActive ? 'active' : ''}" 
                     data-category="${catIndex}">
                    <span class="tree-toggle ${isExpanded ? 'expanded' : ''}">▶</span>
                    <span class="tree-category-label">${escapeHtml(category.label || category.id)}</span>
                    <span class="tree-item-count">${questions.length}</span>
                    <span class="tree-reorder-buttons">
                        <button class="btn-reorder" data-action="move-up" data-category="${catIndex}" 
                                aria-label="Move category up" ${catIndex === 0 ? 'disabled' : ''}>↑</button>
                        <button class="btn-reorder" data-action="move-down" data-category="${catIndex}" 
                                aria-label="Move category down" ${catIndex === schema.categories.length - 1 ? 'disabled' : ''}>↓</button>
                    </span>
                </div>
                <div class="tree-questions ${isExpanded ? 'expanded' : ''}">
        `;
        
        visibleQuestions.forEach((question, qIndex) => {
            const questionIndex = questions.indexOf(question);
            const isQuestionActive = currentView === 'question' && 
                                     currentCategory === catIndex && 
                                     currentQuestion === questionIndex;
            
            html += `
                <div class="tree-question ${isQuestionActive ? 'active' : ''}" 
                     data-category="${catIndex}" data-question="${questionIndex}">
                    <span class="tree-question-label">${escapeHtml(question.label || question.id)}</span>
                    <span class="tree-question-type">${question.type || 'text'}</span>
                    <span class="tree-reorder-buttons">
                        <button class="btn-reorder" data-action="move-up" data-category="${catIndex}" 
                                data-question="${questionIndex}" aria-label="Move question up" 
                                ${questionIndex === 0 ? 'disabled' : ''}>↑</button>
                        <button class="btn-reorder" data-action="move-down" data-category="${catIndex}" 
                                data-question="${questionIndex}" aria-label="Move question down" 
                                ${questionIndex === questions.length - 1 ? 'disabled' : ''}>↓</button>
                    </span>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    });
    
    elements.treeContainer.innerHTML = html;
    
    // Attach click handlers
    document.querySelectorAll('.tree-category-header').forEach(el => {
        el.addEventListener('click', (e) => {
            // Skip if clicking on reorder buttons
            if (e.target.classList.contains('btn-reorder')) return;
            
            const catIndex = parseInt(e.currentTarget.dataset.category);
            const category = schema.categories[catIndex];
            
            // Toggle expansion
            if (expandedCategories.has(category.id)) {
                expandedCategories.delete(category.id);
            } else {
                expandedCategories.add(category.id);
            }
            
            // Show category editor
            showCategoryEditor(catIndex);
            renderTree();
        });
    });
    
    document.querySelectorAll('.tree-question').forEach(el => {
        el.addEventListener('click', (e) => {
            // Skip if clicking on reorder buttons
            if (e.target.classList.contains('btn-reorder')) return;
            
            const catIndex = parseInt(e.currentTarget.dataset.category);
            const qIndex = parseInt(e.currentTarget.dataset.question);
            showQuestionEditor(catIndex, qIndex);
        });
    });
    
    // Attach reorder button handlers
    document.querySelectorAll('.btn-reorder').forEach(btn => {
        btn.addEventListener('click', handleReorderClick);
    });
}

/**
 * Handle reorder button clicks
 */
function handleReorderClick(e) {
    e.stopPropagation(); // Prevent triggering parent element clicks
    
    const btn = e.currentTarget;
    const action = btn.dataset.action;
    const catIndex = parseInt(btn.dataset.category);
    
    if (btn.dataset.question !== undefined) {
        // Reordering a question
        const qIndex = parseInt(btn.dataset.question);
        const category = schema.categories[catIndex];
        const questions = category.questions;
        
        if (action === 'move-up') {
            if (moveItemUp(questions, qIndex)) {
                setModified(true);
                // Update currentQuestion if we're viewing it
                if (currentView === 'question' && currentCategory === catIndex) {
                    if (currentQuestion === qIndex) {
                        currentQuestion = qIndex - 1;
                    } else if (currentQuestion === qIndex - 1) {
                        currentQuestion = qIndex;
                    }
                }
                renderTree();
                if (currentView === 'question') {
                    showQuestionEditor(currentCategory, currentQuestion);
                }
            }
        } else if (action === 'move-down') {
            if (moveItemDown(questions, qIndex)) {
                setModified(true);
                // Update currentQuestion if we're viewing it
                if (currentView === 'question' && currentCategory === catIndex) {
                    if (currentQuestion === qIndex) {
                        currentQuestion = qIndex + 1;
                    } else if (currentQuestion === qIndex + 1) {
                        currentQuestion = qIndex;
                    }
                }
                renderTree();
                if (currentView === 'question') {
                    showQuestionEditor(currentCategory, currentQuestion);
                }
            }
        }
    } else {
        // Reordering a category
        if (action === 'move-up') {
            if (moveItemUp(schema.categories, catIndex)) {
                setModified(true);
                // Update currentCategory if we're viewing it
                if (currentCategory === catIndex) {
                    currentCategory = catIndex - 1;
                } else if (currentCategory === catIndex - 1) {
                    currentCategory = catIndex;
                }
                renderTree();
                if (currentView === 'category') {
                    showCategoryEditor(currentCategory);
                } else if (currentView === 'question') {
                    showQuestionEditor(currentCategory, currentQuestion);
                }
            }
        } else if (action === 'move-down') {
            if (moveItemDown(schema.categories, catIndex)) {
                setModified(true);
                // Update currentCategory if we're viewing it
                if (currentCategory === catIndex) {
                    currentCategory = catIndex + 1;
                } else if (currentCategory === catIndex + 1) {
                    currentCategory = catIndex;
                }
                renderTree();
                if (currentView === 'category') {
                    showCategoryEditor(currentCategory);
                } else if (currentView === 'question') {
                    showQuestionEditor(currentCategory, currentQuestion);
                }
            }
        }
    }
}

/**
 * Show the category editor
 */
function showCategoryEditor(categoryIndex) {
    currentView = 'category';
    currentCategory = categoryIndex;
    currentQuestion = null;
    
    const category = schema.categories[categoryIndex];
    
    // Hide other views
    elements.welcomeScreen.classList.add('d-none');
    elements.questionEditor.classList.add('d-none');
    elements.categoryEditor.classList.remove('d-none');
    
    // Populate form
    elements.categoryId.value = category.id || '';
    elements.categoryLabel.value = category.label || '';
    elements.categoryDescription.value = category.description || '';
    
    document.getElementById('categoryEditorTitle').textContent = 
        `Edit Category: ${category.label || category.id}`;
    
    renderTree();
}

/**
 * Show the question editor
 */
function showQuestionEditor(categoryIndex, questionIndex) {
    currentView = 'question';
    currentCategory = categoryIndex;
    currentQuestion = questionIndex;
    
    const category = schema.categories[categoryIndex];
    const question = category.questions[questionIndex];
    
    // Hide other views
    elements.welcomeScreen.classList.add('d-none');
    elements.categoryEditor.classList.add('d-none');
    elements.questionEditor.classList.remove('d-none');
    
    // Populate form
    elements.questionId.value = question.id || '';
    elements.questionLabel.value = question.label || '';
    elements.questionType.value = question.type || 'text';
    elements.questionHelp.value = question.help || '';
    elements.questionVisibleWhen.value = question.visibleWhen || '';
    elements.questionAllowOther.checked = question.allowOther || false;
    elements.questionOtherPlaceholder.value = question.otherPlaceholder || '';
    
    document.getElementById('questionEditorTitle').textContent = 
        `${question.label || question.id}`;
    document.getElementById('questionEditorSubtitle').textContent = 
        `Category: ${category.label || category.id}`;
    
    // Handle question type-specific fields
    handleQuestionTypeChange();
    
    // Initialize condition builder
    initConditionBuilder(question.visibleWhen);
    
    // Render options if applicable
    if (['radio', 'multiselect', 'dropdown'].includes(question.type)) {
        renderOptions(question.options || []);
    }
    
    renderTree();
}

/**
 * Handle question type change
 */
function handleQuestionTypeChange() {
    const type = elements.questionType.value;
    const needsOptions = ['radio', 'multiselect', 'dropdown'].includes(type);
    
    elements.optionsGroup.style.display = needsOptions ? 'block' : 'none';
    elements.allowOtherGroup.style.display = needsOptions ? 'block' : 'none';
    
    if (needsOptions && currentView === 'question') {
        const question = schema.categories[currentCategory].questions[currentQuestion];
        renderOptions(question.options || []);
    }
    
    // Save the type change when user changes it
    updateQuestionType();
}

/**
 * Render options list
 */
function renderOptions(options) {
    if (!options || options.length === 0) {
        elements.optionsList.innerHTML = '<div style="padding: 1rem; text-align: center; color: #6c757d;">No options yet. Click "+ Add Option" to add one.</div>';
        return;
    }
    
    let html = '';
    options.forEach((option, index) => {
        const optionId = option.id || option.label || '';
        const optionLabel = option.label || option.id || '';
        
        html += `
            <div class="option-item" data-index="${index}">
                <div class="option-item-reorder">
                    <button type="button" class="btn-reorder" data-action="move-up" 
                            data-index="${index}" aria-label="Move option up" 
                            ${index === 0 ? 'disabled' : ''}>↑</button>
                    <button type="button" class="btn-reorder" data-action="move-down" 
                            data-index="${index}" aria-label="Move option down" 
                            ${index === options.length - 1 ? 'disabled' : ''}>↓</button>
                </div>
                <div class="option-item-content">
                    <input type="text" class="form-control mb-1" 
                           placeholder="Option ID" 
                           value="${escapeHtml(optionId)}"
                           data-field="id" data-index="${index}">
                    <input type="text" class="form-control" 
                           placeholder="Option Label" 
                           value="${escapeHtml(optionLabel)}"
                           data-field="label" data-index="${index}">
                </div>
                <div class="option-item-actions">
                    <button type="button" class="btn btn-sm btn-danger" 
                            data-action="delete" data-index="${index}">🗑️</button>
                </div>
            </div>
        `;
    });
    
    elements.optionsList.innerHTML = html;
    
    // Attach event listeners
    elements.optionsList.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', handleOptionChange);
    });
    
    elements.optionsList.querySelectorAll('[data-action="delete"]').forEach(btn => {
        btn.addEventListener('click', handleOptionDelete);
    });
    
    elements.optionsList.querySelectorAll('.btn-reorder').forEach(btn => {
        btn.addEventListener('click', handleOptionReorder);
    });
}

/**
 * Handle option field change
 */
function handleOptionChange(e) {
    const index = parseInt(e.target.dataset.index);
    const field = e.target.dataset.field;
    const value = e.target.value;
    
    const question = schema.categories[currentCategory].questions[currentQuestion];
    if (!question.options) question.options = [];
    if (!question.options[index]) question.options[index] = {};
    
    question.options[index][field] = value;
    markAsModified();
}

/**
 * Handle option deletion
 */
function handleOptionDelete(e) {
    const index = parseInt(e.target.dataset.index);
    const question = schema.categories[currentCategory].questions[currentQuestion];
    
    if (confirm('Delete this option?')) {
        question.options.splice(index, 1);
        renderOptions(question.options);
        markAsModified();
    }
}

/**
 * Handle option reordering
 */
function handleOptionReorder(e) {
    const btn = e.currentTarget;
    const action = btn.dataset.action;
    const index = parseInt(btn.dataset.index);
    
    const question = schema.categories[currentCategory].questions[currentQuestion];
    const options = question.options;
    
    if (action === 'move-up') {
        if (moveItemUp(options, index)) {
            setModified(true);
            renderOptions(options);
        }
    } else if (action === 'move-down') {
        if (moveItemDown(options, index)) {
            setModified(true);
            renderOptions(options);
        }
    }
}

/**
 * Add new option
 */
function addNewOption() {
    const question = schema.categories[currentCategory].questions[currentQuestion];
    if (!question.options) question.options = [];
    
    question.options.push({
        id: '',
        label: 'New Option'
    });
    
    renderOptions(question.options);
    markAsModified();
}

/**
 * Update category ID (validate and save on blur)
 */
function updateCategoryId() {
    if (currentView !== 'category' || currentCategory === null) return;
    
    const category = schema.categories[currentCategory];
    const newId = elements.categoryId.value.trim();
    const errorElement = document.getElementById('categoryIdError');
    
    if (!newId) {
        elements.categoryId.classList.add('is-invalid');
        errorElement.textContent = 'Category ID is required';
        return;
    }
    
    // Check for duplicate ID (if changed)
    if (newId !== category.id) {
        const duplicate = schema.categories.find((c, i) => 
            i !== currentCategory && c.id === newId
        );
        if (duplicate) {
            elements.categoryId.classList.add('is-invalid');
            errorElement.textContent = 'A category with this ID already exists';
            return;
        }
    }
    
    elements.categoryId.classList.remove('is-invalid');
    errorElement.textContent = '';
    
    // Update schema if valid and changed
    if (newId !== category.id) {
        const oldId = category.id;
        category.id = newId;
        
        // Update expanded categories set if ID changed
        if (expandedCategories.has(oldId)) {
            expandedCategories.delete(oldId);
            expandedCategories.add(newId);
        }
        
        markAsModified();
        renderTree();
    }
}

/**
 * Update category label (validate and save on blur)
 */
function updateCategoryLabel() {
    if (currentView !== 'category' || currentCategory === null) return;
    
    const category = schema.categories[currentCategory];
    const newLabel = elements.categoryLabel.value.trim();
    
    if (!newLabel) {
        elements.categoryLabel.classList.add('is-invalid');
        return;
    }
    
    elements.categoryLabel.classList.remove('is-invalid');
    
    // Update schema if changed
    if (newLabel !== category.label) {
        category.label = newLabel;
        markAsModified();
        renderTree();
    }
}

/**
 * Update category description (save on blur)
 */
function updateCategoryDescription() {
    if (currentView !== 'category' || currentCategory === null) return;
    
    const category = schema.categories[currentCategory];
    const newDescription = elements.categoryDescription.value.trim();
    
    // Update schema if changed
    if (newDescription !== category.description) {
        category.description = newDescription;
        markAsModified();
    }
}

/**
 * Validate category ID field
 */
function validateCategoryId() {
    const category = schema.categories[currentCategory];
    const newId = elements.categoryId.value.trim();
    const errorElement = document.getElementById('categoryIdError');
    
    if (!newId) {
        elements.categoryId.classList.add('is-invalid');
        errorElement.textContent = 'Category ID is required';
        return false;
    }
    
    // Check for duplicate ID (if changed)
    if (newId !== category.id) {
        const duplicate = schema.categories.find((c, i) => 
            i !== currentCategory && c.id === newId
        );
        if (duplicate) {
            elements.categoryId.classList.add('is-invalid');
            errorElement.textContent = 'A category with this ID already exists';
            return false;
        }
    }
    
    elements.categoryId.classList.remove('is-invalid');
    errorElement.textContent = '';
    return true;
}

/**
 * Validate category label field
 */
function validateCategoryLabel() {
    const newLabel = elements.categoryLabel.value.trim();
    
    if (!newLabel) {
        elements.categoryLabel.classList.add('is-invalid');
        return false;
    }
    
    elements.categoryLabel.classList.remove('is-invalid');
    return true;
}

/**
 * Update question ID (validate and save on blur)
 */
function updateQuestionId() {
    if (currentView !== 'question' || currentCategory === null || currentQuestion === null) return;
    
    const question = schema.categories[currentCategory].questions[currentQuestion];
    const newId = elements.questionId.value.trim();
    const errorElement = document.getElementById('questionIdError');
    
    if (!newId) {
        elements.questionId.classList.add('is-invalid');
        errorElement.textContent = 'Question ID is required';
        return;
    }
    
    // Check for duplicate ID (across all categories)
    let duplicate = false;
    for (let catIdx = 0; catIdx < schema.categories.length; catIdx++) {
        const cat = schema.categories[catIdx];
        for (let qIdx = 0; qIdx < (cat.questions || []).length; qIdx++) {
            if (catIdx === currentCategory && qIdx === currentQuestion) continue;
            if (cat.questions[qIdx].id === newId) {
                duplicate = true;
                break;
            }
        }
        if (duplicate) break;
    }
    
    if (duplicate) {
        elements.questionId.classList.add('is-invalid');
        errorElement.textContent = 'A question with this ID already exists';
        return;
    }
    
    elements.questionId.classList.remove('is-invalid');
    errorElement.textContent = '';
    
    // Update schema if valid and changed
    if (newId !== question.id) {
        question.id = newId;
        markAsModified();
        renderTree();
    }
}

/**
 * Update question label (validate and save on blur)
 */
function updateQuestionLabel() {
    if (currentView !== 'question' || currentCategory === null || currentQuestion === null) return;
    
    const question = schema.categories[currentCategory].questions[currentQuestion];
    const newLabel = elements.questionLabel.value.trim();
    
    if (!newLabel) {
        elements.questionLabel.classList.add('is-invalid');
        return;
    }
    
    elements.questionLabel.classList.remove('is-invalid');
    
    // Update schema if changed
    if (newLabel !== question.label) {
        question.label = newLabel;
        markAsModified();
        renderTree();
    }
}

/**
 * Update question type (validate and save on blur/change)
 */
function updateQuestionType() {
    if (currentView !== 'question' || currentCategory === null || currentQuestion === null) return;
    
    const question = schema.categories[currentCategory].questions[currentQuestion];
    const newType = elements.questionType.value;
    
    if (!newType) {
        elements.questionType.classList.add('is-invalid');
        return;
    }
    
    elements.questionType.classList.remove('is-invalid');
    
    // Update schema if changed
    if (newType !== question.type) {
        question.type = newType;
        
        // Handle options for choice-based questions
        if (['radio', 'multiselect', 'dropdown'].includes(newType)) {
            if (!question.options) {
                question.options = [];
            }
        } else {
            // Remove options-related fields for non-choice questions
            delete question.options;
            delete question.allowOther;
            delete question.otherPlaceholder;
        }
        
        markAsModified();
        // Don't call handleQuestionTypeChange here as it will be called by the change event
    }
}

/**
 * Update question help text (save on blur)
 */
function updateQuestionHelp() {
    if (currentView !== 'question' || currentCategory === null || currentQuestion === null) return;
    
    const question = schema.categories[currentCategory].questions[currentQuestion];
    const newHelp = elements.questionHelp.value.trim();
    
    // Update schema if changed
    if (newHelp !== (question.help || '')) {
        question.help = newHelp;
        markAsModified();
    }
}

/**
 * Update question visibleWhen (save on blur)
 */
function updateQuestionVisibleWhen() {
    if (currentView !== 'question' || currentCategory === null || currentQuestion === null) return;
    
    const question = schema.categories[currentCategory].questions[currentQuestion];
    const newVisibleWhen = elements.questionVisibleWhen.value.trim();
    
    // Update schema if changed
    const currentValue = question.visibleWhen || '';
    if (newVisibleWhen !== currentValue) {
        question.visibleWhen = newVisibleWhen || undefined;
        markAsModified();
    }
}

/**
 * Condition Builder Functions
 */

/**
 * Normalize visibleWhen conditions from old format to new format
 * Old format: {questionId, equals: [...]}
 * New format: {questionId, operator, value}
 */
function normalizeVisibleWhenConditions(conditions) {
    if (!Array.isArray(conditions)) return [];
    
    return conditions.map(cond => {
        // Check if old format (has 'equals' property)
        if (cond.equals !== undefined) {
            console.log('Converting old format condition to new format:', cond);
            return {
                questionId: cond.questionId || '',
                operator: 'equals',
                value: cond.equals // Keep as array or single value
            };
        }
        
        // Already in new format or needs other handling
        return {
            questionId: cond.questionId || '',
            operator: cond.operator || 'equals',
            value: cond.value || ''
        };
    });
}

/**
 * Initialize the condition builder UI
 */
function initConditionBuilder(visibleWhenData) {
    if (!schema || !schema.categories) return;
    
    const container = document.getElementById('conditionBuilderContainer');
    const legacyContainer = document.getElementById('legacyVisibleWhenContainer');
    if (!container || !legacyContainer) return;
    
    // Parse visibleWhenData - could be array (new format) or string (legacy format)
    let conditions = [];
    let isLegacy = false;
    
    if (typeof visibleWhenData === 'string' && visibleWhenData.trim()) {
        // Legacy string format - attempt to parse
        isLegacy = true;
        elements.questionVisibleWhen.value = visibleWhenData;
        
        // Attempt to convert legacy expression
        conditions = parseLegacyExpression(visibleWhenData);
        
        // Show warning if legacy format detected
        const legacyWarning = document.getElementById('legacyWarning');
        if (legacyWarning) {
            if (conditions.length === 0) {
                // Parsing failed
                legacyWarning.style.display = 'block';
                container.style.display = 'none';
                legacyContainer.style.display = 'block';
                return;
            } else {
                // Parsing succeeded - show option to convert
                legacyWarning.style.display = 'block';
            }
        }
    } else if (Array.isArray(visibleWhenData)) {
        // Array format - could be old or new
        // Normalize to new format {questionId, operator, value}
        conditions = normalizeVisibleWhenConditions(visibleWhenData);
    }
    
    // Store conditions in global state
    window.currentConditions = conditions;
    
    // Render condition rows
    renderConditionRows();
}

/**
 * Get options for a specific question
 * Returns array of {id, label} objects
 */
function getOptionsForQuestion(questionId) {
    if (!questionId) return [];
    
    for (let cat of schema.categories) {
        const q = cat.questions.find(q => q.id === questionId);
        if (q && q.options && Array.isArray(q.options)) {
            // Convert options to {id, label} format if needed
            return q.options.map(opt => {
                if (typeof opt === 'string') {
                    return { id: opt, label: opt };
                } else if (opt.id && opt.label) {
                    return { id: opt.id, label: opt.label };
                }
                return null;
            }).filter(opt => opt !== null);
        }
    }
    
    return [];
}

/**
 * Get a question by ID
 */
function getQuestionById(questionId) {
    if (!questionId) return null;
    
    for (let cat of schema.categories) {
        const q = cat.questions.find(q => q.id === questionId);
        if (q) return q;
    }
    
    return null;
}

/**
 * Check if a question has predefined options
 */
function hasOptionsQuestion(questionId) {
    const question = getQuestionById(questionId);
    if (!question) return false;
    
    const optionBasedTypes = ['radio', 'dropdown', 'multiselect'];
    return optionBasedTypes.includes(question.type) && 
           question.options && 
           Array.isArray(question.options) && 
           question.options.length > 0;
}

/**
 * Update the value field for a condition row based on the selected question
 * This allows updating just the value field without re-rendering the entire row
 */
function updateConditionValueField(index, questionId) {
    const row = document.querySelector(`.condition-row[data-index="${index}"]`);
    if (!row) return;
    
    const valueFieldContainer = row.querySelector('.condition-row-field:nth-child(4)');
    if (!valueFieldContainer) return;
    
    const condition = window.currentConditions[index] || {};
    const selectedValue = condition.value || '';
    
    // Check if the referenced question has predefined options
    if (questionId && hasOptionsQuestion(questionId)) {
        // Question has options - create dropdown selector
        const options = getOptionsForQuestion(questionId);
        const question = getQuestionById(questionId);
        const isMultiselect = question && question.type === 'multiselect';
        
        // For multiselect questions, handle array values
        let selectedValues = [];
        if (Array.isArray(selectedValue)) {
            selectedValues = selectedValue;
        } else if (selectedValue) {
            selectedValues = [selectedValue];
        }
        
        if (isMultiselect) {
            // Multiple select dropdown for multiselect questions
            valueFieldContainer.innerHTML = `
                <label>Value</label>
                <select class="condition-value-select condition-value-multiselect" data-index="${index}" multiple>
                    ${options.map(opt => 
                        `<option value="${escapeHtml(opt.id)}" ${selectedValues.includes(opt.id) ? 'selected' : ''}>${escapeHtml(opt.label)}</option>`
                    ).join('')}
                </select>
                <div class="form-text" style="font-size: 0.75rem; margin-top: 0.25rem;">Select one or more values (OR logic)</div>
            `;
            
            // Re-attach event listener for the new multiselect element
            const valueMultiselect = valueFieldContainer.querySelector('.condition-value-multiselect');
            if (valueMultiselect) {
                valueMultiselect.addEventListener('change', (e) => handleConditionValueChangeMultiselect(e, index));
            }
        } else {
            // Regular single-select dropdown for radio/dropdown questions
            valueFieldContainer.innerHTML = `
                <label>Value</label>
                <select class="condition-value-select" data-index="${index}">
                    <option value="">-- Select Value --</option>
                    ${options.map(opt => 
                        `<option value="${escapeHtml(opt.id)}" ${selectedValues[0] === opt.id ? 'selected' : ''}>${escapeHtml(opt.label)}</option>`
                    ).join('')}
                </select>
            `;
            
            // Re-attach event listener for the new select element
            const valueSelect = valueFieldContainer.querySelector('.condition-value-select');
            if (valueSelect) {
                valueSelect.addEventListener('change', (e) => handleConditionValueChangeSelect(e, index));
            }
        }
    } else {
        // Question has no options or no question selected - use text input
        const valueStr = Array.isArray(selectedValue) ? JSON.stringify(selectedValue) : selectedValue;
        valueFieldContainer.innerHTML = `
            <label>Value</label>
            <input type="text" class="condition-value-input" data-index="${index}" value="${escapeHtml(valueStr)}" placeholder="Value...">
        `;
        
        // Re-attach event listener for the new input element
        const valueInput = valueFieldContainer.querySelector('.condition-value-input');
        if (valueInput) {
            valueInput.addEventListener('blur', (e) => handleConditionValueChange(e, index));
        }
    }
}

/**
 * Render condition rows in the builder
 */
function renderConditionRows() {
    const container = document.getElementById('conditionRowsContainer');
    const countSpan = document.getElementById('conditionCount');
    if (!container) return;
    
    const conditions = window.currentConditions || [];
    
    // Update count
    if (countSpan) countSpan.textContent = conditions.length;
    
    // Clear existing rows
    container.innerHTML = '';
    
    // Render each condition
    conditions.forEach((condition, index) => {
        const row = createConditionRow(condition, index);
        container.appendChild(row);
    });
}

/**
 * Create a single condition row element
 */
function createConditionRow(condition, index) {
    const row = document.createElement('div');
    row.className = 'condition-row';
    row.dataset.index = index;
    
    const condition_obj = condition || {};
    const selectedCategory = getCurrentCategoryForQuestion(condition_obj.questionId);
    const selectedQuestion = condition_obj.questionId || '';
    const selectedValue = condition_obj.value || '';
    
    // Category selector
    const categoryField = document.createElement('div');
    categoryField.className = 'condition-row-field';
    categoryField.innerHTML = `
        <label>Category</label>
        <select class="condition-category-select" data-index="${index}">
            <option value="">-- Select Category --</option>
            ${getCategories().map(cat => 
                `<option value="${cat.id}" ${cat.id === selectedCategory ? 'selected' : ''}>${cat.label}</option>`
            ).join('')}
        </select>
    `;
    
    // Question selector
    const questionField = document.createElement('div');
    questionField.className = 'condition-row-field';
    questionField.innerHTML = `
        <label>Question</label>
        <select class="condition-question-select" data-index="${index}">
            <option value="">-- Select Question --</option>
            ${getQuestionsForCategory(selectedCategory).map(q => 
                `<option value="${q.id}" ${q.id === selectedQuestion ? 'selected' : ''}>${q.label} (${q.id})</option>`
            ).join('')}
        </select>
    `;
    
    // Value field - dynamic based on question type
    const valueField = document.createElement('div');
    valueField.className = 'condition-row-field';
    
    // Check if the referenced question has predefined options
    if (selectedQuestion && hasOptionsQuestion(selectedQuestion)) {
        // Question has options - create dropdown selector (Q3 decision: display labels, store IDs)
        const options = getOptionsForQuestion(selectedQuestion);
        const question = getQuestionById(selectedQuestion);
        const isMultiselect = question && question.type === 'multiselect';
        
        // For multiselect questions, we need to handle array values
        let selectedValues = [];
        if (Array.isArray(selectedValue)) {
            selectedValues = selectedValue;
        } else if (selectedValue) {
            selectedValues = [selectedValue];
        }
        
        if (isMultiselect) {
            // Multiple select dropdown for multiselect questions (Q4 decision: support multiple values with OR logic)
            valueField.innerHTML = `
                <label>Value</label>
                <select class="condition-value-select condition-value-multiselect" data-index="${index}" multiple>
                    ${options.map(opt => 
                        `<option value="${escapeHtml(opt.id)}" ${selectedValues.includes(opt.id) ? 'selected' : ''}>${escapeHtml(opt.label)}</option>`
                    ).join('')}
                </select>
                <div class="form-text" style="font-size: 0.75rem; margin-top: 0.25rem;">Select one or more values (OR logic)</div>
            `;
        } else {
            // Regular single-select dropdown for radio/dropdown questions
            valueField.innerHTML = `
                <label>Value</label>
                <select class="condition-value-select" data-index="${index}">
                    <option value="">-- Select Value --</option>
                    ${options.map(opt => 
                        `<option value="${escapeHtml(opt.id)}" ${selectedValues[0] === opt.id ? 'selected' : ''}>${escapeHtml(opt.label)}</option>`
                    ).join('')}
                </select>
            `;
        }
    } else {
        // Question has no options or no question selected - use text input (Q2 decision: keep text input for free-text questions)
        const valueStr = Array.isArray(selectedValue) ? JSON.stringify(selectedValue) : selectedValue;
        valueField.innerHTML = `
            <label>Value</label>
            <input type="text" class="condition-value-input" data-index="${index}" value="${escapeHtml(valueStr)}" placeholder="Value...">
        `;
    }
    
    // Remove button
    const removeField = document.createElement('div');
    removeField.className = 'condition-row-field';
    removeField.innerHTML = `<button type="button" class="btn-remove-condition" data-index="${index}">✕</button>`;
    
    row.appendChild(categoryField);
    row.appendChild(questionField);
    row.appendChild(valueField);
    row.appendChild(removeField);
    
    // Attach event listeners
    const categorySelect = row.querySelector('.condition-category-select');
    const questionSelect = row.querySelector('.condition-question-select');
    const valueInput = row.querySelector('.condition-value-input');
    const valueSelect = row.querySelector('.condition-value-select');
    const valueMultiselect = row.querySelector('.condition-value-multiselect');
    const removeBtn = row.querySelector('.btn-remove-condition');
    
    categorySelect.addEventListener('change', (e) => handleConditionCategoryChange(e, index));
    questionSelect.addEventListener('change', (e) => handleConditionQuestionChange(e, index));
    
    // Attach appropriate value field listener based on type
    if (valueMultiselect) {
        // Multiselect dropdown - store as array
        valueMultiselect.addEventListener('change', (e) => handleConditionValueChangeMultiselect(e, index));
    } else if (valueSelect) {
        // Single-select dropdown for options
        valueSelect.addEventListener('change', (e) => handleConditionValueChangeSelect(e, index));
    } else if (valueInput) {
        // Text input for free-text questions
        valueInput.addEventListener('blur', (e) => handleConditionValueChange(e, index));
    }
    
    removeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        removeConditionRow(index);
    });
    
    return row;
}

/**
 * Handle condition category change
 */
function handleConditionCategoryChange(event, index) {
    const category = event.target.value;
    // Update questions dropdown when category changes
    const row = document.querySelector(`.condition-row[data-index="${index}"]`);
    if (!row) return;
    
    const questionSelect = row.querySelector('.condition-question-select');
    if (!questionSelect) return;
    
    const questions = getQuestionsForCategory(category);
    questionSelect.innerHTML = '<option value="">-- Select Question --</option>' + 
        questions.map(q => `<option value="${q.id}">${q.label} (${q.id})</option>`).join('');
    
    // Clear condition when category changes (operator always 'equals')
    if (window.currentConditions[index]) {
        window.currentConditions[index].questionId = '';
        window.currentConditions[index].operator = 'equals';
        window.currentConditions[index].value = '';
    }
    
    saveConditionsToQuestion();
}

/**
 * Handle condition question change
 */
function handleConditionQuestionChange(event, index) {
    const questionId = event.target.value;
    
    if (!window.currentConditions[index]) {
        window.currentConditions[index] = {};
    }
    
    window.currentConditions[index].questionId = questionId;
    window.currentConditions[index].operator = 'equals';
    window.currentConditions[index].value = '';
    
    // Update the value field based on the selected question type
    updateConditionValueField(index, questionId);
    
    saveConditionsToQuestion();
}

/**
 * Handle condition value change for select dropdown (option-based questions)
 * Stores the option ID (Q3 decision: store IDs for stability)
 */
function handleConditionValueChangeSelect(event, index) {
    if (!window.currentConditions[index]) {
        window.currentConditions[index] = {};
    }
    
    const selectedValue = event.target.value;
    window.currentConditions[index].value = selectedValue;
    
    saveConditionsToQuestion();
}

/**
 * Handle condition value change for multiselect dropdown
 * Stores as array to support OR logic (Q4 decision: "B" - Allow selecting multiple values)
 */
function handleConditionValueChangeMultiselect(event, index) {
    if (!window.currentConditions[index]) {
        window.currentConditions[index] = {};
    }
    
    // Get selected values from multiselect dropdown (option IDs)
    const selectedOptions = Array.from(event.target.selectedOptions);
    const selectedValues = selectedOptions.map(opt => opt.value);
    
    // Store as array (empty array if nothing selected, or as array of IDs)
    window.currentConditions[index].value = selectedValues.length > 0 ? selectedValues : '';
    
    saveConditionsToQuestion();
}

/**
 * Handle condition value change
 */
function handleConditionValueChange(event, index) {
    if (!window.currentConditions[index]) {
        window.currentConditions[index] = {};
    }
    
    window.currentConditions[index].value = event.target.value;
    saveConditionsToQuestion();
}

/**
 * Add a new condition row
 */
function addConditionRow() {
    if (!window.currentConditions) {
        window.currentConditions = [];
    }
    
    window.currentConditions.push({
        questionId: '',
        operator: 'equals',
        value: ''
    });
    
    renderConditionRows();
}

/**
 * Remove a condition row
 */
function removeConditionRow(index) {
    if (!window.currentConditions) return;
    
    window.currentConditions.splice(index, 1);
    renderConditionRows();
    saveConditionsToQuestion();
}

/**
 * Save conditions to the current question's visibleWhen property
 * Includes validation for equals arrays (Q4 decision: validate for duplicates and valid option IDs)
 */
function saveConditionsToQuestion() {
    if (currentView !== 'question' || currentCategory === null || currentQuestion === null) return;
    
    const question = schema.categories[currentCategory].questions[currentQuestion];
    const conditions = window.currentConditions || [];
    
    if (conditions.length > 0) {
        // Validate and transform conditions to visibleWhen format
        const visibleWhenRules = [];
        const errors = [];
        
        conditions.forEach((condition, index) => {
            // Skip incomplete conditions
            if (!condition.questionId) {
                return;
            }
            
            // Ensure operator is always 'equals' (only implemented operator)
            condition.operator = 'equals';
            
            // Store the rule with 'equals' field
            const rule = {
                questionId: condition.questionId,
                equals: condition.value
            };
            
            // Validate if value is an array (OR logic case)
            if (Array.isArray(condition.value)) {
                // Q4 validation: Check for duplicates
                const uniqueValues = [...new Set(condition.value)];
                if (uniqueValues.length !== condition.value.length) {
                    errors.push(`Condition ${index + 1}: Duplicate values detected in equals array`);
                }
                
                // Q4 validation: Check for valid option IDs if the question has options
                const referencedQuestion = getQuestionById(condition.questionId);
                if (referencedQuestion && hasOptionsQuestion(condition.questionId)) {
                    const validOptionIds = getOptionsForQuestion(condition.questionId).map(opt => opt.id);
                    const invalidValues = condition.value.filter(val => !validOptionIds.includes(val));
                    
                    if (invalidValues.length > 0) {
                        errors.push(`Condition ${index + 1}: Invalid option IDs: ${invalidValues.join(', ')}`);
                    }
                }
                
                // Q1 decision: Support both string and array
                // Convert single-element array to string for cleaner JSON
                if (condition.value.length === 1) {
                    rule.equals = condition.value[0];
                } else if (condition.value.length === 0) {
                    // Empty array - skip this condition
                    return;
                }
                // else: keep as array for OR logic
            } else if (condition.value) {
                // String value - validate if question has options
                const referencedQuestion = getQuestionById(condition.questionId);
                if (referencedQuestion && hasOptionsQuestion(condition.questionId)) {
                    const validOptionIds = getOptionsForQuestion(condition.questionId).map(opt => opt.id);
                    if (!validOptionIds.includes(condition.value)) {
                        errors.push(`Condition ${index + 1}: Invalid option ID: ${condition.value}`);
                    }
                }
            }
            
            visibleWhenRules.push(rule);
        });
        
        // Display errors if any
        if (errors.length > 0) {
            console.error('Conditional visibility validation errors:', errors);
            console.warn('Validation errors in conditional visibility: ' + errors.join('; '));
        }
        
        question.visibleWhen = visibleWhenRules.length > 0 ? visibleWhenRules : undefined;
    } else {
        question.visibleWhen = undefined;
    }
    
    // Update textarea
    elements.questionVisibleWhen.value = JSON.stringify(question.visibleWhen || [], null, 2);
    markAsModified();
}

/**
 * Toggle between builder mode and advanced (textarea) mode
 */
function toggleVisibleWhenMode() {
    const builderContainer = document.getElementById('conditionBuilderContainer');
    const legacyContainer = document.getElementById('legacyVisibleWhenContainer');
    
    if (builderContainer && legacyContainer) {
        const isBuilderVisible = builderContainer.style.display !== 'none';
        
        if (isBuilderVisible) {
            // Switch to legacy mode
            builderContainer.style.display = 'none';
            legacyContainer.style.display = 'block';
        } else {
            // Switch to builder mode
            legacyContainer.style.display = 'none';
            builderContainer.style.display = 'block';
        }
    }
}

/**
 * Get all categories
 */
function getCategories() {
    if (!schema || !schema.categories) return [];
    return schema.categories;
}

/**
 * Get questions for a specific category
 */
function getQuestionsForCategory(categoryId) {
    if (!schema || !schema.categories) return [];
    
    const category = schema.categories.find(c => c.id === categoryId);
    if (!category || !category.questions) return [];
    
    // Exclude the current question being edited
    return category.questions.filter(q => q.id !== currentQuestion);
}

/**
 * Get the current category for a question
 */
function getCurrentCategoryForQuestion(questionId) {
    if (!questionId) return '';
    
    for (let cat of schema.categories) {
        const q = cat.questions.find(q => q.id === questionId);
        if (q) return cat.id;
    }
    
    return '';
}

/**
 * Attempt to parse legacy expression string into conditions
 */
function parseLegacyExpression(expression) {
    // This is a simplified parser for common patterns
    // Pattern 1: answers["QuestionID"] === "Value"
    // Pattern 2: answers["QuestionID"] == "Value"
    
    const conditions = [];
    
    // Split by && to get individual conditions
    const parts = expression.split('&&');
    
    for (let part of parts) {
        part = part.trim();
        
        // Try to match pattern: answers["QuestionID"] OPERATOR "Value"
        const match = part.match(/answers\["([^"]+)"\]\s*(===|==|===|\!==|!==|\.includes\(|\.contains\()\s*"?([^"]+)"?/);
        
        if (match) {
            const questionId = match[1];
            let operator = match[2];
            const value = match[3];
            
            // Normalize operator
            if (operator === '===' || operator === '==') {
                operator = 'equals';
            } else if (operator === '!==' || operator === '!=') {
                operator = 'notEquals';
            } else if (operator.includes('includes') || operator.includes('contains')) {
                operator = 'contains';
            }
            
            conditions.push({
                questionId: questionId,
                operator: operator,
                value: value
            });
        }
    }
    
    return conditions;
}

/**
 * Convert legacy expression to builder UI
 */
function convertLegacyExpressionToBuilder() {
    const expression = elements.questionVisibleWhen.value.trim();
    const conditions = parseLegacyExpression(expression);
    
    if (conditions.length > 0) {
        window.currentConditions = conditions;
        renderConditionRows();
        
        // Switch to builder mode
        const builderContainer = document.getElementById('conditionBuilderContainer');
        const legacyContainer = document.getElementById('legacyVisibleWhenContainer');
        const legacyWarning = document.getElementById('legacyWarning');
        
        if (builderContainer && legacyContainer) {
            builderContainer.style.display = 'block';
            legacyContainer.style.display = 'none';
            if (legacyWarning) legacyWarning.style.display = 'none';
        }
        
        saveConditionsToQuestion();
        showStatus('Expression converted to builder format', 'success');
    } else {
        showStatus('Could not convert expression. Please enter it manually in advanced mode.', 'warning');
    }
}

/**
 * HTML escape helper
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Update question allowOther (save on change)
 */
function updateQuestionAllowOther() {
    if (currentView !== 'question' || currentCategory === null || currentQuestion === null) return;
    
    const question = schema.categories[currentCategory].questions[currentQuestion];
    const newAllowOther = elements.questionAllowOther.checked;
    
    // Update schema if changed
    if (newAllowOther !== (question.allowOther || false)) {
        question.allowOther = newAllowOther;
        markAsModified();
    }
}

/**
 * Update question otherPlaceholder (save on blur)
 */
function updateQuestionOtherPlaceholder() {
    if (currentView !== 'question' || currentCategory === null || currentQuestion === null) return;
    
    const question = schema.categories[currentCategory].questions[currentQuestion];
    const newPlaceholder = elements.questionOtherPlaceholder.value.trim();
    
    // Update schema if changed
    const currentValue = question.otherPlaceholder || '';
    if (newPlaceholder !== currentValue) {
        question.otherPlaceholder = newPlaceholder || undefined;
        markAsModified();
    }
}

/**
 * Validate question ID field
 */
function validateQuestionId() {
    const newId = elements.questionId.value.trim();
    const errorElement = document.getElementById('questionIdError');
    
    if (!newId) {
        elements.questionId.classList.add('is-invalid');
        errorElement.textContent = 'Question ID is required';
        return false;
    }
    
    // Check for duplicate ID (across all categories)
    for (let catIdx = 0; catIdx < schema.categories.length; catIdx++) {
        const cat = schema.categories[catIdx];
        for (let qIdx = 0; qIdx < (cat.questions || []).length; qIdx++) {
            if (catIdx === currentCategory && qIdx === currentQuestion) continue;
            if (cat.questions[qIdx].id === newId) {
                elements.questionId.classList.add('is-invalid');
                errorElement.textContent = 'A question with this ID already exists';
                return false;
            }
        }
    }
    
    elements.questionId.classList.remove('is-invalid');
    errorElement.textContent = '';
    return true;
}

/**
 * Validate question label field
 */
function validateQuestionLabel() {
    const newLabel = elements.questionLabel.value.trim();
    
    if (!newLabel) {
        elements.questionLabel.classList.add('is-invalid');
        return false;
    }
    
    elements.questionLabel.classList.remove('is-invalid');
    return true;
}

/**
 * Validate question type field
 */
function validateQuestionType() {
    const newType = elements.questionType.value;
    
    if (!newType) {
        elements.questionType.classList.add('is-invalid');
        return false;
    }
    
    elements.questionType.classList.remove('is-invalid');
    return true;
}

/**
 * Save category changes
 * Form submit handler - validates all fields (for Enter key support)
 * Note: Individual fields are already saved on blur via update functions
 */
function saveCategoryChanges(e) {
    e.preventDefault();
    
    // Validate all fields
    const isIdValid = validateCategoryId();
    const isLabelValid = validateCategoryLabel();
    
    if (!isIdValid || !isLabelValid) {
        showStatus('Please fix validation errors', 'error');
        return;
    }
    
    // Data is already updated via blur handlers
    // Just trigger a final update and re-render
    updateCategoryId();
    updateCategoryLabel();
    updateCategoryDescription();
    
    renderTree();
    showStatus('Category saved', 'success');
}

/**
 * Save question changes
 * Form submit handler - validates all fields (for Enter key support)
 * Note: Individual fields are already saved on blur via update functions
 */
function saveQuestionChanges(e) {
    e.preventDefault();
    
    // Validate all fields
    const isIdValid = validateQuestionId();
    const isLabelValid = validateQuestionLabel();
    const isTypeValid = validateQuestionType();
    
    if (!isIdValid || !isLabelValid || !isTypeValid) {
        showStatus('Please fix validation errors', 'error');
        return;
    }
    
    // Data is already updated via blur handlers
    // Just trigger a final update and re-render
    updateQuestionId();
    updateQuestionLabel();
    updateQuestionType();
    updateQuestionHelp();
    updateQuestionVisibleWhen();
    updateQuestionAllowOther();
    updateQuestionOtherPlaceholder();
    
    renderTree();
    showStatus('Question saved', 'success');
}

/**
 * Add new category
 */
function addNewCategory() {
    if (!schema.categories) schema.categories = [];
    
    const newId = `NewCategory${schema.categories.length + 1}`;
    const newCategory = {
        id: newId,
        label: 'New Category',
        description: '',
        questions: []
    };
    
    schema.categories.push(newCategory);
    expandedCategories.add(newId);
    
    showCategoryEditor(schema.categories.length - 1);
    markAsModified();
    updateStatusBar();
}

/**
 * Delete category
 */
function deleteCategory() {
    const category = schema.categories[currentCategory];
    const questionCount = (category.questions || []).length;
    
    if (!confirm(`Delete category "${category.label}"? This will also delete ${questionCount} question(s).`)) {
        return;
    }
    
    schema.categories.splice(currentCategory, 1);
    expandedCategories.delete(category.id);
    
    currentView = 'welcome';
    currentCategory = null;
    
    elements.categoryEditor.classList.add('d-none');
    elements.welcomeScreen.classList.remove('d-none');
    
    markAsModified();
    renderTree();
    updateStatusBar();
    showStatus('Category deleted', 'success');
}

/**
 * Add new question to current category
 */
function addNewQuestion() {
    const category = schema.categories[currentCategory];
    if (!category.questions) category.questions = [];
    
    const newQuestion = {
        id: `${category.id}_NewQuestion${category.questions.length + 1}`,
        label: 'New Question',
        type: 'text',
        help: ''
    };
    
    category.questions.push(newQuestion);
    showQuestionEditor(currentCategory, category.questions.length - 1);
    
    markAsModified();
    updateStatusBar();
}

/**
 * Delete question
 */
function deleteQuestion() {
    const category = schema.categories[currentCategory];
    const question = category.questions[currentQuestion];
    
    if (!confirm(`Delete question "${question.label}"?`)) {
        return;
    }
    
    category.questions.splice(currentQuestion, 1);
    
    currentView = 'category';
    currentQuestion = null;
    
    showCategoryEditor(currentCategory);
    
    markAsModified();
    updateStatusBar();
    showStatus('Question deleted', 'success');
}

/**
 * Handle search input
 */
function handleSearch() {
    renderTree();
}

/**
 * Toggle expand all categories
 */
function toggleExpandAll() {
    if (expandedCategories.size > 0) {
        expandedCategories.clear();
        elements.btnExpandAll.textContent = 'Expand All';
    } else {
        schema.categories.forEach(cat => expandedCategories.add(cat.id));
        elements.btnExpandAll.textContent = 'Collapse All';
    }
    renderTree();
}

/**
 * Mark schema as modified and trigger auto-save
 */
function setModified(modified) {
    isModified = modified;
    updateStatusBar();
    
    // Trigger auto-save immediately when modified
    if (modified && !isSaving) {
        autoSave();
    }
}

/**
 * Mark schema as modified (alias for setModified(true))
 */
function markAsModified() {
    setModified(true);
}

/**
 * Auto-save schema (called when changes are made)
 */
async function autoSave() {
    if (isSaving) {
        return; // Prevent concurrent saves
    }
    
    try {
        isSaving = true;
        showStatus('Saving...', 'info');
        
        const response = await fetch('/api/schema', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ schema })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            // Show validation warnings but don't block
            if (data.errors) {
                showValidationWarning(data.errors);
            }
            showStatus('Saved with warnings', 'warning');
        } else {
            showStatus('Saved', 'success');
        }
        
        isModified = false;
        updateStatusBar();
        
    } catch (error) {
        console.error('Error auto-saving schema:', error);
        showStatus(`Auto-save failed: ${error.message}`, 'error');
    } finally {
        isSaving = false;
    }
}

/**
 * Update status bar
 */
function updateStatusBar() {
    const categoryCount = schema ? (schema.categories || []).length : 0;
    let questionCount = 0;
    
    if (schema && schema.categories) {
        schema.categories.forEach(cat => {
            questionCount += (cat.questions || []).length;
        });
    }
    
    elements.statusCategories.textContent = `Categories: ${categoryCount}`;
    elements.statusQuestions.textContent = `Questions: ${questionCount}`;
    elements.statusModified.textContent = isModified ? '● Modified' : '✓ Saved';
    elements.statusModified.style.color = isModified ? '#ffc107' : '#198754';
}

/**
 * Show status message
 */
function showStatus(message, type = 'info') {
    elements.statusMessage.textContent = message;
    
    // Auto-clear after 5 seconds for success messages
    if (type === 'success') {
        setTimeout(() => {
            if (elements.statusMessage.textContent === message) {
                elements.statusMessage.textContent = 'Ready';
            }
        }, 5000);
    }
}

/**
 * Show validation errors
 */
function showValidationErrors(errors) {
    const errorList = errors.map(e => `• ${e}`).join('\n');
    alert(`Validation Errors:\n\n${errorList}`);
}

/**
 * Show validation warnings (non-blocking)
 */
function showValidationWarning(errors) {
    console.warn('Validation warnings:', errors);
    // Don't show alert for warnings, just log them
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(unsafe) {
    if (typeof unsafe !== 'string') return '';
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
