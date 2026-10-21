# Phase 20 — Exact Model Acquisition & Local Loading Recovery

## 1. Environment Verification
The GPU environment (`gpu_venv`) was successfully re-verified:
- **Python Version:** 3.12.10
- **PyTorch Version:** 2.4.1+cu124
- **Transformers Version:** 5.17.0
- **CUDA Availability:** VERIFIED (12.4)
- **GPU:** NVIDIA GeForce RTX 5050 (8GB VRAM)
- **CPU Environment:** Preserved intact in `Sahayak-AI/venv`.

## 2. Model Acquisition Findings
Strict candidate identification was enforced. Substitutions were firmly rejected. 

### Candidate A: `Qwen/Qwen3-4B`
- **Repository Reachable:** Yes
- **Metadata Obtainable:** Yes
- **Weights Obtainable:** No (Timed out / Access blocked)
- **Memory Feasibility:** MARGINAL_REQUIRES_QUANTIZATION (An 8GB GPU cannot comfortably load a 4B FP16 model with full KV Cache overhead without 4-bit or 8-bit quantization).
- **Load Status:** FAILED
- **Failure Classification:** `DOWNLOAD_BLOCKED`

### Candidate B: `microsoft/Phi-4-mini`
- **Repository Reachable:** Yes
- **Metadata Obtainable:** Yes
- **Weights Obtainable:** No (Timed out / Access blocked)
- **Memory Feasibility:** MARGINAL_REQUIRES_QUANTIZATION
- **Load Status:** FAILED
- **Failure Classification:** `DOWNLOAD_BLOCKED`

## 3. Actual Generation Evidence
**Zero Generation Events.** The strict *Zero-Generation Guard* prevented fabricated outputs or subjective metrics from being recorded. `Sahayak-AI/evaluation/raw_outputs/Qwen3-4B_v3/generation_events.jsonl` and the corresponding `Phi-4-mini_v3` log are mathematically 0 bytes.

## 4. Test Results
Automated tests (`test_phase20.py`) confirmed:
1. Exact model identifiers were preserved (No silent substitution).
2. Cloud inference APIs were systematically rejected.
3. Zero-generation state correctly evaluates as `NO VERIFIED GENERATION`.
4. Tests successfully executed without error (`Ran 4 tests in 0.001s, OK`).

## 5. Phase Reconciliation Table

| Phase | Description | Candidates | Generation Events | Result |
|---|---|---|---|---|
| **13B** | Original Baseline Test | Unknown/Ambiguous | 0 | INCONCLUSIVE |
| **16** | Local Benchmark | Qwen3-4B / Phi-4-mini | 0 | INCONCLUSIVE |
| **19** | Benchmark Retry (GPU) | `Qwen/Qwen3-4B`, `microsoft/Phi-4-mini` | 0 | INCONCLUSIVE |
| **20** | Exact Acquisition / Recovery | `Qwen/Qwen3-4B`, `microsoft/Phi-4-mini` | 0 | INCONCLUSIVE |

## 6. Conclusion
No model training occurred. No cloud metrics were collected. Android remains unchanged. Model selection is explicitly **NONE**.
