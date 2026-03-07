// CivicGuardian AI - Demo Interface JavaScript

// Mock data from actual sample outputs
const mockRiskAnalysis = {
    case_id: "demo-001",
    risk_level: "HIGH",
    confidence: 0.87,
    deadline: "2026-02-28",
    required_action: "Submit proof of income to council",
    urgency_indicators: [
        "deadline mentioned",
        "benefit review",
        "14 day response window",
        "suspension risk"
    ],
    sender_authority: "Oxford City Council Housing Department"
};

const mockPolicyResponse = {
    skipped: false,
    reason: "",
    risk_level: "HIGH",
    draft_response: `Dear Housing Officer,

I am writing regarding the housing benefit review dated 15 February 2026. I understand documentation is required by 28 February 2026.

I am gathering the requested proof of income and will submit within the deadline. Please confirm receipt of this acknowledgement.

Thank you for your assistance.`,
    rationale_bullets: [
        "Acknowledges deadline urgency",
        "Confirms engagement with process",
        "Requests confirmation of receipt",
        "Professional and respectful tone"
    ],
    citations: [
        { quote: "housing benefit review", relevance: "Confirms subject matter" }
    ],
    legislation_referenced: ["Housing Benefit Regulations 2006"],
    confidence: 0.82,
    safety_notice: "DRAFT FOR REVIEW - Not legal advice"
};

const mockGovernorValidation = {
    validation_status: "APPROVED",
    confidence_score: 0.82,
    grounding_check: {
        citations_valid: true,
        hallucination_detected: false
    },
    safety_check: {
        contains_draft_notice: true,
        no_definitive_claims: true
    },
    issues_found: [],
    approved: true,
    required_escalation: true
};

const sampleLetterText = `From: Oxford City Council Housing Department
Date: 15 February 2026
Subject: Housing Benefit Review - Action Required

Dear Margaret,

Your housing benefit is under review. Please submit proof of income by 28 February 2026 to avoid suspension of payments.

We require the following documents:
- Last 3 months' bank statements
- Proof of any pension income
- Council tax bill

If you need help gathering these documents, please contact our support team on 01865 252000.

Failure to provide these documents by the deadline may result in suspension of your housing benefit payments.

Yours sincerely,
Housing Benefits Team
Oxford City Council`;

// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const loadSampleBtn = document.getElementById('loadSampleBtn');
const documentPreview = document.getElementById('documentPreview');
const thinkingStreamSection = document.getElementById('thinkingStreamSection');
const visualizationSection = document.getElementById('visualizationSection');
const draftingSuiteSection = document.getElementById('draftingSuiteSection');
const analyzeBtn = document.getElementById('analyzeBtn');
const resetBtn = document.getElementById('resetBtn');
const approveBtn = document.getElementById('approveBtn');

// Event Listeners
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', handleDragOver);
dropZone.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
loadSampleBtn.addEventListener('click', loadSampleLetter);
analyzeBtn.addEventListener('click', analyzeDocument);
resetBtn.addEventListener('click', resetInterface);
approveBtn.addEventListener('click', approveDocument);

// File handling
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.style.borderColor = 'var(--sky-cyan)';
    dropZone.style.transform = 'translateY(-4px)';
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.style.borderColor = '';
    dropZone.style.transform = '';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function processFile(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        displayPreview(file.name, file.size, content);
    };
    reader.readAsText(file);
}

function loadSampleLetter() {
    displayPreview('sample-letter.txt', 1234, sampleLetterText);
}

