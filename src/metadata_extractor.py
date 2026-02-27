"""
Metadata extraction module.
Extracts metadata including sender detection and document classification.
"""

import re


def extract_metadata(text, file_type, extraction_result):
    """
    Extracts metadata including sender detection and document classification.
    
    Args:
        text: Extracted text content
        file_type: Type of file (pdf, image, audio, email)
        extraction_result: Result dict from text extraction
    
    Returns:
        dict: {sender, document_type, confidence, page_count, language}
    """
    return {
        "sender": detect_sender(text),
        "document_type": classify_document_type(file_type),
        "confidence": extraction_result.get("confidence", 1.0),
        "page_count": extraction_result.get("page_count", 1),
        "language": "en-GB"
    }


def detect_sender(text):
    """
    Detects sender organization from text using pattern matching.
    Returns first match or None.
    
    Args:
        text: Extracted text content to search for organization patterns
    
    Returns:
        str or None: First matched organization name or None if no match found
    """
    # Known organization patterns (case-insensitive)
    patterns = [
        r'\bNHS\s+(?:Trust|Foundation|England)\b',
        r'\b(?:City|County|Borough|District)\s+Council\b',
        r'\bDepartment\s+for\s+Work\s+and\s+Pensions\b',
        r'\bDWP\b',
        r'\bHMRC\b',
        r'\bHer\s+Majesty\'?s\s+Revenue\s+and\s+Customs\b',
        r'\bSocial\s+Services\b',
        r'\bAdult\s+Social\s+Care\b'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return None


def classify_document_type(file_type):
    """
    Classifies document type based on file type.
    
    Args:
        file_type: Type of file (pdf, image, audio, email)
    
    Returns:
        str: Document type classification (letter, voicemail, or email)
    """
    type_map = {
        "pdf": "letter",
        "image": "letter",
        "audio": "voicemail",
        "email": "email"
    }
    return type_map.get(file_type, "letter")
