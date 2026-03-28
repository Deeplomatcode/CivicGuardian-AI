// CivicGuardian AI - Demo Interface JavaScript

// ── API config ────────────────────────────────────────────────────────────────
const API_BASE = 'https://2w6h0znfwj.execute-api.eu-west-2.amazonaws.com/prod';
const POLL_INITIAL_DELAY_MS = 5000;   // wait 5s before first poll (ingest takes time)
const POLL_INTERVAL_MS = 5000;        // poll every 5s
const POLL_TIMEOUT_MS = 180000;       // 3 minute total timeout
const TERMINAL_STATUSES = ['RISK_ASSESSED', 'GOVERNOR_VALIDATED', 'AWAITING_APPROVAL', 'APPROVED', 'REJECTED', 'ARCHIVED'];

// Fallback mock data (used only when API call fails)
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

// Real API-backed analysis
async function analyzeDocument() {
    // Determine what we're analysing — real file or sample text
    const previewFilename = document.getElementById('previewFilename').textContent;
    const previewContent = document.getElementById('previewContent').textContent;
    const isSample = (previewFilename === 'sample-letter.txt');

    // Show loading state
    analyzeBtn.disabled = true;
    document.getElementById('analyzeBtnText').textContent = 'Analysing...';
    document.getElementById('analyzeBtnSpinner').style.display = 'inline-block';

    // Show thinking stream
    thinkingStreamSection.style.display = 'block';
    thinkingStreamSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    try {
        let fileToUpload;

        if (isSample) {
            // Wrap sample text as a Blob so we can upload it
            fileToUpload = new File([sampleLetterText], 'sample-letter.txt', { type: 'text/plain' });
        } else {
            // Re-read the actual file from the input
            fileToUpload = fileInput.files[0];
            if (!fileToUpload) {
                // Fallback: wrap preview content as text
                fileToUpload = new File([previewContent], previewFilename, { type: 'text/plain' });
            }
        }

        // ── STEP 1: Get presigned upload URL ─────────────────────────────────
        streamThought('[INIT] Requesting secure upload URL...');
        const presignUrl = `${API_BASE}/presign?filename=${encodeURIComponent(fileToUpload.name)}&type=${encodeURIComponent(fileToUpload.type || 'text/plain')}`;
        const presignResp = await fetch(presignUrl);
        if (!presignResp.ok) throw new Error(`Presign failed: ${presignResp.status}`);
        const { uploadUrl, fileKey } = await presignResp.json();
        streamThought(`[INIT] Upload URL obtained. File key: ${fileKey}`);

        // ── STEP 2: Upload file directly to S3 ───────────────────────────────
        streamThought('[UPLOAD] Uploading document to secure storage...');
        const uploadResp = await fetch(uploadUrl, {
            method: 'PUT',
            headers: { 'Content-Type': fileToUpload.type || 'text/plain' },
            body: fileToUpload,
        });
        if (!uploadResp.ok) throw new Error(`S3 upload failed: ${uploadResp.status}`);
        streamThought('[UPLOAD] Document uploaded successfully.');

        // ── STEP 3: Poll for results ──────────────────────────────────────────
        streamThought('[PROCESS] Starting AI analysis pipeline...');
        const result = await pollForResult(fileKey);

        // ── STEP 4: Display real results ──────────────────────────────────────
        streamThought('[COMPLETE] Analysis complete. Displaying results...');
        displayResults(result);

    } catch (err) {
        console.error('Analysis error:', err);
        streamThought(`[ERROR] ${err.message}`);
        showAnalysisError(err.message);
    } finally {
        analyzeBtn.disabled = false;
        document.getElementById('analyzeBtnText').textContent = 'Analyze Document';
        document.getElementById('analyzeBtnSpinner').style.display = 'none';
    }
}

