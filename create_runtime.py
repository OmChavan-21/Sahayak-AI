import io
import os

pkg = 'app/src/main/java/com/sahayak/app/ai/'

files = {
    'ModelLifecycleState.kt': """package com.sahayak.app.ai

enum class ModelLifecycleState {
    UNAVAILABLE,
    AVAILABLE,
    LOADING,
    READY,
    RUNNING,
    RELEASED,
    ERROR
}
""",
    'ModelConfiguration.kt': """package com.sahayak.app.ai

data class ModelConfiguration(
    val identifier: String,
    val contextLength: Int,
    val maxInputLength: Int,
    val isLocal: Boolean = true,
    val runtimeIdentifier: String
)
""",
    'PromptContext.kt': """package com.sahayak.app.ai

/**
 * Creates a clear architectural boundary between trusted application instructions
 * and untrusted user data to mitigate prompt injection.
 */
data class PromptContext(
    val systemInstructions: String,
    val securityContext: String,
    val observedEvidence: String,
    val untrustedUserContent: String
)
""",
    'RuntimeResponse.kt': """package com.sahayak.app.ai

sealed class RuntimeResponse {
    data class Success(val rawText: String) : RuntimeResponse()
    data class Error(val message: String) : RuntimeResponse()
    object Cancelled : RuntimeResponse()
    object Unavailable : RuntimeResponse()
}
""",
    'LocalAIModelRuntime.kt': """package com.sahayak.app.ai

interface LocalAIModelRuntime {
    val currentState: ModelLifecycleState
    val configuration: ModelConfiguration?
    
    suspend fun loadModel(config: ModelConfiguration): Boolean
    suspend fun generate(prompt: PromptContext): RuntimeResponse
    suspend fun release()
    suspend fun cancel()
}
""",
    'RuntimeBackedLocalAIEngine.kt': """package com.sahayak.app.ai

/**
 * An adapter that bridges the high-level Sahayak AI Engine interface 
 * to a concrete local inference runtime.
 */
class RuntimeBackedLocalAIEngine(private val runtime: LocalAIModelRuntime) : LocalAIEngine {
    override suspend fun analyze(request: LocalAIRequest): LocalAIResult {
        if (runtime.currentState != ModelLifecycleState.READY) {
            return LocalAIResult.Unavailable
        }
        
        // 1. Separate trusted instructions from untrusted user content
        val promptContext = PromptContext(
            systemInstructions = "You are Sahayak, an AI security advisor. Output structured findings.",
            securityContext = "Deterministic Risk Level: \${request.deterministicRiskLevel}",
            observedEvidence = request.extractedEvidence.joinToString { it.value },
            untrustedUserContent = request.originalText // Treat strictly as data
        )
        
        // 2. Execute inference
        val result = runtime.generate(promptContext)
        
        // 3. Map runtime responses safely to domain results
        return when (result) {
            is RuntimeResponse.Success -> {
                // Future task: safely parse rawText into LocalAIResponse
                // For now, we return Error since no real model provides structured data yet.
                LocalAIResult.Error("Structured parsing not implemented yet")
            }
            is RuntimeResponse.Error -> LocalAIResult.Error(result.message)
            is RuntimeResponse.Cancelled -> LocalAIResult.Error("Inference was cancelled")
            is RuntimeResponse.Unavailable -> LocalAIResult.Unavailable
        }
    }
}
"""
}

for filename, content in files.items():
    io.open(os.path.join(pkg, filename), 'w', encoding='utf-8').write(content)

