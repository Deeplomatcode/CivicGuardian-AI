"""
Policy Reasoner Agent using Amazon Bedrock Nova Pro
Generates draft policy responses for MEDIUM/HIGH/CRITICAL risk cases.
"""

import json
import boto3
from botocore.exceptions import ClientError
from processing_function.retry_handler import exponential_backoff_retry


# Amazon Bedrock Nova Pro model ID
BEDROCK_MODEL_ID = "amazon.nova-pro-v1:0"

# Safety notice for all outputs
SAFETY_NOTICE = "DRAFT FOR REVIEW - Not legal advice"


def generate_policy_response(source_text, risk_data):
    """
    Generates draft policy response for cases with MEDIUM/HIGH/CRITICAL risk.
    
    Args:
        source_text: The original document text
        risk_data: Risk assessment dict from risk_analyst_agent
    
    Returns:
        dict: {
            "skipped": bool,
            "reason": str (if skipped),
            "risk_level": str,
            "draft_response": str (max 500 words),
            "rationale_bullets": list (max 5 items),
            "citations": list (max 3 items),
            "legislation_referenced": list,
            "confidence": float (0.0-1.0),
            "safety_notice": str
        }
    """
    risk_level = risk_data.get("risk_level", "UNKNOWN")
    
    # Gating logic: Skip if risk level is LOW or UNKNOWN
    if risk_level not in ["MEDIUM", "HIGH", "CRITICAL"]:
        return {
            "skipped": True,
            "reason": f"Risk level {risk_level} does not require policy response",
            "risk_level": risk_level,
            "draft_response": None,
            "rationale_bullets": [],
            "citations": [],
            "legislation_referenced": [],
            "confidence": 0.0,
            "safety_notice": SAFETY_NOTICE
        }
    
    try:
        # Create Bedrock runtime client
        bedrock_runtime = boto3.client('bedrock-runtime')
        
        # Build the prompt for policy response generation
        prompt = _build_policy_prompt(source_text, risk_data)
        
        # Prepare the request body for Nova Pro
        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            "inferenceConfig": {
                "temperature": 0.3,  # Balanced creativity and consistency
                "maxTokens": 1500
            },
            "system": [
                {
                    "text": "You are a UK social care policy advisor. Generate DRAFT responses only."
                }
            ]
        }
        
        # Call Bedrock with retry logic
        def bedrock_api_call():
            return bedrock_runtime.converse(
                modelId=BEDROCK_MODEL_ID,
                messages=request_body["messages"],
                inferenceConfig=request_body["inferenceConfig"],
                system=request_body["system"]
            )
        
        response = exponential_backoff_retry(
            api_call=bedrock_api_call,
            max_retries=3,
            initial_wait=1,
            service_name="Bedrock"
        )
        
        # Extract the response text
        response_text = response['output']['message']['content'][0]['text']
        
        # Parse and post-process the response
        policy_response = _parse_and_postprocess(response_text, source_text, risk_level)
        
        return policy_response
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', '')
        return {
            "skipped": False,
            "reason": None,
            "risk_level": risk_level,
            "draft_response": f"Policy generation failed: {error_code}",
            "rationale_bullets": ["Manual review required"],
            "citations": [],
            "legislation_referenced": [],
            "confidence": 0.0,
            "safety_notice": SAFETY_NOTICE,
            "error": str(e)
        }
    
    except Exception as e:
        return {
            "skipped": False,
            "reason": None,
            "risk_level": risk_level,
            "draft_response": f"Policy generation error: {type(e).__name__}",
            "rationale_bullets": ["Manual review required"],
            "citations": [],
            "legislation_referenced": [],
            "confidence": 0.0,
            "safety_notice": SAFETY_NOTICE,
            "error": str(e)
        }


