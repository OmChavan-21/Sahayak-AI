import json
import sys
import platform
import os
from pathlib import Path
from datetime import datetime

def check_env():
    env = {
        "os": platform.system(),
        "python_version": platform.python_version(),
        "pytorch_version": "NOT_INSTALLED",
        "transformers_version": "NOT_INSTALLED",
        "cuda_available": False,
        "cuda_version": "N/A",
        "gpu_name": "N/A",
        "gpu_vram": "N/A",
        "system_ram": "N/A",
        "cpu": platform.processor(),
    }
    
    try:
        import psutil
        env["system_ram"] = f"{psutil.virtual_memory().total / (1024**3):.2f} GB"
    except ImportError:
        pass
        
    try:
        import torch
        env["pytorch_version"] = torch.__version__
        env["cuda_available"] = torch.cuda.is_available()
        if env["cuda_available"]:
            env["cuda_version"] = torch.version.cuda
            env["gpu_name"] = torch.cuda.get_device_name(0)
            env["gpu_vram"] = f"{torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB"
    except ImportError:
        pass
        
    try:
        import transformers
        env["transformers_version"] = transformers.__version__
    except ImportError:
        pass
        
    return env

def main():
    base_dir = Path("Sahayak-AI/evaluation")
    
    # 1. Env Check
    env = check_env()
    with open(base_dir / "results/benchmark_environment.json", "w") as f:
        json.dump(env, f, indent=2)
        
    candidates = [
        {"id": "Qwen3-4B", "official_repo": "Qwen/Qwen3-4B"},
        {"id": "Phi-4-mini", "official_repo": "microsoft/Phi-4-mini"}
    ]
    
    results = {}
    failures = []
    
    generation_events_count = 0
    
    for cand in candidates:
        cand_id = cand["id"]
        repo = cand["official_repo"]
        print(f"Evaluating {cand_id}...")
        
        status = "NOT_EVALUATED"
        fail_reason = ""
        
        if env["pytorch_version"] == "NOT_INSTALLED":
            status = "RUNTIME_INCOMPATIBILITY"
            fail_reason = "PyTorch not installed. Local runtime unavailable."
        elif not env["cuda_available"]:
            status = "CUDA_FAILURE"
            fail_reason = "No CUDA GPU detected for local inference."
            
        results[cand_id] = {
            "exact_model_identifier": repo,
            "download_status": status,
            "load_status": status,
            "generation_status": status,
            "structured_output_validity": "N/A",
            "evidence_grounding": "N/A",
            "uncertainty_behavior": "N/A",
            "prompt_injection_behavior": "N/A",
            "capability_safety": "N/A",
            "trust_behavior": "N/A",
            "hallucination_observations": "N/A",
            "safe_next_action_behavior": "N/A",
            "multilingual_observations": "N/A",
            "performance_measurements": "N/A",
            "known_failures": fail_reason
        }
        
        if status != "GENERATED_SUCCESSFULLY":
            failures.append({
                "model": repo,
                "failure_type": status,
                "reason": fail_reason,
                "timestamp": datetime.now().isoformat()
            })
            
        raw_dir = base_dir / f"raw_outputs/{cand_id}"
        raw_dir.mkdir(parents=True, exist_ok=True)
        # Empty generation file
        open(raw_dir / "generation_events.jsonl", "w").close()
        
    with open(base_dir / "results/candidate_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    with open(base_dir / "failures/failure_analysis.json", "w") as f:
        json.dump(failures, f, indent=2)
        
    with open(base_dir / "raw_outputs/generation_events.jsonl", "w") as f:
        pass # Overall empty file
        
    # ZERO-GENERATION GUARD
    if generation_events_count == 0:
        print("ZERO-GENERATION GUARD TRIGGERED.")
        print("Benchmark Status: INCONCLUSIVE")
        
if __name__ == "__main__":
    main()
