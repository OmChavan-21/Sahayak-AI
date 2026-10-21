import io

# Fix EvidenceExtractor.kt
f1 = 'app/src/main/java/com/sahayak/app/input/EvidenceExtractor.kt'
c1 = io.open(f1, 'r', encoding='utf-8').read()
c1 = c1.replace('(?\\s*\\d+', '(\u20b9\\s*\\d+')
io.open(f1, 'w', encoding='utf-8').write(c1)

# Fix TextEvidenceExtractorTest.kt
f2 = 'app/src/test/java/com/sahayak/app/input/TextEvidenceExtractorTest.kt'
c2 = io.open(f2, 'r', encoding='utf-8').read()
c2 = c2.replace('?49', '\u20b949')
c2 = c2.replace('?500', '\u20b9500')
io.open(f2, 'w', encoding='utf-8').write(c2)
