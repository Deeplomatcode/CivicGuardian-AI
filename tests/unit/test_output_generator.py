"""Unit tests for output_generator module."""

import pytest
from datetime import datetime
from processing_function.output_generator import generate_output_json


class TestGenerateOutputJson:
    """Tests for generate_output_json function."""
    
    def test_generate_output_with_high_confidence(self):
        """Test output generation with high confidence (>= 0.5)."""
        case_id = "test-case-123"
        document_s3_key = "s3://bucket/document.pdf"
        extracted_text = "This is extracted text content."
        metadata = {
            "sender": "NHS Trust",
            "document_type": "letter",
            "confidence": 0.85,
            "page_count": 2,
            "language": "en-GB"
        }
        status = "processed"
        
        result = generate_output_json(case_id, document_s3_key, extracted_text, metadata, status)
        
        # Verify all required fields present
        assert result["case_id"] == case_id
        assert result["document_s3_key"] == document_s3_key
        assert result["extracted_text"] == extracted_text
        assert result["status"] == status
        assert isinstance(result["timestamp"], int)
        assert result["timestamp"] > 0
        
        # Verify metadata structure
        assert result["metadata"]["sender"] == "NHS Trust"
        assert result["metadata"]["document_type"] == "letter"
        assert result["metadata"]["confidence"] == 0.85
        assert result["metadata"]["page_count"] == 2
        assert result["metadata"]["language"] == "en-GB"
        
        # Verify ISO 8601 timestamp format with Z suffix
        assert result["created_at"].endswith("Z")
        datetime.fromisoformat(result["created_at"].replace("Z", "+00:00"))
        
        # Verify low confidence flags NOT present for high confidence
        assert "low_confidence" not in result
        assert "manual_review_required" not in result
    
    def test_generate_output_with_low_confidence(self):
        """Test output generation with low confidence (< 0.5)."""
        case_id = "test-case-456"
        document_s3_key = "s3://bucket/document.pdf"
        extracted_text = "Poorly scanned text."
        metadata = {
            "sender": None,
            "document_type": "letter",
            "confidence": 0.35,
            "page_count": 1,
            "language": "en-GB"
        }
        status = "processed"
        
        result = generate_output_json(case_id, document_s3_key, extracted_text, metadata, status)
        
        # Verify low confidence flags ARE present
        assert result["low_confidence"] is True
        assert result["manual_review_required"] is True
        assert result["metadata"]["confidence"] == 0.35
    
    def test_generate_output_with_boundary_confidence(self):
        """Test output generation with confidence exactly at 0.5."""
        metadata = {
            "sender": "Council",
            "document_type": "letter",
            "confidence": 0.5,
            "page_count": 1,
            "language": "en-GB"
        }
        
        result = generate_output_json("case-789", "s3://bucket/doc.pdf", "text", metadata, "processed")
        
        # At exactly 0.5, should NOT trigger low confidence flags
        assert "low_confidence" not in result
        assert "manual_review_required" not in result
    
    def test_generate_output_with_null_sender(self):
        """Test output generation when sender is None."""
        metadata = {
            "sender": None,
            "document_type": "email",
            "confidence": 1.0,
            "page_count": 1,
            "language": "en-GB"
        }
        
        result = generate_output_json("case-null", "s3://bucket/email.txt", "email text", metadata, "processed")
        
        assert result["metadata"]["sender"] is None
    
    def test_generate_output_with_quarantined_status(self):
        """Test output generation for quarantined documents."""
        metadata = {
            "sender": "DWP",
            "document_type": "letter",
            "confidence": 0.0,
            "page_count": 0,
            "language": "en-GB"
        }
        
        result = generate_output_json("case-quarantine", "s3://bucket/bad.pdf", "", metadata, "quarantined")
        
        assert result["status"] == "quarantined"
        assert result["low_confidence"] is True
        assert result["manual_review_required"] is True
