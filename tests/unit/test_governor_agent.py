"""
Unit tests for Governor Validation Agent.
"""

import unittest
from src.governor_agent import validate_policy_response, REQUIRED_SAFETY_NOTICE


class TestGovernorAgent(unittest.TestCase):
    """Tests for Governor validation logic."""
    
    def test_valid_output_approved(self):
        """Test that all checks pass results in APPROVED with approved=True."""
        policy_output = {
            "citations": ["Eviction notice dated 2024-03-15"],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "draft_response": "We recommend contacting housing support services.",
            "confidence": 0.85
        }
        source_text = "Eviction notice dated 2024-03-15. Tenant must vacate."
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        self.assertEqual(result["validation_status"], "APPROVED")
        self.assertTrue(result["approved"])
        self.assertTrue(result["grounding_check"]["citations_valid"])
        self.assertFalse(result["grounding_check"]["hallucination_detected"])
        self.assertTrue(result["safety_check"]["contains_draft_notice"])
        self.assertTrue(result["safety_check"]["no_definitive_claims"])
        self.assertEqual(result["issues_found"], [])
        self.assertFalse(result["required_escalation"])
    
    def test_missing_citation_quote_vetoed(self):
        """Test that quote not in source results in VETOED with hallucination=True."""
        policy_output = {
            "citations": ["This text does not appear in source"],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "draft_response": "Contact support services.",
            "confidence": 0.85
        }
        source_text = "Eviction notice dated 2024-03-15."
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        self.assertEqual(result["validation_status"], "VETOED")
        self.assertFalse(result["approved"])
        self.assertFalse(result["grounding_check"]["citations_valid"])
        self.assertTrue(result["grounding_check"]["hallucination_detected"])
        self.assertIn("Citation quote not found in source", result["issues_found"][0])
        self.assertTrue(result["required_escalation"])
    
    def test_hallucination_detected(self):
        """Test that fabricated quote sets hallucination_detected=True."""
        policy_output = {
            "citations": ["Fabricated quote that doesn't exist"],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "draft_response": "Contact support.",
            "confidence": 0.9
        }
        source_text = "Real document text here."
        risk_data = {"risk_level": "LOW"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        self.assertTrue(result["grounding_check"]["hallucination_detected"])
        self.assertFalse(result["grounding_check"]["citations_valid"])
        self.assertEqual(result["validation_status"], "VETOED")
    
    def test_incorrect_safety_notice_flagged(self):
        """Test that wrong notice string results in FLAGGED."""
        policy_output = {
            "citations": [],
            "safety_notice": "This is a draft",
            "draft_response": "Contact support services.",
            "confidence": 0.85
        }
        source_text = "Some text"
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        self.assertEqual(result["validation_status"], "FLAGGED")
        self.assertFalse(result["approved"])
        self.assertFalse(result["safety_check"]["contains_draft_notice"])
        self.assertIn("Missing or incorrect safety notice", result["issues_found"])
    
    def test_definitive_language_flagged(self):
        """Test that 'must comply' in draft results in FLAGGED with no_definitive_claims=False."""
        policy_output = {
            "citations": [],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "draft_response": "You must comply with this requirement immediately.",
            "confidence": 0.85
        }
        source_text = "Some text"
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        self.assertEqual(result["validation_status"], "FLAGGED")
        self.assertFalse(result["approved"])
        self.assertFalse(result["safety_check"]["no_definitive_claims"])
        self.assertIn("Definitive legal language detected: must comply", result["issues_found"])
    
    def test_low_confidence_vetoed(self):
        """Test that policy confidence=0.6 results in VETOED."""
        policy_output = {
            "citations": [],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "draft_response": "Contact support services.",
            "confidence": 0.6
        }
        source_text = "Some text"
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        self.assertEqual(result["validation_status"], "VETOED")
        self.assertFalse(result["approved"])
        self.assertLess(result["confidence_score"], 0.75)
        self.assertIn("Confidence below threshold (0.75)", result["issues_found"])
    
    def test_critical_risk_approved_still_escalates(self):
        """Test that CRITICAL + APPROVED results in required_escalation=True."""
        policy_output = {
            "citations": [],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "draft_response": "Contact support services.",
            "confidence": 0.95
        }
        source_text = "Some text"
        risk_data = {"risk_level": "CRITICAL"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        self.assertEqual(result["validation_status"], "APPROVED")
        self.assertTrue(result["approved"])
        self.assertTrue(result["required_escalation"])
    
    def test_high_risk_approved_still_escalates(self):
        """Test that HIGH + APPROVED results in required_escalation=True."""
        policy_output = {
            "citations": [],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "draft_response": "Contact support services.",
            "confidence": 0.85
        }
        source_text = "Some text"
        risk_data = {"risk_level": "HIGH"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        self.assertEqual(result["validation_status"], "APPROVED")
        self.assertTrue(result["approved"])
        self.assertTrue(result["required_escalation"])
    
    def test_medium_risk_approved_no_escalation(self):
        """Test that MEDIUM + APPROVED results in required_escalation=False."""
        policy_output = {
            "citations": [],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "draft_response": "Contact support services.",
            "confidence": 0.85
        }
        source_text = "Some text"
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        self.assertEqual(result["validation_status"], "APPROVED")
        self.assertTrue(result["approved"])
        self.assertFalse(result["required_escalation"])
    
    def test_vetoed_always_escalates(self):
        """Test that LOW + VETOED results in required_escalation=True."""
        policy_output = {
            "citations": ["Fake quote"],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "draft_response": "Contact support.",
            "confidence": 0.85
        }
        source_text = "Real text"
        risk_data = {"risk_level": "LOW"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        self.assertEqual(result["validation_status"], "VETOED")
        self.assertFalse(result["approved"])
        self.assertTrue(result["required_escalation"])
    
    def test_confidence_degradation(self):
        """Test that hallucination reduces score by 0.2."""
        policy_output = {
            "citations": ["Fake quote"],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "draft_response": "Contact support.",
            "confidence": 0.9
        }
        source_text = "Real text"
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        # 0.9 - 0.2 (hallucination) = 0.7
        self.assertAlmostEqual(result["confidence_score"], 0.7, places=2)
        self.assertTrue(result["grounding_check"]["hallucination_detected"])
    
    def test_issues_found_populated(self):
        """Test that issues_found contains specific strings."""
        policy_output = {
            "citations": ["Fake quote"],
            "safety_notice": "Wrong notice",
            "draft_response": "You are legally required to comply.",
            "confidence": 0.6
        }
        source_text = "Real text"
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        self.assertGreater(len(result["issues_found"]), 0)
        self.assertTrue(any("Citation quote not found" in issue for issue in result["issues_found"]))
        self.assertIn("Missing or incorrect safety notice", result["issues_found"])
        self.assertTrue(any("Definitive legal language detected" in issue for issue in result["issues_found"]))
        self.assertIn("Confidence below threshold (0.75)", result["issues_found"])
    
    def test_multiple_prohibited_phrases(self):
        """Test detection of multiple prohibited phrases."""
        policy_output = {
            "citations": [],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "draft_response": "This guarantees success and you are legally required to act.",
            "confidence": 0.85
        }
        source_text = "Some text"
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        self.assertEqual(result["validation_status"], "FLAGGED")
        self.assertFalse(result["safety_check"]["no_definitive_claims"])
        # Should detect both "this guarantees" and "you are legally required"
        definitive_issues = [issue for issue in result["issues_found"] if "Definitive legal language" in issue]
        self.assertGreaterEqual(len(definitive_issues), 2)
    
    def test_confidence_clamping_lower_bound(self):
        """Test that confidence score is clamped to 0.0 minimum."""
        policy_output = {
            "citations": ["Fake quote"],
            "safety_notice": "Wrong",
            "draft_response": "You must comply.",
            "confidence": 0.3
        }
        source_text = "Real text"
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        # 0.3 - 0.2 (hallucination) - 0.1 (no notice) - 0.15 (definitive) = -0.15 → clamped to 0.0
        self.assertGreaterEqual(result["confidence_score"], 0.0)
        self.assertLessEqual(result["confidence_score"], 1.0)
    
    def test_confidence_clamping_upper_bound(self):
        """Test that confidence score is clamped to 1.0 maximum."""
        policy_output = {
            "citations": [],
            "safety_notice": REQUIRED_SAFETY_NOTICE,
            "draft_response": "Contact support services.",
            "confidence": 1.5  # Invalid high value
        }
        source_text = "Some text"
        risk_data = {"risk_level": "MEDIUM"}
        
        result = validate_policy_response(policy_output, source_text, risk_data)
        
        self.assertLessEqual(result["confidence_score"], 1.0)
        self.assertGreaterEqual(result["confidence_score"], 0.0)


if __name__ == '__main__':
    unittest.main()
