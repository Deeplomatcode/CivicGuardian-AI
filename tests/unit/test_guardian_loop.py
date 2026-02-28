"""
Unit tests for guardian_loop orchestrator.
Tests end-to-end document processing workflow.
"""

import unittest
import tempfile
import os
import json
import hashlib
from unittest.mock import patch, MagicMock
from processing_function.guardian_loop import process_document


class TestGuardianLoop(unittest.TestCase):
    """Test cases for guardian_loop orchestrator."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directories for test files
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = tempfile.mkdtemp()
        
        # Create test email file
        self.email_file = os.path.join(self.test_dir, "test_email.txt")
        with open(self.email_file, 'w') as f:
            f.write("From: NHS Trust\nSubject: Test\n\nThis is a test email from NHS Trust.")
        
        # Create test PDF file (for unsupported type testing)
        self.pdf_file = os.path.join(self.test_dir, "test_doc.pdf")
        with open(self.pdf_file, 'w') as f:
            f.write("PDF content placeholder")
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
        shutil.rmtree(self.output_dir, ignore_errors=True)
    
    def test_successful_email_processing_end_to_end(self):
        """Test successful email processing through entire pipeline."""
        result = process_document(self.email_file, self.output_dir)
        
        # Verify result structure
        self.assertEqual(result["status"], "success")
        self.assertIn("case_id", result)
        self.assertIn("output_path", result)
        
        # Verify case_id generation
        expected_case_id = hashlib.sha256(self.email_file.encode('utf-8')).hexdigest()
        self.assertEqual(result["case_id"], expected_case_id)
        
        # Verify output file was created
        self.assertTrue(os.path.exists(result["output_path"]))
        
        # Verify output JSON structure
        with open(result["output_path"], 'r') as f:
            output_json = json.load(f)
        
        self.assertEqual(output_json["case_id"], expected_case_id)
        self.assertEqual(output_json["document_s3_key"], self.email_file)
        self.assertIn("NHS Trust", output_json["extracted_text"])
        self.assertEqual(output_json["metadata"]["sender"], "NHS Trust")
        self.assertEqual(output_json["metadata"]["document_type"], "email")
        self.assertEqual(output_json["metadata"]["confidence"], 1.0)
        self.assertEqual(output_json["status"], "processed")
        self.assertIn("timestamp", output_json)
        self.assertIn("created_at", output_json)
    
    def test_unsupported_file_type_handling(self):
        """Test handling of unsupported file types (PDF in Phase 1)."""
        result = process_document(self.pdf_file, self.output_dir)
        
        # Should succeed but with placeholder message
        self.assertEqual(result["status"], "success")
        self.assertIn("case_id", result)
        self.assertIn("output_path", result)
        
        # Verify output contains placeholder message
        with open(result["output_path"], 'r') as f:
            output_json = json.load(f)
        
        self.assertIn("Extraction not yet implemented for pdf", output_json["extracted_text"])
        self.assertEqual(output_json["metadata"]["document_type"], "letter")
    
    def test_case_id_generation_consistency(self):
        """Test that case_id generation is consistent for same file path."""
        result1 = process_document(self.email_file, self.output_dir)
        
        # Clean up first output
        os.remove(result1["output_path"])
        
        result2 = process_document(self.email_file, self.output_dir)
        
        # Case IDs should be identical
        self.assertEqual(result1["case_id"], result2["case_id"])
        
        # Verify it matches expected hash
        expected_case_id = hashlib.sha256(self.email_file.encode('utf-8')).hexdigest()
        self.assertEqual(result1["case_id"], expected_case_id)
    
    def test_error_handling_extraction_failure(self):
        """Test error handling when text extraction fails."""
        with patch('processing_function.guardian_loop.extract_email') as mock_extract:
            mock_extract.return_value = {
                "status": "failed",
                "error": "File not found"
            }
            
            result = process_document(self.email_file, self.output_dir)
            
            self.assertEqual(result["status"], "failed")
            self.assertIn("case_id", result)
            self.assertIn("error", result)
            self.assertIn("File not found", result["error"])
            self.assertNotIn("output_path", result)
    
    def test_error_handling_storage_failure(self):
        """Test error handling when storage operation fails."""
        with patch('processing_function.guardian_loop.save_to_local_file') as mock_save:
            mock_save.return_value = {
                "status": "failed",
                "error": "Permission denied"
            }
            
            result = process_document(self.email_file, self.output_dir)
            
            self.assertEqual(result["status"], "failed")
            self.assertIn("case_id", result)
            self.assertIn("error", result)
            self.assertIn("Permission denied", result["error"])
            self.assertNotIn("output_path", result)
    
    def test_error_handling_metadata_extraction_exception(self):
        """Test error handling when metadata extraction raises exception."""
        with patch('processing_function.guardian_loop.extract_metadata') as mock_metadata:
            mock_metadata.side_effect = ValueError("Invalid metadata")
            
            result = process_document(self.email_file, self.output_dir)
            
            self.assertEqual(result["status"], "failed")
            self.assertIn("case_id", result)
            self.assertIn("error", result)
            self.assertIn("ValueError", result["error"])
            self.assertIn("Invalid metadata", result["error"])
    
    def test_error_handling_file_not_found(self):
        """Test error handling when input file doesn't exist."""
        nonexistent_file = os.path.join(self.test_dir, "nonexistent.txt")
        
        result = process_document(nonexistent_file, self.output_dir)
        
        self.assertEqual(result["status"], "failed")
        self.assertIn("case_id", result)
        self.assertIn("error", result)
    
    @patch('processing_function.guardian_loop.monitoring.log_processing_start')
    @patch('processing_function.guardian_loop.monitoring.log_processing_complete')
    @patch('processing_function.guardian_loop.monitoring.log_error')
    def test_logging_on_success(self, mock_log_error, mock_log_complete, mock_log_start):
        """Test that monitoring logs are called correctly on success."""
        result = process_document(self.email_file, self.output_dir)
        
        # Verify logging calls
        self.assertEqual(result["status"], "success")
        mock_log_start.assert_called_once()
        mock_log_complete.assert_called_once()
        mock_log_error.assert_not_called()
        
        # Verify log_start parameters
        call_args = mock_log_start.call_args[0]
        self.assertEqual(call_args[0], result["case_id"])
        self.assertIsInstance(call_args[1], int)  # file_size
        
        # Verify log_complete parameters
        call_args = mock_log_complete.call_args[0]
        self.assertEqual(call_args[0], result["case_id"])
        self.assertIsInstance(call_args[1], int)  # duration_ms
        self.assertEqual(call_args[2], 1.0)  # confidence
    
    @patch('processing_function.guardian_loop.monitoring.log_processing_start')
    @patch('processing_function.guardian_loop.monitoring.log_processing_complete')
    @patch('processing_function.guardian_loop.monitoring.log_error')
    def test_logging_on_extraction_failure(self, mock_log_error, mock_log_complete, mock_log_start):
        """Test that monitoring logs are called correctly on extraction failure."""
        with patch('processing_function.guardian_loop.extract_email') as mock_extract:
            mock_extract.return_value = {
                "status": "failed",
                "error": "Extraction error"
            }
            
            result = process_document(self.email_file, self.output_dir)
            
            self.assertEqual(result["status"], "failed")
            mock_log_start.assert_called_once()
            mock_log_error.assert_called_once()
            mock_log_complete.assert_called_once()
            
            # Verify log_error parameters
            call_args = mock_log_error.call_args[0]
            self.assertEqual(call_args[0], result["case_id"])
            self.assertEqual(call_args[1], "extraction_failed")
    
    @patch('processing_function.guardian_loop.monitoring.log_processing_start')
    @patch('processing_function.guardian_loop.monitoring.log_processing_complete')
    @patch('processing_function.guardian_loop.monitoring.log_error')
    def test_logging_on_storage_failure(self, mock_log_error, mock_log_complete, mock_log_start):
        """Test that monitoring logs are called correctly on storage failure."""
        with patch('processing_function.guardian_loop.save_to_local_file') as mock_save:
            mock_save.return_value = {
                "status": "failed",
                "error": "Storage error"
            }
            
            result = process_document(self.email_file, self.output_dir)
            
            self.assertEqual(result["status"], "failed")
            mock_log_start.assert_called_once()
            mock_log_error.assert_called_once()
            mock_log_complete.assert_called_once()
            
            # Verify log_error parameters
            call_args = mock_log_error.call_args[0]
            self.assertEqual(call_args[0], result["case_id"])
            self.assertEqual(call_args[1], "storage_failed")
    
    @patch('processing_function.guardian_loop.monitoring.log_processing_start')
    @patch('processing_function.guardian_loop.monitoring.log_processing_complete')
    @patch('processing_function.guardian_loop.monitoring.log_error')
    def test_logging_on_unexpected_exception(self, mock_log_error, mock_log_complete, mock_log_start):
        """Test that monitoring logs are called correctly on unexpected exception."""
        with patch('processing_function.guardian_loop.detect_file_type') as mock_detect:
            mock_detect.side_effect = RuntimeError("Unexpected error")
            
            result = process_document(self.email_file, self.output_dir)
            
            self.assertEqual(result["status"], "failed")
            mock_log_start.assert_called_once()
            mock_log_error.assert_called_once()
            mock_log_complete.assert_called_once()
            
            # Verify log_error parameters
            call_args = mock_log_error.call_args[0]
            self.assertEqual(call_args[0], result["case_id"])
            self.assertEqual(call_args[1], "RuntimeError")
    
    def test_timing_information_included(self):
        """Test that timing information is captured and logged."""
        with patch('processing_function.guardian_loop.monitoring.log_processing_complete') as mock_log:
            result = process_document(self.email_file, self.output_dir)
            
            self.assertEqual(result["status"], "success")
            
            # Verify duration_ms was logged
            call_args = mock_log.call_args[0]
            duration_ms = call_args[1]
            self.assertIsInstance(duration_ms, int)
            self.assertGreaterEqual(duration_ms, 0)  # Can be 0 for very fast operations
    
    def test_html_email_processing(self):
        """Test processing of HTML email files."""
        html_file = os.path.join(self.test_dir, "test_email.html")
        with open(html_file, 'w') as f:
            f.write("<html><body><p>From: DWP</p><p>Test HTML email</p></body></html>")
        
        result = process_document(html_file, self.output_dir)
        
        self.assertEqual(result["status"], "success")
        
        # Verify output
        with open(result["output_path"], 'r') as f:
            output_json = json.load(f)
        
        self.assertIn("DWP", output_json["extracted_text"])
        self.assertEqual(output_json["metadata"]["document_type"], "email")


if __name__ == '__main__':
    unittest.main()
