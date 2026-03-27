// SPM Effort Estimation System - Main Application Logic

// Global variables
// Determine API base URL based on environment
const API_BASE = (() => {
    const hostname = window.location.hostname;
    const protocol = window.location.protocol;
    
    // For localhost, use /api (backend proxy)
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return '/api';
    }
    
    // For Vercel deployed frontend, use environment variable or direct backend URL
    // Check for meta tag or window variable set at runtime
    if (typeof window !== 'undefined' && window.API_BASE) {
        return window.API_BASE;
    }
    
    // Fallback: use /api (should be configured via reverse proxy in deployment)
    return '/api';
})();

let currentProjectId = null;
let chartInstances = {};
let activityHistory = [];
const MAX_HISTORY_ITEMS = 50;

// ==================== THEME MANAGEMENT ====================

function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const body = document.body;
    const themeToggle = document.getElementById('themeToggle');

    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        body.classList.remove('light-theme');
        if (themeToggle) themeToggle.textContent = '☀️ Light';
    } else {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        if (themeToggle) themeToggle.textContent = '🌙 Dark';
    }
}

function toggleTheme() {
    const body = document.body;
    const isDark = body.classList.toggle('dark-theme');
    body.classList.toggle('light-theme');

    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.textContent = isDark ? '☀️ Light' : '🌙 Dark';
    }

    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

// ==================== ACTIVITY HISTORY ====================

function addToHistory(action, details = '') {
    const timestamp = new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });

    activityHistory.unshift({
        action,
        details,
        timestamp
    });

    // Keep only last 50 items
    if (activityHistory.length > MAX_HISTORY_ITEMS) {
        activityHistory.pop();
    }

    // Save to localStorage
    localStorage.setItem('activityHistory', JSON.stringify(activityHistory));

    updateHistoryDisplay();
}

function updateHistoryDisplay() {
    const historyList = document.getElementById('historyList');
    if (!historyList) return;

    if (activityHistory.length === 0) {
        historyList.innerHTML = '<p class="text-muted">No activities yet</p>';
        return;
    }

    let html = '';
    activityHistory.forEach((item, index) => {
        const detail = item.details ? ` - ${item.details}` : '';
        html += `
            <div class="mb-2 pb-2 border-bottom" style="border-color: #ddd;">
                <small class="text-muted">${item.timestamp}</small><br>
                <small><strong>${item.action}</strong>${detail}</small>
            </div>
        `;
    });

    historyList.innerHTML = html;
}

function loadHistoryFromStorage() {
    const saved = localStorage.getItem('activityHistory');
    if (saved) {
        try {
            activityHistory = JSON.parse(saved);
            updateHistoryDisplay();
        } catch (e) {
            console.error('Error loading history:', e);
        }
    }
}

function toggleHistoryPanel() {
    const historySidebar = document.getElementById('historySidebar');
    const mainContent = document.getElementById('mainContent');
    const sidebarNav = document.getElementById('sidebarNav');

    if (historySidebar.style.display === 'none') {
        historySidebar.style.display = 'block';
        mainContent.className = 'col-md-7';
        sidebarNav.className = 'col-md-2';
        addToHistory('Opened History Panel');
    } else {
        historySidebar.style.display = 'none';
        mainContent.className = 'col-md-9';
        sidebarNav.className = 'col-md-3';
        addToHistory('Closed History Panel');
    }
}

function clearHistory() {
    if (confirm('Are you sure you want to clear activity history? This cannot be undone.')) {
        activityHistory = [];
        localStorage.removeItem('activityHistory');
        updateHistoryDisplay();
        showAlert('Activity history cleared successfully', 'success');
    }
}

