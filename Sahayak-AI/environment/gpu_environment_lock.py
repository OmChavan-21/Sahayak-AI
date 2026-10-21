import platform
import os
import sys
import json
import psutil
import subprocess

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
        "python_version": sys.version,
        "python_executable": sys.executable,
        "virtual_env": os.environ.get("VIRTUAL_ENV", "None"),
        "pytorch": {
            "installed": torch is not None,
            "version": torch.__version__ if torch else "N/A",
            "cuda_available": torch.cuda.is_available() if torch else False,
            "cuda_version": torch.version.cuda if torch and torch.cuda.is_available() else "N/A",
            "gpu_name": torch.cuda.get_device_name(0) if torch and torch.cuda.is_available() else "N/A",
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
    
    try:
        smi_out = subprocess.check_output(["nvidia-smi", "--query-gpu=driver_version,memory.total", "--format=csv,noheader,nounits"], text=True).strip().split(",")
        env["nvidia_driver_version"] = smi_out[0].strip()
        env["gpu_vram_total_mb"] = smi_out[1].strip()
    except Exception:
        env["nvidia_driver_version"] = "N/A"
        
    return env

if __name__ == "__main__":
    env = get_env()
    with open("Sahayak-AI/environment/gpu_environment.json", "w") as f:
        json.dump(env, f, indent=2)
    print("Saved GPU environment details to gpu_environment.json")
