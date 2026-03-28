"""
ingest_handler — Lambda entry point
Triggered by: S3 ObjectCreated event on civicguardian-inbox
Responsibilities:
  1. Detect file type from S3 key extension
  2. Route to Textract (pdf/image), Transcribe (audio), or direct read (txt/eml)
  3. Extract metadata (sender, deadline hints)
  4. Write initial case record to DynamoDB CivicGuardianCases
  5. Start Step Functions GuardianLoop execution
  6. Write audit_trail entry
"""

import json
import os
import re
import time
import uuid
import hashlib
import boto3
from datetime import datetime, timezone
from html.parser import HTMLParser
from botocore.exceptions import ClientError

# ── AWS clients ──────────────────────────────────────────────────────────────
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
textract = boto3.client("textract")
transcribe = boto3.client("transcribe")
sfn = boto3.client("stepfunctions")
cloudwatch = boto3.client("cloudwatch")

# ── Environment variables ─────────────────────────────────────────────────────
TABLE_NAME = os.environ["TABLE_NAME"]
INBOX_BUCKET = os.environ["INBOX_BUCKET"]
PROCESSED_BUCKET = os.environ["PROCESSED_BUCKET"]
STATE_MACHINE_ARN = os.environ["STATE_MACHINE_ARN"]

# ── Sender detection patterns ─────────────────────────────────────────────────
SENDER_PATTERNS = [
    r"\bNHS\s+(?:Trust|Foundation|England)\b",
    r"\b(?:City|County|Borough|District)\s+Council\b",
    r"\bDepartment\s+for\s+Work\s+and\s+Pensions\b",
    r"\bDWP\b",
    r"\bHMRC\b",
    r"\bHer\s+Majesty.?s\s+Revenue\s+and\s+Customs\b",
    r"\bSocial\s+Services\b",
    r"\bAdult\s+Social\s+Care\b",
    r"\bHousing\s+(?:Association|Department|Office)\b",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _detect_file_type(key: str) -> tuple[str, str]:
    ext = key.lower().rsplit(".", 1)[-1] if "." in key else ""
    if ext == "pdf":
        return "pdf", ext
    if ext in ("jpg", "jpeg", "png", "tiff"):
        return "image", ext
    if ext in ("mp3", "wav", "m4a"):
        return "audio", ext
    if ext in ("txt", "eml", "html"):
        return "email", ext
    return "unsupported", ext


def _generate_case_id(object_key: str, etag: str) -> str:
    raw = f"{object_key}:{etag}".encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    return str(uuid.UUID(digest[:32]))


def _detect_sender(text: str):
    for pattern in SENDER_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return m.group(0)
    return None


def _strip_html(html: str) -> str:
    class _P(HTMLParser):
        def __init__(self):
            super().__init__()
            self.parts = []
        def handle_data(self, d):
            self.parts.append(d)
    p = _P()
    p.feed(html)
    return "".join(p.parts)


def _extract_email(bucket: str, key: str, ext: str) -> dict:
    obj = s3.get_object(Bucket=bucket, Key=key)
    raw = obj["Body"].read().decode("utf-8", errors="replace")
    text = _strip_html(raw) if ext == "html" else raw
    return {"status": "success", "text": text.strip(), "confidence": 1.0, "page_count": 1}


def _extract_textract(bucket: str, key: str) -> dict:
    try:
        resp = textract.detect_document_text(
            Document={"S3Object": {"Bucket": bucket, "Name": key}}
        )
        lines, scores, pages = [], [], 0
        for block in resp.get("Blocks", []):
            if block["BlockType"] == "LINE":
                lines.append(block["Text"])
                scores.append(block.get("Confidence", 100))
            elif block["BlockType"] == "PAGE":
                pages += 1
        text = "\n".join(lines)
        conf = (sum(scores) / len(scores) / 100.0) if scores else 0.0
        return {"status": "success", "text": text, "confidence": round(conf, 3), "page_count": max(pages, 1)}
    except ClientError as e:
        return {"status": "failed", "error": str(e)}


def _extract_transcribe(bucket: str, key: str) -> dict:
    job_name = f"cg-{int(time.time())}-{uuid.uuid4().hex[:8]}"
    media_uri = f"s3://{bucket}/{key}"
    ext = key.lower().rsplit(".", 1)[-1]
    fmt_map = {"mp3": "mp3", "wav": "wav", "m4a": "mp4"}
    media_format = fmt_map.get(ext, "mp3")
    try:
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": media_uri},
            MediaFormat=media_format,
            LanguageCode="en-GB",
            OutputBucketName=bucket,
            OutputKey=f"transcripts/{job_name}.json",
        )
        # Poll up to 25 seconds
        deadline = time.time() + 25
        while time.time() < deadline:
            time.sleep(3)
            r = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            status = r["TranscriptionJob"]["TranscriptionJobStatus"]
            if status == "COMPLETED":
                out_key = f"transcripts/{job_name}.json"
                obj = s3.get_object(Bucket=bucket, Key=out_key)
                data = json.loads(obj["Body"].read())
                text = data["results"]["transcripts"][0]["transcript"]
                items = data["results"].get("items", [])
                scores = [float(i["alternatives"][0]["confidence"])
                          for i in items if i.get("alternatives") and "confidence" in i["alternatives"][0]]
                conf = sum(scores) / len(scores) if scores else 0.0
                return {"status": "success", "text": text, "confidence": round(conf, 3), "page_count": 1}
            if status == "FAILED":
                return {"status": "failed", "error": "Transcribe job failed"}
        return {"status": "failed", "error": "Transcribe timeout after 25 seconds"}
    except ClientError as e:
        return {"status": "failed", "error": str(e)}


