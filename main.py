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
from kivy.core.text import LabelBase
from kivy.utils import platform

# 파일 경로 설정 (팅김 방지 핵심)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
STORE_FILE = os.path.join(BASE_PATH, 'words.json')
FONT_PATH = os.path.join(BASE_PATH, 'font.ttf')

# 1단계: 폰트 등록 (1번 사진 깨짐 해결)
try:
    LabelBase.register(name="Nanum", fn_regular=FONT_PATH)
except Exception as e:
    print(f"폰트 로드 실패: {e}")

# 안드로이드 발음(TTS) 설정
if platform == 'android':
    try:
        from jnius import autoclass
        Locale = autoclass('java.util.Locale')
        TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
    except:
        pass

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(text="다국어 단어 마스터 2.0", font_name="Nanum", font_size='30sp'))
        
        for text, target in [("학습 시작하기", "lang_select"), ("단어장 관리", "admin")]:
            btn = Button(text=text, font_name="Nanum", size_hint_y=None, height='70dp')
            btn.bind(on_release=lambda x, t=target: setattr(self.manager, 'current', t))
            layout.add_widget(btn)
        self.add_widget(layout)

class LangSelect(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=15)
        layout.add_widget(Label(text="목표 언어를 선택하세요", font_name="Nanum", font_size='25sp'))
        
        for name, code in [("English", "en"), ("Vietnamese", "vi"), ("Chinese", "zh")]:
            btn = Button(text=name, font_name="Nanum", size_hint_y=None, height='60dp')
            btn.bind(on_release=lambda x, c=code: self.start_learning(c))
            layout.add_widget(btn)
        
        back = Button(text="뒤로가기", font_name="Nanum", size_hint_y=None, height='50dp')
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(back)
        self.add_widget(layout)

    def start_learning(self, code):
        self.manager.target_lang = code
        self.manager.current = 'game'

class AdminScreen(Screen):
    def on_enter(self):
        self.refresh()

    def refresh(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        self.inputs = {
            'level': TextInput(hint_text="등급", font_name="Nanum", multiline=False),
            'ko': TextInput(hint_text="한국어", font_name="Nanum", multiline=False),
            'en': TextInput(hint_text="영어", multiline=False),
            'vi': TextInput(hint_text="베트남어", multiline=False)
        }
        for i in self.inputs.values(): layout.add_widget(i)

        btn_box = BoxLayout(size_hint_y=None, height='60dp', spacing=10)
        save = Button(text="저장", font_name="Nanum", background_color=(0, 0.7, 0, 1))
        save.bind(on_release=self.save_word)
        back = Button(text="닫기", font_name="Nanum")
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        
        btn_box.add_widget(save); btn_box.add_widget(back)
        layout.add_widget(btn_box)
        self.add_widget(layout)

    def save_word(self, instance):
        try:
            with open(STORE_FILE, 'r', encoding='utf-8') as f: data = json.load(f)
        except: data = {"초급": {"1": []}}
        
        new_entry = {k: v.text for k, v in self.inputs.items() if k != 'level'}
        data.setdefault("초급", {}).setdefault("1", []).append(new_entry)

        with open(STORE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.refresh()

class GameScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        try:
            with open(STORE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.words = data.get("초급", {}).get("1", [])
        except: self.words = []
        
        if not self.words:
            self.add_widget(Label(text="단어가 없습니다.", font_name="Nanum"))
            return
            
        self.current_q = random.choice(self.words)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # 문제 단어 표시 (선택한 언어)
        target = self.manager.target_lang
        layout.add_widget(Label(text=self.current_q.get(target, ""), font_size='40sp'))
        
        self.ans = TextInput(hint_text="한국어 뜻 입력", font_name="Nanum", multiline=False)
        layout.add_widget(self.ans)
        
        check = Button(text="정답 확인", font_name="Nanum", size_hint_y=None, height='60dp')
        check.bind(on_release=self.check_ans)
        layout.add_widget(check)
        
        exit_btn = Button(text="종료", font_name="Nanum", size_hint_y=None, height='50dp')
        exit_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(exit_btn)
        self.add_widget(layout)

    def check_ans(self, instance):
        if self.ans.text.strip() == self.current_q.get('ko', "").strip():
            self.ans.text = "정답입니다!"
        else:
            self.ans.text = f"틀림! 정답: {self.current_q.get('ko')}"

class MyManager(ScreenManager):
    target_lang = 'en'

class MainApp(App):
    def build(self):
        if not os.path.exists(STORE_FILE):
            with open(STORE_FILE, 'w', encoding='utf-8') as f:
                json.dump({"초급": {"1": [{"ko":"사과", "en":"apple", "vi":"táo"}]}}, f)
        sm = MyManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(LangSelect(name='lang_select'))
        sm.add_widget(AdminScreen(name='admin'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == "__main__":
    MainApp().run()
