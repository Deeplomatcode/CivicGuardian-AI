"""
risk_analyst_handler — Lambda entry point
Invoked by: Step Functions (RunRiskAnalyst state)
Responsibilities:
  1. Fetch raw_text from DynamoDB using case_id
  2. Chunk text to max 1,500 tokens
  3. Call Bedrock Nova Lite for risk analysis
  4. Update DynamoDB with risk fields
  5. Emit NovaLiteInvocations CloudWatch metric
  6. Write audit_trail entry
  7. Return structured result to Step Functions
"""

import json
import os
import time
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
MAX_INPUT_TOKENS = 1500
MAX_OUTPUT_TOKENS = 512

# ── System prompt ─────────────────────────────────────────────────────────────
RISK_SYSTEM_PROMPT = """You are analyzing UK public-service correspondence for a vulnerable adult.
Extract exactly these fields and return ONLY valid JSON — no prose, no markdown, no explanation.

Schema:
{
  "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "deadline": "YYYY-MM-DD or descriptive timeframe or null",
  "required_action": "one sentence, specific action needed",
  "sender_authority": "council | DWP | NHS | housing_association | other",
  "confidence": 0.0 to 1.0
}

Rules:
- CRITICAL applies to: eviction notices, benefit suspension, care plan cancellation
- HIGH applies to: formal warnings, payment demands with deadlines, care reviews
- MEDIUM applies to: review letters, appointment requests, non-urgent benefit changes
- LOW applies to: acknowledgements, routine repairs, information letters
- If ambiguous, set risk_level ONE level higher than your best guess
- Return ONLY the JSON object. No other text."""


def _chunk_text(text: str, max_tokens: int = MAX_INPUT_TOKENS) -> str:
    """Approximate token chunking: ~4 chars per token."""
    max_chars = max_tokens * 4
    return text[:max_chars] if len(text) > max_chars else text


def _call_nova_lite(text: str) -> dict:
    chunked = _chunk_text(text)
    response = bedrock.converse(
        modelId=NOVA_LITE_MODEL,
        system=[{"text": RISK_SYSTEM_PROMPT}],
        messages=[{"role": "user", "content": [{"text": chunked}]}],
        inferenceConfig={"maxTokens": MAX_OUTPUT_TOKENS, "temperature": 0.1},
    )
    return response


def _parse_response(response_text: str) -> dict:
    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON in response")
    data = json.loads(response_text[start:end])

    valid_levels = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    rl = str(data.get("risk_level", "MEDIUM")).upper()
    data["risk_level"] = rl if rl in valid_levels else "MEDIUM"

    conf = data.get("confidence", 0.5)
    data["confidence"] = max(0.0, min(1.0, float(conf)))

    for field in ("deadline", "required_action", "sender_authority"):
        if field not in data:
            data[field] = None

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

    table = dynamodb.Table(TABLE_NAME)

    # ── Fetch raw_text from DynamoDB ──────────────────────────────────────────
    resp = table.get_item(Key={"case_id": case_id, "created_at": created_at})
    item = resp.get("Item", {})
    raw_text = item.get("raw_text", "")

    if not raw_text:
        raise ValueError(f"No raw_text found for case_id={case_id}")

    # ── Call Bedrock Nova Lite ────────────────────────────────────────────────
    bedrock_response = _call_nova_lite(raw_text)
    response_text = bedrock_response["output"]["message"]["content"][0]["text"]
    risk_data = _parse_response(response_text)

    # ── Update DynamoDB with risk fields ──────────────────────────────────────
    now = datetime.now(timezone.utc).isoformat()
    table.update_item(
        Key={"case_id": case_id, "created_at": created_at},
        UpdateExpression="""SET risk_level = :rl,
                               deadline = :dl,
                               required_action = :ra,
                               sender_authority = :sa,
                               risk_confidence = :rc,
                               approval_status = :st""",
        ExpressionAttributeValues={
            ":rl": risk_data["risk_level"],
            ":dl": risk_data.get("deadline"),
            ":ra": risk_data.get("required_action"),
            ":sa": risk_data.get("sender_authority"),
            ":rc": str(risk_data["confidence"]),
            ":st": "RISK_ASSESSED",
        },
    )

    # ── Audit trail ───────────────────────────────────────────────────────────
    _write_audit(table, case_id, created_at, "RISK_ASSESSED", {
        "risk_level": risk_data["risk_level"],
        "confidence": risk_data["confidence"],
        "deadline": risk_data.get("deadline"),
    })

    # ── CloudWatch metric ─────────────────────────────────────────────────────
    cloudwatch.put_metric_data(
        Namespace="CivicGuardian/Performance",
        MetricData=[{"MetricName": "NovaLiteInvocations", "Value": 1, "Unit": "Count"}],
    )

    # ── Emit FalseNegativeRisk if CRITICAL with low confidence ────────────────
    if risk_data["risk_level"] == "CRITICAL" and risk_data["confidence"] < 0.75:
        cloudwatch.put_metric_data(
            Namespace="CivicGuardian/Performance",
            MetricData=[{"MetricName": "FalseNegativeRisk", "Value": 1, "Unit": "Count"}],
        )

    print(json.dumps({"case_id": case_id, "event": "risk_assessed", "risk_level": risk_data["risk_level"]}))

    return {
        "case_id": case_id,
        "created_at": created_at,
        "risk_level": risk_data["risk_level"],
        "deadline": risk_data.get("deadline"),
        "required_action": risk_data.get("required_action"),
        "sender_authority": risk_data.get("sender_authority"),
        "confidence": risk_data["confidence"],
    }
