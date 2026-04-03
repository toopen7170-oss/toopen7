[app]
title = toopen0_Game
package.name = wordgame
package.domain = org.test
source.dir = .

# ttf 확장자를 추가하여 폰트 파일이 앱에 포함되게 합니다.
source.include_exts = py,png,jpg,kv,atlas,json,csv,wav,mp3,ttf

version = 0.1.4

requirements = python3,kivy==2.3.0,requests,certifi,openssl

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a

# 안정적인 빌드 설정
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
