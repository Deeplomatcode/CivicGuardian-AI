# Requirements Document

## Introduction

The Document Ingestion Pipeline is a serverless AWS-based system that securely receives and processes correspondence (letters, emails, voicemails) for vulnerable adults. The system extracts text and metadata from multiple document formats, preparing structured data for downstream risk analysis while maintaining strict security and cost controls within AWS Free Tier limits.

## Glossary

- **Ingestion_Pipeline**: The complete serverless system that receives, processes, and stores documents
- **Document**: Any incoming correspondence including PDF files, images, audio files, or email text
- **Textract_Service**: Amazon Textract API used for optical character recognition on PDF and image files
- **Transcribe_Service**: Amazon Transcribe API used for speech-to-text conversion of audio files
- **Incoming_Bucket**: S3 bucket (civicguardian-incoming) that receives uploaded documents
- **Processed_Bucket**: S3 bucket (civicguardian-processed) that stores extracted JSON output
- **Quarantine_Prefix**: S3 prefix location for documents that cannot be processed
- **Case_Table**: DynamoDB table (civicguardian-cases) that stores case records
- **Processing_Lambda**: Lambda function that orchestrates document processing
- **Confidence_Score**: Numerical value (0.0-1.0) indicating OCR or transcription accuracy
- **Case_ID**: Unique UUID identifier for each processed document
- **Step_Functions_Machine**: AWS Step Functions state machine for downstream workflow orchestration
- **Caseworker**: Human user who reviews flagged documents and manages cases
- **PII**: Personally Identifiable Information including names, addresses, phone numbers, and NHS numbers

## Requirements

### Requirement 1: Document Upload and Event Triggering

**User Story:** As a caseworker, I want documents to be automatically processed when uploaded, so that I don't need to manually trigger processing.

#### Acceptance Criteria

1. WHEN a file is uploaded to THE Incoming_Bucket, THE Ingestion_Pipeline SHALL trigger THE Processing_Lambda within 5 seconds
2. THE Incoming_Bucket SHALL have server-side encryption enabled using SSE-S3
3. THE Incoming_Bucket SHALL have versioning enabled
4. THE Incoming_Bucket SHALL retain all uploaded files until processing is confirmed complete

### Requirement 2: File Type Detection and Routing

**User Story:** As the system, I want to detect file types accurately, so that documents are routed to the correct processing service.

#### Acceptance Criteria

1. WHEN a PDF file is detected, THE Processing_Lambda SHALL route it to THE Textract_Service
2. WHEN an image file is detected with extension jpg, jpeg, png, or tiff, THE Processing_Lambda SHALL route it to THE Textract_Service
3. WHEN an audio file is detected with extension mp3, wav, or m4a, THE Processing_Lambda SHALL route it to THE Transcribe_Service
4. WHEN an email text file is detected with extension txt or html, THE Processing_Lambda SHALL extract text directly without external services
5. WHEN an unsupported file type is detected, THE Processing_Lambda SHALL move the file to THE Quarantine_Prefix and send an SNS alert

### Requirement 3: PDF and Image Text Extraction

**User Story:** As a caseworker, I want text extracted from scanned and digital letters, so that I can analyze the content for risks.

#### Acceptance Criteria

1. WHEN a PDF or image file is processed, THE Processing_Lambda SHALL invoke THE Textract_Service DetectDocumentText API
2. THE Processing_Lambda SHALL extract all text content from THE Textract_Service response
3. THE Processing_Lambda SHALL extract THE Confidence_Score from THE Textract_Service response
4. THE Processing_Lambda SHALL extract page count from THE Textract_Service response
5. IF THE Textract_Service returns a throttling error, THEN THE Processing_Lambda SHALL retry with exponential backoff up to 3 attempts
6. IF THE Textract_Service fails after 3 retry attempts, THEN THE Processing_Lambda SHALL move the document to THE Quarantine_Prefix and send an SNS alert

### Requirement 4: Audio Transcription

**User Story:** As a caseworker, I want voicemails transcribed to text, so that I can review audio correspondence without listening to each recording.

