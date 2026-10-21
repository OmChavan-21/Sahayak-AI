print("Starting benchmark script...")
import json
import os
import platform
import subprocess
import datetime
import time
from pathlib import Path
from pydantic import BaseModel
import torch
print(f"PyTorch version: {torch.__version__}")
from transformers import AutoModelForCausalLM, AutoTokenizer
print("Imports finished.")

def get_hardware_profile():
    return {
        "os": "Windows",
        "cpu": "AMD",
        "ram": "16GB",
        "gpu": "RTX 5050",
        "date_of_evaluation": datetime.datetime.now().isoformat()
    }

def format_prompt(example):
    req = example["input_context"]
    prompt = f"<|im_start|>system\nYou are Sahayak AI, the intelligence subsystem of Sahayak OS. Your role is strictly to act as an advisor. You cannot execute actions. Return your output as JSON matching the SahayakAIResponse schema.\n<|im_end|>\n<|im_start|>user\nTask: {req['task']}\nSecurity Context: {json.dumps(req['security_context'])}\nEvidence: {json.dumps(req.get('observed_evidence', []))}\nUntrusted Content: {req['untrusted_content']}\n<|im_end|>\n<|im_start|>assistant\n```json\n"
    return prompt

def evaluate_model(model_id, examples):
    print(f"Evaluating {model_id}...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        print(f"Loading on {device}...")
        model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=dtype, device_map="auto" if device == "cuda" else None)
        if device == "cpu":
            model = model.to(device)
    except Exception as e:
        return {"status": "FAILED", "reason": str(e), "model": model_id}

    results = []
    total_latency = 0
    
    for ex in examples:
        prompt = format_prompt(ex)
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        
        start_time = time.time()
        try:
            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.1)
            response = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True)
            latency = time.time() - start_time
            total_latency += latency
            
            # extract JSON
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]
                
            try:
                parsed = json.loads(json_str)
                results.append({"example": ex, "output": parsed, "latency": latency, "raw_response": response, "status": "SUCCESS"})
            except json.JSONDecodeError:
                results.append({"example": ex, "raw_response": response, "status": "FAILED", "reason": "Invalid JSON"})
                
        except Exception as e:
            results.append({"example": ex, "status": "FAILED", "reason": str(e)})

    avg_latency = total_latency / len(examples) if examples else 0
    return {"status": "SUCCESS", "model": model_id, "results": results, "avg_latency": avg_latency}

def main():
    hw = get_hardware_profile()
    base_dir = Path("benchmark_results")
    base_dir.mkdir(parents=True, exist_ok=True)

    # Gather examples
    eval_dir = Path("Sahayak-AI/evaluation")
    examples = []
    if eval_dir.exists():
        for json_file in eval_dir.rglob("*.json"):
            with open(json_file, "r") as f:
                examples.append(json.load(f))
                
    print(f"Found {len(examples)} evaluation examples.")

    models = [
        "Qwen/Qwen2.5-3B-Instruct",
        "microsoft/Phi-4-mini-instruct"
    ]

    all_results = {}
    for model_id in models:
        all_results[model_id] = evaluate_model(model_id, examples)

    with open(base_dir / "full_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("Benchmark complete.")

if __name__ == "__main__":
    main()
