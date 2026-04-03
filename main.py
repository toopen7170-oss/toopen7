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

# [기능 개선] 안드로이드 발음(TTS) 기능을 위한 라이브러리 임포트
# PC에서 테스트할 때는 작동하지 않지만, APK로 만들면 작동합니다.
from kivy.utils import platform
if platform == 'android':
    from android.tts import TTS
    android_tts = TTS()
else:
    android_tts = None

# [1단계 완료] 폰트 등록 (폰트 깨짐 해결)
# 파일 목록에 'font.ttf'가 반드시 있어야 합니다.
try:
    LabelBase.register(name="Nanum", fn_regular="font.ttf")
except Exception as e:
    print(f"폰트 등록 실패: {e}. 'font.ttf' 파일을 확인하세요.")

STORE_FILE = 'words.json'

# 전역 변수로 현재 학습 중인 단어 목록 저장
current_word_list = []

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # [복원] 프리스톤테일 메뉴를 지우고 학습 앱 메뉴로 복원
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # 타이틀 (폰트 적용)
        layout.add_widget(Label(text="다국어 단어 마스터 2.0", font_name="Nanum", font_size='30sp', size_hint_y=None, height='100dp'))
        
        btns = [
            ("학습 시작하기 (단어 게임)", "lang_select"),
            ("단어장 관리 (추가/삭제)", "admin")
        ]
        for text, target in btns:
            btn = Button(text=text, font_name="Nanum", size_hint_y=None, height='70dp')
            btn.bind(on_release=lambda x, t=target: setattr(self.manager, 'current', t))
            layout.add_widget(btn)
        
        self.add_widget(layout)

