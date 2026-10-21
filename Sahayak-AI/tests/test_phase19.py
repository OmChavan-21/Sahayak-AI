import unittest
import json
from pathlib import Path

class TestPhase19(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path("Sahayak-AI/evaluation")
        
    def test_zero_generation_enforcement(self):
        # We know Qwen3-4B and Phi-4-mini do not exist or failed to load
        # Ensure generation events are perfectly 0 for Qwen
        qwen_file = self.base_dir / "raw_outputs/Qwen3-4B_v2/generation_events.jsonl"
        self.assertTrue(qwen_file.exists())
        self.assertEqual(qwen_file.stat().st_size, 0)
        
        # Ensure generation events are perfectly 0 for Phi
        phi_file = self.base_dir / "raw_outputs/Phi-4-mini_v2/generation_events.jsonl"
        self.assertTrue(phi_file.exists())
        self.assertEqual(phi_file.stat().st_size, 0)
        
    def test_results_metadata(self):
        res_file = self.base_dir / "results_v2/candidate_results.json"
        self.assertTrue(res_file.exists())
        with open(res_file, "r") as f:
            res = json.load(f)
            self.assertIn("Qwen3-4B", res)
            self.assertIn("Phi-4-mini", res)
            # Verify no metrics were fabricated
            self.assertEqual(res["Qwen3-4B"]["structured_output_validity"], "N/A")

if __name__ == "__main__":
    unittest.main()
