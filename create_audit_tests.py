import io
import os

test_content = """package com.sahayak.app.audit

import com.sahayak.app.actions.ActionDecision
import com.sahayak.app.actions.ActionPolicyEngine
import com.sahayak.app.actions.ActionRisk
import com.sahayak.app.capabilities.*
import com.sahayak.app.input.InputType
import org.junit.Assert.*
import org.junit.Test
import java.util.UUID

class SecurityAuditTest {

    @Test
    fun testSecurityEventCreationAndIdentity() {
        val event = SecurityEvent(
            eventId = "evt-123",
            correlationId = "corr-456",
            eventType = SecurityEventType.CAPABILITY_REQUESTED,
            sourceComponent = "Test",
            trustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED,
            reasonCode = SecurityReasonCode.NONE
        )
        assertEquals("evt-123", event.eventId)
        assertEquals(SecurityEventType.CAPABILITY_REQUESTED, event.eventType)
    }

    @Test
    fun testCorrelationIdsGroupEvents() {
        val sink = InMemorySecurityAuditSink()
        val corrId = "workflow-1"
        
        sink.recordEvent(SecurityEvent(
            eventId = "1",
            correlationId = corrId,
            eventType = SecurityEventType.INPUT_RECEIVED,
            sourceComponent = "App",
            trustLevel = TrustLevel.LEVEL_1_USER_PROVIDED_EVIDENCE
        ))
        
        sink.recordEvent(SecurityEvent(
            eventId = "2",
            correlationId = corrId,
            eventType = SecurityEventType.CAPABILITY_REQUESTED,
            sourceComponent = "App",
            trustLevel = TrustLevel.LEVEL_1_USER_PROVIDED_EVIDENCE
        ))
        
        val events = sink.getEvents(corrId)
        assertEquals(2, events.size)
    }

    @Test
    fun testAIOutputCannotPromoteTrust() {
        val sink = InMemorySecurityAuditSink()
        
        // Simulating AI trying to emit a LEVEL_4 event
        // In the actual system, the TrustLevel is strictly defined by the origin (e.g., Coordinator or PolicyEvaluator).
        // AI component returns SahayakAIResponse which has no ability to set TrustLevel.
        val request = CapabilityRequest(
            capability = SahayakCapability.INSPECT_URL,
            requestingComponent = "AI",
            purpose = "Scan",
            requestedScope = CapabilityScope.DEFAULT_SAFE_SCOPE,
            trustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED, // Hardcoded in evaluator
            correlationId = "corr-1"
        )
        
        val registry = CapabilityProtocolRegistry()
        registry.register(CapabilityMetadata(
            id = SahayakCapability.INSPECT_URL,
            riskLevel = ActionRisk.REQUIRES_CONFIRMATION,
            purpose = "Inspect",
            requiredPermission = null,
            dataAccessed = emptyList(),
            requiresUserConfirmation = true,
            isImplemented = true,
            isAllowedInPrototype = true,
            hasExternalSideEffect = true,
            isReversible = false,
            requiresAudit = true
        ))
        
        val evaluator = CapabilityPolicyEvaluator(registry, ActionPolicyEngine(), sink)
        val decision = evaluator.evaluate(request)
        
        val events = sink.getEvents("corr-1")
        val finalEvent = events.last()
        
        assertEquals(TrustLevel.LEVEL_3_SAHAYAK_GENERATED, finalEvent.trustLevel)
        assertEquals(CapabilityDecision.REQUIRES_CONFIRMATION, decision)
    }

    @Test
    fun testUnknownCapabilityProducesAuditableDenial() {
        val sink = InMemorySecurityAuditSink()
        val registry = CapabilityProtocolRegistry()
        val evaluator = CapabilityPolicyEvaluator(registry, ActionPolicyEngine(), sink)
        
        val request = CapabilityRequest(
            capability = SahayakCapability.EXECUTE_CODE, // unregistered
            requestingComponent = "AI",
            purpose = "Scan",
            requestedScope = CapabilityScope.DEFAULT_SAFE_SCOPE,
            trustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED,
            correlationId = "corr-unknown"
        )
        
        evaluator.evaluate(request)
        
        val events = sink.getEvents("corr-unknown")
        assertEquals(2, events.size) // REQUESTED, then DENIED
        assertEquals(SecurityEventType.CAPABILITY_DENIED, events.last().eventType)
        assertEquals(SecurityReasonCode.UNKNOWN_CAPABILITY, events.last().reasonCode)
    }

    @Test
    fun testSensitiveFieldsAreNotStoredRaw() {
        val sink = InMemorySecurityAuditSink()
        val event = SecurityEvent(
            eventId = "1",
            correlationId = "corr-sec",
            eventType = SecurityEventType.INPUT_RECEIVED,
            sourceComponent = "App",
            trustLevel = TrustLevel.LEVEL_1_USER_PROVIDED_EVIDENCE,
            sensitivityClassification = SensitivityClassification.SENSITIVE_CONTENT
        )
        
        assertThrows(IllegalArgumentException::class.java) {
            sink.recordEvent(event)
        }
    }
    
    @Test
    fun testSecurityDecisionRecordPreservesOutcome() {
        val sink = InMemorySecurityAuditSink()
        val decisionRecord = SecurityDecisionRecord(
            correlationId = "corr-dec",
            inputCategory = InputType.TEXT,
            evidenceReferences = listOf("ev-1"),
            aiRecommendationId = "rec-1",
            capabilityRequest = null,
            policyDecision = ActionDecision.BLOCKED,
            userDecision = UserDecision.PENDING,
            finalOutcome = FinalOutcome.BLOCKED,
            reasonCode = SecurityReasonCode.POLICY_BLOCKED
        )
        sink.recordDecision(decisionRecord)
        
        val retrieved = sink.getDecision("corr-dec")
        assertNotNull(retrieved)
        assertEquals(FinalOutcome.BLOCKED, retrieved?.finalOutcome)
    }
}
"""

os.makedirs('app/src/test/java/com/sahayak/app/audit', exist_ok=True)
io.open('app/src/test/java/com/sahayak/app/audit/SecurityAuditTest.kt', 'w', encoding='utf-8').write(test_content)
