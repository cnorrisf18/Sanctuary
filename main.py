import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.widget import Widget

class BoardGame(Widget):
    pass

class BoardApp(App):
    def build(self):
        return BoardGame()

if __name__ == '__main__':
    BoardApp().run()