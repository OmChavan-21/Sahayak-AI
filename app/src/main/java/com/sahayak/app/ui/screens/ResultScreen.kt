package com.sahayak.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sahayak.app.ai.NoOpSahayakAIEngine
import com.sahayak.app.security.RiskLevel
import com.sahayak.app.security.SecurityAnalysis
import com.sahayak.app.security.SecurityAnalysisCoordinator
import com.sahayak.app.input.UserInput
import com.sahayak.app.input.InputType
import com.sahayak.app.input.ImageInputFactory

import com.sahayak.app.security.SecurityAnalyzer
import com.sahayak.app.actions.ActionDecision
import com.sahayak.app.actions.ActionPolicyEngine
import com.sahayak.app.actions.ActionType


@Composable
fun ResultScreen(
    textToAnalyze: String?,
    imageUri: String? = null,
    onAnalyzeAgain: () -> Unit,
    onBack: () -> Unit,
    modifier: Modifier = Modifier
) {
    val coordinator = remember { SecurityAnalysisCoordinator(aiEngine = NoOpSahayakAIEngine()) }
    var resultState by remember { mutableStateOf<SecurityAnalysis?>(null) }

    LaunchedEffect(textToAnalyze, imageUri) {
        val userInput = if (imageUri != null) {
            ImageInputFactory().createFromImageReference(imageUri, isScreenshot = false)
            ?: UserInput(InputType.TEXT, rawText = "")
        } else {
            UserInput(InputType.TEXT, rawText = textToAnalyze)
        }
        resultState = coordinator.analyze(userInput)
    }

    val result = resultState

    if (result == null) {
        Box(modifier = modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            CircularProgressIndicator()
        }
        return
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp)
            .verticalScroll(rememberScrollState())
    ) {
        val title = when (result.riskLevel) {
            RiskLevel.HIGH_RISK -> "High-risk indicators found"
            RiskLevel.AMBIGUOUS -> "Something looks unusual"
            RiskLevel.NO_STRONG_INDICATORS -> "No strong warning indicators found"
            RiskLevel.UNABLE_TO_ANALYZE -> "Unable to analyze"
        }

        val titleColor = when (result.riskLevel) {
            RiskLevel.HIGH_RISK -> MaterialTheme.colorScheme.error
            RiskLevel.AMBIGUOUS -> Color(0xFFD97706) // Orange/Amber
            RiskLevel.NO_STRONG_INDICATORS -> MaterialTheme.colorScheme.primary
            RiskLevel.UNABLE_TO_ANALYZE -> MaterialTheme.colorScheme.onSurfaceVariant
        }

        Text(
            text = title,
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold,
            color = titleColor
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = result.explanation,
            style = MaterialTheme.typography.bodyLarge,
            fontWeight = if (result.riskLevel == RiskLevel.HIGH_RISK) FontWeight.Bold else FontWeight.Normal
        )

        if (result.riskLevel == RiskLevel.HIGH_RISK || result.indicators.isNotEmpty()) {
            Spacer(modifier = Modifier.height(16.dp))
            result.indicators.forEach { indicator ->
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 4.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                ) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text(
                            text = indicator.description,
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.SemiBold
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "\"${indicator.evidence}\"",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        if (result.riskLevel != RiskLevel.NO_STRONG_INDICATORS) {
            Text(
                text = "What you should do",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(8.dp))
        }

        Text(
            text = result.recommendation,
            style = MaterialTheme.typography.bodyLarge
        )

        Spacer(modifier = Modifier.height(24.dp))

        if (result.riskLevel == RiskLevel.HIGH_RISK) {
            Card(
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer),
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(
                    text = "Important:\nWe cannot confirm that this message is fraudulent.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onErrorContainer,
                    modifier = Modifier.padding(16.dp)
                )
            }
            Spacer(modifier = Modifier.height(24.dp))
        }

        
        // Safe Action Layer Demonstration
        val policyEngine = remember { ActionPolicyEngine() }
        val suggestedAction = if (result.riskLevel == RiskLevel.HIGH_RISK) ActionType.CREATE_DRAFT else ActionType.CREATE_REMINDER
        val decision = policyEngine.evaluate(suggestedAction)
        
        Text(
            text = "Suggested next steps",
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold
        )
        Spacer(modifier = Modifier.height(8.dp))
        
        val actionText = when (suggestedAction) {
            ActionType.CREATE_DRAFT -> "Create report draft"
            ActionType.CREATE_REMINDER -> "Create follow-up reminder"
            else -> "Action"
        }
        
        val safetyText = when (decision) {
            ActionDecision.ALLOWED -> "(Automatic)"
            ActionDecision.REQUIRES_CONFIRMATION -> "(Needs your confirmation)"
            ActionDecision.USER_MUST_EXECUTE -> "(You will review before sending)"
            ActionDecision.BLOCKED -> "(Blocked for safety)"
        }
        
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = "$actionText $safetyText",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSecondaryContainer
                )
            }
        }
        Spacer(modifier = Modifier.height(16.dp))
        Spacer(modifier = Modifier.weight(1f, fill = false))


        Button(
            onClick = { /* TODO: Save Incident */ },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            enabled = false
        ) {
            Text("Save Incident (TODO)", style = MaterialTheme.typography.titleMedium)
        }

        Spacer(modifier = Modifier.height(12.dp))

        OutlinedButton(
            onClick = onAnalyzeAgain,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp)
        ) {
            Text("Analyze Again", style = MaterialTheme.typography.titleMedium)
        }
    }
}
