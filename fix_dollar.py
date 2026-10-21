import io
path = 'app/src/main/java/com/sahayak/app/security/SecurityAnalysisCoordinator.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('\\${ocrResult.errorMessage}', '${ocrResult.errorMessage}')
io.open(path, 'w', encoding='utf-8').write(c)
