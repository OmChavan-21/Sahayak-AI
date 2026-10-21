package com.sahayak.app.ai

sealed class SahayakAIResult {
    data class Success(val response: SahayakAIResponse) : SahayakAIResult()
    data class Error(val errorMessage: String) : SahayakAIResult()
    object Unavailable : SahayakAIResult()
}
