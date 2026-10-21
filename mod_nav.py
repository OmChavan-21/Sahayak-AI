import io
path = 'app/src/main/java/com/sahayak/app/Navigation.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('onAnalyze = { text -> backStack.add(Result(text)) }', 'onAnalyze = { text -> backStack.add(Result(textToAnalyze = text)) },\n              onAnalyzeImage = { uri -> backStack.add(Result(imageUri = uri)) }')
c = c.replace('ResultScreen(\n              textToAnalyze = resultKey.textToAnalyze,\n              onAnalyzeAgain', 'ResultScreen(\n              textToAnalyze = resultKey.textToAnalyze,\n              imageUri = resultKey.imageUri,\n              onAnalyzeAgain')
io.open(path, 'w', encoding='utf-8').write(c)
