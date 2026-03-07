# Screenshot Capture Guide
**Date:** March 6, 2026  
**Duration:** 1 hour  
**Output:** 8 high-quality PNG screenshots

---

## Setup

### 1. Create Screenshots Folder
```bash
cd ~/Projects/CivicGuardian\ AI/article
mkdir -p screenshots
```

### 2. Browser Settings
- **Browser:** Chrome or Safari (latest version)
- **Window Size:** 1920x1080 minimum
- **Zoom:** 100% (except where noted)
- **Dark Mode:** Enabled (System Preferences → Appearance → Dark)
- **Extensions:** Disable ad blockers, screenshot tools

### 3. Screenshot Tool (macOS)
**Option A: Built-in (Recommended)**
- Press: `Cmd + Shift + 4`
- Press: `Space` (to capture window)
- Click window to capture
- File saves to Desktop

**Option B: Full Screen**
- Press: `Cmd + Shift + 3`
- Captures entire screen
- File saves to Desktop

**Option C: Selection**
- Press: `Cmd + Shift + 4`
- Drag to select area
- Release to capture
- File saves to Desktop

### 4. Move Screenshots
After each capture:
```bash
mv ~/Desktop/Screen\ Shot*.png ~/Projects/CivicGuardian\ AI/article/screenshots/screenshot-ui-0X-name.png
```

---

## Screenshot Sequence

### Screenshot 1: Landing Page
**Filename:** `screenshot-ui-01-landing.png`

**Setup:**
1. Open `demo/index.html` in browser
2. Ensure window is 1920x1080
3. Scroll to top of page
4. Wait for animations to settle (2 seconds)

**Capture:**
- Full browser window showing:
  - Demo banner at top
  - Header with KPI cards
  - Upload section (left)
  - Mission panel (right)
  - Footer visible at bottom

**Checklist:**
- [ ] Demo banner visible
- [ ] All 4 KPI cards showing correct values
- [ ] Mission panel fully visible
- [ ] Upload drop zone centered
- [ ] AWS signature in lower-right
- [ ] No scrollbars visible
- [ ] Animations complete

**Save as:** `screenshot-ui-01-landing.png`

---

### Screenshot 2: Document Preview
**Filename:** `screenshot-ui-02-document-preview.png`

**Setup:**
1. Click "Load Sample Case" button
2. Wait for document preview to appear
3. Scroll so preview is centered

**Capture:**
- Document preview section showing:
  - Filename: "sample-letter.txt"
  - File size: "1.2 KB"
  - Letter content (Oxford City Council)
  - "Analyze Document" button

**Checklist:**
- [ ] Preview header visible
- [ ] Full letter text readable
- [ ] "Analyze Document" button prominent
- [ ] Upload section still visible above

**Save as:** `screenshot-ui-02-document-preview.png`

---

### Screenshot 3: Processing Log
**Filename:** `screenshot-ui-03-processing-log.png`

**Setup:**
1. Click "Analyze Document" button
2. Wait ~2 seconds (mid-processing)
3. Capture while log entries are streaming

**Capture:**
- Processing Log section showing:
  - Header: "Processing Log"
  - Status: "PROCESSING" (animated dot)
  - 5-7 log entries visible
  - Timestamps on each entry

**Checklist:**
- [ ] Processing status animated
- [ ] Multiple log entries visible
- [ ] Timestamps showing
- [ ] Dark glassmorphic background
- [ ] Cyan text accents

**Save as:** `screenshot-ui-03-processing-log.png`

---

### Screenshot 4: Risk Assessment Dashboard
**Filename:** `screenshot-ui-04-risk-dashboard.png`

**Setup:**
1. Wait for analysis to complete (~3.5 seconds)
2. Scroll to "Risk Assessment Dashboard" section
3. Ensure all 3 metric cards visible

**Capture:**
- Risk Assessment Dashboard showing:
  - Section header with "Live Analysis" badge
  - Three metric cards:
    - Urgency: HIGH (red bar)
    - Complexity: MEDIUM (amber bar)
    - Confidence: 87% (green bar)
  - Priority banner: "IMMEDIATE" with deadline

**Checklist:**
- [ ] All 3 metric cards visible
- [ ] Progress bars filled correctly
- [ ] Priority banner prominent
- [ ] Deadline countdown showing
- [ ] Gradient effects visible

**Save as:** `screenshot-ui-04-risk-dashboard.png`

---

### Screenshot 5: Draft Response
**Filename:** `screenshot-ui-05-draft-response.png`

**Setup:**
1. Scroll to "AI-Generated Response" section
2. Focus on Draft Response card
3. Ensure full draft text visible

**Capture:**
- Draft Response card showing:
  - Header with edit icon
  - "GENERATED" badge
  - Full draft letter text
  - Rationale bullets (4 items)
  - Legislation Referenced
  - Safety notice
  - "Policy Reasoner Agent" badge

**Checklist:**
- [ ] Full draft text readable
- [ ] Edit icon visible
- [ ] Rationale section expanded
- [ ] Legislation reference showing
- [ ] Safety notice prominent
- [ ] Agent badge at bottom

