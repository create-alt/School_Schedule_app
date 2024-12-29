from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from datetime import date, timedelta
import jpholiday  # 日本の祝日を判定するライブラリ

class Calendar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 7
        self.current_date = date.today()
        self.create_calendar(self.current_date.year, self.current_date.month)

    def create_calendar(self, year, month):
        self.clear_widgets()

        # 曜日のヘッダー
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for i, day in enumerate(days):
            color = (1, 0, 0, 1) if i == 0 else (0, 0, 1, 1) if i == 6 else (0, 0, 0, 1)
            self.add_widget(Label(text=day, size_hint=(1, 0.2), bold=True, color=color))

        # カレンダーの日付生成
        first_day = date(year, month, 1)
        start_weekday = first_day.weekday()
        start_weekday = (start_weekday + 1) % 7  # 日曜日を最初にする

        # 空白の日付（前月分）
        for _ in range(start_weekday):
            self.add_widget(Label(text=""))

        # 現在の月の日付
        days_in_month = (date(year, month + 1, 1) - timedelta(days=1)).day if month != 12 else 31
        today = date.today()

        for day in range(1, days_in_month + 1):
            current_day = date(year, month, day)
            # ボタンの色分け（祝日、土日、平日）
            if current_day == today:
                background_color = (0, 0, 0, 1)  # 今日の日付を黒色で強調
            elif current_day.weekday() == 5:  # 土曜日
                background_color = (0.7, 0.7, 1, 1)  # 青
            elif current_day.weekday() == 6:  # 日曜日
                background_color = (1, 0.7, 0.7, 1)  # 赤
            elif jpholiday.is_holiday(current_day):  # 祝日
                background_color = (1, 0.8, 0.8, 1)  # 薄い赤
            else:
                background_color = (0, 0, 0, 0.4)  # 平日

            # ボタン作成
            btn = Button(text=str(day), background_normal='', background_color=background_color)
            btn.bind(on_release=lambda btn, d=day: self.on_date_select(year, month, d))
            self.add_widget(btn)

    def on_date_select(self, year, month, day):
        selected_date = date(year, month, day)
        popup = Popup(
            title="Selected Date",
            content=Label(text=f"You selected: {selected_date}"),
            size_hint=(0.6, 0.4),
        )
        popup.open()


class CalendarApp(MDApp):
    def build(self):
        self.title = "カレンダーアプリ"
        layout = BoxLayout(orientation="vertical")
        self.calendar = Calendar()

        # ヘッダーナビゲーション
        nav_layout = BoxLayout(size_hint=(1, 0.15), padding=(10, 10))
        prev_button = Button(text="<", size_hint=(0.1, 1), font_size=20)
        prev_button.bind(on_release=self.go_previous_month)
        next_button = Button(text=">", size_hint=(0.1, 1), font_size=20)
        next_button.bind(on_release=self.go_next_month)

        # 現在の年月ラベルを強調表示
        current_month_label = Label(
            text=self.calendar.current_date.strftime("%B %Y"),
            font_size=28,
            color=(0, 0, 0, 1),
            bold=True,
            halign="center",
            size_hint=(0.8, 1),
        )
        self.current_month_label = current_month_label

        nav_layout.add_widget(prev_button)
        nav_layout.add_widget(current_month_label)
        nav_layout.add_widget(next_button)

        layout.add_widget(nav_layout)
        layout.add_widget(self.calendar)

        return layout

    def go_previous_month(self, instance):
        current_date = self.calendar.current_date
        if current_date.month == 1:
            self.calendar.current_date = date(current_date.year - 1, 12, 1)
        else:
            self.calendar.current_date = date(current_date.year, current_date.month - 1, 1)
        self.update_calendar()

    def go_next_month(self, instance):
        current_date = self.calendar.current_date
        if current_date.month == 12:
            self.calendar.current_date = date(current_date.year + 1, 1, 1)
        else:
            self.calendar.current_date = date(current_date.year, current_date.month + 1, 1)
        self.update_calendar()

    def update_calendar(self):
        self.calendar.create_calendar(
            self.calendar.current_date.year, self.calendar.current_date.month
        )
        self.current_month_label.text = self.calendar.current_date.strftime("%B %Y")


if __name__ == "__main__":
    CalendarApp().run()
