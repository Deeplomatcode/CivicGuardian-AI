# Publication Checklist
**Date:** March 6, 2026  
**Deadline:** End of day  
**Platform:** AWS Builder Center

---

## Pre-Publication (Complete Before Uploading)

### Article Content
- [ ] All screenshots captured (8 total)
- [ ] All screenshots saved in `article/screenshots/`
- [ ] Demo video recorded and edited
- [ ] Video saved as `article/demo-video.mp4`
- [ ] Video file size <500MB (or uploaded to YouTube)

### Article Updates
- [ ] Open `article/builder-center-article.md`
- [ ] Add screenshot references with captions
- [ ] Add video embed or link
- [ ] Update "Demo Video" section with actual link
- [ ] Final proofread (spelling, grammar)
- [ ] Verify all technical claims accurate
- [ ] Check all links work
- [ ] Verify GitHub repository public

### Technical Verification
- [ ] GitHub repository: https://github.com/Deeplomatcode/CivicGuardian-AI
- [ ] Repository README updated
- [ ] All code committed and pushed
- [ ] Demo UI accessible (can be cloned and run)
- [ ] No sensitive data in repository (API keys, credentials)

---

## AWS Builder Center Publication

### Step 1: Access Platform
1. Navigate to: https://community.aws/buildon
2. Sign in with AWS account
3. Click "Create Post" or "Write Article"

### Step 2: Article Metadata
**Title:**
```
Building CivicGuardian AI: A Digital Safety Net for Vulnerable Adults Using AWS Bedrock Nova
```

**Category:**
- [ ] Select: "Social Impact" or "AI/ML"

**Tags:**
```
#aideas-2025
#social-impact
#EMEA
#bedrock
#nova
#serverless
#kiro
#ai4good
#public-sector
```

**Summary/Excerpt (150-200 characters):**
```
A serverless AI system built on AWS Bedrock Nova that prevents housing crises for vulnerable adults by monitoring correspondence and flagging urgent risks before deadlines pass.
```

### Step 3: Upload Content
- [ ] Copy article text from `builder-center-article.md`
- [ ] Paste into editor
- [ ] Format headings (H1, H2, H3)
- [ ] Format code blocks
- [ ] Format lists and bullets

### Step 4: Upload Media
**Screenshots:**
- [ ] Upload `screenshot-ui-01-landing.png`
- [ ] Upload `screenshot-ui-02-document-preview.png`
- [ ] Upload `screenshot-ui-03-processing-log.png`
- [ ] Upload `screenshot-ui-04-risk-dashboard.png`
- [ ] Upload `screenshot-ui-05-draft-response.png`
- [ ] Upload `screenshot-ui-06-validation.png`
- [ ] Upload `screenshot-ui-07-full-workflow.png`
- [ ] Upload `screenshot-ui-08-mobile-view.png` (optional)

**Video:**
- [ ] Upload `demo-video.mp4` (if <500MB)
- OR
- [ ] Upload to YouTube as "Unlisted"
- [ ] Copy YouTube URL
- [ ] Embed in article

**Architecture Diagram:**
- [ ] Upload `architecture-diagram.png`

**Sample Outputs:**
- [ ] Upload `sample-output-risk-analyst.json`
- [ ] Upload `sample-output-policy-reasoner.json`
- [ ] Upload `sample-output-governor.json`

### Step 5: Insert Media References
For each screenshot, add caption:
```markdown
![Landing Page](screenshot-ui-01-landing.png)
*Figure 7: CivicGuardian AI landing page showing mission panel and system capabilities*
```

Update figure numbers to match article flow.

### Step 6: Preview
- [ ] Click "Preview" button
- [ ] Verify all images load
- [ ] Verify video plays (or YouTube embed works)
- [ ] Check formatting (headings, code blocks, lists)
- [ ] Verify links work (GitHub, external references)
- [ ] Check mobile view (if platform supports)
- [ ] Read through entire article

### Step 7: Final Checks
- [ ] Spell check complete
- [ ] Grammar check complete
- [ ] Technical accuracy verified
- [ ] No placeholder text (e.g., "[Your Name]")
- [ ] No broken links
- [ ] No missing images
- [ ] Video accessible

### Step 8: Publish
- [ ] Click "Publish" button
- [ ] Confirm publication
- [ ] Copy shareable URL
- [ ] Save URL: ___________________________________

---

## Post-Publication

### Immediate Verification
- [ ] Open published article in new browser tab
- [ ] Verify all content displays correctly
- [ ] Test all links
- [ ] Test video playback
- [ ] Check images load
- [ ] Verify formatting correct

### Social Media Sharing

#### LinkedIn Post
**Template:**
```
🛡️ Introducing CivicGuardian AI - A Digital Safety Net for Vulnerable Adults

Over 12,000 vulnerable adults in the UK lose housing each year due to missed administrative deadlines. Not because help isn't available, but because the system is too complex to navigate.

I built CivicGuardian AI for the AWS 10,000 AIdeas 2025 competition to solve this problem.

🔹 Built on AWS Bedrock with Amazon Nova Lite & Nova Pro
🔹 Serverless, event-driven architecture
🔹 Three-agent validation system (Risk Analyst, Policy Reasoner, Governor)
🔹 GDPR compliant with human-in-the-loop oversight
🔹 122 passing tests, production-ready codebase

The system monitors correspondence, flags urgent risks like eviction notices, and drafts compliant responses before harm occurs—at $0.38 per case.

This isn't automation replacing humans. It's AI assisting caseworkers to safeguard dignity and prevent crises.

Read the full article: [INSERT URL]
GitHub: https://github.com/Deeplomatcode/CivicGuardian-AI

#AWSAIdeas #AI4Good #SocialImpact #AWS #Bedrock #Nova #Serverless #PublicSector

@AWS @AWSCloud @AmazonBedrock
```

