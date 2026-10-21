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
    except ImportError as e:
        print(f"FAILED: Could not import torch: {e}")
        return
        
    result = {
        "python_version": platform.python_version(),
        "pytorch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "gpu_tensor_test": "N/A",
        "smoke_test_successful": False,
        "timestamp": datetime.now().isoformat()
    }
    
    if torch.cuda.is_available():
        result["cuda_version"] = torch.version.cuda
        result["gpu_count"] = torch.cuda.device_count()
        result["gpu_name"] = torch.cuda.get_device_name(0)
        
        # Test basic tensor op
        try:
            a = torch.randn(10, 10).to("cuda")
            b = torch.randn(10, 10).to("cuda")
            c = torch.matmul(a, b)
            result["gpu_tensor_test"] = "SUCCESS"
            
            # Record VRAM usage
            result["vram_allocated_gb"] = round(torch.cuda.memory_allocated(0) / (1024**3), 4)
            result["vram_reserved_gb"] = round(torch.cuda.memory_reserved(0) / (1024**3), 4)
            
        except Exception as e:
            result["gpu_tensor_test"] = f"FAILED: {e}"
            
        # Run tiny model on GPU
        if result["gpu_tensor_test"] == "SUCCESS":
            try:
                from transformers import AutoModelForCausalLM, AutoTokenizer
                model_id = "sshleifer/tiny-gpt2"
                tokenizer = AutoTokenizer.from_pretrained(model_id)
                model = AutoModelForCausalLM.from_pretrained(model_id).to("cuda")
                
                prompt = "This is a GPU test."
                inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
                outputs = model.generate(**inputs, max_new_tokens=5, do_sample=False)
                output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
                
                result["smoke_test_successful"] = True
                result["smoke_test_output"] = output_text
                result["smoke_test_output_hash"] = get_hash(output_text)
                
            except Exception as e:
                result["smoke_test_error"] = str(e)
    else:
        print("CUDA is NOT available in this environment.")
        
    out_file = Path("Sahayak-AI/evaluation/gpu_runtime_test.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
        
    print(f"GPU Test completed. Results saved to {out_file}")

if __name__ == "__main__":
    main()
