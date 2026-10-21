package com.sahayak.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.sahayak.app.input.ShareIntentParser
import com.sahayak.app.ui.theme.SahayakTheme
import android.content.Intent


class MainActivity : ComponentActivity() {
  override fun onCreate(savedInstanceState: Bundle?) {
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
}
