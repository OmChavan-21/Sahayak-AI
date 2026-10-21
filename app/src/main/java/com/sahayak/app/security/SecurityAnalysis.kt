package com.sahayak.app.security

import com.sahayak.app.ai.SahayakAIResponse

data class SecurityAnalysis(
    val riskLevel: RiskLevel,
    val indicators: List<RiskIndicator>,
    val explanation: String,
    val recommendation: String,
    val aiResponse: SahayakAIResponse? = null
)
