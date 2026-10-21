import os
import io

pkg = 'app/src/main/java/com/sahayak/app/capabilities/'
os.makedirs(pkg, exist_ok=True)

files = {
    'SahayakCapability.kt': """package com.sahayak.app.capabilities

import com.sahayak.app.actions.ActionType

enum class SahayakCapability(val actionType: ActionType?) {
    READ_USER_INPUT(null),
    READ_SHARED_CONTENT(null),
    READ_SELECTED_IMAGE(null),
    READ_SELECTED_DOCUMENT(null),
    EXTRACT_TEXT(null),
    EXTRACT_EVIDENCE(null),
    ANALYZE_SECURITY(null),
    HIGHLIGHT_EVIDENCE(ActionType.HIGHLIGHT_EVIDENCE),
    EXPLAIN_CONTENT(ActionType.EXPLAIN),
    CREATE_DRAFT(ActionType.CREATE_DRAFT),
    CREATE_CHECKLIST(null),
    CREATE_REMINDER(ActionType.CREATE_REMINDER),
    SAVE_SECURITY_EVENT(null),
    GENERATE_REPORT_DRAFT(null),
    INSPECT_URL(ActionType.INSPECT_URL),
    
    // Future capabilities (not implemented)
    READ_NOTIFICATION(null),
    READ_BROWSER_CONTEXT(null),
    CAMERA_CAPTURE(null),
    MICROPHONE_INPUT(null),
    CONTACT_SELECTION(null),
    FILE_SELECTION(null),
    SEND_MESSAGE(ActionType.SEND_MESSAGE),
    SUBMIT_REPORT(ActionType.SUBMIT_COMPLAINT),
    MAKE_PAYMENT(ActionType.MAKE_PAYMENT),
    CHANGE_ACCOUNT_INFORMATION(ActionType.CHANGE_ACCOUNT_INFORMATION),
    EXECUTE_CODE(ActionType.UNKNOWN)
}
""",
    'CapabilityMetadata.kt': """package com.sahayak.app.capabilities

import com.sahayak.app.actions.ActionRisk

data class CapabilityMetadata(
    val id: SahayakCapability,
    val riskLevel: ActionRisk,
    val purpose: String,
    val requiredPermission: String?,
    val dataAccessed: List<String>,
    val requiresUserConfirmation: Boolean,
    val isImplemented: Boolean,
    val isAllowedInPrototype: Boolean,
    val hasExternalSideEffect: Boolean,
    val isReversible: Boolean,
    val requiresAudit: Boolean
)
""",
    'CapabilityProtocolRegistry.kt': """package com.sahayak.app.capabilities

class CapabilityProtocolRegistry {
    private val capabilities = mutableMapOf<SahayakCapability, CapabilityMetadata>()

    fun register(metadata: CapabilityMetadata) {
        if (capabilities.containsKey(metadata.id)) {
            throw IllegalArgumentException("Capability ${metadata.id} is already registered")
        }
        capabilities[metadata.id] = metadata
    }

    fun getMetadata(id: SahayakCapability): CapabilityMetadata? {
        return capabilities[id]
    }

    fun getAllRegistered(): List<CapabilityMetadata> {
        return capabilities.values.toList()
    }
}
""",
    'CapabilityRequest.kt': """package com.sahayak.app.capabilities

data class CapabilityRequest(
    val capability: SahayakCapability,
    val requestingComponent: String,
    val purpose: String,
    val targetResource: String? = null,
    val requestedScope: CapabilityScope,
    val originatingRecommendationId: String? = null,
    val timestampMs: Long = System.currentTimeMillis(),
    val trustLevel: TrustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED
)
""",
    'CapabilityScope.kt': """package com.sahayak.app.capabilities

data class CapabilityScope(
    val requireHttps: Boolean = true,
    val isReadOnly: Boolean = true,
    val allowCredentials: Boolean = false,
    val allowCookies: Boolean = false,
    val allowPrivateNetwork: Boolean = false,
    val allowArbitraryCodeExecution: Boolean = false,
    val allowUnrestrictedDownloads: Boolean = false
) {
    companion object {
        val LEAST_PRIVILEGE_URL_INSPECTION = CapabilityScope(
            requireHttps = true,
            isReadOnly = true,
            allowCredentials = false,
            allowCookies = false,
            allowPrivateNetwork = false,
            allowArbitraryCodeExecution = false,
            allowUnrestrictedDownloads = false
        )
        val DEFAULT_SAFE_SCOPE = CapabilityScope()
    }
}
""",
    'CapabilityDecision.kt': """package com.sahayak.app.capabilities

enum class CapabilityDecision {
    ALLOWED,
    REQUIRES_CONFIRMATION,
    DENIED,
    UNAVAILABLE,
    INVALID_REQUEST
}
""",
    'TrustLevel.kt': """package com.sahayak.app.capabilities

enum class TrustLevel(val level: Int) {
    LEVEL_0_UNTRUSTED_EXTERNAL(0),
    LEVEL_1_USER_PROVIDED_EVIDENCE(1),
    LEVEL_2_SYSTEM_VERIFIED(2),
    LEVEL_3_SAHAYAK_GENERATED(3),
    LEVEL_4_EXPLICIT_USER_CONFIRMED(4)
}
""",
    'CapabilityExecutor.kt': """package com.sahayak.app.capabilities

/**
 * The strict boundary for executing capabilities. 
 * AI cannot directly call Android APIs. It must route through here.
 */
interface CapabilityExecutor {
    suspend fun execute(request: CapabilityRequest, decision: CapabilityDecision): Boolean
}
""",
    'CapabilityAuditHook.kt': """package com.sahayak.app.capabilities

enum class AuditEventType {
    CAPABILITY_REQUESTED,
    CAPABILITY_ALLOWED,
    CAPABILITY_DENIED,
    CAPABILITY_REQUIRES_CONFIRMATION,
    CAPABILITY_EXECUTED
}

interface CapabilityAuditHook {
    fun logEvent(
        eventType: AuditEventType, 
        request: CapabilityRequest, 
        decision: CapabilityDecision? = null
    )
}
""",
    'CapabilityPolicyEvaluator.kt': """package com.sahayak.app.capabilities

import com.sahayak.app.actions.ActionPolicyEngine
import com.sahayak.app.actions.ActionDecision

class CapabilityPolicyEvaluator(
    private val registry: CapabilityProtocolRegistry,
    private val actionPolicyEngine: ActionPolicyEngine,
    private val auditHook: CapabilityAuditHook? = null
) {
    fun evaluate(request: CapabilityRequest): CapabilityDecision {
        auditHook?.logEvent(AuditEventType.CAPABILITY_REQUESTED, request)

        // 1. Check registry
        val metadata = registry.getMetadata(request.capability)
        if (metadata == null) {
            // Unknown capability fails closed
            val decision = CapabilityDecision.INVALID_REQUEST
            auditHook?.logEvent(AuditEventType.CAPABILITY_DENIED, request, decision)
            return decision
        }

        if (!metadata.isImplemented || !metadata.isAllowedInPrototype) {
             val decision = CapabilityDecision.UNAVAILABLE
             auditHook?.logEvent(AuditEventType.CAPABILITY_DENIED, request, decision)
             return decision
        }

        // 2. Trust Level verification
        // AI output cannot implicitly increase trust level to bypass confirmation
        if (request.trustLevel.level < TrustLevel.LEVEL_4_EXPLICIT_USER_CONFIRMED.level 
            && metadata.requiresUserConfirmation) {
            // Must require confirmation
        }

        // 3. Consult ActionPolicyEngine
        val actionType = request.capability.actionType
        val finalDecision = if (actionType != null) {
            val actionDecision = actionPolicyEngine.evaluate(actionType)
            when (actionDecision) {
                ActionDecision.ALLOWED -> CapabilityDecision.ALLOWED
                ActionDecision.REQUIRES_CONFIRMATION, ActionDecision.USER_MUST_EXECUTE -> CapabilityDecision.REQUIRES_CONFIRMATION
                ActionDecision.BLOCKED -> CapabilityDecision.DENIED
            }
        } else {
            // Internal capabilities mapped by metadata
            if (metadata.requiresUserConfirmation) CapabilityDecision.REQUIRES_CONFIRMATION else CapabilityDecision.ALLOWED
        }

        // 4. Enforce strict risk limits
        val safeDecision = if (finalDecision == CapabilityDecision.ALLOWED && metadata.requiresUserConfirmation) {
            CapabilityDecision.REQUIRES_CONFIRMATION
        } else {
            finalDecision
        }

        val event = when(safeDecision) {
            CapabilityDecision.ALLOWED -> AuditEventType.CAPABILITY_ALLOWED
            CapabilityDecision.REQUIRES_CONFIRMATION -> AuditEventType.CAPABILITY_REQUIRES_CONFIRMATION
            else -> AuditEventType.CAPABILITY_DENIED
        }
        auditHook?.logEvent(event, request, safeDecision)
        
        return safeDecision
    }
}
"""
}

for filename, content in files.items():
    io.open(os.path.join(pkg, filename), 'w', encoding='utf-8').write(content)
