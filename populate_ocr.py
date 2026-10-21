import io

files = {}

files['app/src/main/java/com/sahayak/app/input/OcrResult.kt'] = """package com.sahayak.app.input

sealed class OcrResult {
    data class Success(val recognizedText: String) : OcrResult()
    data class Error(val errorMessage: String) : OcrResult()
    object Unavailable : OcrResult()
}
"""

files['app/src/main/java/com/sahayak/app/input/OcrEngine.kt'] = """package com.sahayak.app.input

interface OcrEngine {
    /**
     * Attempts to extract text from a given UserInput representing an image/screenshot.
     * It does NOT perform any security analysis.
     */
    suspend fun extractText(input: UserInput): OcrResult
}
"""

files['app/src/main/java/com/sahayak/app/input/NoOpOcrEngine.kt'] = """package com.sahayak.app.input

class NoOpOcrEngine : OcrEngine {
    override suspend fun extractText(input: UserInput): OcrResult {
        // A temporary architectural placeholder.
        // It must NOT pretend that OCR occurred.
        return OcrResult.Unavailable
    }
}
"""

files['app/src/main/java/com/sahayak/app/input/ImageInputFactory.kt'] = """package com.sahayak.app.input

class ImageInputFactory {
    
    /**
     * Converts a generic image reference into a UserInput object.
     * We don't use real Android Bitmaps or Uris here yet to keep it pure and simple.
     */
    fun createFromImageReference(imageIdentifier: String, isScreenshot: Boolean): UserInput {
        return UserInput(
            inputType = if (isScreenshot) InputType.SCREENSHOT else InputType.IMAGE,
            rawText = null, // Text will be populated by OCR later
            metadata = mapOf("image_reference" to imageIdentifier)
        )
    }
}
"""

files['app/src/test/java/com/sahayak/app/input/OcrEngineTest.kt'] = """package com.sahayak.app.input

import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class OcrEngineTest {

    @Test
    fun testNoOpOcrEngineReturnsUnavailable() = runBlocking {
        val engine = NoOpOcrEngine()
        val input = UserInput(InputType.IMAGE)
        val result = engine.extractText(input)
        
        assertEquals(OcrResult.Unavailable, result)
    }

    @Test
    fun testSuccessfulOcrResultContainsText() {
        val result = OcrResult.Success("Recognized text")
        assertEquals("Recognized text", result.recognizedText)
    }

    @Test
    fun testOcrErrorIsRepresentedSafely() {
        val result = OcrResult.Error("Unable to read text from this image.")
        assertEquals("Unable to read text from this image.", result.errorMessage)
    }

    @Test
    fun testImageInputFactoryCreatesImageInput() {
        val factory = ImageInputFactory()
        val input = factory.createFromImageReference("content://media/1", isScreenshot = false)
        
        assertEquals(InputType.IMAGE, input.inputType)
        assertEquals("content://media/1", input.metadata["image_reference"])
        assertEquals(null, input.rawText)
    }

    @Test
    fun testImageInputFactoryCreatesScreenshotInput() {
        val factory = ImageInputFactory()
        val input = factory.createFromImageReference("content://media/2", isScreenshot = true)
        
        assertEquals(InputType.SCREENSHOT, input.inputType)
        assertEquals("content://media/2", input.metadata["image_reference"])
        assertEquals(null, input.rawText)
    }
    
    @Test
    fun testOcrFailureDoesNotBecomeSecurityVerdict() {
        // Conceptually, if OCR returns Unavailable, it should not automatically mark something safe or unsafe.
        // It just means we don't have text to analyze.
        val result: OcrResult = OcrResult.Unavailable
        assertTrue(result is OcrResult.Unavailable)
        // No security RiskLevel is associated with OcrResult.
    }
}
"""

for path, content in files.items():
    io.open(path, 'w', encoding='utf-8').write(content)
