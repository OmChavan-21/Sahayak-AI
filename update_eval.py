import io
import os

path = 'app/src/main/java/com/sahayak/app/capabilities/CapabilityPolicyEvaluator.kt'
c = """package com.sahayak.app.capabilities

import com.sahayak.app.actions.ActionPolicyEngine
import com.sahayak.app.actions.ActionDecision
import com.sahayak.app.audit.*
import java.util.UUID

class CapabilityPolicyEvaluator(
    private val registry: CapabilityProtocolRegistry,
    private val actionPolicyEngine: ActionPolicyEngine,
    private val auditSink: SecurityAuditSink? = null
) {
    fun evaluate(request: CapabilityRequest): CapabilityDecision {
        logAudit(SecurityEventType.CAPABILITY_REQUESTED, request, null, SecurityReasonCode.NONE)

        // 1. Check registry
        val metadata = registry.getMetadata(request.capability)
        if (metadata == null) {
            // Unknown capability fails closed
            val decision = CapabilityDecision.INVALID_REQUEST
            logAudit(SecurityEventType.CAPABILITY_DENIED, request, decision, SecurityReasonCode.UNKNOWN_CAPABILITY)
            return decision
        }

        if (!metadata.isImplemented || (!metadata.isAllowedInPrototype && request.capability != SahayakCapability.INSPECT_URL)) {
             val decision = CapabilityDecision.UNAVAILABLE
             logAudit(SecurityEventType.CAPABILITY_UNAVAILABLE, request, decision, SecurityReasonCode.CAPABILITY_UNAVAILABLE)
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

        val (eventType, reasonCode) = when(safeDecision) {
            CapabilityDecision.ALLOWED -> Pair(SecurityEventType.CAPABILITY_ALLOWED, SecurityReasonCode.NONE)
            CapabilityDecision.REQUIRES_CONFIRMATION -> Pair(SecurityEventType.CAPABILITY_REQUIRES_CONFIRMATION, SecurityReasonCode.USER_CONFIRMATION_REQUIRED)
            else -> Pair(SecurityEventType.CAPABILITY_DENIED, SecurityReasonCode.POLICY_BLOCKED)
        }
        
        logAudit(eventType, request, safeDecision, reasonCode)
        
        return safeDecision
    }
    
    private fun logAudit(
        eventType: SecurityEventType, 
        request: CapabilityRequest, 
        decision: CapabilityDecision?,
        reasonCode: SecurityReasonCode
    ) {
        val event = SecurityEvent(
            eventId = UUID.randomUUID().toString(),
            correlationId = request.correlationId,
            eventType = eventType,
            sourceComponent = request.requestingComponent,
            trustLevel = request.trustLevel,
            capabilityId = request.capability,
            actionType = request.capability.actionType,
            capabilityDecision = decision,
            reasonCode = reasonCode,
            sensitivityClassification = SensitivityClassification.METADATA_ONLY
        )
        auditSink?.recordEvent(event)
    }
}
"""
io.open(path, 'w', encoding='utf-8').write(c)

os.remove('app/src/main/java/com/sahayak/app/capabilities/CapabilityAuditHook.kt')

# Fix tests
path = 'app/src/test/java/com/sahayak/app/capabilities/CapabilitySystemTest.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('import com.sahayak.app.capabilities.CapabilityAuditHook', '')
c = c.replace('import com.sahayak.app.capabilities.AuditEventType', 'import com.sahayak.app.audit.*')
c = c.replace('var auditedEventType: AuditEventType? = null', 'var auditedEventType: SecurityEventType? = null')
c = c.replace('val hook = object : CapabilityAuditHook {', 'val hook = object : SecurityAuditSink {\n            override fun recordDecision(decision: SecurityDecisionRecord) {}\n            override fun recordEvent(event: SecurityEvent) { auditedEventType = event.eventType }')
c = c.replace('override fun logEvent(eventType: AuditEventType, request: CapabilityRequest, decision: CapabilityDecision?) {', '')
c = c.replace('auditedEventType = eventType', '')
c = c.replace('}', '}') # need to be careful with replace here
io.open(path, 'w', encoding='utf-8').write(c)

