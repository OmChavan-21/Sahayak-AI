package com.sahayak.app

import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.safeDrawingPadding
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation3.runtime.entryProvider
import androidx.navigation3.runtime.rememberNavBackStack
import androidx.navigation3.ui.NavDisplay
import com.sahayak.app.ui.screens.MainScreen
import com.sahayak.app.ui.screens.AnalyzeScreen
import com.sahayak.app.ui.screens.ResultScreen

@Composable
fun MainNavigation(initialKey: androidx.navigation3.runtime.NavKey = Main) {
  val backStack = rememberNavBackStack(initialKey)

  NavDisplay(
    backStack = backStack,
    onBack = { backStack.removeLastOrNull() },
    entryProvider =
      entryProvider {
        entry<Main> {
          MainScreen(onItemClick = { navKey -> backStack.add(navKey) }, modifier = Modifier.safeDrawingPadding().padding(16.dp))
        }
        entry<Analyze> { analyzeKey ->
          AnalyzeScreen(
              initialText = analyzeKey.sharedText,
              onAnalyze = { text -> backStack.add(Result(textToAnalyze = text)) },
              onAnalyzeImage = { uri -> backStack.add(Result(imageUri = uri)) },
              onBack = { backStack.removeLastOrNull() },
              modifier = Modifier.safeDrawingPadding().padding(16.dp)
          )
        }
        entry<Result> { resultKey ->
          ResultScreen(
              textToAnalyze = resultKey.textToAnalyze,
              imageUri = resultKey.imageUri,
              onAnalyzeAgain = { 
                  backStack.removeLastOrNull() 
              },
              onBack = { backStack.removeLastOrNull() },
              modifier = Modifier.safeDrawingPadding().padding(16.dp)
          )
        }
      },
  )
}
