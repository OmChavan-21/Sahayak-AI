package com.sahayak.app.input

sealed class OcrResult {
    data class Success(val recognizedText: String) : OcrResult()
    data class Error(val errorMessage: String) : OcrResult()
    object Unavailable : OcrResult()
}
