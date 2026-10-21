import io

path = 'app/src/main/java/com/sahayak/app/input/ShareIntentParser.kt'
c = """package com.sahayak.app.input

import android.content.Intent

class ShareIntentParser {
    fun parse(intent: Intent?): UserInput? {
        if (intent == null) return null
        return parse(intent.action, intent.type, intent.getStringExtra(Intent.EXTRA_TEXT))
    }

    fun parse(action: String?, type: String?, extraText: String?): UserInput? {
        if (action != Intent.ACTION_SEND) return null
        if (type != "text/plain") return null
        if (extraText.isNullOrBlank()) return null

        return UserInput(
            inputType = InputType.SHARED_CONTENT,
            rawText = extraText
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
"""
io.open(test_path, 'w', encoding='utf-8').write(c_test)
