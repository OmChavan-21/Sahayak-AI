import sys
import os
from pathlib import Path
from training.environment_check import check_environment
from training.dataset_loader import DatasetLoader
from training.trainer_config import TrainingConfig
from training.experiment_tracker import ExperimentTracker

def main():
    print("--- Sahayak OS Phase 15 SFT Pipeline ---")
    
    # 0. EXPLICIT EXECUTION LOCK
    if os.environ.get("SAHAYAK_ALLOW_TRAINING_EXECUTION") != "TRUE":
        print("FATAL: Training execution lock is ACTIVE.")
        print("Set SAHAYAK_ALLOW_TRAINING_EXECUTION=TRUE to explicitly authorize training.")
        sys.exit(1)
        
    config = TrainingConfig()
    
    # 1. Environment validation
    if not check_environment(config.method.upper()):
        print("FATAL: Environment validation failed. Cannot proceed with training.")
        sys.exit(1)
        
    # 2. Config & Tracking
    tracker = ExperimentTracker("Sahayak-AI/experiments")
    exp_dir = tracker.create_experiment(config)
    print(f"Created experiment directory: {exp_dir}")
    
    # 3. Dataset loading
    try:
        loader = DatasetLoader("Sahayak-AI/dataset/training/v0_3")
        train_data = loader.load_split("train")
        val_data = loader.load_split("val")
        print(f"Loaded {len(train_data)} train examples and {len(val_data)} validation examples.")
    except Exception as e:
        print(f"FATAL: Dataset loading failed: {e}")
        sys.exit(1)
        
    # 4. Model checks
    if config.model_id == "placeholder_due_to_inconclusive_benchmark":
        print("\n[BLOCKED] Phase 13B Benchmark was INCONCLUSIVE.")
        print("No valid base model has been selected. The SFT Pipeline is structurally ready.")
        print("Aborting before weight download or expensive training loops.")
        sys.exit(0)
        
    # 5. Training Loop (Placeholder for future actual execution)
    print("Beginning training loop...")
    # adapter = QwenCandidateAdapter() ...
    
if __name__ == "__main__":
    main()
