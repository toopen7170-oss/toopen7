import os
import sys
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path

# [중요] 안드로이드 앱 내부 경로 인식 설정
try:
    if getattr(sys, 'frozen', False):
        # 빌드된 환경일 경우
        base_path = os.path.dirname(sys.executable)
    else:
        # 일반 실행 환경일 경우
        base_path = os.path.dirname(__file__)
    
    resource_add_path(base_path)
    
    # 폰트 등록 (오류 방지를 위해 파일 존재 확인 추가)
    font_file = "font.ttf"
    if os.path.exists(font_file):
        LabelBase.register(name="Nanum", fn_regular=font_file)
    else:
        print(f"Font file not found: {font_file}")
except Exception as e:
    print(f"Font setup error: {e}")

class WordGameApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # 폰트가 없을 경우를 대비해 기본 폰트 설정
        f_name = "Nanum" if os.path.exists("font.ttf") else None
        
        main_label = Label(
            text="단어 맞히기 게임 2.0", 
            font_size='30sp', 
            font_name=f_name,
            size_hint_y=0.2
        )
        layout.add_widget(main_label)
        
        word_display = Label(
            text="teacher", 
            font_size='50sp', 
            bold=True,
            size_hint_y=0.3
        )
        layout.add_widget(word_display)
        
        grid = GridLayout(cols=2, spacing=10, size_hint_y=0.4)
        answers = ["선생님", "학생", "학교", "교실"]
        
        for ans in answers:
            btn = Button(
                text=ans, 
                font_name=f_name, 
                font_size='20sp',
                background_color=(0.1, 0.3, 0.5, 1)
            )
            grid.add_widget(btn)
            
        layout.add_widget(grid)
        
        return layout

if __name__ == "__main__":
    WordGameApp().run()
