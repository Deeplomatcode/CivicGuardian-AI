# Screenshot Guide - Caseworker Portal Demo

**Purpose:** Capture professional screenshots for AWS Builder Center article

## Quick Start

1. Open the demo:
   ```bash
   open demo/index.html
   ```

2. Follow the steps below for each screenshot

3. Save screenshots to `article/` folder with naming convention:
   - `screenshot-06-ui-overview.png`
   - `screenshot-07-risk-panel.png`
   - `screenshot-08-policy-panel.png`
   - `screenshot-09-governor-panel.png`

## Screenshot 1: UI Overview (Full Interface)

**Steps:**
1. Click "Load Sample Letter"
2. Wait for preview to appear
3. Click "Analyze Document"
4. Wait 2 seconds for results
5. Scroll to show all three panels in view

**What to capture:**
- Full browser window showing complete interface
- All three result panels visible
- Professional, clean layout

**Save as:** `article/screenshot-06-ui-overview.png`

**macOS:** `Cmd + Shift + 4`, then drag to select area  
**Windows:** `Win + Shift + S`, then select area

---

## Screenshot 2: Risk Assessment Panel (Close-up)

**Steps:**
1. After analysis completes, scroll to Risk Assessment panel
2. Ensure panel is centered and fully visible
3. Capture just the Risk Assessment panel

**What to capture:**
- Panel header with "Risk Assessment" and HIGH badge
- All metrics (Risk Level, Confidence, Deadline, Required Action)
- Urgency indicators list
- "Powered by Amazon Bedrock Nova Lite" footer

**Save as:** `article/screenshot-07-risk-panel.png`

**Tip:** Zoom in slightly (Cmd/Ctrl + +) for better detail

---

## Screenshot 3: Draft Response Panel (Close-up)

**Steps:**
1. Scroll to Policy Reasoner panel
2. Ensure full draft response is visible
3. Capture the complete panel

**What to capture:**
- Panel header with "Draft Response" and GENERATED badge
- Full draft letter text
- Rationale bullets
- Legislation referenced
- Safety notice (yellow warning box)
- "Powered by Amazon Bedrock Nova Pro" footer

**Save as:** `article/screenshot-08-policy-panel.png`

**Tip:** This is the most important screenshot - shows AI-generated content

---

## Screenshot 4: Validation Status Panel (Close-up)

**Steps:**
1. Scroll to Governor Validation panel
2. Ensure all validation checks are visible
3. Capture the complete panel

**What to capture:**
- Panel header with "Validation Status" and APPROVED badge
- Validation metrics (Status, Confidence Score)
- All four validation checks with green checkmarks
- Escalation notice (red warning box)
- "Pure Python Validation" footer

**Save as:** `article/screenshot-09-governor-panel.png`

**Tip:** Shows the Governor's safety checks - important for trust

---

## Screenshot 5: Upload Interface (Optional)

**Steps:**
1. Refresh the page to reset
2. Hover over upload area to show hover state
3. Capture the upload section

**What to capture:**
- Upload area with icon and text
- "Load Sample Letter" button
- Clean, inviting interface

**Save as:** `article/screenshot-10-upload.png`

**Use case:** Shows ease of use for non-technical voters

---

## Screenshot Settings

### Resolution
- **Minimum:** 1920x1080 (Full HD)
- **Recommended:** 2560x1440 (2K) or higher
- **Format:** PNG (lossless)

### Browser Settings
- **Zoom:** 100% (or 110% for better readability)
- **Window size:** Maximised or 1600px wide minimum
- **Hide browser chrome:** Press F11 (full screen) for cleaner shots

### Lighting & Clarity
- Use light mode (already default in demo)
- Ensure text is crisp and readable
- No blur or compression artefacts

---

## After Taking Screenshots

### 1. Review Quality
- Check all text is readable
- Verify no personal information visible
- Ensure professional appearance

### 2. Move to Article Folder
```bash
mv ~/Desktop/Screenshot*.png article/
# Or manually drag from Desktop to article/ folder
```

### 3. Rename Files
```bash
cd article/
mv Screenshot-2025-03-05-at-10.30.45.png screenshot-06-ui-overview.png
# Repeat for each screenshot
```

### 4. Commit to Git
```bash
git add article/screenshot-*.png
git commit -m "Add Caseworker Portal UI screenshots for article"
git push origin main
```

---

## Video Recording Guide

