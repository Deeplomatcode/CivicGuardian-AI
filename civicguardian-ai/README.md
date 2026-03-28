# CivicGuardian AI — Backend

Multi-agent safeguarding platform protecting vulnerable adults from missing critical deadlines.

**Stack:** Python 3.12 · AWS Lambda · Step Functions · S3 · DynamoDB · SNS · API Gateway · Bedrock (Nova Lite + Nova Pro) · Textract · Transcribe · CloudWatch · IAM · Budgets

---

## Rules (locked for every session)

- Python 3.12 only. No Node.js. No Go.
- Step Functions orchestrates everything. No Lambda calling another Lambda directly.
- Nova Pro called ONLY from `policy_reasoner_handler`. CostGate enforced at state machine level.
- No Cognito. Authentication is API key via API Gateway only.
- Bucket name: `civicguardian-inbox` (not civicguardian-incoming).
- DynamoDB table: `CivicGuardianCases`.

---

## Project Structure

```
civicguardian-ai/
├── lambdas/
│   ├── ingest_handler/     # S3 trigger → Textract/Transcribe/direct → DDB → SFN
│   ├── risk_analyst/       # Nova Lite risk assessment
│   ├── policy_reasoner/    # Nova Pro draft generation (MEDIUM/HIGH/CRITICAL only)
│   ├── governor/           # Nova Lite validation (factual, legal, tone, deadline)
│   └── escalation/         # SNS alert + task token + approve/reject API handler
├── statemachine/
│   └── guardian_loop.asl.json   # Step Functions Standard Workflow
├── infra/
│   └── template.yaml            # SAM template — all AWS resources
├── tests/
│   └── fixtures/                # 5 UK letter test cases
└── README.md
```

---

## Prerequisites

- AWS SAM CLI >= 1.100.0 (`sam --version`)
- AWS credentials configured (`aws sts get-caller-identity`)
- Python 3.12 installed
- Bedrock Nova Lite and Nova Pro enabled in eu-west-2 (check AWS console → Bedrock → Model access)

---

## Phase 2 — Local Test (run AFTER Phase 1 verification)

```bash
cd civicguardian-ai

# Build all Lambda packages
sam build --template infra/template.yaml

# Test risk analyst with eviction notice (expect CRITICAL)
sam local invoke RiskAnalystFunction \
  --event tests/fixtures/eviction_notice_sfn_event.json \
  --env-vars tests/env.json

# Test risk analyst with council tax demand (expect MEDIUM)
sam local invoke RiskAnalystFunction \
  --event tests/fixtures/council_tax_sfn_event.json \
  --env-vars tests/env.json
```

---

## Phase 3 — Deploy to AWS (eu-west-2)

```bash
sam build --template infra/template.yaml

sam deploy --guided \
  --stack-name civicguardian-ai \
  --region eu-west-2 \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --parameter-overrides CaseworkerEmail=deeplomatawslearning@gmail.com
```

**After deploy:**
1. Check your email — confirm the SNS subscription from AWS Notifications
2. Copy the `ApiGatewayBaseUrl` from the Outputs section
3. Redeploy with the real URL: `--parameter-overrides ApiGatewayUrl=https://YOUR_ID.execute-api.eu-west-2.amazonaws.com/prod`

---

## Smoke Test

```bash
# Upload eviction notice to inbox bucket
aws s3 cp tests/fixtures/eviction_notice.txt \
  s3://civicguardian-inbox/eviction_notice.txt \
  --region eu-west-2

# Watch Step Functions execution in AWS console:
# https://eu-west-2.console.aws.amazon.com/states/home?region=eu-west-2
```

---

## IMPORTANT: SNS Email Confirmation

Email subscriptions require manual confirmation. After `sam deploy`, check `deeplomatawslearning@gmail.com` for a confirmation email from AWS and click the confirmation link before testing.

---

## Services Used (approved list only)

Lambda · Step Functions · S3 · DynamoDB · SNS · API Gateway · CloudWatch · IAM · Budgets · Textract · Transcribe · Bedrock
