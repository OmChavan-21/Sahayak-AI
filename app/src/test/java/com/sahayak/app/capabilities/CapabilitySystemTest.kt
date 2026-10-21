package com.sahayak.app.capabilities

import com.sahayak.app.actions.ActionDecision
import com.sahayak.app.actions.ActionPolicyEngine
import com.sahayak.app.actions.ActionRisk
import com.sahayak.app.actions.ActionType
import com.sahayak.app.audit.*
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertThrows
import org.junit.Assert.assertTrue
import org.junit.Test

class CapabilitySystemTest {

    private fun createRegistry(): CapabilityProtocolRegistry {
        val registry = CapabilityProtocolRegistry()
        registry.register(CapabilityMetadata(
            id = SahayakCapability.READ_USER_INPUT,
            riskLevel = ActionRisk.SAFE,
            purpose = "Read user text",
            requiredPermission = null,
            dataAccessed = listOf("user_text"),
            requiresUserConfirmation = false,
            isImplemented = true,
            isAllowedInPrototype = true,
            hasExternalSideEffect = false,
            isReversible = true,
            requiresAudit = false
        ))
        registry.register(CapabilityMetadata(
            id = SahayakCapability.INSPECT_URL,
            riskLevel = ActionRisk.REQUIRES_CONFIRMATION,
            purpose = "Inspect URL safely",
            requiredPermission = "INTERNET",
            dataAccessed = listOf("url_content"),
            requiresUserConfirmation = true,
            isImplemented = true,
            isAllowedInPrototype = true,
            hasExternalSideEffect = true,
            isReversible = false,
            requiresAudit = true
        ))
        registry.register(CapabilityMetadata(
            id = SahayakCapability.MAKE_PAYMENT,
            riskLevel = ActionRisk.BLOCKED,
            purpose = "Pay",
            requiredPermission = null,
            dataAccessed = listOf("financial"),
            requiresUserConfirmation = true,
            isImplemented = false,
            isAllowedInPrototype = false,
            hasExternalSideEffect = true,
            isReversible = false,
            requiresAudit = true
        ))
        return registry
    }

    @Test
    fun testKnownCapabilityLookup() {
        val registry = createRegistry()
        val metadata = registry.getMetadata(SahayakCapability.READ_USER_INPUT)
        assertNotNull(metadata)
        assertEquals(SahayakCapability.READ_USER_INPUT, metadata?.id)
    }

    @Test
    fun testUnknownCapabilityRejection() {
        val registry = createRegistry()
        val metadata = registry.getMetadata(SahayakCapability.EXECUTE_CODE)
        assertNull(metadata)
    }

    @Test
    fun testDuplicateCapabilityRegistration() {
        val registry = createRegistry()
        assertThrows(IllegalArgumentException::class.java) {
            registry.register(CapabilityMetadata(
                id = SahayakCapability.READ_USER_INPUT,
                riskLevel = ActionRisk.SAFE,
                purpose = "Duplicate",
                requiredPermission = null,
                dataAccessed = emptyList(),
                requiresUserConfirmation = false,
                isImplemented = true,
                isAllowedInPrototype = true,
                hasExternalSideEffect = false,
                isReversible = true,
                requiresAudit = false
            ))
        }
    }

    @Test
    fun testCapabilityMetadataIntegrity() {
        val registry = createRegistry()
        val metadata = registry.getMetadata(SahayakCapability.INSPECT_URL)!!
        assertEquals("INTERNET", metadata.requiredPermission)
        assertTrue(metadata.requiresUserConfirmation)
        assertTrue(metadata.hasExternalSideEffect)
    }

    @Test
    fun testCapabilityRequestIsNotAuthorization() {
        val request = CapabilityRequest(
            capability = SahayakCapability.INSPECT_URL,
            requestingComponent = "AI",
            purpose = "Check",
            requestedScope = CapabilityScope.DEFAULT_SAFE_SCOPE,
            trustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED,
            correlationId = "test-123"
        )
        // Request object has no execute method, merely data
        assertEquals(SahayakCapability.INSPECT_URL, request.capability)
    }

    @Test
    fun testDangerousCapabilityIsNotAccidentallyEnabled() {
        val registry = createRegistry()
        val evaluator = CapabilityPolicyEvaluator(registry, ActionPolicyEngine())
        val request = CapabilityRequest(
            capability = SahayakCapability.MAKE_PAYMENT,
            requestingComponent = "AI",
            purpose = "Pay",
            requestedScope = CapabilityScope.DEFAULT_SAFE_SCOPE,
            trustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED,
            correlationId = "test-123"
        )
        val decision = evaluator.evaluate(request)
        // Since isAllowedInPrototype = false, it should be UNAVAILABLE or DENIED
        assertEquals(CapabilityDecision.UNAVAILABLE, decision)
    }

