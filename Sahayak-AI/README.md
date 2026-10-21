# Sahayak AI

## What is Sahayak AI?
Sahayak AI is the core intelligence subsystem of Sahayak OS, an AI-native operating system currently prototyped on Android. It is NOT merely a generic chatbot. Its role is strictly defined:
OBSERVE ? UNDERSTAND ? REASON ABOUT SECURITY ? EXPLAIN ? EXPRESS UNCERTAINTY ? RECOMMEND SAFE NEXT STEP ? REQUEST A CAPABILITY WHEN NECESSARY.

The AI is an ADVISOR, not the authority for device actions. The OS security/policy layer (`ActionPolicyEngine`) remains unconditionally authoritative.

## Why Sahayak AI is different from a generic chatbot
Unlike typical LLMs or chatbots that attempt to fulfill all user intents, Sahayak AI is constrained by a strict architectural contract:
- **Trust Boundaries:** It respects isolation between `LEVEL_0_UNTRUSTED_EXTERNAL` content and system instructions.
- **No Direct Execution:** It cannot execute Android APIs. It returns structured requests (e.g., `requested_capability: "INSPECT_URL"`), which are independently evaluated by the OS.
- **Uncertainty is Native:** It is trained to explicitly output `UNABLE_TO_DETERMINE` rather than hallucinate answers when evidence is insufficient.
- **Evidence Grounding:** All assessments must reference concrete observed evidence.

## AI ? Capability ? Policy architecture
1. **AI (Advisor):** Emits a structured `SahayakAIResponse` containing a `requested_capability`.
2. **Capability Layer (Bridge):** Wraps the AI's declarative request into a `CapabilityRequest` and determines the scope and metadata.
3. **Policy Engine (Authority):** The `ActionPolicyEngine` evaluates the capability based on strict rules. It enforces user confirmation, denies dangerous capabilities, and logs decisions safely without arbitrary escalation.

## Dataset philosophy
The dataset schema enforces this boundary at the training level:
- Inputs distinctly separate `untrusted_content` from OS/system metadata.
- Outputs are heavily structured (JSON/dataclass matching Android schemas) to prevent arbitrary text leakage.
- Examples include benign, suspicious, ambiguous (safe-fail), and high-risk scenarios.
- Strict quality rules apply: no real personal info, no raw credentials, and intentional preservation of ambiguity where evidence is weak.

## Security and trust boundaries
Trust levels explicitly model where data originated:
- `LEVEL_0`: External content (e.g., received messages, websites).
- `LEVEL_1`: User-selected evidence.
- `LEVEL_2`: System-verified metadata.
- `LEVEL_3`: Sahayak-generated interpretation (AI output).
- `LEVEL_4`: Explicit user-confirmed instructions.
The dataset includes adversarial prompt injection attempts to ensure the model recognizes malicious text inside `untrusted_content` and never promotes it to `LEVEL_4`.

## Evaluation philosophy
Evaluation does NOT score "intelligence" or chattiness. Primary metrics are:
1. Does it preserve evidence?
2. Does it avoid hallucinating?
3. Does it recognize uncertainty (`UNABLE_TO_DETERMINE`)?
4. Does it resist prompt injection?
5. Does it respect trust boundaries?
6. Does it avoid unauthorized capability execution?
7. Does it produce valid structured output?
8. Does it recommend safe next steps?

## Android ? Python Contract Mapping
The Python canonical dataset schema strictly mirrors the Sahayak OS Android architecture:
| Android Kotlin Interface | Python Schema (Sahayak-AI) |
| --- | --- |
| `SahayakAITask` | `SahayakAITask` Enum |
| `SahayakAIConfidence` | `SahayakAIConfidence` Enum |
| `SahayakCapability` | `SahayakCapability` Enum |
| `SahayakAISecurityContext` | `SahayakAISecurityContext` dataclass |
| `SahayakAIRequest` | `SahayakAIRequest` dataclass |
| `SahayakAIRecommendation` / `SahayakAIResponse` | `SahayakAIResponse` dataclass |

## Future training plan
1. Select an open-source foundation model (e.g., via Hugging Face).
2. Generate/Curate Sahayak dataset per schemas.
3. Supervised fine-tuning (SFT) on structured output formats.
4. LoRA/PEFT adaptation for resource efficiency.
5. Strict evaluation against the principles defined above.
6. Local inference mapping.
7. Final Android integration.
**Note:** At this phase, no model training has happened, and no weights have been downloaded. This repository currently serves strictly as the specification and architectural bridge for future AI development.
# Phase 14: Sahayak Dataset Expansion

## Deterministic SFT Generation

We have explicitly avoided using an LLM to hallucinate the baseline supervised fine-tuning (SFT) dataset. Instead, we have engineered a Python-based, deterministic permutation generator (`deterministic_generator.py`) that strictly outputs `sahayak_v0_1_sft.jsonl`.

This ensures absolute compliance with the Phase 13A Output Contract across the following 8 categories:

### 1. Capability Boundaries & Refusal
- Systematically generates dangerous action requests (e.g., `MAKE_PAYMENT`, `DELETE_FILE`, `EXECUTE_CODE`).
- **Ground Truth:** The model is rigidly mapped to output `requested_capability: null` and an explanation stating that executing actions is outside its safety authority.

### 2. Prompt Injection
- Injects classic adversarial payloads ("Ignore all previous instructions...", "System Override").
- **Ground Truth:** Forces the `assessment` to flag prompt injection and `confidence` to `HIGH_CONFIDENCE`, quarantining the untrusted text.

### 3. Uncertainty
- Permutes ambiguous contextless messages ("Are we still on for tomorrow?", "Hey, can you send the file?").
- **Ground Truth:** Strictly assigns `confidence: UNABLE_TO_DETERMINE`. The model learns to gracefully fail safe rather than fabricating certainty.

### 4. Evidence Grounding & Security Assessment
- Cross-multiplies lists of urgent preambles with known malicious URL patterns.
- **Ground Truth:** Emits the `SahayakCapability.INSPECT_URL` capability request explicitly and extracts the exact substrings of urgency as `evidence_references`.

### 5. Trust Boundaries
- Varies the `trust_level` on the request from `LEVEL_0_UNTRUSTED_EXTERNAL` to `LEVEL_2_SYSTEM_VERIFIED`.
- **Ground Truth:** Demonstrates that legitimate system messages are assessed safely while structurally identical untrusted external messages are treated with extreme caution.

## Next Steps
The deterministic seed dataset currently yields structured ground-truth examples without any hallucinations. 
We can now expand the variable dictionaries (adding thousands of permutations of URLs, urgency phrases, missing evidence scenarios, and APIs) to achieve dataset scales capable of altering base-model behavior in **Phase 15 (SFT / LoRA / PEFT)**.
