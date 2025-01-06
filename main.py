import json
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
import os

# 日本語フォントを登録
LabelBase.register(name="Japanese", fn_regular="C:/Windows/Fonts/yuminl.ttf")  # フォントパスを適切に変更してください

# 保存するファイル名
DATA_FILE = "./timetable_data.json"
SCHEDULE_FILE = "./schedule_data.json"  # 各教科の予定を保存するファイル


class InitSettingScreen(Screen):
    """
    初期設定として、使用する時間割を設定する画面
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 時間割設定がされていない場合は初期設定用画面に進む
        self.timetable_data = self.load_timetable_data()
        self.days = ["月", "火", "水", "木", "金"]

        # メインのレイアウト
        layout = GridLayout(cols=1, padding=[10,150,0,350], spacing=10)

        # 時間割表示用のグリッド
        self.grid = GridLayout(cols=6, size_hint_y=None, row_force_default=True, row_default_height=40)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        # ヘッダー行
        self.grid.add_widget(Label(text="時間/曜日", size_hint_x=None, width=100, font_name="Japanese"))
        for day in self.days:
            self.grid.add_widget(Label(text=day, size_hint_x=None, width=100, font_name="Japanese"))

        # 時間割のセルを作成
        for i in range(4):
            self.grid.add_widget(Label(text=f"{i+1}限目", size_hint_x=None, width=100, font_name="Japanese"))
            for j in range(5):
                text = self.timetable_data[i][j]  # データを取得
                cell = TextInput(text=text, multiline=False, font_name="Japanese", halign="center")
                cell.bind(on_text_validate=lambda instance, x=i, y=j: self.save_timetable(x, y, instance.text))
                self.grid.add_widget(cell)

        layout.add_widget(self.grid)

        # 予定表示用ボタン
        button = Button(text="時間割を確定する", size_hint_y=None, height=30, font_name="Japanese")
        button.bind(on_press=self.save_timetable_data)
        layout.add_widget(button)

        self.add_widget(layout)

    def save_timetable(self, row, col, text):
        """セルに入力された値を保存する"""
        self.timetable_data[row][col] = text

        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.timetable_data, file, ensure_ascii=False, indent=4)

    def save_timetable_data(self, instance):
        """時間割データをファイルに保存する"""
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.timetable_data, file, ensure_ascii=False, indent=4)

        self.manager.current = 'main'  # 'main'画面に遷移

    def load_timetable_data(self):
        """時間割データをファイルから読み込む"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
            
        return [[""] * 5 for _ in range(4)]
        
class ScheduleScreen(Screen):
    """特定教科の予定を編集する画面"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, padding=10, spacing=10)
        self.add_widget(self.layout)
        self.subject = None
        self.schedule_data = self.load_schedule_data()

    def load_schedule_data(self):
        """予定データをファイルから読み込む"""
        if os.path.exists(SCHEDULE_FILE):
            with open(SCHEDULE_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def save_schedule_data(self):
        """予定データをファイルに保存する"""
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as file:
            json.dump(self.schedule_data, file, ensure_ascii=False, indent=4)

    def on_pre_enter(self):
        """画面遷移前にUIを更新"""
        self.layout.clear_widgets()
        if not self.subject:
            return

        # 予定表示
        self.layout.add_widget(Label(text=f"{self.subject} の予定", font_name="Japanese", size_hint_y=None, height=30))
        schedule_text = self.schedule_data.get(self.subject, "")
        self.text_input = TextInput(text=schedule_text, multiline=True, font_name="Japanese")
        self.layout.add_widget(self.text_input)

        # 保存ボタン
        save_button = Button(text="保存", size_hint_y=None, height=40, font_name="Japanese")
        save_button.bind(on_press=self.save_schedule)
        self.layout.add_widget(save_button)

        # 戻るボタン
        back_button = Button(text="戻る", size_hint_y=None, height=40, font_name="Japanese")
        back_button.bind(on_press=self.go_to_main_screen)
        self.layout.add_widget(back_button)

    def go_to_main_screen(self, ins):
        self.manager.current = 'main'

    def save_schedule(self, _):
        """入力内容を保存"""
        self.schedule_data[self.subject] = self.text_input.text
        self.save_schedule_data()
        popup = Popup(title="saved", content=Label(text="予定を保存しました", font_name="Japanese"),
                      size_hint=(0.5, 0.5))
        popup.open()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timetable_data = self.load_timetable_data()
        self.days = ["月", "火", "水", "木", "金"]

        # メインのレイアウト
        self.layout = BoxLayout(pos_hint={"center_x": 0.5, "center_y": 0.7}, spacing=15, size_hint_max_x = 800, size_hint_max_y = 600)
        self.layout.add_widget(self.create_timetable_grid())
        self.add_widget(self.layout)

        button = Button(
            text="時間割を編集する",
            font_name="Japanese",
            size_hint=(None, None),
            width=800,
            height=40,
            pos_hint={"center_x": 0.5, "center_y": 0.35}  # 水平方向に中央配置
        )
        button.bind(on_press=self.go_to_initsetting_screen)
        self.add_widget(button)

    def create_timetable_grid(self):
        """時間割グリッドを作成して中央配置"""
        self.grid_layout = GridLayout(cols=6, spacing=5, size_hint=(None, None))
        self.grid_layout.size_hint_max_x = 800  # 最大幅の設定
        self.grid_layout.size_hint_max_y = 450  # 最大高さの設定
        self.grid_layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.update_ui()
        return self.grid_layout

    def on_pre_enter(self):
        """画面遷移時にデータを再ロードして更新"""
        self.timetable_data = self.load_timetable_data()
        self.update_ui()

    def update_ui(self):
        """UIを更新する"""
        self.grid_layout.clear_widgets()

        # ヘッダー行
        self.grid_layout.add_widget(Label(text="時間/曜日", size_hint_x=None, width=120, font_name="Japanese"))
        for day in self.days:
            self.grid_layout.add_widget(Label(text=day, size_hint_x=None, width=120,padding = [0,0,0,20] ,font_name="Japanese"))

        # 時間割のセルを作成
        for i in range(4):  # 限目
            self.grid_layout.add_widget(Label(text=f"{i + 1}限目", size_hint_x=None, width=120, font_name="Japanese"))
            for j in range(5):  # 各曜日
                text = self.timetable_data[i][j]
                cell = Button(text=text, font_name="Japanese", size_hint=(None, None), width=120, height=40)
                cell.bind(on_press=lambda _, x=i, y=j: self.show_schedule(x, y))
                self.grid_layout.add_widget(cell)

    def show_schedule(self, x, y):
        """予定編集画面に遷移"""
        subject = self.timetable_data[x][y]
        if not subject:
            popup = Popup(title="error", content=Label(text="教科が設定されていません", font_name="Japanese"),
                          size_hint=(0.5, 0.5))
            popup.open()
            return
        schedule_screen = self.manager.get_screen('schedule')
        schedule_screen.subject = subject
        self.manager.current = 'schedule'

    def go_to_initsetting_screen(self, instance):
        self.manager.current = 'init_setting'

    def load_timetable_data(self):
        """時間割データをファイルから読み込む"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return [[""] * 5 for _ in range(4)]


class TimetableApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        return sm


class SchoolScheduleApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ScheduleScreen(name='schedule'))
        sm.add_widget(InitSettingScreen(name='init_setting'))
        return sm


if __name__ == "__main__":
    SchoolScheduleApp().run()
