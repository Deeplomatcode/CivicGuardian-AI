# Browser Test Checklist
**Date:** March 6, 2026  
**Purpose:** Verify demo UI before screenshot capture

---

## How to Test

1. Open Terminal
2. Navigate to demo folder:
   ```bash
   cd ~/Projects/CivicGuardian\ AI/demo
   ```
3. Open in browser:
   ```bash
   open index.html
   ```
4. Complete checklist below

---

## Visual Checks

### Header Section
- [ ] Demo banner shows: "Demo Mode — Synthetic examples only"
- [ ] Brand icon (🛡️) displays
- [ ] Title: "CivicGuardian AI"
- [ ] Subtitle: "Casework Intelligence Platform"
- [ ] Strapline: "AI-assisted correspondence triage with human oversight"
- [ ] KPI Cards show:
  - [ ] "Processing: Serverless"
  - [ ] "Response: Real-time"
  - [ ] "Validation: 3-Agent"
  - [ ] "Oversight: Human-in-Loop"
- [ ] Case reference: "Case #CG-2026-001"
- [ ] Status: "All Systems Operational" (green dot)

### Mission Panel (Right Side)
- [ ] Title: "🛡️ Protecting Vulnerable Adults"
- [ ] "Who We Serve" section lists 4 groups
- [ ] "What We Prevent" section (NO numbers like "12,000+")
- [ ] "How It Works" shows 4 steps
- [ ] "System Capabilities" shows 4 items:
  - [ ] "Instant risk triage"
  - [ ] "Multi-agent validation"
  - [ ] "Serverless cost model"
  - [ ] "UK public sector ready"

### Upload Section (Left Side)
- [ ] Title: "Upload Correspondence"
- [ ] Badge: "Step 1"
- [ ] Drop zone with upload icon
- [ ] Text: "Drop correspondence here"
- [ ] Formats: "PDF • TXT • EML • DOCX"
- [ ] Button: "Load Sample Case"

### Footer
- [ ] Text: "CivicGuardian AI — AWS 10,000 AIdeas 2025 | Team Phenix"
- [ ] GitHub link present
- [ ] Documentation link present

### AWS Signature
- [ ] Lower-right corner shows "Powered by AWS"
- [ ] Orange AWS branding visible
- [ ] Glassmorphic pill styling

---

## Functional Tests

### Test 1: Load Sample Case
1. [ ] Click "Load Sample Case" button
2. [ ] Document preview appears
3. [ ] Filename shows: "sample-letter.txt"
4. [ ] File size shows: "1.2 KB"
5. [ ] Letter content displays (Oxford City Council)
6. [ ] "Analyze Document" button appears

### Test 2: Analyze Document
1. [ ] Click "Analyze Document" button
2. [ ] Button text changes to "Analysing..."
3. [ ] Spinner appears
4. [ ] Processing Log section appears
5. [ ] Log entries stream in sequence:
   - [ ] [INIT] Document ingestion started...
   - [ ] [EXTRACT] Parsing text content...
   - [ ] [DETECT] Identified sender...
   - [ ] [ANALYZE] Extracting deadline...
   - [ ] [BEDROCK] Invoking Risk Analyst Agent...
   - [ ] [RISK] Risk level: HIGH...
   - [ ] [BEDROCK] Invoking Policy Reasoner Agent...
   - [ ] [DRAFT] Generating response...
   - [ ] [VALIDATE] Running Governor validation...
   - [ ] [COMPLETE] Analysis complete...

### Test 3: Risk Assessment Dashboard
After analysis completes:
- [ ] "Risk Assessment Dashboard" section appears
- [ ] Three metric cards display:
  - [ ] Urgency: HIGH (red bar ~85%)
  - [ ] Complexity: MEDIUM (amber bar ~60%)
  - [ ] Confidence: 87% (green bar 87%)
- [ ] Priority banner shows:
  - [ ] Icon: 🔴
  - [ ] "Review Priority: IMMEDIATE"
  - [ ] Deadline countdown (days remaining)

