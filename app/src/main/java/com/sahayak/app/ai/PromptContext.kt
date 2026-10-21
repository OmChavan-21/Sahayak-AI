package com.sahayak.app.ai

/**
 * Creates a clear architectural boundary between trusted application instructions
 * and untrusted user data to mitigate prompt injection.
 */
data class PromptContext(
    val systemInstructions: String,
    val securityContext: String,
    val observedEvidence: String,
    val untrustedUserContent: String
)
