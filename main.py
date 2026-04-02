import json
import random
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import SoundLoader

# 기본 설정: 핸드폰 화면에 꽉 차도록 설정
Window.clearcolor = get_color_from_hex('#121212')

# 데이터 저장소 설정
store = JsonStore('user_data.json')
if not store.exists('profile'):
    store.put('profile', name='Guest', total_score=0, correct=0, wrong=0, level='basic', stage=1)

# [폰트 해결] 안드로이드에서 한글/외국어 깨짐 방지를 위해 시스템 폰트 경로 설정 가능
# 기본적으로 Kivy는 나눔고딕 등을 번들링해야 하지만, 여기서는 기본 설정을 유지합니다.

class MainMenu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(text="외국어 단어 마스터 2.0", font_size='30sp', color=get_color_from_hex('#FFD700'), size_hint_y=0.2)
        layout.add_widget(title)

        buttons = [
            ("게임 시작", "game_select"),
            ("오답 노트", "incorrect_note"),
            ("단어장", "word_book"),
            ("명예의 전당", "hall_of_fame"),
            ("설정/관리", "settings")
        ]

        for text, screen in buttons:
            btn = Button(text=text, font_size='20sp', background_color=get_color_from_hex('#1E88E5'))
            btn.bind(on_release=lambda x, s=screen: self.change_screen(s))
            layout.add_widget(btn)
        
        self.add_widget(layout)

    def change_screen(self, screen_name):
        self.manager.current = screen_name

class GameSelect(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = GridLayout(cols=2, padding=20, spacing=20)
        
        levels = [
            ("기초 (4칸)", "basic"),
            ("초급 (6칸)", "beginner"),
            ("중급 (9칸)", "intermediate"),
            ("고급 (16칸)", "advanced"),
            ("최상급", "expert"),
            ("마스터", "master")
        ]

        for text, level_id in levels:
            btn = Button(text=text, font_size='18sp', background_color=get_color_from_hex('#43A047'))
            btn.bind(on_release=lambda x, l=level_id: self.start_game(l))
            self.layout.add_widget(btn)
            
        back_btn = Button(text="뒤로가기", size_hint_y=0.2)
        back_btn.bind(on_release=lambda x: self.change_screen("main_menu"))
        
        root = BoxLayout(orientation='vertical')
        root.add_widget(self.layout)
        root.add_widget(back_btn)
        self.add_widget(root)

    def start_game(self, level):
        # 단계별 잠금 로직 적용 지점
        self.manager.get_screen('quiz_screen').current_level = level
        self.manager.current = 'quiz_screen'

    def change_screen(self, name):
        self.manager.current = name

class QuizScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.hearts = 5
        self.current_level = "basic"
        self.stage = 1
        self.layout = BoxLayout(orientation='vertical', padding=10)
        
        # 상단 바 (하트, 점수)
        self.top_bar = BoxLayout(size_hint_y=0.1)
        self.heart_label = Label(text="❤️❤️❤️❤️❤️", font_size='20sp')
        self.score_label = Label(text="정답: 0  오답: 0", font_size='18sp')
        self.top_bar.add_widget(self.heart_label)
        self.top_bar.add_widget(self.score_label)
        
        # 문제 영역
        self.question_label = Label(text="문제를 생성 중...", font_size='24sp', size_hint_y=0.2)
        
        # 선택지 영역
        self.options_layout = GridLayout(cols=2, spacing=10)
        
        # 하단 버튼
        self.nav_bar = BoxLayout(size_hint_y=0.1, spacing=5)
        self.nav_bar.add_widget(Button(text="일시정지", on_release=self.toggle_pause))
        self.nav_bar.add_widget(Button(text="종료", on_release=self.exit_game))
        
        # 숨은 하트 충전 버튼 (초기엔 투명)
        self.hidden_refill_btn = Button(text="하트충전", size_hint=(None, None), size=(100, 50), opacity=0)
        self.hidden_refill_btn.bind(on_release=self.refill_hearts)

        self.layout.add_widget(self.top_bar)
        self.layout.add_widget(self.question_label)
        self.layout.add_widget(self.options_layout)
        self.layout.add_widget(self.nav_bar)
        self.add_widget(self.layout)
        
        self.paused = False

    def on_enter(self):
        self.load_next_question()

    def load_next_question(self):
        self.options_layout.clear_widgets()
        # 여기에 단어 로직 (랜덤 선택) 추가
        # 예시 데이터
        q_word = "Apple"
        correct_ans = "사과"
        options = ["사과", "포도", "바나나", "수박"]
        random.shuffle(options)

        self.question_label.text = f"단어를 듣고 맞추세요\n(발음 재생 중...)"
        # 발음 재생 코드 (TTS 또는 오디오 파일)
        
        for opt in options:
            btn = Button(text=opt, font_size='18sp')
            btn.bind(on_release=lambda x, a=opt: self.check_answer(a, correct_ans))
            self.options_layout.add_widget(btn)

    def check_answer(self, user_ans, correct_ans):
        if user_ans == correct_ans:
            # 정답 처리
            self.show_popup("O", "정답입니다!")
            self.load_next_question()
        else:
            # 오답 처리
            self.hearts -= 1
            self.update_hearts()
            self.show_popup("X", "외때려! 틀렸습니다.")
            if self.hearts <= 0:
                self.exit_game()
            else:
                self.load_next_question()

    def update_hearts(self):
        self.heart_label.text = "❤️" * self.hearts
        if self.hearts == 1:
            self.hidden_refill_btn.opacity = 1
            self.layout.add_widget(self.hidden_refill_btn)

    def refill_hearts(self, instance):
        self.hearts = 5
        self.update_hearts()
        self.hidden_refill_btn.opacity = 0
        self.layout.remove_widget(self.hidden_refill_btn)

    def toggle_pause(self, instance):
        self.paused = not self.paused
        # 일시 정지 로직

    def exit_game(self, instance=None):
        self.manager.current = 'main_menu'

    def show_popup(self, title, msg):
        content = Button(text=msg)
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        content.bind(on_release=popup.dismiss)
        popup.open()

# 나머지 화면 클래스 (명예의전당, 오답노트 등)는 위 구조와 유사하게 구현됩니다.

class WordGameApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(GameSelect(name='game_select'))
        sm.add_widget(QuizScreen(name='quiz_screen'))
        # 추가 화면들 등록...
        return sm

if __name__ == '__main__':
    WordGameApp().run()
