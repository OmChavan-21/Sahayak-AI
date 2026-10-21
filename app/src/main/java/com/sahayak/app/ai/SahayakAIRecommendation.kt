package com.sahayak.app.ai

import com.sahayak.app.capabilities.SahayakCapability

data class SahayakAIRecommendation(
    val safeNextStep: String,
    val requestedCapability: SahayakCapability? = null,
    val capabilityReason: String? = null
)
