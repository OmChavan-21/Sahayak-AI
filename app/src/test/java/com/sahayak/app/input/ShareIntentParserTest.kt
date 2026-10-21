package com.sahayak.app.input

import android.content.Intent
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

class ShareIntentParserTest {

    private val parser = ShareIntentParser()

    @Test
    fun testValidActionSendTextPlainIntent() {
        val userInput = parser.parse(Intent.ACTION_SEND, "text/plain", "Hello Sahayak")
        assertEquals(InputType.SHARED_CONTENT, userInput?.inputType)
        assertEquals("Hello Sahayak", userInput?.rawText)
    }

    @Test
    fun testNullIntent() {
        assertNull(parser.parse(null))
    }

    @Test
    fun testNullExtraText() {
        assertNull(parser.parse(Intent.ACTION_SEND, "text/plain", null))
    }

    @Test
    fun testEmptyExtraText() {
        assertNull(parser.parse(Intent.ACTION_SEND, "text/plain", ""))
    }

    @Test
    fun testWhitespaceOnlyExtraText() {
        assertNull(parser.parse(Intent.ACTION_SEND, "text/plain", "   \n  "))
    }

    @Test
    fun testUnsupportedMimeType() {
        assertNull(parser.parse(Intent.ACTION_SEND, "image/png", "Hello Sahayak"))
    }

    @Test
    fun testUnsupportedAction() {
        assertNull(parser.parse(Intent.ACTION_VIEW, "text/plain", "Hello Sahayak"))
    }

    @Test
    fun testMalformedIntent() {
        assertNull(parser.parse(null, null, "Hello Sahayak"))
    }
}