async function pollForResult(fileKey) {
    // URL-encode the fileKey so the slash in uploads/filename is preserved
    // Use encodeURIComponent which encodes / as %2F — API Gateway will decode it
    // back via pathParameters, and our handler URL-decodes it before the DB lookup
    const encodedKey = encodeURIComponent(fileKey);
    const statusUrl = `${API_BASE}/status/${encodedKey}`;
    const deadline = Date.now() + POLL_TIMEOUT_MS;
    let lastStatus = '';
    let pollCount = 0;

    // Initial delay — give ingest_handler time to write the case to DynamoDB
    streamThought(`[POLL] Waiting for pipeline to initialise (${POLL_INITIAL_DELAY_MS / 1000}s)...`);
    await new Promise(r => setTimeout(r, POLL_INITIAL_DELAY_MS));

    while (Date.now() < deadline) {
        pollCount++;
        console.log(`[poll #${pollCount}] GET ${statusUrl}`);
        streamThought(`[POLL] Checking status for ${fileKey} (attempt ${pollCount})...`);

        let resp;
        try {
            resp = await fetch(statusUrl);
        } catch (networkErr) {
            streamThought(`[POLL] Network error: ${networkErr.message} — retrying...`);
            await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
            continue;
        }

        if (resp.status === 404) {
            streamThought('[POLL] Case not yet in database — waiting...');
            await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
            continue;
        }

        if (!resp.ok) {
            throw new Error(`Status check failed with HTTP ${resp.status}`);
        }

        const data = await resp.json();
        const status = data.status || '';

        console.log(`[poll #${pollCount}] status=${status}`, data);

        if (status !== lastStatus) {
            lastStatus = status;
            if (status === 'INGESTING') {
                streamThought('[INGEST] Document received — extracting text...');
            } else if (status === 'PROCESSING') {
                streamThought('[BEDROCK] Invoking Risk Analyst Agent (Nova Lite)...');
            } else if (status === 'RISK_ASSESSED') {
                streamThought(`[RISK] Risk level: ${data.risk_level || '?'} | Confidence: ${data.governor_confidence ? Math.round(data.governor_confidence * 100) + '%' : '?'}`);
                streamThought('[BEDROCK] Invoking Policy Reasoner Agent (Nova Pro)...');
            } else if (status === 'GOVERNOR_VALIDATED') {
                streamThought('[VALIDATE] Governor validation complete.');
            } else if (status === 'AWAITING_APPROVAL') {
                streamThought('[ESCALATE] Case escalated for caseworker approval.');
            }
        }

        if (TERMINAL_STATUSES.includes(status)) {
            return data;
        }

        await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
    }

    throw new Error('Analysis timed out after 3 minutes. The pipeline may still be running — check DynamoDB directly.');
}

