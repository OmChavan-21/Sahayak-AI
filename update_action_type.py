import io
import os

path = 'app/src/main/java/com/sahayak/app/actions/ActionType.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('CHANGE_ACCOUNT_INFORMATION,', 'CHANGE_ACCOUNT_INFORMATION,\n    INSPECT_URL,')
io.open(path, 'w', encoding='utf-8').write(c)

path = 'app/src/main/java/com/sahayak/app/actions/ActionPolicy.kt'
c = io.open(path, 'r', encoding='utf-8').read()
c = c.replace('ActionType.UNKNOWN -> ActionRisk.BLOCKED', 'ActionType.INSPECT_URL -> ActionRisk.REQUIRES_CONFIRMATION\n            ActionType.UNKNOWN -> ActionRisk.BLOCKED')
io.open(path, 'w', encoding='utf-8').write(c)
