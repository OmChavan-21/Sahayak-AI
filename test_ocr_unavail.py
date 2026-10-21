import io
path = 'app/src/test/java/com/sahayak/app/input/OcrEngineTest.kt'
c = io.open(path, 'r', encoding='utf-8').read()

imports = """import com.sahayak.app.security.RiskLevel
import com.sahayak.app.security.SecurityAnalysisCoordinator
import com.sahayak.app.ai.NoOpLocalAIEngine
import kotlinx.coroutines.runBlocking
"""
if "import com.sahayak.app.security.RiskLevel" not in c:
    c = c.replace('import kotlinx.coroutines.runBlocking', imports)

test = """
    @Test
    fun testOcrUnavailableProducesUnableToAnalyze() = runBlocking {
        val coordinator = SecurityAnalysisCoordinator(aiEngine = NoOpLocalAIEngine())
        val input = UserInput(InputType.IMAGE)
        val result = coordinator.analyze(input)
        
        assertEquals(RiskLevel.UNABLE_TO_ANALYZE, result.riskLevel)
        assertTrue(result.explanation.contains("Unable to read text"))
    }
}"""
c = c[:c.rfind('}')] + test
io.open(path, 'w', encoding='utf-8').write(c)
