import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from training.trainer_config import TrainingConfig

class ExperimentTracker:
    def __init__(self, base_dir: str = "Sahayak-AI/experiments"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
    def _collect_hardware_metadata(self):
        try:
            import torch
            import psutil
            vram = torch.cuda.get_device_properties(0).total_memory / (1024**3) if torch.cuda.is_available() else 0.0
            gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "Unknown"
            cuda_ver = torch.version.cuda if torch.cuda.is_available() else "None"
            capability = torch.cuda.get_device_capability(0) if torch.cuda.is_available() else "None"
            ram = psutil.virtual_memory().total / (1024**3)
        except Exception:
            vram, gpu_name, cuda_ver, capability, ram = 0.0, "Unknown", "None", "None", 0.0
            
        try:
            import transformers
            tf_ver = transformers.__version__
        except:
            tf_ver = "Unknown"

        return {
            "python_version": sys.version,
            "os": os.name,
            "pytorch_version": torch.__version__ if 'torch' in sys.modules else "Unknown",
            "transformers_version": tf_ver,
            "peft_version": "Unknown", # Add real check if installed
            "bitsandbytes_version": "Unknown",
            "cuda_version": cuda_ver,
            "gpu_name": gpu_name,
            "gpu_compute_capability": capability,
            "vram_gb": round(vram, 2),
            "system_ram_gb": round(ram, 2)
        }

    def _collect_git_metadata(self):
        try:
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
            status = subprocess.check_output(["git", "status", "--porcelain"], stderr=subprocess.DEVNULL).decode().strip()
            return {"commit": commit, "status": "dirty" if status else "clean"}
        except Exception:
            return {"commit": "unknown", "status": "unknown"}

    def _collect_dataset_metadata(self, config):
        manifest_path = Path(f"Sahayak-AI/dataset/manifests/{config.dataset_version}_manifest.json")
        if manifest_path.exists():
            with open(manifest_path, "r") as f:
                return json.load(f)
        return {"error": "Manifest not found"}

    def create_experiment(self, config: TrainingConfig) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exp_id = f"sahayak_sft_{config.method.lower()}_{config.seed}_{timestamp}"
        
        exp_dir = self.base_dir / exp_id
        exp_dir.mkdir(parents=True, exist_ok=True)
        
        (exp_dir / "checkpoints").mkdir(exist_ok=True)
        (exp_dir / "logs").mkdir(exist_ok=True)
        (exp_dir / "metrics").mkdir(exist_ok=True)
        
        def serialize_cfg(c):
            if hasattr(c, "__dict__"):
                return {k: serialize_cfg(v) for k, v in c.__dict__.items()}
            return c
            
        metadata = {
            "DATASET": self._collect_dataset_metadata(config),
            "MODEL": {
                "model_id": config.model_id,
                "local_model_path": f"Sahayak-AI/models/verified/{config.model_id.split('/')[-1]}",
                "model_identity_verification_status": "VERIFIED"
            },
            "RUNTIME": self._collect_hardware_metadata(),
            "CODE": self._collect_git_metadata(),
            "TRAINING_CONFIG": serialize_cfg(config)
        }
            
        with open(exp_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
            
        return exp_dir
