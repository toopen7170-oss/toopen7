import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.text import LabelBase

# 폰트 등록
try:
    LabelBase.register(name="Nanum", fn_regular="font.ttf")
except:
    pass

# 단어 데이터 대폭 추가 예시
WORD_DATA = [
    {"en": "teacher", "ko": "선생님"}, {"en": "student", "ko": "학생"},
    {"en": "school", "ko": "학교"}, {"en": "classroom", "ko": "교실"},
    {"en": "apple", "ko": "사과"}, {"en": "banana", "ko": "바나나"},
    {"en": "library", "ko": "도서관"}, {"en": "book", "ko": "책"},
    {"en": "computer", "ko": "컴퓨터"}, {"en": "pencil", "ko": "연필"},
    {"en": "water", "ko": "물"}, {"en": "bread", "ko": "빵"},
    {"en": "friend", "ko": "친구"}, {"en": "family", "ko": "가족"},
    {"en": "house", "ko": "집"}, {"en": "car", "ko": "자동차"}
]

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        # 버튼 디자인 개선
        levels = [("기초 (4칸)", 4), ("초급 (6칸)", 6), ("중급 (9칸)", 9), ("고급 (16칸)", 16)]
        for text, size in levels:
            btn = Button(text=text, font_name="Nanum", font_size='22sp', 
                         background_normal='', background_color=(0.2, 0.2, 0.2, 1))
            btn.bind(on_release=lambda x, s=size: self.go_to_game(s))
            layout.add_widget(btn)
        self.add_widget(layout)

    def go_to_game(self, size):
        self.manager.grid_size = size
        self.manager.current = 'game'

class GameScreen(Screen):
    def on_enter(self):
        self.hearts = 5
        self.init_game()

    def init_game(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 하트 표시
        self.heart_label = Label(text="❤️" * self.hearts, font_size='25sp', size_hint_y=0.1)
        layout.add_widget(self.heart_label)

        # 문제
        self.target = random.choice(WORD_DATA)
        layout.add_widget(Label(text=self.target['en'], font_size='45sp', bold=True, size_hint_y=0.2))

        # 그리드 설정 (9칸, 16칸 최적화)
        size = self.manager.grid_size
        col_count = 2 if size <= 6 else (3 if size == 9 else 4)
        grid = GridLayout(cols=col_count, spacing=5, size_hint_y=0.6)
        
        options = [self.target['ko']]
        while len(options) < size:
            wrong = random.choice(WORD_DATA)['ko']
            if wrong not in options: options.append(wrong)
        random.shuffle(options)

        # 글자 크기 자동 조절 (칸이 많아지면 작게)
        f_size = '18sp' if size <= 6 else ('14sp' if size == 9 else '11sp')

        for opt in options:
            btn = Button(text=opt, font_name="Nanum", font_size=f_size)
            btn.bind(on_release=self.check_answer)
            grid.add_widget(btn)
            
        layout.add_widget(grid)
        self.add_widget(layout)

    def check_answer(self, instance):
        if instance.text == self.target['ko']:
            instance.background_color = (0, 1, 0, 1)
            Clock.schedule_once(lambda dt: self.init_game(), 0.5)
        else:
            instance.background_color = (1, 0, 0, 1)
            self.hearts -= 1
            self.heart_label.text = "❤️" * self.hearts
            if self.hearts <= 0: self.manager.current = 'menu'

class MyManager(ScreenManager):
    grid_size = 4

class MainApp(App):
    def build(self):
        sm = MyManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == "__main__":
    MainApp().run()