function clearAllData() {
    const confirmClear = confirm(
        '⚠️ WARNING: This will DELETE ALL data:\n' +
        '- All projects\n' +
        '- All estimations\n' +
        '- All risk assessments\n' +
        '- All EVM tracking data\n' +
        '- All activity history\n\n' +
        'This action CANNOT be undone. Continue?'
    );

    if (confirmClear) {
        const finalConfirm = confirm(
            'This is your last chance! Type "DELETE" to confirm you want to delete ALL data.'
        );

        if (finalConfirm) {
            // Clear all data from backend
            fetch(`${API_BASE}/clear-all-data`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        // Clear local data
                        activityHistory = [];
                        localStorage.removeItem('activityHistory');
                        currentProjectId = null;

                        // Clear all forms
                        const forms = document.querySelectorAll('form');
                        forms.forEach(form => form.reset());

                        // Clear all charts
                        Object.keys(chartInstances).forEach(key => {
                            if (chartInstances[key]) {
                                chartInstances[key].destroy();
                            }
                        });
                        chartInstances = {};

                        // Update UI
                        updateHistoryDisplay();
                        loadProjects();

                        showAlert('✓ All data has been permanently deleted!', 'success');
                        addToHistory('Cleared', 'All system data');
                    }
                })
                .catch(err => {
                    console.error(err);
                    showAlert('Error clearing data', 'danger');
                });
        }
    }
}

