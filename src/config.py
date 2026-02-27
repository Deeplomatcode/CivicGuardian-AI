# Configuration module
# Defines environment variables and constants

import os


class Config:
    """Configuration constants for the document ingestion pipeline."""
    
    # S3 Buckets
    PROCESSED_BUCKET = os.environ.get('PROCESSED_BUCKET', 'civicguardian-processed')
    
    # DynamoDB Table
    CASE_TABLE = os.environ.get('CASE_TABLE', 'civicguardian-cases')
    
    # Step Functions
    STEP_FUNCTIONS_ARN = os.environ.get('STEP_FUNCTIONS_ARN', '')
    
    # SNS Topic
    SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', '')
    
    # Usage Limits (AWS Free Tier)
    TEXTRACT_PAGE_LIMIT = int(os.environ.get('TEXTRACT_PAGE_LIMIT', '900'))
    TRANSCRIBE_MINUTE_LIMIT = int(os.environ.get('TRANSCRIBE_MINUTE_LIMIT', '55'))
    
    # Quarantine Configuration
    QUARANTINE_PREFIX = 'quarantine/'
    
    # Lambda Configuration
    LAMBDA_TIMEOUT_WARNING = 28  # seconds - warn when approaching 30s timeout
