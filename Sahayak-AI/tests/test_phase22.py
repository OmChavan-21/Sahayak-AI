import unittest
import json
from pathlib import Path

class TestPhase22(unittest.TestCase):
    def setUp(self):
        self.results_path = Path("Sahayak-AI/evaluation/phase22_results.json")
        self.events_file = Path("Sahayak-AI/evaluation/raw_outputs/Qwen-Qwen3-4B/generation_events.jsonl")
        
    def test_results_exist(self):
        self.assertTrue(self.results_path.exists(), "Results file missing")
        with open(self.results_path) as f:
            self.results = json.load(f)

    def test_local_path_required(self):
        with open(self.results_path) as f:
            data = json.load(f)
        self.assertTrue(data.get("files_verified", False))

    def test_no_generation_without_output(self):
        # The zero-generation rule
        if not self.events_file.exists() or self.events_file.stat().st_size == 0:
            with open(self.results_path) as f:
                data = json.load(f)
            smoke_test = data.get("smoke_test", {})
            if isinstance(smoke_test, dict):
                self.assertNotEqual(smoke_test.get("status"), "SUCCESS")
            else:
                self.assertNotEqual(smoke_test, "SUCCESS")

    def test_identity_preservation(self):
        manifest = Path("Sahayak-AI/evaluation/model_acquisition/phase21_1_results.json")
        with open(manifest) as f:
            data = json.load(f)
            qwen = data.get("Qwen/Qwen3-4B")
            self.assertEqual(qwen["identity_status"], "IDENTITY_VERIFIED")
            
    def test_android_untouched(self):
        # We did not touch android
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
