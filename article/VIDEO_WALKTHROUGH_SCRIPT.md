# CivicGuardian AI - Video Walkthrough Script
## App Demonstration for AWS 10,000 AIdeas 2025

**Duration**: 3-5 minutes  
**Tone**: Conversational, clear, professional  
**Audience**: AWS judges, social good evaluators, technical reviewers

---

## OPENING (0:00 - 0:30)

**[SCREEN: Show demo homepage with header visible]**

**SCRIPT:**
"Hi, I'm presenting CivicGuardian AI - a casework intelligence platform built to help vulnerable adults in the UK who struggle with complex correspondence.

Every year, over 12,000 vulnerable adults lose their housing because they miss critical deadlines in letters they receive. People with dementia, mental health conditions, or learning disabilities often can't navigate these complex documents, and caseworkers are overwhelmed managing 40 or more clients each.

CivicGuardian AI solves this by providing AI-assisted correspondence triage with mandatory human oversight."

---

## SECTION 1: THE DASHBOARD (0:30 - 1:00)

**[SCREEN: Slowly pan across the header showing KPIs]**

**SCRIPT:**
"Let me show you how it works. This is the caseworker dashboard. At the top, you can see real-time metrics - though these are demo values for this presentation.

**[HOVER over each KPI card as you mention it]**

The system tracks cases processed today, average response time under 3 seconds, accuracy rates, and active users. You'll notice the 'Demo Mode' banner at the top - all the data you're seeing is synthetic for demonstration purposes.

**[CLICK on one KPI card to show tooltip]**

Each metric is interactive. For example, clicking on 'Accuracy' explains that our three-agent system - Risk Analyst, Policy Reasoner, and Governor - work together to validate every analysis."

---

## SECTION 2: THE PROBLEM & MISSION (1:00 - 1:45)

**[SCREEN: Scroll down to show Mission & Impact panel on the right]**

**SCRIPT:**
"On the right, you can see our mission statement. This isn't just about technology - it's about preventing real harm.

**[POINT to the problem statement]**

We're targeting four vulnerable groups: people with early-stage dementia, mental health conditions, learning disabilities, and elderly isolated adults.

**[SCROLL through the 'What We Prevent' section]**

The stakes are high. We're preventing housing evictions from missed deadlines, benefit suspensions from delayed responses, and care disruptions from administrative gaps.

**[POINT to the 4-step pipeline]**

Our system uses a four-step process: First, a Risk Analyst powered by Amazon Nova Lite identifies urgency. Second, a Policy Reasoner using Nova Pro drafts responses. Third, a Governor validates everything. And fourth - critically - a human caseworker must approve before anything is sent."

---

## SECTION 3: UPLOADING A DOCUMENT (1:45 - 2:15)

**[SCREEN: Focus on the Upload Correspondence section]**

**SCRIPT:**
"Let's walk through an actual case. On the left, caseworkers can upload correspondence in multiple formats - PDF, text files, emails, or Word documents.

**[CLICK 'Load Sample Case' button]**

I'll load a sample case. This is a housing benefit review letter - a common type of correspondence that vulnerable adults receive.

**[SCREEN: Document preview appears]**

The system immediately shows a preview. You can see the filename, file size, and the full content of the letter. This particular letter is from a local council requesting proof of income within 14 days.

**[HOVER over 'Analyze Document' button]**

Now, let's analyze it."

---

## SECTION 4: AI PROCESSING (2:15 - 2:45)

**[SCREEN: CLICK 'Analyze Document' - show processing log appearing]**

**SCRIPT:**
"When I click 'Analyze Document,' you'll see our three-agent system spring into action.

**[SCREEN: Processing log shows agent activity]**

The Processing Log shows each agent working in real-time. The Risk Analyst is extracting key information - deadlines, required actions, and urgency levels. The Policy Reasoner is drafting a response based on UK legislation. And the Governor is validating that everything is accurate and safe.

**[SCREEN: Risk Assessment Dashboard appears]**

The Risk Assessment Dashboard gives caseworkers instant visibility. This case is marked as HIGH urgency because there's a deadline within 13 days. The complexity is MEDIUM - it's a straightforward document request. And the system has 87% confidence in its classification."

---

## SECTION 5: THE AI-GENERATED RESPONSE (2:45 - 3:30)

**[SCREEN: Scroll to show the three-card layout]**

**SCRIPT:**
"Now here's where it gets powerful. The system generates three outputs:

**[POINT to Risk Assessment card]**

First, the Risk Assessment from our Risk Analyst. It identifies this as a HIGH risk case with an 87% confidence level. The deadline is February 28th, and the required action is to submit proof of income. It lists all the urgency indicators it found.

**[POINT to Draft Response card]**

Second, the Draft Response from our Policy Reasoner. This is a complete letter ready for the caseworker to review. It explains the situation in plain English, references the relevant UK legislation - like the Housing Benefit Regulations 2006 - and provides clear next steps.

Notice the warning at the bottom: 'DRAFT FOR REVIEW - Not legal advice.' This is crucial. We're not replacing caseworkers; we're giving them a head start.

**[POINT to Validation card]**

Third, the Validation Status from our Governor agent. It runs multiple checks: Are the citations valid? Are there any unsupported claims? Is the safety notice present? 