#### Acceptance Criteria

1. WHEN an audio file is processed, THE Processing_Lambda SHALL invoke THE Transcribe_Service StartTranscriptionJob API with language code en-GB
2. THE Processing_Lambda SHALL poll THE Transcribe_Service until transcription is complete or timeout occurs
3. THE Processing_Lambda SHALL extract the transcribed text from THE Transcribe_Service response
4. THE Processing_Lambda SHALL extract THE Confidence_Score from THE Transcribe_Service response
5. IF THE Transcribe_Service returns a throttling error, THEN THE Processing_Lambda SHALL retry with exponential backoff up to 3 attempts
6. IF transcription does not complete within 25 seconds, THEN THE Processing_Lambda SHALL log a timeout error and move the document to THE Quarantine_Prefix

### Requirement 5: Email Text Extraction

**User Story:** As a caseworker, I want email content extracted directly, so that text-based correspondence is processed quickly without external API calls.

#### Acceptance Criteria

1. WHEN a plain text email file is processed, THE Processing_Lambda SHALL read the file content directly
2. WHEN an HTML email file is processed, THE Processing_Lambda SHALL strip HTML tags and extract plain text
3. THE Processing_Lambda SHALL set THE Confidence_Score to 1.0 for directly extracted email text
4. THE Processing_Lambda SHALL set page count to 1 for email documents

### Requirement 6: Metadata Extraction

**User Story:** As a caseworker, I want sender and document type information extracted, so that I can quickly identify the source of correspondence.

#### Acceptance Criteria

1. THE Processing_Lambda SHALL attempt to detect the sender organization from document text using pattern matching
2. WHEN sender detection fails, THE Processing_Lambda SHALL set sender to null
3. THE Processing_Lambda SHALL classify each document as letter, email, or voicemail based on file type and content
4. THE Processing_Lambda SHALL detect document language and set it to en-GB by default
5. THE Processing_Lambda SHALL generate a unique Case_ID as a UUID for each processed document

### Requirement 7: Structured Output Storage

**User Story:** As a downstream system, I want processed documents stored in a consistent JSON format, so that I can reliably parse the data.

#### Acceptance Criteria

1. WHEN processing completes successfully, THE Processing_Lambda SHALL create a JSON file in THE Processed_Bucket
2. THE JSON file SHALL contain case_id, timestamp, document_s3_key, extracted_text, metadata object, status, and created_at fields
3. THE metadata object SHALL contain sender, document_type, confidence, page_count, and language fields
4. THE Processed_Bucket SHALL have server-side encryption enabled using SSE-S3
5. THE JSON filename SHALL use the format: {case_id}.json

### Requirement 8: Database Record Creation

**User Story:** As a caseworker, I want case records stored in a database, so that I can query and track all processed documents.

#### Acceptance Criteria

1. WHEN processing completes successfully, THE Processing_Lambda SHALL write a record to THE Case_Table
2. THE Case_Table record SHALL contain all fields from the JSON output schema
3. THE Case_Table SHALL use case_id as the partition key
4. WHEN THE Case_Table write fails, THE Processing_Lambda SHALL retry once
5. IF THE Case_Table write fails after retry, THEN THE Processing_Lambda SHALL log the error and send an SNS alert

### Requirement 9: Downstream Workflow Triggering

**User Story:** As the system, I want to trigger the next processing step automatically, so that documents flow through the complete analysis pipeline.

#### Acceptance Criteria

1. WHEN a document is successfully stored in THE Processed_Bucket and THE Case_Table, THE Processing_Lambda SHALL trigger THE Step_Functions_Machine
2. THE Processing_Lambda SHALL pass the case_id to THE Step_Functions_Machine as input
3. IF THE Step_Functions_Machine trigger fails, THEN THE Processing_Lambda SHALL log the error and send an SNS alert

### Requirement 10: Low Confidence Flagging

**User Story:** As a caseworker, I want documents with low OCR confidence flagged, so that I can manually review potentially inaccurate extractions.