function exportData() {
    const data = {
        exportDate: new Date().toISOString(),
        history: activityHistory,
        timestamp: new Date().getTime()
    };

    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `spm-history-${new Date().toISOString().slice(0, 10)}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showAlert('History exported successfully', 'success');
    addToHistory('Exported', 'Activity history');
}

function importData() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = (event) => {
            try {
                const imported = JSON.parse(event.target.result);
                if (imported.history && Array.isArray(imported.history)) {
                    activityHistory = imported.history;
                    localStorage.setItem('activityHistory', JSON.stringify(activityHistory));
                    updateHistoryDisplay();
                    showAlert('History imported successfully', 'success');
                    addToHistory('Imported', 'Activity history');
                } else {
                    showAlert('Invalid file format', 'danger');
                }
            } catch (err) {
                console.error(err);
                showAlert('Error importing file', 'danger');
            }
        };
        reader.readAsText(file);
    };
    input.click();
}

// ==================== AUTHENTICATION ====================

async function checkAuth() {
    try {
        const response = await fetch('/api/user');
        if (response.status === 401) {
            // Not authenticated, redirect to login
            window.location.href = '/login';
            return;
        }
        const data = await response.json();
        if (data.user) {
            // Display username in navbar
            const userDisplay = document.getElementById('userDisplay');
            if (userDisplay) {
                userDisplay.textContent = `👤 ${data.user}`;
            }
        }
    } catch (error) {
        console.error('Auth check error:', error);
    }
}

// Check authentication on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    loadHistoryFromStorage();
    checkAuth();

    // Setup event listeners
    const themeToggle = document.getElementById('themeToggle');
    const historyToggle = document.getElementById('historyToggle');

    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    if (historyToggle) {
        historyToggle.addEventListener('click', toggleHistoryPanel);
    }
});

// ==================== MODULE SWITCHING ====================

function switchModule(moduleId, subSectionId = null) {
    // Hide all modules
    const modules = document.querySelectorAll('.module-content');
    modules.forEach(mod => mod.style.display = 'none');

    // Show selected module
    const selectedModule = document.getElementById(moduleId);
    if (selectedModule) {
        selectedModule.style.display = 'block';
        
        // Scroll to sub-section if provided
        if (subSectionId) {
            setTimeout(() => {
                const subSection = document.getElementById(subSectionId);
                if (subSection) {
                    subSection.scrollIntoView({ behavior: 'smooth' });
                }
            }, 100);
        }
    }

    // Update sidebar active state
    const buttons = document.querySelectorAll('.list-group-item');
    buttons.forEach(btn => {
        btn.classList.remove('active');
        // Check if this button's onclick calls the current moduleId
        if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(`'${moduleId}'`)) {
            btn.classList.add('active');
        }
    });

    // Add to history
    const moduleNames = {
        'project': 'Project Input',
        'estimation': 'Effort Estimation',
        'schedule': 'Schedule & Cost',
        'risk': 'Risk Management',
        'evm': 'EVM Tracking',
        'dashboard': 'Dashboard',
        'report': 'Reports'
    };
    addToHistory('Switched to', moduleNames[moduleId] || moduleId);

    // Load project lists when switching to modules
    if (moduleId === 'estimation' || moduleId === 'schedule' || moduleId === 'risk' ||
        moduleId === 'evm' || moduleId === 'dashboard' || moduleId === 'report') {
        loadProjectsForModule(moduleId);
    }
}

// ==================== PROJECT INPUT MODULE ====================

document.addEventListener('DOMContentLoaded', function () {
    const projectForm = document.getElementById('projectForm');
    if (projectForm) {
        projectForm.addEventListener('submit', handleProjectSubmit);
    }

    const riskForm = document.getElementById('riskForm');
    if (riskForm) {
        riskForm.addEventListener('submit', handleRiskSubmit);
    }

    const evmForm = document.getElementById('evmForm');
    if (evmForm) {
        evmForm.addEventListener('submit', handleEVMSubmit);
    }

    loadProjects();
});

function handleProjectSubmit(e) {
    e.preventDefault();

    const projectData = {
        project_name: document.getElementById('projectName').value,
        project_type: document.getElementById('projectType').value,
        kloc: document.getElementById('kloc').value,
        cost_per_person_month: document.getElementById('costPerPersonMonth').value,
        team_experience: document.getElementById('teamExperience').value
    };

    fetch(`${API_BASE}/projects`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(projectData)
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showAlert('Project created successfully!', 'success');
                addToHistory('Created Project', projectData.project_name);
                document.getElementById('projectForm').reset();
                currentProjectId = data.project_id;
                loadProjects();
            } else {
                showAlert('Error: ' + data.error, 'danger');
            }
        })
        .catch(err => {
            console.error(err);
            showAlert('Error creating project', 'danger');
        });
}

function loadProjects() {
    fetch(`${API_BASE}/projects`)
        .then(res => res.json())
        .then(projects => {
            const projectList = document.getElementById('projectList');
            projectList.innerHTML = '';

            if (projects.length === 0) {
                projectList.innerHTML = '<div class="alert alert-info">No projects yet</div>';
                return;
            }

            let html = '<table class="table table-sm">';
            html += '<thead><tr><th>Project</th><th>Type</th><th>Size (KLOC)</th><th>Created</th></tr></thead>';
            html += '<tbody>';

            projects.forEach(project => {
                html += `<tr>
                    <td><strong>${project.project_name}</strong></td>
                    <td>${project.project_type}</td>
                    <td>${project.kloc}</td>
                    <td>${new Date(project.created_date).toLocaleDateString()}</td>
                </tr>`;
            });

            html += '</tbody></table>';
            projectList.innerHTML = html;
        })
        .catch(err => {
            console.error(err);
        });
}

// ==================== PROJECT LOADING FOR MODULES ====================

function loadProjectsForModule(moduleId) {
    const selectIds = {
        'estimation': 'estimationProject',
        'schedule': 'scheduleProject',
        'risk': 'riskProject',
        'evm': 'evmProject',
        'dashboard': 'dashboardProject',
        'report': 'reportProject'
    };

    const selectId = selectIds[moduleId];
    if (!selectId) return;

    fetch(`${API_BASE}/projects`)
        .then(res => res.json())
        .then(projects => {
            const select = document.getElementById(selectId);
            select.innerHTML = '<option value="">-- Select Project --</option>';

            projects.forEach(project => {
                const option = document.createElement('option');
                option.value = project.id;
                option.textContent = project.project_name;
                select.appendChild(option);
            });
        })
        .catch(err => console.error(err));
}

// ==================== EFFORT ESTIMATION MODULE ====================

function loadProjectForEstimation() {
    const projectId = document.getElementById('estimationProject').value;
    if (!projectId) return;

    currentProjectId = projectId;
    document.getElementById('basicResults').innerHTML = '';
    document.getElementById('intermediateResults').innerHTML = '';
}

function calculateBasicCOCOMO() {
    if (!currentProjectId) {
        showAlert('Please select a project first', 'warning');
        return;
    }

    fetch(`${API_BASE}/estimations/basic-cocomo/${currentProjectId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                let html = `
            <div class="result-box">
                <div class="result-label">Model</div>
                <div class="result-value">${data.model}</div>
            </div>
            
            <div class="row mt-3">
                <div class="col-md-4">
                    <div class="result-box">
                        <div class="result-label">Effort (Person-Months)</div>
                        <div class="result-value">${data.effort_person_months}</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="result-box">
                        <div class="result-label">Duration (Months)</div>
                        <div class="result-value">${data.duration_months}</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="result-box">
                        <div class="result-label">Total Cost</div>
                        <div class="result-value">${data.total_cost.toFixed(2)}</div>
                    </div>
                </div>
            </div>
            
            <h6 class="mt-4">Phase-wise Cost Distribution</h6>
            <table class="table table-sm">
                <tr><td><strong>Design</strong></td><td>${data.cost_per_phase.Design.toFixed(2)}</td></tr>
                <tr><td><strong>Code</strong></td><td>${data.cost_per_phase.Code.toFixed(2)}</td></tr>
                <tr><td><strong>Test</strong></td><td>${data.cost_per_phase.Test.toFixed(2)}</td></tr>
                <tr><td><strong>Integration</strong></td><td>${data.cost_per_phase.Integration.toFixed(2)}</td></tr>
            </table>
            `;

                document.getElementById('basicResults').innerHTML = html;
                showAlert('Basic COCOMO calculated successfully', 'success');
            } else {
                showAlert('Error: ' + data.error, 'danger');
            }
        })
        .catch(err => {
            console.error(err);
            showAlert('Error calculating COCOMO', 'danger');
        });
}

