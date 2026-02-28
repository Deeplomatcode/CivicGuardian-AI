"""Unit tests for email_extractor module."""

import os
import tempfile
import pytest
from processing_function.text_extractors.email_extractor import extract, strip_html_tags


class TestEmailExtractor:
    """Test suite for email text extraction."""
    
    def test_extract_plain_text(self):
        """Test extraction from plain text file."""
        # Create temporary text file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("This is a plain text email.\nWith multiple lines.")
            temp_path = f.name
        
        try:
            result = extract(temp_path, 'txt')
            
            assert result["status"] == "success"
            assert result["text"] == "This is a plain text email.\nWith multiple lines."
            assert result["confidence"] == 1.0
            assert result["page_count"] == 1
        finally:
            os.unlink(temp_path)
    
    def test_extract_html(self):
        """Test extraction from HTML file with tag stripping."""
        html_content = """
        <html>
            <head><title>Email</title></head>
            <body>
                <h1>Hello</h1>
                <p>This is an <strong>HTML</strong> email.</p>
            </body>
        </html>
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_content)
            temp_path = f.name
        
        try:
            result = extract(temp_path, 'html')
            
            assert result["status"] == "success"
            # HTML tags should be stripped
            assert "<html>" not in result["text"]
            assert "<p>" not in result["text"]
            assert "Hello" in result["text"]
            assert "HTML" in result["text"]
            assert "email" in result["text"]
            assert result["confidence"] == 1.0
            assert result["page_count"] == 1
        finally:
            os.unlink(temp_path)
    
    def test_extract_empty_file(self):
        """Test extraction from empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("")
            temp_path = f.name
        
        try:
            result = extract(temp_path, 'txt')
            
            assert result["status"] == "success"
            assert result["text"] == ""
            assert result["confidence"] == 1.0
            assert result["page_count"] == 1
        finally:
            os.unlink(temp_path)
    
    def test_extract_file_not_found(self):
        """Test extraction with non-existent file."""
        result = extract("/nonexistent/file.txt", 'txt')
        
        assert result["status"] == "failed"
        assert "error" in result
        assert "FileNotFoundError" in result["error"]
    
    def test_strip_html_tags_simple(self):
        """Test HTML tag stripping with simple HTML."""
        html = "<p>Hello <strong>world</strong>!</p>"
        text = strip_html_tags(html)
        
        assert text == "Hello world!"
        assert "<p>" not in text
        assert "<strong>" not in text
    
    def test_strip_html_tags_complex(self):
        """Test HTML tag stripping with complex HTML."""
        html = """
        <div class="container">
            <h1>Title</h1>
            <p>Paragraph with <a href="link">link</a>.</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
        </div>
        """
        text = strip_html_tags(html)
        
        assert "Title" in text
        assert "Paragraph" in text
        assert "link" in text
        assert "Item 1" in text
        assert "Item 2" in text
        assert "<div>" not in text
        assert "<a" not in text
    
    def test_extract_special_characters(self):
        """Test extraction with special characters and encoding."""
        content = "Email with special chars: £€¥ and unicode: 你好"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = extract(temp_path, 'txt')
            
            assert result["status"] == "success"
            assert "£€¥" in result["text"]
            assert "你好" in result["text"]
        finally:
            os.unlink(temp_path)
