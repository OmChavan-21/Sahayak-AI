package com.sahayak.app.audit

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
