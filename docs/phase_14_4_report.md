# Phase 14.4 — Dataset Split Isolation & Diversity Correction

## 1. Methodology & Data Generation
Dataset `v0_3` was generated strictly using deterministic Python scripts (`deterministic_generator_v3.py`) with zero reliance on LLMs, cloud APIs, or automated modifications to the canonical Android Kotlin contract.

The generator was refactored into a **Scenario Family Architecture**. The fundamental unit of data generation and splitting is now the *Scenario Family* (e.g., `B_ROUTINE_MEETING`, `S_URGENT_PHISHING`).

- **Total Examples:** 2,240
- **Train:** 1,968 (87.8%)
- **Validation:** 132 (5.9%)
- **Test:** 140 (6.2%)
(Distribution targets prioritizing zero-leakage family isolation over exact 70/15/15 ratios).

## 2. Split Contamination Analysis
An independent split validation script (`split_validator.py`) mathematically verified isolation.
- **Family Overlap:** 0
- **Template Overlap:** 0
- **Exact Overlap:** 0
- **Normalized Text Overlap:** 0

The Train, Validation, and Test datasets share **zero** overlapping scenario structures, assuring that the Test set strictly evaluates out-of-distribution generalization.

## 3. Diversity Enhancements
To combat the "marginal" diversity reported in Phase 14.3, we explicitly generated diverse conceptual scenarios rather than merely injecting more URLs:
- **Benign Counterexamples:** Injected `B_INVOICE_URL` and `B_PAYMENT_REMINDER` to teach the model that presence of a URL or financial amount is *not* intrinsically malicious.
- **Ambiguity/Uncertainty:** Included `U_SHORT_QUESTION`, `U_MISSING_CONTEXT`, and `U_AMBIGUOUS_AMOUNT` across English, Hindi, and Marathi to train robust fail-safe states (`confidence: UNABLE_TO_DETERMINE`).
- **Prompt Injection Depth:** Distinguished between malicious overriding (`I_DEV_MODE`, `I_IGNORE_PREVIOUS`) and benign discussion (`I_BENIGN_QUOTE`).
- **Capability Boundaries:** Included blocks for `MAKE_PAYMENT` and `CHANGE_ACCOUNT_INFORMATION`, while generating explicit approval patterns for `CREATE_REMINDER` and `EXPLAIN_CONTENT`.

## 4. Languages
- English: 1,504
- Hindi: 396
- Marathi: 200
- En-Hi-CodeMix: 140

## 5. Artifact Immutability & Evaluation Isolation
The previous `v0_1` and `v0_2` artifacts were completely preserved. No historical data was overwritten. Evaluation-only datasets remain out-of-scope for this generator and completely isolated from `Sahayak-AI/dataset/training/v0_3/`.

## Final Readiness Decision
**READY FOR RE-AUDIT**
