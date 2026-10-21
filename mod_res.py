import io
path = 'app/src/main/java/com/sahayak/app/ui/screens/ResultScreen.kt'
c = io.open(path, 'r', encoding='utf-8').read()

imports = """import com.sahayak.app.input.UserInput
import com.sahayak.app.input.InputType
import com.sahayak.app.input.ImageInputFactory
"""

c = c.replace('import com.sahayak.app.security.SecurityAnalysisCoordinator', 'import com.sahayak.app.security.SecurityAnalysisCoordinator\n' + imports)

replace_sig = """fun ResultScreen(
    textToAnalyze: String?,
    imageUri: String? = null,
    onAnalyzeAgain: () -> Unit,
    onBack: () -> Unit,
    modifier: Modifier = Modifier
) {
    val coordinator = remember { SecurityAnalysisCoordinator(aiEngine = NoOpLocalAIEngine()) }
    var resultState by remember { mutableStateOf<SecurityAnalysis?>(null) }

    LaunchedEffect(textToAnalyze, imageUri) {
        val userInput = if (imageUri != null) {
            ImageInputFactory().createFromImageReference(imageUri, isScreenshot = false)
        } else {
            UserInput(InputType.TEXT, rawText = textToAnalyze)
        }
        resultState = coordinator.analyze(userInput)
    }"""

# Find the signature
start_idx = c.find('fun ResultScreen(')
end_idx = c.find('    }', c.find('LaunchedEffect')) + 5
c = c[:start_idx] + replace_sig + c[end_idx:]

io.open(path, 'w', encoding='utf-8').write(c)
