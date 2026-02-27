# Email text extraction module
# Extracts text directly from email files (txt and html)

from html.parser import HTMLParser


def extract(file_path, extension):
    """
    Extracts text directly from email files (txt or html).
    
    Phase 1: Works with local files
    Phase 3: Will be updated to work with S3 (bucket, key parameters)
    
    Args:
        file_path: Path to the local file
        extension: File extension (txt or html)
    
    Returns:
        dict: {status, text, confidence, page_count, error}
    """
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Process based on extension
        if extension == 'html':
            text = strip_html_tags(content)
        else:
            text = content
        
        return {
            "status": "success",
            "text": text.strip(),
            "confidence": 1.0,  # Direct extraction has perfect confidence
            "page_count": 1
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "error": f"Email extraction failed: {type(e).__name__}"
        }


def strip_html_tags(html_content):
    """
    Strips HTML tags and returns plain text.
    
    Args:
        html_content: HTML string
    
    Returns:
        str: Plain text with HTML tags removed
    """
    class HTMLTextExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text = []
        
        def handle_data(self, data):
            self.text.append(data)
        
        def get_text(self):
            return ''.join(self.text)
    
    parser = HTMLTextExtractor()
    parser.feed(html_content)
    return parser.get_text()
