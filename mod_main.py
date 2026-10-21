import io
path = 'app/src/main/java/com/sahayak/app/MainActivity.kt'
c = io.open(path, 'r', errors='ignore').read()

import_stat = """import com.sahayak.app.input.ShareIntentParser
import com.sahayak.app.ui.theme.SahayakTheme
import android.content.Intent
"""
c = c.replace('import com.sahayak.app.ui.theme.SahayakTheme', import_stat)

onCreate = """  override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    
    val parser = ShareIntentParser()
    val userInput = parser.parse(intent)
    val initialKey = if (userInput != null) {
        Analyze(sharedText = userInput.rawText)
    } else {
        Main
    }

    enableEdgeToEdge()
    setContent {
      SahayakTheme { Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) { MainNavigation(initialKey) } }
    }
  }

  override fun onNewIntent(intent: Intent) {
      super.onNewIntent(intent)
      setIntent(intent)
      // For a robust implementation, we would update the Compose state here, 
      // but restarting the activity or standard launchMode covers most sharing flows.
  }
"""

start_oncreate = c.find("  override fun onCreate")
end_oncreate = c.find("  }\n}", start_oncreate) + 4
c = c[:start_oncreate] + onCreate + c[end_oncreate:]

io.open(path, 'w', encoding='utf-8').write(c)
