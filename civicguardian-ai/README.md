# CivicGuardian AI
A multi-agent AI safeguarding platform built on AWS that protects
vulnerable adults from missing critical deadlines in housing,
benefits, and healthcare correspondence.

Built for the AWS 10,000 AIdeas 2025 Competition — Social Impact
category. Team Phenix. Built using Kiro and deployed on AWS
Free Tier in eu-west-2 (London).

---

## The Problem

Margaret is 72 and has early-stage dementia. She receives 15
letters a month from her council, housing association, and NHS
trust. Last month she missed a critical deadline buried in a
housing benefit review notice. Two weeks later she received an
eviction warning.

Over 12,000 vulnerable adults in the UK lose housing each year
due to missed correspondence deadlines. Caseworkers manage 40+
clients each and cannot monitor all incoming mail. CivicGuardian
AI is their digital advocate.

---

## What It Does

CivicGuardian AI reads every letter, classifies the risk level,
drafts a legally-grounded response using UK legislation, validates
the draft for accuracy, and alerts a caseworker before harm occurs.
A human always approves before anything is sent. No vulnerable
adult falls through the cracks because of a missed deadline.

---

## Live Smoke Test Results (Real AWS Run — 28 March 2026)

Document tested: UK council eviction notice (CRITICAL case)

| Step | Result |
|---|---|
| S3 upload to Step Functions start | < 1 second |
| Nova Lite risk classification | CRITICAL |
| Cost gate (Nova Pro only for MEDIUM+) | Enforced at state machine level |
| Nova Pro policy draft (UK Housing Act 1996) | Generated |
| Nova Lite governor validation | Passed |
| SNS caseworker alert | Sent to Gmail |
| Caseworker approval via /approve endpoint | Approved |
| Step Functions execution status | SUCCEEDED |
| Total processing time (upload to SNS alert) | < 7 seconds |
| DynamoDB case record | approval_status = APPROVED |

All results from live AWS execution. Not simulated.

---

## Architecture

Three-agent pipeline orchestrated by AWS Step Functions:

Agent 1 — Risk Analyst (Nova Lite)
Triages every document. Classifies risk as LOW, MEDIUM, HIGH,
or CRITICAL. Returns deadline, required action, and confidence
score. Called on 100% of cases.

Agent 2 — Policy Reasoner (Nova Pro)
Drafts a legally-grounded response citing UK Care Act 2014,
Housing Act 1996, or Welfare Reform Act 2012 as appropriate.
Called ONLY when risk is MEDIUM or above. Cost gate enforced
at the Step Functions CostGate Choice state — never inside
application code.

Agent 3 — Governor (Nova Lite)
Validates the draft for factual consistency, legal soundness,
tone, and deadline logic. Can veto the Policy Reasoner output.
If confidence < 0.75 or risk is CRITICAL, mandatory human
escalation regardless of governor result.

Human approval is mandatory for all CRITICAL and HIGH cases
via SNS alert with approve/reject links. Step Functions pauses
execution using waitForTaskToken for up to 7 days.

---

## AWS Services

Service | Role
Amazon Bedrock Nova Lite | Risk Analyst and Governor agents
Amazon Bedrock Nova Pro | Policy Reasoner agent (MEDIUM+ only)
AWS Lambda Python 3.12 | 5 handlers plus 1 status handler
AWS Step Functions | GuardianLoop orchestrator
Amazon S3 | Inbox bucket and processed bucket
Amazon DynamoDB | CivicGuardianCases full audit trail
Amazon SNS | Caseworker alerts
Amazon API Gateway | presign approve reject status endpoints
Amazon Textract | PDF and image OCR
Amazon Transcribe | Voicemail to text
Amazon CloudWatch | Logs metrics dashboard alarms
AWS IAM | Least-privilege roles per Lambda
AWS Budgets | 150 USD cost ceiling with alerts

Region: eu-west-2 (London) — UK citizen data stays in UK.

---

## Cost Discipline

Nova Pro is called ONLY via the Step Functions CostGate state.
Nova Lite handles 100% of triage and validation.
Estimated cost per case: $0.26 average.
Nova Pro invocations per CRITICAL case: 1.
Nova Lite invocations per case: 2.
LOW risk cases (routine letters): 0 Bedrock Pro calls.

---

## Project Structure

civicguardian-ai/
lambdas/
ingest_handler/     S3 trigger, OCR, DynamoDB, Step Functions
risk_analyst/       Nova Lite triage
policy_reasoner/    Nova Pro draft MEDIUM+ only
governor/           Nova Lite validation and veto
escalation/         SNS alert and approve reject handler
status_handler/     Frontend polling endpoint
statemachine/
guardian_loop.asl.json
infra/
template.yaml       SAM template all AWS resources
tests/
fixtures/           5 UK letter test cases

---

## Deploy

Requirements: AWS SAM CLI, Python 3.12, AWS credentials

cd civicguardian-ai
sam build --template-file infra/template.yaml
sam deploy --guided --template-file infra/template.yaml --stack-name civicguardian-ai --region eu-west-2 --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

After deploy confirm the SNS email subscription from your inbox.

---

## Responsible AI

Human approval is mandatory for all CRITICAL cases with no
exceptions and no overrides. Governor agent can veto any
Policy Reasoner output. Every Lambda writes an audit_trail
entry to DynamoDB. Confidence threshold: cases below 0.75
always escalate. AI assists — humans decide. The vulnerable
adult is the beneficiary, not the operator.

---

## Built With Kiro

Kiro was used for specification-driven development throughout.
It generated all 6 Lambda handler scaffolds, wrote the Step
Functions ASL state machine, built the complete SAM template
including IAM roles, diagnosed and fixed 4 circular dependency
errors during deployment, and identified and fixed the URL
decode bug in the status handler. Total Kiro credits used:
under 50 of 2500 available.

---

## Builder Center Article

Search CivicGuardian AI on community.aws

## GitHub

https://github.com/Deeplomatcode/CivicGuardian-AI
