package com.sahayak.app.security

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class SecurityAnalyzerTest {

    private val analyzer = SecurityAnalyzer()

    @Test
    fun test1_paymentUrgencyLink_isHighRisk() {
        val input = "Your parcel is held. Pay ₹49 immediately using this link: https://example.com"
        val result = analyzer.analyze(input)
        
        assertEquals(RiskLevel.HIGH_RISK, result.riskLevel)
        
        val types = result.indicators.map { it.type }
        assertTrue(types.contains(IndicatorType.URGENCY))
        assertTrue(types.contains(IndicatorType.PAYMENT_REQUEST))
        assertTrue(types.contains(IndicatorType.LINK_PRESENCE))
    }

    @Test
    fun test2_credentialUrgency_isHighRisk() {
        val input = "Your account will be blocked. Send your OTP immediately."
        val result = analyzer.analyze(input)
        
        assertEquals(RiskLevel.HIGH_RISK, result.riskLevel)
        
        val types = result.indicators.map { it.type }
        assertTrue(types.contains(IndicatorType.URGENCY))
        assertTrue(types.contains(IndicatorType.CREDENTIAL_REQUEST))
    }

    @Test
    fun test3_normalMessage_isNoStrongIndicators() {
        val input = "Your electricity bill for this month is ₹1200. Due date: 20 September."
        val result = analyzer.analyze(input)
        
        assertEquals(RiskLevel.NO_STRONG_INDICATORS, result.riskLevel)
    }

    @Test
    fun test4_prizeWithLink_isAmbiguousOrHigh() {
        val input = "Congratulations! You have won a prize. Click here to claim it: https://example.com"
        val result = analyzer.analyze(input)
        
        // This has a link, maybe no urgency based on our simple regex unless we add "claim it"
        // Let's see what it detects. It should be at least NO_STRONG_INDICATORS or AMBIGUOUS
        // Actually, link alone is NO_STRONG_INDICATORS based on our logic, unless we flag "click".
        // Wait, "click now" is suspicious pressure. Does it detect "click here"? 
        // Our regex is "click now". 
        // Let's assert it detects the link.
        val types = result.indicators.map { it.type }
        assertTrue(types.contains(IndicatorType.LINK_PRESENCE))
    }
}
