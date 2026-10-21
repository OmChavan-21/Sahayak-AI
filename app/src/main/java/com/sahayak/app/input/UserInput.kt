package com.sahayak.app.input

data class UserInput(
    val inputType: InputType,
    val rawText: String? = null,
    val metadata: Map<String, String> = emptyMap(),
    val extractedEvidence: List<Evidence> = emptyList()
)
