package com.sahayak.app.ai

sealed class RuntimeResponse {
    data class Success(val rawText: String) : RuntimeResponse()
    data class Error(val message: String) : RuntimeResponse()
    object Cancelled : RuntimeResponse()
    object Unavailable : RuntimeResponse()
}
