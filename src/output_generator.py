# Output generation and validation module
# Generates structured JSON output and validates schema

import time
from datetime import datetime


def generate_output_json(case_id, document_s3_key, extracted_text, metadata, status):
    """
    Generates structured JSON output conforming to schema.
    
    Args:
        case_id: Unique UUID identifier for the case
        document_s3_key: S3 URI of the source document
        extracted_text: Extracted text content from the document
        metadata: Dict containing sender, document_type, confidence, page_count, language
        status: Processing status (processed or quarantined)
    
    Returns:
        dict: Complete output JSON with all required fields
    """
    output = {
        "case_id": case_id,
        "timestamp": int(time.time()),
        "document_s3_key": document_s3_key,
        "extracted_text": extracted_text,
        "metadata": {
            "sender": metadata["sender"],
            "document_type": metadata["document_type"],
            "confidence": metadata["confidence"],
            "page_count": metadata["page_count"],
            "language": metadata["language"]
        },
        "status": status,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    # Add low confidence flags if needed
    if metadata["confidence"] < 0.5:
        output["low_confidence"] = True
        output["manual_review_required"] = True
    
    return output


def validate_schema(output_json):
    """
    Validates that output JSON contains all required fields.
    
    Returns:
        bool: True if valid, False otherwise
    """
    # Implementation will be added in subsequent tasks
    pass
