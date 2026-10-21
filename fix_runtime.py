import io
path = 'app/src/main/java/com/sahayak/app/ai/RuntimeBackedLocalAIEngine.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('\\${request.deterministicRiskLevel}', '${request.deterministicRiskLevel}')
io.open(path, 'w', encoding='utf-8').write(c)
