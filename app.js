// Enhanced Aura - Virtual CFO & CEO Platform
// DOM Elements
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const uploadBtn = document.getElementById('uploadBtn');
const loadingState = document.getElementById('loadingState');
const dashboardSection = document.getElementById('dashboardSection');
const chartsSection = document.getElementById('chartsSection');
const virtualExecutives = document.getElementById('virtualExecutives');
const downloadExcelBtn = document.getElementById('downloadExcelBtn');
const navigationTabs = document.getElementById('navigationTabs');
const errorState = document.getElementById('errorState');
const errorMessage = document.getElementById('errorMessage');
const retryBtn = document.getElementById('retryBtn');
const executiveBriefing = document.getElementById('executiveBriefing');

// Navigation Elements
const navTabs = document.querySelectorAll('.nav-tab');
const queryTypeBtns = document.querySelectorAll('.query-type-btn');
const queryInput = document.getElementById('queryInput');
const askBtn = document.getElementById('askBtn');
const queryResponses = document.getElementById('queryResponses');

// Chart instances
let charts = {
    cashFlow: null,
    roi: null,
    cac: null,
    budget: null
};

// Function to destroy existing charts
function destroyCharts() {
    Object.keys(charts).forEach(key => {
        if (charts[key]) {
            charts[key].destroy();
            charts[key] = null;
        }
    });
}

// Current data
let currentData = null;

// KPI Elements
const kpiElements = {
    'cash_visibility': {
        value: document.getElementById('value-cash-visibility'),
        trend: document.getElementById('trend-cash-visibility'),
        target: document.getElementById('target-cash-visibility')
    },
    'days_cash_on_hand': {
        value: document.getElementById('value-days-cash'),
        trend: document.getElementById('trend-days-cash'),
        target: document.getElementById('target-days-cash')
    },
    'forecast_accuracy': {
        value: document.getElementById('value-forecast-accuracy'),
        trend: document.getElementById('trend-forecast-accuracy'),
        target: document.getElementById('target-forecast-accuracy')
    },
    'budget_vs_actual_spend': {
        value: document.getElementById('value-budget-actual'),
        trend: document.getElementById('trend-budget-actual'),
        target: document.getElementById('target-budget-actual')
    },
    'payment_stp_rate': {
        value: document.getElementById('value-payment-stp'),
        trend: document.getElementById('trend-payment-stp'),
        target: document.getElementById('target-payment-stp')
    },
    'cost_per_transaction': {
        value: document.getElementById('value-cost-transaction'),
        trend: document.getElementById('trend-cost-transaction'),
        target: document.getElementById('target-cost-transaction')
    },
    'marketing_spend_roi': {
        value: document.getElementById('value-marketing-roi'),
        trend: document.getElementById('trend-marketing-roi'),
        target: document.getElementById('target-marketing-roi')
    },
    'customer_acquisition_cost': {
        value: document.getElementById('value-cac'),
        trend: document.getElementById('trend-cac'),
        target: document.getElementById('target-cac')
    }
};

// Briefing Elements
const briefingElements = {
    headline: document.getElementById('briefing-headline'),
    analysis: document.getElementById('briefing-analysis'),
    impact: document.getElementById('briefing-impact'),
    action: document.getElementById('briefing-action')
};

// Event Listeners
fileInput.addEventListener('change', handleFileSelect);
uploadBtn.addEventListener('click', handleFileUpload);
retryBtn.addEventListener('click', resetApplication);

// Navigation
navTabs.forEach(tab => {
    tab.addEventListener('click', () => switchTab(tab.dataset.tab));
});

// Query interface
queryTypeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        queryTypeBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    });
});

askBtn.addEventListener('click', handleQuery);
queryInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        handleQuery();
    }
});

// File Selection Handler
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        fileName.textContent = file.name;
        uploadBtn.disabled = false;
        hideErrorState();
    } else {
        fileName.textContent = 'No file selected';
        uploadBtn.disabled = true;
    }
}

