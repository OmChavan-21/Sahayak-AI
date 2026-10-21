# Phase 14.1 — Semantic Security Audit Report

## Methodology
An independent, deterministic Python script was developed to audit the `sahayak_v0_1_sft.jsonl` dataset generated during Phase 14. This script strictly validated the dataset against the canonical Android Kotlin classes (`SahayakAIRequest`, `SahayakAIResponse`, etc.). The audit assessed 39 total examples across capabilities, prompt injections, and uncertainties.

## Dataset Status & Statistics
- **Total Examples Audited:** 39
- **Languages:** 100% English (No Hindi/Marathi code-mixing present).
- **Categories:** SUGGEST_SAFE_NEXT_STEP (24), ASSESS_SECURITY (14), EXPLAIN_CONTENT (1).
- **Confidence Spreads:** 35 High Confidence, 4 Unable to Determine.
- **Benign vs Suspicious:** 33 Benign/Refusals vs 6 Suspicious.
- **Evidence Grounding:** 0 Failures (All extracted substrings rigorously match the untrusted content).
- **Prompt Injection:** 2 instances.
- **Refusals:** 24 instances (refusing dangerous capability executions).

## Contract Concerns
**CRITICAL:** The deterministic generator used a Python `SahayakAIResponse` schema that severely diverges from the canonical Android Kotlin contract. 
1. **Contract Drift (Response):** The dataset outputs `recommended_next_step`, `requested_capability`, and `capability_reason` at the root object level. In the Android `SahayakAIResponse.kt` code, these three fields are nested inside a single optional `recommendation: SahayakAIRecommendation` object.
2. **Contract Drift (Request):** The Python dataset generator includes `trust_level` directly in `SahayakAIRequest`. The canonical Kotlin request correctly manages trust natively in the OS; it does not pass `trust_level` to the AI logic block directly. 
These drifts account for 117 critical schema violations that would prevent the Android OS from parsing model output.

## Security & Capability Concerns
- **Capability Boundaries:** Handled robustly. 24 examples successfully simulate users explicitly demanding unauthorized execution (e.g., "MAKE_PAYMENT"). The dataset accurately maps these to `requested_capability: null`, respecting the AI's limited advisory role.
- **Prompt Injection:** Attack payloads ("Ignore all previous instructions") correctly categorize as untrusted content rather than executing. 

## Diversity & Contamination Concerns
- **Diversity:** The 39 examples rely on highly repetitive templating. Generating 40,000 permutations from this exact script would over-train superficial lexical shortcuts (e.g., mapping exact urgency phrases to URLs) rather than true security reasoning. 
- **Contamination:** There are no distinct train/test/validation splits established natively. `evaluation` examples were generated separately in Phase 13, avoiding crossover, but scaling this generator will require mathematically isolating template roots. 
- **Sensitive Data:** 0 occurrences of real private keys, passwords, or financial credentials.

## Phase 13B Benchmark Post-Mortem
A late review of the delayed Phase 13B background task artifacts reveals:
- **Models Evaluated:** `Qwen/Qwen2.5-3B-Instruct` and `microsoft/Phi-4-mini-instruct`.
- **Hardware Used:** CPU inference fallback (`torch 2.14.0+cpu` instead of GPU).
- **Test Cases:** Evaluated 0 examples due to absolute directory path resolution mismatches when invoking the evaluation loop out-of-tree.
- **Latency/Token Stats:** 0 ms avg latency (no tokens generated).
- **Model-Quality Conclusion:** **No conclusion is justified**. Because 0 generation events actually occurred on the models, any judgment regarding Qwen vs Phi-4 capability boundaries is purely fabricated. The benchmark script successfully validated environment instantiation but failed operational validation.

## Final Readiness Decision
**REQUIRES DATASET CORRECTIONS**

---

### SUMMARY

PHASE 14.1 STATUS: COMPLETE
DATASET STATUS: REQUIRES CORRECTIONS
CONTRACT STATUS: CRITICAL DRIFT (Flattened capabilities & injected trust fields)
SEMANTIC SECURITY STATUS: ROBUST (Refusals and boundaries logically hold)
DIVERSITY STATUS: POOR (Highly templated)
CONTAMINATION STATUS: ACCEPTABLE (No overlap, but no explicit structural splits)
PHASE 13B BENCHMARK STATUS: INCONCLUSIVE (0 generation events recorded)
FINAL DECISION: REQUIRES DATASET CORRECTIONS
