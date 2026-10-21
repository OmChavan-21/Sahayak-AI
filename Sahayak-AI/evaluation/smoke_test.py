import json
import time
import platform
import hashlib
from datetime import datetime
from pathlib import Path

def get_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def main():
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as e:
        print(f"RUNTIME_DEPENDENCY_MISSING: {e}")
        return
        
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # We use sshleifer/tiny-gpt2 (approx 2MB) as a minimal local test fixture
    # to prove the pipeline: tokenizer -> model -> device -> generation -> captured output
    model_id = "sshleifer/tiny-gpt2"
    
    start_time = time.time()
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id).to(device)
    except Exception as e:
        print(f"Failed to load model {model_id}: {e}")
        return
        
    prompt = "This is a local inference test."
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    try:
        outputs = model.generate(**inputs, max_new_tokens=5, do_sample=False)
        output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Generation failed: {e}")
        return
        
    latency = time.time() - start_time
    print(f"Generated text: {output_text}")
    
    result = {
        "model_identifier": model_id,
        "model_revision": "main",
        "runtime": f"PyTorch {torch.__version__}",
        "device": device,
        "input_hash": get_hash(prompt),
        "output_hash": get_hash(output_text),
        "output_token_count": len(outputs[0]),
        "generation_parameters": {"max_new_tokens": 5, "do_sample": False},
        "latency_seconds": latency,
        "timestamp": datetime.now().isoformat(),
        "environment_identifier": platform.node()
    }
    
    out_file = Path("Sahayak-AI/evaluation/runtime_smoke_test.json")
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
        
    print(f"Smoke test successful. Results saved to {out_file}")

if __name__ == "__main__":
    main()