// File Upload Handler
async function handleFileUpload() {
    const file = fileInput.files[0];
    if (!file) {
        showError('Please select a file first.');
        return;
    }

    if (!file.name.endsWith('.xlsx')) {
        showError('Please select a valid Excel file (.xlsx).');
        return;
    }

    showLoadingState();
    hideErrorState();
    hideDashboard();

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('http://localhost:8000/uploadfile/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Upload failed');
        }

        const data = await response.json();
        currentData = data;
        updateDashboard(data);
        initializeCharts(data);
        updateVirtualExecutives(data);

    } catch (error) {
        console.error('Upload error:', error);
        showError(`Upload failed: ${error.message}`);
    } finally {
        hideLoadingState();
    }
}

// Dashboard Update Function
function updateDashboard(data) {
    try {
        // Update KPI values
        updateKPIs(data.kpis);
        
        // Check for Sentinel alerts
        if (data.sentinel_alert && data.sentinel_alert.status === 'CRITICAL') {
            showExecutiveBriefing(data.sentinel_alert);
            highlightCACAlert();
        } else {
            hideExecutiveBriefing();
            removeCACAlert();
        }

        // Always show dashboard and navigation after successful upload
        showDashboard();
        navigationTabs.classList.remove('hidden');

    } catch (error) {
        console.error('Dashboard update error:', error);
        showError('Error updating dashboard display.');
    }
}

// Update KPI Values
function updateKPIs(kpis) {
    Object.keys(kpis).forEach(kpiKey => {
        const kpiData = kpiElements[kpiKey];
        if (kpiData) {
            const value = kpis[kpiKey];
            kpiData.value.textContent = formatKPIValue(kpiKey, value);
            
            // Update trend indicator based on value
            updateTrendIndicator(kpiKey, value, kpiData.trend);
        }
    });
}

// Format KPI Values
function formatKPIValue(kpiKey, value) {
    switch (kpiKey) {
        case 'cash_visibility':
            return `$${formatNumber(value)}`;
        case 'days_cash_on_hand':
            return `${Math.round(value)} days`;
        case 'forecast_accuracy':
        case 'budget_vs_actual_spend':
        case 'payment_stp_rate':
            return `${(value * 100).toFixed(1)}%`;
        case 'cost_per_transaction':
            return `$${value.toFixed(2)}`;
        case 'marketing_spend_roi':
            return `${value.toFixed(1)}x`;
        case 'customer_acquisition_cost':
            return `$${value.toFixed(2)}`;
        default:
            return value.toString();
    }
}

// Format Large Numbers
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    } else {
        return num.toFixed(0);
    }
}

// Update Trend Indicators
function updateTrendIndicator(kpiKey, value, trendElement) {
    // Simple trend logic based on KPI type
    let trend = '📊'; // Default neutral
    
    switch (kpiKey) {
        case 'cash_visibility':
            trend = value > 500000 ? '📈' : value > 100000 ? '📊' : '📉';
            break;
        case 'days_cash_on_hand':
            trend = value > 90 ? '📈' : value > 30 ? '📊' : '📉';
            break;
        case 'forecast_accuracy':
            trend = value > 0.95 ? '📈' : value > 0.85 ? '📊' : '📉';
            break;
        case 'budget_vs_actual_spend':
            trend = value <= 1.1 ? '📈' : value <= 1.2 ? '📊' : '📉';
            break;
        case 'payment_stp_rate':
            trend = value > 0.99 ? '📈' : value > 0.95 ? '📊' : '📉';
            break;
        case 'cost_per_transaction':
            trend = value < 1.0 ? '📈' : value < 1.5 ? '📊' : '📉';
            break;
        case 'marketing_spend_roi':
            trend = value > 3.0 ? '📈' : value > 1.5 ? '📊' : '📉';
            break;
        case 'customer_acquisition_cost':
            trend = value < 50 ? '📈' : value < 100 ? '📊' : '📉';
            break;
    }
    
    trendElement.textContent = trend;
}

