package com.sahayak.app.input

class ImageInputFactory {
    
    /**
     * Converts a generic image reference into a UserInput object.
     * We don't use real Android Bitmaps or Uris here yet to keep it pure and simple.
     */
    fun createFromImageReference(imageIdentifier: String, isScreenshot: Boolean): UserInput? {
        if (imageIdentifier.isBlank()) return null
        return UserInput(
            inputType = if (isScreenshot) InputType.SCREENSHOT else InputType.IMAGE,
            rawText = null, // Text will be populated by OCR later
            metadata = mapOf("image_reference" to imageIdentifier)
        )
    }
}
