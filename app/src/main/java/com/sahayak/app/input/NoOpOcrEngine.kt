package com.sahayak.app.input

class NoOpOcrEngine : OcrEngine {
    override suspend fun extractText(input: UserInput): OcrResult {
        // A temporary architectural placeholder.
        // It must NOT pretend that OCR occurred.
        return OcrResult.Unavailable
    }
}
