# Sahayak AI Model Card

## Model Details
- **Model Name:** [PENDING]
- **Base Model:** [PENDING (Phase 13B was inconclusive)]
- **Training Method:** [e.g., QLoRA]
- **Dataset:** Sahayak OS Training Dataset
- **Dataset Version:** v0.3
- **License:** [PENDING]

## Intended Use
- **Training Purpose:** To act as the Sahayak AI Advisor, securely parsing contextual evidence and returning deterministic JSON-structured security assessments for the Android OS ActionPolicyEngine.
- **Intended Use:** On-device security advisor.
- **Out-of-scope Use:** Autonomous system administration, execution of payments, permission granting, overriding OS policies.

## Known Limitations
- **Security Limitations:** The model is an advisor, not a trusted OS root. It cannot guarantee absolute security if the host OS policy engine is compromised.
- **Prompt Injection Limitations:** Resists known permutations but may be susceptible to unknown zero-day semantic jailbreaks. OS fail-safes are required.
- **Hallucination Limitations:** Instructed to output UNABLE_TO_DETERMINE, but probabilistic hallucination remains non-zero.
- **Multilingual Limitations:** Supports English, Hindi, Marathi, and Code-Mixed text. Degradation expected outside these bounds.

## Hardware Requirements
- **Training:** >8GB VRAM (QLoRA), 16GB System RAM.
- **Inference (On-Device):** [PENDING quantization details].

## Evaluation Results
- **Structured Output:** [PENDING]
- **Evidence Grounding:** [PENDING]
- **Capability Safety:** [PENDING]
- **Prompt Injection:** [PENDING]
