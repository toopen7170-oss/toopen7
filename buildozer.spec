[app]
# 내부 관리용 이름 (영문 권장)
title = WordMaster_V2
package.name = wordmaster2
package.domain = org.toopen
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,csv,wav,mp3,ttf
version = 2.0.3

requirements = python3,kivy==2.3.0,pyjnius,requests,certifi,openssl

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a

# [핵심] 핸드폰 화면에 표시될 한글 이름 설정
# 이 설정을 넣으면 앱 아이콘 아래에 '외국어 단어 마스터'라고 표시됩니다.
android.meta_data = app_name=외국어 단어 마스터

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

[buildozer]
log_level = 2
warn_on_root = 1
