# Retry handler module
# Implements exponential backoff retry logic for AWS service calls

import time
from botocore.exceptions import ClientError


def exponential_backoff_retry(api_call, max_retries, initial_wait, service_name):
    """
    Executes API call with exponential backoff retry logic.
    
    Args:
        api_call: Callable function that makes the API call
        max_retries: Maximum number of retry attempts (3)
        initial_wait: Initial wait time in seconds (1)
        service_name: Name of service for logging (Textract/Transcribe)
    
    Returns:
        API response if successful
    
    Raises:
        Exception if all retries exhausted
    """
    wait_time = initial_wait
    
    for attempt in range(max_retries + 1):
        try:
            response = api_call()
            return response
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            
            # Check if throttling error
            if error_code in ['ThrottlingException', 'ProvisionedThroughputExceededException']:
                if attempt < max_retries:
                    log_retry(service_name, attempt + 1, wait_time)
                    time.sleep(wait_time)
                    wait_time *= 2  # Exponential backoff: 1s, 2s, 4s
                else:
                    log_retry_exhausted(service_name, max_retries)
                    raise
            else:
                # Non-throttling error, don't retry
                raise
        
        except Exception as e:
            # Non-ClientError exceptions, don't retry
            raise


def log_retry(service_name, attempt, wait_time):
    """Logs retry attempt (no PII)."""
    print(f"{service_name} throttled, retry {attempt} after {wait_time}s")


def log_retry_exhausted(service_name, max_retries):
    """Logs when retries are exhausted (no PII)."""
    print(f"{service_name} failed after {max_retries} retries")
