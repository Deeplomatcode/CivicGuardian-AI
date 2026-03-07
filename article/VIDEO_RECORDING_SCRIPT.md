# Demo Video Recording Script
**Date:** March 6, 2026  
**Duration:** 3-5 minutes  
**Target:** AWS 10,000 AIdeas 2025 submission

---

## Pre-Recording Setup

### 1. Recording Software
**Option A: QuickTime Player (macOS Built-in)**
```
1. Open QuickTime Player
2. File → New Screen Recording
3. Click Options:
   - Microphone: Built-in Microphone (or external)
   - Quality: Maximum
4. Click red record button
5. Click anywhere to start recording
```

**Option B: OBS Studio (Free, More Features)**
```
1. Download: https://obsproject.com/
2. Install and open OBS
3. Add Source → Display Capture
4. Settings:
   - Video: 1920x1080, 30fps
   - Audio: 44.1kHz, stereo
5. Click "Start Recording"
```

### 2. Environment Setup
- [ ] Quiet room (no background noise)
- [ ] Close unnecessary apps
- [ ] Disable notifications (Do Not Disturb)
- [ ] Clear desktop (minimize distractions)
- [ ] Test microphone (record 10 seconds, playback)
- [ ] Browser window: 1920x1080
- [ ] Demo page loaded: `demo/index.html`
- [ ] Script printed or on second monitor

### 3. Voice Preparation
- [ ] Drink water (avoid dry mouth)
- [ ] Practice script 2-3 times
- [ ] Speak clearly and slowly
- [ ] Smile while speaking (improves tone)
- [ ] Pause between sections

---

## Video Script (3-5 minutes)

### [0:00-0:30] INTRODUCTION (30 seconds)

**[Show: Landing page, full view]**

> "Hi, I'm [Your Name] from Team Phenix, and this is CivicGuardian AI—a digital safety net for vulnerable adults built for the AWS 10,000 AIdeas 2025 competition."

**[Pause 2 seconds]**

> "Let me show you how it works."

**ACTION:** Scroll slowly down to show header and mission panel

---

### [0:30-1:15] THE PROBLEM (45 seconds)

**[Show: Mission panel - "Who We Serve" section]**

> "In the UK, over 12,000 vulnerable adults lose housing each year—not because help isn't available, but because critical deadlines are buried in complex correspondence."

**[Pause 2 seconds]**

**[Show: Mission panel - "What We Prevent" section]**

> "Margaret is 72 with early-stage dementia. Last month, she received 15 letters from her council, housing association, and NHS trust. A critical deadline in paragraph four triggered an eviction warning."

**[Pause 2 seconds]**

> "CivicGuardian AI ensures no letter goes unread, and no deadline is missed."

**ACTION:** Scroll back to upload section

---

### [1:15-2:00] THE SOLUTION - UPLOAD (45 seconds)

**[Show: Upload section]**

> "The workflow is simple. A caseworker or family member uploads correspondence—PDF, email, or scanned letter."

**[Pause 1 second]**

**ACTION:** Click "Load Sample Case" button

**[Show: Document preview appears]**

> "Here's a real example: a housing benefit review from Oxford City Council with a 13-day deadline."

**[Pause 2 seconds, let viewer read first few lines]**

> "Let's analyze it."

**ACTION:** Click "Analyze Document" button

---

### [2:00-2:45] THE TECHNOLOGY - PROCESSING (45 seconds)

**[Show: Processing log streaming]**

> "Watch the three-agent system work in real-time."

**[Pause 2 seconds, let log stream]**

> "First, the Risk Analyst Agent—powered by Amazon Bedrock Nova Lite—classifies urgency and extracts deadlines."

**[Pause 2 seconds]**

> "Then, the Policy Reasoner Agent—using Nova Pro—drafts a compliant response based on UK housing law."

**[Pause 2 seconds]**

> "Finally, the Governor Agent validates for accuracy and safety using pure Python—no AI hallucinations allowed."

**[Pause 2 seconds, wait for "COMPLETE" message]**

**ACTION:** Scroll down to Risk Assessment Dashboard

---

### [2:45-3:30] THE RESULTS - RISK DASHBOARD (45 seconds)

**[Show: Risk Assessment Dashboard with 3 metric cards]**

> "The system detected HIGH urgency—a 13-day deadline with benefit suspension risk."

**[Pause 2 seconds]**

**[Show: Priority banner]**

> "Review priority: IMMEDIATE."

**ACTION:** Scroll down to Draft Response card

**[Show: Draft Response]**

> "Here's the AI-generated draft response—acknowledging the deadline, confirming engagement, and requesting receipt confirmation."

**[Pause 2 seconds]**

**[Show: Legislation Referenced]**

> "It references the Housing Benefit Regulations 2006, and includes a safety notice: 'Draft for review—not legal advice.'"

**ACTION:** Scroll down to Validation card

---

### [3:30-4:15] THE GOVERNANCE - VALIDATION (45 seconds)

**[Show: Validation Status card]**

> "The Governor Agent approved the draft with 82% confidence."

**[Pause 2 seconds]**

**[Show: Validation Checks]**

> "All citations are valid, no unsupported claims found, and the safety notice is present."

**[Pause 2 seconds]**

**[Show: Human Review Required section]**

> "But here's the critical part: because this is a HIGH risk case, human review is required."

**[Pause 2 seconds]**

**[Show: Review Triggers]**

> "The system explains exactly why: deadline within 14 days, benefits suspension risk, citizen action required, and council-originated compliance notice."

**[Pause 2 seconds]**

> "This isn't automation replacing humans—it's AI assisting caseworkers to make better, faster decisions."

---

### [4:15-4:45] THE ARCHITECTURE (30 seconds)

