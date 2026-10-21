package com.sahayak.app.ai

/**
 * An adapter that bridges the high-level Sahayak AI Engine interface 
 * to a concrete local inference runtime.
 */
class RuntimeBackedSahayakAIEngine(private val runtime: LocalAIModelRuntime) : SahayakAIEngine {
    override suspend fun analyze(request: SahayakAIRequest): SahayakAIResult {
        if (runtime.currentState != ModelLifecycleState.READY) {
            return SahayakAIResult.Unavailable
        }
        
        // 1. Separate trusted instructions from untrusted user content
        val promptContext = PromptContext(
            systemInstructions = "You are Sahayak, an AI security advisor. Task: ${request.task}. Output structured findings.",
            securityContext = "Deterministic Risk Level: ${request.securityContext.deterministicRiskLevel}",
            observedEvidence = request.observedEvidence.joinToString { it.value },
            untrustedUserContent = request.untrustedContent // Treat strictly as data
        )
        
        // 2. Execute inference
        val result = runtime.generate(promptContext)
        
        // 3. Map runtime responses safely to domain results
        return when (result) {
            is RuntimeResponse.Success -> {
                SahayakAIResult.Error("Structured parsing not implemented yet")
            }
            is RuntimeResponse.Error -> SahayakAIResult.Error(result.message)
            is RuntimeResponse.Cancelled -> SahayakAIResult.Error("Inference was cancelled")
            is RuntimeResponse.Unavailable -> SahayakAIResult.Unavailable
        }
    }
}
