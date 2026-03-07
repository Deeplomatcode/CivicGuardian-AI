# CivicGuardian AI - Complete Video Walkthrough Script

**TOTAL DURATION:** 4 minutes 30 seconds  
**TARGET AUDIENCE:** AWS judges, community voters, potential users  
**TONE:** Professional but accessible, storytelling approach

---

## [0:00-0:30] OPENING: THE PROBLEM WE'RE SOLVING

**SCREEN ACTION:**
1. Show full homepage with header visible
2. Camera slowly pans to mission panel on right side
3. Pause on "12,000+ vulnerable adults" statistic
4. Highlight the four target group tags

**NARRATION:**
"In the UK, over twelve thousand vulnerable adults lose their homes every year. Not because they can't pay rent. But because they miss critical deadlines in correspondence they receive.

Margaret is seventy-two. She has early-stage dementia. Every month, she gets letters from her local council, the housing office, the NHS, and benefits agencies.

The letters are dense, confusing, and full of deadlines. When she misses just one deadline, it can trigger an eviction process.

Caseworkers want to help. But they're overwhelmed. Each one manages over forty clients.

CivicGuardian AI was built to prevent these crises."

**UI ELEMENTS TO POINT OUT:**
✓ "12,000+ vulnerable adults lose housing each year" statistic
✓ Four target group tags (dementia, mental health, learning disabilities, elderly)
✓ "40+ clients each" caseworker burden
✓ Demo Mode banner (explain synthetic data)

**WHY THIS SECTION MATTERS:**
Sets up the human impact story. Makes the problem real and urgent. Establishes emotional connection before showing technology.

---

## [0:30-1:15] SECTION 1: THE DASHBOARD & UPLOAD

**SCREEN ACTION:**
1. Pan across header showing KPI metrics
2. Hover over "Accuracy" KPI card (shows info icon)
3. Click to show tooltip explaining three-agent system
4. Close tooltip
5. Scroll down to Upload Correspondence section
6. Hover mouse over upload zone (shows cyan glow effect)
7. Point to supported formats text

**NARRATION:**
"This is the caseworker dashboard. Let me show you the key metrics.

Cases processed today. Average response time under three seconds. Accuracy at ninety-four percent. Active users across the system.

Click any metric to learn more. For example, 'Accuracy' shows how our three AI assistants work together. One analyzes risk. One drafts responses. One validates everything.

Here's how it works. When Margaret receives a letter about her housing benefit, her caseworker uploads it here. The system accepts PDFs, scanned images, emails, even Word documents.

Notice we're in Demo Mode. All the data you're seeing is synthetic for this presentation.

Let me show you what happens when we upload a real housing benefit review letter."

**UI ELEMENTS TO POINT OUT:**
✓ Cases Today: 247 (Demo)
✓ Avg Response: <3s (Demo)
✓ Accuracy: 94.2% (Demo)
✓ Active Users: 1,500+ (Demo)
✓ System status indicator (green dot, "All Systems Operational")
✓ Case reference number (CG-2026-001)
✓ Upload drop zone with animated cyan border on hover
✓ Supported formats list (PDF, TXT, EML, DOCX)
✓ "Load Sample Case" button

**WHY THIS SECTION MATTERS:**
Shows the system is operational and user-friendly. Establishes trust with real-time metrics. Demonstrates the upload process is simple and supports multiple formats.

---

## [1:15-2:45] SECTION 2: THE THREE-AGENT PROCESSING SYSTEM

**SCREEN ACTION:**
1. Click "Load Sample Case" button
2. Document preview appears (wait for animation)
3. Show preview content briefly
4. Click "Analyze Document" button
5. Processing Log section appears on left
6. Watch agent messages stream in real-time
7. Risk Assessment Dashboard appears on right
8. Point to each risk metric as it populates

**NARRATION:**
"I'll load a sample case. This is a housing benefit review letter from a local council. They're requesting proof of income within fourteen days.

The system shows a preview. Filename, file size, full content. Everything is visible before analysis.

Now I'll click 'Analyze Document.' Watch what happens.

The system uses three specialized AI assistants, all running on Amazon Bedrock, AWS's AI service.

[Point to Processing Log]
First, the Risk Analyst, powered by Nova Lite, scans the letter in seconds. It's looking for urgency signals. Keywords like 'within fourteen days' or 'mandatory review.' It extracts the deadline, identifies required actions, calculates urgency.

[Point to Processing Log]
Second, the Policy Reasoner, powered by Nova Pro, takes over. This is the more thorough AI model. It cross-references the letter against UK Housing Benefit Regulations. It generates a draft response that's compliant with the law. It explains its reasoning.

