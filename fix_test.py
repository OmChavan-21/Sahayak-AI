import io
import os

path = 'app/src/test/java/com/sahayak/app/capabilities/CapabilitySystemTest.kt'
c = io.open(path, 'r', encoding='utf-8').read()

import re

# find the method testAuditHookReceivesSecurityRelevantDecisions and replace it entirely
def replace_test(match):
    return """@Test
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
"""

new_c = re.sub(r'@Test\s+fun testAuditHookReceivesSecurityRelevantDecisions\(\) \{.*\}', replace_test, c, flags=re.DOTALL)
io.open(path, 'w', encoding='utf-8').write(new_c)

