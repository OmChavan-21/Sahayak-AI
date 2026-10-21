import io
path = 'app/src/main/java/com/sahayak/app/security/SecurityAnalysisCoordinator.kt'
c = io.open(path, 'r', encoding='utf-8').read()
idx = c.find('    suspend fun analyzeTextOld(text: String): SecurityAnalysis {')
if idx != -1:
    c = c[:idx] + "}\n"
io.open(path, 'w', encoding='utf-8').write(c)