def _build_policy_prompt(source_text, risk_data):
    """
    Builds the prompt for Bedrock Nova Pro policy response generation.
    
    Args:
        source_text: The original document text
        risk_data: Risk assessment dict
    
    Returns:
        str: Formatted prompt for the AI model
    """
    risk_level = risk_data.get("risk_level", "UNKNOWN")
    deadline = risk_data.get("deadline", "Not specified")
    required_action = risk_data.get("required_action", "Review required")
    risk_indicators = risk_data.get("risk_indicators", [])
    
    indicators_text = ", ".join(risk_indicators) if risk_indicators else "None specified"
    
    prompt = f"""You are a UK social care policy advisor. Generate a DRAFT response for the following case.

RISK ASSESSMENT:
- Risk Level: {risk_level}
- Deadline: {deadline}
- Required Action: {required_action}
- Risk Indicators: {indicators_text}

ORIGINAL DOCUMENT:
{source_text}

TASK:
Generate a draft policy response that addresses the identified risks. Include:
1. A clear, actionable draft response (max 500 words)
2. Rationale bullets explaining your reasoning (max 5 points)
3. Citations from the source document (max 3 quotes)
4. Relevant UK legislation or policy references

OUTPUT FORMAT (JSON only, no other text):
{{
  "draft_response": "Your draft response here (max 500 words)",
  "rationale_bullets": ["Reason 1", "Reason 2", "Reason 3"],
  "citations": ["Quote from source 1", "Quote from source 2"],
  "legislation_referenced": ["Care Act 2014", "Housing Act 1996"],
  "confidence": 0.0-1.0
}}

IMPORTANT:
- Only cite text that appears EXACTLY in the source document
- Keep draft response under 500 words
- Limit rationale to 5 bullets maximum
- Limit citations to 3 maximum
- This is a DRAFT for review, not final legal advice

Respond with ONLY the JSON object, no additional text."""
    
    return prompt


def _parse_and_postprocess(response_text, source_text, risk_level):
    """
    Parses the Bedrock response and applies post-processing rules.
    
    Args:
        response_text: Raw text response from Bedrock
        source_text: Original document text for citation validation
        risk_level: Risk level from risk assessment
    
    Returns:
        dict: Validated and post-processed policy response
    """
    try:
        # Extract JSON from response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx == -1 or end_idx == 0:
            raise ValueError("No JSON found in response")
        
        json_str = response_text[start_idx:end_idx]
        policy_data = json.loads(json_str)
        
        # Post-processing: Truncate draft_response to 500 words
        draft = policy_data.get("draft_response", "")
        words = draft.split()
        if len(words) > 500:
            draft = " ".join(words[:500]) + "..."
        
        # Post-processing: Limit rationale_bullets to 5
        rationale = policy_data.get("rationale_bullets", [])
        if len(rationale) > 5:
            rationale = rationale[:5]
        
        # Post-processing: Limit citations to 3
        citations = policy_data.get("citations", [])
        if len(citations) > 3:
            citations = citations[:3]
        
        # Post-processing: Validate citations appear in source_text
        validated_citations = []
        for citation in citations:
            # Check if citation text appears in source (case-insensitive, whitespace-normalized)
            citation_normalized = " ".join(citation.split()).lower()
            source_normalized = " ".join(source_text.split()).lower()
            if citation_normalized in source_normalized:
                validated_citations.append(citation)
        
        # Post-processing: Clamp confidence to [0, 1]
        confidence = policy_data.get("confidence", 0.5)
        if not isinstance(confidence, (int, float)):
            confidence = 0.5
        confidence = max(0.0, min(1.0, float(confidence)))
        
        # Get legislation references
        legislation = policy_data.get("legislation_referenced", [])
        
        return {
            "skipped": False,
            "reason": None,
            "risk_level": risk_level,
            "draft_response": draft,
            "rationale_bullets": rationale,
            "citations": validated_citations,
            "legislation_referenced": legislation,
            "confidence": confidence,
            "safety_notice": SAFETY_NOTICE
        }
        
    except (json.JSONDecodeError, ValueError) as e:
        # If parsing fails, return a safe default
        return {
            "skipped": False,
            "reason": None,
            "risk_level": risk_level,
            "draft_response": "Unable to parse policy response",
            "rationale_bullets": ["Manual review required"],
            "citations": [],
            "legislation_referenced": [],
            "confidence": 0.0,
            "safety_notice": SAFETY_NOTICE,
            "parse_error": str(e)
        }
