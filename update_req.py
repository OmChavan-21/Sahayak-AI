import io
path = 'app/src/main/java/com/sahayak/app/capabilities/CapabilityRequest.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('val originatingRecommendationId: String? = null,', 'val originatingRecommendationId: String? = null,\n    val requiresUserConfirmation: Boolean = true,')
io.open(path, 'w', encoding='utf-8').write(c)