function calculateIntermediateCOCOMO() {
    if (!currentProjectId) {
        showAlert('Please select a project first', 'warning');
        return;
    }

    const multipliers = {
        'Required Software Reliability': document.getElementById('reliability').value,
        'Product Complexity': document.getElementById('complexity').value
    };

    fetch(`${API_BASE}/estimations/intermediate-cocomo/${currentProjectId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ multipliers: multipliers })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                let html = `
            <div class="result-box">
                <div class="result-label">Model</div>
                <div class="result-value">${data.model}</div>
            </div>
            
            <div class="row mt-3">
                <div class="col-md-6">
                    <div class="result-box">
                        <div class="result-label">Base Effort</div>
                        <div class="result-value">${data.base_effort}</div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="result-box">
                        <div class="result-label">Multiplier Impact</div>
                        <div class="result-value">${data.multiplier_impact}x</div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-3">
                <div class="col-md-4">
                    <div class="result-box">
                        <div class="result-label">Adjusted Effort</div>
                        <div class="result-value">${data.effort_person_months}</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="result-box">
                        <div class="result-label">Duration (Months)</div>
                        <div class="result-value">${data.duration_months}</div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="result-box">
                        <div class="result-label">Total Cost</div>
                        <div class="result-value">${data.total_cost.toFixed(2)}</div>
                    </div>
                </div>
            </div>
            `;

                document.getElementById('intermediateResults').innerHTML = html;
                showAlert('Intermediate COCOMO calculated successfully', 'success');
            } else {
                showAlert('Error: ' + data.error, 'danger');
            }
        })
        .catch(err => {
            console.error(err);
            showAlert('Error calculating Intermediate COCOMO', 'danger');
        });
}

// ==================== SCHEDULE & COST MODULE ====================

function loadScheduleData() {
    const projectId = document.getElementById('scheduleProject').value;
    if (!projectId) return;

    currentProjectId = projectId;

    fetch(`${API_BASE}/projects/${projectId}`)
        .then(res => res.json())
        .then(project => {
            // Display project info
            let html = `
            <div class="alert alert-info">
                <strong>${project.project_name}</strong> - ${project.project_type} | 
                Size: ${project.kloc} KLOC | Cost/Month: ${project.cost_per_person_month}
            </div>
            `;

            document.getElementById('scheduleResults').innerHTML = html;

            // Create sample Gantt chart
            createGanttChart();
            createCostChart();
        })
        .catch(err => {
            console.error(err);
            showAlert('Error loading project data', 'danger');
        });
}

function createCostChart() {
    const ctx = document.getElementById('costChart');
    if (!ctx) return;

    // Destroy existing chart if it exists
    if (chartInstances.costChart) {
        chartInstances.costChart.destroy();
    }

    chartInstances.costChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Design (40%)', 'Code (30%)', 'Test (20%)', 'Integration (10%)'],
            datasets: [{
                data: [40, 30, 20, 10],
                backgroundColor: [
                    '#0d6efd',
                    '#198754',
                    '#0dcaf0',
                    '#ffc107'
                ],
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: { size: 12, weight: '500' }
                    }
                }
            }
        }
    });
}

function createGanttChart() {
    const ganttDiv = document.getElementById('ganttChart');
    if (!ganttDiv) return;

    const phases = [
        { name: 'Design Phase', duration: 30, start: 0 },
        { name: 'Coding Phase', duration: 45, start: 30 },
        { name: 'Testing Phase', duration: 30, start: 75 },
        { name: 'Integration & Deployment', duration: 15, start: 105 }
    ];

    let html = '<div style="margin-top: 10px;">';

    phases.forEach(phase => {
        const width = (phase.duration / 150) * 100; // 150 is total duration
        const left = (phase.start / 150) * 100;

        html += `
        <div style="margin-bottom: 20px;">
            <div style="font-weight: 600; margin-bottom: 5px; font-size: 0.9rem;">${phase.name} (${phase.duration} days)</div>
            <div style="position: relative; height: 30px; background-color: #f0f0f0; border-radius: 4px; overflow: hidden;">
                <div class="gantt-bar" style="width: ${width}%; margin-left: ${left}%; background: linear-gradient(90deg, #0d6efd 0%, #0dcaf0 100%);">
                    ${phase.duration}d
                </div>
            </div>
        </div>
        `;
    });

    html += '</div>';
    ganttDiv.innerHTML = html;
}

// ==================== RISK MANAGEMENT MODULE ====================

function loadProjectRisks() {
    const projectId = document.getElementById('riskProject').value;
    if (!projectId) return;

    currentProjectId = projectId;
    displayProjectRisks(projectId);
}

function handleRiskSubmit(e) {
    e.preventDefault();

    if (!currentProjectId) {
        showAlert('Please select a project first', 'warning');
        return;
    }

    const riskData = {
        risk_name: document.getElementById('riskName').value,
        risk_category: document.getElementById('riskCategory').value,
        probability: parseFloat(document.getElementById('probability').value),
        impact: parseFloat(document.getElementById('impact').value),
        adjustment_factor: parseFloat(document.getElementById('adjustmentFactor').value),
        description: document.getElementById('riskDescription').value
    };

    fetch(`${API_BASE}/risks/${currentProjectId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(riskData)
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showAlert('Risk added successfully', 'success');
                document.getElementById('riskForm').reset();
                displayProjectRisks(currentProjectId);
            } else {
                showAlert('Error: ' + data.error, 'danger');
            }
        })
        .catch(err => {
            console.error(err);
            showAlert('Error adding risk', 'danger');
        });
}

