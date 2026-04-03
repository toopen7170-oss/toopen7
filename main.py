import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
from kivy.core.window import Window

# [중요] 한글 폰트 등록 (font.ttf 파일이 프로젝트 폴더에 있어야 함)
# 만약 다운로드한 폰트 이름이 다르면 아래 'font.ttf' 부분을 파일 이름과 똑같이 수정하세요.
try:
    LabelBase.register(name="Nanum", fn_regular="font.ttf")
except Exception as e:
    print(f"Font registration failed: {e}")

class WordGameApp(App):
    def build(self):
        # 전체 앱의 기본 폰트를 등록한 폰트로 고정
        self.title = "한글 단어 게임"
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # 폰트 적용 예시 (font_name="Nanum" 추가)
        main_label = Label(
            text="단어 맞히기 게임 2.0", 
            font_size='30sp', 
            font_name="Nanum",
            size_hint_y=0.2
        )
        layout.add_widget(main_label)
        
        # 단어 표시 영역
        word_display = Label(
            text="teacher", 
            font_size='50sp', 
            bold=True,
            size_hint_y=0.3
        )
        layout.add_widget(word_display)
        
        # 정답 버튼 영역 (2x2 그리드)
        grid = GridLayout(cols=2, spacing=10, size_hint_y=0.4)
        answers = ["선생님", "학생", "학교", "교실"]
        
        for ans in answers:
            btn = Button(
                text=ans, 
                font_name="Nanum", 
                font_size='20sp',
                background_color=(0.1, 0.3, 0.5, 1)
            )
            grid.add_widget(btn)
            
        layout.add_widget(grid)
        
        # 하단 메뉴 버튼
        bottom_btn = Button(
            text="다음 문제", 
            font_name="Nanum", 
            size_hint_y=0.1,
            background_color=(0.2, 0.5, 0.2, 1)
        )
        layout.add_widget(bottom_btn)
        
        return layout

if __name__ == "__main__":
    WordGameApp().run()
