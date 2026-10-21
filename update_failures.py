import json
from pathlib import Path

base_dir = Path("Sahayak-AI/benchmark_results")
failures = [
    {
        "model": "Qwen/Qwen2.5-3B-Instruct",
        "test_id": "ALL_TESTS",
        "input_category": "ALL",
        "expected_behavior": "Download model weights and evaluate Sahayak schemas.",
        "actual_output": "Hugging Face LFS (safetensors) download timed out/blocked at 0 bytes.",
        "failure_category": "NETWORK_LFS_BLOCK",
        "severity": "CRITICAL",
        "could_be_fixed_by_finetuning": False
    },
    {
        "model": "microsoft/Phi-4-mini-instruct",
        "test_id": "ALL_TESTS",
        "input_category": "ALL",
        "expected_behavior": "Download model weights and evaluate Sahayak schemas.",
        "actual_output": "Hugging Face LFS (safetensors) download timed out/blocked at 0 bytes.",
        "failure_category": "NETWORK_LFS_BLOCK",
        "severity": "CRITICAL",
        "could_be_fixed_by_finetuning": False
    }
]

with open(base_dir / "failure_analysis" / "failures.json", "w") as f:
    json.dump(failures, f, indent=2)

with open(base_dir / "README.md", "a") as f:
    f.write("\n## Phase 13B.1 Network Limitation Update\n")
    f.write("A real local inference environment (`.venv` with `torch 2.14`, `transformers 5.17`, and `accelerate`) was successfully established using `uv`. However, execution of the final benchmark on `Qwen2.5-3B-Instruct` and `Phi-4-mini-instruct` was forcibly aborted because the host network blocks or drops HuggingFace Large File Storage (LFS) `.safetensors` downloads (0 bytes downloaded after multiple minutes). Per strict Sahayak AI protocol, these limitations are recorded as a critical failure rather than fabricating data.")
