import io
import os

# Update SecurityAnalysisCoordinator
path = 'app/src/main/java/com/sahayak/app/security/SecurityAnalysisCoordinator.kt'
c = io.open(path, 'r', encoding='utf-8').read()

c = c.replace('import com.sahayak.app.ai.LocalAIEngine', 'import com.sahayak.app.ai.SahayakAIEngine')
c = c.replace('import com.sahayak.app.ai.LocalAIRequest', 'import com.sahayak.app.ai.SahayakAIRequest\nimport com.sahayak.app.ai.SahayakAITask\nimport com.sahayak.app.ai.SahayakAISecurityContext')
c = c.replace('import com.sahayak.app.ai.LocalAIResult', 'import com.sahayak.app.ai.SahayakAIResult')
c = c.replace('private val aiEngine: LocalAIEngine', 'private val aiEngine: SahayakAIEngine')
c = c.replace('val request = LocalAIRequest(\n            originalText = textToAnalyze,\n            deterministicRiskLevel = deterministicResult.riskLevel,\n            securityIndicators = deterministicResult.indicators,\n            extractedEvidence = extractedEvidence,\n            extractedContext = null\n        )', 
"""val request = SahayakAIRequest(
            task = SahayakAITask.ASSESS_SECURITY,
            securityContext = SahayakAISecurityContext(
                deterministicRiskLevel = deterministicResult.riskLevel,
                securityIndicators = deterministicResult.indicators
            ),
            observedEvidence = extractedEvidence,
            untrustedContent = textToAnalyze
        )""")
c = c.replace('is LocalAIResult.Unavailable, is LocalAIResult.Error', 'is SahayakAIResult.Unavailable, is SahayakAIResult.Error')
c = c.replace('is LocalAIResult.Success', 'is SahayakAIResult.Success')

io.open(path, 'w', encoding='utf-8').write(c)


# Update SecurityAnalysis
path = 'app/src/main/java/com/sahayak/app/security/SecurityAnalysis.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('import com.sahayak.app.ai.LocalAIResponse', 'import com.sahayak.app.ai.SahayakAIResponse')
c = c.replace('val aiResponse: LocalAIResponse? = null', 'val aiResponse: SahayakAIResponse? = null')
io.open(path, 'w', encoding='utf-8').write(c)

# Update ResultScreen
path = 'app/src/main/java/com/sahayak/app/ui/screens/ResultScreen.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('import com.sahayak.app.ai.NoOpLocalAIEngine', 'import com.sahayak.app.ai.NoOpSahayakAIEngine')
c = c.replace('NoOpLocalAIEngine()', 'NoOpSahayakAIEngine()')
io.open(path, 'w', encoding='utf-8').write(c)

