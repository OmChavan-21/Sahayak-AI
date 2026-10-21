package com.sahayak.app.ai

interface LocalAIModelRuntime {
    val currentState: ModelLifecycleState
    val configuration: ModelConfiguration?
    
    suspend fun loadModel(config: ModelConfiguration): Boolean
    suspend fun generate(prompt: PromptContext): RuntimeResponse
    suspend fun release()
    suspend fun cancel()
}