[Point to Processing Log]
Third, the Governor validates everything. It's checking: Are all the claims in the draft actually supported by the original letter? Is there a disclaimer saying this requires human review? Is the tone professional and respectful?

[Point to Risk Assessment Dashboard]
The Risk Assessment Dashboard appears. This case is HIGH urgency. Why? Deadline within thirteen days. Complexity is MEDIUM. It's a straightforward document request. Confidence is eighty-seven percent. The system is very certain about this classification.

All of this happens in under two minutes."

**UI ELEMENTS TO POINT OUT:**
✓ Document preview box with filename (sample-letter.txt) and size (1.2 KB)
✓ Preview content showing letter text
✓ "Analyze Document" button (changes to "Analysing..." with spinner)
✓ Processing Log section appearing
✓ Agent messages streaming (Risk Analyst → Policy Reasoner → Governor)
✓ Agent pipeline visualization in Mission panel (four numbered steps)
✓ Risk Assessment Dashboard with three cards:
  - Urgency: HIGH (85% red bar, "Deadline within 13 days")
  - Complexity: MEDIUM (60% yellow bar, "Multi-document review")
  - Confidence: 87% (87% green bar, "High certainty classification")
✓ Priority banner: IMMEDIATE with red icon
✓ Deadline countdown: "13 days remaining"

**WHY THIS SECTION MATTERS:**
Shows the AI working transparently. Demonstrates the multi-agent architecture that makes this system credible. Proves the system is fast and thorough. Shows explainability in real-time.

---

## [2:45-3:30] SECTION 3: THE RESULTS - RISK ASSESSMENT

**SCREEN ACTION:**
1. Scroll down to AI-Generated Response section
2. Focus on Risk Assessment card (left)
3. Highlight risk level badge (HIGH in red)
4. Point to each info row (Risk Level, Confidence, Deadline, Required Action)
5. Scroll through Urgency Indicators list
6. Point to "Risk Analyst Agent" badge at bottom

**NARRATION:**
"Now let's look at what the system found.

The Risk Analyst has flagged this as HIGH risk. That means it needs immediate attention.

Confidence: eighty-seven percent. The system is very certain about this classification.

Deadline: February twenty-eighth, twenty twenty-six. That's thirteen days away.

Required Action: Submit proof of income. Clear and specific.

It identified four urgency indicators. Deadline within fourteen days. Benefits suspension risk. Citizen action required. Council-originated compliance notice.

Notice the agent badge at the bottom. This assessment came from the Risk Analyst, powered by Amazon Nova Lite. Fast analysis for urgent triage."

**UI ELEMENTS TO POINT OUT:**
✓ Risk Assessment card with cyan border
✓ Risk Level badge: HIGH (red background)
✓ Confidence: 87%
✓ Deadline: 28 February 2026
✓ Required Action: Submit proof of income
✓ Urgency Indicators list (4 items with icons):
  - 📅 Deadline within 14 days
  - ⚠️ Benefits suspension risk
  - 📋 Citizen action required
  - 🏛️ Council-originated compliance notice
✓ "Risk Analyst Agent" badge with lightning icon

**WHY THIS SECTION MATTERS:**
Shows explainability and transparency. Demonstrates the system identifies specific, actionable information. Builds credibility by showing confidence levels and reasoning.

---

## [3:30-4:00] SECTION 4: THE DRAFT RESPONSE

**SCREEN ACTION:**
1. Scroll to Draft Response card (center)
2. Highlight the "GENERATED" status badge
3. Show draft text content (scroll through briefly)
4. Point to Rationale section
5. Point to Legislation Referenced section
6. Highlight the orange "DRAFT FOR REVIEW" warning box
7. Point to "Policy Reasoner Agent" badge

**NARRATION:**
"Here's the draft response the Policy Reasoner generated.

At the top, there's a status badge: 'GENERATED.' This draft is ready for caseworker review.

The draft acknowledges the deadline, confirms Margaret is engaging with the process, and requests the specific documents the housing office needs. It's written in plain English, respectful and professional.

Below the draft, the system shows its reasoning. Why did it include these paragraphs? It lists each rationale point.

It references specific UK legislation. Housing Benefit Regulations two thousand and six. Care Act twenty fourteen. This transparency lets the caseworker verify the AI's logic.

And here's the critical warning: 'DRAFT FOR REVIEW - Not legal advice.' This is prominent, impossible to miss.

The caseworker must review, edit if needed, and approve before anything is sent. The AI assists. It doesn't decide."

