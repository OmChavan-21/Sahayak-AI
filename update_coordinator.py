import io

path = 'app/src/main/java/com/sahayak/app/security/RiskLevel.kt'
c = io.open(path, 'r', encoding='utf-8').read()
if "UNABLE_TO_ANALYZE" not in c:
    c = c.replace("NO_STRONG_INDICATORS", "NO_STRONG_INDICATORS,\n    UNABLE_TO_ANALYZE")
io.open(path, 'w', encoding='utf-8').write(c)

path = 'app/src/main/java/com/sahayak/app/security/SecurityAnalysisCoordinator.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('import com.sahayak.app.input.UserInput', 'import com.sahayak.app.input.UserInput\nimport com.sahayak.app.input.OcrEngine\nimport com.sahayak.app.input.NoOpOcrEngine\nimport com.sahayak.app.input.OcrResult')
c = c.replace('private val textExtractor: TextEvidenceExtractor = TextEvidenceExtractor()', 'private val textExtractor: TextEvidenceExtractor = TextEvidenceExtractor(),\n    private val ocrEngine: OcrEngine = NoOpOcrEngine()')

analyze_method = """
    suspend fun analyze(userInput: UserInput): SecurityAnalysis {
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
                        explanation = "Unable to read text from this image. \${ocrResult.errorMessage}",
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
        val deterministicResult = deterministicAnalyzer.analyze(textToAnalyze)

        val request = LocalAIRequest(
            originalText = textToAnalyze,
            deterministicRiskLevel = deterministicResult.riskLevel,
            securityIndicators = deterministicResult.indicators,
            extractedEvidence = extractedEvidence,
            extractedContext = null
        )

        val aiResult = aiEngine.analyze(request)

        return when (aiResult) {
            is LocalAIResult.Unavailable, is LocalAIResult.Error -> deterministicResult
            is LocalAIResult.Success -> deterministicResult.copy(aiResponse = aiResult.response)
        }
    }
"""

if "fun analyze(" not in c:
    c = c.replace("    suspend fun analyzeText(text: String): SecurityAnalysis {", analyze_method + "\n    suspend fun analyzeText(text: String): SecurityAnalysis {")

io.open(path, 'w', encoding='utf-8').write(c)

# Update ResultScreen to use analyze(UserInput) where appropriate? 
# Wait, ResultScreen uses analyzeText(text). I don't need to change ResultScreen if it still calls analyzeText!
# analyzeText can just call analyze(UserInput(TEXT, text))
c = c.replace("""    suspend fun analyzeText(text: String): SecurityAnalysis {
        // 0. Extract evidence""", """    suspend fun analyzeText(text: String): SecurityAnalysis {
        return analyze(UserInput(inputType = InputType.TEXT, rawText = text))
    }
    
    suspend fun analyzeTextOld(text: String): SecurityAnalysis {
        // 0. Extract evidence""")

io.open(path, 'w', encoding='utf-8').write(c)
