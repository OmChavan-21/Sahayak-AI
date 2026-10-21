# Sahayak OS

## What is Sahayak?
Sahayak is an AI-powered cybersecurity and action assistant for everyday digital life. It helps users analyze text, images, documents, and voice for security risks before taking action.

## Current MVP Stage
This project is currently an Android prototype foundation. The core UI and package structure have been established, but AI, backend, and security analysis features are intentionally not yet implemented. This provides a clean slate for building out the planned architecture.

## Planned Architecture
The project is organized to support future features cleanly:
- \com.sahayak.app.ui\: Contains Compose screens and themes.
- \com.sahayak.app.core\: Core utilities and base classes.
- \com.sahayak.app.security\: The security and validation layer for actions.
- \com.sahayak.app.ai\: Abstractions for communicating with the AI.
- \com.sahayak.app.input\: Handlers for text, image, document, and voice inputs.
- \com.sahayak.app.data\: Repositories and local data sources.
- \com.sahayak.app.actions\: Handlers for user-confirmed safe actions.

## Security Principle
The AI is treated as an analysis component, NOT as an unrestricted authority. The architecture ensures:
AI analysis ? structured result ? security/validation layer ? user confirmation ? action.
The AI layer cannot directly perform sensitive actions.

## Privacy Principle
Sahayak follows a privacy-first design:
- Minimizes collected data.
- Avoids storing sensitive raw content by default.
- Never requests OTPs, PINs, passwords, or similar secrets.
- Sensitive actions require explicit user control.

## Local AI Architecture
- Sahayak is designed to support an on-device/open-source AI model.
- The exact model will be selected based on the hackathon-provided hardware/model.
- AI is separated from the security/action layer.
- Deterministic checks remain important.
- AI does not directly execute actions.
- The architecture supports graceful fallback when local AI is unavailable.

## Input & Evidence Architecture
- Sahayak is inherently input-agnostic. It can eventually understand information from shared text, screenshots when permitted, camera input, documents, voice transcripts, and future system integrations.
- Sahayak does NOT bypass Android restrictions. Any future integrations will request explicit permissions and operate strictly within the user's control.
- Evidence is separated from interpretation. The system preserves the original observed evidence (what was actually there) and strictly distinguishes it from AI-generated reasoning or interpretation.

## Action & Permission Safety
- Sahayak does not give unrestricted control to AI.
- Actions are classified by risk.
- Consequential actions require user involvement.
- Payments and account changes are outside Sahayak's action authority.
- AI cannot override the action policy.
- Future action integrations must pass through the policy layer.
- Principle: **"AI recommends. Policy decides. User controls."**

## Android Share Integration
- Sahayak can receive text explicitly shared by the user via the standard Android share menu.
- Shared content naturally enters the exact same UserInput ? evidence ? security pipeline as manually typed text.
- Sahayak does not access other apps' private data, bypass screenshot limits, or use intrusive APIs (like Accessibility or Notification Listeners).
- The user is shown the shared content and must review it before analysis begins.
- Principle: **"User chooses what Sahayak sees."**

## Image Input
- Users can explicitly select images using the modern Android system Photo Picker.
- Sahayak does not require broad storage access (READ_EXTERNAL_STORAGE) for this workflow; it relies on safe URI delegation.
- Selected images are abstracted through ImageInputFactory and UserInput to keep the domain pure.
- The user is always shown a preview of the image before analysis, and analysis begins only after explicit user confirmation.
- Actual OCR is not integrated yet (currently defaults to NoOpOcrEngine).
- OCR failure or unavailability never artificially generates a safe or unsafe security verdict. It defaults safely to an "Unable to analyze" state.
- Screenshot restrictions are respected by relying entirely on Android's secure UI paradigms. Sahayak does not bypass Android security controls or use screen-recording workarounds.

## Local AI Runtime Architecture
- Sahayak is explicitly architected for on-device local/open-source AI. 
- The current build contains a robust architectural abstraction (LocalAIModelRuntime), but intentionally lacks model weights or hard-coded implementations, keeping it fully decoupled until the target device specs are known.
- No cloud fallback or external AI APIs are integrated.
- The AI operates strictly as an advisor in the pipeline.
- The deterministic security logic remains independent and authoritative—an AI failure (e.g. out of memory, cancellation) gracefully falls back to deterministic analysis without crashing.
- To prevent prompt injection, untrusted user content (images, messages) is explicitly separated from trusted system instructions via PromptContext.
- Principle: **"The model can recommend. The safety layer decides. The user controls consequential actions."**

## AI-Native Sahayak OS Architecture
Sahayak is not just an app with an AI feature; it is an AI-native OS architecture prototyped on Android. 
The core of this is the **Sahayak AI Contract**, which governs how the AI communicates with the OS:
- **The AI is an Advisor**: It observes evidence and security context, produces structured recommendations, and may request capabilities (like INSPECT_URL or CREATE_DRAFT).
- **Separation of Trust**: User-provided content is strictly isolated as untrusted data (untrustedContent) from system instructions, neutralizing prompt injection at the architectural level.
- **Capabilities, Not Permissions**: The AI does not receive unrestricted Android permissions and does not directly execute device actions. It returns a equestedCapability and a capabilityReason.
- **Safety First**: The OS security and capability layers (ActionPolicyEngine) remain absolutely authoritative.
- **Uncertainty is Native**: The AI can explicitly declare UNABLE_TO_DETERMINE when evidence is weak, rather than hallucinating safe verdicts.
- **Local-First**: The pipeline relies entirely on a localized RuntimeBackedSahayakAIEngine abstraction, ready for a private, on-device open-source model.

## AI -> Capability -> Action Security Model
Sahayak AI is an advisor. The capability layer is the controlled bridge between AI recommendations and device capabilities.

- **Authoritative Policy Engine**: The ActionPolicyEngine remains strictly authoritative. Unknown capabilities gracefully fail closed.
- **Strict Capabilities Boundaries**: A capability request is merely a structured object, not authorization or execution. The AI cannot grant itself permissions or bypass established safeguards.
- **Explicit Trust Levels**: AI-generated responses (Level 3) are architecturally separated from explicit user-confirmed instructions (Level 4), ensuring an AI can never independently increase trust.
- **Execution Adapter Isolation**: The capability registry handles capability decisions, while execution flows exclusively through a restricted executor, completely cutting off the AI from raw Android APIs.
- **User Control**: Explicit user confirmation continues to be mandated for any consequential operation.

## Security Audit & Trust Architecture
Sahayak OS treats AI reasoning, user evidence, policy decisions, and device actions as separate security events.

- **Immutable Fact Record**: The audit layer strictly records security decisions, capabilities requested, and system outcomes, but it does not execute or authorize actions itself.
- **Trust Isolation**: Sahayak AI is treated as a component, meaning its output (LEVEL_3_SAHAYAK_GENERATED) cannot unilaterally bypass explicit user confirmation (LEVEL_4_EXPLICIT_USER_CONFIRMED). AI cannot increase trust natively.
- **Authoritative Flow**: The ActionPolicyEngine stays strictly authoritative at all levels of capability invocation and logging.
- **Privacy First**: Sensitive content like OTPs, pins, passwords, or raw user screenshots are architecturally prevented from leaking into the audit log via strict SensitivityClassification metadata barriers.
