import io
path = 'app/src/main/java/com/sahayak/app/security/SecurityAnalyzer.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace(
    'RiskLevel.NO_STRONG_INDICATORS -> "No strong risk indicators were found, but always verify unexpected requests."\n        }',
    'RiskLevel.NO_STRONG_INDICATORS -> "No strong risk indicators were found, but always verify unexpected requests."\n            RiskLevel.UNABLE_TO_ANALYZE -> "Unable to read text from this image."\n        }'
)
c = c.replace(
    'RiskLevel.NO_STRONG_INDICATORS -> "Safe to read, but remain vigilant with links or attachments."\n        }',
    'RiskLevel.NO_STRONG_INDICATORS -> "Safe to read, but remain vigilant with links or attachments."\n            RiskLevel.UNABLE_TO_ANALYZE -> "Try a clearer image or provide the text another way."\n        }'
)
io.open(path, 'w', encoding='utf-8').write(c)

path = 'app/src/main/java/com/sahayak/app/ui/screens/ResultScreen.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace(
    'RiskLevel.NO_STRONG_INDICATORS -> MaterialTheme.colorScheme.primary\n        }',
    'RiskLevel.NO_STRONG_INDICATORS -> MaterialTheme.colorScheme.primary\n            RiskLevel.UNABLE_TO_ANALYZE -> MaterialTheme.colorScheme.onSurfaceVariant\n        }'
)
c = c.replace(
    'RiskLevel.NO_STRONG_INDICATORS -> "?"\n        }',
    'RiskLevel.NO_STRONG_INDICATORS -> "?"\n            RiskLevel.UNABLE_TO_ANALYZE -> "???"\n        }'
)
io.open(path, 'w', encoding='utf-8').write(c)
