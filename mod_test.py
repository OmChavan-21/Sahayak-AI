import io

path = 'app/src/test/java/com/sahayak/app/input/OcrEngineTest.kt'
c = io.open(path, 'r', encoding='utf-8').read()
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
c = c[:c.rfind('}')] + test
io.open(path, 'w', encoding='utf-8').write(c)

path = 'app/src/main/java/com/sahayak/app/ui/screens/ResultScreen.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('ImageInputFactory().createFromImageReference(imageUri, isScreenshot = false)', 'ImageInputFactory().createFromImageReference(imageUri, isScreenshot = false)\n            ?: UserInput(InputType.TEXT, rawText = "")')
io.open(path, 'w', encoding='utf-8').write(c)