### Test 4: AI-Generated Response
- [ ] "AI-Generated Response" section appears
- [ ] Badge: "Step 3"
- [ ] Three cards display:

**Risk Assessment Card:**
- [ ] Title: "🎯 Risk Assessment"
- [ ] Badge: "HIGH"
- [ ] Risk Level: HIGH
- [ ] Confidence: 87%
- [ ] Deadline: 28 February 2026
- [ ] Required Action: "Submit proof of income"
- [ ] Urgency Indicators list (4 items)
- [ ] Agent badge: "Risk Analyst Agent"

**Draft Response Card:**
- [ ] Title: "📝 Draft Response"
- [ ] Edit icon button visible
- [ ] Badge: "GENERATED"
- [ ] Draft text displays (starts with "Dear Housing Officer")
- [ ] Rationale section (4 bullets)
- [ ] Legislation Referenced: "Housing Benefit Regulations 2006"
- [ ] Safety notice: "⚠️ DRAFT FOR REVIEW — Not legal advice"
- [ ] Agent badge: "Policy Reasoner Agent"

**Validation Card:**
- [ ] Title: "✓ Validation Status"
- [ ] Badge: "APPROVED"
- [ ] Status: APPROVED
- [ ] Confidence: 82%
- [ ] Validation Checks (5 items with checkmarks/warnings)
- [ ] "Human Review Required" section visible
- [ ] Review Triggers list (4 items):
  - [ ] "Deadline within 14 days"
  - [ ] "Benefits suspension risk"
  - [ ] "Citizen action required"
  - [ ] "Council-originated compliance notice"
- [ ] Agent badge: "Governor Agent"

### Test 5: Action Buttons
- [ ] "Analyze Another Document" button visible
- [ ] "Approve & Forward to Caseworker" button visible
- [ ] Click "Approve" shows alert with production workflow

### Test 6: Reset
- [ ] Click "Analyze Another Document"
- [ ] All sections hide except upload
- [ ] Page scrolls to top
- [ ] Ready for new document

---

## Visual Quality Checks

### Design System
- [ ] Dark background (#0A0E1A or similar)
- [ ] Cyan/teal accents (#00F0FF)
- [ ] Animated tech grid background visible
- [ ] Glassmorphism effects (blur, transparency)
- [ ] Glowing badges and status indicators
- [ ] Smooth animations (no jank)
- [ ] Premium cinematic HUD aesthetic

### Typography
- [ ] System fonts loading correctly
- [ ] Text readable (good contrast)
- [ ] Hierarchy clear (headings vs body)
- [ ] No font loading errors

### Responsive Design
- [ ] Layout adapts to window size
- [ ] No horizontal scrolling (at 1920px width)
- [ ] Mission panel stacks on narrow screens
- [ ] All content accessible

---

## Browser Console Checks

### Open Developer Tools
- **Chrome/Safari:** Cmd + Option + I
- **Firefox:** Cmd + Option + K

### Console Tab
- [ ] No JavaScript errors (red text)
- [ ] No missing resource errors (404s)
- [ ] No CORS errors
- [ ] No font loading errors

### Network Tab
- [ ] All resources load successfully
- [ ] No external CDN requests (competition compliance)
- [ ] Only local files loaded

---

## Screenshot Readiness

If all checks pass:
- [ ] UI is screenshot-ready
- [ ] Proceed to screenshot capture (Hour 3)

If any checks fail:
- [ ] Note issues below
- [ ] Fix before proceeding

---

## Issues Found

*List any issues discovered during testing:*

1. 
2. 
3. 

---

## Sign-Off

- [ ] All visual checks passed
- [ ] All functional tests passed
- [ ] No console errors
- [ ] Ready for screenshot capture

**Tested by:** _______________  
**Date:** March 6, 2026  
**Time:** _______________  
**Browser:** _______________  
**Version:** _______________

---

**Next Step:** Proceed to HOUR 3 (Screenshot Capture)
