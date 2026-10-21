import unittest
import json
from pathlib import Path

class TestPhase25(unittest.TestCase):
    def setUp(self):
        self.summary_path = Path("Sahayak-AI/evaluation/phase25/benchmark_summary.json")
        self.qwen_events_file = Path("Sahayak-AI/evaluation/phase25/raw_outputs/Qwen-Qwen3-4B/generation_events.jsonl")
        
    def test_summary_exists(self):
        self.assertTrue(self.summary_path.exists())
        
    def test_model_identity_and_local_loading(self):
        with open(self.summary_path) as f:
            data = json.load(f)
        qwen = data["models"].get("Qwen/Qwen3-4B")
        self.assertIsNotNone(qwen)
        self.assertEqual(qwen.get("identity"), "VERIFIED")
        self.assertEqual(qwen.get("local_weights"), "PRESENT")
        
    def test_zero_generation_guard(self):
        with open(self.summary_path) as f:
            data = json.load(f)
        qwen = data["models"].get("Qwen/Qwen3-4B")
        if qwen.get("generation") == "VERIFIED":
            self.assertTrue(self.qwen_events_file.exists())
            with open(self.qwen_events_file) as f:
                lines = f.readlines()
            self.assertTrue(len(lines) > 0)
            self.assertEqual(len(lines), qwen.get("generation_events"))
            
    def test_no_overall_ranking(self):
        with open(self.summary_path) as f:
            data = json.load(f)
        self.assertNotIn("winner", data)
        self.assertNotIn("best_model", data)
        self.assertNotIn("overall_score", data)
        self.assertNotIn("ranking", data)
        
    def test_independent_dimensions(self):
        with open(self.summary_path) as f:
            data = json.load(f)
        qwen = data["models"].get("Qwen/Qwen3-4B")
        dims = qwen.get("dimensions", {})
        self.assertIn("Structured Output", dims)
        self.assertIn("Safe Next Action", dims)
        
    def test_phi4_missing(self):
        with open(self.summary_path) as f:
            data = json.load(f)
        phi = data["models"].get("microsoft/Phi-4-mini")
        self.assertIsNotNone(phi)
        self.assertEqual(phi.get("local_weights"), "MISSING")
        self.assertIn(phi.get("generation"), ["NOT_ATTEMPTED", "FAILED"])
        
if __name__ == "__main__":
    unittest.main()
