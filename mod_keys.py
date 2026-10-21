import io
path = 'app/src/main/java/com/sahayak/app/NavigationKeys.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('@Serializable data class Result(val textToAnalyze: String) : NavKey', '@Serializable data class Result(val textToAnalyze: String? = null, val imageUri: String? = null) : NavKey')
io.open(path, 'w', encoding='utf-8').write(c)