#### Acceptance Criteria

1. WHEN THE Confidence_Score is less than 0.5, THE Processing_Lambda SHALL set low_confidence to true in THE Case_Table record
2. WHEN THE Confidence_Score is less than 0.5, THE Processing_Lambda SHALL add a manual_review_required flag to the JSON output
3. WHEN low_confidence is true, THE Processing_Lambda SHALL send an SNS notification to the caseworker review queue

### Requirement 11: PII Protection in Logs

**User Story:** As a data protection officer, I want PII excluded from logs, so that we comply with GDPR and protect vulnerable adults' privacy.

#### Acceptance Criteria

1. THE Processing_Lambda SHALL NOT write extracted_text to CloudWatch Logs
2. THE Processing_Lambda SHALL NOT write sender names or addresses to CloudWatch Logs
3. WHEN logging errors, THE Processing_Lambda SHALL use THE Case_ID as the only identifier
4. THE Processing_Lambda SHALL log only file type, file size, and processing status to CloudWatch Logs

### Requirement 12: Lambda Resource Limits

**User Story:** As a system administrator, I want Lambda execution constrained, so that runaway processes don't incur unexpected costs.

#### Acceptance Criteria

1. THE Processing_Lambda SHALL have a timeout of 30 seconds
2. THE Processing_Lambda SHALL have 512 MB of memory allocated
3. WHEN THE Processing_Lambda approaches timeout at 28 seconds, THE Processing_Lambda SHALL log a warning and gracefully terminate
4. THE Processing_Lambda SHALL use reserved concurrency of 10 to prevent cost overruns

### Requirement 13: AWS Free Tier Compliance

**User Story:** As a project manager, I want processing to stay within AWS Free Tier limits, so that we minimize operational costs during pilot phase.

#### Acceptance Criteria

1. THE Ingestion_Pipeline SHALL track monthly Textract page count
2. WHEN monthly Textract usage exceeds 900 pages, THE Ingestion_Pipeline SHALL send an SNS alert
3. THE Ingestion_Pipeline SHALL track monthly Transcribe minutes
4. WHEN monthly Transcribe usage exceeds 55 minutes, THE Ingestion_Pipeline SHALL send an SNS alert
5. THE Processing_Lambda SHALL log usage metrics to CloudWatch Metrics for monitoring

### Requirement 14: Retry Logic for Transient Failures

**User Story:** As a system administrator, I want transient failures handled automatically, so that temporary issues don't require manual intervention.

#### Acceptance Criteria

1. WHEN THE Textract_Service returns a throttling error, THE Processing_Lambda SHALL wait 1 second and retry
2. WHEN THE Textract_Service returns a throttling error on second attempt, THE Processing_Lambda SHALL wait 2 seconds and retry
3. WHEN THE Textract_Service returns a throttling error on third attempt, THE Processing_Lambda SHALL wait 4 seconds and retry
4. IF THE Textract_Service fails after 3 retries, THEN THE Processing_Lambda SHALL move the document to THE Quarantine_Prefix
5. THE retry logic SHALL apply identically to THE Transcribe_Service throttling errors

### Requirement 15: Document Quarantine and Alerting

**User Story:** As a caseworker, I want to be notified when documents fail processing, so that I can manually handle problematic files.

#### Acceptance Criteria

1. WHEN a document cannot be processed after all retries, THE Processing_Lambda SHALL move it to THE Quarantine_Prefix
2. THE Quarantine_Prefix SHALL be s3://civicguardian-incoming/quarantine/
3. WHEN a document is quarantined, THE Processing_Lambda SHALL send an SNS notification with the case_id and failure reason
4. THE Processing_Lambda SHALL write a quarantine record to THE Case_Table with status set to quarantined
5. THE quarantine record SHALL include the original S3 key and error message

### Requirement 16: Idempotent Processing

**User Story:** As a system administrator, I want duplicate uploads handled gracefully, so that reprocessing the same document doesn't create duplicate case records.

#### Acceptance Criteria

