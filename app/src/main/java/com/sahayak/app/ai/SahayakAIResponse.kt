package com.sahayak.app.ai

data class SahayakAIResponse(
    val assessment: String,
    val explanation: String,
    val evidenceReferences: List<String>,
    val confidence: SahayakAIConfidence,
    val recommendation: SahayakAIRecommendation? = null
)