**[POINT to the escalation notice]**

And here's the key safeguard: 'Human Review Required.' Because this is a HIGH risk case with a tight deadline and benefits at stake, it MUST be reviewed by a caseworker before being sent."

---

## SECTION 6: HUMAN OVERSIGHT & COMPLIANCE (3:30 - 4:00)

**[SCREEN: Scroll back to Mission panel, show compliance section]**

**SCRIPT:**
"This brings me to our core principle: 100% human oversight is required. Every single output must be approved by a qualified caseworker.

**[POINT to compliance checkmarks]**

We're built for the public sector. We're GDPR compliant under Articles 6 and 9. We align with the Care Act 2014 Section 42. And we follow the UK Data Protection Act 2018.

**[SCREEN: Show the two action buttons at bottom]**

The caseworker has two options: They can analyze another document, or they can approve this response and forward it to the client. But that approval step is mandatory - the system won't send anything without it."

---

## SECTION 7: THE IMPACT (4:00 - 4:30)

**[SCREEN: Scroll to show the target metrics]**

**SCRIPT:**
"So what's the impact? Our targets are ambitious but achievable.

**[POINT to each metric]**

We're aiming for less than 5% missed deadline rate - down from the current crisis levels. We want 80% or higher caseworker approval, meaning our drafts are genuinely helpful. And we're cost-effective, running on AWS serverless infrastructure.

**[SCREEN: Show AWS logo at bottom right]**

Everything runs on AWS - Amazon Bedrock for the AI agents, Lambda for serverless processing, and S3 for secure document storage. This keeps costs low while maintaining enterprise-grade security."

---

## CLOSING (4:30 - 5:00)

**[SCREEN: Zoom out to show full dashboard]**

**SCRIPT:**
"CivicGuardian AI isn't about replacing human judgment. It's about giving caseworkers superpowers - helping them work faster, catch critical deadlines, and serve more vulnerable adults effectively.

**[SCREEN: Show GitHub link in footer]**

The code is open source on GitHub. The architecture is documented. And we've built this with real-world constraints in mind - GDPR compliance, data protection, and the absolute requirement for human oversight.

**[SCREEN: Fade to AWS 10,000 AIdeas logo or project title card]**

Thank you for watching. CivicGuardian AI - protecting vulnerable adults through AI-assisted casework intelligence."

---

## RECORDING NOTES

### Technical Setup
- **Resolution**: 1920x1080 minimum
- **Frame rate**: 30fps or 60fps
- **Audio**: Clear microphone, minimal background noise
- **Screen recording**: Use OBS Studio, Loom, or similar

### Camera Angles
- **Wide shot**: Show full dashboard for context
- **Close-ups**: Zoom to 150% when showing specific UI elements
- **Smooth transitions**: Use slow pans, avoid jerky movements

### Timing Tips
- **Pause briefly** after each major point (1-2 seconds)
- **Slow down** when showing complex information
- **Speed up** during transitions between sections
- **Total runtime**: Aim for 4:00-4:30, maximum 5:00

### Interactive Elements to Demonstrate
1. ✅ Click KPI card to show tooltip
2. ✅ Click "Load Sample Case" button
3. ✅ Show document preview appearing
4. ✅ Click "Analyze Document" button
5. ✅ Show processing log animation
6. ✅ Show risk dashboard appearing
7. ✅ Scroll through all three output cards
8. ✅ Hover over action buttons

### Emphasis Points (Speak Slower)
- "12,000 vulnerable adults lose housing each year"
- "100% human oversight required"
- "DRAFT FOR REVIEW - Not legal advice"
- "Human Review Required"
- "GDPR compliant"

### Visual Highlights (Use Cursor/Pointer)
- Circle or highlight key numbers (12,000, 40+ clients)
- Point to the 4-step agent pipeline
- Underline "Human Review Required" text
- Highlight compliance checkmarks

---

## POST-PRODUCTION CHECKLIST

- [ ] Add subtle background music (low volume, non-distracting)
- [ ] Add text overlays for key statistics
- [ ] Add zoom effects for important UI elements
- [ ] Add transition effects between sections
- [ ] Color grade for consistency
- [ ] Normalize audio levels
- [ ] Add captions/subtitles (accessibility)
- [ ] Export in multiple formats (MP4, WebM)
- [ ] Test playback on different devices

---

## ALTERNATIVE SHORTER VERSION (2-3 minutes)

If you need a condensed version, focus on:
1. **Problem statement** (30 seconds)
2. **Upload & analyze demo** (60 seconds)
3. **Three-agent output** (60 seconds)
4. **Human oversight emphasis** (30 seconds)

Skip the detailed KPI explanation and compliance deep-dive.

---

## SCRIPT VARIATIONS

### For Technical Audience
- Add more detail on AWS services (Bedrock, Lambda, S3)
- Mention the three Amazon Nova models specifically
- Explain the serverless architecture benefits

### For Social Good Audience
- Lead with the human impact story
- Spend more time on the vulnerable populations
- Emphasize the 12,000 housing loss statistic

### For Business Audience
- Focus on cost-effectiveness
- Highlight caseworker productivity gains
- Emphasize scalability and ROI

---

**END OF SCRIPT**
