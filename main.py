import json
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
import os

# 日本語フォントを登録
LabelBase.register(name="Japanese", fn_regular="C:/Windows/Fonts/yuminl.ttf")  # フォントパスを適切に変更してください

# 保存するファイル名
DATA_FILE = "./timetable_data.json"


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
        layout = GridLayout(cols=1, padding=10, spacing=10)

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
        
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 時間割設定がされていない場合は初期設定用画面に進む
        self.timetable_data = self.load_timetable_data()
        self.days = ["月", "火", "水", "木", "金"]

        # メインのレイアウト
        layout = GridLayout(cols=1, padding=10, spacing=10)

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
                cell = Button(text=text,font_name="Japanese")
                cell.bind(on_text_validate=lambda instance, x=i, y=j: self.save_timetable(x, y, instance.text))
                self.grid.add_widget(cell)

        layout.add_widget(self.grid)


        # 時間割変更用ボタン
        button = Button(text="時間割を変更する", size_hint_y=None, height=30, font_name="Japanese")
        button.bind(on_press=self.go_to_init_setting)
        layout.add_widget(button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        """画面遷移時にデータを再ロードして更新"""
        self.timetable_data = self.load_timetable_data()
        self.update_ui()

    def update_ui(self):
        """UIを更新する"""
        self.grid.clear_widgets()

        # ヘッダー行
        self.grid.add_widget(Label(text="時間/曜日", size_hint_x=None, width=100, font_name="Japanese"))
        for day in self.days:
            self.grid.add_widget(Label(text=day, size_hint_x=None, width=100, font_name="Japanese"))

        # 時間割のセルを作成
        for i in range(4):
            self.grid.add_widget(Label(text=f"{i+1}限目", size_hint_x=None, width=100, font_name="Japanese"))
            for j in range(5):
                text = self.timetable_data[i][j]  # データを取得
                cell = Button(text=text, font_name="Japanese")
                self.grid.add_widget(cell)

    def show_schedule(self, x, y):
        """
        押下した欄の教科の予定をすべて表示する
        """
        pass

    def save_timetable_schedule(self, x, y, text):
        """
        押下した欄の教科の予定を保存する
        """
        pass

    def load_timetable_data(self):
        """時間割データをファイルから読み込む"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
            
        return [[""] * 5 for _ in range(4)]
    
    def go_to_init_setting(self, instance):
        self.manager.current = 'init_setting'

# アプリケーション本体
class ScreenSwitchApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(MainScreen(name='main'))  # 'second'画面を追加
        sm.add_widget(InitSettingScreen(name='init_setting'))  # 'main'画面を追加
        
        return sm

if __name__ == "__main__":
    ScreenSwitchApp().run()
