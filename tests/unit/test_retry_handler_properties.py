"""
Property-based tests for retry_handler module.
Uses Hypothesis to verify exponential backoff behavior with throttling errors.

**Validates: Requirements 3.5, 4.5, 14.1, 14.5**
"""
import time
from unittest.mock import Mock, patch
from hypothesis import given, strategies as st, settings
from botocore.exceptions import ClientError
from processing_function.retry_handler import exponential_backoff_retry


class TestExponentialBackoffProperty:
    """
    Property 4: Exponential Backoff Retry
    **Validates: Requirements 3.5, 4.5, 14.1, 14.5**
    
    Property: For any AWS service throttling error, the system SHALL retry
    with exponential backoff using wait times of 1 second, 2 seconds, and
    4 seconds for attempts 1, 2, and 3 respectively.
    """
    
    @given(
        service_name=st.sampled_from(['Textract', 'Transcribe', 'DynamoDB', 'S3']),
        throttle_error=st.sampled_from(['ThrottlingException', 'ProvisionedThroughputExceededException'])
    )
    @settings(max_examples=100)
    def test_exponential_backoff_timing(self, service_name, throttle_error):
        """
        Property: Retry wait times must follow exponential backoff pattern: 1s, 2s, 4s.
        **Validates: Requirements 14.1, 14.2, 14.3**
        """
        # Create a mock API call that fails with throttling errors
        call_count = 0
        call_times = []
        
        def mock_api_call():
            nonlocal call_count
            call_times.append(time.time())
            call_count += 1
            
            # Fail all attempts with throttling error
            error_response = {
                'Error': {
                    'Code': throttle_error,
                    'Message': 'Rate exceeded'
                }
            }
            raise ClientError(error_response, 'TestOperation')
        
        # Execute with exponential backoff
        start_time = time.time()
        try:
            with patch('time.sleep') as mock_sleep:
                exponential_backoff_retry(
                    api_call=mock_api_call,
                    max_retries=3,
                    initial_wait=1,
                    service_name=service_name
                )
        except ClientError:
            # Expected to fail after all retries
            pass
        
        # Verify retry count
        assert call_count == 4, f"Expected 4 calls (1 initial + 3 retries), got {call_count}"
        
        # Verify sleep was called with correct wait times
        assert mock_sleep.call_count == 3, f"Expected 3 sleep calls, got {mock_sleep.call_count}"
        
        # Extract sleep durations
        sleep_durations = [call[0][0] for call in mock_sleep.call_args_list]
        
        # Verify exponential backoff pattern: 1s, 2s, 4s
        assert sleep_durations[0] == 1, f"First retry should wait 1s, got {sleep_durations[0]}s"
        assert sleep_durations[1] == 2, f"Second retry should wait 2s, got {sleep_durations[1]}s"
        assert sleep_durations[2] == 4, f"Third retry should wait 4s, got {sleep_durations[2]}s"
    
    @given(
        service_name=st.sampled_from(['Textract', 'Transcribe']),
        throttle_error=st.sampled_from(['ThrottlingException', 'ProvisionedThroughputExceededException']),
        success_on_attempt=st.integers(min_value=1, max_value=3)
    )
    @settings(max_examples=100)
    def test_retry_success_before_exhaustion(self, service_name, throttle_error, success_on_attempt):
        """
        Property: If API call succeeds before max retries, return immediately.
        **Validates: Requirements 3.5, 4.5**
        """
        call_count = 0
        expected_response = {'Status': 'Success', 'Data': 'test_data'}
        
        def mock_api_call():
            nonlocal call_count
            call_count += 1
            
            if call_count < success_on_attempt:
                # Fail with throttling error
                error_response = {
                    'Error': {
                        'Code': throttle_error,
                        'Message': 'Rate exceeded'
                    }
                }
                raise ClientError(error_response, 'TestOperation')
            else:
                # Succeed on the specified attempt
                return expected_response
        
        # Execute with exponential backoff
        with patch('time.sleep'):
            result = exponential_backoff_retry(
                api_call=mock_api_call,
                max_retries=3,
                initial_wait=1,
                service_name=service_name
            )
        
        # Verify success
        assert result == expected_response, f"Expected {expected_response}, got {result}"
        assert call_count == success_on_attempt, f"Expected {success_on_attempt} calls, got {call_count}"
    
    @given(
        service_name=st.sampled_from(['Textract', 'Transcribe']),
        non_throttle_error=st.sampled_from([
            'InvalidParameterException',
            'ResourceNotFoundException',
            'AccessDeniedException',
            'ValidationException',
            'InternalServerError'
        ])
    )
    @settings(max_examples=100)
    def test_no_retry_on_non_throttling_errors(self, service_name, non_throttle_error):
        """
        Property: Non-throttling errors must not trigger retries.
        **Validates: Requirements 14.1, 14.5**
        """
        call_count = 0
        
        def mock_api_call():
            nonlocal call_count
            call_count += 1
            
            # Fail with non-throttling error
            error_response = {
                'Error': {
                    'Code': non_throttle_error,
                    'Message': 'Non-throttling error'
                }
            }
            raise ClientError(error_response, 'TestOperation')
        
        # Execute with exponential backoff
        try:
            with patch('time.sleep') as mock_sleep:
                exponential_backoff_retry(
                    api_call=mock_api_call,
                    max_retries=3,
                    initial_wait=1,
                    service_name=service_name
                )
        except ClientError as e:
            # Expected to fail immediately
            assert e.response['Error']['Code'] == non_throttle_error
        
        # Verify no retries occurred
        assert call_count == 1, f"Expected 1 call (no retries), got {call_count}"
        assert mock_sleep.call_count == 0, f"Expected 0 sleep calls, got {mock_sleep.call_count}"
    
    @given(
        service_name=st.sampled_from(['Textract', 'Transcribe']),
        throttle_error=st.sampled_from(['ThrottlingException', 'ProvisionedThroughputExceededException'])
    )
    @settings(max_examples=100)
    def test_max_retries_exhaustion(self, service_name, throttle_error):
        """
        Property: After max_retries exhausted, raise the throttling exception.
        **Validates: Requirements 14.4**
        """
        call_count = 0
        
        def mock_api_call():
            nonlocal call_count
            call_count += 1
            
            # Always fail with throttling error
            error_response = {
                'Error': {
                    'Code': throttle_error,
                    'Message': 'Rate exceeded'
                }
            }
            raise ClientError(error_response, 'TestOperation')
        
        # Execute with exponential backoff
        exception_raised = False
        try:
            with patch('time.sleep'):
                exponential_backoff_retry(
                    api_call=mock_api_call,
                    max_retries=3,
                    initial_wait=1,
                    service_name=service_name
                )
        except ClientError as e:
            exception_raised = True
            assert e.response['Error']['Code'] == throttle_error
        
        # Verify exception was raised after all retries
        assert exception_raised, "Expected ClientError to be raised after retries exhausted"
        assert call_count == 4, f"Expected 4 calls (1 initial + 3 retries), got {call_count}"
    
    @given(
        service_name=st.sampled_from(['Textract', 'Transcribe']),
        max_retries=st.integers(min_value=1, max_value=5),
        initial_wait=st.integers(min_value=1, max_value=3)
    )
    @settings(max_examples=100)
    def test_configurable_retry_parameters(self, service_name, max_retries, initial_wait):
        """
        Property: Retry logic must respect configurable max_retries and initial_wait parameters.
        **Validates: Requirements 14.1**
        """
        call_count = 0
        
        def mock_api_call():
            nonlocal call_count
            call_count += 1
            
            # Always fail with throttling error
            error_response = {
                'Error': {
                    'Code': 'ThrottlingException',
                    'Message': 'Rate exceeded'
                }
            }
            raise ClientError(error_response, 'TestOperation')
        
        # Execute with exponential backoff
        try:
            with patch('time.sleep') as mock_sleep:
                exponential_backoff_retry(
                    api_call=mock_api_call,
                    max_retries=max_retries,
                    initial_wait=initial_wait,
                    service_name=service_name
                )
        except ClientError:
            # Expected to fail after all retries
            pass
        
        # Verify retry count matches max_retries
        assert call_count == max_retries + 1, f"Expected {max_retries + 1} calls, got {call_count}"
        
        # Verify sleep was called max_retries times
        assert mock_sleep.call_count == max_retries, f"Expected {max_retries} sleep calls, got {mock_sleep.call_count}"
        
        # Verify first wait time matches initial_wait
        if mock_sleep.call_count > 0:
            first_wait = mock_sleep.call_args_list[0][0][0]
            assert first_wait == initial_wait, f"First wait should be {initial_wait}s, got {first_wait}s"
            
            # Verify exponential growth pattern
            for i in range(1, min(mock_sleep.call_count, 3)):
                expected_wait = initial_wait * (2 ** i)
                actual_wait = mock_sleep.call_args_list[i][0][0]
                assert actual_wait == expected_wait, f"Wait {i+1} should be {expected_wait}s, got {actual_wait}s"
    
    @given(
        service_name=st.sampled_from(['Textract', 'Transcribe'])
    )
    @settings(max_examples=100)
    def test_non_boto3_exceptions_not_retried(self, service_name):
        """
        Property: Non-boto3 exceptions (e.g., ValueError, TypeError) must not trigger retries.
        **Validates: Requirements 14.1**
        """
        call_count = 0
        
        def mock_api_call():
            nonlocal call_count
            call_count += 1
            raise ValueError("Invalid parameter")
        
        # Execute with exponential backoff
        exception_raised = False
        try:
            with patch('time.sleep') as mock_sleep:
                exponential_backoff_retry(
                    api_call=mock_api_call,
                    max_retries=3,
                    initial_wait=1,
                    service_name=service_name
                )
        except ValueError:
            exception_raised = True
        
        # Verify exception was raised immediately without retries
        assert exception_raised, "Expected ValueError to be raised"
        assert call_count == 1, f"Expected 1 call (no retries), got {call_count}"
        assert mock_sleep.call_count == 0, f"Expected 0 sleep calls, got {mock_sleep.call_count}"
