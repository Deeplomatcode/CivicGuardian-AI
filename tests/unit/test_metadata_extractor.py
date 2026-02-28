"""
Unit tests for metadata_extractor module.
Tests sender detection, document classification, and metadata extraction.
"""

import pytest
from processing_function.metadata_extractor import (
    extract_metadata,
    detect_sender,
    classify_document_type
)


class TestDetectSender:
    """Tests for detect_sender function."""
    
    def test_nhs_trust_pattern(self):
        """Test detection of NHS Trust."""
        text = "This letter is from NHS Trust regarding your appointment."
        assert detect_sender(text) == "NHS Trust"
    
    def test_nhs_foundation_pattern(self):
        """Test detection of NHS Foundation."""
        text = "Contact NHS Foundation for more information."
        assert detect_sender(text) == "NHS Foundation"
    
    def test_nhs_england_pattern(self):
        """Test detection of NHS England."""
        text = "NHS England has updated their policy."
        assert detect_sender(text) == "NHS England"
    
    def test_city_council_pattern(self):
        """Test detection of City Council."""
        text = "City Council has received your application."
        assert detect_sender(text) == "City Council"
    
    def test_county_council_pattern(self):
        """Test detection of County Council."""
        text = "County Council social services department."
        assert detect_sender(text) == "County Council"
    
    def test_borough_council_pattern(self):
        """Test detection of Borough Council."""
        text = "Borough Council housing department."
        assert detect_sender(text) == "Borough Council"
    
    def test_district_council_pattern(self):
        """Test detection of District Council."""
        text = "District Council planning office."
        assert detect_sender(text) == "District Council"
    
    def test_dwp_full_name_pattern(self):
        """Test detection of Department for Work and Pensions."""
        text = "Department for Work and Pensions benefit decision."
        assert detect_sender(text) == "Department for Work and Pensions"
    
    def test_dwp_abbreviation_pattern(self):
        """Test detection of DWP abbreviation."""
        text = "DWP has reviewed your claim."
        assert detect_sender(text) == "DWP"
    
    def test_hmrc_pattern(self):
        """Test detection of HMRC."""
        text = "HMRC tax assessment for 2023."
        assert detect_sender(text) == "HMRC"
    
    def test_hmrc_full_name_pattern(self):
        """Test detection of Her Majesty's Revenue and Customs."""
        text = "Her Majesty's Revenue and Customs notice."
        assert detect_sender(text) == "Her Majesty's Revenue and Customs"
    
    def test_social_services_pattern(self):
        """Test detection of Social Services."""
        text = "Social Services assessment report."
        assert detect_sender(text) == "Social Services"
    
    def test_adult_social_care_pattern(self):
        """Test detection of Adult Social Care."""
        text = "Adult Social Care team will visit."
        assert detect_sender(text) == "Adult Social Care"
    
    def test_case_insensitive_matching(self):
        """Test that pattern matching is case-insensitive."""
        text_lower = "nhs trust appointment"
        text_upper = "NHS TRUST APPOINTMENT"
        text_mixed = "Nhs TrUsT appointment"
        
        assert detect_sender(text_lower) == "nhs trust"
        assert detect_sender(text_upper) == "NHS TRUST"
        assert detect_sender(text_mixed) == "Nhs TrUsT"
    
    def test_first_match_returned(self):
        """Test that first matched organization is returned when multiple present."""
        text = "NHS Trust and City Council joint letter."
        # NHS Trust pattern comes first in the patterns list
        assert detect_sender(text) == "NHS Trust"
    
    def test_no_pattern_found(self):
        """Test that None is returned when no organization pattern found."""
        text = "This is a personal letter from a friend."
        assert detect_sender(text) is None
    
    def test_empty_text(self):
        """Test that None is returned for empty text."""
        assert detect_sender("") is None
    
    def test_pattern_with_apostrophe_variation(self):
        """Test Her Majesty's with and without apostrophe."""
        text1 = "Her Majesty's Revenue and Customs"
        text2 = "Her Majestys Revenue and Customs"
        
        assert detect_sender(text1) == "Her Majesty's Revenue and Customs"
        assert detect_sender(text2) == "Her Majestys Revenue and Customs"