function displayProjectRisks(projectId) {
    fetch(`${API_BASE}/risks/${projectId}`)
        .then(res => res.json())
        .then(risks => {
            const riskList = document.getElementById('riskList');
            riskList.innerHTML = '';

            if (risks.length === 0) {
                riskList.innerHTML = '<div class="alert alert-info">No risks added yet</div>';
                return;
            }

            risks.forEach(risk => {
                const riskCard = document.createElement('div');
                riskCard.className = 'risk-card';
                riskCard.innerHTML = `
                    <strong>${risk.risk_name}</strong>
                    <div class="small text-muted">Category: ${risk.risk_category}</div>
                    <div class="small">Probability: ${risk.probability} | Impact: ${risk.impact} | Adjustment Factor: ${risk.adjustment_factor}</div>
                    <div class="small mt-2">${risk.description}</div>
                `;
                riskList.appendChild(riskCard);
            });
        })
        .catch(err => {
            console.error(err);
        });
}

function applyRiskAdjustments() {
    if (!currentProjectId) {
        showAlert('Please select a project first', 'warning');
        return;
    }

    fetch(`${API_BASE}/risks/${currentProjectId}/apply-adjustments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                let html = `
            <div class="alert alert-warning">
                <strong>Risk Adjustments Applied</strong>
                <div class="mt-2">
                    <p>Adjustment Factor: <strong>${data.adjustment_factor}</strong></p>
                    <p>Adjusted Effort: <strong>${data.adjusted_effort} person-months</strong></p>
                    <p>Adjusted Cost: <strong>${data.adjusted_cost.toFixed(2)}</strong></p>
                </div>
            </div>
            `;
                document.getElementById('adjustmentResults').innerHTML = html;
                showAlert('Risk adjustments applied successfully', 'success');
            } else {
                showAlert('Error: ' + data.error, 'danger');
            }
        })
        .catch(err => {
            console.error(err);
            showAlert('Error applying risk adjustments', 'danger');
        });
}

// ==================== EVM MODULE ====================

function loadEVMData() {
    const projectId = document.getElementById('evmProject').value;
    if (!projectId) return;

    currentProjectId = projectId;
    document.getElementById('evmMetrics').innerHTML = '<div class="alert alert-info">Record EVM data to calculate metrics</div>';
}

function handleEVMSubmit(e) {
    e.preventDefault();

    if (!currentProjectId) {
        showAlert('Please select a project first', 'warning');
        return;
    }

    const evmData = {
        planned_value: parseFloat(document.getElementById('pv').value),
        earned_value: parseFloat(document.getElementById('ev').value),
        actual_cost: parseFloat(document.getElementById('ac').value),
        percentage_complete: parseFloat(document.getElementById('percentComplete').value)
    };

    fetch(`${API_BASE}/evm/${currentProjectId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(evmData)
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                let html = `
            <div class="alert alert-info">
                <h6>EVM Metrics Calculated</h6>
                <div class="row mt-2">
                    <div class="col-md-4">
                        <strong>Cost Variance:</strong> ${data.metrics.cost_variance.toFixed(2)}
                    </div>
                    <div class="col-md-4">
                        <strong>Schedule Variance:</strong> ${data.metrics.schedule_variance.toFixed(2)}
                    </div>
                    <div class="col-md-4">
                        <strong>Cost Performance Index:</strong> ${data.metrics.cost_performance_index.toFixed(2)}
                    </div>
                </div>
                <div class="row mt-2">
                    <div class="col-md-6">
                        <strong>Schedule Performance Index:</strong> ${data.metrics.schedule_performance_index.toFixed(2)}
                    </div>
                    <div class="col-md-6">
                        <strong>Estimate at Completion:</strong> ${data.estimate_at_completion.toFixed(2)}
                    </div>
                </div>
            </div>
            
            <div class="alert alert-${data.project_status === 'Green' ? 'success' : data.project_status === 'Yellow' ? 'warning' : 'danger'} mt-3">
                <strong>Project Status: <span class="status-${data.project_status.toLowerCase()}">${data.project_status}</span></strong>
                <div class="mt-2">${data.status_reason}</div>
            </div>
            `;

                document.getElementById('evmMetrics').innerHTML = html;
                showAlert('EVM data recorded successfully', 'success');
                document.getElementById('evmForm').reset();

                // Update charts
                createEVMCharts(data.metrics, data.project_status);
            } else {
                showAlert('Error: ' + data.error, 'danger');
            }
        })
        .catch(err => {
            console.error(err);
            showAlert('Error recording EVM data', 'danger');
        });
}

