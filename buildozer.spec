[app]
title = Multi Word Master
package.name = multiwordmaster
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 1.0.2

# 핵심: pyjnius 추가 (안드로이드 시스템 기능 사용)
requirements = python3,kivy==2.3.0,android,pyjnius

orientation = portrait
android.permissions = INTERNET, WAKE_LOCK
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.keep_screen_on = True

[buildozer]
log_level = 2
warn_on_root = 1
