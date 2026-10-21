import unittest
from dataset.schema.sahayak_schema import (
    SahayakAITask, SahayakAIConfidence, SahayakCapability, 
    TrustLevel, TrainingExample, SahayakAIRequest, SahayakAIResponse,
    SahayakAISecurityContext
)

class TestSahayakSchema(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "input_context": {
                "task": "ASSESS_SECURITY",
                "security_context": {
                    "deterministic_risk_level": "HIGH_RISK",
                    "security_indicators": ["urgency", "suspicious_link"]
                },
                "observed_evidence": [{"type": "URL", "value": "http://bad.com", "sourceSnippet": "Click here: http://bad.com"}],
                "untrusted_content": "Your account is locked. Click here: http://bad.com",
                "trust_level": "LEVEL_0_UNTRUSTED_EXTERNAL"
            },
            "expected_output": {
                "assessment": "The message attempts to steal credentials.",
                "explanation": "The urgency combined with a non-standard HTTP link indicates a phishing attempt.",
                "evidence_references": ["urgency", "http://bad.com"],
                "confidence": "HIGH_CONFIDENCE",
                "recommended_next_step": "Do not click the link and delete the message.",
                "requested_capability": "INSPECT_URL",
                "capability_reason": "Inspect the URL to confirm it is a phishing site if the user wants proof."
            }
        }

    def test_valid_example_accepted(self):
        example = TrainingExample.from_dict(self.valid_data)
        self.assertEqual(example.input_context.task, SahayakAITask.ASSESS_SECURITY)
        self.assertEqual(example.expected_output.confidence, SahayakAIConfidence.HIGH_CONFIDENCE)
        self.assertEqual(example.expected_output.requested_capability, SahayakCapability.INSPECT_URL)

    def test_missing_required_field_rejected(self):
        del self.valid_data['expected_output']['confidence']
        with self.assertRaises(KeyError):
            TrainingExample.from_dict(self.valid_data)
            
    def test_invalid_confidence_rejected(self):
        self.valid_data['expected_output']['confidence'] = "95%"
        with self.assertRaises(ValueError):
            TrainingExample.from_dict(self.valid_data)

    def test_invalid_capability_rejected(self):
        self.valid_data['expected_output']['requested_capability'] = "HACK_DEVICE"
        with self.assertRaises(ValueError):
            TrainingExample.from_dict(self.valid_data)
            
    def test_untrusted_content_field_exists(self):
        example = TrainingExample.from_dict(self.valid_data)
        self.assertEqual(example.input_context.untrusted_content, "Your account is locked. Click here: http://bad.com")
        
    def test_capability_request_is_declarative(self):
        example = TrainingExample.from_dict(self.valid_data)
        self.assertNotEqual(example.expected_output.requested_capability, "execute INSPECT_URL")
        self.assertEqual(example.expected_output.requested_capability, SahayakCapability.INSPECT_URL)

if __name__ == '__main__':
    unittest.main()
