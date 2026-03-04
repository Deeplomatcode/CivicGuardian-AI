"""
Governor Validation Agent - Pure Python validation layer for policy responses.

This module provides validation functions to verify policy responses from the
Policy Reasoner Agent, including grounding checks, safety validation, confidence
scoring, and approval/escalation logic.

No AWS/boto3 dependencies - pure Python validation logic.
"""

from typing import Dict, List, Any


REQUIRED_SAFETY_NOTICE = "DRAFT FOR REVIEW - Not legal advice"

PROHIBITED_PHRASES = [
    "legally required",
    "you are legally required",
    "this guarantees",
    "certainly",
    "will be upheld",
    "must comply"
]


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
                "validation_status": str,  # "APPROVED" or "FLAGGED" or "VETOED"
                "confidence_score": float,  # 0.0 to 1.0
                "grounding_check": {
                    "citations_valid": bool,
                    "hallucination_detected": bool
                },
                "safety_check": {
                    "contains_draft_notice": bool,
                    "no_definitive_claims": bool
                },
                "issues_found": list[str],
                "approved": bool,
                "required_escalation": bool
            }
    """
    issues_found = []
    
    # 1. GROUNDING CHECK
    grounding_result = _check_grounding(policy_output, source_text, issues_found)
    citations_valid = grounding_result["citations_valid"]
    hallucination_detected = grounding_result["hallucination_detected"]
    
    # 2. SAFETY CHECK
    safety_result = _check_safety(policy_output, issues_found)
    contains_draft_notice = safety_result["contains_draft_notice"]
    no_definitive_claims = safety_result["no_definitive_claims"]
    
    # 3. CONFIDENCE SCORING
    confidence_score = policy_output.get("confidence", 0.0)
    
    if hallucination_detected:
        confidence_score -= 0.2
        if "Hallucination detected" not in issues_found:
            issues_found.append("Hallucination detected")
    
    if not contains_draft_notice:
        confidence_score -= 0.1
    
    if not no_definitive_claims:
        confidence_score -= 0.15
    
    # Clamp to [0.0, 1.0]
    confidence_score = max(0.0, min(1.0, confidence_score))
    
    # 4. APPROVAL LOGIC
    # Check confidence threshold BEFORE degradation for VETOED vs FLAGGED distinction
    original_confidence = policy_output.get("confidence", 0.0)
    
    if hallucination_detected or original_confidence < 0.75:
        validation_status = "VETOED"
        approved = False
        if confidence_score < 0.75 and "Confidence below threshold (0.75)" not in issues_found:
            issues_found.append("Confidence below threshold (0.75)")
    elif not contains_draft_notice or not no_definitive_claims:
        validation_status = "FLAGGED"
        approved = False
    else:
        validation_status = "APPROVED"
        approved = True
    
    # 5. ESCALATION LOGIC
    original_risk_level = original_risk_data.get("risk_level", "UNKNOWN")
    required_escalation = (
        original_risk_level in ["HIGH", "CRITICAL"] or
        validation_status == "VETOED"
    )
    
    return {
        "validation_status": validation_status,
        "confidence_score": confidence_score,
        "grounding_check": {
            "citations_valid": citations_valid,
            "hallucination_detected": hallucination_detected
        },
        "safety_check": {
            "contains_draft_notice": contains_draft_notice,
            "no_definitive_claims": no_definitive_claims
        },
        "issues_found": issues_found,
        "approved": approved,
        "required_escalation": required_escalation
    }


def _check_grounding(
    policy_output: Dict[str, Any],
    source_text: str,
    issues_found: List[str]
) -> Dict[str, bool]:
    """
    Checks if all citations in the policy response are grounded in the source text.
    
    Args:
        policy_output: The policy response dict
        source_text: The original document text
        issues_found: List to append issues to
    
    Returns:
        dict: {
            "citations_valid": bool,
            "hallucination_detected": bool
        }
    """
    citations = policy_output.get("citations", [])
    
    if not citations:
        return {
            "citations_valid": True,
            "hallucination_detected": False
        }
    
    # Normalize source text for comparison
    source_normalized = source_text.lower()
    
    hallucination_detected = False
    for citation in citations:
        citation_normalized = citation.lower()
        if citation_normalized not in source_normalized:
            hallucination_detected = True
            issues_found.append(f"Citation quote not found in source: {citation}")
    
    citations_valid = not hallucination_detected
    
    return {
        "citations_valid": citations_valid,
        "hallucination_detected": hallucination_detected
    }


def _check_safety(
    policy_output: Dict[str, Any],
    issues_found: List[str]
) -> Dict[str, bool]:
    """
    Checks if the policy response contains the exact required safety notice
    and does not contain prohibited definitive language.
    
    Args:
        policy_output: The policy response dict
        issues_found: List to append issues to
    
    Returns:
        dict: {
            "contains_draft_notice": bool,
            "no_definitive_claims": bool
        }
    """
    # Check safety notice
    actual_notice = policy_output.get("safety_notice")
    contains_draft_notice = actual_notice == REQUIRED_SAFETY_NOTICE
    
    if not contains_draft_notice:
        issues_found.append("Missing or incorrect safety notice")
    
    # Check for prohibited definitive language
    draft_response = policy_output.get("draft_response", "")
    draft_response_lower = draft_response.lower()
    
    no_definitive_claims = True
    for phrase in PROHIBITED_PHRASES:
        if phrase in draft_response_lower:
            no_definitive_claims = False
            issues_found.append(f"Definitive legal language detected: {phrase}")
    
    return {
        "contains_draft_notice": contains_draft_notice,
        "no_definitive_claims": no_definitive_claims
    }
