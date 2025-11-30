"""
Web UI HTML Template for RDD Framework
This file contains the inline HTML/CSS/JS for the web interface.
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>RDD Framework - Web UI</title>
  <style>
    :root {
      --bg: #f5f5f7;
      --sidebar-bg: #1f2933;
      --sidebar-text: #e5e7eb;
      --sidebar-accent: #60a5fa;
      --card-bg: #ffffff;
      --border: #d1d5db;
      --text-main: #111827;
      --text-muted: #6b7280;
      --accent: #2563eb;
      --accent-soft: #dbeafe;
      --success: #10b981;
      --danger: #ef4444;
      --warning: #f59e0b;
      --radius: 8px;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text-main);
      display: flex;
      min-height: 100vh;
    }

    #app {
      display: flex;
      width: 100%;
    }

    /* Sidebar Navigation */
    #sidebar {
      width: 260px;
      background: var(--sidebar-bg);
      color: var(--sidebar-text);
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      position: sticky;
      top: 0;
      align-self: flex-start;
      max-height: 100vh;
      overflow-y: auto;
    }

    #sidebar h1 {
      font-size: 18px;
      margin: 0 0 4px;
    }

    #sidebar .subtitle {
      font-size: 12px;
      color: #9ca3af;
    }

    .nav-group-title {
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #9ca3af;
      margin: 8px 0 4px;
    }

    .nav-group {
      border-top: 1px solid rgba(156, 163, 175, 0.3);
      padding-top: 8px;
      margin-top: 4px;
    }

    .nav-item {
      font-size: 13px;
      padding: 6px 8px;
      border-radius: 6px;
      margin-bottom: 2px;
      cursor: pointer;
      display: block;
      color: var(--sidebar-text);
    }

    .nav-item:hover {
      background: rgba(148, 163, 184, 0.35);
    }

    .nav-item.active {
      background: rgba(37, 99, 235, 0.28);
      color: #f9fafb;
    }

    .nav-footer {
      font-size: 11px;
      margin-top: auto;
      color: #9ca3af;
    }

    /* Main Layout */
    #main {
      flex: 1;
      padding: 16px 24px 32px;
      overflow-y: auto;
    }

    .top-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 16px;
    }

    .top-title {
      font-size: 20px;
      font-weight: 600;
    }

    .top-subtitle {
      font-size: 13px;
      color: var(--text-muted);
    }

    /* Cards */
    .card {
      background: var(--card-bg);
      border-radius: var(--radius);
      border: 1px solid var(--border);
      padding: 16px;
      margin-bottom: 16px;
    }

    .card-title {
      font-size: 16px;
      font-weight: 600;
      margin: 0 0 12px;
    }

    .card-subtitle {
      font-size: 13px;
      color: var(--text-muted);
      margin-bottom: 12px;
    }

    /* Buttons */
    .btn {
      border-radius: 6px;
      border: 1px solid var(--border);
      background: #ffffff;
      font-size: 13px;
      padding: 8px 16px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: inherit;
    }

    .btn-primary {
      background: var(--accent);
      border-color: var(--accent);
      color: #f9fafb;
    }

    .btn-success {
      background: var(--success);
      border-color: var(--success);
      color: #ffffff;
    }

    .btn-danger {
      background: var(--danger);
      border-color: var(--danger);
      color: #ffffff;
    }

    .btn:hover {
      filter: brightness(0.95);
    }

    .btn:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }

    /* Forms */
    input[type="text"],
    textarea,
    select {
      width: 100%;
      padding: 8px 10px;
      border-radius: 6px;
      border: 1px solid var(--border);
      font-size: 13px;
      font-family: inherit;
    }

    textarea {
      min-height: 80px;
      resize: vertical;
    }

    .form-group {
      margin-bottom: 16px;
    }

    .form-label {
      display: block;
      margin-bottom: 6px;
      font-size: 13px;
      font-weight: 500;
    }

    .form-error {
      color: var(--danger);
      font-size: 12px;
      margin-top: 4px;
    }

    /* Task List */
    .task-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .task-item {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 12px;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .task-status {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }

    .task-status.pending { background: var(--text-muted); }
    .task-status.running { background: var(--accent); animation: pulse 2s infinite; }
    .task-status.completed { background: var(--success); }
    .task-status.failed { background: var(--danger); }
    .task-status.cancelled { background: var(--warning); }

    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.5; }
    }

    .task-info {
      flex: 1;
    }

    .task-action {
      font-weight: 500;
      font-size: 14px;
    }

    .task-time {
      font-size: 12px;
      color: var(--text-muted);
    }

    .task-actions {
      display: flex;
      gap: 8px;
    }

    /* Log Viewer */
    .log-viewer {
      background: #1e1e1e;
      color: #d4d4d4;
      padding: 12px;
      border-radius: 6px;
      font-family: 'Courier New', monospace;
      font-size: 12px;
      max-height: 400px;
      overflow-y: auto;
      white-space: pre-wrap;
      word-wrap: break-word;
    }

    .log-line {
      margin-bottom: 2px;
    }

    /* Status Badge */
    .badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 500;
      text-transform: uppercase;
    }

    .badge-success { background: var(--success); color: white; }
    .badge-danger { background: var(--danger); color: white; }
    .badge-warning { background: var(--warning); color: white; }
    .badge-info { background: var(--accent); color: white; }

    /* File Browser */
    .file-tree {
      list-style: none;
      padding-left: 0;
    }

    .file-tree li {
      padding: 4px 8px;
      cursor: pointer;
      border-radius: 4px;
    }

    .file-tree li:hover {
      background: var(--accent-soft);
    }

    .file-tree .folder {
      font-weight: 500;
    }

    .hidden {
      display: none !important;
    }

    /* Dashboard Grid */
    .dashboard-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }

    .action-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .action-card:hover {
      border-color: var(--accent);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      transform: translateY(-2px);
    }

    .action-card h3 {
      margin: 0 0 8px;
      font-size: 16px;
    }

    .action-card p {
      margin: 0;
      font-size: 13px;
      color: var(--text-muted);
    }

    /* Tabs */
    .tabs {
      display: flex;
      border-bottom: 1px solid var(--border);
      margin-bottom: 16px;
    }

    .tab {
      padding: 8px 16px;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      font-size: 14px;
    }

    .tab:hover {
      background: var(--accent-soft);
    }

    .tab.active {
      border-bottom-color: var(--accent);
      color: var(--accent);
      font-weight: 500;
    }

    .tab-content {
      display: none;
    }

    .tab-content.active {
      display: block;
    }

    @media (max-width: 900px) {
      #sidebar {
        display: none;
      }
      #main {
        padding: 12px;
      }
      .dashboard-grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
<div id="app">
  <aside id="sidebar">
    <div>
      <h1>RDD Framework</h1>
      <div class="subtitle">Requirements-Driven Development</div>
    </div>

    <div class="nav-group">
      <div class="nav-group-title">Main Menu</div>
      <a href="#" class="nav-item" data-view="dashboard">Dashboard</a>
      <a href="#" class="nav-item" data-view="tasks">Tasks</a>
      <a href="#" class="nav-item" data-view="config">Configuration</a>
      <a href="#" class="nav-item" data-view="files">Files</a>
    </div>

    <div class="nav-group">
      <div class="nav-group-title">Advanced</div>
      <a href="#" class="nav-item" data-view="advanced">Advanced Actions</a>
    </div>

    <div class="nav-footer">
      <div id="version-info">Loading...</div>
      <div id="branch-info" style="margin-top: 4px;">Loading...</div>
    </div>
  </aside>

  <main id="main">
    <!-- Dashboard View -->
    <div id="view-dashboard" class="view-content">
      <div class="top-bar">
        <div>
          <div class="top-title">Dashboard</div>
          <div class="top-subtitle">Quick actions and system status</div>
        </div>
      </div>

      <div class="card">
        <div class="card-title">System Status</div>
        <div id="status-info">Loading...</div>
      </div>

      <div class="card-title" style="margin-bottom: 12px;">Quick Actions</div>
      <div class="dashboard-grid">
        <div class="action-card" onclick="showCreateIterationForm()">
          <h3>Create New Iteration</h3>
          <p>Start work on a new feature or fix</p>
        </div>
        <div class="action-card" onclick="executeAction('update_from_default')">
          <h3>Update from Default</h3>
          <p>Sync with latest changes from default branch</p>
        </div>
        <div class="action-card" onclick="executeAction('complete_iteration')">
          <h3>Complete Iteration</h3>
          <p>Archive work and return to default branch</p>
        </div>
        <div class="action-card" onclick="showView('config')">
          <h3>Configuration</h3>
          <p>Manage framework settings</p>
        </div>
      </div>
    </div>

    <!-- Tasks View -->
    <div id="view-tasks" class="view-content hidden">
      <div class="top-bar">
        <div>
          <div class="top-title">Tasks</div>
          <div class="top-subtitle">Monitor running and completed tasks</div>
        </div>
        <button class="btn btn-primary" onclick="refreshTasks()">Refresh</button>
      </div>

      <div id="tasks-container"></div>
    </div>

    <!-- Configuration View -->
    <div id="view-config" class="view-content hidden">
      <div class="top-bar">
        <div>
          <div class="top-title">Configuration</div>
          <div class="top-subtitle">Edit framework settings</div>
        </div>
        <button class="btn btn-success" onclick="saveConfig()">Save Changes</button>
      </div>

      <div class="card">
        <div class="form-group">
          <label class="form-label">Default Branch</label>
          <input type="text" id="config-defaultBranch" />
        </div>
        <div class="form-group">
          <label class="form-label">Local-Only Mode</label>
          <select id="config-localOnly">
            <option value="false">Disabled</option>
            <option value="true">Enabled</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Files View -->
    <div id="view-files" class="view-content hidden">
      <div class="top-bar">
        <div>
          <div class="top-title">Files</div>
          <div class="top-subtitle">Browse workspace and templates</div>
        </div>
        <button class="btn btn-primary" onclick="refreshFiles()">Refresh</button>
      </div>

      <div id="files-container"></div>
    </div>

    <!-- Advanced View -->
    <div id="view-advanced" class="view-content hidden">
      <div class="top-bar">
        <div>
          <div class="top-title">Advanced Actions</div>
          <div class="top-subtitle">Domain-based commands</div>
        </div>
      </div>

      <div class="tabs">
        <div class="tab active" onclick="showTab('branch')">Branch</div>
        <div class="tab" onclick="showTab('workspace')">Workspace</div>
        <div class="tab" onclick="showTab('git')">Git</div>
        <div class="tab" onclick="showTab('prompt')">Prompt</div>
      </div>

      <div id="tab-branch" class="tab-content active">
        <div class="card">
          <div class="card-title">Branch Operations</div>
          <p>Advanced branch management commands</p>
        </div>
      </div>

      <div id="tab-workspace" class="tab-content">
        <div class="card">
          <div class="card-title">Workspace Operations</div>
          <p>Advanced workspace management commands</p>
        </div>
      </div>

      <div id="tab-git" class="tab-content">
        <div class="card">
          <div class="card-title">Git Operations</div>
          <p>Advanced git commands</p>
        </div>
      </div>

      <div id="tab-prompt" class="tab-content">
        <div class="card">
          <div class="card-title">Prompt Operations</div>
          <p>Manage execution prompts</p>
        </div>
      </div>
    </div>
  </main>
</div>

<!-- Create Iteration Modal -->
<div id="modal-create-iteration" class="hidden" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;">
  <div class="card" style="width: 500px; max-width: 90%;">
    <div class="card-title">Create New Iteration</div>
    <div class="form-group">
      <label class="form-label">Branch Name</label>
      <input type="text" id="create-branch-name" placeholder="my-feature" />
      <div id="create-branch-error" class="form-error hidden"></div>
    </div>
    <div style="display: flex; gap: 8px; justify-content: flex-end;">
      <button class="btn" onclick="hideModal('modal-create-iteration')">Cancel</button>
      <button class="btn btn-primary" onclick="submitCreateIteration()">Create</button>
    </div>
  </div>
</div>

<script>
// Global state
const API_TOKEN = '{{TOKEN}}';
const BASE_URL = '';
let currentView = 'dashboard';
let statusCheckInterval = null;

// Utility functions
function apiUrl(endpoint) {
  return `${BASE_URL}${endpoint}?token=${API_TOKEN}`;
}

async function apiGet(endpoint) {
  const response = await fetch(apiUrl(endpoint));
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.json();
}

async function apiPost(endpoint, data) {
  const response = await fetch(apiUrl(endpoint), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.json();
}

// View management
function showView(viewName) {
  document.querySelectorAll('.view-content').forEach(el => el.classList.add('hidden'));
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  
  const viewEl = document.getElementById(`view-${viewName}`);
  if (viewEl) {
    viewEl.classList.remove('hidden');
    currentView = viewName;
  }
  
  const navItem = document.querySelector(`[data-view="${viewName}"]`);
  if (navItem) navItem.classList.add('active');
  
  // Load view data
  if (viewName === 'tasks') refreshTasks();
  else if (viewName === 'config') loadConfig();
  else if (viewName === 'files') refreshFiles();
}

function showTab(tabName) {
  document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  
  event.target.classList.add('active');
  document.getElementById(`tab-${tabName}`).classList.add('active');
}

// Modal management
function showModal(modalId) {
  document.getElementById(modalId).classList.remove('hidden');
}

function hideModal(modalId) {
  document.getElementById(modalId).classList.add('hidden');
}

// Status functions
async function loadStatus() {
  try {
    const status = await apiGet('/api/status');
    document.getElementById('version-info').textContent = `Version ${status.version}`;
    document.getElementById('branch-info').textContent = `Branch: ${status.current_branch}`;
    
    document.getElementById('status-info').innerHTML = `
      <p><strong>Current Branch:</strong> ${status.current_branch}</p>
      <p><strong>Default Branch:</strong> ${status.default_branch}</p>
      <p><strong>Framework Version:</strong> ${status.version}</p>
    `;
  } catch (error) {
    console.error('Failed to load status:', error);
  }
}

// Task functions
async function refreshTasks() {
  try {
    const tasks = await apiGet('/api/tasks');
    const container = document.getElementById('tasks-container');
    
    if (tasks.length === 0) {
      container.innerHTML = '<div class="card"><p>No tasks found</p></div>';
      return;
    }
    
    container.innerHTML = tasks.map(task => `
      <div class="task-item">
        <div class="task-status ${task.state}"></div>
        <div class="task-info">
          <div class="task-action">${task.action}</div>
          <div class="task-time">${new Date(task.start_time).toLocaleString()}</div>
        </div>
        <div class="task-actions">
          ${task.state === 'running' ? 
            `<button class="btn btn-danger" onclick="cancelTask('${task.run_id}')">Cancel</button>` :
            `<button class="btn" onclick="viewTaskLogs('${task.run_id}')">View Logs</button>`
          }
        </div>
      </div>
    `).join('');
  } catch (error) {
    console.error('Failed to refresh tasks:', error);
  }
}

async function executeAction(action, options = {}) {
  try {
    const result = await apiPost('/api/tasks', { action, options });
    alert(`Task started: ${result.run_id}`);
    showView('tasks');
    refreshTasks();
  } catch (error) {
    alert(`Failed to start task: ${error.message}`);
  }
}

async function cancelTask(runId) {
  try {
    await apiPost(`/api/tasks/${runId}/cancel`, {});
    alert('Task cancelled');
    refreshTasks();
  } catch (error) {
    alert(`Failed to cancel task: ${error.message}`);
  }
}

async function viewTaskLogs(runId) {
  try {
    const task = await apiGet(`/api/tasks/${runId}`);
    const logs = task.output_buffer.join('\\n');
    alert(`Task Logs:\\n\\n${logs}`);
  } catch (error) {
    alert(`Failed to load logs: ${error.message}`);
  }
}

// Create iteration
function showCreateIterationForm() {
  document.getElementById('create-branch-name').value = '';
  document.getElementById('create-branch-error').classList.add('hidden');
  showModal('modal-create-iteration');
}

async function submitCreateIteration() {
  const branchName = document.getElementById('create-branch-name').value.trim();
  const errorEl = document.getElementById('create-branch-error');
  
  if (!branchName) {
    errorEl.textContent = 'Branch name is required';
    errorEl.classList.remove('hidden');
    return;
  }
  
  try {
    const result = await apiPost('/api/tasks', {
      action: 'create_iteration',
      options: { branch_name: branchName }
    });
    hideModal('modal-create-iteration');
    alert(`Iteration creation started: ${result.run_id}`);
    showView('tasks');
    refreshTasks();
  } catch (error) {
    errorEl.textContent = `Error: ${error.message}`;
    errorEl.classList.remove('hidden');
  }
}

// Configuration
async function loadConfig() {
  try {
    const config = await apiGet('/api/config');
    document.getElementById('config-defaultBranch').value = config.defaultBranch || '';
    document.getElementById('config-localOnly').value = config.localOnly ? 'true' : 'false';
  } catch (error) {
    console.error('Failed to load config:', error);
  }
}

async function saveConfig() {
  try {
    const config = {
      defaultBranch: document.getElementById('config-defaultBranch').value,
      localOnly: document.getElementById('config-localOnly').value === 'true'
    };
    
    await apiPost('/api/config', config);
    alert('Configuration saved');
  } catch (error) {
    alert(`Failed to save config: ${error.message}`);
  }
}

// Files
async function refreshFiles() {
  const container = document.getElementById('files-container');
  container.innerHTML = '<div class="card"><p>File browser not yet implemented</p></div>';
}

// Navigation setup
document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', (e) => {
    e.preventDefault();
    const view = item.getAttribute('data-view');
    if (view) showView(view);
  });
});

// Initial load
loadStatus();
statusCheckInterval = setInterval(loadStatus, 30000); // Refresh every 30 seconds

// Handle modal clicks
document.getElementById('modal-create-iteration').addEventListener('click', (e) => {
  if (e.target.id === 'modal-create-iteration') {
    hideModal('modal-create-iteration');
  }
});
</script>
</body>
</html>
"""
