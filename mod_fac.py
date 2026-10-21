import io
path = 'app/src/main/java/com/sahayak/app/input/ImageInputFactory.kt'
c = io.open(path, 'r', encoding='utf-8').read()

replace = """    fun createFromImageReference(imageIdentifier: String, isScreenshot: Boolean): UserInput? {
        if (imageIdentifier.isBlank()) {
            return null
        }
        return UserInput(
            inputType = if (isScreenshot) InputType.SCREENSHOT else InputType.IMAGE,
            rawText = null, // Text will be populated by OCR later
            metadata = mapOf("image_reference" to imageIdentifier)
        )
    }"""
c = c.replace('    fun createFromImageReference(imageIdentifier: String, isScreenshot: Boolean): UserInput {', '    fun createFromImageReference(imageIdentifier: String, isScreenshot: Boolean): UserInput? {')
c = c.replace("""        return UserInput(
            inputType = if (isScreenshot) InputType.SCREENSHOT else InputType.IMAGE,
            rawText = null, // Text will be populated by OCR later
            metadata = mapOf("image_reference" to imageIdentifier)
        )""", """        if (imageIdentifier.isBlank()) return null
        return UserInput(
            inputType = if (isScreenshot) InputType.SCREENSHOT else InputType.IMAGE,
            rawText = null, // Text will be populated by OCR later
            metadata = mapOf("image_reference" to imageIdentifier)
        )""")
io.open(path, 'w', encoding='utf-8').write(c)

path = 'app/src/test/java/com/sahayak/app/input/OcrEngineTest.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('assertEquals(InputType.IMAGE, input.inputType)', 'assertEquals(InputType.IMAGE, input?.inputType)')
c = c.replace('assertEquals("content://media/1", input.metadata["image_reference"])', 'assertEquals("content://media/1", input?.metadata?.get("image_reference"))')
c = c.replace('assertEquals(null, input.rawText)', 'assertEquals(null, input?.rawText)')
c = c.replace('assertEquals(InputType.SCREENSHOT, input.inputType)', 'assertEquals(InputType.SCREENSHOT, input?.inputType)')
c = c.replace('assertEquals("content://media/2", input.metadata["image_reference"])', 'assertEquals("content://media/2", input?.metadata?.get("image_reference"))')

test = """
    @Test
    fun testInvalidBlankImageReferencesAreHandledSafely() {
        val factory = ImageInputFactory()
        val input = factory.createFromImageReference("   ", isScreenshot = false)
        val input2 = factory.createFromImageReference("", isScreenshot = true)
        
        assertEquals(null, input)
        assertEquals(null, input2)
    }
}"""
c = c.replace('}', test)
# Fix the end of file which had 2 }'s. 
# wait, c.replace('}', test) will replace ALL closing brackets. No!
