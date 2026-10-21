# Phase 27: Training Readiness Corrections

## A. Phase 26 Failures
Phase 26 identified three mandatory blocker categories:
1. **Dataset split mismatch**: Actual Train (1968), Validation (132), Test (140) did not match the strict constraints.
2. **Hardware resource gate failure**: Global environment check explicitly rejected RTX 5050 with 7.96 GB VRAM and 15.26 GB RAM.
3. **Reproducibility metadata gaps**: ExperimentTracker lacked crucial model, dataset, hash, code, and OS-level configurations.

## B. Dataset Correction Method
The Phase 14.4 family-level separation guarantee makes achieving exactly 802, 171, and 173 examples a constraint satisfaction problem, as families map deterministically to combinations resulting in even numbers. To achieve the exact counts while preserving family isolation:
- We derived a deterministic family-preserving partition capable of yielding equal or greater counts per split.
- For each split, entire scenario families were grouped together.
- A deterministic cryptographic SHA-256 hash was applied to sort the dataset rows, and exactly the target subset top-K examples were sub-sampled. 

## C. Corrected Split Statistics
- **Train**: 802
- **Validation**: 171
- **Test**: 173

## D. Leakage Results
- Family separation between Train/Validation/Test is mathematically absolute.
- Train families: C_MAKE_PAYMENT, B_ROUTINE_MEETING, B_DELIVERY_UPDATE, B_PAYMENT_REMINDER, C_CREATE_REMINDER, S_URGENT_PHISHING, I_IGNORE_PREVIOUS, S_IMPERSONATION, U_SHORT_QUESTION, I_BENIGN_QUOTE, I_DEV_MODE.
- Validation families: B_INVOICE_URL, S_ATTACHMENT_MALWARE, U_MISSING_CONTEXT, U_AMBIGUOUS_AMOUNT.
- Test families: C_CHANGE_PASSWORD, B_CONVERSATION, S_FAKE_RECEIPT.
- **Leakage Detected: 0%**.

## E. Dataset Hashes
Hashes and dataset parameters were successfully recorded in `dataset/manifests/v0.3_manifest.json` ensuring cryptographic integrity matching `v3_deterministic_partition`.

## F. Reproducibility Improvements
`ExperimentTracker` was upgraded to inject the following metadata automatically at experiment creation:
- **Dataset metadata** (path, version, SHA-256 checksums from the manifest).
- **Model metadata** (provenance, local status).
- **Runtime configurations** (PyTorch, Transformers versions, Python, RAM, GPU, CUDA versions).
- **Code metadata** (Git status/commit).

## G. Hardware Analysis
The system provides:
- GPU: NVIDIA GeForce RTX 5050 (Compute capability `sm_120`)
- VRAM: 7.96 GB usable
- RAM: 15.26 GB usable

## H. Method-Specific Hardware Analysis
A global minimum safety gate prevents training under 4GB VRAM and 8GB RAM.
1. **FULL FINE-TUNING**: BLOCKED (Requires >24GB VRAM, >32GB RAM).
2. **LORA**: BLOCKED (Requires >16GB VRAM, >24GB RAM).
3. **QLORA**: ALLOWED (Requires >6GB VRAM, >16GB RAM). *Wait, system has 15.26 GB RAM. QLoRA needs 16.0 GB RAM? We set the profile limit to 16.0GB. It means QLoRA is technically BLOCKED on RAM? Or is it NOT_PRACTICAL?*

Let me check the instructions:
`QLORA: [ALLOWED/BLOCKED/NOT_PRACTICAL]`

Since RAM is 15.26 GB and QLoRA profile minimum RAM is 16.0 GB, it's BLOCKED by the 16.0 GB method-specific gate. This is acceptable and expected according to the instructions ("If hardware still cannot safely satisfy the configured training method: TRAINING_STILL_BLOCKED. This is acceptable and expected. Do not weaken safety requirements merely to obtain TRAINING_READY."). So QLoRA is BLOCKED due to RAM.

## I. Training Execution Lock
An explicit execution lock is now injected into `train_sft.py`. Training cannot be launched without the explicit `SAHAYAK_ALLOW_TRAINING_EXECUTION=TRUE` environment variable, ensuring the pipeline cannot silently trigger training runs.

## J. Qwen Status
- **LOCAL WEIGHTS**: PRESENT
- **IDENTITY**: VERIFIED
- **GENERATION**: VERIFIED

## K. Phi-4-mini Status
- **LOCAL WEIGHTS**: MISSING
- **GENERATION**: NOT VERIFIED

## L. Android Status
Android OS source code, policies, logic, and dependencies remain completely UNCHANGED. 

## M. Remaining Blockers
- **Hardware RAM Limitation**: While QLoRA VRAM requirements (6.0 GB) are met by the RTX 5050 (7.96 GB), the system RAM requirement (16.0 GB) is slightly missed by the usable (15.26 GB). Training is safely blocked to prevent Out-Of-Memory (OOM) operating system crashes.
