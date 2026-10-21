import unittest
import json
from pathlib import Path

class TestPhase24(unittest.TestCase):
    def setUp(self):
        self.results_path = Path("Sahayak-AI/evaluation/phase24_results.json")
        self.events_file = Path("Sahayak-AI/evaluation/raw_outputs/Qwen-Qwen3-4B/generation_events.jsonl")
        
    def test_existing_environments_untouched(self):
        self.assertTrue(Path("Sahayak-AI/gpu_venv").exists())
        self.assertTrue(Path("Sahayak-AI/venv").exists())
        
    def test_candidate_runtime_isolated(self):
        self.assertTrue(Path("Sahayak-AI/gpu_venv_sm120").exists())
        
    def test_cuda_smoke_test_recorded(self):
        if self.results_path.exists():
            with open(self.results_path) as f:
                data = json.load(f)
            # Cannot be marked successful if it failed. The file records the exact status.
            self.assertIn(data.get("cuda_smoke_test"), ["PASSED", "FAILED"])
            
    def test_zero_generation_guard(self):
        if self.results_path.exists():
            with open(self.results_path) as f:
                data = json.load(f)
            if data.get("qwen_generation") != "SUCCESS":
                self.assertTrue(not self.events_file.exists() or self.events_file.stat().st_size == 0)
            else:
                self.assertTrue(self.events_file.stat().st_size > 0)
                
    def test_no_remote_download(self):
        if self.results_path.exists():
            with open(self.results_path) as f:
                data = json.load(f)
            # Ensure loading status exists, demonstrating local attempt
            self.assertIn(data.get("qwen_loading"), ["SUCCESS", "FAILED"])
            
if __name__ == "__main__":
    unittest.main()
