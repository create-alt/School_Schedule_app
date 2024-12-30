from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

# 画面1
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        label = Label(text="メイン画面", font_size=24)

        button = Button(text="次の画面へ", font_size=20, size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        button.bind(on_press=self.go_to_next_screen)  # ボタン押下時の動作を設定

        layout.add_widget(label)
        layout.add_widget(button)
        self.add_widget(layout)

    def go_to_next_screen(self, instance):
        self.manager.current = 'second'  # 'second'画面に遷移

# 画面2
class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        label = Label(text="セカンド画面", font_size=24)

        button = Button(text="メイン画面に戻る", font_size=20, size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        button.bind(on_press=self.go_to_main_screen)  # ボタン押下時の動作を設定

        layout.add_widget(label)
        layout.add_widget(button)
        self.add_widget(layout)

    def go_to_main_screen(self, instance):
        self.manager.current = 'main'  # 'main'画面に遷移

# アプリケーション本体
class ScreenSwitchApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))  # 'main'画面を追加
        sm.add_widget(SecondScreen(name='second'))  # 'second'画面を追加
        return sm

if __name__ == "__main__":
    ScreenSwitchApp().run()
