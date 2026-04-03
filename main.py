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
from kivy.core.text import LabelBase

# [1단계] 폰트 등록 (파일 목록에 있는 font.ttf 사용)
# 모든 UI 요소에 이 폰트를 적용해야 1번 사진의 깨짐 현상이 해결됩니다.
LabelBase.register(name="Nanum", fn_regular="font.ttf")

STORE_FILE = 'words.json'

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 상단 타이틀
        layout.add_widget(Label(text="프리스톤테일 관리 시스템", font_name="Nanum", font_size='25sp', size_hint_y=None, height='80dp'))
        
        # 검색창 (전체 검색 기능)
        search_layout = BoxLayout(size_hint_y=None, height='50dp', spacing=10)
        self.search_input = TextInput(hint_text="계정, 캐릭터, 아이템 검색...", font_name="Nanum", multiline=False)
        search_btn = Button(text="검색", font_name="Nanum", size_hint_x=0.3)
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(search_btn)
        layout.add_widget(search_layout)

        # 메뉴 버튼들
        btns = [("계정 생성/관리", "admin"), ("언어 설정 (학습)", "lang_select")]
        for text, target in btns:
            btn = Button(text=text, font_name="Nanum", size_hint_y=None, height='60dp')
            btn.bind(on_release=lambda x, t=target: setattr(self.manager, 'current', t))
            layout.add_widget(btn)
        
        self.add_widget(layout)

class LangSelect(Screen):
    # [2단계] 언어 선택 화면 (2번 사진 대응)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=15)
        layout.add_widget(Label(text="목표 언어를 선택하세요", font_name="Nanum", font_size='20sp'))
        
        langs = [("English", "en"), ("Vietnamese", "vi"), ("Chinese", "zh"), ("Japanese", "ja")]
        for name, code in langs:
            # 버튼에도 반드시 font_name을 적용하여 깨짐 방지
            btn = Button(text=name, font_name="Nanum", size_hint_y=None, height='60dp')
            layout.add_widget(btn)
        
        back_btn = Button(text="메인으로", font_name="Nanum", size_hint_y=None, height='50dp', background_color=(0.5, 0.5, 0.5, 1))
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(back_btn)
        self.add_widget(layout)

class AdminScreen(Screen):
    """ 계정 및 세부 캐릭터 내역 관리 (수정, 저장, 추가, 삭제) """
    def on_enter(self):
        self.refresh()

    def refresh(self):
        self.clear_widgets()
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # 스크롤 뷰를 통한 입력 필드 배치 (1번 사진의 폰트 깨짐 해결을 위해 모든 곳에 Nanum 적용)
        scroll = ScrollView()
        input_layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=[0, 10])
        input_layout.bind(minimum_height=input_layout.setter('height'))

        fields = [
            ('level', "레벨"), ('job', "직업"), ('name', "이름"),
            ('weapon', "양손/한손무기"), ('armor', "갑옷/로브"), ('shield', "방패"),
            ('armlet', "암릿 (누락수정)"), ('gloves', "장갑"), ('boots', "부츠"),
            ('amulet', "아뮬렛"), ('ring', "링"), ('shelton', "쉘텀")
        ]
        
        self.inputs = {}
        for key, hint in fields:
            # 힌트 텍스트와 입력 텍스트 모두 폰트 지정
            ti = TextInput(hint_text=hint, font_name="Nanum", multiline=False, size_hint_y=None, height='45dp')
            self.inputs[key] = ti
            input_layout.add_widget(ti)

        scroll.add_widget(input_layout)
        main_layout.add_widget(scroll)

        # 하단 버튼 바 (저장, 삭제, 뒤로가기)
        btn_box = BoxLayout(size_hint_y=None, height='60dp', spacing=10)
        
        save_btn = Button(text="저장", font_name="Nanum", background_color=(0, 0.7, 0, 1))
        save_btn.bind(on_release=self.save_data)
        
        del_btn = Button(text="삭제", font_name="Nanum", background_color=(0.8, 0, 0, 1))
        del_btn.bind(on_release=self.delete_data)
        
        back_btn = Button(text="닫기", font_name="Nanum")
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))

        btn_box.add_widget(save_btn)
        btn_box.add_widget(del_btn)
        btn_box.add_widget(back_btn)
        
        main_layout.add_widget(btn_box)
        self.add_widget(main_layout)

    def save_data(self, instance):
        # 데이터 저장 로직 (UTF-8 인코딩 필수)
        try:
            with open(STORE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except: data = []

        new_entry = {k: v.text for k, v in self.inputs.items()}
        data.append(new_entry)

        with open(STORE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("데이터 저장 완료")

    def delete_data(self, instance):
        # 입력 필드 초기화 (삭제 기능)
        for ti in self.inputs.values():
            ti.text = ""

class MyManager(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        # UTF-8 기반 기본 파일 생성
        if not os.path.exists(STORE_FILE):
            with open(STORE_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)

        sm = MyManager()
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(LangSelect(name='lang_select'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm

if __name__ == "__main__":
    MainApp().run()