function displayPreview(fileName, fileSize, content) {
    document.getElementById('previewFilename').textContent = fileName;
    document.getElementById('previewFilesize').textContent = formatFileSize(fileSize);
    document.getElementById('previewContent').textContent = content;
    
    documentPreview.style.display = 'block';
    thinkingStreamSection.style.display = 'none';
    visualizationSection.style.display = 'none';
    draftingSuiteSection.style.display = 'none';
    
    // Smooth scroll to preview
    documentPreview.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Analysis simulation with thinking stream
function analyzeDocument() {
    // Show loading state
    analyzeBtn.disabled = true;
    document.getElementById('analyzeBtnText').textContent = 'Analysing...';
    document.getElementById('analyzeBtnSpinner').style.display = 'inline-block';
    
    // Show thinking stream section
    thinkingStreamSection.style.display = 'block';
    thinkingStreamSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // Simulate thinking stream
    const thinkingSteps = [
        { delay: 200, message: '[INIT] Document ingestion started...' },
        { delay: 500, message: '[EXTRACT] Parsing text content from uploaded file...' },
        { delay: 800, message: '[DETECT] Identified sender: Oxford City Council Housing Department' },
        { delay: 1200, message: '[ANALYZE] Extracting deadline: 28 February 2026' },
        { delay: 1500, message: '[BEDROCK] Invoking Risk Analyst Agent (Nova Lite)...' },
        { delay: 1800, message: '[RISK] Risk level: HIGH | Confidence: 87%' },
        { delay: 2100, message: '[BEDROCK] Invoking Policy Reasoner Agent (Nova Pro)...' },
        { delay: 2400, message: '[DRAFT] Generating response based on Housing Benefit Regulations 2006...' },
        { delay: 2700, message: '[VALIDATE] Running Governor validation checks...' },
        { delay: 3000, message: '[COMPLETE] Analysis complete. Displaying results...' }
    ];
    
    thinkingSteps.forEach(step => {
        setTimeout(() => streamThought(step.message), step.delay);
    });
    
    // Show results after thinking stream completes
    setTimeout(() => {
        displayResults();
        
        // Reset button state
        analyzeBtn.disabled = false;
        document.getElementById('analyzeBtnText').textContent = 'Analyze Document';
        document.getElementById('analyzeBtnSpinner').style.display = 'none';
    }, 3200);
}

// Stream a thought to the thinking stream
function streamThought(message) {
    const thinkingStream = document.getElementById('thinkingStream');
    const logEntry = document.createElement('div');
    logEntry.className = 'thinking-log';
    
    const timestamp = new Date().toLocaleTimeString('en-GB', { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit',
        fractionalSecondDigits: 3
    });
    
    logEntry.innerHTML = `<span class="timestamp">[${timestamp}]</span> <span class="message">${message}</span>`;
    thinkingStream.appendChild(logEntry);
    
    // Auto-scroll to bottom
    thinkingStream.scrollTop = thinkingStream.scrollHeight;
}

function displayResults() {
    // Show visualization and drafting suite sections
    visualizationSection.style.display = 'block';
    draftingSuiteSection.style.display = 'grid';
    
    // Update Risk Scorecard with data
    const urgency = 85; // HIGH risk = high urgency
    const complexity = 60; // Medium complexity
    const confidence = mockRiskAnalysis.confidence * 100;
    
    // Calculate deadline countdown
    const deadline = new Date(mockRiskAnalysis.deadline);
    const today = new Date();
    const daysRemaining = Math.ceil((deadline - today) / (1000 * 60 * 60 * 24));
    
    // Update Urgency Card
    document.getElementById('urgencyValue').textContent = 'HIGH';
    document.getElementById('urgencyBar').style.width = urgency + '%';
    document.getElementById('urgencyDetail').textContent = `Deadline within ${daysRemaining} days`;
    
    // Update Complexity Card
    document.getElementById('complexityValue').textContent = 'MEDIUM';
    document.getElementById('complexityBar').style.width = complexity + '%';
    document.getElementById('complexityDetail').textContent = 'Multi-document review';
    
    // Update Confidence Card
    document.getElementById('confidenceValue').textContent = Math.round(confidence) + '%';
    document.getElementById('confidenceBar').style.width = confidence + '%';
    document.getElementById('confidenceDetail').textContent = 'High certainty classification';
    
    // Update Priority Banner
    document.getElementById('deadlineCountdown').textContent = `${daysRemaining} days remaining`;
    
    // Populate Risk Assessment
    document.getElementById('riskBadge').textContent = mockRiskAnalysis.risk_level;
    document.getElementById('riskLevel').textContent = mockRiskAnalysis.risk_level;
    document.getElementById('riskConfidence').textContent = (mockRiskAnalysis.confidence * 100).toFixed(0) + '%';
    document.getElementById('deadline').textContent = formatDate(mockRiskAnalysis.deadline);
    document.getElementById('requiredAction').textContent = mockRiskAnalysis.required_action;
    
    const urgencyList = document.getElementById('urgencyIndicators');
    urgencyList.innerHTML = '';
    mockRiskAnalysis.urgency_indicators.forEach(indicator => {
        const li = document.createElement('li');
        li.textContent = indicator;
        urgencyList.appendChild(li);
    });
    
    // Populate Draft Response
    document.getElementById('draftText').textContent = mockPolicyResponse.draft_response;
    
    const rationaleList = document.getElementById('rationaleList');
    rationaleList.innerHTML = '';
    mockPolicyResponse.rationale_bullets.forEach(bullet => {
        const li = document.createElement('li');
        li.textContent = bullet;
        rationaleList.appendChild(li);
    });
    
    const legislationList = document.getElementById('legislationList');
    legislationList.innerHTML = '';
    mockPolicyResponse.legislation_referenced.forEach(law => {
        const li = document.createElement('li');
        li.textContent = law;
        legislationList.appendChild(li);
    });
    
    // Populate Validation
    document.getElementById('validationBadge').textContent = mockGovernorValidation.validation_status;
    document.getElementById('validationStatus').textContent = mockGovernorValidation.validation_status;
    document.getElementById('validationConfidence').textContent = (mockGovernorValidation.confidence_score * 100).toFixed(0) + '%';
    
    // Show/hide escalation notice
    document.getElementById('escalationNotice').style.display = 
        mockGovernorValidation.required_escalation ? 'block' : 'none';
    
    // Scroll to visualization
    visualizationSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function getRiskBadgeClass(riskLevel) {
    // Not used in new design - badges styled directly in CSS
    return '';
}

function getValidationBadgeClass(status) {
    // Not used in new design - badges styled directly in CSS
    return '';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB', { 
        day: 'numeric', 
        month: 'long', 
        year: 'numeric' 
    });
}

