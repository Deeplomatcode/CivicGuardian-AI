# GitHub Repository Setup Instructions

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in repository details:
   - **Name:** `CivicGuardian-AI`
   - **Description:** `AI-powered digital advocate for vulnerable adults - AWS 10,000 AIdeas 2026 semifinalist`
   - **Visibility:** Public
   - **Initialize:** Do NOT add README, .gitignore, or license (we already have these)
3. Click "Create repository"

## Step 2: Connect Local Repository to GitHub

Run these commands in your terminal:

```bash
cd ~/Projects/CivicGuardian\ AI

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/CivicGuardian-AI.git

# Verify remote was added
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 3: Verify Upload

1. Go to `https://github.com/YOUR_USERNAME/CivicGuardian-AI`
2. Verify all files are visible
3. Check that README.md displays correctly
4. Verify architecture diagram renders

## Step 4: Update Article with GitHub URL

Once repository is live, update the article:

**File:** `article/builder-center-article.md`

**Section:** "Try It Yourself"

**Change:**
```markdown
**GitHub Repository:** [Will add link]
```

**To:**
```markdown
**GitHub Repository:** https://github.com/YOUR_USERNAME/CivicGuardian-AI
```

Then commit:
```bash
git add article/builder-center-article.md
git commit -m "Add GitHub repository URL to article"
git push
```

## Step 5: Optional - Add Topics to Repository

On GitHub repository page:
1. Click "Add topics"
2. Add: `aws`, `bedrock`, `nova`, `ai`, `social-impact`, `serverless`, `kiro`, `vulnerable-adults`, `uk-care`
3. Save changes

## Troubleshooting

**Error: "remote origin already exists"**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/CivicGuardian-AI.git
```

**Error: "failed to push"**
```bash
git pull origin main --rebase
git push -u origin main
```

**Large files warning**
- All files should be under 100MB
- Largest file is architecture-diagram.png (333KB) - well within limits

---

**Estimated Time:** 10 minutes total
