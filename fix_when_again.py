import io
path = 'app/src/main/java/com/sahayak/app/security/SecurityAnalyzer.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace(
    'RiskLevel.NO_STRONG_INDICATORS -> "We did not find strong warning indicators in the text provided. This does not guarantee that the message is legitimate."\n        }',
    'RiskLevel.NO_STRONG_INDICATORS -> "We did not find strong warning indicators in the text provided. This does not guarantee that the message is legitimate."\n            RiskLevel.UNABLE_TO_ANALYZE -> "Unable to read text from this image."\n        }'
)
c = c.replace(
    'RiskLevel.NO_STRONG_INDICATORS -> "Always remain cautious with unexpected messages."\n        }',
    'RiskLevel.NO_STRONG_INDICATORS -> "Always remain cautious with unexpected messages."\n            RiskLevel.UNABLE_TO_ANALYZE -> "Try a clearer image or provide the text another way."\n        }'
)
io.open(path, 'w', encoding='utf-8').write(c)

path = 'app/src/main/java/com/sahayak/app/ui/screens/ResultScreen.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace(
    'RiskLevel.NO_STRONG_INDICATORS -> "No strong warning indicators found"\n        }',
    'RiskLevel.NO_STRONG_INDICATORS -> "No strong warning indicators found"\n            RiskLevel.UNABLE_TO_ANALYZE -> "Unable to analyze"\n        }'
)
io.open(path, 'w', encoding='utf-8').write(c)
