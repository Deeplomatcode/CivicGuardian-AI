"""
Unit tests for monitoring.py module.
Tests CloudWatch logging functions with JSON structured output.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from processing_function.monitoring import (
    log_processing_start,
    log_processing_complete,
    log_error,
    log_warning
)


class TestLoggingFunctions:
    """Test suite for CloudWatch logging functions."""
    
    @patch('builtins.print')
    @patch('time.time', return_value=1234567890.123)
    def test_log_processing_start(self, mock_time, mock_print):
        """Test log_processing_start outputs correct JSON format."""
        case_id = "550e8400-e29b-41d4-a716-446655440000"
        file_size = 1024
        
        log_processing_start(case_id, file_size)
        
        # Verify print was called once
        assert mock_print.call_count == 1
        
        # Parse the JSON output
        logged_data = json.loads(mock_print.call_args[0][0])
        
        # Verify structure and content
        assert logged_data["event"] == "processing_start"
        assert logged_data["case_id"] == case_id
        assert logged_data["file_size"] == file_size
        assert logged_data["timestamp"] == 1234567890.123
        
        # Verify no PII fields present
        assert "extracted_text" not in logged_data
        assert "sender" not in logged_data
        assert "address" not in logged_data
    
    @patch('builtins.print')
    @patch('time.time', return_value=1234567890.456)
    def test_log_processing_complete(self, mock_time, mock_print):
        """Test log_processing_complete outputs correct JSON format."""
        case_id = "550e8400-e29b-41d4-a716-446655440000"
        duration_ms = 2500
        confidence = 0.95
        
        log_processing_complete(case_id, duration_ms, confidence)
        
        # Verify print was called once
        assert mock_print.call_count == 1
        
        # Parse the JSON output
        logged_data = json.loads(mock_print.call_args[0][0])
        
        # Verify structure and content
        assert logged_data["event"] == "processing_complete"
        assert logged_data["case_id"] == case_id
        assert logged_data["duration_ms"] == duration_ms
        assert logged_data["confidence"] == confidence
        assert logged_data["timestamp"] == 1234567890.456
        
        # Verify no PII fields present
        assert "extracted_text" not in logged_data
        assert "sender" not in logged_data
    
    @patch('builtins.print')
    @patch('time.time', return_value=1234567890.789)
    def test_log_error(self, mock_time, mock_print):
        """Test log_error outputs correct JSON format."""
        case_id = "550e8400-e29b-41d4-a716-446655440000"
        error_type = "ThrottlingException"
        
        log_error(case_id, error_type)
        
        # Verify print was called once
        assert mock_print.call_count == 1
        
        # Parse the JSON output
        logged_data = json.loads(mock_print.call_args[0][0])
        
        # Verify structure and content
        assert logged_data["event"] == "error"
        assert logged_data["case_id"] == case_id
        assert logged_data["error_type"] == error_type
        assert logged_data["timestamp"] == 1234567890.789
        
        # Verify no PII fields present
        assert "extracted_text" not in logged_data
        assert "sender" not in logged_data
        assert "address" not in logged_data
    
    @patch('builtins.print')
    @patch('time.time', return_value=1234567891.0)
    def test_log_warning(self, mock_time, mock_print):
        """Test log_warning outputs correct JSON format."""
        message = "Lambda approaching timeout at 28 seconds"
        
        log_warning(message)
        
        # Verify print was called once
        assert mock_print.call_count == 1
        
        # Parse the JSON output
        logged_data = json.loads(mock_print.call_args[0][0])
        
        # Verify structure and content
        assert logged_data["event"] == "warning"
        assert logged_data["message"] == message
        assert logged_data["timestamp"] == 1234567891.0
    
    @patch('builtins.print')
    def test_log_processing_start_with_large_file(self, mock_print):
        """Test logging with large file size."""
        case_id = "test-case-id"
        file_size = 104857600  # 100 MB
        
        log_processing_start(case_id, file_size)
        
        logged_data = json.loads(mock_print.call_args[0][0])
        assert logged_data["file_size"] == file_size
    
    @patch('builtins.print')
    def test_log_processing_complete_with_low_confidence(self, mock_print):
        """Test logging with low confidence score."""
        case_id = "test-case-id"
        duration_ms = 5000
        confidence = 0.35  # Low confidence
        
        log_processing_complete(case_id, duration_ms, confidence)
        
        logged_data = json.loads(mock_print.call_args[0][0])
        assert logged_data["confidence"] == 0.35
    
    @patch('builtins.print')
    def test_log_error_with_various_error_types(self, mock_print):
        """Test logging different error types."""
        case_id = "test-case-id"
        error_types = [
            "ThrottlingException",
            "ProvisionedThroughputExceededException",
            "ServiceException",
            "ValidationException"
        ]
        
        for error_type in error_types:
            log_error(case_id, error_type)
            logged_data = json.loads(mock_print.call_args[0][0])
            assert logged_data["error_type"] == error_type
    
    @patch('builtins.print')
    def test_json_output_is_valid(self, mock_print):
        """Test that all logging functions produce valid JSON."""
        # Test each logging function
        log_processing_start("case-1", 1024)
        json.loads(mock_print.call_args[0][0])  # Should not raise
        
        log_processing_complete("case-2", 2000, 0.9)
        json.loads(mock_print.call_args[0][0])  # Should not raise
        
        log_error("case-3", "TestError")
        json.loads(mock_print.call_args[0][0])  # Should not raise
        
        log_warning("Test warning")
        json.loads(mock_print.call_args[0][0])  # Should not raise
    
    @patch('builtins.print')
    def test_case_id_is_only_identifier(self, mock_print):
        """Test that case_id is the only identifier in logs (no PII)."""
        case_id = "550e8400-e29b-41d4-a716-446655440000"
        
        # Test processing start
        log_processing_start(case_id, 1024)
        logged_data = json.loads(mock_print.call_args[0][0])
        assert logged_data["case_id"] == case_id
        assert len([k for k in logged_data.keys() if "id" in k.lower()]) == 1
        
        # Test processing complete
        log_processing_complete(case_id, 2000, 0.9)
        logged_data = json.loads(mock_print.call_args[0][0])
        assert logged_data["case_id"] == case_id
        
        # Test error logging
        log_error(case_id, "TestError")
        logged_data = json.loads(mock_print.call_args[0][0])
        assert logged_data["case_id"] == case_id
