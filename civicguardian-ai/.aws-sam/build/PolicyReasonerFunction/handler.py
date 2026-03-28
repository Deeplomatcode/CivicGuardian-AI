"""
policy_reasoner_handler — Lambda entry point
Invoked by: Step Functions (RunPolicyReasoner state) — ONLY for MEDIUM/HIGH/CRITICAL
Responsibilities:
  1. Fetch raw_text and risk fields from DynamoDB
  2. Build context-enriched prompt with UK legislation excerpts
  3. Call Bedrock Nova Pro (max 3,000 input tokens)
  4. Update DynamoDB with draft_response
  5. Emit NovaProInvocations + CostPerCase CloudWatch metrics
  6. Write audit_trail entry
  7. Return draft to Step Functions
"""

import json
import os
import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError

# ── AWS clients ───────────────────────────────────────────────────────────────
dynamodb = boto3.resource("dynamodb")
bedrock = boto3.client("bedrock-runtime")
cloudwatch = boto3.client("cloudwatch")

# ── Environment variables ─────────────────────────────────────────────────────
TABLE_NAME = os.environ["TABLE_NAME"]

# ── Bedrock model ─────────────────────────────────────────────────────────────
NOVA_PRO_MODEL = "amazon.nova-pro-v1:0"
MAX_INPUT_TOKENS = 3000
MAX_OUTPUT_TOKENS = 1500

# Estimated cost per Nova Pro call (input + output tokens at published rates)
NOVA_PRO_COST_ESTIMATE_USD = 0.012

# ── System prompt (legislation context injected into user message per spec) ───
POLICY_SYSTEM_PROMPT = """You are a UK social care policy advisor drafting a formal response letter for a vulnerable adult.
Generate a DRAFT response only — this will be reviewed by a caseworker before sending.
Return ONLY valid JSON — no prose, no markdown outside the JSON values.

Schema:
{
  "draft_response": "Full letter text: salutation, body paragraphs citing correct statute, requested action, sign-off",
  "legislation_cited": ["Act name and section"],
  "confidence": 0.0 to 1.0,
  "safety_notice": "DRAFT FOR REVIEW - Not legal advice"
}

Rules:
- Do NOT use definitive language: 'legally required', 'this guarantees', 'certainly', 'will be upheld', 'must comply'
- Always include the safety_notice field with exact value: DRAFT FOR REVIEW - Not legal advice
- Cite only legislation relevant to the case type
- Keep draft_response under 500 words
- Return ONLY the JSON object"""

# ── UK Legislation context (injected into user message) ──────────────────────
LEGISLATION_CONTEXT = """
RELEVANT UK LEGISLATION EXCERPTS:

Care Act 2014:
- Section 9: Local authority must assess any adult who appears to have care and support needs
- Section 10: Local authority must assess a carer who appears to have support needs
- Section 18: Local authority must meet eligible care and support needs of an adult
- Section 19: Local authority may meet care and support needs not meeting eligibility criteria

Housing Act 1996:
- Part VI (s.159-174): Allocation of social housing; local authority duties to applicants
- Part VII (s.175-218): Homelessness; local authority duty to provide accommodation to eligible homeless persons

Welfare Reform Act 2012:
- DWP obligations to notify claimants of changes to Universal Credit entitlement
- Mandatory reconsideration rights before appeal to First-tier Tribunal

Local Authority Complaint Rights:
- Right to complain to Local Government and Social Care Ombudsman
- Complaint must be acknowledged within 3 working days
- Full response required within 20 working days
"""


def _chunk_text(text: str, max_tokens: int = MAX_INPUT_TOKENS) -> str:
    max_chars = max_tokens * 4
    return text[:max_chars] if len(text) > max_chars else text


def _build_user_message(raw_text: str, risk_level: str, deadline, required_action: str) -> str:
    chunked = _chunk_text(raw_text, max_tokens=2500)
    return f"""{LEGISLATION_CONTEXT}

CASE DETAILS:
- Risk Level: {risk_level}
- Deadline: {deadline or 'Not specified'}
- Required Action: {required_action or 'Review required'}

ORIGINAL DOCUMENT:
{chunked}

Generate the draft response JSON now."""


