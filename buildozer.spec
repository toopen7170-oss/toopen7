[app]

# (section) Title of your application
title = Multi Word Master

# (section) Package name
package.name = multiwordmaster

# (section) Package domain (needed for android packaging)
package.domain = org.test

# (section) Source code where the main.py live
source.dir = .

# (section) Source files to include (let empty to include all the files)
# [중요] font.ttf와 words.json이 반드시 포함되어야 합니다.
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# (section) Application version
version = 1.0.1

# (section) Application requirements
# [중요] 외국어 처리 및 발음 기능을 위해 android가 포함되어야 합니다.
requirements = python3,kivy==2.3.0,kivymd,pillow,android

# (section) Supported orientations
orientation = portrait

# (section) Android specific
# [중요] TTS 발음 기능을 위해 WAKE_LOCK 권한이 필요합니다.
android.permissions = INTERNET, WAKE_LOCK

# (section) Android API (21 is for Android 5.0)
android.api = 33
android.minapi = 21
android.ndk = 25b

# (section) Android SDK directory (if empty, it will be installed automatically)
# android.sdk = 

# (section) Android architecture to build for
android.archs = arm64-v8a, armeabi-v7a

# (section) Allow backup
android.allow_backup = True

# (section) Screen usage
android.skip_update = False
android.keep_screen_on = True

# (section) Presplash and Icon
# android.presplash_color = #FFFFFF
# android.icon.filename = %(source.dir)s/icon.png

[buildozer]
# (section) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (section) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
