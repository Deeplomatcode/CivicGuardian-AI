# CivicGuardian AI — Demo Video Script
2 minutes | AWS 10,000 AIdeas 2025 | Team Phenix

## Section 1 — Hook [0:00-0:15]
On screen: CivicGuardian AI frontend at localhost:8000
Narrator: "Margaret is 72, has early-stage dementia, and last month she missed a housing benefit deadline buried in a council letter. This is the tool that makes sure that never happens again."

## Section 2 — Upload [0:15-0:35]
On screen: Upload eviction_notice.txt from tests/fixtures/
Narrator: "We are uploading a real UK council eviction notice. The frontend requests a presigned S3 URL, uploads directly to the inbox bucket, and the pipeline starts."

## Section 3 — Pipeline [0:35-1:05]
On screen: Processing log polling, then Step Functions execution graph
Narrator: "AWS Step Functions orchestrates three AI agents. The Risk Analyst on Nova Lite classifies the risk. The Policy Reasoner on Nova Pro drafts a response citing the Housing Act 1996. The Governor on Nova Lite validates the draft before anything goes further."

## Section 4 — Results [1:05-1:25]
On screen: Frontend results — CRITICAL risk, confidence score, draft letter
Narrator: "Risk level CRITICAL, confidence 87 percent, deadline flagged. Full response letter drafted. Governor approved it. Under seven seconds from upload."

## Section 5 — SNS Alert [1:25-1:40]
On screen: Gmail inbox — URGENT CivicGuardian email
Narrator: "Because this is CRITICAL, Step Functions paused and sent an SNS alert to the caseworker. Risk level, draft preview, approve or reject."

## Section 6 — Approval [1:40-1:55]
On screen: Click approve, Step Functions SUCCEEDED, DynamoDB APPROVED
Narrator: "The caseworker clicks approve. Execution completes. DynamoDB records the full audit trail. Case closed. Human in the loop the whole way."

## Section 7 — Close [1:55-2:00]
On screen: GitHub repo then back to frontend
Narrator: "This is CivicGuardian AI — built on AWS, protecting vulnerable adults one letter at a time."

## Real Test Metrics (Live AWS — 28 March 2026)

| Document | Risk | Confidence | Status |
|---|---|---|---|
| eviction_notice.txt | CRITICAL | 0.95 | APPROVED |
| benefit_review.txt | HIGH | 0.95 | AWAITING_APPROVAL |
| care_plan_change.txt | MEDIUM | 0.85 | AWAITING_APPROVAL |
| council_tax_demand.txt | HIGH | 0.90 | AWAITING_APPROVAL |
| routine_repair.txt | LOW | 0.90 | ARCHIVED |

Average confidence: 0.91
Cost gate proof: routine_repair archived with zero Nova Pro calls.
