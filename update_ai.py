import os
import glob
import io

# 1. Define new contents
files = {
    'SahayakAITask.kt': """package com.sahayak.app.ai

enum class SahayakAITask {
    EXPLAIN_CONTENT,
    ASSESS_SECURITY,
    SUMMARIZE_EVIDENCE,
    SUGGEST_SAFE_NEXT_STEP,
    GENERATE_DRAFT
}
""",
    'SahayakAIConfidence.kt': """package com.sahayak.app.ai

enum class SahayakAIConfidence {
    HIGH_CONFIDENCE,
    MEDIUM_CONFIDENCE,
    LOW_CONFIDENCE,
    UNABLE_TO_DETERMINE
}
""",
    'SahayakAICapability.kt': """package com.sahayak.app.ai

enum class SahayakAICapability {
    INSPECT_URL,
    CREATE_DRAFT,
    CREATE_REMINDER,
    NONE
}
""",
    'SahayakAISecurityContext.kt': """package com.sahayak.app.ai

import com.sahayak.app.security.RiskLevel
import com.sahayak.app.security.RiskIndicator

data class SahayakAISecurityContext(
    val deterministicRiskLevel: RiskLevel,
    val securityIndicators: List<RiskIndicator>
)
""",
    'SahayakAIRequest.kt': """package com.sahayak.app.ai

import com.sahayak.app.input.Evidence

data class SahayakAIRequest(
    val task: SahayakAITask,
    val securityContext: SahayakAISecurityContext,
    val observedEvidence: List<Evidence>,
    val untrustedContent: String
)
""",
    'SahayakAIRecommendation.kt': """package com.sahayak.app.ai

data class SahayakAIRecommendation(
    val safeNextStep: String,
    val requestedCapability: SahayakAICapability? = null,
    val capabilityReason: String? = null
)
""",
    'SahayakAIResponse.kt': """package com.sahayak.app.ai

data class SahayakAIResponse(
    val assessment: String,
    val explanation: String,
    val evidenceReferences: List<String>,
    val confidence: SahayakAIConfidence,
    val recommendation: SahayakAIRecommendation? = null
)
""",
    'SahayakAIResult.kt': """package com.sahayak.app.ai

sealed class SahayakAIResult {
    data class Success(val response: SahayakAIResponse) : SahayakAIResult()
    data class Error(val errorMessage: String) : SahayakAIResult()
    object Unavailable : SahayakAIResult()
}
""",
    'SahayakAIEngine.kt': """package com.sahayak.app.ai

interface SahayakAIEngine {
    suspend fun analyze(request: SahayakAIRequest): SahayakAIResult
}

class NoOpSahayakAIEngine : SahayakAIEngine {
    override suspend fun analyze(request: SahayakAIRequest): SahayakAIResult {
        return SahayakAIResult.Unavailable
    }
}
""",
    'RuntimeBackedSahayakAIEngine.kt': """package com.sahayak.app.ai

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
"""
}

ai_path = 'app/src/main/java/com/sahayak/app/ai/'
for filename, content in files.items():
    io.open(os.path.join(ai_path, filename), 'w', encoding='utf-8').write(content)
    
# Remove old LocalAI files
old_files = ['LocalAIEngine.kt', 'LocalAIRequest.kt', 'LocalAIResponse.kt', 'LocalAIResult.kt', 'RuntimeBackedLocalAIEngine.kt']
for filename in old_files:
    f = os.path.join(ai_path, filename)
    if os.path.exists(f):
        os.remove(f)

