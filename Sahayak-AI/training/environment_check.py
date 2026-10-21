import sys
from pathlib import Path
import json

class TrainingMethodProfile:
    def __init__(self, method, min_vram, min_ram, supported_precision, requires_quantization, desc):
        self.method = method
        self.min_vram = min_vram
        self.min_ram = min_ram
        self.supported_precision = supported_precision
        self.requires_quantization = requires_quantization
        self.desc = desc

PROFILES = {
    "FULL": TrainingMethodProfile("FULL", 24.0, 32.0, "bfloat16", False, "Full fine-tuning requires keeping all optimizer states, gradients, and parameters in VRAM."),
    "LORA": TrainingMethodProfile("LORA", 16.0, 24.0, "bfloat16", False, "LoRA reduces trainable parameters but still requires base model weights and activations in unquantized precision."),
    "QLORA": TrainingMethodProfile("QLORA", 6.0, 16.0, "nf4", True, "QLoRA loads the base model in 4-bit precision, significantly reducing VRAM requirements.")
}

def check_environment(method_name: str = "QLORA"):
    print(f"Running Environment Validation for method: {method_name}...")
    errors = []
    
    if method_name not in PROFILES:
        print(f"FATAL: Unknown method {method_name}")
        return False
        
    profile = PROFILES[method_name]
    
    # 1. Global Safety Gate: Hardware basics
    if sys.version_info < (3, 8):
        errors.append("Python version must be >= 3.8")
        
    try:
        import torch
        if not torch.cuda.is_available():
            errors.append("CUDA is not available. GPU is required for training.")
            vram = 0.0
        else:
            vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            # GLOBAL GATE: Absolutely no training allowed with < 4GB VRAM
            if vram < 4.0:
                errors.append(f"Global hardware gate failed: Insufficient VRAM ({vram:.2f}GB < 4.0GB minimum).")
            
            # PROFILE GATE
            if vram < profile.min_vram:
                errors.append(f"Profile {method_name} hardware gate failed: Insufficient VRAM ({vram:.2f}GB < {profile.min_vram}GB required).")
    except ImportError:
        errors.append("PyTorch is not installed.")
            
    try:
        import psutil
        ram = psutil.virtual_memory().total / (1024**3)
        # GLOBAL GATE: Absolutely no training allowed with < 8GB RAM
        if ram < 8.0:
            errors.append(f"Global hardware gate failed: Insufficient RAM ({ram:.2f}GB < 8.0GB minimum).")
        # PROFILE GATE
        if ram < profile.min_ram:
            errors.append(f"Profile {method_name} hardware gate failed: Insufficient RAM ({ram:.2f}GB < {profile.min_ram}GB required).")
    except ImportError:
        errors.append("psutil is not installed (cannot verify RAM).")
        
    # Check Dataset
    base_dir = Path("Sahayak-AI/dataset/training/v0_3")
    required_splits = ["sahayak_v0_3_sft_train.jsonl", "sahayak_v0_3_sft_val.jsonl", "sahayak_v0_3_sft_test.jsonl"]
    for split in required_splits:
        if not (base_dir / split).exists():
            errors.append(f"Missing dataset split: {split}")
            
    if errors:
        print("ENVIRONMENT VALIDATION FAILED:")
        for e in errors:
            print(f" - {e}")
        return False
        
    print("Environment validation passed.")
    return True

if __name__ == "__main__":
    check_environment()
