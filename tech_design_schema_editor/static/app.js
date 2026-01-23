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
    
    // Question form
    elements.questionForm.addEventListener('submit', saveQuestionChanges);
    elements.questionType.addEventListener('change', handleQuestionTypeChange);
    elements.btnAddOption.addEventListener('click', addNewOption);
    elements.btnDeleteQuestion.addEventListener('click', deleteQuestion);
    
    // Track modifications
    elements.categoryForm.addEventListener('input', markAsModified);
    elements.questionForm.addEventListener('input', markAsModified);
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
        
        showStatus(`Backup created: ${data.path}`, 'success');
        
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
        `Edit Question: ${question.label || question.id}`;
    document.getElementById('questionEditorSubtitle').textContent = 
        `Category: ${category.label || category.id}`;
    
    // Handle question type-specific fields
    handleQuestionTypeChange();
    
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
 * Save category changes
 */
function saveCategoryChanges(e) {
    e.preventDefault();
    
    const category = schema.categories[currentCategory];
    const newId = elements.categoryId.value.trim();
    const newLabel = elements.categoryLabel.value.trim();
    
    // Validate
    if (!newId) {
        showStatus('Category ID is required', 'error');
        return;
    }
    
    if (!newLabel) {
        showStatus('Category label is required', 'error');
        return;
    }
    
    // Check for duplicate ID (if changed)
    if (newId !== category.id) {
        const duplicate = schema.categories.find((c, i) => 
            i !== currentCategory && c.id === newId
        );
        if (duplicate) {
            showStatus('A category with this ID already exists', 'error');
            return;
        }
    }
    
    // Update category
    const oldId = category.id;
    category.id = newId;
    category.label = newLabel;
    category.description = elements.categoryDescription.value.trim();
    
    // Update expanded categories set if ID changed
    if (oldId !== newId && expandedCategories.has(oldId)) {
        expandedCategories.delete(oldId);
        expandedCategories.add(newId);
    }
    
    markAsModified();
    renderTree();
    showStatus('Category updated', 'success');
}

/**
 * Save question changes
 */
function saveQuestionChanges(e) {
    e.preventDefault();
    
    const question = schema.categories[currentCategory].questions[currentQuestion];
    const newId = elements.questionId.value.trim();
    const newLabel = elements.questionLabel.value.trim();
    const newType = elements.questionType.value;
    
    // Validate
    if (!newId) {
        showStatus('Question ID is required', 'error');
        return;
    }
    
    if (!newLabel) {
        showStatus('Question label is required', 'error');
        return;
    }
    
    if (!newType) {
        showStatus('Question type is required', 'error');
        return;
    }
    
    // Check for duplicate ID (across all categories)
    for (let catIdx = 0; catIdx < schema.categories.length; catIdx++) {
        const cat = schema.categories[catIdx];
        for (let qIdx = 0; qIdx < (cat.questions || []).length; qIdx++) {
            if (catIdx === currentCategory && qIdx === currentQuestion) continue;
            if (cat.questions[qIdx].id === newId) {
                showStatus('A question with this ID already exists', 'error');
                return;
            }
        }
    }
    
    // Update question
    question.id = newId;
    question.label = newLabel;
    question.type = newType;
    question.help = elements.questionHelp.value.trim();
    question.visibleWhen = elements.questionVisibleWhen.value.trim() || undefined;
    
    // Handle options for choice-based questions
    if (['radio', 'multiselect', 'dropdown'].includes(newType)) {
        question.allowOther = elements.questionAllowOther.checked;
        question.otherPlaceholder = elements.questionOtherPlaceholder.value.trim() || undefined;
        // Options are already updated via handleOptionChange
    } else {
        // Remove options-related fields for non-choice questions
        delete question.options;
        delete question.allowOther;
        delete question.otherPlaceholder;
    }
    
    markAsModified();
    renderTree();
    showStatus('Question updated', 'success');
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
