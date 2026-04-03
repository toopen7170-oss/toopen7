[app]
title = toopen0_Game
package.name = wordgame
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,csv,wav,mp3

# 버전을 반드시 입력해야 에러가 나지 않습니다.
version = 0.1

requirements = python3,kivy,requests,android
orientation = portrait
fullscreen = 1
android.arch = arm64-v8a
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
