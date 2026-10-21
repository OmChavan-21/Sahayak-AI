package com.sahayak.app.capabilities

data class CapabilityRequest(
    val capability: SahayakCapability,
    val requestingComponent: String,
    val purpose: String,
    val targetResource: String? = null,
    val requestedScope: CapabilityScope,
    val originatingRecommendationId: String? = null,
    val requiresUserConfirmation: Boolean = true,
    val timestampMs: Long = System.currentTimeMillis(),
    val trustLevel: TrustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED,
    val correlationId: String
)
