"""
Unit tests for storage_manager module.
Tests the save_to_local_file function (Phase 1).
"""

import json
import os
import tempfile
import shutil
import pytest
from processing_function.storage_manager import save_to_local_file


class TestSaveToLocalFile:
    """Tests for save_to_local_file function."""
    
    def setup_method(self):
        """Create a temporary directory for each test."""
        self.test_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Clean up temporary directory after each test."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_save_simple_data(self):
        """Test saving simple JSON data to file."""
        data = {
            "case_id": "test-123",
            "status": "processed",
            "text": "Sample text"
        }
        filename = "test.json"
        
        result = save_to_local_file(self.test_dir, filename, data)
        
        assert result["status"] == "success"
        
        # Verify file was created
        file_path = os.path.join(self.test_dir, filename)
        assert os.path.exists(file_path)
        
        # Verify content
        with open(file_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        assert saved_data == data
    
    def test_save_with_indent(self):
        """Test that JSON is saved with indent=2."""
        data = {"key1": "value1", "key2": {"nested": "value2"}}
        filename = "indented.json"
        
        result = save_to_local_file(self.test_dir, filename, data)
        
        assert result["status"] == "success"
        
        # Read raw content to check formatting
        file_path = os.path.join(self.test_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verify indent=2 formatting
        assert '  "key1"' in content or '  "key2"' in content
    
    def test_create_directory_if_not_exists(self):
        """Test that output directory is created if it doesn't exist."""
        new_dir = os.path.join(self.test_dir, "subdir", "nested")
        data = {"test": "data"}
        filename = "test.json"
        
        # Directory should not exist yet
        assert not os.path.exists(new_dir)
        
        result = save_to_local_file(new_dir, filename, data)
        
        assert result["status"] == "success"
        assert os.path.exists(new_dir)
        assert os.path.exists(os.path.join(new_dir, filename))
    
    def test_save_complex_data(self):
        """Test saving complex nested JSON data."""
        data = {
            "case_id": "uuid-123",
            "timestamp": 1234567890,
            "metadata": {
                "sender": "NHS Trust",
                "confidence": 0.95,
                "page_count": 3
            },
            "extracted_text": "Long text content...",
            "status": "processed"
        }
        filename = "complex.json"
        
        result = save_to_local_file(self.test_dir, filename, data)
        
        assert result["status"] == "success"
        
        # Verify content
        file_path = os.path.join(self.test_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        assert saved_data == data
        assert saved_data["metadata"]["sender"] == "NHS Trust"
    
    def test_save_with_special_characters(self):
        """Test saving data with special characters and unicode."""
        data = {
            "text": "Special chars: £€¥ 你好 مرحبا",
            "symbols": "!@#$%^&*()",
            "quotes": 'He said "hello"'
        }
        filename = "special.json"
        
        result = save_to_local_file(self.test_dir, filename, data)
        
        assert result["status"] == "success"
        
        # Verify content
        file_path = os.path.join(self.test_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        assert saved_data == data
    
    def test_overwrite_existing_file(self):
        """Test that existing file is overwritten."""
        filename = "overwrite.json"
        file_path = os.path.join(self.test_dir, filename)
        
        # Create initial file
        initial_data = {"version": 1}
        save_to_local_file(self.test_dir, filename, initial_data)
        
        # Overwrite with new data
        new_data = {"version": 2}
        result = save_to_local_file(self.test_dir, filename, new_data)
        
        assert result["status"] == "success"
        
        # Verify new content
        with open(file_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        assert saved_data == new_data
        assert saved_data["version"] == 2
    
    def test_save_empty_dict(self):
        """Test saving an empty dictionary."""
        data = {}
        filename = "empty.json"
        
        result = save_to_local_file(self.test_dir, filename, data)
        
        assert result["status"] == "success"
        
        file_path = os.path.join(self.test_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        assert saved_data == {}
    
    def test_invalid_directory_path(self):
        """Test handling of invalid directory path."""
        # Use a path that cannot be created (e.g., under a file)
        file_path = os.path.join(self.test_dir, "file.txt")
        with open(file_path, 'w') as f:
            f.write("test")
        
        # Try to create directory under a file (should fail)
        invalid_dir = os.path.join(file_path, "subdir")
        data = {"test": "data"}
        
        result = save_to_local_file(invalid_dir, "test.json", data)
        
        assert result["status"] == "failed"
        assert "error" in result
    
    def test_non_serializable_data(self):
        """Test handling of non-JSON-serializable data."""
        # Create data with non-serializable object
        class CustomObject:
            pass
        
        data = {"object": CustomObject()}
        filename = "invalid.json"
        
        result = save_to_local_file(self.test_dir, filename, data)
        
        assert result["status"] == "failed"
        assert "error" in result
    
    def test_filename_with_subdirectory(self):
        """Test that filename can include subdirectory path."""
        data = {"test": "data"}
        filename = "subdir/test.json"
        
        result = save_to_local_file(self.test_dir, filename, data)
        
        assert result["status"] == "success"
        
        file_path = os.path.join(self.test_dir, filename)
        assert os.path.exists(file_path)
