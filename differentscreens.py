from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from classes import GUI, MainApp, Board
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
                root.manager.current = 'main'
                print(1)
                root.get_player_num(1)
        Button:
            text : '2'
            id : 2
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'main'
                root.get_player_num(2)
                print(2)
        Button:
            text : '3'
            id : 3
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'main'
                print(3)
                root.get_player_num(3)
        Button:
            text : '4'
            id : 4
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'main'
                print(4)
                root.get_player_num(4)
            
""")

class MainScreen(Screen):
    pass

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        self.numplayers = 0
        super(Screen, self).__init__(**kwargs)
    def get_player_num(self,num):
        global playernum
        playernum = int(num)
        self.numplayers = int(num)
# Create the screen manager
class GUI(Screen):
    #the main game class that things will be drawn onto
    boardlist = []
    _disabled_count = 0
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        l = Label(text = 'Sanctuary')
        # l.x = Window.width/2 -l.width/2
        # l.y = Window.height*.8
        #self.add_widget(l)
        self.add_boards()
        xpos = 250
        ypos = 250
        i = 1
        for board in self.boardlist:
            board.setPos(xpos, ypos)
            if i == 3:
                ypos += 255
                xpos = 250
            else:
                xpos += 255
            i += 1
    def add_boards(self):
        global playernum
        for i in range(1, playernum+1):
            board = Board()
            self.boardlist.append(board)
            self.add_widget(board)

sm = ScreenManager()
set = SettingsScreen(name='settings')
sm.add_widget(set)
print(set.numplayers)
#sm.add_widget(GUI(name = 'main'))
class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()