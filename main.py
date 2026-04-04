import traceback
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty

# KV 디자인 정의 (한 번에 로드)
Builder.load_string('''
<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        Label:
            text: "다국어 단어 마스터 2.0"
            font_size: '30sp'
            size_hint_y: 0.6
            # font_name: 'YourFont.ttf' # 폰트 파일이 있다면 주석 해제

        Button:
            text: "학습 시작하기"
            size_hint_y: 0.2
            background_color: 0.3, 0.3, 0.3, 1
            on_release: root.manager.current = 'language_select'

        Button:
            text: "단어 관리 (추가/삭제)"
            size_hint_y: 0.2
            background_color: 0.3, 0.3, 0.3, 1
            # 1번 문제 해결: 정확한 화면 이름 'word_manage' 호출
            on_release: root.manager.current = 'word_manage'

<LanguageSelectScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "목표 언어를 선택하세요"
            size_hint_y: 0.4
        
        Button:
            text: "English"
            size_hint_y: 0.2
            on_release: root.select_lang("English")
        Button:
            text: "Vietnamese"
            size_hint_y: 0.2
            on_release: root.select_lang("Vietnamese")
        Button:
            text: "Chinese"
            size_hint_y: 0.2
            on_release: root.select_lang("Chinese")

<StudyScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            # 2번 문제 해결: 데이터가 없을 때 표시될 텍스트
            text: root.display_text
            font_size: '20sp'
        Button:
            text: "메뉴로 돌아가기"
            size_hint_y: 0.2
            on_release: root.manager.current = 'menu'

<WordManageScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "단어 관리 화면"
        Button:
            text: "돌아가기"
            size_hint_y: 0.2
            on_release: root.manager.current = 'menu'
''')

# 1. 메인 메뉴 화면
class MenuScreen(Screen):
    pass

# 2. 언어 선택 화면
class LanguageSelectScreen(Screen):
    def select_lang(self, lang):
        app = App.get_running_app()
        app.target_lang = lang
        
        # 데이터 존재 여부 확인 로직
        if lang in app.word_db and app.word_db[lang]:
            self.manager.get_screen('study').display_text = f"{lang} 학습을 시작합니다."
        else:
            # 2번 증상 대응: 데이터가 없을 경우
            self.manager.get_screen('study').display_text = "학습할 단어가 없습니다.\n관리 화면에서 단어를 추가해주세요."
        
        self.manager.current = 'study'

# 3. 학습 화면
class StudyScreen(Screen):
    display_text = StringProperty("")

# 4. 단어 관리 화면 (1번 튕김 현상 방지를 위해 클래스 생성)
class WordManageScreen(Screen):
    pass

class WordMasterApp(App):
    target_lang = StringProperty("")
    # 임시 데이터베이스 (실제 구현 시 SQLite 등 연결 가능)
    word_db = ListProperty({"English": ["Apple"], "Vietnamese": [], "Chinese": []})

    def build(self):
        sm = ScreenManager()
        # 모든 화면을 등록해야 튕기지 않습니다.
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LanguageSelectScreen(name='language_select'))
        sm.add_widget(StudyScreen(name='study'))
        sm.add_widget(WordManageScreen(name='word_manage'))
        return sm

if __name__ == '__main__':
    try:
        WordMasterApp().run()
    except Exception:
        # 에러 발생 시 로그 출력
        traceback.print_exc()