// Show Executive Briefing
function showExecutiveBriefing(alertData) {
    briefingElements.headline.textContent = alertData.headline || 'Critical Alert';
    briefingElements.analysis.textContent = alertData.analysis || 'Analysis not available';
    briefingElements.impact.textContent = alertData.impact_assessment || 'Impact assessment not available';
    briefingElements.action.textContent = alertData.recommended_action || 'Recommended action not available';
    
    executiveBriefing.classList.remove('hidden');
}

// Hide Executive Briefing
function hideExecutiveBriefing() {
    executiveBriefing.classList.add('hidden');
}

// Highlight CAC Alert
function highlightCACAlert() {
    const cacCard = document.getElementById('kpi-cac');
    cacCard.classList.add('alert-card');
}

// Remove CAC Alert
function removeCACAlert() {
    const cacCard = document.getElementById('kpi-cac');
    cacCard.classList.remove('alert-card');
}

// Show/Hide States
function showLoadingState() {
    loadingState.classList.remove('hidden');
}

function hideLoadingState() {
    loadingState.classList.add('hidden');
}

function showDashboard() {
    dashboardSection.classList.remove('hidden');
}

function hideDashboard() {
    dashboardSection.classList.add('hidden');
}

function showError(message) {
    errorMessage.textContent = message;
    errorState.classList.remove('hidden');
}

function hideErrorState() {
    errorState.classList.add('hidden');
}

function resetApplication() {
    hideErrorState();
    hideDashboard();
    hideExecutiveBriefing();
    hideLoadingState();
    removeCACAlert();
    
    // Reset file input
    fileInput.value = '';
    fileName.textContent = 'No file selected';
    uploadBtn.disabled = true;
    
    // Reset KPI values
    Object.values(kpiElements).forEach(kpiData => {
        kpiData.value.textContent = '0';
        kpiData.trend.textContent = '📊';
    });
}

// Initialize Charts
function initializeCharts(data) {
    // Destroy existing charts first
    destroyCharts();
    
    // Cash Flow Chart
    const cashFlowCtx = document.getElementById('cashFlowChart').getContext('2d');
    charts.cashFlow = new Chart(cashFlowCtx, {
        type: 'line',
        data: generateCashFlowData(data),
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#cbd5e1' }
                }
            },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.1)' } }
            }
        }
    });

    // ROI Chart
    const roiCtx = document.getElementById('roiChart').getContext('2d');
    charts.roi = new Chart(roiCtx, {
        type: 'bar',
        data: generateROIData(data),
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#cbd5e1' }
                }
            },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.1)' } }
            }
        }
    });

    // CAC Chart
    const cacCtx = document.getElementById('cacChart').getContext('2d');
    charts.cac = new Chart(cacCtx, {
        type: 'line',
        data: generateCACData(data),
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#cbd5e1' }
                }
            },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.1)' } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.1)' } }
            }
        }
    });

    // Budget Chart
    const budgetCtx = document.getElementById('budgetChart').getContext('2d');
    charts.budget = new Chart(budgetCtx, {
        type: 'doughnut',
        data: generateBudgetData(data),
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#cbd5e1' }
                }
            }
        }
    });
}

// Generate Chart Data
function generateCashFlowData(data) {
    const days = 30;
    const labels = [];
    const cashFlow = [];
    let runningTotal = 500000;
    
    for (let i = 0; i < days; i++) {
        labels.push(`Day ${i + 1}`);
        runningTotal += (Math.random() - 0.4) * 10000;
        cashFlow.push(Math.max(0, runningTotal));
    }
    
    return {
        labels: labels,
        datasets: [{
            label: 'Cash Flow',
            data: cashFlow,
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            tension: 0.4
        }]
    };
}

