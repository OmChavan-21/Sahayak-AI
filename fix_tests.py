import os
import io

# Fix SahayakAIContractTest
path = 'app/src/test/java/com/sahayak/app/ai/SahayakAIContractTest.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('RiskLevel.HIGH', 'RiskLevel.HIGH_RISK')
c = c.replace('Evidence(EvidenceType.URL, "http://suspicious.com")', 'Evidence(EvidenceType.URL, "http://suspicious.com", "http://suspicious.com")')
c = c.replace('Evidence(EvidenceType.PHONE_NUMBER, "+1234567890")', 'Evidence(EvidenceType.PHONE_NUMBER, "+1234567890", "+1234567890")')
io.open(path, 'w', encoding='utf-8').write(c)

# Refactor LocalAIEngineTest -> SahayakAIEngineTest
old_test = 'app/src/test/java/com/sahayak/app/ai/LocalAIEngineTest.kt'
new_test = 'app/src/test/java/com/sahayak/app/ai/SahayakAIEngineTest.kt'

content = """package com.sahayak.app.ai

import com.sahayak.app.security.RiskLevel
import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class SahayakAIEngineTest {

    @Test
    fun testNoOpEngineReturnsUnavailable() = runBlocking {
        val engine = NoOpSahayakAIEngine()
        val request = SahayakAIRequest(
            task = SahayakAITask.ASSESS_SECURITY,
            securityContext = SahayakAISecurityContext(RiskLevel.NO_STRONG_INDICATORS, emptyList()),
            observedEvidence = emptyList(),
            untrustedContent = "test"
        )
        val result = engine.analyze(request)
        
        assertTrue(result is SahayakAIResult.Unavailable)
    }

    @Test
    fun testSahayakAIRequestCanContainStructuredEvidence() {
        val request = SahayakAIRequest(
            task = SahayakAITask.EXPLAIN_CONTENT,
            securityContext = SahayakAISecurityContext(RiskLevel.HIGH_RISK, emptyList()),
            observedEvidence = emptyList(),
            untrustedContent = "text"
        )
        
        assertEquals("text", request.untrustedContent)
    }

    @Test
    fun testSahayakAIResponseSupportsUncertainty() {
        val response = SahayakAIResponse(
            assessment = "Summary",
            explanation = "Unable to verify",
            evidenceReferences = emptyList(),
            confidence = SahayakAIConfidence.UNABLE_TO_DETERMINE,
            recommendation = null
        )
        
        assertEquals(SahayakAIConfidence.UNABLE_TO_DETERMINE, response.confidence)
    }
}
"""

if os.path.exists(old_test):
    os.remove(old_test)

io.open(new_test, 'w', encoding='utf-8').write(content)

