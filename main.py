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
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.storage.jsonstore import JsonStore

# 화면 배경색 및 설정
Window.clearcolor = get_color_from_hex('#121212')

class QuizScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.hearts = 5
        self.max_hearts = 5
        self.current_level = "basic"
        self.stage = 1
        self.correct_count = 0
        self.wrong_count = 0
        self.words_data = {}
        self.load_data()
        
        # 메인 레이아웃
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 상단 정보창 (하트, 점수)
        self.top_info = BoxLayout(size_hint_y=0.1)
        self.heart_label = Label(text="❤️❤️❤️❤️❤️", font_size='22sp', color=(1,0,0,1))
        self.score_label = Label(text="정답: 0 | 오답: 0", font_size='18sp')
        self.top_info.add_widget(self.heart_label)
        self.top_info.add_widget(self.score_label)
        
        # 문제 출력창
        self.question_box = BoxLayout(orientation='vertical', size_hint_y=0.3)
        self.level_label = Label(text="기초 단계", font_size='16sp', color=(0.7,0.7,0.7,1))
        self.word_label = Label(text="준비 중...", font_size='32sp', bold=True)
        self.question_box.add_widget(self.level_label)
        self.question_box.add_widget(self.word_label)
        
        # 선택지 버튼 창
        self.options_grid = GridLayout(cols=2, spacing=10, size_hint_y=0.5)
        
        # 하단 컨트롤 바
        self.nav_bar = BoxLayout(size_hint_y=0.1, spacing=5)
        self.nav_bar.add_widget(Button(text="일시정지", background_color=(0.3,0.3,0.3,1), on_release=self.toggle_pause))
        self.nav_bar.add_widget(Button(text="종료", background_color=(0.8,0.2,0.2,1), on_release=self.go_back))
        
        self.layout.add_widget(self.top_info)
        self.layout.add_widget(self.question_box)
        self.layout.add_widget(self.options_grid)
        self.layout.add_widget(self.nav_bar)
        
        self.add_widget(self.layout)
        
        # 숨은 하트 버튼 (평소엔 안보임)
        self.hidden_btn = Button(text="❤️+", size_hint=(None, None), size=(60, 60), 
                                 pos_hint={'right': 1, 'bottom': 1}, opacity=0)
        self.hidden_btn.bind(on_release=self.refill_hearts)
        self.add_widget(self.hidden_btn)

    def load_data(self):
        try:
            with open('words.json', 'r', encoding='utf-8') as f:
                self.words_data = json.load(f)
        except:
            self.words_data = {"basic": [{"en":"apple", "ko":"사과"}]}

    def on_enter(self):
        self.next_question()

    def next_question(self):
        self.options_grid.clear_widgets()
        level_list = self.words_data.get(self.current_level, [])
        if not level_list: return
        
        target = random.choice(level_list)
        correct_ans = target['ko']
        self.word_label.text = target['en'] # 여기에 발음 기능 연동 가능
        
        # 4지선다 만들기
        options = [correct_ans]
        all_ko = [w['ko'] for w in level_list if w['ko'] != correct_ans]
        options += random.sample(all_ko, min(len(all_ko), 3))
        random.shuffle(options)
        
        for opt in options:
            btn = Button(text=opt, font_size='20sp', background_color=(0.2,0.5,0.8,1))
            btn.bind(on_release=lambda x, a=opt, c=correct_ans: self.check_answer(a, c))
            self.options_grid.add_widget(btn)

    def check_answer(self, user_ans, correct_ans):
        if user_ans == correct_ans:
            self.correct_count += 1
            self.show_popup("정답!", "O", (0,1,0,1))
        else:
            self.wrong_count += 1
            self.hearts -= 1
            self.show_popup("오답!", "외때려! X", (1,0,0,1))
            self.update_hearts_ui()
            
        self.score_label.text = f"정답: {self.correct_count} | 오답: {self.wrong_count}"
        if self.hearts > 0:
            self.next_question()
        else:
            self.go_back()

    def update_hearts_ui(self):
        self.heart_label.text = "❤️" * self.hearts
        self.hidden_btn.opacity = 1 if self.hearts == 1 else 0

    def refill_hearts(self, instance):
        self.hearts = 5
        self.update_hearts_ui()

    def toggle_pause(self, instance):
        pass # 일시정지 로직

    def go_back(self, instance=None):
        self.manager.current = 'main_menu'

    def show_popup(self, title, msg, color):
        p = Popup(title=title, content=Label(text=msg, font_size='20sp', color=color), size_hint=(0.7, 0.4))
        p.open()
        Clock.schedule_once(lambda dt: p.dismiss(), 0.8)

class MainMenu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        layout.add_widget(Label(text="단어 맞추기 2.0", font_size='40sp', bold=True))
        
        start_btn = Button(text="게임 시작", size_hint_y=0.2, background_color=(0.1, 0.7, 0.3, 1))
        start_btn.bind(on_release=self.start)
        layout.add_widget(start_btn)
        
        exit_btn = Button(text="종료", size_hint_y=0.2)
        exit_btn.bind(on_release=lambda x: App.get_running_app().stop())
        layout.add_widget(exit_btn)
        self.add_widget(layout)

    def start(self, instance):
        self.manager.current = 'quiz_screen'

class WordApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(QuizScreen(name='quiz_screen'))
        return sm

if __name__ == '__main__':
    WordApp().run()
