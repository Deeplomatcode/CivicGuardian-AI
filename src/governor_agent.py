"""
Governor Agent - Validation and approval logic for policy responses.

This module provides validation functions to verify policy responses from the
Policy Reasoner Agent, including grounding checks, safety validation, confidence
scoring, and approval/escalation logic.
"""

from typing import Dict, List, Any


REQUIRED_SAFETY_NOTICE = "DRAFT FOR REVIEW - Not legal advice"


def validate_policy_response(
    policy_output: Dict[str, Any],
    source_text: str,
    original_risk_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Validates a policy response from the Policy Reasoner Agent.
    
    Args:
        policy_output: The policy response dict from Policy Reasoner Agent
        source_text: The original document text
        original_risk_data: The risk assessment data used to generate the policy
    
    Returns:
        dict: Validation result with structure:
            {
                "approved": bool,
                "validation_passed": bool,
                "grounding_check": dict,
                "safety_check": dict,
                "confidence_check": dict,
                "escalation_required": bool,
                "escalation_reason": str or None,
                "validation_errors": list[str]
            }
    """
    validation_errors = []
    
    # Run all validation checks
    grounding_result = _check_grounding(policy_output, source_text)
    safety_result = _check_safety_notice(policy_output)
    confidence_result = _check_confidence(policy_output, original_risk_data)
    
    # Collect errors
    if not grounding_result["passed"]:
        validation_errors.extend(grounding_result["errors"])
    if not safety_result["passed"]:
        validation_errors.append(safety_result["error"])
    if not confidence_result["passed"]:
        validation_errors.append(confidence_result["error"])
    
    # Determine if validation passed
    validation_passed = (
        grounding_result["passed"] and
        safety_result["passed"] and
        confidence_result["passed"]
    )
    
    # Determine approval and escalation
    approval_result = _determine_approval(
        validation_passed,
        policy_output,
        original_risk_data,
        grounding_result,
        confidence_result
    )
    
    return {
        "approved": approval_result["approved"],
        "validation_passed": validation_passed,
        "grounding_check": grounding_result,
        "safety_check": safety_result,
        "confidence_check": confidence_result,
        "escalation_required": approval_result["escalation_required"],
        "escalation_reason": approval_result["escalation_reason"],
        "validation_errors": validation_errors
    }


def _check_grounding(policy_output: Dict[str, Any], source_text: str) -> Dict[str, Any]:
    """
    Checks if all citations in the policy response are grounded in the source text.
    
    Args:
        policy_output: The policy response dict
        source_text: The original document text
    
    Returns:
        dict: {
            "passed": bool,
            "total_citations": int,
            "valid_citations": int,
            "invalid_citations": list[str],
            "errors": list[str]
        }
    """
    citations = policy_output.get("citations", [])
    
    if not citations:
        return {
            "passed": True,
            "total_citations": 0,
            "valid_citations": 0,
            "invalid_citations": [],
            "errors": []
        }
    
    # Normalize source text for comparison
    source_normalized = " ".join(source_text.split()).lower()
    
    invalid_citations = []
    for citation in citations:
        citation_normalized = " ".join(citation.split()).lower()
        if citation_normalized not in source_normalized:
            invalid_citations.append(citation)
    
    valid_count = len(citations) - len(invalid_citations)
    passed = len(invalid_citations) == 0
    
    errors = []
    if not passed:
        errors.append(f"Found {len(invalid_citations)} ungrounded citation(s)")
    
    return {
        "passed": passed,
        "total_citations": len(citations),
        "valid_citations": valid_count,
        "invalid_citations": invalid_citations,
        "errors": errors
    }


def _check_safety_notice(policy_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Checks if the policy response contains the exact required safety notice.
    
    Args:
        policy_output: The policy response dict
    
    Returns:
        dict: {
            "passed": bool,
            "expected": str,
            "actual": str or None,
            "error": str or None
        }
    """
    actual_notice = policy_output.get("safety_notice")
    passed = actual_notice == REQUIRED_SAFETY_NOTICE
    
    error = None
    if not passed:
        if actual_notice is None:
            error = "Missing safety_notice field"
        else:
            error = f"Incorrect safety notice: expected '{REQUIRED_SAFETY_NOTICE}', got '{actual_notice}'"
    
    return {
        "passed": passed,
        "expected": REQUIRED_SAFETY_NOTICE,
        "actual": actual_notice,
        "error": error
    }


def _check_confidence(
    policy_output: Dict[str, Any],
    original_risk_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Checks if the confidence score is valid and appropriate for the risk level.
    
    Args:
        policy_output: The policy response dict
        original_risk_data: The risk assessment data
    
    Returns:
        dict: {
            "passed": bool,
            "confidence": float or None,
            "in_valid_range": bool,
            "risk_level": str,
            "error": str or None
        }
    """
    confidence = policy_output.get("confidence")
    risk_level = original_risk_data.get("risk_level", "UNKNOWN")
    
    # Check if confidence exists and is a number
    if confidence is None:
        return {
            "passed": False,
            "confidence": None,
            "in_valid_range": False,
            "risk_level": risk_level,
            "error": "Missing confidence field"
        }
    
    if not isinstance(confidence, (int, float)):
        return {
            "passed": False,
            "confidence": confidence,
            "in_valid_range": False,
            "risk_level": risk_level,
            "error": f"Confidence must be a number, got {type(confidence).__name__}"
        }
    
    # Check if confidence is in valid range [0.0, 1.0]
    in_valid_range = 0.0 <= confidence <= 1.0
    
    if not in_valid_range:
        return {
            "passed": False,
            "confidence": confidence,
            "in_valid_range": False,
            "risk_level": risk_level,
            "error": f"Confidence {confidence} outside valid range [0.0, 1.0]"
        }
    
    return {
        "passed": True,
        "confidence": confidence,
        "in_valid_range": True,
        "risk_level": risk_level,
        "error": None
    }


def _determine_approval(
    validation_passed: bool,
    policy_output: Dict[str, Any],
    original_risk_data: Dict[str, Any],
    grounding_result: Dict[str, Any],
    confidence_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Determines if the policy response should be approved or escalated.
    
    Approval logic:
    - If validation failed: not approved, escalate
    - If CRITICAL risk: always escalate for human review
    - If HIGH risk and confidence < 0.7: escalate
    - If confidence < 0.5: escalate
    - Otherwise: approve
    
    Args:
        validation_passed: Whether all validation checks passed
        policy_output: The policy response dict
        original_risk_data: The risk assessment data
        grounding_result: Result from grounding check
        confidence_result: Result from confidence check
    
    Returns:
        dict: {
            "approved": bool,
            "escalation_required": bool,
            "escalation_reason": str or None
        }
    """
    risk_level = original_risk_data.get("risk_level", "UNKNOWN")
    confidence = confidence_result.get("confidence", 0.0)
    
    # If validation failed, escalate
    if not validation_passed:
        return {
            "approved": False,
            "escalation_required": True,
            "escalation_reason": "Validation checks failed"
        }
    
    # CRITICAL risk always requires human review
    if risk_level == "CRITICAL":
        return {
            "approved": False,
            "escalation_required": True,
            "escalation_reason": "CRITICAL risk level requires human review"
        }
    
    # HIGH risk with low confidence requires escalation
    if risk_level == "HIGH" and confidence < 0.7:
        return {
            "approved": False,
            "escalation_required": True,
            "escalation_reason": f"HIGH risk with low confidence ({confidence:.2f})"
        }
    
    # Low confidence requires escalation
    if confidence < 0.5:
        return {
            "approved": False,
            "escalation_required": True,
            "escalation_reason": f"Low confidence score ({confidence:.2f})"
        }
    
    # All checks passed, approve
    return {
        "approved": True,
        "escalation_required": False,
        "escalation_reason": None
    }
