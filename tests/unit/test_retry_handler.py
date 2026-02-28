"""
Unit tests for retry_handler module.
Tests exponential backoff retry logic for AWS service calls.
"""
import pytest
import time
from unittest.mock import Mock, patch
from botocore.exceptions import ClientError
from processing_function.retry_handler import exponential_backoff_retry


class TestExponentialBackoffRetry:
    """Test suite for exponential_backoff_retry function."""
    
    # Test successful call on first attempt
    def test_successful_first_attempt(self):
        """Test API call succeeds on first attempt without retry."""
        # Create mock API call that succeeds
        mock_api_call = Mock(return_value={"status": "success"})
        
        # Execute with retry logic
        result = exponential_backoff_retry(
            api_call=mock_api_call,
            max_retries=3,
            initial_wait=1,
            service_name="TestService"
        )
        
        # Assert call succeeded and was only called once
        assert result == {"status": "success"}
        assert mock_api_call.call_count == 1
    
    # Test retry with throttling errors (1s, 2s, 4s waits)
    def test_retry_with_throttling_exception(self):
        """Test retry logic with ThrottlingException and exponential backoff."""
        # Create mock that fails twice with throttling, then succeeds
        mock_api_call = Mock()
        throttling_error = ClientError(
            error_response={'Error': {'Code': 'ThrottlingException'}},
            operation_name='TestOperation'
        )
        mock_api_call.side_effect = [
            throttling_error,  # First attempt fails
            throttling_error,  # Second attempt fails
            {"status": "success"}  # Third attempt succeeds
        ]
        
        # Track sleep times
        sleep_times = []
        with patch('time.sleep', side_effect=lambda x: sleep_times.append(x)):
            result = exponential_backoff_retry(
                api_call=mock_api_call,
                max_retries=3,
                initial_wait=1,
                service_name="Textract"
            )
        
        # Assert call eventually succeeded
        assert result == {"status": "success"}
        assert mock_api_call.call_count == 3
        
        # Assert exponential backoff: 1s, 2s
        assert sleep_times == [1, 2]
    
    def test_retry_with_provisioned_throughput_exception(self):
        """Test retry logic with ProvisionedThroughputExceededException."""
        # Create mock that fails once with throughput error, then succeeds
        mock_api_call = Mock()
        throughput_error = ClientError(
            error_response={'Error': {'Code': 'ProvisionedThroughputExceededException'}},
            operation_name='TestOperation'
        )
        mock_api_call.side_effect = [
            throughput_error,  # First attempt fails
            {"status": "success"}  # Second attempt succeeds
        ]
        
        # Track sleep times
        sleep_times = []
        with patch('time.sleep', side_effect=lambda x: sleep_times.append(x)):
            result = exponential_backoff_retry(
                api_call=mock_api_call,
                max_retries=3,
                initial_wait=1,
                service_name="Transcribe"
            )
        
        # Assert call eventually succeeded
        assert result == {"status": "success"}
        assert mock_api_call.call_count == 2
        
        # Assert waited 1 second before retry
        assert sleep_times == [1]
    
    def test_exponential_backoff_timing(self):
        """Test that exponential backoff follows 1s, 2s, 4s pattern."""
        # Create mock that fails 3 times with throttling, then succeeds
        mock_api_call = Mock()
        throttling_error = ClientError(
            error_response={'Error': {'Code': 'ThrottlingException'}},
            operation_name='TestOperation'
        )
        mock_api_call.side_effect = [
            throttling_error,  # Attempt 1 fails
            throttling_error,  # Attempt 2 fails
            throttling_error,  # Attempt 3 fails
            {"status": "success"}  # Attempt 4 succeeds
        ]
        
        # Track sleep times
        sleep_times = []
        with patch('time.sleep', side_effect=lambda x: sleep_times.append(x)):
            result = exponential_backoff_retry(
                api_call=mock_api_call,
                max_retries=3,
                initial_wait=1,
                service_name="Textract"
            )
        
        # Assert exponential backoff: 1s, 2s, 4s
        assert sleep_times == [1, 2, 4]
        assert mock_api_call.call_count == 4
    
    # Test max retries exhaustion
    def test_max_retries_exhausted(self):
        """Test that exception is raised after max retries exhausted."""
        # Create mock that always fails with throttling
        mock_api_call = Mock()
        throttling_error = ClientError(
            error_response={'Error': {'Code': 'ThrottlingException'}},
            operation_name='TestOperation'
        )
        mock_api_call.side_effect = throttling_error
        
        # Track sleep times
        sleep_times = []
        with patch('time.sleep', side_effect=lambda x: sleep_times.append(x)):
            # Assert exception is raised after max retries
            with pytest.raises(ClientError) as exc_info:
                exponential_backoff_retry(
                    api_call=mock_api_call,
                    max_retries=3,
                    initial_wait=1,
                    service_name="Textract"
                )
        
        # Assert correct error code
        assert exc_info.value.response['Error']['Code'] == 'ThrottlingException'
        
        # Assert retried 3 times (4 total attempts)
        assert mock_api_call.call_count == 4
        
        # Assert exponential backoff: 1s, 2s, 4s
        assert sleep_times == [1, 2, 4]
    
    # Test non-throttling errors (no retry)
    def test_non_throttling_error_no_retry(self):
        """Test that non-throttling errors are not retried."""
        # Create mock that fails with non-throttling error
        mock_api_call = Mock()
        access_denied_error = ClientError(
            error_response={'Error': {'Code': 'AccessDeniedException'}},
            operation_name='TestOperation'
        )
        mock_api_call.side_effect = access_denied_error
        
        # Track sleep times
        sleep_times = []
        with patch('time.sleep', side_effect=lambda x: sleep_times.append(x)):
            # Assert exception is raised immediately without retry
            with pytest.raises(ClientError) as exc_info:
                exponential_backoff_retry(
                    api_call=mock_api_call,
                    max_retries=3,
                    initial_wait=1,
                    service_name="Textract"
                )
        
        # Assert correct error code
        assert exc_info.value.response['Error']['Code'] == 'AccessDeniedException'
        
        # Assert only called once (no retries)
        assert mock_api_call.call_count == 1
        
        # Assert no sleep occurred
        assert sleep_times == []
    
    def test_non_client_error_no_retry(self):
        """Test that non-ClientError exceptions are not retried."""
        # Create mock that raises generic exception
        mock_api_call = Mock()
        mock_api_call.side_effect = ValueError("Invalid parameter")
        
        # Track sleep times
        sleep_times = []
        with patch('time.sleep', side_effect=lambda x: sleep_times.append(x)):
            # Assert exception is raised immediately without retry
            with pytest.raises(ValueError) as exc_info:
                exponential_backoff_retry(
                    api_call=mock_api_call,
                    max_retries=3,
                    initial_wait=1,
                    service_name="Textract"
                )
        
        # Assert correct error message
        assert str(exc_info.value) == "Invalid parameter"
        
        # Assert only called once (no retries)
        assert mock_api_call.call_count == 1
        
        # Assert no sleep occurred
        assert sleep_times == []
    
    # Additional edge cases
    def test_different_initial_wait_time(self):
        """Test retry with different initial wait time."""
        # Create mock that fails once with throttling, then succeeds
        mock_api_call = Mock()
        throttling_error = ClientError(
            error_response={'Error': {'Code': 'ThrottlingException'}},
            operation_name='TestOperation'
        )
        mock_api_call.side_effect = [
            throttling_error,
            {"status": "success"}
        ]
        
        # Track sleep times
        sleep_times = []
        with patch('time.sleep', side_effect=lambda x: sleep_times.append(x)):
            result = exponential_backoff_retry(
                api_call=mock_api_call,
                max_retries=3,
                initial_wait=2,  # Different initial wait
                service_name="Textract"
            )
        
        # Assert waited 2 seconds (not 1)
        assert sleep_times == [2]
        assert result == {"status": "success"}
    
    def test_logging_output(self, capsys):
        """Test that retry attempts are logged correctly."""
        # Create mock that fails once with throttling, then succeeds
        mock_api_call = Mock()
        throttling_error = ClientError(
            error_response={'Error': {'Code': 'ThrottlingException'}},
            operation_name='TestOperation'
        )
        mock_api_call.side_effect = [
            throttling_error,
            {"status": "success"}
        ]
        
        # Execute with retry logic
        with patch('time.sleep'):
            exponential_backoff_retry(
                api_call=mock_api_call,
                max_retries=3,
                initial_wait=1,
                service_name="Textract"
            )
        
        # Capture printed output
        captured = capsys.readouterr()
        
        # Assert retry was logged
        assert "Textract throttled, retry 1 after 1s" in captured.out
    
    def test_logging_retry_exhausted(self, capsys):
        """Test that retry exhaustion is logged correctly."""
        # Create mock that always fails with throttling
        mock_api_call = Mock()
        throttling_error = ClientError(
            error_response={'Error': {'Code': 'ThrottlingException'}},
            operation_name='TestOperation'
        )
        mock_api_call.side_effect = throttling_error
        
        # Execute with retry logic
        with patch('time.sleep'):
            with pytest.raises(ClientError):
                exponential_backoff_retry(
                    api_call=mock_api_call,
                    max_retries=3,
                    initial_wait=1,
                    service_name="Textract"
                )
        
        # Capture printed output
        captured = capsys.readouterr()
        
        # Assert all retries were logged
        assert "Textract throttled, retry 1 after 1s" in captured.out
        assert "Textract throttled, retry 2 after 2s" in captured.out
        assert "Textract throttled, retry 3 after 4s" in captured.out
        assert "Textract failed after 3 retries" in captured.out
