import json
import sys
import platform
import os
import traceback
from pathlib import Path
from datetime import datetime
try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
except ImportError:
    torch = None

def get_env():
    return {
        "os": platform.system(),
        "python_version": sys.version,
        "pytorch_version": torch.__version__ if torch else "N/A",
        "cuda_available": torch.cuda.is_available() if torch else False,
        "cuda_version": torch.version.cuda if torch and torch.cuda.is_available() else "N/A",
        "gpu_name": torch.cuda.get_device_name(0) if torch and torch.cuda.is_available() else "N/A",
    }

def main():
    base_dir = Path("Sahayak-AI/evaluation")
    out_dir = base_dir / "results_v2"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    env = get_env()
    with open(out_dir / "benchmark_environment.json", "w") as f:
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
        print(f"\nEvaluating {cand_id} ({repo})...")
        
        status = "NOT_EVALUATED"
        fail_reason = ""
        
        if not torch or not torch.cuda.is_available():
            status = "CUDA_FAILURE"
            fail_reason = "GPU environment unavailable"
        else:
            try:
                print(f"Attempting to download/load tokenizer and model for {repo}...")
                # Try to load tokenizer and model
                tokenizer = AutoTokenizer.from_pretrained(repo)
                model = AutoModelForCausalLM.from_pretrained(repo, device_map="auto")
                
                # If we get here, generate a test sequence
                inputs = tokenizer("Test", return_tensors="pt").to("cuda")
                outputs = model.generate(**inputs, max_new_tokens=5)
                generation_events_count += 1
                status = "VERIFIED_GENERATION"
            except Exception as e:
                err_str = str(e)
                print(f"Failed: {err_str}")
                if "401" in err_str or "404" in err_str or "not found" in err_str.lower() or "connection" in err_str.lower():
                    status = "DOWNLOAD_BLOCKED"
                    fail_reason = f"Repository not found or network blocked: {err_str}"
                elif "OutOfMemory" in err_str:
                    status = "VRAM_INSUFFICIENT"
                    fail_reason = "CUDA Out of Memory"
                else:
                    status = "MODEL_LOAD_FAILURE"
                    fail_reason = traceback.format_exc()

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
        
        if status not in ["VERIFIED_GENERATION"]:
            failures.append({
                "model": repo,
                "failure_type": status,
                "reason": fail_reason,
                "timestamp": datetime.now().isoformat()
            })
            
        raw_dir = base_dir / f"raw_outputs/{cand_id}_v2"
        raw_dir.mkdir(parents=True, exist_ok=True)
        open(raw_dir / "generation_events.jsonl", "w").close()
        
    with open(out_dir / "candidate_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    with open(base_dir / "failures/failure_analysis_v2.json", "w") as f:
        json.dump(failures, f, indent=2)
        
    print(f"\nTotal verified generation events: {generation_events_count}")
    if generation_events_count == 0:
        print("ZERO-GENERATION GUARD TRIGGERED.")
        print("Benchmark Status: INCONCLUSIVE")
        
if __name__ == "__main__":
    main()
