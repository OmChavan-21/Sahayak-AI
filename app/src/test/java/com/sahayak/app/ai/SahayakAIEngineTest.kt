package com.sahayak.app.ai

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
