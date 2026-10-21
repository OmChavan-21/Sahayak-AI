import io
path = 'app/src/main/AndroidManifest.xml'
c = io.open(path, 'r', encoding='utf-8').read()

intent_filter = """            <intent-filter>
                <action android:name="android.intent.action.SEND" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="text/plain" />
            </intent-filter>
"""

if "android.intent.action.SEND" not in c:
    c = c.replace("</activity>", intent_filter + "        </activity>")

io.open(path, 'w', encoding='utf-8').write(c)
