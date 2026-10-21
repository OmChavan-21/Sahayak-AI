import io
path = 'app/src/main/java/com/sahayak/app/ui/screens/MainScreen.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('onItemClick(Analyze)', 'onItemClick(Analyze())')
io.open(path, 'w', encoding='utf-8').write(c)