**UI ELEMENTS TO POINT OUT:**
✓ Draft Response card with cyan border
✓ "GENERATED" status badge (green)
✓ Edit icon button (pencil icon, top right)
✓ Draft text content (formatted letter)
✓ Rationale section with checkmark bullets (3-4 items)
✓ Legislation Referenced section with section symbol bullets (2-3 items)
✓ "⚠️ DRAFT FOR REVIEW - Not legal advice" warning (orange background)
✓ "Policy Reasoner Agent" badge with lightning icon

**WHY THIS SECTION MATTERS:**
Shows human-in-the-loop design. Makes clear the AI assists, doesn't decide. Demonstrates transparency in reasoning. Emphasizes the safety warning.

---

## [4:00-4:15] SECTION 5: SAFETY VALIDATION

**SCREEN ACTION:**
1. Scroll to Validation Status card (right)
2. Highlight "APPROVED" badge (green)
3. Point to Status and Confidence rows
4. Scroll through Validation Checks list (5 items with checkmarks)
5. Highlight the "Human Review Required" escalation notice (orange box)
6. Point to Review Triggers list (4 items)
7. Point to "Governor Agent" badge

**NARRATION:**
"Finally, the Governor validates everything.

Status: APPROVED. The draft passed all automated checks. Confidence: eighty-two percent.

It ran five validation checks. Citations valid. No unsupported claims found. Human review required. Safety notice present. No definitive claims.

But here's the key safeguard. 'Human Review Required.' Because this is HIGH risk with a tight deadline and benefits at stake, a caseworker MUST review before sending.

The system lists four review triggers. Deadline within fourteen days. Benefits suspension risk. Citizen action required. Council-originated compliance notice.

The caseworker is always in control. Every decision requires a real person to approve."

**UI ELEMENTS TO POINT OUT:**
✓ Validation Status card with cyan border
✓ "APPROVED" badge (green background)
✓ Status: APPROVED
✓ Confidence: 82%
✓ Validation Checks list (5 items):
  - ✓ Citations valid
  - ✓ No unsupported claims found
  - ⚠ Human review required (yellow warning)
  - ✓ Safety notice present
  - ✓ No definitive claims
✓ "⚠️ Human Review Required" escalation notice (orange box)
✓ "HIGH risk case — caseworker approval needed" reason
✓ Review Triggers list (4 items with icons)
✓ "Governor Agent" badge with circle icon

**WHY THIS SECTION MATTERS:**
Shows the safety guardrails. Demonstrates responsible AI design. Emphasizes mandatory human oversight. Builds trust through transparency.

---

## [4:15-4:30] CLOSING: IMPACT AND TECHNOLOGY

**SCREEN ACTION:**
1. Scroll to action buttons at bottom
2. Hover over "Approve & Forward to Caseworker" button (green, prominent)
3. Scroll back up to Mission panel on right
4. Show target metrics (three cards: <5%, 80%+, Cost-Effective)
5. Show compliance checkmarks (GDPR, Care Act, Data Protection)
6. Zoom out to show full dashboard
7. End on AWS logo at bottom right

**NARRATION:**
"The caseworker has two options. Analyze another document. Or approve this response and forward it.

But that approval step is mandatory. The system won't send anything without it. One hundred percent human oversight required.

So what's the impact? Our targets are ambitious.

Less than five percent missed deadline rate. That's down from crisis levels.

Eighty percent caseworker approval or higher. Our drafts are genuinely helpful.

Cost-effective per case. Running on AWS serverless infrastructure.

We're built for the public sector. GDPR compliant under Articles six and nine. Aligned with the Care Act twenty fourteen Section forty-two. Following UK Data Protection Act twenty eighteen.

Everything runs on AWS. Amazon Bedrock for the AI. Lambda for serverless processing. S3 for secure storage. Enterprise-grade security at low cost.

CivicGuardian AI. Protecting vulnerable adults through AI-assisted casework intelligence. With mandatory human oversight.

Built for the AWS ten thousand AIdeas twenty twenty-five competition, Social Good category, by Team Phenix.

Thank you."

**UI ELEMENTS TO POINT OUT:**
✓ "Analyze Another Document" button (secondary, gray)
✓ "Approve & Forward to Caseworker" button (primary, green, prominent)
✓ Target metrics in Mission panel (three cards):
  - <5% Missed Deadline Rate (Goal)
  - 80%+ Caseworker Approval Target
  - Cost-Effective Per Case (AWS)
✓ Compliance checkmarks (4 items):
  - ✓ 100% human oversight required
  - ✓ GDPR Articles 6 & 9 compliant
  - ✓ Care Act 2014 Section 42 aligned
  - ✓ UK Data Protection Act 2018
