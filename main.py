import os
import sys
import traceback
from plyer import share  # 공유 기능을 위해 추가

# --- [최상단] 에러 로그 및 안드로이드 공유 설정 ---
def logger(type, value, tb):
    # 1. 임시로 내부 저장소에 로그 기록
    log_content = "".join(traceback.format_exception(type, value, tb))
    # 앱 내부 경로에 에러 로그 생성
    temp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "error_log.txt")
    
    try:
        with open(temp_path, "w", encoding='utf-8') as f:
            f.write("--- PT1 Manager Error Log ---\n")
            f.write(log_content)
        
        # 2. 안드로이드 공유 창 띄우기 (다운로드 폴더 저장 및 카톡 전송 가능)
        share.share(temp_path)
    except Exception as e:
        print(f"Log sharing failed: {e}")

# 시스템 예외 발생 시 위 함수 실행
sys.excepthook = logger

# --- Kivy 앱 로직 시작 ---
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty

# KV 디자인 정의
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

        Button:
            text: "학습 시작하기"
            size_hint_y: 0.2
            background_color: 0.3, 0.3, 0.3, 1
            on_release: root.manager.current = 'language_select'

        Button:
            text: "단어 관리 (추가/삭제)"
            size_hint_y: 0.2
            background_color: 0.3, 0.3, 0.3, 1
            # 1번 문제 해결: 정확한 화면 이름 'word_manage' 매칭
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
            # 2번 문제 해결: 선택된 언어에 단어가 없을 때 메시지 표시
            text: root.display_text
            font_size: '18sp'
            halign: 'center'
        Button:
            text: "메뉴로 돌아가기"
            size_hint_y: 0.2
            on_release: root.manager.current = 'menu'

<WordManageScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: "단어 관리 화면\\n(여기에 단어 추가 로직을 구현하세요)"
            halign: 'center'
        Button:
            text: "돌아가기"
            size_hint_y: 0.2
            on_release: root.manager.current = 'menu'
''')

class MenuScreen(Screen):
    pass

class LanguageSelectScreen(Screen):
    def select_lang(self, lang):
        app = App.get_running_app()
        app.target_lang = lang
        
        # 2번 문제 해결: 데이터베이스(word_db)에서 단어 유무 확인
        if lang in app.word_db and app.word_db[lang]:
            self.manager.get_screen('study').display_text = f"[{lang}] 학습 화면입니다."
        else:
            self.manager.get_screen('study').display_text = "학습할 단어가 없습니다.\\n관리 화면에서 단어를 추가해주세요."
        
        self.manager.current = 'study'

class StudyScreen(Screen):
    display_text = StringProperty("")

class WordManageScreen(Screen):
    pass

class WordMasterApp(App):
    target_lang = StringProperty("")
    # 샘플 데이터베이스 (학습할 단어가 있는지 체크용)
    word_db = ListProperty({"English": ["Apple"], "Vietnamese": [], "Chinese": []})

    def build(self):
        sm = ScreenManager()
        # 모든 Screen 클래스를 등록해야 전환 시 튕기지 않습니다.
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LanguageSelectScreen(name='language_select'))
        sm.add_widget(StudyScreen(name='study'))
        sm.add_widget(WordManageScreen(name='word_manage'))
        return sm

if __name__ == '__main__':
    WordMasterApp().run()
