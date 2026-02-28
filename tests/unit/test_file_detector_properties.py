"""
Property-based tests for file_detector module.
Uses Hypothesis to generate random filenames and verify correct routing.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**
"""
from hypothesis import given, strategies as st
from processing_function.file_detector import detect_file_type


# Define supported extensions for each file type
PDF_EXTENSIONS = ['pdf']
IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'tiff']
AUDIO_EXTENSIONS = ['mp3', 'wav', 'm4a']
EMAIL_EXTENSIONS = ['txt', 'html']
UNSUPPORTED_EXTENSIONS = ['docx', 'xlsx', 'zip', 'exe', 'bin', 'dat', 'csv', 'json', 'xml']

# Strategy for generating random filenames
filename_strategy = st.text(
    alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=65, max_codepoint=122),
    min_size=1,
    max_size=50
).filter(lambda x: '.' not in x)

# Strategy for generating S3 paths (optional)
path_strategy = st.lists(
    st.text(
        alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'), min_codepoint=65, max_codepoint=122),
        min_size=1,
        max_size=20
    ).filter(lambda x: '.' not in x),
    min_size=0,
    max_size=5
)


class TestFileTypeRoutingProperty:
    """
    Property 1: File Type Routing
    **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**
    
    Property: For any filename with a supported extension, detect_file_type
    must correctly route it to the appropriate file type category.
    """
    
    @given(
        filename=filename_strategy,
        path_components=path_strategy
    )
    def test_pdf_routing(self, filename, path_components):
        """
        Property: All files with .pdf extension (case-insensitive) 
        must be routed to 'pdf' type.
        **Validates: Requirements 2.1**
        """
        # Generate random case variation of 'pdf'
        extension_cases = ['pdf', 'PDF', 'Pdf', 'pDf', 'pdF', 'PdF', 'pDF', 'PDf']
        for ext_case in extension_cases:
            # Build S3 key with optional path
            if path_components:
                object_key = '/'.join(path_components) + '/' + filename + '.' + ext_case
            else:
                object_key = filename + '.' + ext_case
            
            file_type, extension = detect_file_type(object_key)
            
            assert file_type == 'pdf', f"Expected 'pdf' but got '{file_type}' for {object_key}"
            assert extension == 'pdf', f"Expected lowercase 'pdf' but got '{extension}'"
    
    @given(
        filename=filename_strategy,
        path_components=path_strategy,
        image_ext=st.sampled_from(IMAGE_EXTENSIONS)
    )
    def test_image_routing(self, filename, path_components, image_ext):
        """
        Property: All files with image extensions (jpg, jpeg, png, tiff)
        must be routed to 'image' type.
        **Validates: Requirements 2.2**
        """
        # Test with various case combinations
        extension_cases = [
            image_ext.lower(),
            image_ext.upper(),
            image_ext.capitalize()
        ]
        
        for ext_case in extension_cases:
            # Build S3 key with optional path
            if path_components:
                object_key = '/'.join(path_components) + '/' + filename + '.' + ext_case
            else:
                object_key = filename + '.' + ext_case
            
            file_type, extension = detect_file_type(object_key)
            
            assert file_type == 'image', f"Expected 'image' but got '{file_type}' for {object_key}"
            assert extension == image_ext.lower(), f"Expected '{image_ext.lower()}' but got '{extension}'"
    
    @given(
        filename=filename_strategy,
        path_components=path_strategy,
        audio_ext=st.sampled_from(AUDIO_EXTENSIONS)
    )
    def test_audio_routing(self, filename, path_components, audio_ext):
        """
        Property: All files with audio extensions (mp3, wav, m4a)
        must be routed to 'audio' type.
        **Validates: Requirements 2.3**
        """
        # Test with various case combinations
        extension_cases = [
            audio_ext.lower(),
            audio_ext.upper(),
            audio_ext.capitalize()
        ]
        
        for ext_case in extension_cases:
            # Build S3 key with optional path
            if path_components:
                object_key = '/'.join(path_components) + '/' + filename + '.' + ext_case
            else:
                object_key = filename + '.' + ext_case
            
            file_type, extension = detect_file_type(object_key)
            
            assert file_type == 'audio', f"Expected 'audio' but got '{file_type}' for {object_key}"
            assert extension == audio_ext.lower(), f"Expected '{audio_ext.lower()}' but got '{extension}'"
    
    @given(
        filename=filename_strategy,
        path_components=path_strategy,
        email_ext=st.sampled_from(EMAIL_EXTENSIONS)
    )
    def test_email_routing(self, filename, path_components, email_ext):
        """
        Property: All files with email extensions (txt, html)
        must be routed to 'email' type.
        **Validates: Requirements 2.4**
        """
        # Test with various case combinations
        extension_cases = [
            email_ext.lower(),
            email_ext.upper(),
            email_ext.capitalize()
        ]
        
        for ext_case in extension_cases:
            # Build S3 key with optional path
            if path_components:
                object_key = '/'.join(path_components) + '/' + filename + '.' + ext_case
            else:
                object_key = filename + '.' + ext_case
            
            file_type, extension = detect_file_type(object_key)
            
            assert file_type == 'email', f"Expected 'email' but got '{file_type}' for {object_key}"
            assert extension == email_ext.lower(), f"Expected '{email_ext.lower()}' but got '{extension}'"
    
    @given(
        filename=filename_strategy,
        path_components=path_strategy,
        unsupported_ext=st.sampled_from(UNSUPPORTED_EXTENSIONS)
    )
    def test_unsupported_routing(self, filename, path_components, unsupported_ext):
        """
        Property: All files with unsupported extensions must be routed
        to 'unsupported' type.
        **Validates: Requirements 2.5**
        """
        # Build S3 key with optional path
        if path_components:
            object_key = '/'.join(path_components) + '/' + filename + '.' + unsupported_ext
        else:
            object_key = filename + '.' + unsupported_ext
        
        file_type, extension = detect_file_type(object_key)
        
        assert file_type == 'unsupported', f"Expected 'unsupported' but got '{file_type}' for {object_key}"
        assert extension == unsupported_ext.lower(), f"Expected '{unsupported_ext.lower()}' but got '{extension}'"
    
    @given(
        filename=filename_strategy,
        path_components=path_strategy
    )
    def test_no_extension_unsupported(self, filename, path_components):
        """
        Property: Files without extensions must be routed to 'unsupported' type.
        **Validates: Requirements 2.5**
        """
        # Build S3 key without extension
        if path_components:
            object_key = '/'.join(path_components) + '/' + filename
        else:
            object_key = filename
        
        file_type, extension = detect_file_type(object_key)
        
        assert file_type == 'unsupported', f"Expected 'unsupported' but got '{file_type}' for {object_key}"
    
    @given(
        base_filename=filename_strategy,
        num_dots=st.integers(min_value=1, max_value=5),
        final_ext=st.sampled_from(PDF_EXTENSIONS + IMAGE_EXTENSIONS + AUDIO_EXTENSIONS + EMAIL_EXTENSIONS)
    )
    def test_multiple_dots_routing(self, base_filename, num_dots, final_ext):
        """
        Property: For filenames with multiple dots, only the final extension
        should determine the file type.
        **Validates: Requirements 2.1, 2.2, 2.3, 2.4**
        """
        # Create filename with multiple dots
        parts = [base_filename] + ['part'] * num_dots
        object_key = '.'.join(parts) + '.' + final_ext
        
        file_type, extension = detect_file_type(object_key)
        
        # Determine expected file type based on extension
        if final_ext in PDF_EXTENSIONS:
            expected_type = 'pdf'
        elif final_ext in IMAGE_EXTENSIONS:
            expected_type = 'image'
        elif final_ext in AUDIO_EXTENSIONS:
            expected_type = 'audio'
        elif final_ext in EMAIL_EXTENSIONS:
            expected_type = 'email'
        else:
            expected_type = 'unsupported'
        
        assert file_type == expected_type, f"Expected '{expected_type}' but got '{file_type}' for {object_key}"
        assert extension == final_ext.lower(), f"Expected '{final_ext.lower()}' but got '{extension}'"
