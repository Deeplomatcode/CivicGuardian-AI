"""
governor_handler — Lambda entry point
Invoked by: Step Functions (RunGovernor state)
Responsibilities:
  1. Fetch raw_text and draft_response from DynamoDB
  2. Call Bedrock Nova Lite with both texts for validation
  3. Check: factual consistency, legal soundness, tone, deadline logic
  4. Update DynamoDB with governor fields
  5. Emit NovaLiteInvocations CloudWatch metric
  6. Write audit_trail entry
  7. Return {confidence_score, approved, veto_reason} to Step Functions
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
NOVA_LITE_MODEL = "amazon.nova-lite-v1:0"
MAX_OUTPUT_TOKENS = 512

# ── Governor system prompt ────────────────────────────────────────────────────
GOVERNOR_SYSTEM_PROMPT = """You are a governance validator for an AI safeguarding system reviewing a draft letter for a vulnerable adult.
Check four things:
1. Factual consistency: Does the draft reference the correct deadline from the original document?
2. Legal soundness: Is the cited statute relevant to this case type?
3. Tone: Is the letter respectful, clear, and assertive where needed?
4. Deadline logic: Is the proposed response timeline achievable given the deadline?

Return ONLY valid JSON, no prose:
{
  "confidence_score": 0.0 to 1.0,
  "approved": true or false,
  "veto_reason": "reason string or null",
  "checks": {
    "factual_consistency": true or false,
    "legal_soundness": true or false,
    "tone": true or false,
    "deadline_logic": true or false
  }
}

Set approved=false if ANY check fails or confidence_score < 0.75.
Return ONLY the JSON object."""


def _chunk_text(text: str, max_chars: int = 3000) -> str:
    return text[:max_chars] if len(text) > max_chars else text


def _build_validation_message(raw_text: str, draft_response: str, deadline, risk_level: str) -> str:
    return f"""ORIGINAL DOCUMENT (source of truth):
{_chunk_text(raw_text, 2000)}

DRAFT RESPONSE TO VALIDATE:
{_chunk_text(draft_response, 2000)}

CASE CONTEXT:
- Risk Level: {risk_level}
- Deadline: {deadline or 'Not specified'}

Validate the draft against the original document and return the JSON assessment."""


def _parse_response(text: str) -> dict:
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON in governor response")
    data = json.loads(text[start:end])

    conf = data.get("confidence_score", 0.0)
    data["confidence_score"] = max(0.0, min(1.0, float(conf)))

    if "approved" not in data:
        data["approved"] = data["confidence_score"] >= 0.75

    if "veto_reason" not in data:
        data["veto_reason"] = None

    if "checks" not in data:
        data["checks"] = {
            "factual_consistency": True,
            "legal_soundness": True,
            "tone": True,
            "deadline_logic": True,
        }

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

    table = dynamodb.Table(TABLE_NAME)

    # ── Fetch raw_text and draft_response from DynamoDB ───────────────────────
    resp = table.get_item(Key={"case_id": case_id, "created_at": created_at})
    item = resp.get("Item", {})
    raw_text = item.get("raw_text", "")
    draft_response = item.get("draft_response", "")

    if not draft_response:
        # No draft to validate — auto-veto, escalate to human
        return {
            "case_id": case_id,
            "created_at": created_at,
            "risk_level": risk_level,
            "deadline": deadline,
            "confidence_score": 0.0,
            "approved": False,
            "veto_reason": "No draft response available for validation",
        }

    # ── Call Bedrock Nova Lite ────────────────────────────────────────────────
    user_message = _build_validation_message(raw_text, draft_response, deadline, risk_level)

    bedrock_response = bedrock.converse(
        modelId=NOVA_LITE_MODEL,
        system=[{"text": GOVERNOR_SYSTEM_PROMPT}],
        messages=[{"role": "user", "content": [{"text": user_message}]}],
        inferenceConfig={"maxTokens": MAX_OUTPUT_TOKENS, "temperature": 0.1},
    )

    response_text = bedrock_response["output"]["message"]["content"][0]["text"]
    gov_data = _parse_response(response_text)

    confidence_score = gov_data["confidence_score"]
    approved = gov_data["approved"]
    veto_reason = gov_data.get("veto_reason")
    checks = gov_data.get("checks", {})

    # ── Update DynamoDB ───────────────────────────────────────────────────────
    table.update_item(
        Key={"case_id": case_id, "created_at": created_at},
        UpdateExpression="""SET governor_confidence = :gc,
                               governor_approved = :ga,
                               veto_reason = :vr,
                               governor_checks = :ch,
                               approval_status = :st""",
        ExpressionAttributeValues={
            ":gc": str(confidence_score),
            ":ga": approved,
            ":vr": veto_reason,
            ":ch": checks,
            ":st": "GOVERNOR_REVIEWED",
        },
    )

    # ── Audit trail ───────────────────────────────────────────────────────────
    _write_audit(table, case_id, created_at, "GOVERNOR_REVIEWED", {
        "confidence_score": confidence_score,
        "approved": approved,
        "veto_reason": veto_reason,
        "checks": checks,
    })

    # ── CloudWatch metric ─────────────────────────────────────────────────────
    cloudwatch.put_metric_data(
        Namespace="CivicGuardian/Performance",
        MetricData=[{"MetricName": "NovaLiteInvocations", "Value": 1, "Unit": "Count"}],
    )

    print(json.dumps({
        "case_id": case_id,
        "event": "governor_reviewed",
        "approved": approved,
        "confidence_score": confidence_score,
    }))

    return {
        "case_id": case_id,
        "created_at": created_at,
        "risk_level": risk_level,
        "deadline": deadline,
        "confidence_score": confidence_score,
        "approved": approved,
        "veto_reason": veto_reason,
    }
