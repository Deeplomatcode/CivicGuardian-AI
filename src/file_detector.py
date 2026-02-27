# File type detection module
# Detects file types from S3 object keys for routing to appropriate processors


def detect_file_type(object_key):
    """
    Detects file type from S3 object key extension.
    
    Args:
        object_key: S3 object key (path/to/file.ext)
    
    Returns:
        tuple: (file_type, extension)
            file_type: pdf, image, audio, email, unsupported
            extension: lowercase file extension
    """
    # Extract extension (case-insensitive)
    extension = object_key.lower().split('.')[-1]
    
    # PDF files
    if extension == 'pdf':
        return ('pdf', extension)
    
    # Image files
    if extension in ['jpg', 'jpeg', 'png', 'tiff']:
        return ('image', extension)
    
    # Audio files
    if extension in ['mp3', 'wav', 'm4a']:
        return ('audio', extension)
    
    # Email files
    if extension in ['txt', 'html']:
        return ('email', extension)
    
    # Unsupported
    return ('unsupported', extension)
