import os
import io

audit_pkg = 'app/src/main/java/com/sahayak/app/audit/'
os.makedirs(audit_pkg, exist_ok=True)

files = {
    'SecurityEventType.kt': """package com.sahayak.app.audit

enum class SecurityEventType {
    INPUT_RECEIVED,
    EVIDENCE_EXTRACTED,
    AI_ANALYSIS_REQUESTED,
    AI_ANALYSIS_COMPLETED,
    AI_RECOMMENDATION_CREATED,
    CAPABILITY_REQUESTED,
    CAPABILITY_ALLOWED,
    CAPABILITY_REQUIRES_CONFIRMATION,
    CAPABILITY_DENIED,
    CAPABILITY_UNAVAILABLE,
    USER_CONFIRMATION_REQUESTED,
    USER_CONFIRMED,
    USER_REJECTED,
    ACTION_REQUESTED,
    ACTION_ALLOWED,
    ACTION_BLOCKED,
    ACTION_EXECUTED,
    SECURITY_STATE_CHANGED
}
""",
    'SecurityReasonCode.kt': """package com.sahayak.app.audit

enum class SecurityReasonCode {
    UNKNOWN_CAPABILITY,
    POLICY_BLOCKED,
    USER_CONFIRMATION_REQUIRED,
    USER_REJECTED,
    UNTRUSTED_SOURCE,
    INSUFFICIENT_EVIDENCE,
    DANGEROUS_ACTION,
    CAPABILITY_UNAVAILABLE,
    INVALID_REQUEST,
    SCOPE_VIOLATION,
    AI_RECOMMENDATION_ONLY,
    USER_CONFIRMED,
    NONE
}
""",
    'SensitivityClassification.kt': """package com.sahayak.app.audit

enum class SensitivityClassification {
    PUBLIC_SAFE,
    METADATA_ONLY,
    REDACTED_CONTENT,
    SENSITIVE_CONTENT
}
""",
    'SecurityEvent.kt': """package com.sahayak.app.audit

import com.sahayak.app.actions.ActionDecision
import com.sahayak.app.actions.ActionType
import com.sahayak.app.capabilities.CapabilityDecision
import com.sahayak.app.capabilities.SahayakCapability
import com.sahayak.app.capabilities.TrustLevel

data class SecurityEvent(
    val eventId: String,
    val correlationId: String,
    val eventType: SecurityEventType,
    val timestampMs: Long = System.currentTimeMillis(),
    val sourceComponent: String,
    val trustLevel: TrustLevel,
    val capabilityId: SahayakCapability? = null,
    val actionType: ActionType? = null,
    val capabilityDecision: CapabilityDecision? = null,
    val actionDecision: ActionDecision? = null,
    val reasonCode: SecurityReasonCode = SecurityReasonCode.NONE,
    val sensitivityClassification: SensitivityClassification = SensitivityClassification.METADATA_ONLY
)
""",
    'SecurityDecisionRecord.kt': """package com.sahayak.app.audit

import com.sahayak.app.input.InputType
import com.sahayak.app.actions.ActionDecision
import com.sahayak.app.capabilities.CapabilityRequest

data class SecurityDecisionRecord(
    val correlationId: String,
    val inputCategory: InputType,
    val evidenceReferences: List<String>,
    val aiRecommendationId: String?,
    val capabilityRequest: CapabilityRequest?,
    val policyDecision: ActionDecision,
    val userDecision: UserDecision,
    val finalOutcome: FinalOutcome,
    val reasonCode: SecurityReasonCode
)

enum class UserDecision {
    CONFIRMED,
    REJECTED,
    NOT_APPLICABLE,
    PENDING
}

enum class FinalOutcome {
    ALLOWED,
    BLOCKED,
    EXECUTED,
    UNAVAILABLE,
    PENDING
}
""",
    'SecurityAuditSink.kt': """package com.sahayak.app.audit

interface SecurityAuditSink {
    fun recordEvent(event: SecurityEvent)
    fun recordDecision(decision: SecurityDecisionRecord)
}

class InMemorySecurityAuditSink : SecurityAuditSink {
    private val events = mutableListOf<SecurityEvent>()
    private val decisions = mutableListOf<SecurityDecisionRecord>()
    
    override fun recordEvent(event: SecurityEvent) {
        // Enforce privacy constraint: don't store raw sensitive content
        require(event.sensitivityClassification != SensitivityClassification.SENSITIVE_CONTENT) {
            "Raw sensitive content cannot be audited."
        }
        events.add(event)
    }
    
    override fun recordDecision(decision: SecurityDecisionRecord) {
        decisions.add(decision)
    }

    fun getEvents(correlationId: String): List<SecurityEvent> {
        return events.filter { it.correlationId == correlationId }
    }
    
    fun getDecision(correlationId: String): SecurityDecisionRecord? {
        return decisions.find { it.correlationId == correlationId }
    }
    
    fun clear() {
        events.clear()
        decisions.clear()
    }
}
"""
}

for filename, content in files.items():
    io.open(os.path.join(audit_pkg, filename), 'w', encoding='utf-8').write(content)

