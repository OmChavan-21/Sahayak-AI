import io
path = 'app/src/main/java/com/sahayak/app/ui/screens/ResultScreen.kt'
c = io.open(path, 'r', encoding='utf-8').read()

import_statement = "import com.sahayak.app.actions.ActionDecision\nimport com.sahayak.app.actions.ActionPolicyEngine\nimport com.sahayak.app.actions.ActionType\n"
if "com.sahayak.app.actions" not in c:
    c = c.replace("import com.sahayak.app.security.SecurityAnalyzer", "import com.sahayak.app.security.SecurityAnalyzer\n" + import_statement)

# Add the UI snippet
# After "Spacer(modifier = Modifier.weight(1f, fill = false))"
ui_snippet = """
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
"""

if "Suggested next steps" not in c:
    c = c.replace("Spacer(modifier = Modifier.weight(1f, fill = false))", ui_snippet)

io.open(path, 'w', encoding='utf-8').write(c)
