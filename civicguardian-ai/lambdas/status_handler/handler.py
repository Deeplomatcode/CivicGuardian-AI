"""
status_handler — Lambda for GET /status/{fileKey}
Queries DynamoDB by file_key using a full-table scan with FilterExpression.
The fileKey path parameter is URL-decoded before comparison.
"""

import json
import os
import urllib.parse
import boto3
from boto3.dynamodb.conditions import Attr

TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb = boto3.resource("dynamodb")

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
}


def _ok(body: dict) -> dict:
    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps(body, default=str),
    }


def _err(code: int, msg: str) -> dict:
    return {
        "statusCode": code,
        "headers": CORS_HEADERS,
        "body": json.dumps({"error": msg}),
    }


def lambda_handler(event, context):
    # Handle CORS preflight
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": CORS_HEADERS, "body": ""}

    path_params = event.get("pathParameters") or {}
    raw_key = path_params.get("fileKey", "")

    if not raw_key:
        return _err(400, "Missing fileKey path parameter")

    # URL-decode: API Gateway may encode the slash in uploads/filename
    # as %2F, so we need to decode it back to match what ingest_handler stored
    file_key = urllib.parse.unquote(raw_key)

    print(json.dumps({"event": "status_lookup", "raw_key": raw_key, "file_key": file_key}))

    table = dynamodb.Table(TABLE_NAME)

    # Full scan with FilterExpression — paginate to ensure we don't miss items
    items = []
    scan_kwargs = {"FilterExpression": Attr("file_key").eq(file_key)}

    while True:
        resp = table.scan(**scan_kwargs)
        items.extend(resp.get("Items", []))
        last = resp.get("LastEvaluatedKey")
        if not last:
            break
        scan_kwargs["ExclusiveStartKey"] = last

    print(json.dumps({"event": "status_scan_result", "file_key": file_key, "items_found": len(items)}))

    if not items:
        return _err(404, f"Case not found for file_key: {file_key}")

    # Take the most recent item
    item = sorted(items, key=lambda x: x.get("created_at", ""), reverse=True)[0]

    status = item.get("approval_status", "PROCESSING")

    # Safely coerce governor_confidence — DynamoDB may store as Decimal
    raw_conf = item.get("governor_confidence") or item.get("extraction_confidence") or 0
    try:
        conf = float(raw_conf)
    except (TypeError, ValueError):
        conf = 0.0

    payload = {
        "status": status,
        "approval_status": status,
        "case_id": item.get("case_id"),
        "risk_level": item.get("risk_level"),
        "deadline": item.get("deadline"),
        "required_action": item.get("required_action"),
        "urgency_indicators": item.get("urgency_indicators") or [],
        "sender_authority": item.get("sender_authority"),
        "draft_response": item.get("draft_response"),
        "rationale_bullets": item.get("rationale_bullets") or [],
        "legislation_referenced": item.get("legislation_referenced") or [],
        "governor_confidence": conf,
        "required_escalation": bool(item.get("required_escalation", False)),
    }

    print(json.dumps({"event": "status_response", "case_id": payload["case_id"], "status": status}))
    return _ok(payload)
