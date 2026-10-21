import io
path = 'app/src/test/java/com/sahayak/app/ai/SahayakAIContractTest.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('package com.sahayak.app.ai', 'package com.sahayak.app.ai\n\nimport com.sahayak.app.capabilities.SahayakCapability')
io.open(path, 'w', encoding='utf-8').write(c)
