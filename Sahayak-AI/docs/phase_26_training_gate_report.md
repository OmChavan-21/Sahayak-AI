# Phase 26 — Sahayak Training Gate Audit

## A. Dataset readiness
- **Version:** v0.3
- **Expected Counts:** Total 2240 (Train: 802, Val: 171, Test: 173) -> Sum mismatch.
- **Actual Counts:** Total 2240 (Train: 1968, Val: 132, Test: 140)
- **Status:** **FAILED**. Split counts do not match the expected baseline parameters.

## B. Contract readiness
- `SahayakAIRequest` cleanly lacks the deprecated `trust_level`.
- `SahayakAIResponse` correctly uses the nested `SahayakAIRecommendation`.
- The `DatasetLoader` properly translates these structures and strictly enforces separation of contexts (System, Security, Evidence, Untrusted Content).
- **Status:** **PASSED**.

## C. Training pipeline readiness
- The `train_sft.py` correctly acts as a pipeline rather than auto-running logic.
- Protections against dataset mutation exist (loader is read-only).
- **Status:** **BLOCKED** due to missing reproducibility metadata (hashes, code commit, hardware info, runtime versions) in `ExperimentTracker`.

## D. Hardware readiness
- **GPU:** RTX 5050 Laptop GPU (12.0 sm_120)
- **VRAM:** 7.96 GB Usable
- **System RAM:** 15.26 GB Usable
- **Status:** **BLOCKED**. `environment_check.py` strictly requires >= 8.0 GB VRAM and >= 16.0 GB System RAM. The available resources fall slightly short.

## E. Model availability
- `Qwen/Qwen3-4B`: PRESENT and VERIFIED.
- `microsoft/Phi-4-mini`: MISSING.
- **Note:** No model ranking or selection is performed.

## F. Phase 25 evidence
- `benchmark_summary.json` and `generation_events.jsonl` are present, showing exactly 6 real, zero-fake Qwen generation events.
- **Status:** **VERIFIED**.

## G. Safety protections
- Unsafe capabilities (like network model download) are blocked because the pipeline aborts if `model_id` is `"placeholder_due_to_inconclusive_benchmark"`.
- Separation of test datasets holds firm in `DatasetLoader`.

## H. Reproducibility
- **Status:** **INCOMPLETE**. `ExperimentTracker` only logs `configs.json` without tracking dataset hashes, runtime environment hashes, or code commits.

## I. Known limitations
- The RTX 5050's ~7.96 GB VRAM is a hard blocker against QLoRA 4B parameter training unless further offloading (e.g. DeepSpeed ZeRO-3 or CPU-offload) is aggressively configured.

## J. Exact blockers
1. Actual dataset split counts (Train 1968, Val 132, Test 140) differ entirely from expected (Train 802, Val 171, Test 173).
2. Hardware environment does not pass `environment_check.py`.
3. Reproducibility metadata is missing from the `ExperimentTracker`.

## K. Training authorization status
- **TRAINING_BLOCKED**.
