import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

class BoardGame(Widget):
    pass

class RootWidget(BoxLayout):
    pass

class CustomLayout(FloatLayout):
    pass


class BoardApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main_':
    BoardApp().run()

