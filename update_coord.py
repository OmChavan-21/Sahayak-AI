import io
import os

path = 'app/src/main/java/com/sahayak/app/security/SecurityAnalysisCoordinator.kt'
c = """package com.sahayak.app.security

import com.sahayak.app.ai.SahayakAIEngine
import com.sahayak.app.ai.SahayakAIRequest
import com.sahayak.app.ai.SahayakAITask
import com.sahayak.app.ai.SahayakAISecurityContext
import com.sahayak.app.ai.SahayakAIResult
import com.sahayak.app.input.InputType
import com.sahayak.app.input.TextEvidenceExtractor
import com.sahayak.app.input.UserInput
import com.sahayak.app.input.OcrEngine
import com.sahayak.app.input.NoOpOcrEngine
import com.sahayak.app.input.OcrResult
import com.sahayak.app.audit.*
import com.sahayak.app.capabilities.TrustLevel
import java.util.UUID

class SecurityAnalysisCoordinator(
    private val deterministicAnalyzer: SecurityAnalyzer = SecurityAnalyzer(),
    private val aiEngine: SahayakAIEngine,
    private val textExtractor: TextEvidenceExtractor = TextEvidenceExtractor(),
    private val ocrEngine: OcrEngine = NoOpOcrEngine(),
    private val auditSink: SecurityAuditSink? = null
) {

    suspend fun analyze(userInput: UserInput): SecurityAnalysis {
        val correlationId = UUID.randomUUID().toString()
        logAudit(correlationId, SecurityEventType.INPUT_RECEIVED, TrustLevel.LEVEL_1_USER_PROVIDED_EVIDENCE)

        val textToAnalyze: String

        if (userInput.inputType == InputType.IMAGE || userInput.inputType == InputType.SCREENSHOT) {
            val ocrResult = ocrEngine.extractText(userInput)
            when (ocrResult) {
                is OcrResult.Success -> {
                    textToAnalyze = ocrResult.recognizedText
                }
                is OcrResult.Error -> {
                    return SecurityAnalysis(
                        riskLevel = RiskLevel.UNABLE_TO_ANALYZE,
                        indicators = emptyList(),
                        explanation = "Unable to read text from this image. ${ocrResult.errorMessage}",
                        recommendation = "Try a clearer image or provide the text another way."
                    )
                }
                is OcrResult.Unavailable -> {
                    return SecurityAnalysis(
                        riskLevel = RiskLevel.UNABLE_TO_ANALYZE,
                        indicators = emptyList(),
                        explanation = "Unable to read text from this image.",
                        recommendation = "Try a clearer image or provide the text another way."
                    )
                }
            }
        } else {
            textToAnalyze = userInput.rawText ?: ""
        }

        val extractedEvidence = textExtractor.extract(userInput.copy(rawText = textToAnalyze))
        logAudit(correlationId, SecurityEventType.EVIDENCE_EXTRACTED, TrustLevel.LEVEL_2_SYSTEM_VERIFIED)

        val deterministicResult = deterministicAnalyzer.analyze(textToAnalyze)

        val request = SahayakAIRequest(
            task = SahayakAITask.ASSESS_SECURITY,
            securityContext = SahayakAISecurityContext(
                deterministicRiskLevel = deterministicResult.riskLevel,
                securityIndicators = deterministicResult.indicators
            ),
            observedEvidence = extractedEvidence,
            untrustedContent = textToAnalyze
        )

        logAudit(correlationId, SecurityEventType.AI_ANALYSIS_REQUESTED, TrustLevel.LEVEL_2_SYSTEM_VERIFIED)
        val aiResult = aiEngine.analyze(request)
        logAudit(correlationId, SecurityEventType.AI_ANALYSIS_COMPLETED, TrustLevel.LEVEL_3_SAHAYAK_GENERATED)

        return when (aiResult) {
            is SahayakAIResult.Unavailable, is SahayakAIResult.Error -> deterministicResult
            is SahayakAIResult.Success -> {
                if (aiResult.response.recommendation != null) {
                    logAudit(correlationId, SecurityEventType.AI_RECOMMENDATION_CREATED, TrustLevel.LEVEL_3_SAHAYAK_GENERATED)
                }
                deterministicResult.copy(aiResponse = aiResult.response)
            }
        }
    }

    suspend fun analyzeText(text: String): SecurityAnalysis {
        return analyze(UserInput(inputType = InputType.TEXT, rawText = text))
    }
    
    private fun logAudit(correlationId: String, eventType: SecurityEventType, trustLevel: TrustLevel) {
        val event = SecurityEvent(
            eventId = UUID.randomUUID().toString(),
            correlationId = correlationId,
            eventType = eventType,
            sourceComponent = "SecurityAnalysisCoordinator",
            trustLevel = trustLevel,
            sensitivityClassification = SensitivityClassification.METADATA_ONLY
        )
        auditSink?.recordEvent(event)
    }
}
"""
io.open(path, 'w', encoding='utf-8').write(c)

# We need to update SecurityAnalysisCoordinatorTest to compile correctly without issues.