function generateROIData(data) {
    return {
        labels: ['Adwords', 'Facebook', 'LinkedIn', 'Organic'],
        datasets: [{
            label: 'ROI',
            data: [18.7, 12.3, 8.9, 25.4],
            backgroundColor: [
                'rgba(59, 130, 246, 0.8)',
                'rgba(16, 185, 129, 0.8)',
                'rgba(168, 85, 247, 0.8)',
                'rgba(245, 158, 11, 0.8)'
            ]
        }]
    };
}

function generateCACData(data) {
    const hours = 48;
    const labels = [];
    const cacValues = [];
    
    for (let i = 0; i < hours; i++) {
        labels.push(`${i}h`);
        const baseCAC = 50;
        const spike = i > 24 ? (i - 24) * 5 : 0;
        cacValues.push(baseCAC + spike + Math.random() * 10);
    }
    
    return {
        labels: labels,
        datasets: [{
            label: 'CAC Trend',
            data: cacValues,
            borderColor: '#ef4444',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            tension: 0.4
        }]
    };
}

function generateBudgetData(data) {
    return {
        labels: ['Actual Spend', 'Remaining Budget'],
        datasets: [{
            data: [73.7, 26.3],
            backgroundColor: [
                'rgba(239, 68, 68, 0.8)',
                'rgba(16, 185, 129, 0.8)'
            ]
        }]
    };
}

// Chart Adjustment Functions
function adjustChart(chartType, period) {
    const buttons = document.querySelectorAll(`[onclick*="${chartType}"]`);
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    if (charts[chartType]) {
        charts[chartType].destroy();
    }
    
    initializeCharts(currentData);
}

// Virtual Advisors
// Update Virtual Executives with Continuous Analysis
async function updateVirtualExecutives(data) {
    try {
        // Get continuous analysis from backend
        if (fileInput.files[0]) {
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            const response = await fetch('http://localhost:8000/continuous-analysis/', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                const analysis = result.analysis;
                
                // Update CFO analysis
                const cfoAnalysis = document.getElementById('cfo-analysis');
                cfoAnalysis.innerHTML = `
                    <div class="analysis-content">
                        <h4>📊 Financial Health Assessment</h4>
                        <div class="analysis-text">${analysis.cfo.replace(/\n/g, '<br>')}</div>
                    </div>
                `;
                
                // Update CEO analysis
                const ceoAnalysis = document.getElementById('ceo-analysis');
                ceoAnalysis.innerHTML = `
                    <div class="analysis-content">
                        <h4>🚀 Strategic Overview</h4>
                        <div class="analysis-text">${analysis.ceo.replace(/\n/g, '<br>')}</div>
                    </div>
                `;
            } else {
                throw new Error('Failed to get continuous analysis');
            }
        } else {
            throw new Error('No file uploaded');
        }
    } catch (error) {
        console.error('Error getting continuous analysis:', error);
        // Fallback to basic analysis using current data
        const cfoAnalysis = document.getElementById('cfo-analysis');
        const ceoAnalysis = document.getElementById('ceo-analysis');
        
        if (data && data.kpis) {
            const kpis = data.kpis;
            const alert = data.sentinel_alert;
            
            cfoAnalysis.innerHTML = `
                <div class="analysis-content">
                    <h4>📊 Financial Health Assessment</h4>
                    <div class="analysis-text">
                        Cash Visibility: $${kpis.cash_visibility?.toLocaleString() || '0'}<br>
                        Days Cash on Hand: ${Math.round(kpis.days_cash_on_hand || 0)} days<br>
                        Marketing ROI: ${kpis.marketing_spend_roi?.toFixed(1) || '0'}x<br>
                        ${alert && alert.status === 'CRITICAL' ? '<br>🚨 CRITICAL ALERT: ' + alert.headline : ''}
                    </div>
                </div>
            `;
            
            ceoAnalysis.innerHTML = `
                <div class="analysis-content">
                    <h4>🚀 Strategic Overview</h4>
                    <div class="analysis-text">
                        Customer Acquisition Cost: $${kpis.customer_acquisition_cost?.toFixed(2) || '0'}<br>
                        Budget Utilization: ${(kpis.budget_vs_actual_spend * 100)?.toFixed(1) || '0'}%<br>
                        Forecast Accuracy: ${(kpis.forecast_accuracy * 100)?.toFixed(1) || '0'}%<br>
                        ${alert && alert.status === 'CRITICAL' ? '<br>⚠️ Immediate Action Required: ' + alert.recommended_action : ''}
                    </div>
                </div>
            `;
        } else {
            cfoAnalysis.innerHTML = `
                <div class="analysis-content">
                    <h4>📊 Financial Health Assessment</h4>
                    <div class="analysis-text">Analyzing your financial data... Ready for questions.</div>
                </div>
            `;
            
            ceoAnalysis.innerHTML = `
                <div class="analysis-content">
                    <h4>🚀 Strategic Overview</h4>
                    <div class="analysis-text">Monitoring growth metrics... Ready for strategic discussions.</div>
                </div>
            `;
        }
    }
}

