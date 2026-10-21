import unittest
from pathlib import Path
from training.dataset_loader import DatasetLoader
from training.trainer_config import TrainingConfig
from training.experiment_tracker import ExperimentTracker

class TestPipeline(unittest.TestCase):
    def test_dataset_loader(self):
        loader = DatasetLoader(Path("Sahayak-AI/dataset/training/v0_3"))
        train_data = loader.load_split("train")
        self.assertTrue(len(train_data) > 0)
        
        # Check prompt format
        first = train_data[0]
        self.assertIn("<|system|>", first["prompt"])
        self.assertIn("Task:", first["prompt"])
        
    def test_config(self):
        cfg = TrainingConfig(method="QLoRA")
        self.assertIsNotNone(cfg.quantization)
        self.assertIsNotNone(cfg.lora)
        
    def test_experiment_tracker(self):
        tracker = ExperimentTracker(Path("Sahayak-AI/experiments"))
        cfg = TrainingConfig()
        exp_dir = tracker.create_experiment(cfg)
        self.assertTrue(exp_dir.exists())
        self.assertTrue((exp_dir / "configs.json").exists())

if __name__ == "__main__":
    unittest.main()
