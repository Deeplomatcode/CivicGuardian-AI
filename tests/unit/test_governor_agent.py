"""
Unit tests for Governor Agent validation logic.
"""

import pytest
from src.governor_agent import (
    validate_policy_response,
    _check_grounding,
    _check_safety_notice,
    _check_confidence,
    _determine_approval,
    REQUIRED_SAFETY_NOTICE
)


class TestGroundingCheck:
    """Tests for citation grounding validation."""
    
    def test_all_citations_grounded(self):
        """Test that valid citations pass grounding check."""
        policy_output = {
            "citations": [
                "Eviction notice dated 2024-03-15",
                "Tenant must vacate property by 2024-04-15"
            ]
        }
        source_text = """
        Eviction notice dated 2024-03-15.
        Tenant must vacate property by 2024-04-15 due to rent arrears.
        """
        
        result = _check_grounding(policy_output, source_text)
        
        assert result["passed"] is True
        assert result["total_citations"] == 2
        assert result["valid_citations"] == 2
        assert result["invalid_citations"] == []
        assert result["errors"] == []
    
    def test_ungrounded_citation_fails(self):
        """Test that ungrounded citations fail grounding check."""
        policy_output = {
            "citations": [
                "This text does not appear in source",
                "Eviction notice dated 2024-03-15"
            ]
        }
        source_text = "Eviction notice dated 2024-03-15."
        
        result = _check_grounding(policy_output, source_text)
        
        assert result["passed"] is False
        assert result["total_citations"] == 2
        assert result["valid_citations"] == 1
        assert len(result["invalid_citations"]) == 1
        assert "This text does not appear in source" in result["invalid_citations"]
        assert len(result["errors"]) == 1
    
    def test_case_insensitive_matching(self):
        """Test that grounding check is case-insensitive."""
        policy_output = {
            "citations": ["EVICTION NOTICE"]
        }
        source_text = "eviction notice dated 2024-03-15"
        
        result = _check_grounding(policy_output, source_text)
        
        assert result["passed"] is True
        assert result["valid_citations"] == 1
    
    def test_whitespace_normalized_matching(self):
        """Test that grounding check normalizes whitespace."""
        policy_output = {
            "citations": ["Eviction    notice"]
        }
        source_text = "Eviction\nnotice\tdated 2024-03-15"
        
        result = _check_grounding(policy_output, source_text)
        
        assert result["passed"] is True
        assert result["valid_citations"] == 1
    
    def test_no_citations_passes(self):
        """Test that policy with no citations passes grounding check."""
        policy_output = {"citations": []}
        source_text = "Some text"
        
        result = _check_grounding(policy_output, source_text)
        
        assert result["passed"] is True
        assert result["total_citations"] == 0


class TestSafetyNoticeCheck:
    """Tests for safety notice validation."""
    
    def test_correct_safety_notice_passes(self):
        """Test that correct safety notice passes validation."""
        policy_output = {
            "safety_notice": REQUIRED_SAFETY_NOTICE
        }
        
        result = _check_safety_notice(policy_output)
        
        assert result["passed"] is True
        assert result["expected"] == REQUIRED_SAFETY_NOTICE
        assert result["actual"] == REQUIRED_SAFETY_NOTICE
        assert result["error"] is None
    
    def test_incorrect_safety_notice_fails(self):
        """Test that incorrect safety notice fails validation."""
        policy_output = {
            "safety_notice": "This is a draft"
        }
        
        result = _check_safety_notice(policy_output)
        
        assert result["passed"] is False
        assert result["error"] is not None
        assert "Incorrect safety notice" in result["error"]
    
    def test_missing_safety_notice_fails(self):
        """Test that missing safety notice fails validation."""
        policy_output = {}
        
        result = _check_safety_notice(policy_output)
        
        assert result["passed"] is False
        assert result["actual"] is None
        assert "Missing safety_notice field" in result["error"]


class TestConfidenceCheck:
    """Tests for confidence score validation."""
    
    def test_valid_confidence_passes(self):
        """Test that valid confidence score passes validation."""
        policy_output = {"confidence": 0.85}
        risk_data = {"risk_level": "MEDIUM"}
        
        result = _check_confidence(policy_output, risk_data)
        
        assert result["passed"] is True
        assert result["confidence"] == 0.85
        assert result["in_valid_range"] is True
        assert result["error"] is None
    
    def test_confidence_below_zero_fails(self):
        """Test that confidence < 0.0 fails validation."""
        policy_output = {"confidence": -0.1}
        risk_data = {"risk_level": "MEDIUM"}
        
        result = _check_confidence(policy_output, risk_data)
        
        assert result["passed"] is False
        assert result["in_valid_range"] is False
        assert "outside valid range" in result["error"]
    
    def test_confidence_above_one_fails(self):
        """Test that confidence > 1.0 fails validation."""
        policy_output = {"confidence": 1.5}
        risk_data = {"risk_level": "MEDIUM"}
        
        result = _check_confidence(policy_output, risk_data)
        
        assert result["passed"] is False
        assert result["in_valid_range"] is False
        assert "outside valid range" in result["error"]
    
    def test_missing_confidence_fails(self):
        """Test that missing confidence fails validation."""
        policy_output = {}
        risk_data = {"risk_level": "MEDIUM"}
        
        result = _check_confidence(policy_output, risk_data)
        
        assert result["passed"] is False
        assert result["confidence"] is None
        assert "Missing confidence field" in result["error"]
    
    def test_non_numeric_confidence_fails(self):
        """Test that non-numeric confidence fails validation."""
        policy_output = {"confidence": "high"}
        risk_data = {"risk_level": "MEDIUM"}
        
        result = _check_confidence(policy_output, risk_data)
        
        assert result["passed"] is False
        assert "must be a number" in result["error"]