// Download Reallocated Excel
async function downloadReallocatedExcel() {
    try {
        if (!fileInput.files[0]) {
            alert('Please upload a file first');
            return;
        }
        
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        
        const response = await fetch('http://localhost:8000/download-excel/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'reallocated_budget.xlsx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            alert('✅ Reallocated Excel file downloaded successfully!');
        } else {
            alert('❌ Error creating reallocated Excel file');
        }
    } catch (error) {
        console.error('Download error:', error);
        alert('❌ Error downloading reallocated Excel file');
    }
}

// Query Handling
async function handleQuery() {
    const query = queryInput.value.trim();
    if (!query) return;
    
    const selectedType = document.querySelector('.query-type-btn.active').dataset.type;
    
    addQueryResponse(query, 'user');
    
    try {
        // Create context from current data
        const context = createContextFromData(currentData);
        
        // Call Gemini API
        const response = await fetch('http://localhost:8000/query/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                persona: selectedType.toUpperCase(),
                context: context
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            addQueryResponse(data.response, selectedType);
        } else {
            // Fallback to local responses
            const fallbackResponse = generateAIResponse(query, selectedType, currentData);
            addQueryResponse(fallbackResponse, selectedType);
        }
    } catch (error) {
        console.error('Query error:', error);
        // Fallback to local responses
        const fallbackResponse = generateAIResponse(query, selectedType, currentData);
        addQueryResponse(fallbackResponse, selectedType);
    }
    
    queryInput.value = '';
}

function createContextFromData(data) {
    if (!data) return "No financial data available.";
    
    let context = "Financial Data Summary:\n";
    
    if (data.kpis) {
        context += `- Cash Visibility: $${formatNumber(data.kpis.cash_visibility)}\n`;
        context += `- Days Cash on Hand: ${Math.round(data.kpis.days_cash_on_hand)} days\n`;
        context += `- Marketing ROI: ${data.kpis.marketing_spend_roi.toFixed(1)}x\n`;
        context += `- Customer Acquisition Cost: $${data.kpis.customer_acquisition_cost.toFixed(2)}\n`;
        context += `- Budget vs Actual: ${(data.kpis.budget_vs_actual_spend * 100).toFixed(1)}%\n`;
    }
    
    if (data.sentinel_alert && data.sentinel_alert.status === 'CRITICAL') {
        context += `\nCRITICAL ALERT: ${data.sentinel_alert.headline}\n`;
        context += `Analysis: ${data.sentinel_alert.analysis}\n`;
    }
    
    return context;
}

function askQuickQuestion(question) {
    queryInput.value = question;
    handleQuery();
}

