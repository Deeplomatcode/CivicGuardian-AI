"""
Unit tests for risk_analyst_agent module.
Tests risk analysis using Amazon Bedrock Nova Lite.
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError
from processing_function.risk_analyst_agent import (
    analyze_risk,
    _build_risk_analysis_prompt,
    _parse_bedrock_response,
    _get_default_value
)


class TestAnalyzeRisk:
    """Tests for analyze_risk function."""
    
    @patch('src.risk_analyst_agent.boto3.client')
    @patch('processing_function.risk_analyst_agent.exponential_backoff_retry')
    def test_successful_risk_analysis_critical(self, mock_retry, mock_boto_client):
        """Test successful risk analysis with CRITICAL risk level."""
        # Mock Bedrock response
        mock_response = {
            'output': {
                'message': {
                    'content': [{
                        'text': json.dumps({
                            "risk_level": "CRITICAL",
                            "deadline": "2024-02-15",
                            "required_action": "Immediate intervention required - eviction notice",
                            "confidence_score": 0.95,
                            "reasoning": "Eviction notice with 7-day deadline detected",
                            "risk_indicators": ["eviction_notice", "urgent_deadline"]
                        })
                    }]
                }
            }
        }
        
        mock_retry.return_value = mock_response
        
        text = "EVICTION NOTICE: You must vacate the premises by February 15, 2024."
        result = analyze_risk(text)
        
        assert result["risk_level"] == "CRITICAL"
        assert result["deadline"] == "2024-02-15"
        assert "eviction" in result["required_action"].lower()
        assert result["confidence_score"] == 0.95
        assert "eviction_notice" in result["risk_indicators"]
        
        # Verify Bedrock was called
        mock_retry.assert_called_once()
    
    @patch('src.risk_analyst_agent.boto3.client')
    @patch('processing_function.risk_analyst_agent.exponential_backoff_retry')
    def test_successful_risk_analysis_high(self, mock_retry, mock_boto_client):
        """Test successful risk analysis with HIGH risk level."""
        mock_response = {
            'output': {
                'message': {
                    'content': [{
                        'text': json.dumps({
                            "risk_level": "HIGH",
                            "deadline": "within 14 days",
                            "required_action": "Contact DWP immediately to appeal benefit suspension",
                            "confidence_score": 0.88,
                            "reasoning": "Benefit suspension notice with appeal deadline",
                            "risk_indicators": ["benefit_suspension", "appeal_deadline"]
                        })
                    }]
                }
            }
        }
        
        mock_retry.return_value = mock_response
        
        text = "Your benefits have been suspended. You have 14 days to appeal."
        result = analyze_risk(text)
        
        assert result["risk_level"] == "HIGH"
        assert result["deadline"] == "within 14 days"
        assert "appeal" in result["required_action"].lower()
        assert result["confidence_score"] == 0.88
    
    @patch('src.risk_analyst_agent.boto3.client')
    @patch('processing_function.risk_analyst_agent.exponential_backoff_retry')
    def test_successful_risk_analysis_medium(self, mock_retry, mock_boto_client):
        """Test successful risk analysis with MEDIUM risk level."""
        mock_response = {
            'output': {
                'message': {
                    'content': [{
                        'text': json.dumps({
                            "risk_level": "MEDIUM",
                            "deadline": None,
                            "required_action": "Schedule follow-up appointment within 30 days",
                            "confidence_score": 0.75,
                            "reasoning": "Routine medical follow-up required",
                            "risk_indicators": ["medical_followup"]
                        })
                    }]
                }
            }
        }
        
        mock_retry.return_value = mock_response
        
        text = "Please schedule a follow-up appointment for your recent assessment."
        result = analyze_risk(text)
        
        assert result["risk_level"] == "MEDIUM"
        assert result["deadline"] is None
        assert result["confidence_score"] == 0.75
    
    @patch('src.risk_analyst_agent.boto3.client')
    @patch('processing_function.risk_analyst_agent.exponential_backoff_retry')
    def test_successful_risk_analysis_low(self, mock_retry, mock_boto_client):
        """Test successful risk analysis with LOW risk level."""
        mock_response = {
            'output': {
                'message': {
                    'content': [{
                        'text': json.dumps({
                            "risk_level": "LOW",
                            "deadline": None,
                            "required_action": "No immediate action required",
                            "confidence_score": 0.92,
                            "reasoning": "Informational letter with no urgent concerns",
                            "risk_indicators": []
                        })
                    }]
                }
            }
        }
        
        mock_retry.return_value = mock_response
        
        text = "Thank you for your recent inquiry. We will be in touch."
        result = analyze_risk(text)
        
        assert result["risk_level"] == "LOW"
        assert result["deadline"] is None
        assert result["confidence_score"] == 0.92
        assert len(result["risk_indicators"]) == 0
    
    @patch('src.risk_analyst_agent.boto3.client')
    @patch('processing_function.risk_analyst_agent.exponential_backoff_retry')
    def test_risk_analysis_with_metadata(self, mock_retry, mock_boto_client):
        """Test risk analysis includes metadata in prompt."""
        mock_response = {
            'output': {
                'message': {
                    'content': [{
                        'text': json.dumps({
                            "risk_level": "HIGH",
                            "deadline": "2024-03-01",
                            "required_action": "Contact NHS Trust",
                            "confidence_score": 0.85,
                            "reasoning": "Medical appointment required",
                            "risk_indicators": ["medical_urgency"]
                        })
                    }]
                }
            }
        }
        
        mock_retry.return_value = mock_response
        
        metadata = {
            "sender": "NHS Trust",
            "document_type": "letter"
        }
        
        text = "Urgent medical appointment required by March 1st."
        result = analyze_risk(text, metadata)
        
        assert result["risk_level"] == "HIGH"
        # Verify metadata was used (check the call to retry)
        assert mock_retry.called
    
    @patch('src.risk_analyst_agent.boto3.client')
    @patch('processing_function.risk_analyst_agent.exponential_backoff_retry')
    def test_bedrock_throttling_error(self, mock_retry, mock_boto_client):
        """Test handling of Bedrock throttling errors."""
        mock_retry.side_effect = ClientError(
            error_response={'Error': {'Code': 'ThrottlingException'}},
            operation_name='Converse'
        )
        
        text = "Test document"
        result = analyze_risk(text)
        
        assert result["risk_level"] == "UNKNOWN"
        assert result["confidence_score"] == 0.0
        assert "Manual review required" in result["required_action"]
        assert "error" in result
    
    @patch('src.risk_analyst_agent.boto3.client')
    @patch('processing_function.risk_analyst_agent.exponential_backoff_retry')
    def test_bedrock_access_denied_error(self, mock_retry, mock_boto_client):
        """Test handling of Bedrock access denied errors."""
        mock_retry.side_effect = ClientError(
            error_response={'Error': {'Code': 'AccessDeniedException'}},
            operation_name='Converse'
        )
        
        text = "Test document"
        result = analyze_risk(text)
        
        assert result["risk_level"] == "UNKNOWN"
        assert result["confidence_score"] == 0.0
        assert "Bedrock API error" in result["reasoning"]
    
    @patch('src.risk_analyst_agent.boto3.client')
    @patch('processing_function.risk_analyst_agent.exponential_backoff_retry')
    def test_invalid_json_response(self, mock_retry, mock_boto_client):
        """Test handling of invalid JSON in Bedrock response."""
        mock_response = {
            'output': {
                'message': {
                    'content': [{
                        'text': 'This is not valid JSON'
                    }]
                }
            }
        }
        
        mock_retry.return_value = mock_response
        
        text = "Test document"
        result = analyze_risk(text)
        
        assert result["risk_level"] == "MEDIUM"
        assert result["confidence_score"] == 0.3
        assert "parsing" in result["reasoning"].lower()
    
    @patch('src.risk_analyst_agent.boto3.client')
    @patch('processing_function.risk_analyst_agent.exponential_backoff_retry')
    def test_partial_json_response(self, mock_retry, mock_boto_client):
        """Test handling of partial JSON response (missing fields)."""
        mock_response = {
            'output': {
                'message': {
                    'content': [{
                        'text': json.dumps({
                            "risk_level": "HIGH",
                            "confidence_score": 0.8
                            # Missing other required fields
                        })
                    }]
                }
            }
        }
        
        mock_retry.return_value = mock_response
        
        text = "Test document"
        result = analyze_risk(text)
        
        assert result["risk_level"] == "HIGH"
        assert result["confidence_score"] == 0.8
        # Should have default values for missing fields
        assert "deadline" in result
        assert "required_action" in result
        assert "reasoning" in result


class TestBuildRiskAnalysisPrompt:
    """Tests for _build_risk_analysis_prompt function."""
    
    def test_prompt_with_metadata(self):
        """Test prompt building with metadata."""
        text = "Test document content"
        metadata = {
            "sender": "NHS Trust",
            "document_type": "letter"
        }
        
        prompt = _build_risk_analysis_prompt(text, metadata)
        
        assert "NHS Trust" in prompt
        assert "letter" in prompt
        assert "Test document content" in prompt
        assert "RISK INDICATORS" in prompt
        assert "OUTPUT FORMAT" in prompt
    
    def test_prompt_without_metadata(self):
        """Test prompt building without metadata."""
        text = "Test document content"
        
        prompt = _build_risk_analysis_prompt(text, None)
        
        assert "Unknown" in prompt
        assert "document" in prompt
        assert "Test document content" in prompt
    
    def test_prompt_includes_risk_indicators(self):
        """Test that prompt includes all required risk indicators."""
        text = "Test"
        prompt = _build_risk_analysis_prompt(text, None)
        
        assert "Eviction" in prompt
        assert "Benefit suspension" in prompt
        assert "Care gaps" in prompt
        assert "deadlines" in prompt
        assert "Medical emergencies" in prompt
        assert "Financial hardship" in prompt
        assert "Safeguarding" in prompt
    
    def test_prompt_specifies_json_format(self):
        """Test that prompt specifies JSON output format."""
        text = "Test"
        prompt = _build_risk_analysis_prompt(text, None)
        
        assert "JSON" in prompt
        assert "risk_level" in prompt
        assert "deadline" in prompt
        assert "required_action" in prompt
        assert "confidence_score" in prompt
        assert "reasoning" in prompt


class TestParseBedrockResponse:
    """Tests for _parse_bedrock_response function."""
    
    def test_parse_valid_json(self):
        """Test parsing valid JSON response."""
        response_text = json.dumps({
            "risk_level": "HIGH",
            "deadline": "2024-03-01",
            "required_action": "Contact immediately",
            "confidence_score": 0.9,
            "reasoning": "Urgent deadline detected",
            "risk_indicators": ["deadline", "urgency"]
        })
        
        result = _parse_bedrock_response(response_text)
        
        assert result["risk_level"] == "HIGH"
        assert result["deadline"] == "2024-03-01"
        assert result["confidence_score"] == 0.9
        assert len(result["risk_indicators"]) == 2
    
    def test_parse_json_with_extra_text(self):
        """Test parsing JSON embedded in extra text."""
        response_text = """Here is the analysis:
        {
            "risk_level": "MEDIUM",
            "deadline": null,
            "required_action": "Review",
            "confidence_score": 0.7,
            "reasoning": "Standard case"
        }
        That's my assessment."""
        
        result = _parse_bedrock_response(response_text)
        
        assert result["risk_level"] == "MEDIUM"
        assert result["confidence_score"] == 0.7
    
    def test_parse_invalid_risk_level(self):
        """Test parsing with invalid risk level."""
        response_text = json.dumps({
            "risk_level": "SUPER_HIGH",  # Invalid
            "deadline": None,
            "required_action": "Review",
            "confidence_score": 0.8,
            "reasoning": "Test"
        })
        
        result = _parse_bedrock_response(response_text)
        
        # Should default to MEDIUM
        assert result["risk_level"] == "MEDIUM"
    
    def test_parse_invalid_confidence_score(self):
        """Test parsing with invalid confidence score."""
        response_text = json.dumps({
            "risk_level": "HIGH",
            "deadline": None,
            "required_action": "Review",
            "confidence_score": "high",  # Invalid type
            "reasoning": "Test"
        })
        
        result = _parse_bedrock_response(response_text)
        
        # Should default to 0.5
        assert result["confidence_score"] == 0.5
    
    def test_parse_confidence_score_out_of_range(self):
        """Test parsing with confidence score out of range."""
        response_text = json.dumps({
            "risk_level": "HIGH",
            "deadline": None,
            "required_action": "Review",
            "confidence_score": 1.5,  # > 1.0
            "reasoning": "Test"
        })
        
        result = _parse_bedrock_response(response_text)
        
        # Should clamp to 1.0
        assert result["confidence_score"] == 1.0
    
    def test_parse_missing_fields(self):
        """Test parsing with missing required fields."""
        response_text = json.dumps({
            "risk_level": "LOW"
            # Missing all other fields
        })
        
        result = _parse_bedrock_response(response_text)
        
        assert result["risk_level"] == "LOW"
        assert "deadline" in result
        assert "required_action" in result
        assert "confidence_score" in result
        assert "reasoning" in result
    
    def test_parse_completely_invalid_json(self):
        """Test parsing completely invalid JSON."""
        response_text = "This is not JSON at all!"
        
        result = _parse_bedrock_response(response_text)
        
        assert result["risk_level"] == "MEDIUM"
        assert result["confidence_score"] == 0.3
        assert "parsing" in result["reasoning"].lower()
        assert "parse_error" in result


class TestGetDefaultValue:
    """Tests for _get_default_value function."""
    
    def test_default_risk_level(self):
        """Test default value for risk_level."""
        assert _get_default_value("risk_level") == "MEDIUM"
    
    def test_default_deadline(self):
        """Test default value for deadline."""
        assert _get_default_value("deadline") is None
    
    def test_default_required_action(self):
        """Test default value for required_action."""
        assert _get_default_value("required_action") == "Review required"
    
    def test_default_confidence_score(self):
        """Test default value for confidence_score."""
        assert _get_default_value("confidence_score") == 0.5
    
    def test_default_reasoning(self):
        """Test default value for reasoning."""
        assert _get_default_value("reasoning") == "Incomplete analysis"
    
    def test_default_unknown_field(self):
        """Test default value for unknown field."""
        assert _get_default_value("unknown_field") is None
