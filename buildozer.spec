[app]
title = Multi_Word_Master
package.name = multi.word.master
package.domain = org.toopen
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,csv,wav,mp3,ttf
version = 2.4.0

requirements = python3,kivy==2.3.0,pyjnius,requests,certifi,openssl
android.meta_data = app_name=5개국어 단어 마스터

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 31
orientation = portrait

[buildozer]
log_level = 2
