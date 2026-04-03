[app]
# 앱 이름 및 패키지 설정
title = toopen0_Game
package.name = wordgame
package.domain = org.test

# 소스 코드 위치 및 포함할 파일 확장자 (ttf 폰트 꼭 포함!)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,csv,wav,mp3,ttf
version = 0.1.6

# [중요] 필요한 라이브러리 목록 (pyjnius는 소리 재생에 필수입니다)
requirements = python3,kivy==2.3.0,requests,certifi,openssl,pyjnius

# 화면 방향 (세로 고정)
orientation = portrait
fullscreen = 1

# 안드로이드 아키텍처 설정
android.archs = arm64-v8a

# 안드로이드 API 및 SDK 설정 (가장 안정적인 버전)
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# [중요] 앱 권한 설정 (인터넷 및 저장소)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# 빌드 시 안드로이드 X 사용 설정
android.enable_androidx = True

[buildozer]
# 빌드 로그 상세 출력 (오류 확인용)
log_level = 2
warn_on_root = 1
