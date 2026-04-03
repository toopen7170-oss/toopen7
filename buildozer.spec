[app]
title = toopen0_Game
package.name = wordgame
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,csv,wav,mp3
version = 0.1

# 빌드 안정성을 위해 라이브러리 목록 최적화
requirements = python3,kivy==2.3.0,requests,android,certifi

orientation = portrait
fullscreen = 1
android.arch = arm64-v8a

# 빌드 오류 방지를 위한 API 및 NDK 설정
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