✓ Four-step pipeline visualization (Risk Analyst → Policy Reasoner → Governor → Human Approval)
✓ AWS logo at bottom right ("Powered by AWS")
✓ GitHub link in footer

**WHY THIS SECTION MATTERS:**
Ties technical solution to social impact. Shows AWS tech stack. Reinforces competition positioning. Emphasizes human oversight one final time. Ends with clear call to action.

---

## ADDITIONAL NOTES FOR VIDEO RECORDING

### PACING
- Speak slowly and clearly (120-140 words per minute)
- Pause for 1-2 seconds between major sections
- Let animations complete before moving on
- Slow down when mentioning statistics (12,000, 87%, etc.)
- Pause after "Human Review Required" for emphasis

### MOUSE MOVEMENTS
- Point to specific UI elements as you mention them
- Use smooth, deliberate movements (not jerky)
- Circle or highlight key elements briefly
- Hover to show interactive effects (cyan glow, tooltips)
- Don't move the mouse while speaking important points

### SCREEN TRANSITIONS
- Scroll smoothly (not too fast, not too slow)
- Pause on each section for 2-3 seconds before speaking
- End with the full page in view
- Use zoom effects in post-production for small text

### EMPHASIS POINTS (Speak Slower)
- "twelve thousand vulnerable adults" ← PAUSE
- "over forty clients each" ← PAUSE
- "one hundred percent human oversight required" ← SLOW + PAUSE
- "DRAFT FOR REVIEW - Not legal advice" ← SLOW
- "Human Review Required" ← SLOW + PAUSE
- "caseworker MUST review" ← EMPHASIS
- "The caseworker is always in control" ← SLOW

### BACKUP TIMINGS

**If you need to shorten to 3 minutes:**
- Cut Section 1 (dashboard) to 20 seconds (skip KPI tooltip demo)
- Combine Sections 3 and 4 (risk + draft) into one 45-second section
- Skip detailed validation checks, just show "Human Review Required"

**If you need to extend to 5 minutes:**
- Add a "Technical Architecture" section (30 seconds on AWS services)
- Expand the problem statement with more about Margaret (30 seconds)
- Add a "Cost Breakdown" section (30 seconds on AWS Free Tier usage)

---

## ELEVATOR PITCH VERSION (30 SECONDS)

If you need a super-short version for social media:

"CivicGuardian AI helps vulnerable adults avoid eviction by ensuring they never miss critical correspondence deadlines. Three AI assistants analyze letters, flag urgent risks, and draft compliant responses in under two minutes. Human caseworkers review and approve everything. Built on Amazon Bedrock. Cost-effective per case. Fully GDPR compliant. Protecting twelve thousand vulnerable adults annually from preventable housing crises. Built for AWS ten thousand AIdeas twenty twenty-five."

---

## COMMON MISTAKES TO AVOID

### Don't:
- ❌ Rush through the demo (take your time)
- ❌ Use jargon without explanation ("multi-agent system" → "three AI assistants")
- ❌ Skip the "human oversight" emphasis (mention it 3-4 times)
- ❌ Forget to mention it's demo data (say it early and clearly)
- ❌ Talk over animations (let them play, then speak)
- ❌ Use filler words (um, uh, like, you know)
- ❌ Apologize or sound uncertain
- ❌ Read from a script (sound conversational)

### Do:
- ✅ Speak clearly and confidently
- ✅ Pause after important points
- ✅ Emphasize human oversight repeatedly
- ✅ Show genuine enthusiasm for the social impact
- ✅ Use concrete examples (Margaret, housing letters)
- ✅ Maintain consistent energy throughout
- ✅ Sound like you're explaining to a friend
- ✅ Practice 3-5 times before recording

---

## FINAL CHECKLIST BEFORE RECORDING

- [ ] Demo is loaded and working in browser
- [ ] Screen recorder is set up and tested (OBS Studio, Loom, etc.)
- [ ] Microphone is working and positioned correctly
- [ ] Room is quiet (no background noise, notifications off)
- [ ] Script is printed or on second monitor
- [ ] Water is nearby (for dry mouth)
- [ ] Phone is on silent
- [ ] Browser is in full-screen mode (F11)
- [ ] Demo Mode banner is visible
- [ ] You've practiced the full script 2-3 times
- [ ] You're ready to record!

---

**Good luck with your recording! 🎬**

**Remember:** This is about helping vulnerable people. Let that passion come through in your voice. You're not just demonstrating software - you're showing how technology can prevent real human suffering.

**END OF SCRIPT**
