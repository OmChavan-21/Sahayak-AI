import io
path = 'app/src/main/java/com/sahayak/app/ui/screens/AnalyzeScreen.kt'
c = io.open(path, 'r', errors='ignore').read()

c = c.replace('fun AnalyzeScreen(\n    onAnalyze: (String) -> Unit,', 'fun AnalyzeScreen(\n    initialText: String? = null,\n    onAnalyze: (String) -> Unit,')
c = c.replace('var textInput by rememberSaveable { mutableStateOf("") }', 'var textInput by rememberSaveable { mutableStateOf(initialText ?: "") }')

snippet = """
        Spacer(modifier = Modifier.height(24.dp))

        if (initialText != null) {
            Text(
                text = "Imported from another app",
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(8.dp))
        }

        OutlinedTextField(
"""

c = c.replace("""
        Spacer(modifier = Modifier.height(24.dp))

        OutlinedTextField(""", snippet)

io.open(path, 'w', encoding='utf-8').write(c)
