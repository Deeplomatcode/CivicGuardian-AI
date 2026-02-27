"""
Guardian Loop - Phase 1 Orchestrator
Ties together all implemented modules for document processing.
"""

import hashlib
import time
import os
from processing_function.file_detector import detect_file_type
from processing_function.text_extractors.email_extractor import extract as extract_email
from processing_function.metadata_extractor import extract_metadata
from processing_function.risk_analyst_agent import analyze_risk
from processing_function.output_generator import generate_output_json
from processing_function.storage_manager import save_to_local_file
from processing_function import monitoring


def process_document(file_path, output_dir):
    """
    Orchestrates document processing through all pipeline stages.
    
    Args:
        file_path: Path to the document file to process
        output_dir: Directory where output JSON should be saved
    
    Returns:
        dict: {
            "status": "success" or "failed",
            "case_id": generated case ID,
            "output_path": path to saved JSON file (if successful),
            "error": error message (if failed)
        }
    """
    # Generate case_id from file_path
    case_id = hashlib.sha256(file_path.encode('utf-8')).hexdigest()
    
    # Get file size for logging
    try:
        file_size = os.path.getsize(file_path)
    except Exception:
        file_size = 0
    
    # Log processing start
    monitoring.log_processing_start(case_id, file_size)
    start_time = time.time()
    
    try:
        # Step 1: Detect file type
        file_type, extension = detect_file_type(file_path)
        
        # Step 2: Extract text based on file type
        if file_type == 'email':
            extraction_result = extract_email(file_path, extension)
        else:
            extraction_result = {
                "status": "success",
                "text": f"Extraction not yet implemented for {file_type}",
                "confidence": 1.0,
                "page_count": 1
            }
        
        # Check if extraction failed
        if extraction_result["status"] == "failed":
            error_msg = extraction_result.get("error", "Unknown extraction error")
            monitoring.log_error(case_id, "extraction_failed")
            duration_ms = int((time.time() - start_time) * 1000)
            monitoring.log_processing_complete(case_id, duration_ms, 0.0)
            return {
                "status": "failed",
                "case_id": case_id,
                "error": error_msg
            }
        
        extracted_text = extraction_result["text"]
        
        # Step 3: Extract metadata
        metadata = extract_metadata(extracted_text, file_type, extraction_result)
        
        # Step 4: Analyze risk using Amazon Bedrock Nova Lite
        risk_assessment = analyze_risk(extracted_text, metadata)
        
        # Step 5: Generate output JSON
        output_json = generate_output_json(
            case_id=case_id,
            document_s3_key=file_path,  # Will be S3 URI in Phase 3
            extracted_text=extracted_text,
            metadata=metadata,
            status="processed"
        )
        
        # Add risk assessment to output
        output_json["risk_assessment"] = risk_assessment
        
        # Step 6: Save to storage
        filename = f"{case_id}.json"
        save_result = save_to_local_file(output_dir, filename, output_json)
        
        # Check if save failed
        if save_result["status"] == "failed":
            error_msg = save_result.get("error", "Unknown storage error")
            monitoring.log_error(case_id, "storage_failed")
            duration_ms = int((time.time() - start_time) * 1000)
            monitoring.log_processing_complete(case_id, duration_ms, metadata["confidence"])
            return {
                "status": "failed",
                "case_id": case_id,
                "error": error_msg
            }
        
        # Log successful completion
        duration_ms = int((time.time() - start_time) * 1000)
        monitoring.log_processing_complete(case_id, duration_ms, metadata["confidence"])
        
        # Return success result
        output_path = os.path.join(output_dir, filename)
        return {
            "status": "success",
            "case_id": case_id,
            "output_path": output_path
        }
        
    except Exception as e:
        # Catch any unexpected errors
        error_msg = f"{type(e).__name__}: {str(e)}"
        monitoring.log_error(case_id, type(e).__name__)
        duration_ms = int((time.time() - start_time) * 1000)
        monitoring.log_processing_complete(case_id, duration_ms, 0.0)
        return {
            "status": "failed",
            "case_id": case_id,
            "error": error_msg
        }