function showAnalysisError(message) {
    // Surface the error in the results panel without touching any UI structure
    visualizationSection.style.display = 'block';
    draftingSuiteSection.style.display = 'grid';

    const errorHtml = `<p style="color:#ff6b6b;padding:1rem;">
        ⚠ Analysis failed: ${message}<br>
        <small>Showing demo data as fallback.</small>
    </p>`;

    const riskPanel = document.getElementById('riskBadge');
    if (riskPanel) riskPanel.closest('section, .card, [class]').insertAdjacentHTML('afterbegin', errorHtml);

    // Fall back to mock data so the UI isn't empty
    displayResults(null);
    visualizationSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
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

function displayResults(apiData) {
    // Show visualization and drafting suite sections
    visualizationSection.style.display = 'block';
    draftingSuiteSection.style.display = 'grid';

    // Merge real API data over mock fallbacks
    const riskData = {
        risk_level:         (apiData && apiData.risk_level)          || mockRiskAnalysis.risk_level,
        confidence:         (apiData && apiData.governor_confidence)  || mockRiskAnalysis.confidence,
        deadline:           (apiData && apiData.deadline)             || mockRiskAnalysis.deadline,
        required_action:    (apiData && apiData.required_action)      || mockRiskAnalysis.required_action,
        urgency_indicators: (apiData && apiData.urgency_indicators && apiData.urgency_indicators.length)
                                ? apiData.urgency_indicators
                                : mockRiskAnalysis.urgency_indicators,
        sender_authority:   (apiData && apiData.sender_authority)     || mockRiskAnalysis.sender_authority,
    };

    const policyData = {
        draft_response:       (apiData && apiData.draft_response)             || mockPolicyResponse.draft_response,
        rationale_bullets:    (apiData && apiData.rationale_bullets && apiData.rationale_bullets.length)
                                  ? apiData.rationale_bullets
                                  : mockPolicyResponse.rationale_bullets,
        legislation_referenced: (apiData && apiData.legislation_referenced && apiData.legislation_referenced.length)
                                  ? apiData.legislation_referenced
                                  : mockPolicyResponse.legislation_referenced,
    };

    const govData = {
        validation_status:  (apiData && apiData.status)              || mockGovernorValidation.validation_status,
        confidence_score:   (apiData && apiData.governor_confidence)  || mockGovernorValidation.confidence_score,
        required_escalation:(apiData && apiData.required_escalation != null)
                                ? apiData.required_escalation
                                : mockGovernorValidation.required_escalation,
    };

    // Update Risk Scorecard
    const urgency = riskData.risk_level === 'HIGH' || riskData.risk_level === 'CRITICAL' ? 85 : 45;
    const complexity = 60;
    const confidence = riskData.confidence * 100;

    const deadline = new Date(riskData.deadline);
    const today = new Date();
    const daysRemaining = Math.ceil((deadline - today) / (1000 * 60 * 60 * 24));

    document.getElementById('urgencyValue').textContent = riskData.risk_level === 'CRITICAL' ? 'CRITICAL' : 'HIGH';
    document.getElementById('urgencyBar').style.width = urgency + '%';
    document.getElementById('urgencyDetail').textContent = `Deadline within ${daysRemaining} days`;

    document.getElementById('complexityValue').textContent = 'MEDIUM';
    document.getElementById('complexityBar').style.width = complexity + '%';
    document.getElementById('complexityDetail').textContent = 'Multi-document review';

    document.getElementById('confidenceValue').textContent = Math.round(confidence) + '%';
    document.getElementById('confidenceBar').style.width = confidence + '%';
    document.getElementById('confidenceDetail').textContent = 'High certainty classification';

    document.getElementById('deadlineCountdown').textContent = `${daysRemaining} days remaining`;

    // Populate Risk Assessment
    document.getElementById('riskBadge').textContent = riskData.risk_level;
    document.getElementById('riskLevel').textContent = riskData.risk_level;
    document.getElementById('riskConfidence').textContent = (riskData.confidence * 100).toFixed(0) + '%';
    document.getElementById('deadline').textContent = formatDate(riskData.deadline);
    document.getElementById('requiredAction').textContent = riskData.required_action;

    const urgencyList = document.getElementById('urgencyIndicators');
    urgencyList.innerHTML = '';
    riskData.urgency_indicators.forEach(indicator => {
        const li = document.createElement('li');
        li.textContent = indicator;
        urgencyList.appendChild(li);
    });

    // Populate Draft Response
    document.getElementById('draftText').textContent = policyData.draft_response;

    const rationaleList = document.getElementById('rationaleList');
    rationaleList.innerHTML = '';
    policyData.rationale_bullets.forEach(bullet => {
        const li = document.createElement('li');
        li.textContent = bullet;
        rationaleList.appendChild(li);
    });

    const legislationList = document.getElementById('legislationList');
    legislationList.innerHTML = '';
    policyData.legislation_referenced.forEach(law => {
        const li = document.createElement('li');
        li.textContent = law;
        legislationList.appendChild(li);
    });

    // Populate Validation
    document.getElementById('validationBadge').textContent = govData.validation_status;
    document.getElementById('validationStatus').textContent = govData.validation_status;
    document.getElementById('validationConfidence').textContent = (govData.confidence_score * 100).toFixed(0) + '%';

    document.getElementById('escalationNotice').style.display =
        govData.required_escalation ? 'block' : 'none';

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
