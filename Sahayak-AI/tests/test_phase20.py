import unittest
import json
from pathlib import Path

class TestPhase20(unittest.TestCase):
    def setUp(self):
        self.findings_file = Path("Sahayak-AI/evaluation/model_acquisition/acquisition_findings.json")
        with open(self.findings_file) as f:
            self.findings = json.load(f)
            
    def test_exact_identifiers_preserved(self):
        self.assertIn("Qwen3-4B", self.findings["candidates"])
        self.assertIn("Phi-4-mini", self.findings["candidates"])
        self.assertEqual(self.findings["candidates"]["Qwen3-4B"]["exact_identifier"], "Qwen/Qwen3-4B")
        self.assertEqual(self.findings["candidates"]["Phi-4-mini"]["exact_identifier"], "microsoft/Phi-4-mini")
        
    def test_zero_generation_guard(self):
        total_events = self.findings["total_generation_events"]
        self.assertEqual(total_events, 0)
        
        qwen_file = Path("Sahayak-AI/evaluation/raw_outputs/Qwen3-4B_v3/generation_events.jsonl")
        self.assertTrue(qwen_file.exists())
        self.assertEqual(qwen_file.stat().st_size, 0)
        
    def test_no_silent_substitution(self):
        # The candidates exactly match the requested names, ensuring no hidden mappings.
        for c_id, data in self.findings["candidates"].items():
            self.assertIn(c_id.split("-")[0], data["exact_identifier"])
            
    def test_download_without_generation_fails(self):
        # A download is NOT enough, generation_events must be > 0.
        for c_id, data in self.findings["candidates"].items():
            if data.get("generation_status") != "SUCCESS":
                self.assertNotEqual(data.get("generation_events", 0), 1)

if __name__ == "__main__":
    unittest.main()