function createEVMCharts(metrics, status) {
    // Status Indicator Chart
    const statusCtx = document.getElementById('statusChart');
    if (statusCtx) {
        if (chartInstances.statusChart) {
            chartInstances.statusChart.destroy();
        }

        const statusColor = status === 'Green' ? '#198754' : status === 'Yellow' ? '#ffc107' : '#dc3545';

        chartInstances.statusChart = new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: [status, 'Other'],
                datasets: [{
                    data: [100, 0],
                    backgroundColor: [statusColor, '#f0f0f0'],
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // Performance Indices Chart
    const evmCtx = document.getElementById('evmChart');
    if (evmCtx) {
        if (chartInstances.evmChart) {
            chartInstances.evmChart.destroy();
        }

        chartInstances.evmChart = new Chart(evmCtx, {
            type: 'bar',
            data: {
                labels: ['CPI', 'SPI'],
                datasets: [{
                    label: 'Performance Index',
                    data: [metrics.cost_performance_index, metrics.schedule_performance_index],
                    backgroundColor: ['#0d6efd', '#198754'],
                    borderRadius: 4,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1.5
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
}

// ==================== DASHBOARD MODULE ====================

function loadDashboard() {
    const projectId = document.getElementById('dashboardProject').value;
    if (!projectId) return;

    fetch(`${API_BASE}/reports/${projectId}`)
        .then(res => res.json())
        .then(data => {
            let html = `
            <div class="row">
                <div class="col-md-6">
                    <div class="card bg-light">
                        <div class="card-body">
                            <h6>Project Information</h6>
                            <table class="table table-sm">
                                <tr><td><strong>Name:</strong></td><td>${data.project.name}</td></tr>
                                <tr><td><strong>Type:</strong></td><td>${data.project.type}</td></tr>
                                <tr><td><strong>Size (KLOC):</strong></td><td>${data.project.size_kloc}</td></tr>
                                <tr><td><strong>Experience Level:</strong></td><td>${data.project.team_experience}</td></tr>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card bg-light">
                        <div class="card-body">
                            <h6>Estimation Summary</h6>
                            <table class="table table-sm">
                                <tr><td><strong>Model:</strong></td><td>${data.estimation.model_used}</td></tr>
                                <tr><td><strong>Effort:</strong></td><td>${data.estimation.effort_person_months} PM</td></tr>
                                <tr><td><strong>Duration:</strong></td><td>${data.estimation.duration_months} months</td></tr>
                                <tr><td><strong>Total Cost:</strong></td><td>${data.estimation.total_cost.toFixed(2)}</td></tr>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            `;

            if (data.evm && data.evm.project_status !== 'Not Tracked') {
                html += `
                <div class="row mt-3">
                    <div class="col-md-12">
                        <div class="card bg-light">
                            <div class="card-body">
                                <h6>EVM Status</h6>
                                <p><strong>Project Status:</strong> <span class="status-${data.evm.project_status.toLowerCase()}">${data.evm.project_status}</span></p>
                                <p><strong>Cost Variance:</strong> ${data.evm.cost_variance.toFixed(2)} | 
                                   <strong>Schedule Variance:</strong> ${data.evm.schedule_variance.toFixed(2)}</p>
                                <p><strong>CPI:</strong> ${data.evm.cost_performance_index.toFixed(2)} | 
                                   <strong>SPI:</strong> ${data.evm.schedule_performance_index.toFixed(2)}</p>
                            </div>
                        </div>
                    </div>
                </div>
                `;
            }

            document.getElementById('dashboardContent').innerHTML = html;
        })
        .catch(err => {
            console.error(err);
            showAlert('Error loading dashboard', 'danger');
        });
}

// ==================== REPORT MODULE ====================

function loadReport() {
    const projectId = document.getElementById('reportProject').value;
    if (!projectId) return;

    fetch(`${API_BASE}/reports/${projectId}`)
        .then(res => res.json())
        .then(data => {
            generateReportHTML(data);
        })
        .catch(err => {
            console.error(err);
            showAlert('Error generating report', 'danger');
        });
}

function generateReportHTML(data) {
    let html = `
    <div id="reportPrintContent" class="report-container">
        <h3>Software Project Estimation Report</h3>
        <p><em>Generated: ${new Date().toLocaleString()}</em></p>
        
        <h5>1. Project Information</h5>
        <table class="table table-bordered">
            <tr><td><strong>Project Name</strong></td><td>${data.project.name}</td></tr>
            <tr><td><strong>Project Type</strong></td><td>${data.project.type}</td></tr>
            <tr><td><strong>Size (KLOC)</strong></td><td>${data.project.size_kloc}</td></tr>
            <tr><td><strong>Cost per Person-Month</strong></td><td>${data.project.cost_per_person_month}</td></tr>
            <tr><td><strong>Team Experience</strong></td><td>${data.project.team_experience}</td></tr>
        </table>
        
        <h5>2. Effort Estimation Results</h5>
        <table class="table table-bordered">
            <tr><td><strong>COCOMO Model Used</strong></td><td>${data.estimation.model_used}</td></tr>
            <tr><td><strong>Effort Estimate (Person-Months)</strong></td><td>${data.estimation.effort_person_months}</td></tr>
            <tr><td><strong>Duration (Months)</strong></td><td>${data.estimation.duration_months}</td></tr>
            <tr><td><strong>Total Project Cost</strong></td><td>${data.estimation.total_cost.toFixed(2)}</td></tr>
            <tr><td><strong>Risk Adjustment Factor</strong></td><td>${data.estimation.risk_adjustment_factor}</td></tr>
        </table>
    `;

    if (data.risks && data.risks.length > 0) {
        html += '<h5>3. Project Risks</h5><table class="table table-bordered"><thead><tr><th>Risk</th><th>Category</th><th>Probability</th><th>Impact</th><th>Adjustment</th></tr></thead><tbody>';
        data.risks.forEach(risk => {
            html += `<tr><td>${risk.name}</td><td>${risk.category}</td><td>${risk.probability}</td><td>${risk.impact}</td><td>${risk.adjustment_factor}</td></tr>`;
        });
        html += '</tbody></table>';
    }

    if (data.evm && data.evm.project_status !== 'Not Tracked') {
        html += `
        <h5>4. Earned Value Management</h5>
        <table class="table table-bordered">
            <tr><td><strong>Planned Value (PV)</strong></td><td>${data.evm.planned_value.toFixed(2)}</td></tr>
            <tr><td><strong>Earned Value (EV)</strong></td><td>${data.evm.earned_value.toFixed(2)}</td></tr>
            <tr><td><strong>Actual Cost (AC)</strong></td><td>${data.evm.actual_cost.toFixed(2)}</td></tr>
            <tr><td><strong>Cost Variance (CV)</strong></td><td>${data.evm.cost_variance.toFixed(2)}</td></tr>
            <tr><td><strong>Schedule Variance (SV)</strong></td><td>${data.evm.schedule_variance.toFixed(2)}</td></tr>
            <tr><td><strong>Cost Performance Index (CPI)</strong></td><td>${data.evm.cost_performance_index.toFixed(2)}</td></tr>
            <tr><td><strong>Schedule Performance Index (SPI)</strong></td><td>${data.evm.schedule_performance_index.toFixed(2)}</td></tr>
            <tr><td><strong>Project Status</strong></td><td><span class="status-${data.evm.project_status.toLowerCase()}">${data.evm.project_status}</span></td></tr>
            <tr><td><strong>Progress</strong></td><td>${data.evm.percentage_complete}%</td></tr>
        </table>
        `;
    }

    html += '</div>';
    document.getElementById('reportContent').innerHTML = html;
}

function printReport() {
    window.print();
}

// ==================== UTILITY FUNCTIONS ====================

function showAlert(message, type) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Insert at top of main content
    const mainContent = document.querySelector('.container-fluid');
    mainContent.insertBefore(alertDiv, mainContent.firstChild);

    // Auto-dismiss after 5 seconds
    setTimeout(() => alertDiv.remove(), 5000);
}
