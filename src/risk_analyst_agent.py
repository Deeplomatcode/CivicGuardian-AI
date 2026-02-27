"""
Risk Analyst Agent using Amazon Bedrock Nova Lite
Analyzes extracted text for risk indicators and provides structured risk assessment.
"""

import json
import boto3
from botocore.exceptions import ClientError
from processing_function.retry_handler import exponential_backoff_retry


# Amazon Bedrock Nova Lite model ID
BEDROCK_MODEL_ID = "amazon.nova-lite-v1:0"


def analyze_risk(extracted_text, metadata=None):
    """
    Analyzes extracted text for risk indicators using Amazon Bedrock Nova Lite.
    
    Args:
        extracted_text: The text content to analyze
        metadata: Optional metadata dict with sender, document_type, etc.
    
    Returns:
        dict: {
            "risk_level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
            "deadline": extracted date string or None,
            "required_action": specific steps needed,
            "confidence_score": 0.0-1.0,
            "reasoning": brief explanation,
            "risk_indicators": list of detected indicators
        }
    """
    try:
        # Create Bedrock runtime client
        bedrock_runtime = boto3.client('bedrock-runtime')
        
        # Build the prompt for risk analysis
        prompt = _build_risk_analysis_prompt(extracted_text, metadata)
        
        # Prepare the request body for Nova Lite
        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            "inferenceConfig": {
                "temperature": 0.1,  # Low temperature for consistent analysis
                "maxTokens": 1000
            }
        }
        
        # Call Bedrock with retry logic
        def bedrock_api_call():
            return bedrock_runtime.converse(
                modelId=BEDROCK_MODEL_ID,
                messages=request_body["messages"],
                inferenceConfig=request_body["inferenceConfig"]
            )
        
        response = exponential_backoff_retry(
            api_call=bedrock_api_call,
            max_retries=3,
            initial_wait=1,
            service_name="Bedrock"
        )
        
        # Extract the response text
        response_text = response['output']['message']['content'][0]['text']
        
        # Parse the JSON response
        risk_assessment = _parse_bedrock_response(response_text)
        
        return risk_assessment
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', '')
        return {
            "risk_level": "UNKNOWN",
            "deadline": None,
            "required_action": "Manual review required - AI analysis failed",
            "confidence_score": 0.0,
            "reasoning": f"Bedrock API error: {error_code}",
            "risk_indicators": [],
            "error": str(e)
        }
    
    except Exception as e:
        return {
            "risk_level": "UNKNOWN",
            "deadline": None,
            "required_action": "Manual review required - Analysis failed",
            "confidence_score": 0.0,
            "reasoning": f"Analysis error: {type(e).__name__}",
            "risk_indicators": [],
            "error": str(e)
        }


def _build_risk_analysis_prompt(extracted_text, metadata):
    """
    Builds the prompt for Bedrock Nova Lite risk analysis.
    
    Args:
        extracted_text: The document text to analyze
        metadata: Optional metadata dict
    
    Returns:
        str: Formatted prompt for the AI model
    """
    sender = metadata.get("sender", "Unknown") if metadata else "Unknown"
    doc_type = metadata.get("document_type", "document") if metadata else "document"
    
    prompt = f"""You are a risk analyst for vulnerable adult social services. Analyze the following {doc_type} from {sender} for risk indicators.

DOCUMENT TEXT:
{extracted_text}

RISK INDICATORS TO DETECT:
1. Eviction notices or housing threats
2. Benefit suspension or termination
3. Care gaps or service interruptions
4. Urgent deadlines or time-sensitive actions
5. Medical emergencies or health deterioration
6. Financial hardship or debt
7. Safeguarding concerns

ANALYSIS REQUIREMENTS:
- Identify the overall risk level: LOW, MEDIUM, HIGH, or CRITICAL
- Extract any deadlines mentioned (dates, timeframes)
- Specify required actions with urgency
- Provide confidence score (0.0-1.0) based on clarity of information
- List specific risk indicators found
- Explain your reasoning briefly

OUTPUT FORMAT (JSON only, no other text):
{{
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "deadline": "YYYY-MM-DD or descriptive timeframe or null",
  "required_action": "Specific steps needed",
  "confidence_score": 0.0-1.0,
  "reasoning": "Brief explanation of risk assessment",
  "risk_indicators": ["indicator1", "indicator2"]
}}

Respond with ONLY the JSON object, no additional text."""
    
    return prompt


def _parse_bedrock_response(response_text):
    """
    Parses the Bedrock response and validates the structure.
    
    Args:
        response_text: Raw text response from Bedrock
    
    Returns:
        dict: Validated risk assessment
    """
    try:
        # Try to extract JSON from the response
        # Sometimes the model includes extra text, so we need to find the JSON
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx == -1 or end_idx == 0:
            raise ValueError("No JSON found in response")
        
        json_str = response_text[start_idx:end_idx]
        risk_data = json.loads(json_str)
        
        # Validate required fields
        required_fields = ["risk_level", "deadline", "required_action", 
                          "confidence_score", "reasoning"]
        
        for field in required_fields:
            if field not in risk_data:
                risk_data[field] = _get_default_value(field)
        
        # Validate risk_level
        valid_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL", "UNKNOWN"]
        if risk_data["risk_level"] not in valid_levels:
            risk_data["risk_level"] = "MEDIUM"
        
        # Validate confidence_score
        if not isinstance(risk_data["confidence_score"], (int, float)):
            risk_data["confidence_score"] = 0.5
        else:
            risk_data["confidence_score"] = max(0.0, min(1.0, float(risk_data["confidence_score"])))
        
        # Ensure risk_indicators exists
        if "risk_indicators" not in risk_data:
            risk_data["risk_indicators"] = []
        
        return risk_data
        
    except (json.JSONDecodeError, ValueError) as e:
        # If parsing fails, return a safe default
        return {
            "risk_level": "MEDIUM",
            "deadline": None,
            "required_action": "Manual review required - Unable to parse AI response",
            "confidence_score": 0.3,
            "reasoning": f"Response parsing error: {str(e)}",
            "risk_indicators": [],
            "parse_error": str(e)
        }


def _get_default_value(field):
    """Returns default value for a missing field."""
    defaults = {
        "risk_level": "MEDIUM",
        "deadline": None,
        "required_action": "Review required",
        "confidence_score": 0.5,
        "reasoning": "Incomplete analysis",
        "risk_indicators": []
    }
    return defaults.get(field, None)
