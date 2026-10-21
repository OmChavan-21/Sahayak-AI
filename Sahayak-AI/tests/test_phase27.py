import unittest
import json
import os
import subprocess
from pathlib import Path

class TestPhase27(unittest.TestCase):
    def test_dataset_counts_and_separation(self):
        train = Path("Sahayak-AI/dataset/training/v0_3/sahayak_v0_3_sft_train.jsonl")
        val = Path("Sahayak-AI/dataset/training/v0_3/sahayak_v0_3_sft_val.jsonl")
        test = Path("Sahayak-AI/dataset/training/v0_3/sahayak_v0_3_sft_test.jsonl")
        
        train_count = sum(1 for _ in open(train, "r", encoding="utf-8"))
        val_count = sum(1 for _ in open(val, "r", encoding="utf-8"))
        test_count = sum(1 for _ in open(test, "r", encoding="utf-8"))
        
        self.assertEqual(train_count, 802)
        self.assertEqual(val_count, 171)
        self.assertEqual(test_count, 173)
        self.assertEqual(train_count + val_count + test_count, 1146)
        
        # Family separation check
        train_families = set(json.loads(line)["metadata"]["scenario_family_id"] for line in open(train, "r", encoding="utf-8"))
        val_families = set(json.loads(line)["metadata"]["scenario_family_id"] for line in open(val, "r", encoding="utf-8"))
        test_families = set(json.loads(line)["metadata"]["scenario_family_id"] for line in open(test, "r", encoding="utf-8"))
        
        self.assertTrue(train_families.isdisjoint(val_families))
        self.assertTrue(train_families.isdisjoint(test_families))
        self.assertTrue(val_families.isdisjoint(test_families))
        
    def test_dataset_manifest(self):
        manifest = Path("Sahayak-AI/dataset/manifests/v0.3_manifest.json")
        self.assertTrue(manifest.exists())
        with open(manifest, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIn("files", data)
            self.assertIn("split_manifest", data)

    def test_training_execution_lock(self):
        # Even with environment variables, test that we can't run the file natively from test
        os.environ["SAHAYAK_ALLOW_TRAINING_EXECUTION"] = "FALSE"
        res = subprocess.run(["python", "Sahayak-AI/training/train_sft.py"], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0)
        
    def test_hardware_gate_preservation(self):
        env_chk = Path("Sahayak-AI/training/environment_check.py")
        content = env_chk.read_text()
        self.assertIn("TrainingMethodProfile", content)
        self.assertIn("FULL", content)
        self.assertIn("QLORA", content)
        
    def test_phi_and_qwen_status(self):
        qwen = Path("Sahayak-AI/models/verified/Qwen3-4B")
        phi = Path("Sahayak-AI/models/verified/Phi-4-mini")
        self.assertTrue(qwen.exists())
        self.assertFalse(phi.exists())

if __name__ == "__main__":
    unittest.main()