function resetInterface() {
    documentPreview.style.display = 'none';
    thinkingStreamSection.style.display = 'none';
    visualizationSection.style.display = 'none';
    draftingSuiteSection.style.display = 'none';
    fileInput.value = '';
    
    // Clear thinking stream
    document.getElementById('thinkingStream').innerHTML = '';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function approveDocument() {
    alert('✓ Document approved and forwarded to caseworker for review.\n\nIn production, this would:\n• Log approval in DynamoDB\n• Send SNS notification to caseworker\n• Update case status\n• Track deadline in monitoring system');
}


// ============================================
// KPI TOOLTIP FUNCTIONALITY
// ============================================

const kpiTooltipData = {
    processing: {
        title: "Cases Today (Demo Data)",
        content: `
            <p>This shows the <strong>number of cases processed today</strong> in a live system.</p>
            <p><strong>What it means:</strong> The system handles correspondence automatically as it arrives. Each letter, email, or document is analyzed within seconds.</p>
            <p><strong>How it works:</strong> When a vulnerable adult receives official mail (like housing benefit reviews or council notices), the system:</p>
            <ul>
                <li>Reads and understands the letter</li>
                <li>Identifies deadlines and risks</li>
                <li>Flags urgent cases for immediate attention</li>
                <li>Helps caseworkers respond quickly</li>
            </ul>
            <p><em>Note: 247 is synthetic demo data. Real usage would vary by organization size.</em></p>
        `
    },
    response: {
        title: "Average Response Time (Demo Data)",
        content: `
            <p>This shows <strong>how quickly the system analyzes each case</strong>.</p>
            <p><strong>What it means:</strong> Less than 3 seconds from upload to complete analysis. This includes risk assessment, draft response generation, and validation checks.</p>
            <p><strong>Why it matters:</strong> Traditional manual review can take hours or days. Fast processing means:</p>
            <ul>
                <li>Urgent cases are identified immediately</li>
                <li>Deadlines are never missed</li>
                <li>Caseworkers can focus on complex decisions</li>
                <li>Vulnerable adults get help faster</li>
            </ul>
            <p><em>Note: <3s is synthetic demo data based on AWS Bedrock performance estimates.</em></p>
        `
    },
    validation: {
        title: "System Accuracy (Demo Data)",
        content: `
            <p>This shows the <strong>accuracy of the AI's risk assessments and draft responses</strong>.</p>
            <p><strong>What it means:</strong> 94.2% of AI-generated outputs are approved by human caseworkers without major changes.</p>
            <p><strong>How we ensure accuracy:</strong> The system uses a 3-agent validation process:</p>
            <ul>
                <li><strong>Risk Analyst Agent:</strong> Identifies urgency, deadlines, and required actions</li>
                <li><strong>Policy Reasoner Agent:</strong> Drafts responses based on UK housing and benefits regulations</li>
                <li><strong>Governor Agent:</strong> Checks for errors, hallucinations, and compliance issues</li>
            </ul>
            <p><strong>Human oversight:</strong> Every output requires caseworker approval before sending. The AI assists, humans decide.</p>
            <p><em>Note: 94.2% is synthetic demo data. Real accuracy would be measured through pilot testing.</em></p>
        `
    },
    oversight: {
        title: "Active Users (Demo Data)",
        content: `
            <p>This shows the <strong>number of caseworkers using the system</strong>.</p>
            <p><strong>What it means:</strong> 1,500+ social care professionals, housing officers, and support workers actively using the platform to help vulnerable adults.</p>
            <p><strong>Who uses it:</strong></p>
            <ul>
                <li><strong>Social workers:</strong> Managing cases for adults with dementia or learning disabilities</li>
                <li><strong>Housing officers:</strong> Preventing evictions from missed correspondence</li>
                <li><strong>Benefits advisors:</strong> Ensuring timely responses to avoid payment suspensions</li>
                <li><strong>Care coordinators:</strong> Protecting isolated elderly residents</li>
            </ul>
            <p><strong>100% human-in-the-loop:</strong> Every AI recommendation requires human approval. The system supports decisions, it doesn't make them.</p>
            <p><em>Note: 1,500+ is synthetic demo data representing potential scale across UK councils.</em></p>
        `
    }
};

// Get modal elements
const kpiTooltipModal = document.getElementById('kpiTooltipModal');
const kpiTooltipOverlay = document.getElementById('kpiTooltipOverlay');
const kpiTooltipClose = document.getElementById('kpiTooltipClose');
const kpiTooltipBody = document.getElementById('kpiTooltipBody');

// Add click handlers to KPI cards
document.querySelectorAll('.kpi-card-clickable').forEach(card => {
    card.addEventListener('click', function() {
        const tooltipType = this.getAttribute('data-tooltip');
        const tooltipData = kpiTooltipData[tooltipType];
        
        if (tooltipData) {
            kpiTooltipBody.innerHTML = `
                <h3>${tooltipData.title}</h3>
                ${tooltipData.content}
            `;
            kpiTooltipModal.style.display = 'flex';
        }
    });
});

// Close modal handlers
function closeKpiTooltip() {
    kpiTooltipModal.style.display = 'none';
}

kpiTooltipClose.addEventListener('click', closeKpiTooltip);
kpiTooltipOverlay.addEventListener('click', closeKpiTooltip);

// Close on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && kpiTooltipModal.style.display === 'flex') {
        closeKpiTooltip();
    }
});
