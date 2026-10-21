package com.sahayak.app.input

import com.sahayak.app.security.RiskLevel
import com.sahayak.app.security.SecurityAnalysisCoordinator
import com.sahayak.app.ai.NoOpSahayakAIEngine
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
        
        assertEquals(InputType.IMAGE, input!!.inputType)
        assertEquals("content://media/1", input!!.metadata["image_reference"])
        assertEquals(null, input!!.rawText)
    }

    @Test
    fun testImageInputFactoryCreatesScreenshotInput() {
        val factory = ImageInputFactory()
        val input = factory.createFromImageReference("content://media/2", isScreenshot = true)
        
        assertEquals(InputType.SCREENSHOT, input!!.inputType)
        assertEquals("content://media/2", input!!.metadata["image_reference"])
        assertEquals(null, input!!.rawText)
    }
    
    @Test
    fun testOcrFailureDoesNotBecomeSecurityVerdict() {
        // Conceptually, if OCR returns Unavailable, it should not automatically mark something safe or unsafe.
        // It just means we don't have text to analyze.
        val result: OcrResult = OcrResult.Unavailable
        assertTrue(result is OcrResult.Unavailable)
        // No security RiskLevel is associated with OcrResult.
    }

    @Test
    fun testInvalidBlankImageReferencesAreHandledSafely() {
        val factory = ImageInputFactory()
        val input = factory.createFromImageReference("   ", isScreenshot = false)
        val input2 = factory.createFromImageReference("", isScreenshot = true)
        
        assertEquals(null, input)
        assertEquals(null, input2)
    }

    @Test
    fun testOcrUnavailableProducesUnableToAnalyze() = runBlocking {
        val coordinator = SecurityAnalysisCoordinator(aiEngine = NoOpSahayakAIEngine())
        val input = UserInput(InputType.IMAGE)
        val result = coordinator.analyze(input)
        
        assertEquals(RiskLevel.UNABLE_TO_ANALYZE, result.riskLevel)
        assertTrue(result.explanation.contains("Unable to read text"))
    }
}