class LangSelect(Screen):
    # [2단계 수리] 외국어 버튼 작동 불능 해결 (6번 사진 대응)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=15)
        layout.add_widget(Label(text="목표 언어를 선택하세요", font_name="Nanum", font_size='25sp'))
        
        langs = [("English", "en"), ("Vietnamese", "vi"), ("Chinese", "zh"), ("Japanese", "ja")]
        for name, code in langs:
            # 버튼에도 폰트 적용
            btn = Button(text=name, font_name="Nanum", size_hint_y=None, height='60dp')
            # [수정] 버튼을 누르면 start_learning 함수가 호출되도록 바인딩
            btn.bind(on_release=lambda x, c=code: self.start_learning(c))
            layout.add_widget(btn)
            
        back_btn = Button(text="메인으로", font_name="Nanum", size_hint_y=None, height='50dp', background_color=(0.5, 0.5, 0.5, 1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def start_learning(self, lang_code):
        # 학습할 언어를 매니저에 저장하고 게임 화면으로 이동
        self.manager.target_lang = lang_code
        self.manager.current = 'game'

class AdminScreen(Screen):
    # [복원] 프리스톤테일 관리 화면을 단어 관리 화면으로 복원
    def on_enter(self):
        self.refresh()

    def refresh(self):
        self.clear_widgets()
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # 입력 필드 (폰트 적용)
        input_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height='200dp')
        self.inputs = {
            'level': TextInput(hint_text="등급 (초급/중급/상급)", font_name="Nanum", multiline=False),
            'step': TextInput(hint_text="단계 (1~10)", multiline=False),
            'ko': TextInput(hint_text="한국어 뜻", font_name="Nanum", multiline=False),
            'en': TextInput(hint_text="영어 단어", multiline=False),
            'vi': TextInput(hint_text="베트남어 단어", multiline=False),
            'zh': TextInput(hint_text="중국어 단어", multiline=False)
        }
        for i in self.inputs.values(): input_layout.add_widget(i)
        main_layout.add_widget(input_layout)

        # 버튼 바
        btn_box = BoxLayout(size_hint_y=None, height='60dp', spacing=10)
        save_btn = Button(text="단어 저장", font_name="Nanum", background_color=(0, 0.7, 0, 1))
        save_btn.bind(on_release=self.save_word)
        back_btn = Button(text="닫기", font_name="Nanum")
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        
        btn_box.add_widget(save_btn)
        btn_box.add_widget(back_btn)
        main_layout.add_widget(btn_box)
        self.add_widget(main_layout)

    def save_word(self, instance):
        # UTF-8 인코딩으로 단어 저장
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
        print("단어 저장 완료")
        self.refresh()

class GameScreen(Screen):
    # [복원 및 신규] 단어 게임 및 발음 공부 화면
    def on_enter(self):
        self.load_words()
        self.next_question()

    def load_words(self):
        global current_word_list
        # words.json에서 데이터를 불러와서 학습 리스트를 만듭니다.
        # (실제 앱에서는 선택한 등급/단계에 따라 필터링하는 로직이 필요합니다.)
        try:
            with open(STORE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 예시로 '초급'의 '1'단계를 가져옵니다.
                current_word_list = data.get('초급', {}).get('1', [])
        except:
            current_word_list = []

    def next_question(self):
        self.clear_widgets()
        if not current_word_list:
            self.add_widget(Label(text="학습할 단어가 없습니다.\n단어장에서 단어를 추가해주세요.", font_name="Nanum", halign="center"))
            back_btn = Button(text="메인으로", font_name="Nanum", size_hint=(None, None), size=('120dp', '50dp'), pos_hint={'center_x': 0.5, 'center_y': 0.2})
            back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
            self.add_widget(back_btn)
            return

        # 랜덤하게 문제 출제
        self.question_word = random.choice(current_word_list)
        target_lang = self.manager.target_lang
        
        # 문제 단어 (외국어)
        self.word_text = self.question_word.get(target_lang, "")
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # 상단: 문제 단어 및 발음 버튼
        top_layout = BoxLayout(size_hint_y=None, height='100dp', spacing=10)
        top_layout.add_widget(Label(text=self.word_text, font_size='40sp', color=(1,1,1,1))) # 외국어 단어는 기본 폰트(깨짐 주의, font_ttf에 해당 언어가 포함되어야 함)
        
        # [신규] 발음 듣기 버튼 추가
        speak_btn = Button(text="📢 듣기", font_name="Nanum", size_hint_x=None, width='100dp')
        speak_btn.bind(on_release=self.speak_word)
        top_layout.add_widget(speak_btn)
        main_layout.add_widget(top_layout)
        
        # 하단: 뜻 입력 및 확인
        self.answer_input = TextInput(hint_text="한국어 뜻을 입력하세요", font_name="Nanum", multiline=False, size_hint_y=None, height='60dp')
        main_layout.add_widget(self.answer_input)
        
        btn_layout = BoxLayout(size_hint_y=None, height='60dp', spacing=10)
        check_btn = Button(text="정답 확인", font_name="Nanum", background_color=(0, 0.7, 0, 1))
        check_btn.bind(on_release=self.check_answer)
        next_btn = Button(text="다음 단어", font_name="Nanum")
        next_btn.bind(on_release=lambda x: self.next_question())
        
        btn_layout.add_widget(check_btn)
        btn_layout.add_widget(next_btn)
        main_layout.add_widget(btn_layout)
        
        # 뒤로가기 버튼
        back_btn = Button(text="학습 종료", font_name="Nanum", size_hint_y=None, height='50dp', background_color=(0.5, 0.5, 0.5, 1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        main_layout.add_widget(back_btn)

        self.add_widget(main_layout)

    def speak_word(self, instance):
        # [신규] 발음하기 기능 구현
        if android_tts:
            lang_code = self.manager.target_lang
            # 안드로이드 TTS 언어 코드 설정 (예: en_US, vi_VN, zh_CN)
            if lang_code == 'en': android_lang = 'en_US'
            elif lang_code == 'vi': android_lang = 'vi_VN'
            elif lang_code == 'zh': android_lang = 'zh_CN'
            else: android_lang = 'en_US'
            
            android_tts.speak(self.word_text, android_lang)
        else:
            print("발음 기능은 안드로이드 기기에서만 작동합니다.")

    def check_answer(self, instance):
        user_answer = self.answer_input.text.strip()
        correct_answer = self.question_word.get('ko', "").strip()
        
        if user_answer == correct_answer:
            self.answer_input.background_color = (0, 1, 0, 0.2) # 초록색 배경 (정답)
        else:
            self.answer_input.background_color = (1, 0, 0, 0.2) # 빨간색 배경 (오답)
            self.answer_input.text = f"{user_answer} (오답! 정답: {correct_answer})"

class MyManager(ScreenManager):
    target_lang = 'en' # 기본 학습 언어

class MainApp(App):
    def build(self):
        # UTF-8 기반 기본 파일 및 예시 데이터 생성
        if not os.path.exists(STORE_FILE):
            example_data = {
                "초급": {
                    "1": [
                        {"ko": "안녕하세요", "en": "Hello", "vi": "Xin chào", "zh": "你好"},
                        {"ko": "감사합니다", "en": "Thank you", "vi": "Cảm ơn", "zh": "谢谢"},
                        {"ko": "사과", "en": "Apple", "vi": "Quả táo", "zh": "苹果"}
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
