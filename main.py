import os
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from kivy.app import App
# ... 기타 필요한 import들

# 1. 한글 폰트 등록 (파일 이름이 font.ttf 라고 가정)
# 이 코드를 App 클래스 시작 전, 상단에 넣으세요.
LabelBase.register(name="Nanum", fn_regular="font.ttf")

class YourApp(App):
    def build(self):
        # 2. 기본 폰트를 'Nanum'으로 설정
        from kivy.core.window import Window
        from kivy.uix.label import Label
        
        # 모든 위젯에 기본 폰트 적용
        from kivy.config import Config
        Config.set('kivy', 'default_font', ['Nanum', 'font.ttf'])
        
        # 만약 특정 버튼이나 레이블만 안 나온다면 
        # Label(text="안녕", font_name="Nanum") 처럼 직접 지정도 가능합니다.
        return YourRootWidget()
