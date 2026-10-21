package com.sahayak.app.input

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class TextEvidenceExtractorTest {

    private val extractor = TextEvidenceExtractor()

    @Test
    fun testUserInputCreation() {
        val input = UserInput(
            inputType = InputType.TEXT,
            rawText = "Hello"
        )
        assertEquals(InputType.TEXT, input.inputType)
        assertEquals("Hello", input.rawText)
    }

    @Test
    fun testEvidenceCreation() {
        val evidence = Evidence(
            type = EvidenceType.AMOUNT,
            value = "₹500",
            sourceSnippet = "₹500"
        )
        assertEquals(EvidenceType.AMOUNT, evidence.type)
        assertEquals("₹500", evidence.sourceSnippet)
    }

    @Test
    fun testUrlExtraction() {
        val input = UserInput(InputType.TEXT, "Check this link: https://example.com/login")
        val evidence = extractor.extract(input)
        
        val urls = evidence.filter { it.type == EvidenceType.URL }
        assertEquals(1, urls.size)
        assertEquals("https://example.com/login", urls[0].value)
        assertEquals("https://example.com/login", urls[0].sourceSnippet)
    }

    @Test
    fun testAmountExtraction() {
        val input = UserInput(InputType.TEXT, "You owe me ₹49 or Rs 100 or $50 or 500 INR.")
        val evidence = extractor.extract(input)
        
        val amounts = evidence.filter { it.type == EvidenceType.AMOUNT }.map { it.value }
        assertTrue(amounts.contains("₹49"))
        assertTrue(amounts.contains("Rs 100"))
        assertTrue(amounts.contains("$50"))
        assertTrue(amounts.contains("500 INR"))
    }

    @Test
    fun testPhoneNumberExtraction() {
        val input = UserInput(InputType.TEXT, "Call me at +91 9876543210 or 1234567890")
        val evidence = extractor.extract(input)
        
        val phones = evidence.filter { it.type == EvidenceType.PHONE_NUMBER }.map { it.value }
        assertTrue(phones.contains("+91 9876543210"))
        assertTrue(phones.contains("1234567890"))
    }

    @Test
    fun testEmptyOrMalformedTextDoesNotCrash() {
        val inputEmpty = UserInput(InputType.TEXT, "")
        val resultEmpty = extractor.extract(inputEmpty)
        assertTrue(resultEmpty.isEmpty())

        val inputNull = UserInput(InputType.TEXT, null)
        val resultNull = extractor.extract(inputNull)
        assertTrue(resultNull.isEmpty())
    }
}
