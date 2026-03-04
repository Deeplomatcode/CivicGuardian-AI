# Screenshot Guide for CivicGuardian AI

## Screenshot 1: Git Commit History (Proof of Development)

**Command to run:**
```bash
git log --oneline --graph --all --decorate -15
```

**What to capture:** Terminal showing 15 commits with graph

**Save as:** `article/screenshot-01-git-history.png`

**Article reference:** "Figure 2: Complete development history with Kiro-assisted commits"

---

## Screenshot 2: All Agent Files (Code Proof)

**Command to run:**
```bash
ls -lh src/*_agent.py src/guardian_loop.py src/monitoring.py
```

**What to capture:** Terminal showing all agent files with sizes

**Save as:** `article/screenshot-02-agent-files.png`

**Article reference:** "Figure 3: Core agent implementations (23KB total)"

---

## Screenshot 3: Test Suite (Quality Proof)

**Command to run:**
```bash
find tests/unit -name "test_*.py" -exec ls -lh {} \; | head -15
```

**What to capture:** Terminal showing test files

**Save as:** `article/screenshot-03-test-suite.png`

**Article reference:** "Figure 4: Comprehensive test coverage (13 test files, 122 tests)"

---

## Screenshot 4: Sample JSON Output (Workflow Proof)

**Command to run:**
```bash
cat article/sample-output-policy-reasoner.json | python3 -m json.tool
```

**What to capture:** Terminal showing formatted JSON (policy reasoner output)

**Save as:** `article/screenshot-04-json-output.png`

**Article reference:** "Figure 5: Policy Reasoner output with UK legal citations"

---

## Screenshot 5: Project Structure (Organization Proof)

**Command to run:**
```bash
ls -la | grep -v ".git\|__pycache__\|.pytest"
```

**What to capture:** Terminal showing clean project structure

**Save as:** `article/screenshot-05-project-structure.png`

**Article reference:** "Figure 6: Production-ready repository organization"

---

## Quick Screenshot Instructions

**For macOS:**
1. Run command in terminal
2. Press `Cmd + Shift + 4` (select area)
3. Drag to select terminal output
4. Image saves to Desktop
5. Move to article/ folder: `mv ~/Desktop/Screenshot*.png article/screenshot-0X-name.png`

**For Windows:**
1. Run command in terminal
2. Press `Windows + Shift + S` (snipping tool)
3. Select terminal area
4. Save as PNG
5. Move to article/ folder

**Time estimate:** 15 minutes for all 5 screenshots
