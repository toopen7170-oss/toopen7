[app]
title = toopen0_Game
package.name = wordgame
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,csv,wav,mp3
version = 0.1.2

# 쉼표 뒤에 공백이 없도록 주의하세요.
requirements = python3,kivy==2.3.0,requests,certifi,openssl

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a

# API 레벨 및 NDK 설정 유지
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
