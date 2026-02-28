"""
Unit tests for file_detector module.
Tests file type detection from S3 object keys.
"""
import pytest
from processing_function.file_detector import detect_file_type


class TestDetectFileType:
    """Test suite for detect_file_type function."""
    
    # PDF files (Requirement 2.1)
    def test_pdf_lowercase(self):
        """Test PDF file with lowercase extension."""
        file_type, extension = detect_file_type("document.pdf")
        assert file_type == "pdf"
        assert extension == "pdf"
    
    def test_pdf_uppercase(self):
        """Test PDF file with uppercase extension (case-insensitive)."""
        file_type, extension = detect_file_type("document.PDF")
        assert file_type == "pdf"
        assert extension == "pdf"
    
    def test_pdf_mixed_case(self):
        """Test PDF file with mixed case extension."""
        file_type, extension = detect_file_type("document.Pdf")
        assert file_type == "pdf"
        assert extension == "pdf"
    
    def test_pdf_with_path(self):
        """Test PDF file with S3 path prefix."""
        file_type, extension = detect_file_type("path/to/document.pdf")
        assert file_type == "pdf"
        assert extension == "pdf"
    
    # Image files (Requirement 2.2)
    def test_jpg_extension(self):
        """Test JPG image file."""
        file_type, extension = detect_file_type("photo.jpg")
        assert file_type == "image"
        assert extension == "jpg"
    
    def test_jpeg_extension(self):
        """Test JPEG image file."""
        file_type, extension = detect_file_type("photo.jpeg")
        assert file_type == "image"
        assert extension == "jpeg"
    
    def test_png_extension(self):
        """Test PNG image file."""
        file_type, extension = detect_file_type("screenshot.png")
        assert file_type == "image"
        assert extension == "png"
    
    def test_tiff_extension(self):
        """Test TIFF image file."""
        file_type, extension = detect_file_type("scan.tiff")
        assert file_type == "image"
        assert extension == "tiff"
    
    def test_image_uppercase(self):
        """Test image file with uppercase extension."""
        file_type, extension = detect_file_type("photo.JPG")
        assert file_type == "image"
        assert extension == "jpg"
    
    # Audio files (Requirement 2.3)
    def test_mp3_extension(self):
        """Test MP3 audio file."""
        file_type, extension = detect_file_type("voicemail.mp3")
        assert file_type == "audio"
        assert extension == "mp3"
    
    def test_wav_extension(self):
        """Test WAV audio file."""
        file_type, extension = detect_file_type("recording.wav")
        assert file_type == "audio"
        assert extension == "wav"
    
    def test_m4a_extension(self):
        """Test M4A audio file."""
        file_type, extension = detect_file_type("message.m4a")
        assert file_type == "audio"
        assert extension == "m4a"
    
    def test_audio_uppercase(self):
        """Test audio file with uppercase extension."""
        file_type, extension = detect_file_type("voicemail.MP3")
        assert file_type == "audio"
        assert extension == "mp3"
    
    # Email files (Requirement 2.4)
    def test_txt_extension(self):
        """Test TXT email file."""
        file_type, extension = detect_file_type("email.txt")
        assert file_type == "email"
        assert extension == "txt"
    
    def test_html_extension(self):
        """Test HTML email file."""
        file_type, extension = detect_file_type("email.html")
        assert file_type == "email"
        assert extension == "html"
    
    def test_email_uppercase(self):
        """Test email file with uppercase extension."""
        file_type, extension = detect_file_type("email.TXT")
        assert file_type == "email"
        assert extension == "txt"
    
    # Unsupported files (Requirement 2.5)
    def test_unsupported_docx(self):
        """Test unsupported DOCX file."""
        file_type, extension = detect_file_type("document.docx")
        assert file_type == "unsupported"
        assert extension == "docx"
    
    def test_unsupported_xlsx(self):
        """Test unsupported XLSX file."""
        file_type, extension = detect_file_type("spreadsheet.xlsx")
        assert file_type == "unsupported"
        assert extension == "xlsx"
    
    def test_unsupported_zip(self):
        """Test unsupported ZIP file."""
        file_type, extension = detect_file_type("archive.zip")
        assert file_type == "unsupported"
        assert extension == "zip"
    
    def test_unsupported_no_extension(self):
        """Test file without extension."""
        file_type, extension = detect_file_type("filename")
        assert file_type == "unsupported"
        assert extension == "filename"
    
    # Edge cases
    def test_multiple_dots_in_filename(self):
        """Test filename with multiple dots."""
        file_type, extension = detect_file_type("my.document.name.pdf")
        assert file_type == "pdf"
        assert extension == "pdf"
    
    def test_complex_s3_path(self):
        """Test complex S3 path with multiple directories."""
        file_type, extension = detect_file_type("uploads/2024/01/15/document.pdf")
        assert file_type == "pdf"
        assert extension == "pdf"
    
    def test_filename_with_spaces(self):
        """Test filename with spaces (URL encoded in real S3)."""
        file_type, extension = detect_file_type("my document.pdf")
        assert file_type == "pdf"
        assert extension == "pdf"