def _write_audit(table, case_id: str, action: str, detail: dict):
    now = datetime.now(timezone.utc).isoformat()
    table.update_item(
        Key={"case_id": case_id, "created_at": detail.get("created_at", now)},
        UpdateExpression="SET audit_trail = list_append(if_not_exists(audit_trail, :empty), :entry)",
        ExpressionAttributeValues={
            ":empty": [],
            ":entry": [{"action": action, "timestamp": now, "detail": json.dumps(detail)}],
        },
    )


# ── Handler ───────────────────────────────────────────────────────────────────

def lambda_handler(event, context):
    record = event["Records"][0]["s3"]
    bucket = record["bucket"]["name"]
    key = record["object"]["key"]
    etag = record["object"].get("eTag", record["object"].get("etag", ""))
    file_size = record["object"].get("size", 0)

    case_id = _generate_case_id(key, etag)
    created_at = datetime.now(timezone.utc).isoformat()
    expires_at = int(time.time()) + (90 * 86400)  # 90-day TTL

    file_type, ext = _detect_file_type(key)

    # ── Route to extractor ────────────────────────────────────────────────────
    if file_type == "pdf" or file_type == "image":
        extraction = _extract_textract(bucket, key)
    elif file_type == "audio":
        extraction = _extract_transcribe(bucket, key)
    elif file_type == "email":
        extraction = _extract_email(bucket, key, ext)
    else:
        # Unsupported — quarantine by copying to processed/quarantine/
        s3.copy_object(
            Bucket=PROCESSED_BUCKET,
            CopySource={"Bucket": bucket, "Key": key},
            Key=f"quarantine/{case_id}/{key}",
        )
        print(json.dumps({"case_id": case_id, "event": "quarantined", "reason": "unsupported_file_type"}))
        return {"statusCode": 400, "body": "Unsupported file type"}

    if extraction["status"] == "failed":
        print(json.dumps({"case_id": case_id, "event": "extraction_failed", "error": extraction.get("error")}))
        return {"statusCode": 500, "body": "Extraction failed"}

    raw_text = extraction["text"]
    confidence = extraction["confidence"]
    page_count = extraction["page_count"]
    sender = _detect_sender(raw_text)

    # ── Write initial DynamoDB record ─────────────────────────────────────────
    table = dynamodb.Table(TABLE_NAME)
    item = {
        "case_id": case_id,
        "created_at": created_at,
        "file_key": key,
        "file_type": file_type,
        "raw_text": raw_text,
        "sender_authority": sender or "unknown",
        "extraction_confidence": str(confidence),
        "page_count": page_count,
        "approval_status": "INGESTING",
        "audit_trail": [
            {
                "action": "INGESTED",
                "timestamp": created_at,
                "detail": json.dumps({
                    "file_type": file_type,
                    "file_size": file_size,
                    "confidence": confidence,
                }),
            }
        ],
        "expires_at": expires_at,
    }
    table.put_item(Item=item)

    # ── Start Step Functions execution ────────────────────────────────────────
    sfn_input = {
        "case_id": case_id,
        "created_at": created_at,
        "file_key": key,
        "file_type": file_type,
        "sender_authority": sender or "unknown",
    }
    sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        name=f"case-{case_id[:8]}-{int(time.time())}",
        input=json.dumps(sfn_input),
    )

    # ── CloudWatch metric ─────────────────────────────────────────────────────
    cloudwatch.put_metric_data(
        Namespace="CivicGuardian/Performance",
        MetricData=[{"MetricName": "DocumentsIngested", "Value": 1, "Unit": "Count"}],
    )

    print(json.dumps({"case_id": case_id, "event": "ingestion_complete", "file_type": file_type}))
    return {"statusCode": 200, "body": json.dumps({"case_id": case_id, "status": "INGESTING"})}