**Save as:** `screenshot-ui-05-draft-response.png`

---

### Screenshot 6: Validation Status
**Filename:** `screenshot-ui-06-validation.png`

**Setup:**
1. Scroll to Validation Status card
2. Ensure escalation notice fully visible
3. All review triggers showing

**Capture:**
- Validation Status card showing:
  - Header with "APPROVED" badge
  - Status and confidence
  - Validation Checks (5 items)
  - "Human Review Required" section
  - Review Triggers (4 items with icons)
  - "Governor Agent" badge

**Checklist:**
- [ ] All validation checks visible
- [ ] Warning icon on "Human review required"
- [ ] Escalation notice expanded
- [ ] All 4 review triggers showing
- [ ] Icons visible (📅, ⚠️, 📋, 🏛️)
- [ ] Agent badge at bottom

**Save as:** `screenshot-ui-06-validation.png`

---

### Screenshot 7: Full Workflow
**Filename:** `screenshot-ui-07-full-workflow.png`

**Setup:**
1. Zoom out to 67% (Cmd + -)
2. Scroll to show maximum content
3. Capture full page view

**Capture:**
- Full page showing:
  - Header (top)
  - Processing Log
  - Risk Assessment Dashboard
  - All 3 draft cards
  - Action buttons
  - Footer (bottom)

**Checklist:**
- [ ] Multiple sections visible
- [ ] Complete workflow shown
- [ ] Text still readable at 67%
- [ ] Layout balanced

**Save as:** `screenshot-ui-07-full-workflow.png`

---

### Screenshot 8: Mobile View (OPTIONAL)
**Filename:** `screenshot-ui-08-mobile-view.png`

**Setup:**
1. Open Chrome DevTools (Cmd + Option + I)
2. Click device toolbar icon (Cmd + Shift + M)
3. Select "iPhone 14 Pro" or similar
4. Refresh page

**Capture:**
- Mobile layout showing:
  - Stacked sections
  - Responsive mission panel
  - Touch-friendly buttons
  - Readable text

**Checklist:**
- [ ] Layout stacks vertically
- [ ] Text readable on small screen
- [ ] Buttons accessible
- [ ] No horizontal scroll

**Save as:** `screenshot-ui-08-mobile-view.png`

---

## Post-Capture Checklist

### Verify All Screenshots
```bash
cd ~/Projects/CivicGuardian\ AI/article/screenshots
ls -lh
```

**Expected output:**
```
screenshot-ui-01-landing.png          (~500KB - 2MB)
screenshot-ui-02-document-preview.png (~400KB - 1.5MB)
screenshot-ui-03-processing-log.png   (~300KB - 1MB)
screenshot-ui-04-risk-dashboard.png   (~400KB - 1.5MB)
screenshot-ui-05-draft-response.png   (~400KB - 1.5MB)
screenshot-ui-06-validation.png       (~400KB - 1.5MB)
screenshot-ui-07-full-workflow.png    (~600KB - 2.5MB)
screenshot-ui-08-mobile-view.png      (~300KB - 1MB) [OPTIONAL]
```

### Quality Check Each Screenshot
- [ ] Resolution: 1920x1080 or higher
- [ ] Format: PNG (lossless)
- [ ] File size: Reasonable (not corrupted)
- [ ] Content: Correct section captured
- [ ] Clarity: Text readable, no blur
- [ ] Colors: Cyan accents visible, dark theme
- [ ] No artifacts: No compression issues

### Open Each Screenshot
```bash
open screenshot-ui-01-landing.png
open screenshot-ui-02-document-preview.png
open screenshot-ui-03-processing-log.png
open screenshot-ui-04-risk-dashboard.png
open screenshot-ui-05-draft-response.png
open screenshot-ui-06-validation.png
open screenshot-ui-07-full-workflow.png
```

Visual inspection:
- [ ] All screenshots open successfully
- [ ] Content matches expected capture
- [ ] Quality acceptable for article
- [ ] No missing elements

---

## Troubleshooting

### Screenshot Too Small
- Increase browser window size
- Use higher resolution display
- Retake at 100% zoom

### Screenshot Too Large (>5MB)
- Use PNG compression tool:
  ```bash
  brew install pngquant
  pngquant --quality=80-95 screenshot-ui-*.png
  ```

### Wrong Content Captured
- Scroll to correct position
- Wait for animations to complete
- Retake screenshot

### Colors Look Washed Out
- Enable dark mode in System Preferences
- Refresh browser
- Check display color profile

### Text Not Readable
- Increase zoom to 125%
- Use higher resolution display
- Adjust browser window size

---

## Next Steps

After all screenshots captured and verified:

1. **Update Article:**
   - Add screenshot references to `builder-center-article.md`
   - Write descriptive captions
   - Verify paths correct

2. **Proceed to HOUR 4:**
   - Demo video recording
   - Use screenshots as reference for video script

---

**Status:** Ready to capture screenshots  
**Time Required:** 45-60 minutes  
**Next Action:** Open demo/index.html and begin Screenshot 1