**[Show: Scroll back to header, show KPI cards]**

> "The architecture is serverless, event-driven, and cost-optimized."

**[Pause 1 second]**

> "Built on AWS Bedrock with Nova Lite and Nova Pro, AWS Lambda for processing, and S3 for storage."

**[Pause 2 seconds]**

> "It's GDPR compliant, with 122 passing tests, and ready for pilot deployment with UK social care charities."

**[Pause 2 seconds]**

**[Show: AWS signature in lower-right]**

> "Powered by AWS."

---

### [4:45-5:00] CALL TO ACTION (15 seconds)

**[Show: Full page view, zoom out slightly]**

> "This is more than automation—it's safeguarding dignity and preventing crises before they happen."

**[Pause 2 seconds]**

> "Thank you for watching. The full source code and documentation are available on GitHub."

**[Pause 2 seconds]**

**[Show: Footer with GitHub link]**

> "CivicGuardian AI—built with AWS Kiro for the AWS 10,000 AIdeas 2025 competition."

**[Pause 2 seconds, fade to black]**

---

## Post-Recording Checklist

### Immediate Review
- [ ] Stop recording
- [ ] Save file as: `demo-video-raw.mov` or `.mp4`
- [ ] Watch full video
- [ ] Check audio quality (clear, no background noise)
- [ ] Check video quality (smooth, no lag)
- [ ] Verify all sections covered

### Re-record If Needed
**Re-record if:**
- Audio has background noise or echo
- Video is choppy or laggy
- You stumbled over words significantly
- Timing is off (too fast/slow)
- Missing key sections

**Don't re-record for:**
- Minor word stumbles (natural, authentic)
- Small pauses (helps comprehension)
- Slight timing variations

---

## Video Editing (Basic)

### Option A: QuickTime Player (Trim Only)
```
1. Open video in QuickTime Player
2. Edit → Trim
3. Drag yellow handles to trim start/end
4. File → Export As → 1080p
5. Save as: demo-video.mp4
```

### Option B: iMovie (Title Cards + Trim)
```
1. Open iMovie
2. Create New Project → Movie
3. Import video file
4. Add title card at start:
   - Text: "CivicGuardian AI"
   - Subtitle: "AWS 10,000 AIdeas 2025"
   - Duration: 3 seconds
5. Trim start/end if needed
6. Add end card:
   - Text: "Built with AWS Kiro"
   - Subtitle: "github.com/Deeplomatcode/CivicGuardian-AI"
   - Duration: 3 seconds
7. File → Share → File
   - Resolution: 1080p
   - Quality: High
   - Format: MP4
8. Save as: demo-video.mp4
```

### Option C: DaVinci Resolve (Advanced, Free)
```
1. Download: https://www.blackmagicdesign.com/products/davinciresolve
2. Import video
3. Add title cards, transitions, color grading
4. Export as MP4 (H.264, 1080p, 30fps)
```

---

## Export Settings

### Recommended Settings
- **Format:** MP4 (H.264)
- **Resolution:** 1920x1080
- **Frame Rate:** 30fps
- **Bitrate:** 8-10 Mbps (video), 192 kbps (audio)
- **Audio:** AAC, 44.1kHz, stereo
- **File Size Target:** <500MB (for easy upload)

### Compression (If File Too Large)
```bash
# Install ffmpeg
brew install ffmpeg

# Compress video
ffmpeg -i demo-video-raw.mp4 -vcodec h264 -crf 23 -preset medium -acodec aac -b:a 192k demo-video.mp4
```

---

## Upload Options

### Option 1: AWS Builder Center (Direct Upload)
- Max file size: Usually 100MB-500MB
- If video <500MB, upload directly to article

### Option 2: YouTube (Unlisted)
```
1. Upload to YouTube as "Unlisted"
2. Title: "CivicGuardian AI - AWS 10,000 AIdeas 2025"
3. Description: Link to GitHub + article
4. Copy video URL
5. Embed in article
```

### Option 3: Vimeo (Private)
```
1. Upload to Vimeo
2. Privacy: "Hide from Vimeo"
3. Copy embed code
4. Add to article
```

---

## Final Checklist

- [ ] Video recorded (3-5 minutes)
- [ ] Audio clear and professional
- [ ] All sections covered
- [ ] Title card added (optional)
- [ ] End card added (optional)
- [ ] Exported as MP4 (1080p, <500MB)
- [ ] File saved: `CivicGuardian AI/article/demo-video.mp4`
- [ ] Watched final export (quality check)
- [ ] Ready for article integration

---

## Troubleshooting

### Audio Issues
- **Echo:** Record in smaller room, add soft furnishings
- **Background noise:** Use Do Not Disturb, close windows
- **Low volume:** Speak closer to mic, increase input volume

### Video Issues
- **Choppy playback:** Close other apps, reduce recording quality
- **File too large:** Compress with ffmpeg (see above)
- **Wrong resolution:** Re-export at 1080p

### Timing Issues
- **Too fast:** Re-record, speak slower, add pauses
- **Too slow:** Edit out long pauses, trim sections
- **Too long (>5 min):** Cut introduction or architecture section

---

**Status:** Ready to record  
**Time Required:** 1-2 hours (including retakes and editing)  
**Next Action:** Set up recording software and begin recording

---

## Pro Tips

1. **Practice first:** Record a test run, watch it, then record for real
2. **Smile while speaking:** Improves vocal tone and energy
3. **Pause between sections:** Makes editing easier
4. **Point with cursor:** Help viewers follow along
5. **Slow down:** You're probably speaking faster than you think
6. **Hydrate:** Keep water nearby
7. **One take is fine:** Don't aim for perfection, aim for authentic
8. **Show, don't tell:** Let the UI speak for itself with pauses