**Actions:**
- [ ] Post to LinkedIn
- [ ] Tag AWS, AWS Bedrock, AWS Kiro
- [ ] Add article link
- [ ] Add screenshot (use screenshot-ui-01-landing.png)

#### Twitter/X Post
**Template:**
```
🛡️ Built CivicGuardian AI for @AWS 10,000 AIdeas 2025

A digital safety net for vulnerable adults that prevents housing crises by monitoring correspondence and flagging urgent risks.

✅ AWS Bedrock Nova Lite + Pro
✅ Serverless architecture
✅ 3-agent validation
✅ GDPR compliant
✅ 122 tests passing

Article: [INSERT URL]
GitHub: https://github.com/Deeplomatcode/CivicGuardian-AI

#AWSAIdeas #AI4Good #SocialImpact
```

**Actions:**
- [ ] Post to Twitter/X
- [ ] Tag @AWS, @AWSCloud
- [ ] Add article link
- [ ] Add screenshot

#### AWS Community Slack
**Template:**
```
Hi everyone! 👋

I just published my AWS 10,000 AIdeas 2025 submission: CivicGuardian AI - a digital safety net for vulnerable adults built on AWS Bedrock Nova.

The system prevents housing crises by monitoring correspondence and flagging urgent risks before deadlines pass. Built with serverless architecture, three-agent validation, and human-in-the-loop oversight.

Would love your feedback!

Article: [INSERT URL]
GitHub: https://github.com/Deeplomatcode/CivicGuardian-AI

#aideas-2025 #social-impact
```

**Actions:**
- [ ] Post in #aideas-2025 channel (if exists)
- [ ] Post in #bedrock channel
- [ ] Post in #serverless channel
- [ ] Post in #community-builders channel

### Competition Submission

#### AWS 10,000 AIdeas Portal
1. Navigate to: https://aws.amazon.com/10000aideas/
2. Click "Submit Project"
3. Fill in submission form:
   - [ ] Project name: CivicGuardian AI
   - [ ] Category: Social Good
   - [ ] Region: EMEA
   - [ ] Article URL: [INSERT URL]
   - [ ] GitHub URL: https://github.com/Deeplomatcode/CivicGuardian-AI
   - [ ] Video URL: [INSERT URL or YouTube link]
   - [ ] Team name: Team Phenix
   - [ ] Team members: [Your name]
4. Submit

**Confirmation:**
- [ ] Submission confirmation email received
- [ ] Submission ID: ___________________________________
- [ ] Submission date: March 6, 2026

---

## Backup & Archive

### Save Local Copies
```bash
cd ~/Projects/CivicGuardian\ AI/article

# Create archive
tar -czf civicguardian-ai-submission-2026-03-06.tar.gz \
  builder-center-article.md \
  screenshots/ \
  demo-video.mp4 \
  architecture-diagram.png \
  sample-output-*.json

# Move to safe location
mv civicguardian-ai-submission-2026-03-06.tar.gz ~/Documents/Backups/
```

### Git Commit
```bash
cd ~/Projects/CivicGuardian\ AI

git add .
git commit -m "Final submission: Article published, screenshots captured, video recorded"
git push origin main
```

### Cloud Backup (Optional)
- [ ] Upload archive to Google Drive
- [ ] Upload archive to Dropbox
- [ ] Upload archive to iCloud

---

## Success Metrics

### Publication Metrics (Track Over Time)
- [ ] Article views: ___________
- [ ] Article likes: ___________
- [ ] Article comments: ___________
- [ ] GitHub stars: ___________
- [ ] GitHub forks: ___________
- [ ] LinkedIn engagement: ___________
- [ ] Twitter engagement: ___________

### Competition Metrics
- [ ] Submission confirmed: Yes/No
- [ ] Finalist notification: (Wait for email)
- [ ] Final presentation: (If selected)

---

## Timeline Summary

**Hour 1-2:** UI optimization ✅ COMPLETE
**Hour 3:** Screenshot capture → IN PROGRESS
**Hour 4-5:** Video recording → PENDING
**Hour 6:** Article updates → PENDING
**Hour 7-8:** Publication & sharing → PENDING

---

## Emergency Contacts

**AWS Builder Center Support:**
- Email: community-support@aws.amazon.com
- Forum: https://community.aws/support

**AWS 10,000 AIdeas Support:**
- Email: aideas@aws.amazon.com
- FAQ: https://aws.amazon.com/10000aideas/faq

**Technical Issues:**
- GitHub Issues: https://github.com/Deeplomatcode/CivicGuardian-AI/issues

---

## Final Sign-Off

- [ ] Article published successfully
- [ ] URL saved and shared
- [ ] Social media posts live
- [ ] Competition submission confirmed
- [ ] Backup created
- [ ] Git repository updated

**Published by:** _______________  
**Date:** March 6, 2026  
**Time:** _______________  
**Article URL:** _______________  
**Submission ID:** _______________

---

**🎉 CONGRATULATIONS! 🎉**

You've completed the emergency same-day publication push. The article is live, the demo is polished, and your submission is in.

Now rest, and wait for the finalist announcement!

**Competition Deadline:** March 13, 2026 (7 days remaining)  
**Finalist Notification:** TBD (check email)

Good luck! 🍀
