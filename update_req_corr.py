import io
import os

path = 'app/src/main/java/com/sahayak/app/capabilities/CapabilityRequest.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('val trustLevel: TrustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED', 'val trustLevel: TrustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED,\n    val correlationId: String')
io.open(path, 'w', encoding='utf-8').write(c)

path = 'app/src/test/java/com/sahayak/app/capabilities/CapabilitySystemTest.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('trustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED', 'trustLevel = TrustLevel.LEVEL_3_SAHAYAK_GENERATED,\n            correlationId = "test-123"')
c = c.replace('trustLevel = TrustLevel.LEVEL_0_UNTRUSTED_EXTERNAL', 'trustLevel = TrustLevel.LEVEL_0_UNTRUSTED_EXTERNAL,\n            correlationId = "test-123"')
io.open(path, 'w', encoding='utf-8').write(c)
