package com.sahayak.app.input

interface OcrEngine {
    /**
     * Attempts to extract text from a given UserInput representing an image/screenshot.
     * It does NOT perform any security analysis.
     */
    suspend fun extractText(input: UserInput): OcrResult
}
