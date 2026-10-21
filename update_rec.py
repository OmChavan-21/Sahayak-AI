import io
import os

path = 'app/src/main/java/com/sahayak/app/ai/SahayakAIRecommendation.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('import com.sahayak.app.ai.SahayakAICapability', 'import com.sahayak.app.capabilities.SahayakCapability')
c = c.replace('val requestedCapability: SahayakAICapability? = null', 'val requestedCapability: SahayakCapability? = null')
io.open(path, 'w', encoding='utf-8').write(c)

os.remove('app/src/main/java/com/sahayak/app/ai/SahayakAICapability.kt')

# Update test that used SahayakAICapability
path = 'app/src/test/java/com/sahayak/app/ai/SahayakAIContractTest.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('import com.sahayak.app.ai.SahayakAICapability', 'import com.sahayak.app.capabilities.SahayakCapability')
c = c.replace('SahayakAICapability.INSPECT_URL', 'SahayakCapability.INSPECT_URL')
c = c.replace('SahayakAICapability.CREATE_DRAFT', 'SahayakCapability.CREATE_DRAFT')
io.open(path, 'w', encoding='utf-8').write(c)
