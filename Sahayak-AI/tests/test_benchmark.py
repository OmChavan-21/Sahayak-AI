import unittest
import json
from pathlib import Path

class TestPhase16Benchmark(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path("Sahayak-AI/evaluation")
        
    def test_environment_captured(self):
        env_file = self.base_dir / "results/benchmark_environment.json"
        self.assertTrue(env_file.exists())
        with open(env_file, "r") as f:
            env = json.load(f)
            self.assertIn("pytorch_version", env)
            
    def test_zero_generation_guard(self):
        gen_file = self.base_dir / "raw_outputs/generation_events.jsonl"
        self.assertTrue(gen_file.exists())
        # Should be empty
        self.assertEqual(gen_file.stat().st_size, 0)
        
    def test_candidate_results(self):
        res_file = self.base_dir / "results/candidate_results.json"
        self.assertTrue(res_file.exists())
        with open(res_file, "r") as f:
            res = json.load(f)
            self.assertIn("Qwen3-4B", res)
            self.assertIn("Phi-4-mini", res)
            self.assertEqual(res["Qwen3-4B"]["download_status"], "RUNTIME_INCOMPATIBILITY")

if __name__ == "__main__":
    unittest.main()