def _parse_response(text: str) -> dict:
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON in response")
    data = json.loads(text[start:end])
    conf = data.get("confidence", 0.5)
    data["confidence"] = max(0.0, min(1.0, float(conf)))
    if "safety_notice" not in data:
        data["safety_notice"] = "DRAFT FOR REVIEW - Not legal advice"
    return data


def _write_audit(table, case_id: str, created_at: str, action: str, detail: dict):
    now = datetime.now(timezone.utc).isoformat()
    table.update_item(
        Key={"case_id": case_id, "created_at": created_at},
        UpdateExpression="SET audit_trail = list_append(if_not_exists(audit_trail, :empty), :entry)",
        ExpressionAttributeValues={
            ":empty": [],
            ":entry": [{"action": action, "timestamp": now, "detail": json.dumps(detail)}],
        },
    )


def lambda_handler(event, context):
    case_id = event["case_id"]
    created_at = event["created_at"]
    risk_level = event.get("risk_level", "MEDIUM")
    deadline = event.get("deadline")
    required_action = event.get("required_action", "Review required")

    table = dynamodb.Table(TABLE_NAME)

    # ── Fetch raw_text from DynamoDB ──────────────────────────────────────────
    resp = table.get_item(Key={"case_id": case_id, "created_at": created_at})
    item = resp.get("Item", {})
    raw_text = item.get("raw_text", "")

    if not raw_text:
        raise ValueError(f"No raw_text for case_id={case_id}")

    # ── Call Bedrock Nova Pro ─────────────────────────────────────────────────
    user_message = _build_user_message(raw_text, risk_level, deadline, required_action)

    bedrock_response = bedrock.converse(
        modelId=NOVA_PRO_MODEL,
        system=[{"text": POLICY_SYSTEM_PROMPT}],
        messages=[{"role": "user", "content": [{"text": user_message}]}],
        inferenceConfig={"maxTokens": MAX_OUTPUT_TOKENS, "temperature": 0.3},
    )

    response_text = bedrock_response["output"]["message"]["content"][0]["text"]
    policy_data = _parse_response(response_text)

    draft_response = policy_data.get("draft_response", "")
    legislation_cited = policy_data.get("legislation_cited", [])
    confidence = policy_data["confidence"]

    # ── Update DynamoDB ───────────────────────────────────────────────────────
    table.update_item(
        Key={"case_id": case_id, "created_at": created_at},
        UpdateExpression="""SET draft_response = :dr,
                               legislation_cited = :lc,
                               policy_model = :pm,
                               approval_status = :st""",
        ExpressionAttributeValues={
            ":dr": draft_response,
            ":lc": legislation_cited,
            ":pm": "nova-pro",
            ":st": "POLICY_DRAFTED",
        },
    )

    # ── Audit trail ───────────────────────────────────────────────────────────
    _write_audit(table, case_id, created_at, "POLICY_DRAFTED", {
        "model": "nova-pro",
        "confidence": confidence,
        "legislation_cited": legislation_cited,
    })

    # ── CloudWatch metrics ────────────────────────────────────────────────────
    cloudwatch.put_metric_data(
        Namespace="CivicGuardian/Performance",
        MetricData=[
            {"MetricName": "NovaProInvocations", "Value": 1, "Unit": "Count"},
            {"MetricName": "CostPerCase", "Value": NOVA_PRO_COST_ESTIMATE_USD, "Unit": "None"},
        ],
    )

    print(json.dumps({"case_id": case_id, "event": "policy_drafted", "confidence": confidence}))

    return {
        "case_id": case_id,
        "created_at": created_at,
        "risk_level": risk_level,
        "deadline": deadline,
        "required_action": required_action,
        "draft_confidence": confidence,
    }
