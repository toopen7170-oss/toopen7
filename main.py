import os
import sys
import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path

# [중요] 한글 폰트 및 경로 설정
try:
    base_path = os.path.dirname(__file__)
    resource_add_path(base_path)
    if os.path.exists("font.ttf"):
        LabelBase.register(name="Nanum", fn_regular="font.ttf")
except:
    pass

class WordGameApp(App):
    def build(self):
        # 1. 단어 데이터 (나중에 words.json에서 불러오게 확장 가능)
        self.word_data = [
            {"en": "teacher", "ko": "선생님"},
            {"en": "student", "ko": "학생"},
            {"en": "school", "ko": "학교"},
            {"en": "classroom", "ko": "교실"},
            {"en": "apple", "ko": "사과"},
            {"en": "banana", "ko": "바나나"}
        ]
        self.current_word = {}
        self.f_name = "Nanum" if os.path.exists("font.ttf") else None
        
        # 메인 레이아웃
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # 상단 제목
        self.main_layout.add_widget(Label(
            text="단어 맞히기 게임 2.0", 
            font_size='25sp', font_name=self.f_name, size_hint_y=0.1))
        
        # 단어 표시 라벨
        self.word_label = Label(text="", font_size='60sp', bold=True, size_hint_y=0.3)
        self.main_layout.add_widget(self.word_label)
        
        # 정답 버튼 그리드
        self.grid = GridLayout(cols=2, spacing=10, size_hint_y=0.5)
        self.main_layout.add_widget(self.grid)
        
        # 첫 문제 시작
        self.next_question()
        
        return self.main_layout

    def next_question(self, *args):
        # 다음 문제 세팅
        self.current_word = random.choice(self.word_data)
        self.word_label.text = self.current_word["en"]
        
        # 안드로이드 소리 읽기 (TTS 호출 시도)
        self.play_sound(self.current_word["en"])
        
        # 버튼 초기화 및 생성
        self.grid.clear_widgets()
        
        # 보기 생성 (정답 1개 + 오답 3개)
        options = [self.current_word["ko"]]
        others = [d["ko"] for d in self.word_data if d["ko"] != self.current_word["ko"]]
        options.extend(random.sample(others, 3))
        random.shuffle(options)
        
        for text in options:
            btn = Button(
                text=text, font_name=self.f_name, font_size='22sp',
                background_color=(0.1, 0.3, 0.5, 1)
            )
            btn.bind(on_release=self.check_answer) # 클릭 이벤트 연결
            self.grid.add_widget(btn)

    def check_answer(self, instance):
        # 정답 확인
        if instance.text == self.current_word["ko"]:
            instance.background_color = (0.2, 0.8, 0.2, 1) # 정답이면 초록색
            self.next_question() # 바로 다음 문제로
        else:
            instance.background_color = (0.8, 0.2, 0.2, 1) # 틀리면 빨간색

    def play_sound(self, text):
        # 안드로이드 자체 TTS 엔진 사용 시도
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
            Locale = autoclass('java.util.Locale')
            
            # 간단한 발음 로직 (안드로이드 전용)
            if not hasattr(self, 'tts'):
                self.tts = TextToSpeech(PythonActivity.mActivity, None)
            
            self.tts.setLanguage(Locale.US)
            self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None)
        except:
            print("소리 재생 실패 (안드로이드 환경이 아님)")

if __name__ == "__main__":
    WordGameApp().run()
