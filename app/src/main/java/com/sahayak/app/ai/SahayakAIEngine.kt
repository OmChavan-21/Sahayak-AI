package com.sahayak.app.ai

interface SahayakAIEngine {
    suspend fun analyze(request: SahayakAIRequest): SahayakAIResult
}

class NoOpSahayakAIEngine : SahayakAIEngine {
    override suspend fun analyze(request: SahayakAIRequest): SahayakAIResult {
        return SahayakAIResult.Unavailable
    }
}