    @Test
    fun testConfirmationRequiredCapabilityCannotSilentlyExecute() {
        val registry = createRegistry()
        val evaluator = CapabilityPolicyEvaluator(registry, ActionPolicyEngine())
        val request = CapabilityRequest(
            capability = SahayakCapability.INSPECT_URL,
            requestingComponent = "AI",
            purpose = "Inspect",
            requestedScope = CapabilityScope.DEFAULT_SAFE_SCOPE,
            trustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED,
            correlationId = "test-123"
        )
        val decision = evaluator.evaluate(request)
        assertEquals(CapabilityDecision.REQUIRES_CONFIRMATION, decision)
    }

    @Test
    fun testAIOutputCannotIncreaseTrustLevel() {
        val registry = createRegistry()
        val evaluator = CapabilityPolicyEvaluator(registry, ActionPolicyEngine())
        val request = CapabilityRequest(
            capability = SahayakCapability.INSPECT_URL,
            requestingComponent = "AI",
            purpose = "Inspect",
            requestedScope = CapabilityScope.DEFAULT_SAFE_SCOPE,
            trustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED,
            correlationId = "test-123"
        )
        val decision = evaluator.evaluate(request)
        // AI trust level 3 cannot bypass the confirmation required for INSPECT_URL
        assertEquals(CapabilityDecision.REQUIRES_CONFIRMATION, decision)
    }

    @Test
    fun testScopeRestrictionsArePreserved() {
        val scope = CapabilityScope.LEAST_PRIVILEGE_URL_INSPECTION
        assertTrue(scope.requireHttps)
        assertTrue(scope.isReadOnly)
        assertEquals(false, scope.allowArbitraryCodeExecution)
    }

    @Test
    fun testUnknownCapabilityFailsClosed() {
        val registry = createRegistry()
        val evaluator = CapabilityPolicyEvaluator(registry, ActionPolicyEngine())
        val request = CapabilityRequest(
            capability = SahayakCapability.EXECUTE_CODE, // not registered
            requestingComponent = "AI",
            purpose = "Hack",
            requestedScope = CapabilityScope.DEFAULT_SAFE_SCOPE,
            trustLevel = TrustLevel.LEVEL_0_UNTRUSTED_EXTERNAL,
            correlationId = "test-123"
        )
        val decision = evaluator.evaluate(request)
        assertEquals(CapabilityDecision.INVALID_REQUEST, decision)
    }

    @Test
    fun testCapabilityDecisionDoesNotBypassActionPolicyEngine() {
        val registry = createRegistry()
        // Register SEND_MESSAGE which maps to ActionType.SEND_MESSAGE
        registry.register(CapabilityMetadata(
            id = SahayakCapability.SEND_MESSAGE,
            riskLevel = ActionRisk.USER_MUST_EXECUTE,
            purpose = "Send",
            requiredPermission = null,
            dataAccessed = emptyList(),
            requiresUserConfirmation = false, // Set to false to try to bypass
            isImplemented = true,
            isAllowedInPrototype = true,
            hasExternalSideEffect = true,
            isReversible = false,
            requiresAudit = true
        ))
        val evaluator = CapabilityPolicyEvaluator(registry, ActionPolicyEngine())
        val request = CapabilityRequest(
            capability = SahayakCapability.SEND_MESSAGE,
            requestingComponent = "AI",
            purpose = "Send",
            requestedScope = CapabilityScope.DEFAULT_SAFE_SCOPE,
            trustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED,
            correlationId = "test-123"
        )
        val decision = evaluator.evaluate(request)
        // Even though metadata says requiresUserConfirmation = false, ActionPolicyEngine sees SEND_MESSAGE as USER_MUST_EXECUTE
        assertEquals(CapabilityDecision.REQUIRES_CONFIRMATION, decision)
    }

    @Test
    fun testAuditHookReceivesSecurityRelevantDecisions() {
        val registry = createRegistry()
        var auditedEventType: SecurityEventType? = null
        val hook = object : SecurityAuditSink {
            override fun recordDecision(decision: SecurityDecisionRecord) {}
            override fun recordEvent(event: SecurityEvent) { 
                auditedEventType = event.eventType 
            }
        }
        val evaluator = CapabilityPolicyEvaluator(registry, ActionPolicyEngine(), hook)
        val request = CapabilityRequest(
            capability = SahayakCapability.INSPECT_URL,
            requestingComponent = "AI",
            purpose = "Inspect",
            requestedScope = CapabilityScope.DEFAULT_SAFE_SCOPE,
            trustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED,
            correlationId = "test-123"
        )
        evaluator.evaluate(request)
        assertEquals(SecurityEventType.CAPABILITY_REQUIRES_CONFIRMATION, auditedEventType)
    }
}
