title = toopen0_Game
package.name = wordgame
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,csv,wav,mp3
requirements = python3,kivy,requests,android

# (안드로이드 전체화면 및 방향 설정)
orientation = portrait
fullscreen = 1
android.arch = arm64-v8a

# (권한 설정: 오디오 및 저장소)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, RECORD_AUDIO
