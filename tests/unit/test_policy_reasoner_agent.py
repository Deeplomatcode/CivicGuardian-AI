"""
Unit tests for Policy Reasoner Agent
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError
from src.policy_reasoner_agent import (
    generate_policy_response,
    _build_policy_prompt,
    _parse_and_postprocess,
    BEDROCK_MODEL_ID,
    SAFETY_NOTICE
)


# Test 1: Gating logic - Skip LOW risk
def test_gating_skips_low_risk():
    """Test that LOW risk cases are skipped without calling Bedrock."""
    source_text = "Sample document text"
    risk_data = {
        "risk_level": "LOW",
        "deadline": None,
        "required_action": "No action needed",
        "risk_indicators": []
    }
    
    result = generate_policy_response(source_text, risk_data)
    
    assert result["skipped"] is True
    assert result["reason"] == "Risk level LOW does not require policy response"
    assert result["risk_level"] == "LOW"
    assert result["draft_response"] is None
    assert result["safety_notice"] == SAFETY_NOTICE


# Test 2: Gating logic - Skip UNKNOWN risk
def test_gating_skips_unknown_risk():
    """Test that UNKNOWN risk cases are skipped without calling Bedrock."""
    source_text = "Sample document text"
    risk_data = {
        "risk_level": "UNKNOWN",
        "deadline": None,
        "required_action": "Manual review",
        "risk_indicators": []
    }
    
    result = generate_policy_response(source_text, risk_data)
    
    assert result["skipped"] is True
    assert "UNKNOWN" in result["reason"]
    assert result["risk_level"] == "UNKNOWN"


# Test 3: Successful Bedrock call for MEDIUM risk
@patch('src.policy_reasoner_agent.boto3.client')
@patch('src.policy_reasoner_agent.exponential_backoff_retry')
def test_successful_bedrock_call_medium_risk(mock_retry, mock_boto_client):
    """Test successful policy generation for MEDIUM risk case."""
    source_text = "Eviction notice dated 2024-03-15. Tenant must vacate by 2024-04-15."
    risk_data = {
        "risk_level": "MEDIUM",
        "deadline": "2024-04-15",
        "required_action": "Contact housing support",
        "risk_indicators": ["eviction"]
    }
    
    # Mock Bedrock response
    mock_response = {
        'output': {
            'message': {
                'content': [{
                    'text': json.dumps({
                        "draft_response": "We recommend contacting housing support immediately.",
                        "rationale_bullets": ["Eviction deadline approaching", "Housing support available"],
                        "citations": ["Eviction notice dated 2024-03-15"],
                        "legislation_referenced": ["Housing Act 1996"],
                        "confidence": 0.85
                    })
                }]
            }
        }
    }
    
    mock_retry.return_value = mock_response
    
    result = generate_policy_response(source_text, risk_data)
    
    assert result["skipped"] is False
    assert result["risk_level"] == "MEDIUM"
    assert "housing support" in result["draft_response"].lower()
    assert len(result["rationale_bullets"]) == 2
    assert len(result["citations"]) == 1
    assert "Housing Act 1996" in result["legislation_referenced"]
    assert result["confidence"] == 0.85
    assert result["safety_notice"] == SAFETY_NOTICE
    
    # Verify Bedrock was called with correct parameters
    mock_retry.assert_called_once()


# Test 4: Successful Bedrock call for HIGH risk
@patch('src.policy_reasoner_agent.boto3.client')
@patch('src.policy_reasoner_agent.exponential_backoff_retry')
def test_successful_bedrock_call_high_risk(mock_retry, mock_boto_client):
    """Test successful policy generation for HIGH risk case."""
    source_text = "Benefits suspended. Appeal deadline: 14 days."
    risk_data = {
        "risk_level": "HIGH",
        "deadline": "14 days",
        "required_action": "File appeal immediately",
        "risk_indicators": ["benefit suspension", "urgent deadline"]
    }
    
    mock_response = {
        'output': {
            'message': {
                'content': [{
                    'text': json.dumps({
                        "draft_response": "File appeal within 14 days to preserve benefits.",
                        "rationale_bullets": ["Urgent deadline", "Benefits at risk"],
                        "citations": ["Appeal deadline: 14 days"],
                        "legislation_referenced": ["Social Security Act 1998"],
                        "confidence": 0.9
                    })
                }]
            }
        }
    }
    
    mock_retry.return_value = mock_response
    
    result = generate_policy_response(source_text, risk_data)
    
    assert result["skipped"] is False
    assert result["risk_level"] == "HIGH"
    assert "appeal" in result["draft_response"].lower()


# Test 5: Successful Bedrock call for CRITICAL risk
@patch('src.policy_reasoner_agent.boto3.client')
@patch('src.policy_reasoner_agent.exponential_backoff_retry')
def test_successful_bedrock_call_critical_risk(mock_retry, mock_boto_client):
    """Test successful policy generation for CRITICAL risk case."""
    source_text = "Immediate safeguarding concern. Contact social services."
    risk_data = {
        "risk_level": "CRITICAL",
        "deadline": "Immediate",
        "required_action": "Emergency intervention",
        "risk_indicators": ["safeguarding"]
    }
    
    mock_response = {
        'output': {
            'message': {
                'content': [{
                    'text': json.dumps({
                        "draft_response": "Emergency intervention required immediately.",
                        "rationale_bullets": ["Safeguarding concern identified"],
                        "citations": ["Immediate safeguarding concern"],
                        "legislation_referenced": ["Care Act 2014"],
                        "confidence": 0.95
                    })
                }]
            }
        }
    }
    
    mock_retry.return_value = mock_response
    
    result = generate_policy_response(source_text, risk_data)
    
    assert result["skipped"] is False
    assert result["risk_level"] == "CRITICAL"


# Test 6: Post-processing - Word limit truncation
def test_postprocessing_word_limit():
    """Test that draft responses are truncated to 500 words."""
    source_text = "Sample text"
    risk_level = "MEDIUM"
    
    # Create a response with >500 words
    long_draft = " ".join(["word"] * 600)
    response_text = json.dumps({
        "draft_response": long_draft,
        "rationale_bullets": ["Reason 1"],
        "citations": [],
        "legislation_referenced": [],
        "confidence": 0.8
    })
    
    result = _parse_and_postprocess(response_text, source_text, risk_level)
    
    # Should be truncated to 500 words + "..."
    words = result["draft_response"].split()
    assert len(words) <= 501  # 500 words + "..."
    assert result["draft_response"].endswith("...")


# Test 7: Post-processing - Bullet limit
def test_postprocessing_bullet_limit():
    """Test that rationale bullets are limited to 5."""
    source_text = "Sample text"
    risk_level = "MEDIUM"
    
    response_text = json.dumps({
        "draft_response": "Draft response",
        "rationale_bullets": ["R1", "R2", "R3", "R4", "R5", "R6", "R7"],
        "citations": [],
        "legislation_referenced": [],
        "confidence": 0.8
    })
    
    result = _parse_and_postprocess(response_text, source_text, risk_level)
    
    assert len(result["rationale_bullets"]) == 5
    assert result["rationale_bullets"] == ["R1", "R2", "R3", "R4", "R5"]


# Test 8: Post-processing - Citation limit
def test_postprocessing_citation_limit():
    """Test that citations are limited to 3."""
    source_text = "Quote 1. Quote 2. Quote 3. Quote 4. Quote 5."
    risk_level = "MEDIUM"
    
    response_text = json.dumps({
        "draft_response": "Draft response",
        "rationale_bullets": ["Reason 1"],
        "citations": ["Quote 1", "Quote 2", "Quote 3", "Quote 4", "Quote 5"],
        "legislation_referenced": [],
        "confidence": 0.8
    })
    
    result = _parse_and_postprocess(response_text, source_text, risk_level)
    
    assert len(result["citations"]) <= 3


# Test 9: Post-processing - Citation validation
def test_postprocessing_citation_validation():
    """Test that citations are validated against source text."""
    source_text = "This is the actual source text with real quotes."
    risk_level = "MEDIUM"
    
    response_text = json.dumps({
        "draft_response": "Draft response",
        "rationale_bullets": ["Reason 1"],
        "citations": [
            "actual source text",  # Valid - appears in source
            "fake quote not in source",  # Invalid - not in source
            "real quotes"  # Valid - appears in source
        ],
        "legislation_referenced": [],
        "confidence": 0.8
    })
    
    result = _parse_and_postprocess(response_text, source_text, risk_level)
    
    # Only valid citations should remain
    assert len(result["citations"]) == 2
    assert "actual source text" in result["citations"]
    assert "real quotes" in result["citations"]
    assert "fake quote not in source" not in result["citations"]


# Test 10: Post-processing - Confidence clamping
def test_postprocessing_confidence_clamping():
    """Test that confidence scores are clamped to [0, 1]."""
    source_text = "Sample text"
    risk_level = "MEDIUM"
    
    # Test confidence > 1
    response_text_high = json.dumps({
        "draft_response": "Draft",
        "rationale_bullets": [],
        "citations": [],
        "legislation_referenced": [],
        "confidence": 1.5
    })
    
    result_high = _parse_and_postprocess(response_text_high, source_text, risk_level)
    assert result_high["confidence"] == 1.0
    
    # Test confidence < 0
    response_text_low = json.dumps({
        "draft_response": "Draft",
        "rationale_bullets": [],
        "citations": [],
        "legislation_referenced": [],
        "confidence": -0.5
    })
    
    result_low = _parse_and_postprocess(response_text_low, source_text, risk_level)
    assert result_low["confidence"] == 0.0
    
    # Test invalid confidence (string)
    response_text_invalid = json.dumps({
        "draft_response": "Draft",
        "rationale_bullets": [],
        "citations": [],
        "legislation_referenced": [],
        "confidence": "high"
    })
    
    result_invalid = _parse_and_postprocess(response_text_invalid, source_text, risk_level)
    assert result_invalid["confidence"] == 0.5  # Default


# Test 11: Bedrock ClientError handling
@patch('src.policy_reasoner_agent.boto3.client')
@patch('src.policy_reasoner_agent.exponential_backoff_retry')
def test_bedrock_client_error(mock_retry, mock_boto_client):
    """Test handling of Bedrock ClientError."""
    source_text = "Sample text"
    risk_data = {
        "risk_level": "MEDIUM",
        "deadline": None,
        "required_action": "Review",
        "risk_indicators": []
    }
    
    # Mock ClientError
    error_response = {'Error': {'Code': 'ThrottlingException', 'Message': 'Rate exceeded'}}
    mock_retry.side_effect = ClientError(error_response, 'converse')
    
    result = generate_policy_response(source_text, risk_data)
    
    assert result["skipped"] is False
    assert "failed" in result["draft_response"].lower()
    assert result["confidence"] == 0.0
    assert result["safety_notice"] == SAFETY_NOTICE
    assert "error" in result


# Test 12: JSON parsing error handling
def test_json_parsing_error():
    """Test handling of malformed JSON response."""
    source_text = "Sample text"
    risk_level = "MEDIUM"
    
    # Invalid JSON
    response_text = "This is not valid JSON at all"
    
    result = _parse_and_postprocess(response_text, source_text, risk_level)
    
    assert result["draft_response"] == "Unable to parse policy response"
    assert result["rationale_bullets"] == ["Manual review required"]
    assert result["confidence"] == 0.0
    assert "parse_error" in result


# Test 13: Prompt building
def test_build_policy_prompt():
    """Test that prompt is built correctly with all risk data."""
    source_text = "Document content here"
    risk_data = {
        "risk_level": "HIGH",
        "deadline": "2024-04-15",
        "required_action": "File appeal",
        "risk_indicators": ["eviction", "deadline"]
    }
    
    prompt = _build_policy_prompt(source_text, risk_data)
    
    assert "HIGH" in prompt
    assert "2024-04-15" in prompt
    assert "File appeal" in prompt
    assert "eviction" in prompt
    assert "deadline" in prompt
    assert "Document content here" in prompt
    assert "JSON" in prompt
    assert "500 words" in prompt


# Test 14: Schema validation - All required fields present
@patch('src.policy_reasoner_agent.boto3.client')
@patch('src.policy_reasoner_agent.exponential_backoff_retry')
def test_schema_validation_all_fields(mock_retry, mock_boto_client):
    """Test that all required fields are present in output."""
    source_text = "Sample text"
    risk_data = {
        "risk_level": "MEDIUM",
        "deadline": None,
        "required_action": "Review",
        "risk_indicators": []
    }
    
    mock_response = {
        'output': {
            'message': {
                'content': [{
                    'text': json.dumps({
                        "draft_response": "Response",
                        "rationale_bullets": ["Reason"],
                        "citations": [],
                        "legislation_referenced": ["Care Act 2014"],
                        "confidence": 0.7
                    })
                }]
            }
        }
    }
    
    mock_retry.return_value = mock_response
    
    result = generate_policy_response(source_text, risk_data)
    
    # Verify all required fields are present
    required_fields = [
        "skipped", "reason", "risk_level", "draft_response",
        "rationale_bullets", "citations", "legislation_referenced",
        "confidence", "safety_notice"
    ]
    
    for field in required_fields:
        assert field in result, f"Missing required field: {field}"


# Test 15: Empty risk indicators handling
@patch('src.policy_reasoner_agent.boto3.client')
@patch('src.policy_reasoner_agent.exponential_backoff_retry')
def test_empty_risk_indicators(mock_retry, mock_boto_client):
    """Test handling of empty risk indicators list."""
    source_text = "Sample text"
    risk_data = {
        "risk_level": "MEDIUM",
        "deadline": None,
        "required_action": "Review",
        "risk_indicators": []
    }
    
    mock_response = {
        'output': {
            'message': {
                'content': [{
                    'text': json.dumps({
                        "draft_response": "Response",
                        "rationale_bullets": [],
                        "citations": [],
                        "legislation_referenced": [],
                        "confidence": 0.5
                    })
                }]
            }
        }
    }
    
    mock_retry.return_value = mock_response
    
    result = generate_policy_response(source_text, risk_data)
    
    assert result["skipped"] is False
    assert result["risk_level"] == "MEDIUM"
