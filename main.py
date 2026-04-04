import json
import os
import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.text import LabelBase

# [기초 다지기] 파일 경로를 안전하게 설정합니다. (팅김 방지 핵심)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
STORE_FILE = os.path.join(BASE_PATH, 'words.json')
FONT_PATH = os.path.join(BASE_PATH, 'font.ttf')

# [2번 수리] 폰트 등록 (8번 사진 깨짐 해결)
# font.ttf 파일이 리포지토리에 반드시 존재해야 합니다.
try:
    LabelBase.register(name="Nanum", fn_regular=FONT_PATH)
except Exception as e:
    print(f"폰트 로드 실패: {e}")

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        # 타이틀 (폰트 적용)
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
    # [3번 수리] 일본어 추가 (7번 사진 대응)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=15)
        layout.add_widget(Label(text="목표 언어를 선택하세요", font_name="Nanum", font_size='25sp'))
        
        # 일본어(ja) 항목 추가
        langs = [("English", "en"), ("Vietnamese", "vi"), ("Chinese", "zh"), ("Japanese", "ja")]
        for name, code in langs:
            # 버튼에도 폰트 적용
            btn = Button(text=name, font_name="Nanum", size_hint_y=None, height='60dp')
            btn.bind(on_release=lambda x, c=code: self.start_learning(c))
            layout.add_widget(btn)
        
        # 메인으로 돌아가기 버튼 (안전 장치)
        back_btn = Button(text="메인으로", font_name="Nanum", size_hint_y=None, height='50dp', background_color=(0.5, 0.5, 0.5, 1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)

    def start_learning(self, lang_code):
        self.manager.target_lang = lang_code
        self.manager.current = 'game'

class AdminScreen(Screen):
    # [2번 수리] 입력 폼 화면 복원 및 폰트 적용 (8번 사진 대응)
    def on_enter(self):
        self.refresh()

    def refresh(self):
        self.clear_widgets()
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # 스크롤 가능한 입력 레이아웃
        scroll = ScrollView()
        input_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        input_layout.bind(minimum_height=input_layout.setter('height'))

        # 입력 필드 정의
        self.inputs = {
            'level': TextInput(hint_text="등급 (초급/중급/상급)", font_name="Nanum", multiline=False, size_hint_y=None, height='50dp'),
            'step': TextInput(hint_text="단계 (1~10)", multiline=False, size_hint_y=None, height='50dp'),
            'ko': TextInput(hint_text="한국어 뜻", font_name="Nanum", multiline=False, size_hint_y=None, height='50dp'),
            'en': TextInput(hint_text="영어 단어", multiline=False, size_hint_y=None, height='50dp'),
            'vi': TextInput(hint_text="베트남어 단어", multiline=False, size_hint_y=None, height='50dp'),
            'zh': TextInput(hint_text="중국어 단어", multiline=False, size_hint_y=None, height='50dp'),
            'ja': TextInput(hint_text="일본어 단어", multiline=False, size_hint_y=None, height='50dp')
        }
        
        # 힌트 텍스트 폰트 적용을 위해 레이블 추가
        for key, ti in self.inputs.items():
            input_layout.add_widget(ti)

        scroll.add_widget(input_layout)
        main_layout.add_widget(scroll, size_hint_y=0.7)

        # 버튼 바 (저장, 삭제, 뒤로가기)
        btn_box = BoxLayout(size_hint_y=0.15, spacing=10)
        
        save_btn = Button(text="단어 저장", font_name="Nanum", background_color=(0, 0.7, 0, 1))
        save_btn.bind(on_release=self.save_word)
        
        # [2번 수리] 삭제 버튼 기능 추가
        del_btn = Button(text="필드 초기화", font_name="Nanum", background_color=(0.7, 0, 0, 1))
        del_btn.bind(on_release=self.clear_inputs)
        
        back_btn = Button(text="뒤로가기", font_name="Nanum")
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))

        btn_box.add_widget(save_btn)
        btn_box.add_widget(del_btn)
        btn_box.add_widget(back_btn)
        
        main_layout.add_widget(btn_box)
        self.add_widget(main_layout)

    def save_word(self, instance):
        # UTF-8 인코딩으로 데이터 저장 (깨짐 방지)
        try:
            with open(STORE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except: data = {}

        lv = self.inputs['level'].text
        st = self.inputs['step'].text
        if not lv or not st: return # 등급/단계 미입력 시 저장 안 함

        if lv not in data: data[lv] = {}
        if st not in data[lv]: data[lv][st] = []

        new_entry = {k: v.text for k, v in self.inputs.items() if k not in ['level', 'step']}
        data[lv][st].append(new_entry)

        with open(STORE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("단어 저장 완료")
        self.refresh()

    def clear_inputs(self, instance):
        for ti in self.inputs.values(): ti.text = ""

class GameScreen(Screen):
    # [1번 수리] 단어 없음 메시지 및 뒤로가기 버튼 추가 (9번 사진 대응)
    def on_enter(self):
        self.refresh_data()

    def refresh_data(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # 데이터 불러오기
        try:
            with open(STORE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 초기 데이터를 위해 '초급'의 '1'단계를 가져옵니다.
                self.words = data.get('초급', {}).get('1', [])
        except: self.words = []

        # 1번 문제 해결: 단어가 없을 때 메시지와 뒤로가기 버튼 표시
        if not self.words:
            layout.add_widget(Label(text="학습할 단어가 없습니다.\n관리 화면에서 단어를 추가해주세요.", font_name="Nanum", halign="center"))
            back_btn = Button(text="메인으로 돌아가기", font_name="Nanum", size_hint=(None, None), size=('150dp', '50dp'), pos_hint={'center_x': 0.5})
            back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
            layout.add_widget(back_btn)
            self.add_widget(layout)
            return

        # 랜덤 단어 출제
        current_q = random.choice(self.words)
        target_lang = self.manager.target_lang
        
        layout.add_widget(Label(text=f"문제: {current_q.get(target_lang, 'N/A')}", font_size='30sp'))
        layout.add_widget(Label(text=f"(한국어 뜻: {current_q.get('ko', 'N/A')})", font_name="Nanum", font_size='18sp', color=(0.7, 0.7, 0.7, 1)))

        next_btn = Button(text="다음 단어", font_name="Nanum", size_hint_y=None, height='60dp')
        next_btn.bind(on_release=lambda x: self.refresh_data())
        layout.add_widget(next_btn)
        
        # 학습 중료 버튼
        back_btn = Button(text="학습 종료 (메인으로)", font_name="Nanum", size_hint_y=None, height='50dp', background_color=(0.5, 0.5, 0.5, 1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(back_btn)

        self.add_widget(layout)

class MyManager(ScreenManager):
    target_lang = 'en' # 기본 목표 언어

class MainApp(App):
    def build(self):
        # UTF-8 기반 기본 파일 생성 및 초기 데이터 (팅김 방지)
        if not os.path.exists(STORE_FILE):
            example_data = {
                "초급": {
                    "1": [
                        {"ko": "안녕하세요", "en": "Hello", "vi": "Xin chào", "zh": "你好", "ja": "こんにちは"}
                    ]
                }
            }
            with open(STORE_FILE, 'w', encoding='utf-8') as f:
                json.dump(example_data, f, ensure_ascii=False, indent=2)

        sm = MyManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(LangSelect(name='lang_select'))
        sm.add_widget(AdminScreen(name='admin'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == "__main__":
    MainApp().run()