1. THE Processing_Lambda SHALL generate THE Case_ID deterministically from the S3 object key and upload timestamp
2. WHEN a document with an existing Case_ID is processed, THE Processing_Lambda SHALL update the existing Case_Table record
3. THE Processing_Lambda SHALL NOT create duplicate entries in THE Case_Table for the same document
4. THE Processing_Lambda SHALL log when a duplicate document is detected

### Requirement 17: Sender Detection

**User Story:** As a caseworker, I want sender organizations automatically detected, so that I can quickly identify correspondence from councils, NHS trusts, and benefits offices.

#### Acceptance Criteria

1. THE Processing_Lambda SHALL search extracted text for known organization patterns including "NHS", "Council", "Department for Work and Pensions", "DWP", "HMRC"
2. WHEN an organization pattern is found, THE Processing_Lambda SHALL set the sender field to the detected organization name
3. WHEN no organization pattern is found, THE Processing_Lambda SHALL set the sender field to null
4. THE Processing_Lambda SHALL use case-insensitive pattern matching for sender detection
5. THE Processing_Lambda SHALL store the first detected organization when multiple are found

### Requirement 18: Output Schema Validation

**User Story:** As a downstream system developer, I want all JSON outputs to conform to a strict schema, so that I can parse them reliably without error handling for missing fields.

#### Acceptance Criteria

1. THE Processing_Lambda SHALL validate that every JSON output contains all required fields: case_id, timestamp, document_s3_key, extracted_text, metadata, status, created_at
2. THE Processing_Lambda SHALL validate that the metadata object contains all required fields: sender, document_type, confidence, page_count, language
3. WHEN schema validation fails, THE Processing_Lambda SHALL log a critical error and send an SNS alert
4. THE Processing_Lambda SHALL NOT write invalid JSON to THE Processed_Bucket
5. THE Processing_Lambda SHALL use ISO 8601 format for the created_at timestamp

### Requirement 19: S3 Bucket Lifecycle Management

**User Story:** As a system administrator, I want old processed documents archived automatically, so that storage costs remain low while maintaining compliance.

#### Acceptance Criteria

1. THE Incoming_Bucket SHALL transition objects to S3 Glacier after 90 days
2. THE Processed_Bucket SHALL transition objects to S3 Glacier after 90 days
3. THE Incoming_Bucket SHALL permanently delete objects after 7 years to comply with data retention policies
4. THE Processed_Bucket SHALL permanently delete objects after 7 years to comply with data retention policies

### Requirement 20: Monitoring and Observability

**User Story:** As a system administrator, I want comprehensive logging and metrics, so that I can monitor system health and troubleshoot issues.

#### Acceptance Criteria

1. THE Processing_Lambda SHALL log processing start with case_id, file_type, and file_size
2. THE Processing_Lambda SHALL log processing completion with case_id, processing_duration, and confidence_score
3. THE Processing_Lambda SHALL log all errors with case_id, error_type, and retry_count
4. THE Processing_Lambda SHALL emit CloudWatch Metrics for documents_processed, documents_quarantined, and average_confidence_score
5. THE Processing_Lambda SHALL emit CloudWatch Metrics for textract_pages_used and transcribe_minutes_used

## Non-Functional Requirements

### Security

- All data at rest SHALL be encrypted using AWS managed keys
- All data in transit SHALL use TLS 1.2 or higher
- IAM roles SHALL follow least privilege principle
- No PII SHALL appear in logs or error messages

### Performance

- 95% of documents SHALL be processed within 10 seconds
- The system SHALL handle up to 100 documents per day
- Lambda cold start time SHALL NOT exceed 3 seconds

### Cost

- Monthly AWS costs SHALL NOT exceed $5 during pilot phase
- The system SHALL operate within AWS Free Tier limits where possible
- Cost per document SHALL NOT exceed $0.05

### Reliability

- The system SHALL have 99% availability during business hours (9am-5pm GMT)
- Transient failures SHALL be retried automatically
- Permanent failures SHALL trigger alerts within 1 minute