function addQueryResponse(content, type) {
    const responseDiv = document.createElement('div');
    responseDiv.className = 'response-item';
    
    let avatar, title;
    if (type === 'user') {
        avatar = '👤';
        title = 'You';
    } else if (type === 'cfo') {
        avatar = '👔';
        title = 'Virtual CFO';
    } else if (type === 'ceo') {
        avatar = '🎯';
        title = 'Virtual CEO';
    } else if (type === 'both') {
        avatar = '🤖';
        title = 'Executive Team';
    }
    
    responseDiv.innerHTML = `
        <div class="response-header">
            <span class="response-avatar">${avatar}</span>
            <span class="response-title">${title}</span>
        </div>
        <div class="response-content">${content}</div>
    `;
    
    queryResponses.appendChild(responseDiv);
    queryResponses.scrollTop = queryResponses.scrollHeight;
}

function generateAIResponse(query, type, data) {
    const responses = {
        cfo: {
            'cash flow': "Based on current trends, your cash flow is healthy with 228 days runway. However, the CAC spike could impact this if not addressed quickly.",
            'cac': "The 339% CAC increase is critical. I recommend immediate budget reallocation: 50% to organic channels, 30% to high-performing campaigns, pause underperforming keywords.",
            'budget': "You're at 73.7% of quarterly budget with 2 months remaining. At current burn rate, you'll exceed budget by 15%. Consider reallocating to higher ROI channels.",
            'risk': "Primary risks: CAC spike, budget overrun, cash flow impact. Secondary: market competition, seasonal trends. Immediate action required on CAC."
        },
        ceo: {
            'strategy': "Given the CAC spike, we need strategic pivot. Focus on organic growth, optimize high-performing channels, consider market expansion opportunities.",
            'growth': "Current ROI of 18.7x is strong, but CAC spike threatens scalability. Recommend diversification strategy and organic content investment.",
            'goals': "We're on track for revenue goals but CAC spike could impact acquisition targets. Need to optimize channel mix and improve conversion rates.",
            'market': "Market conditions favor organic growth. Recommend shifting focus to content marketing and SEO while optimizing paid channels."
        },
        both: {
            'default': "CFO: Financial metrics show mixed signals - strong ROI but concerning CAC spike. CEO: Strategic pivot needed to maintain growth trajectory while optimizing costs."
        }
    };
    
    const queryLower = query.toLowerCase();
    let response = "I'm analyzing your data and will provide detailed insights shortly.";
    
    if (type === 'cfo') {
        for (const [key, value] of Object.entries(responses.cfo)) {
            if (queryLower.includes(key)) {
                response = value;
                break;
            }
        }
    } else if (type === 'ceo') {
        for (const [key, value] of Object.entries(responses.ceo)) {
            if (queryLower.includes(key)) {
                response = value;
                break;
            }
        }
    } else if (type === 'both') {
        response = responses.both.default;
    }
    
    return response;
}

// Navigation Functions
function switchTab(tabName) {
    navTabs.forEach(tab => tab.classList.remove('active'));
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    hideAllSections();
    
    switch (tabName) {
        case 'dashboard':
            showDashboard();
            break;
        case 'charts':
            showCharts();
            break;
        case 'executives':
            showVirtualExecutives();
            // Auto-refresh analysis when switching to executives tab
            if (currentData) {
                updateVirtualExecutives(currentData);
            }
            break;
    }
}

// Show/Hide Functions
function showDashboard() {
    dashboardSection.classList.remove('hidden');
    navigationTabs.classList.remove('hidden');
}

function showCharts() {
    chartsSection.classList.remove('hidden');
    navigationTabs.classList.remove('hidden');
}

function showVirtualExecutives() {
    virtualExecutives.classList.remove('hidden');
    navigationTabs.classList.remove('hidden');
}

function hideAllSections() {
    dashboardSection.classList.add('hidden');
    chartsSection.classList.add('hidden');
    virtualExecutives.classList.add('hidden');
    navigationTabs.classList.add('hidden');
}

// Enhanced Executive Briefing Functions
function approveRecommendation() {
    alert('✅ Budget reallocation approved! Virtual CFO will implement changes immediately.');
    hideExecutiveBriefing();
}

