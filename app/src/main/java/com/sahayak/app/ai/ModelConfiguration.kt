package com.sahayak.app.ai

data class ModelConfiguration(
    val identifier: String,
    val contextLength: Int,
    val maxInputLength: Int,
    val isLocal: Boolean = true,
    val runtimeIdentifier: String
)
