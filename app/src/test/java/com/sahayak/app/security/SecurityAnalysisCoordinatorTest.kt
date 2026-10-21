package com.sahayak.app.security

import com.sahayak.app.ai.NoOpSahayakAIEngine
import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Test

class SecurityAnalysisCoordinatorTest {

    @Test
    fun testAiUnavailableFallbackToDeterministic() = runBlocking {
        val coordinator = SecurityAnalysisCoordinator(aiEngine = NoOpSahayakAIEngine())
        val input = "Pay ₹49 immediately"
        
        // This should trigger HIGH_RISK or AMBIGUOUS (depends on exact regex matches, but it has pay and immediately)
        val result = coordinator.analyzeText(input)
        
        // Verify it doesn't crash and falls back to deterministic risk level
        assertNotNull(result)
        assertEquals(RiskLevel.HIGH_RISK, result.riskLevel)
        assertEquals(null, result.aiResponse) // Because NoOp engine returns unavailable
    }
}