class TestApprovalLogic:
    """Tests for approval and escalation logic."""
    
    def test_validation_failure_escalates(self):
        """Test that validation failure triggers escalation."""
        policy_output = {"confidence": 0.9}
        risk_data = {"risk_level": "MEDIUM"}
        grounding_result = {"passed": True}
        confidence_result = {"passed": True, "confidence": 0.9}
        
        result = _determine_approval(
            validation_passed=False,
            policy_output=policy_output,
            original_risk_data=risk_data,
            grounding_result=grounding_result,
            confidence_result=confidence_result
        )
        
        assert result["approved"] is False
        assert result["escalation_required"] is True
        assert "Validation checks failed" in result["escalation_reason"]
    
    def test_critical_risk_always_escalates(self):
        """Test that CRITICAL risk always requires escalation."""
        policy_output = {"confidence": 0.95}
        risk_data = {"risk_level": "CRITICAL"}
        grounding_result = {"passed": True}
        confidence_result = {"passed": True, "confidence": 0.95}
        
        result = _determine_approval(
            validation_passed=True,
            policy_output=policy_output,
            original_risk_data=risk_data,
            grounding_result=grounding_result,
            confidence_result=confidence_result
        )
        
        assert result["approved"] is False
        assert result["escalation_required"] is True
        assert "CRITICAL risk level" in result["escalation_reason"]
    
    def test_high_risk_low_confidence_escalates(self):
        """Test that HIGH risk with confidence < 0.7 escalates."""
        policy_output = {"confidence": 0.65}
        risk_data = {"risk_level": "HIGH"}
        grounding_result = {"passed": True}
        confidence_result = {"passed": True, "confidence": 0.65}
        
        result = _determine_approval(
            validation_passed=True,
            policy_output=policy_output,
            original_risk_data=risk_data,
            grounding_result=grounding_result,
            confidence_result=confidence_result
        )
        
        assert result["approved"] is False
        assert result["escalation_required"] is True
        assert "HIGH risk with low confidence" in result["escalation_reason"]
    
    def test_low_confidence_escalates(self):
        """Test that confidence < 0.5 triggers escalation."""
        policy_output = {"confidence": 0.4}
        risk_data = {"risk_level": "MEDIUM"}
        grounding_result = {"passed": True}
        confidence_result = {"passed": True, "confidence": 0.4}
        
        result = _determine_approval(
            validation_passed=True,
            policy_output=policy_output,
            original_risk_data=risk_data,
            grounding_result=grounding_result,
            confidence_result=confidence_result
        )
        
        assert result["approved"] is False
        assert result["escalation_required"] is True
        assert "Low confidence score" in result["escalation_reason"]
    
    def test_medium_risk_high_confidence_approves(self):
        """Test that MEDIUM risk with high confidence is approved."""
        policy_output = {"confidence": 0.85}
        risk_data = {"risk_level": "MEDIUM"}
        grounding_result = {"passed": True}
        confidence_result = {"passed": True, "confidence": 0.85}
        
        result = _determine_approval(
            validation_passed=True,
            policy_output=policy_output,
            original_risk_data=risk_data,
            grounding_result=grounding_result,
            confidence_result=confidence_result
        )
        
        assert result["approved"] is True
        assert result["escalation_required"] is False
        assert result["escalation_reason"] is None


class TestValidatePolicyResponse:
    """Integration tests for full validation pipeline."""
    
    def test_fully_valid_response_approved(self):
        """Test that a fully valid response is approved."""
        policy_output = {
            "citations": ["Eviction notice dated 2024-03-15"],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "confidence": 0.85
        }
        source_text = "Eviction notice dated 2024-03-15."
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        assert result["approved"] is True
        assert result["validation_passed"] is True
        assert result["escalation_required"] is False
        assert result["validation_errors"] == []
    
    def test_ungrounded_citation_rejected(self):
        """Test that ungrounded citations cause rejection."""
        policy_output = {
            "citations": ["This text is not in source"],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "confidence": 0.85
        }
        source_text = "Eviction notice dated 2024-03-15."
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        assert result["approved"] is False
        assert result["validation_passed"] is False
        assert result["escalation_required"] is True
        assert len(result["validation_errors"]) > 0
    
    def test_missing_safety_notice_rejected(self):
        """Test that missing safety notice causes rejection."""
        policy_output = {
            "citations": [],
            "confidence": 0.85
        }
        source_text = "Some text"
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        assert result["approved"] is False
        assert result["validation_passed"] is False
        assert result["escalation_required"] is True
        assert any("safety_notice" in err for err in result["validation_errors"])
    
    def test_invalid_confidence_rejected(self):
        """Test that invalid confidence causes rejection."""
        policy_output = {
            "citations": [],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "confidence": 1.5
        }
        source_text = "Some text"
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        assert result["approved"] is False
        assert result["validation_passed"] is False
        assert result["escalation_required"] is True
        assert any("outside valid range" in err for err in result["validation_errors"])
    
    def test_critical_risk_escalates_even_if_valid(self):
        """Test that CRITICAL risk escalates even with valid response."""
        policy_output = {
            "citations": [],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "confidence": 0.95
        }
        source_text = "Some text"
        risk_data = {"risk_level": "CRITICAL"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        assert result["approved"] is False
        assert result["validation_passed"] is True
        assert result["escalation_required"] is True
        assert "CRITICAL" in result["escalation_reason"]
