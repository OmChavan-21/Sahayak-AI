package com.sahayak.app.ai

import com.sahayak.app.input.Evidence

data class SahayakAIRequest(
    val task: SahayakAITask,
    val securityContext: SahayakAISecurityContext,
    val observedEvidence: List<Evidence>,
    val untrustedContent: String
)