### Recording Setup

**Tools:**
- **macOS:** QuickTime Player (File → New Screen Recording)
- **Windows:** Xbox Game Bar (Win + G)
- **Cross-platform:** OBS Studio (free, professional)

**Settings:**
- **Resolution:** 1920x1080 minimum
- **Frame rate:** 30 FPS
- **Audio:** Optional voiceover or silent with captions
- **Length:** 2-3 minutes maximum

### Video Script (2:30 minutes)

**0:00-0:15 - Introduction**
- Show full interface
- "This is CivicGuardian AI, a digital advocate for vulnerable adults"

**0:15-0:35 - Upload**
- Click "Load Sample Letter"
- Show document preview
- "Caseworkers upload correspondence from vulnerable adults"

**0:35-1:05 - Analysis**
- Click "Analyze Document"
- Show loading spinner (2 seconds)
- "Three AI agents analyse the letter in seconds"

**1:05-1:35 - Risk Assessment**
- Scroll to Risk panel
- Highlight HIGH risk badge
- Point out deadline and urgency indicators
- "Nova Lite identifies urgent risks and deadlines"

**1:35-2:05 - Draft Response**
- Scroll to Policy panel
- Show draft letter
- Highlight rationale and legislation
- "Nova Pro generates policy-compliant draft responses"

**2:05-2:25 - Validation**
- Scroll to Governor panel
- Show validation checks
- Highlight escalation notice
- "Pure Python validation ensures safety and accuracy"

**2:25-2:30 - Conclusion**
- Show full interface again
- "Preventing crises before they happen"

### Video Editing

**Optional enhancements:**
- Add text overlays for key points
- Highlight important elements (arrows, circles)
- Add background music (royalty-free)
- Include captions for accessibility

**Export settings:**
- Format: MP4 (H.264)
- Resolution: 1920x1080
- Bitrate: 5-10 Mbps
- File size: <50MB for easy sharing

---

## Using Screenshots in Article

### Builder Center Article

Add screenshots after the "Demo: How It Works" section:

```markdown
## Visual Demo

![Caseworker Portal Overview](screenshot-06-ui-overview.png)
*Figure 7: Caseworker Portal interface showing the complete three-agent workflow*

![Risk Assessment](screenshot-07-risk-panel.png)
*Figure 8: Risk Analyst identifies HIGH risk with 87% confidence and 13-day deadline*

![Draft Response](screenshot-08-policy-panel.png)
*Figure 9: Policy Reasoner generates compliant draft response with UK legislation citations*

![Validation Status](screenshot-09-governor-panel.png)
*Figure 10: Governor validates output and flags for human review (HIGH risk cases)*
```

### Social Media

**LinkedIn Post:**
- Use screenshot-06-ui-overview.png as main image
- Caption: "CivicGuardian AI in action: Three AI agents working together to prevent housing crises for vulnerable adults. Built with Amazon Bedrock Nova. #aideas2025 #socialimpact"

**Twitter/X Post:**
- Use screenshot-07-risk-panel.png or screenshot-08-policy-panel.png
- Caption: "AI that safeguards dignity: CivicGuardian AI analyses urgent correspondence and drafts responses for vulnerable adults. Competing for @awscloud 10,000 AIdeas Finals. 🛡️"

---

## Troubleshooting

### Screenshot is blurry
- Increase browser zoom to 110-125%
- Use higher resolution display
- Save as PNG, not JPG

### Text is too small
- Zoom browser to 125%
- Increase system display scaling
- Use larger monitor or higher DPI

### Colours look washed out
- Check display colour profile
- Use sRGB colour space
- Adjust monitor brightness

### File size too large
- Use PNG compression tool (TinyPNG, ImageOptim)
- Reduce resolution to 1920x1080
- Crop unnecessary whitespace

---

## Checklist

Before submitting article:

- [ ] Screenshot 1: UI Overview (full interface)
- [ ] Screenshot 2: Risk Assessment panel
- [ ] Screenshot 3: Draft Response panel
- [ ] Screenshot 4: Validation Status panel
- [ ] All screenshots in `article/` folder
- [ ] All screenshots committed to Git
- [ ] Screenshots referenced in article
- [ ] Video recorded (optional but recommended)
- [ ] Video uploaded to YouTube/Vimeo (optional)

---

**Ready to capture professional screenshots for your AWS Builder Center article!** 📸
