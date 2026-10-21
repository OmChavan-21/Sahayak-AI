import os
import io

test_dir = 'app/src/test/java/com/sahayak/app/ai/'
old_test_file = os.path.join(test_dir, 'RuntimeBackedLocalAIEngineTest.kt')
new_test_file = os.path.join(test_dir, 'RuntimeBackedSahayakAIEngineTest.kt')

if os.path.exists(old_test_file):
    c = io.open(old_test_file, 'r', encoding='utf-8').read()
    c = c.replace('RuntimeBackedLocalAIEngineTest', 'RuntimeBackedSahayakAIEngineTest')
    c = c.replace('RuntimeBackedLocalAIEngine', 'RuntimeBackedSahayakAIEngine')
    c = c.replace('LocalAIResult', 'SahayakAIResult')
    
    # We need to construct SahayakAIRequest instead of LocalAIRequest
    c = c.replace('LocalAIRequest("test", RiskLevel.NO_STRONG_INDICATORS, emptyList())', 
    """SahayakAIRequest(
            task = SahayakAITask.ASSESS_SECURITY,
            securityContext = SahayakAISecurityContext(RiskLevel.NO_STRONG_INDICATORS, emptyList()),
            observedEvidence = emptyList(),
            untrustedContent = "test"
        )""")
        
    io.open(new_test_file, 'w', encoding='utf-8').write(c)
    os.remove(old_test_file)

# What about SecurityAnalysisCoordinatorTest.kt?
coord_test = 'app/src/test/java/com/sahayak/app/security/SecurityAnalysisCoordinatorTest.kt'
if os.path.exists(coord_test):
    c = io.open(coord_test, 'r', encoding='utf-8').read()
    c = c.replace('import com.sahayak.app.ai.NoOpLocalAIEngine', 'import com.sahayak.app.ai.NoOpSahayakAIEngine')
    c = c.replace('NoOpLocalAIEngine()', 'NoOpSahayakAIEngine()')
    io.open(coord_test, 'w', encoding='utf-8').write(c)
    
ocr_test = 'app/src/test/java/com/sahayak/app/input/OcrEngineTest.kt'
if os.path.exists(ocr_test):
    c = io.open(ocr_test, 'r', encoding='utf-8').read()
    c = c.replace('import com.sahayak.app.ai.NoOpLocalAIEngine', 'import com.sahayak.app.ai.NoOpSahayakAIEngine')
    c = c.replace('NoOpLocalAIEngine()', 'NoOpSahayakAIEngine()')
    io.open(ocr_test, 'w', encoding='utf-8').write(c)