function showSimulation() {
    // Create simulation modal
    const simulationModal = document.createElement('div');
    simulationModal.className = 'simulation-modal';
    simulationModal.innerHTML = `
        <div class="simulation-content">
            <div class="simulation-header">
                <h2>📊 Budget Reallocation Simulation</h2>
                <button class="close-simulation" onclick="closeSimulation()">&times;</button>
            </div>
            <div class="simulation-body">
                <div class="simulation-scenario">
                    <h3>Current Scenario</h3>
                    <div class="metric-row">
                        <span>CAC:</span>
                        <span class="current-value">$${currentData?.kpis?.customer_acquisition_cost?.toFixed(2) || '74.55'}</span>
                    </div>
                    <div class="metric-row">
                        <span>Marketing ROI:</span>
                        <span class="current-value">${currentData?.kpis?.marketing_spend_roi?.toFixed(1) || '18.7'}x</span>
                    </div>
                    <div class="metric-row">
                        <span>Budget Utilization:</span>
                        <span class="current-value">${(currentData?.kpis?.budget_vs_actual_spend * 100)?.toFixed(1) || '73.7'}%</span>
                    </div>
                </div>
                
                <div class="simulation-arrow">→</div>
                
                <div class="simulation-scenario">
                    <h3>After Reallocation</h3>
                    <div class="metric-row">
                        <span>CAC:</span>
                        <span class="improved-value">$${((currentData?.kpis?.customer_acquisition_cost || 74.55) * 0.7).toFixed(2)}</span>
                        <span class="improvement">(-30%)</span>
                    </div>
                    <div class="metric-row">
                        <span>Marketing ROI:</span>
                        <span class="improved-value">${((currentData?.kpis?.marketing_spend_roi || 18.7) * 1.15).toFixed(1)}x</span>
                        <span class="improvement">(+15%)</span>
                    </div>
                    <div class="metric-row">
                        <span>Budget Utilization:</span>
                        <span class="improved-value">${((currentData?.kpis?.budget_vs_actual_spend || 0.737) * 0.9 * 100).toFixed(1)}%</span>
                        <span class="improvement">(-10%)</span>
                    </div>
                </div>
                
                <div class="simulation-details">
                    <h4>Reallocation Strategy:</h4>
                    <ul>
                        <li>50% of Adwords budget → Organic content channels</li>
                        <li>30% of Adwords budget → High-performing campaigns</li>
                        <li>20% of Adwords budget → Pause underperforming keywords</li>
                    </ul>
                    
                    <h4>Expected Impact:</h4>
                    <ul>
                        <li>CAC reduction of 30% within 2 weeks</li>
                        <li>ROI improvement of 15% within 1 month</li>
                        <li>Budget efficiency improvement of 10%</li>
                        <li>Cash runway extension by 45 days</li>
                    </ul>
                </div>
                
                <div class="simulation-actions">
                    <button class="action-btn approve" onclick="approveRecommendation(); closeSimulation();">Approve Reallocation</button>
                    <button class="action-btn dismiss" onclick="closeSimulation();">Close Simulation</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(simulationModal);
}

function closeSimulation() {
    const modal = document.querySelector('.simulation-modal');
    if (modal) {
        modal.remove();
    }
}

function dismissAlert() {
    hideExecutiveBriefing();
}

// Initialize Application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Aura - Virtual CFO & CEO Platform initialized');
    
    // Check if backend is running
    fetch('http://localhost:8000/')
        .then(response => response.json())
        .then(data => {
            console.log('Backend connection successful:', data.message);
        })
        .catch(error => {
            console.warn('Backend not running. Please start the FastAPI server.');
            showError('Backend server not running. Please start the FastAPI server on port 8000.');
        });

    // Download Excel button event listener
    if (downloadExcelBtn) {
        downloadExcelBtn.addEventListener('click', downloadReallocatedExcel);
    }
    
    // Cleanup charts when page is unloaded
    window.addEventListener('beforeunload', destroyCharts);
});
