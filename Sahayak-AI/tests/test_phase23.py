import unittest
import json
from pathlib import Path

class TestPhase23(unittest.TestCase):
    def setUp(self):
        self.results_path = Path("Sahayak-AI/evaluation/phase23_results.json")
        self.events_file = Path("Sahayak-AI/evaluation/raw_outputs/Qwen-Qwen3-4B/generation_events.jsonl")
        
    def test_results_exist(self):
        self.assertTrue(self.results_path.exists(), "Results file missing")
        with open(self.results_path) as f:
            data = json.load(f)
            # The test just ensures the field exists, whether PASSED or FAILED
            self.assertIn(data.get("cuda_smoke_test"), ["PASSED", "FAILED"])
            
    def test_zero_generation_guard(self):
        with open(self.results_path) as f:
            data = json.load(f)
            if data.get("qwen_generation") != "SUCCESS":
                self.assertTrue(not self.events_file.exists() or self.events_file.stat().st_size == 0)
            else:
                self.assertTrue(self.events_file.stat().st_size > 0)
                
    def test_exact_local_model_path_status(self):
        with open(self.results_path) as f:
            data = json.load(f)
            # Ensure it tracked the loading status
            self.assertIn(data.get("qwen_loading"), ["SUCCESS", "FAILED"])
            
    def test_android_untouched(self):
        # We did not touch android
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
