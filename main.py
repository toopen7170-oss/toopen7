import os
import sys
import random
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window

# 폰트 등록
try:
    LabelBase.register(name="Nanum", fn_regular="font.ttf")
except:
    pass

# 데이터 저장소
store = JsonStore('user_data.json')
word_store = JsonStore('words.json')

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        layout.add_widget(Label(text="외국어 마스터 2.0", font_size='40sp', font_name="Nanum"))
        
        self.user_id = TextInput(hint_text="아이디", multiline=False, size_hint_y=None, height='50dp')
        self.user_pw = TextInput(hint_text="비밀번호", password=True, multiline=False, size_hint_y=None, height='50dp')
        
        layout.add_widget(self.user_id)
        layout.add_widget(self.user_pw)
        
        btn_layout = BoxLayout(spacing=10, size_hint_y=None, height='60dp')
        login_btn = Button(text="로그인", font_name="Nanum", background_color=(0.2, 0.6, 1, 1))
        login_btn.bind(on_release=self.login)
        reg_btn = Button(text="회원가입", font_name="Nanum", background_color=(0.3, 0.3, 0.3, 1))
        reg_btn.bind(on_release=self.register)
        
        btn_layout.add_widget(login_btn)
        btn_layout.add_widget(reg_btn)
        layout.add_widget(btn_layout)
        self.add_widget(layout)

    def login(self, instance):
        uid = self.user_id.text
        upw = self.user_pw.text
        if store.exists(uid) and store.get(uid)['pw'] == upw:
            self.manager.current_user = uid
            self.manager.current = 'menu'
        
    def register(self, instance):
        uid = self.user_id.text
        upw = self.user_pw.text
        if uid and upw and not store.exists(uid):
            store.put(uid, pw=upw, level='basic', stage=1, total_score=0, correct=0, wrong=0)
            self.login(None)

class MenuScreen(Screen):
    def on_enter(self):
        self.refresh()

    def refresh(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        user_info = store.get(self.manager.current_user)
        info_label = Label(text=f"ID: {self.manager.current_user} | 점수: {user_info['total_score']}", 
                           font_name="Nanum", size_hint_y=0.1)
        layout.add_widget(info_label)

        levels = [("기초 (4칸)", 'basic', 4), ("초급 (6칸)", 'beginner', 6), 
                  ("중급 (9칸)", 'middle', 9), ("고급 (16칸)", 'advanced', 16)]
        
        curr_level = user_info['level']
        
        for name, lv_id, grid_size in levels:
            btn = Button(text=name, font_name="Nanum", font_size='20sp')
            # 잠금 로직 (단순화: 기초부터 순차적)
            btn.bind(on_release=lambda x, gs=grid_size, li=lv_id: self.start_game(gs, li))
            layout.add_widget(btn)
            
        self.add_widget(layout)

    def start_game(self, grid_size, level_id):
        self.manager.game_grid_size = grid_size
        self.manager.game_level_id = level_id
        self.manager.current = 'game'

class GameScreen(Screen):
    def on_enter(self):
        self.hearts = 5
        self.correct_in_row = 0
        self.init_ui()
        self.next_question()

    def init_ui(self):
        self.clear_widgets()
        self.main_layout = BoxLayout(orientation='vertical', padding=10)
        
        # 상단바 (하트 및 점수)
        top_bar = BoxLayout(size_hint_y=0.1)
        self.heart_label = Label(text="❤️" * self.hearts, font_size='25sp')
        self.score_label = Label(text="정답: 0 | 오답: 0", font_name="Nanum")
        top_bar.add_widget(self.heart_label)
        top_bar.add_widget(self.score_label)
        self.main_layout.add_widget(top_bar)

        # 문제 단어 표시
        self.word_label = Label(text="준비...", font_size='50sp', bold=True, size_hint_y=0.2)
        self.main_layout.add_widget(self.word_label)

        # 정답 그리드
        gs = self.manager.game_grid_size
        cols = 2 if gs == 4 else (3 if gs == 9 else 4)
        self.grid = GridLayout(cols=cols, spacing=5, size_hint_y=0.6)
        self.main_layout.add_widget(self.grid)

        # 하단 숨겨진 버튼 (하트 1개일 때만 활성화)
        self.hidden_btn = Button(text="❤️ 채우기", size_hint=(None, None), size=(100, 50), 
                                 opacity=0, disabled=True, font_name="Nanum")
        self.hidden_btn.bind(on_release=self.refill_hearts)
        self.main_layout.add_widget(self.hidden_btn)
        
        self.add_widget(self.main_layout)

    def refill_hearts(self, instance):
        self.hearts = 5
        self.heart_label.text = "❤️" * self.hearts
        self.hidden_btn.opacity = 0
        self.hidden_btn.disabled = True

    def next_question(self):
        # 샘플 데이터 (실제는 words.json 연동)
        words = [
            {"en": "apple", "ko": "사과"}, {"en": "teacher", "ko": "선생님"},
            {"en": "student", "ko": "학생"}, {"en": "school", "ko": "학교"},
            {"en": "banana", "ko": "바나나"}, {"en": "water", "ko": "물"}
        ]
        self.q_word = random.choice(words)
        self.word_label.text = self.q_word['en']
        self.play_tts(self.q_word['en'])

        self.grid.clear_widgets()
        options = [self.q_word['ko']]
        while len(options) < self.manager.game_grid_size:
            w = random.choice(words)['ko']
            if w not in options: options.append(w)
        random.shuffle(options)

        for opt in options:
            btn = Button(text=opt, font_name="Nanum", font_size='18sp', background_color=(0.1, 0.2, 0.4, 1))
            btn.bind(on_release=self.check_answer)
            self.grid.add_widget(btn)

    def check_answer(self, instance):
        if instance.text == self.q_word['ko']:
            self.word_label.text = "O"
            self.correct_in_row += 1
            self.play_tts(self.q_word['en'])
            Clock.schedule_once(lambda dt: self.next_question(), 1)
        else:
            self.word_label.text = "X 외때려"
            self.hearts -= 1
            self.heart_label.text = "❤️" * self.hearts
            if self.hearts == 1:
                self.hidden_btn.opacity = 1
                self.hidden_btn.disabled = False
            if self.hearts <= 0:
                self.manager.current = 'menu'
            else:
                Clock.schedule_once(lambda dt: self.next_question(), 1)

    def play_tts(self, text):
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
            Locale = autoclass('java.util.Locale')
            if not hasattr(self, 'tts'):
                self.tts = TextToSpeech(PythonActivity.mActivity, None)
            self.tts.setLanguage(Locale.US)
            self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None)
        except:
            print(f"TTS: {text}")

class WindowManager(ScreenManager):
    current_user = ""
    game_grid_size = 4
    game_level_id = 'basic'

class MainApp(App):
    def build(self):
        wm = WindowManager()
        wm.add_widget(LoginScreen(name='login'))
        wm.add_widget(MenuScreen(name='menu'))
        wm.add_widget(GameScreen(name='game'))
        return wm

if __name__ == "__main__":
    MainApp().run()
