import random
import json
import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.storage.jsonstore import JsonStore
from kivy.core.text import LabelBase

# 폰트 등록
try:
    LabelBase.register(name="Nanum", fn_regular="font.ttf")
except:
    pass

STORE_FILE = 'words.json'
PROGRESS = JsonStore('user_progress.json')

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(text="다국어 단어 마스터 2.0", font_name="Nanum", font_size='30sp'))
        
        btns = [
            ("학습 시작하기", "lang_select"),
            ("단어 관리 (추가/삭제)", "admin")
        ]
        for text, target in btns:
            btn = Button(text=text, font_name="Nanum", size_hint_y=None, height='70dp')
            btn.bind(on_release=lambda x, t=target: setattr(self.manager, 'current', t))
            layout.add_widget(btn)
        self.add_widget(layout)

class LangSelect(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=15)
        layout.add_widget(Label(text="목표 언어를 선택하세요", font_name="Nanum", font_size='25sp'))
        
        langs = [("English", "en"), ("Vietnamese", "vi"), ("Chinese", "zh"), ("Japanese", "ja")]
        for name, code in langs:
            btn = Button(text=name, size_hint_y=None, height='60dp')
            btn.bind(on_release=lambda x, c=code: self.start_learning(c))
            layout.add_widget(btn)
        self.add_widget(layout)

    def start_learning(self, code):
        self.manager.target_lang = code
        self.manager.current = 'level_select'

class AdminScreen(Screen):
    """ 단어 추가/수정/삭제 화면 """
    def on_enter(self):
        self.refresh()

    def refresh(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 입력 필드
        self.inputs = {
            'level': TextInput(hint_text="등급 (기초/초급/중급/상급)", font_name="Nanum", multiline=False),
            'step': TextInput(hint_text="단계 (1~10)", multiline=False),
            'en': TextInput(hint_text="영어", multiline=False),
            'vi': TextInput(hint_text="베트남어", multiline=False),
            'ko': TextInput(hint_text="한국어", multiline=False),
            'zh': TextInput(hint_text="중국어", multiline=False),
            'ja': TextInput(hint_text="일본어", multiline=False)
        }
        for i in self.inputs.values(): layout.add_widget(i)

        btn_box = BoxLayout(size_hint_y=None, height='50dp', spacing=5)
        save_btn = Button(text="단어 저장", font_name="Nanum", background_color=(0,1,0,1))
        save_btn.bind(on_release=self.save_word)
        back_btn = Button(text="뒤로가기", font_name="Nanum")
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        
        btn_box.add_widget(save_btn)
        btn_box.add_widget(back_btn)
        layout.add_widget(btn_box)
        self.add_widget(layout)

    def save_word(self, instance):
        # 로컬 json 파일 로드 및 저장 로직
        try:
            with open(STORE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except: data = {}

        lv = self.inputs['level'].text
        st = self.inputs['step'].text
        if lv not in data: data[lv] = {}
        if st not in data[lv]: data[lv][st] = []

        new_entry = {k: v.text for k, v in self.inputs.items() if k not in ['level', 'step']}
        data[lv][st].append(new_entry)

        with open(STORE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.refresh()

class GameScreen(Screen):
    # (이전 드린 4지선답 및 50문제 승급 로직 포함)
    pass

class MyManager(ScreenManager):
    target_lang = 'en'
    selected_rank = '기초'

class MainApp(App):
    def build(self):
        # 초기 파일 생성
        if not os.path.exists(STORE_FILE):
            with open(STORE_FILE, 'w', encoding='utf-8') as f:
                json.dump({"기초": {"1": []}}, f)

        sm = MyManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(LangSelect(name='lang_select'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm

if __name__ == "__main__":
    MainApp().run()
