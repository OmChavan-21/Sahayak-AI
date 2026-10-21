# Phase 28: Training Path & Resource Feasibility Analysis

## Executive Summary
This report analyzes the engineering feasibility of training the Sahayak AI model locally. No training was executed during this phase. The analysis confirms that while QLoRA VRAM requirements are technically met by the NVIDIA RTX 5050 (7.96 GB VRAM), the available System RAM (15.26 GB) fails the safety margin for quantization and data loading. Furthermore, critical dependencies for QLoRA (`bitsandbytes`, `peft`) are currently missing from the runtime environment.

## Current Verified State
- **Dataset**: v0.3 is fully verified (2240 total: 802 Train, 171 Validation, 173 Test) with strict family isolation, complete SHA-256 manifests, and 0% leakage.
- **Qwen3-4B**: Exact local weights are present. Identity and integrity are verified. Local GPU generation was successfully verified.
- **Phi-4-mini**: Local weights remain MISSING. Generation is NOT VERIFIED.

## Hardware Constraints
- **GPU**: NVIDIA RTX 5050 Laptop GPU
- **Compute Capability**: `sm_120` (CUDA 12.8 support)
- **Usable VRAM**: 7.96 GB
- **Usable System RAM**: 15.26 GB
- **Execution Lock**: ACTIVE

## Method-by-Method Memory Analysis
*Calculations based on Qwen3-4B (approx. 4.02B parameters)*

### A. Full Fine-Tuning
- **Model Parameter Count**: ~4.02B
- **Dtype**: bfloat16
- **Quantization Mode**: None
- **Sequence Length**: 2048
- **Batch Size**: 4
- **Gradient Accumulation**: 4
- **Optimizer**: AdamW
- **Optimizer State Requirements**: ~32.16 GB (8 bytes per parameter for moments and copies)
- **Activation/Checkpointing Configuration**: Standard
- **Expected Model Memory**: 8.04 GB (calculated)
- **Expected Optimizer Memory**: 32.16 GB (calculated)
- **Expected Activation Memory**: ~6.0 GB (estimate)
- **Expected VRAM**: > 46.0 GB
- **Expected System RAM**: > 32.0 GB
- **Status**: BLOCKED

### B. LoRA
- **Model Parameter Count**: ~4.02B
- **Dtype**: bfloat16
- **Quantization Mode**: None
- **Sequence Length**: 2048
- **Batch Size**: 4
- **Gradient Accumulation**: 4
- **Optimizer**: AdamW
- **Optimizer State Requirements**: ~0.1 GB (applied only to LoRA adapters `r=16`)
- **Activation/Checkpointing Configuration**: Standard
- **Expected Model Memory**: 8.04 GB (calculated, frozen)
- **Expected Optimizer Memory**: ~0.1 GB (estimate)
- **Expected Activation Memory**: ~6.0 GB (estimate)
- **Expected VRAM**: ~14.5 GB
- **Expected System RAM**: > 16.0 GB
- **Status**: BLOCKED

### C. QLoRA
- **Model Parameter Count**: ~4.02B
- **Dtype**: bfloat16 computation, nf4 storage
- **Quantization Mode**: NF4 (4-bit)
- **Sequence Length**: 2048
- **Batch Size**: 4
- **Gradient Accumulation**: 4
- **Optimizer**: PagedAdamW (assumed)
- **Optimizer State Requirements**: ~0.1 GB
- **Activation/Checkpointing Configuration**: Gradient checkpointing required
- **Expected Model Memory**: ~2.2 GB (calculated)
- **Expected Optimizer Memory**: ~0.1 GB (estimate)
- **Expected Activation Memory**: ~3.0 GB (estimate)
- **Expected VRAM**: ~5.5 GB
- **Expected System RAM**: > 16.0 GB (required for initial FP16 weight loading before quantization)
- **Status**: BLOCKED (System RAM safety gate failure)

## QLoRA Feasibility
The QLoRA method passes the VRAM threshold (requires ~5.5 GB, available 7.96 GB) but fails the RAM threshold.
- **Minimum Practical System RAM**: 16.0 GB minimum is strict. During model initialization, Hugging Face `transformers` loads the 8.04 GB fp16 model into RAM before pushing it to VRAM in 4-bit. With the OS consuming 4-6 GB, 15.26 GB leaves almost zero margin for data loaders or background processes, risking a hard OOM crash.
- **CPU Offloading & Paged Optimizers**: Paged optimizers push memory spikes to System RAM. With limited RAM, this increases swapping and crash risk.
- **24 GB RAM**: Would provide a sufficient margin for QLoRA.
- **32 GB RAM**: Would provide a highly safe operating margin.
- **Missing Dependencies**: The current `gpu_venv_sm120` environment lacks `bitsandbytes` (required for 4-bit NF4) and `peft`.

## Qwen3-4B Compatibility Analysis
- **Supported Loading Format**: Hugging Face `safetensors`. Compatible.
- **Quantization Compatibility**: Compatible with `bitsandbytes` NF4.
- **Tokenizer Compatibility**: Compatible.
- **PEFT / QLoRA Compatibility**: Compatible (target modules `q_proj`, `v_proj` exist).
- **Modification**: Original files are unmodified. Training adapters will be saved separately.

## Phi-4-mini Status
- Exact local weights remain MISSING. Generation is not verified.

## Runtime Compatibility
- **Python**: 3.12.10
- **PyTorch**: 2.11.0+cu128 (Compatible with `sm_120`)
- **CUDA**: 12.8
- **Transformers**: 5.17.0
- **PEFT**: Missing (Blocker for LoRA/QLoRA)
- **BitsAndBytes**: Missing (Blocker for QLoRA)
- **Accelerate**: 1.15.0
- **OS**: Windows
- **GPU Architecture**: `sm_120` (Requires `cu128` wheels).

## Dataset Readiness
- Canonical source: `Sahayak-AI/dataset/manifests/v0.3_manifest.json`
- Counts exactly match requirements.
- Hashes and deterministic reproducibility are verified.
- Loader compatibility is verified.

## Hardware Upgrade Scenarios
- **Current (15.26 GB RAM / 7.96 GB VRAM)**: All methods blocked.
- **Hypothetical 24 GB RAM**: Would unlock QLoRA by providing safe system RAM margins for 4-bit quantization initialization. VRAM remains the bottleneck for LoRA/FULL.
- **Hypothetical 32 GB RAM**: Would safely unlock QLoRA and potentially standard LoRA if VRAM management is highly optimized (e.g., batch size 1, sequence length 1024), though VRAM (7.96GB) would still likely block standard LoRA.

*Note: Hardware upgrades do not guarantee training success. Optimization of gradient checkpointing and batch sizes must still be verified experimentally.*

## Alternative Legitimate Paths
A. Upgrade system RAM to 24+ GB and attempt QLoRA after installing missing dependencies.
B. Use a legitimate higher-memory training machine.
C. Use an approved local workstation/server with sufficient resources.
D. Use another training-compatible architecture if explicitly approved later.

## Unresolved Questions
- Is `bitsandbytes` fully compiled and compatible with Windows `sm_120` CUDA 12.8 environments?
- Can gradient checkpointing reduce Qwen3-4B activations enough to fit strictly within 7.96 GB VRAM during QLoRA?

## Exact Prerequisites for Phase 29
1. Resolution of the RAM hardware gate (via upgrade or offloading strategy).
2. Installation and verification of `peft` and `bitsandbytes` in the `sm_120` runtime.
3. Explicit `SAHAYAK_ALLOW_TRAINING_EXECUTION=TRUE` authorization.

**NO TRAINING WAS EXECUTED DURING PHASE 28.**
