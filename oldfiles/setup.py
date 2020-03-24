from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from classes import GUI
Builder.load_string("""
<MainScreen>:

<SettingsScreen>:
    BoxLayout:
        orientation : 'vertical'
        Label:
            text: 'Select the number of players'
        Button:
            text : '1'
            id: 1
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = '1'
                print(1)
        Button:
            text : '2'
            id : 2
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = '2'
                print(2)
        Button:
            text : '3'
            id : 3
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = '3'
                print(3)

        Button:
            text : '4'
            id : 4
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = '4'
                print(4)
            
<IntroScreen>:
""")

class MainScreen(Screen):
    pass

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        self.numplayers = 0
        super(Screen, self).__init__(**kwargs)
# Create the screen manager


sm = ScreenManager()
set = SettingsScreen(name='settings')
sm.add_widget(set)
for i in range(1, 5):
    sm.add_widget(GUI(name = str(i), pnum=i))
    print(f'created widget with name {str(i)}')

class TestApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()