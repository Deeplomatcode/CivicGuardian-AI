# CivicGuardian AI - Caseworker Portal Demo

**Purpose:** Demonstration interface for AWS 10,000 AIdeas competition submission

## Overview

This is a minimal, single-page HTML interface that demonstrates the CivicGuardian AI three-agent workflow:

1. **Risk Analyst** (Amazon Bedrock Nova Lite) - Analyses correspondence urgency
2. **Policy Reasoner** (Amazon Bedrock Nova Pro) - Generates draft responses
3. **Governor** (Pure Python) - Validates AI outputs

## Files

```
demo/
├── index.html          # Main interface
├── style.css           # Styling (minimal, professional)
├── demo.js             # Mock backend simulation
├── sample-letter.txt   # Sample housing benefit letter
└── README.md           # This file
```

## Features

- **Upload Area:** Drag-and-drop or click to upload letters (PDF/TXT/EML)
- **Document Preview:** Shows uploaded letter content
- **Three-Panel Results:**
  - Risk Assessment with urgency indicators
  - Draft Response with rationale and legislation
  - Validation Status with checks and escalation notice
- **Mock Data:** Uses actual sample outputs from the backend agents
- **Loading Simulation:** 2-second delay to simulate processing
- **Professional Design:** Clean, accessible, screenshot-ready

## How to Use

### Local Testing

1. Open `index.html` in a web browser:
   ```bash
   open demo/index.html
   ```

2. Click "Load Sample Letter" to load the demo letter

3. Click "Analyze Document" to see the three-agent workflow

4. Review the results in all three panels

### Taking Screenshots

**For Builder Center Article:**

1. Load sample letter
2. Click analyze and wait for results
3. Take screenshots of:
   - Full interface (overview)
   - Risk Assessment panel (close-up)
   - Draft Response panel (close-up)
   - Validation Status panel (close-up)

**Screenshot Tips:**
- Use browser zoom (Cmd/Ctrl + +/-) to adjust size
- Hide browser chrome for cleaner shots
- Capture at 1920x1080 or higher resolution

### Recording Demo Video

**Suggested Script (2-3 minutes):**

1. **Intro (15s):** "This is CivicGuardian AI, a digital advocate for vulnerable adults"
2. **Upload (20s):** Show drag-and-drop or load sample letter
3. **Preview (15s):** Briefly show the letter content
4. **Analyze (30s):** Click analyze, show loading, wait for results
5. **Risk Panel (30s):** Explain HIGH risk, deadline, urgency indicators
6. **Policy Panel (30s):** Show draft response, rationale, legislation
7. **Governor Panel (30s):** Explain validation checks, escalation notice
8. **Conclusion (20s):** "Three agents working together to prevent crises"

**Recording Tools:**
- macOS: QuickTime Screen Recording
- Windows: Xbox Game Bar (Win + G)
- Cross-platform: OBS Studio (free)

## Technical Notes

### No AWS Services Required

This demo uses **mock data only** - no live AWS services needed:
- No Amazon Bedrock API calls
- No Lambda functions
- No DynamoDB queries
- No S3 uploads

### Mock Data Source

All mock data comes from actual backend outputs:
- `article/sample-output-risk-analyst.json`
- `article/sample-output-policy-reasoner.json`
- `article/sample-output-governor.json`

### Browser Compatibility

Tested on:
- Chrome 120+
- Firefox 120+
- Safari 17+
- Edge 120+

### Accessibility

- Semantic HTML5
- ARIA labels where needed
- Keyboard navigation support
- Colour contrast WCAG AA compliant

## Deployment (Optional)

### Option 1: GitHub Pages

1. Push to GitHub repository
2. Enable GitHub Pages in repository settings
3. Set source to `main` branch, `/demo` folder
4. Access at: `https://username.github.io/CivicGuardian-AI/demo/`

### Option 2: S3 Static Website

1. Create S3 bucket
2. Enable static website hosting
3. Upload demo files
4. Set bucket policy for public read
5. Access via S3 website endpoint

### Option 3: Local Python Server

```bash
cd demo
python3 -m http.server 8000
# Open http://localhost:8000
```

## Competition Use

**For AWS Builder Center Article:**
- Include 3-4 screenshots showing the workflow
- Embed demo video (2-3 minutes)
- Link to live demo (if deployed)

**For Social Media:**
- Share screenshots with captions
- Post demo video on LinkedIn/Twitter
- Highlight the three-agent architecture

## Future Enhancements

**Not needed for competition, but possible:**
- Connect to actual Lambda backend
- Add authentication (API Gateway + IAM)
- Real-time updates via WebSocket
- Case history dashboard
- Multi-document batch processing

## License

Part of CivicGuardian AI - AWS 10,000 AIdeas 2026 submission  
Team Phenix | Mohammed Bakare

---

**Demo Status:** ✅ Ready for screenshots and video recording
