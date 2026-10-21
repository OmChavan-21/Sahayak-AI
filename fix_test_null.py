import io
path = 'app/src/test/java/com/sahayak/app/input/OcrEngineTest.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('assertEquals(InputType.IMAGE, input?.inputType)', 'assertEquals(InputType.IMAGE, input!!.inputType)')
c = c.replace('assertEquals("content://media/1", input?.metadata?.get("image_reference"))', 'assertEquals("content://media/1", input!!.metadata["image_reference"])')
c = c.replace('assertEquals(null, input?.rawText)', 'assertEquals(null, input!!.rawText)')
c = c.replace('assertEquals(InputType.SCREENSHOT, input?.inputType)', 'assertEquals(InputType.SCREENSHOT, input!!.inputType)')
c = c.replace('assertEquals("content://media/2", input?.metadata?.get("image_reference"))', 'assertEquals("content://media/2", input!!.metadata["image_reference"])')

c = c.replace('assertEquals(InputType.IMAGE, input.inputType)', 'assertEquals(InputType.IMAGE, input!!.inputType)')
c = c.replace('assertEquals("content://media/1", input.metadata["image_reference"])', 'assertEquals("content://media/1", input!!.metadata["image_reference"])')
c = c.replace('assertEquals(null, input.rawText)', 'assertEquals(null, input!!.rawText)')
c = c.replace('assertEquals(InputType.SCREENSHOT, input.inputType)', 'assertEquals(InputType.SCREENSHOT, input!!.inputType)')
c = c.replace('assertEquals("content://media/2", input.metadata["image_reference"])', 'assertEquals("content://media/2", input!!.metadata["image_reference"])')
io.open(path, 'w', encoding='utf-8').write(c)
