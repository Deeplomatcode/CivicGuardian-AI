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
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const loadSampleBtn = document.getElementById('loadSampleBtn');
const previewSection = document.getElementById('previewSection');
const resultsSection = document.getElementById('resultsSection');
const analyzeBtn = document.getElementById('analyzeBtn');
const resetBtn = document.getElementById('resetBtn');
const approveBtn = document.getElementById('approveBtn');

// Event Listeners
uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
loadSampleBtn.addEventListener('click', loadSampleLetter);
analyzeBtn.addEventListener('click', analyzeDocument);
resetBtn.addEventListener('click', resetInterface);
approveBtn.addEventListener('click', approveDocument);

// File handling
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.style.borderColor = 'var(--primary-color)';
    uploadArea.style.backgroundColor = '#f1f5f9';
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.style.borderColor = '';
    uploadArea.style.backgroundColor = '';
    
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
    document.getElementById('fileName').textContent = fileName;
    document.getElementById('fileSize').textContent = formatFileSize(fileSize);
    document.getElementById('previewContent').textContent = content;
    
    previewSection.style.display = 'block';
    resultsSection.style.display = 'none';
    
    // Smooth scroll to preview
    previewSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Analysis simulation
function analyzeDocument() {
    // Show loading state
    analyzeBtn.disabled = true;
    document.getElementById('analyzeText').textContent = 'Analysing...';
    document.getElementById('analyzeSpinner').style.display = 'inline-block';
    
    // Simulate processing delay (2 seconds)
    setTimeout(() => {
        displayResults();
        
        // Reset button state
        analyzeBtn.disabled = false;
        document.getElementById('analyzeText').textContent = 'Analyze Document';
        document.getElementById('analyzeSpinner').style.display = 'none';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 2000);
}

function displayResults() {
    // Show results section
    resultsSection.style.display = 'block';
    
    // Populate Risk Assessment
    document.getElementById('riskBadge').textContent = mockRiskAnalysis.risk_level;
    document.getElementById('riskBadge').className = 'badge ' + getRiskBadgeClass(mockRiskAnalysis.risk_level);
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
    
    // Populate Policy Response
    document.getElementById('draftResponse').textContent = mockPolicyResponse.draft_response;
    
    const rationaleList = document.getElementById('rationale');
    rationaleList.innerHTML = '';
    mockPolicyResponse.rationale_bullets.forEach(bullet => {
        const li = document.createElement('li');
        li.textContent = bullet;
        rationaleList.appendChild(li);
    });
    
    const legislationList = document.getElementById('legislation');
    legislationList.innerHTML = '';
    mockPolicyResponse.legislation_referenced.forEach(law => {
        const li = document.createElement('li');
        li.textContent = law;
        legislationList.appendChild(li);
    });
    
    // Populate Governor Validation
    document.getElementById('validationBadge').textContent = mockGovernorValidation.validation_status;
    document.getElementById('validationBadge').className = 'badge ' + getValidationBadgeClass(mockGovernorValidation.validation_status);
    document.getElementById('validationStatus').textContent = mockGovernorValidation.validation_status;
    document.getElementById('validationConfidence').textContent = (mockGovernorValidation.confidence_score * 100).toFixed(0) + '%';
    
    // Show/hide escalation notice
    document.getElementById('escalationNotice').style.display = 
        mockGovernorValidation.required_escalation ? 'block' : 'none';
}

function getRiskBadgeClass(riskLevel) {
    const classes = {
        'LOW': 'badge-success',
        'MEDIUM': 'badge-warning',
        'HIGH': 'badge-danger',
        'CRITICAL': 'badge-danger'
    };
    return classes[riskLevel] || '';
}

function getValidationBadgeClass(status) {
    const classes = {
        'APPROVED': 'badge-success',
        'FLAGGED': 'badge-warning',
        'VETOED': 'badge-danger'
    };
    return classes[status] || '';
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
    previewSection.style.display = 'none';
    resultsSection.style.display = 'none';
    fileInput.value = '';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function approveDocument() {
    alert('✓ Document approved and forwarded to caseworker for review.\n\nIn production, this would:\n• Log approval in DynamoDB\n• Send SNS notification to caseworker\n• Update case status\n• Track deadline in monitoring system');
}

// Add CSS classes dynamically for badge variants
const style = document.createElement('style');
style.textContent = `
    .badge-warning {
        background-color: #fef3c7;
        color: #92400e;
    }
    .badge-danger {
        background-color: #fee2e2;
        color: #991b1b;
    }
`;
document.head.appendChild(style);
