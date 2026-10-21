package com.sahayak.app.input

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
