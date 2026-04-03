[app]
# 앱 정보 설정
title = Foreign_Word_Master_2.0
package.name = wordmaster2
package.domain = org.toopen0
source.dir = .

# 포함할 파일 확장자 (ttf 폰트와 json 데이터 필수 포함)
source.include_exts = py,png,jpg,kv,atlas,json,csv,wav,mp3,ttf
version = 2.0.1

# 빌드에 필요한 라이브러리 (requirements.txt와 동일하게 설정)
requirements = python3,kivy==2.3.0,pyjnius,requests,certifi,openssl

# 화면 및 디자인 설정
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a
android.allow_backup = True

# 안드로이드 권한 (인터넷 및 파일 읽기/쓰기)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# 안드로이드 SDK 및 API 설정 (안정 버전)
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# 빌드 시 안드로이드 X 사용 및 메인 화면 유지
android.enable_androidx = True
android.skip_update = False

[buildozer]
# 빌드 로그 상세 출력
log_level = 2
warn_on_root = 1
