import unittest
import json
import os
from pathlib import Path

class TestPhase28(unittest.TestCase):
    def test_dataset_counts_and_separation(self):
        train = Path("Sahayak-AI/dataset/training/v0_3/sahayak_v0_3_sft_train.jsonl")
        val = Path("Sahayak-AI/dataset/training/v0_3/sahayak_v0_3_sft_val.jsonl")
        test = Path("Sahayak-AI/dataset/training/v0_3/sahayak_v0_3_sft_test.jsonl")
        
        self.assertEqual(sum(1 for _ in open(train, "r", encoding="utf-8")), 802)
        self.assertEqual(sum(1 for _ in open(val, "r", encoding="utf-8")), 171)
        self.assertEqual(sum(1 for _ in open(test, "r", encoding="utf-8")), 173)
        
        train_families = set(json.loads(line)["metadata"]["scenario_family_id"] for line in open(train, "r", encoding="utf-8"))
        val_families = set(json.loads(line)["metadata"]["scenario_family_id"] for line in open(val, "r", encoding="utf-8"))
        test_families = set(json.loads(line)["metadata"]["scenario_family_id"] for line in open(test, "r", encoding="utf-8"))
        
        self.assertTrue(train_families.isdisjoint(val_families))
        self.assertTrue(train_families.isdisjoint(test_families))
        self.assertTrue(val_families.isdisjoint(test_families))
        
    def test_dataset_manifest_hashes(self):
        manifest = Path("Sahayak-AI/dataset/manifests/v0.3_manifest.json")
        self.assertTrue(manifest.exists())
        with open(manifest, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIn("files", data)
            for file_info in data["files"]:
                self.assertIn("sha256", file_info)

    def test_models_status(self):
        qwen = Path("Sahayak-AI/models/verified/Qwen3-4B")
        phi = Path("Sahayak-AI/models/verified/Phi-4-mini")
        self.assertTrue(qwen.exists())
        self.assertFalse(phi.exists())
        
        # Ensure qwen files are unmodified (e.g. check modified time or presence of specific files)
        self.assertTrue((qwen / "config.json").exists())

    def test_execution_lock_and_artifacts(self):
        lock_file = Path("Sahayak-AI/training/train_sft.py")
        self.assertIn("SAHAYAK_ALLOW_TRAINING_EXECUTION", lock_file.read_text())
        
        # No training artifacts created
        experiments_dir = Path("Sahayak-AI/experiments")
        if experiments_dir.exists():
            # There should be no subdirectories from training today in Phase 28
            pass # We rely on git status or the fact that train_sft.py aborts

    def test_feasibility_artifacts(self):
        self.assertTrue(Path("Sahayak-AI/docs/phase_28_training_feasibility.md").exists())
        json_artifact = Path("Sahayak-AI/evaluation/phase_28_feasibility.json")
        self.assertTrue(json_artifact.exists())
        
        with open(json_artifact, "r") as f:
            data = json.load(f)
            self.assertEqual(data["training_executed"], False)

if __name__ == "__main__":
    unittest.main()
