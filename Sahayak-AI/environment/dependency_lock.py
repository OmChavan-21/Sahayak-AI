import platform
import os
import sys
import json
import psutil
try:
    import torch
except ImportError:
    torch = None
try:
    import transformers
except ImportError:
    transformers = None
try:
    import accelerate
except ImportError:
    accelerate = None

def get_env():
    env = {
        "os": platform.system(),
        "os_release": platform.release(),
        "python_version": sys.version,
        "python_executable": sys.executable,
        "cpu": platform.processor(),
        "system_ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "virtual_env": os.environ.get("VIRTUAL_ENV", "None"),
        "pytorch": {
            "installed": torch is not None,
            "version": torch.__version__ if torch else "N/A",
            "cuda_available": torch.cuda.is_available() if torch else False,
            "cuda_version": torch.version.cuda if torch and torch.cuda.is_available() else "N/A",
            "gpu_count": torch.cuda.device_count() if torch and torch.cuda.is_available() else 0,
            "gpu_name": torch.cuda.get_device_name(0) if torch and torch.cuda.is_available() else "N/A",
            "vram_gb": round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2) if torch and torch.cuda.is_available() else "N/A",
        },
        "transformers": {
            "installed": transformers is not None,
            "version": transformers.__version__ if transformers else "N/A"
        },
        "accelerate": {
            "installed": accelerate is not None,
            "version": accelerate.__version__ if accelerate else "N/A"
        }
    }
    return env

if __name__ == "__main__":
    env = get_env()
    with open("Sahayak-AI/environment/phase_17_environment.json", "w") as f:
        json.dump(env, f, indent=2)
    print("Saved environment details to phase_17_environment.json")
