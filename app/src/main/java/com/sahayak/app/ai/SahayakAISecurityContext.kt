package com.sahayak.app.ai

import com.sahayak.app.security.RiskLevel
import com.sahayak.app.security.RiskIndicator

data class SahayakAISecurityContext(
    val deterministicRiskLevel: RiskLevel,
    val securityIndicators: List<RiskIndicator>
)