class TestClassifyDocumentType:
    """Tests for classify_document_type function."""
    
    def test_pdf_classified_as_letter(self):
        """Test that PDF files are classified as letter."""
        assert classify_document_type("pdf") == "letter"
    
    def test_image_classified_as_letter(self):
        """Test that image files are classified as letter."""
        assert classify_document_type("image") == "letter"
    
    def test_audio_classified_as_voicemail(self):
        """Test that audio files are classified as voicemail."""
        assert classify_document_type("audio") == "voicemail"
    
    def test_email_classified_as_email(self):
        """Test that email files are classified as email."""
        assert classify_document_type("email") == "email"
    
    def test_unknown_type_defaults_to_letter(self):
        """Test that unknown file types default to letter."""
        assert classify_document_type("unknown") == "letter"
        assert classify_document_type("video") == "letter"


class TestExtractMetadata:
    """Tests for extract_metadata function."""
    
    def test_complete_metadata_extraction(self):
        """Test complete metadata extraction with all fields."""
        text = "NHS Trust appointment letter"
        file_type = "pdf"
        extraction_result = {
            "confidence": 0.95,
            "page_count": 3
        }
        
        metadata = extract_metadata(text, file_type, extraction_result)
        
        assert metadata["sender"] == "NHS Trust"
        assert metadata["document_type"] == "letter"
        assert metadata["confidence"] == 0.95
        assert metadata["page_count"] == 3
        assert metadata["language"] == "en-GB"
    
    def test_metadata_with_no_sender(self):
        """Test metadata extraction when no sender is detected."""
        text = "Personal correspondence"
        file_type = "email"
        extraction_result = {
            "confidence": 1.0,
            "page_count": 1
        }
        
        metadata = extract_metadata(text, file_type, extraction_result)
        
        assert metadata["sender"] is None
        assert metadata["document_type"] == "email"
        assert metadata["confidence"] == 1.0
        assert metadata["page_count"] == 1
        assert metadata["language"] == "en-GB"
    
    def test_metadata_with_default_confidence(self):
        """Test metadata extraction with default confidence when not provided."""
        text = "DWP benefit letter"
        file_type = "image"
        extraction_result = {
            "page_count": 2
        }
        
        metadata = extract_metadata(text, file_type, extraction_result)
        
        assert metadata["sender"] == "DWP"
        assert metadata["document_type"] == "letter"
        assert metadata["confidence"] == 1.0  # Default value
        assert metadata["page_count"] == 2
        assert metadata["language"] == "en-GB"
    
    def test_metadata_with_default_page_count(self):
        """Test metadata extraction with default page count when not provided."""
        text = "HMRC tax notice"
        file_type = "audio"
        extraction_result = {
            "confidence": 0.87
        }
        
        metadata = extract_metadata(text, file_type, extraction_result)
        
        assert metadata["sender"] == "HMRC"
        assert metadata["document_type"] == "voicemail"
        assert metadata["confidence"] == 0.87
        assert metadata["page_count"] == 1  # Default value
        assert metadata["language"] == "en-GB"
    
    def test_metadata_language_always_en_gb(self):
        """Test that language is always set to en-GB."""
        text = "Social Services report"
        file_type = "pdf"
        extraction_result = {"confidence": 0.9, "page_count": 5}
        
        metadata = extract_metadata(text, file_type, extraction_result)
        
        assert metadata["language"] == "en-GB"
    
    def test_metadata_with_empty_extraction_result(self):
        """Test metadata extraction with empty extraction result dict."""
        text = "City Council notice"
        file_type = "email"
        extraction_result = {}
        
        metadata = extract_metadata(text, file_type, extraction_result)
        
        assert metadata["sender"] == "City Council"
        assert metadata["document_type"] == "email"
        assert metadata["confidence"] == 1.0  # Default
        assert metadata["page_count"] == 1  # Default
        assert metadata["language"] == "en-GB"
