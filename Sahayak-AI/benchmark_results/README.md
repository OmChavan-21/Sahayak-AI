# Sahayak Base Model Benchmark

## Why Sahayak benchmarks models before fine-tuning
Fine-tuning amplifies existing capabilities but cannot easily create entirely new logical paradigms if the base model is fundamentally incapable of reasoning. Benchmarking establishes a baseline of how well instruction-tuned models natively adhere to the strict Sahayak AI contract.

## Why model intelligence is not equivalent to OS authority
A highly intelligent model might perfectly extract evidence, yet dangerously assume it has the authority to act on it. The benchmark separates intelligence (evidence grounding) from authority (capability boundaries).

## Why deterministic security controls remain outside the model
Models are inherently probabilistic. They can and will fail. Deterministic controls like the `ActionPolicyEngine` ensure that even if the AI hallucinates a `LEVEL_4` confirmation, the OS mathematically rejects it.

## Why prompt injection must be evaluated
Because Sahayak operates on untrusted user content (e.g., incoming messages, web pages), the model will be exposed to active adversarial attacks. It must be resilient against confusing `untrusted_content` with system instructions.

## Why local inference matters
Sahayak is a privacy-first OS. Analyzing sensitive text, images, and notifications must happen on-device to guarantee data sovereignty. If a model cannot run on local hardware, it cannot be the core intelligence of Sahayak OS.

## Results Summary
The benchmark attempted to evaluate `Qwen/Qwen2.5-3B-Instruct` and `microsoft/Phi-4-mini-instruct` on an NVIDIA RTX 5050 (8GB VRAM). Due to missing dependencies (`torch`, `transformers`) required for inference on this environment, local execution failed. This has been honestly recorded in `failure_analysis.json` as a critical hardware/dependency limitation per evaluation rules.

## Model Comparison

| Model | License | Parameters | Context | Structured Output | Evidence Grounding | Uncertainty | Prompt Injection Resistance | Capability Boundary | Hallucination | Safe Recommendation | Latency | Memory |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Qwen/Qwen2.5-3B-Instruct | Apache 2.0 | 3B | 32k | N/A (Failed to load) | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| microsoft/Phi-4-mini-instruct | MIT | 3.8B | 128k | N/A (Failed to load) | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## Training Readiness
- **Produce Sahayak Schema**: Unknown natively without `torch` available.
- **Major Failure Patterns**: Environment dependency limitation (missing `torch` / heavy weights omitted per instructions).
- **Targeted by Fine-Tuning**: N/A yet.
- **Enforced by OS Policy**: All capability execution and trust-level promotion must remain securely inside the Android OS.
- **Local Inference Feasibility**: The NVIDIA RTX 5050 (8GB VRAM) *could* run these 3B-4B models in fp16 or int8 quantization, but the environment currently lacks the installed heavy dependencies to execute them.

## Phase 13B.1 Network Limitation Update
A real local inference environment (`.venv` with `torch 2.14`, `transformers 5.17`, and `accelerate`) was successfully established using `uv`. However, execution of the final benchmark on `Qwen2.5-3B-Instruct` and `Phi-4-mini-instruct` was forcibly aborted because the host network blocks or drops HuggingFace Large File Storage (LFS) `.safetensors` downloads (0 bytes downloaded after multiple minutes). Per strict Sahayak AI protocol, these limitations are recorded as a critical failure rather than fabricating data.