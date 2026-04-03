[app]
title = toopen0_Game
package.name = wordgame
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,csv,wav,mp3
version = 0.1.1

# 최신 규격에 맞게 archs로 수정
requirements = python3,kivy==2.3.0,requests,android,certifi
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a

# 안정적인 빌드 설정
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
