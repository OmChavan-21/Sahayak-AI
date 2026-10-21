import io
import os

path = 'app/src/main/java/com/sahayak/app/input/ShareIntentParser.kt'

c = """package com.sahayak.app.input

import android.content.Intent

class ShareIntentParser {
    fun parse(intent: Intent?): UserInput? {
        if (intent == null) return null
        if (intent.action != Intent.ACTION_SEND) return null
        if (intent.type != "text/plain") return null

        val sharedText = intent.getStringExtra(Intent.EXTRA_TEXT)
        if (sharedText.isNullOrBlank()) return null

        return UserInput(
            inputType = InputType.SHARED_CONTENT,
            rawText = sharedText
        )
    }
}
"""

io.open(path, 'w', encoding='utf-8').write(c)

test_path = 'app/src/test/java/com/sahayak/app/input/ShareIntentParserTest.kt'
c_test = """package com.sahayak.app.input

import android.content.Intent
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner

@RunWith(RobolectricTestRunner::class)
class ShareIntentParserTest {

    private val parser = ShareIntentParser()

    @Test
    fun testValidActionSendTextPlainIntent() {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, "Hello Sahayak")
        }
        val userInput = parser.parse(intent)
        assertEquals(InputType.SHARED_CONTENT, userInput?.inputType)
        assertEquals("Hello Sahayak", userInput?.rawText)
    }

    @Test
    fun testNullIntent() {
        assertNull(parser.parse(null))
    }

    @Test
    fun testNullExtraText() {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            // No EXTRA_TEXT put
        }
        assertNull(parser.parse(intent))
    }

    @Test
    fun testEmptyExtraText() {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, "")
        }
        assertNull(parser.parse(intent))
    }

    @Test
    fun testWhitespaceOnlyExtraText() {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, "   \n  ")
        }
        assertNull(parser.parse(intent))
    }

    @Test
    fun testUnsupportedMimeType() {
        val intent = Intent(Intent.ACTION_SEND).apply {
            type = "image/png"
            putExtra(Intent.EXTRA_TEXT, "Hello Sahayak")
        }
        assertNull(parser.parse(intent))
    }

    @Test
    fun testUnsupportedAction() {
        val intent = Intent(Intent.ACTION_VIEW).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_TEXT, "Hello Sahayak")
        }
        assertNull(parser.parse(intent))
    }

    @Test
    fun testMalformedIntent() {
        val intent = Intent().apply {
            putExtra(Intent.EXTRA_TEXT, "Hello Sahayak")
        }
        assertNull(parser.parse(intent))
    }
}
"""

io.open(test_path, 'w', encoding='utf-8').write(c_test)
