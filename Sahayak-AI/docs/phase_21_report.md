# Phase 21 — Offline Exact Model Import & Cryptographic Verification

## A. Acquisition Problem
The candidate models (`Qwen/Qwen3-4B` and `microsoft/Phi-4-mini`) could not be acquired through official Hugging Face Hub APIs in Phase 20 due to network constraints/unavailability, resulting in an `INCONCLUSIVE` loop. An alternative secure acquisition path was required without violating the no-cloud strictures.

## B. Offline Import Design
An offline model intake workflow was designed using isolated subdirectories:
- `models/incoming/` for unverified drops.
- `models/verified/` for mathematically validated candidates.
- `models/rejected/` for corrupted or mismatched files.
- `models/manifests/` for JSON auditing manifests.

## C. Exact Identity Verification
The importer script (`offline_importer.py`) bypasses directory names completely. It strictly inspects `config.json` inside incoming folders to read the `_name_or_path` metadata. Any candidate not explicitly resolving to `Qwen/Qwen3-4B` or `microsoft/Phi-4-mini` is flagged as `REJECTED_UNRELATED_MODEL`. 

## D. Hash/Integrity Verification
All files introduced into `models/incoming/` are scanned to compute exact SHA-256 hashes. These are recorded into the `manifests/` directory. Official hashes are explicitly marked `UNAVAILABLE` rather than fabricated.

## E. Memory Feasibility
Based on estimates, 8GB VRAM is highly restrictive for 4B parameter models running in raw FP16/BF16 alongside context KV caches. Safe local loading is expected to strictly require quantization (4-bit/8-bit), which remains designated for a future controlled phase.

## F. Local Loading Result
No exact offline model weights for `Qwen/Qwen3-4B` or `microsoft/Phi-4-mini` were successfully provided to the incoming directory. The dummy test configurations were used to prove the workflow works, but no production model load could take place.

## G. Actual Generation Result
Because no true weights were processed, the actual generated output length is exactly 0 bytes (verified locally by `generation_events.jsonl` remaining empty). The Zero-Generation Guard was successfully applied.

## H. Test Results
Automated testing (`test_phase21.py`) proved:
1. Exact model IDs are immutable.
2. Folder names (e.g. `microsoft-Phi-4-mini`) do not override internal identity validation (rejected `Phi-3-mini` correctly).
3. SHA-256 hashes are always generated safely.
4. Zero-generation correctly outputs `INCONCLUSIVE`.

## I. Phase History Reconciliation

| Phase | Description | Result |
|---|---|---|
| **13B** | Baseline Generation Attempt | INCONCLUSIVE (0 generations) |
| **16** | Local Candidate Benchmark | INCONCLUSIVE (0 generations) |
| **19** | Exact Model Hub Download | INCONCLUSIVE (0 generations) |
| **20** | Model Loading Recovery | INCONCLUSIVE (0 generations) |
| **21** | Offline Identity Verification | INCONCLUSIVE (0 generations) |
