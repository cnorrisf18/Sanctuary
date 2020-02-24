import kivy

kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle
from random import randint
from kivy.config import Config
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

import random

Config.set('graphics', 'resizable', 1)


class GraphicsDrawer(Widget):
    # this will be used to draw everything
    def __init__(self, imageStr = "None",**kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.size = (Window.width * .002 * 25, Window.width * .002 * 25)
            self.rect_bg = Rectangle(source=imageStr, pos=self.pos, size=self.size)
            self.bind(pos=self.update_graphics_pos)
            self.x = self.center_x
            self.y = self.center_y
            self.pos = (self.x, self.y)
            self.rect_bg.pos = self.pos


    def update_graphics_pos(self, instance, value):
        self.rect_bg.pos = value


    def setSize(self, width, height):
        self.size = (width, height)

    def setPos(self, xpos, ypos):
        self.x = xpos
        self.y = ypos

class Board(GraphicsDrawer):
    # the board, containing all the animal houses it can
    def __init__(self, **kwargs):

        self.small_animals = 0
        self.medium_animals = 0
        self.large_animals = 0
        self.total_animals = 0
        self.max_animals = 20
        self.ambassadors = []
        self.hasbeenlabored = False
        super().__init__('farm.jpg', **kwargs)

    def add_animals(self, animals):
        # animals should be a list of objects of the Animals class
        starting_total = self.total_animals
        for animal in animals:
            if animal.asize == 'large':
                self.max_animals = 5
                self.large_animals += 1
            elif animal.asize == 'medium' and self.large_animals == 0:
                self.max_animals = 10
                self.medium_animals += 1
            elif animal.asize == 'medium':
                self.medium_animals += 1
            else:
                self.small_animals += 1
            #print(animal.asize)
            self.total_animals += 1
            #print(self.total_animals)
            if self.total_animals > self.max_animals:
                self.total_animals = starting_total
                raise ValueError('Could not perform operation; You are putting too many animals in one plot!')
            self.draw_shelter(animal.size)
            self.ambassadors.append(animal)

    def draw_shelter(self, asize):
        # this will draw a graphic on the screen that indicates the animal or the animal's shelter
        if asize == 'small':
            pass
        elif asize == 'medium':
            pass
        elif asize == 'large':
            pass

    def labor(self, food, game):
        # food supply will be an object from the Feed class; it is a number representing the total amount of food available
        for animal in self.ambassadors:
            feed = animal.feed
            print(f'It will take {feed} feed to feed {animal.aname}.')
            food.total_supply = food.total_supply - feed
            if food.total_supply < 0:
                game = True
                print('there is not enough food to feed all of the animals!')
                return game
            animal.givefood()
            print(f'Fed {animal.aname}.There is {food.total_supply} feed left.')
        self.hasbeenlabored = True
        return game
    def reset(self):
        for animal in self.ambassadors:
            animal.reset()
        self.hasbeenlabored = False

class Animal(GraphicsDrawer):
    def __init__(self, size = None, aname='', species= None, **kwargs):
        self.asize = str(size).lower()
        self.aname = str(aname)
        self.species = str(species).lower()
        self.hasbeenfed = False
        self.feed = 0
        self.inspiration = 0
        self.vp = 0
        super().__init__(**kwargs)

    def __str__(self):
        return self.aname

    def calculate_stats(self):
        if self.asize == 'large':
            self.inspiration = 6
            self.feed = 10
            self.vp = 10
        elif self.asize == 'medium':
            self.inspiration = 4
            self.feed = 6
            self.vp = 6
        elif self.asize == 'small':
            self.inspiration = 1
            self.feed = 1
            self.vp = 1

    def givefood(self):
        self.hasbeenfed = True

    def reset(self):
        self.hasbeenfed = False

class Feed(GraphicsDrawer):
    def __init__(self, **kwargs):
        self.total_supply = 0
        super().__init__(**kwargs)
    def buy_feed(self, money):
        purchased_feed = money // 2
        self.total_supply = self.total_supply + purchased_feed
        return purchased_feed

class Workforce(GraphicsDrawer):
    def __init__(self, numplayers, **kwargs):
        self.players = numplayers
        self.volunteers = 0
        self.employees = 0
        super().__init__(**kwargs)
    def calculate_labor_for_upkeep(self):
        return self.players*2 + self.volunteers//5 + self.employees
    def calculate_labor_for_actions(self):
        return self.players*2 + self.volunteers//5 + self.emplyees//2

    def hire_employees(self, numactions):
        self.employees += int(numactions)
        return (f'Hired {numactions} employees')
    def recruit_volunteers(self, numactions):
        total_recruits = 0
        for n in range(1,int(numactions)+1):
            roll = random.randint(1, 20)   #might replace this with a cool dice rolling graphic later
            rnum = 0
            if 1 <= roll <= 5:
                rnum = 2
            elif 6 <= roll <= 10:
               rnum = 4
            elif 11 <= roll <= 15:
                rnum = 6
            elif 16 <= roll <= 20:
                rnum = 10
            total_recruits += rnum
            self.volunteers += rnum
            print(f'Rolled a {roll}, recruited {rnum} volunteers')
        print(f'Recruited {total_recruits} volunteers in total')

class Players(GraphicsDrawer):
    def __init__(self, playernum, **kwargs):
        self.players = int(playernum)
        self.inspiration = 0
        self.total_money = 0
        self.supporters = 0
        self.total_sanctuary_animals = []
        self.boardlist = [Board() for player in range(0,playernum)]
        super().__init__(**kwargs)
    def gain_inspiration(self):
        #total_sanctuary_animals should be a list of objects of the Animals class
        self.inspiration += [animal.inspiration for animal in self.total_sanctuary_animals]
    def spend_money(self, money):
        startcash = self.total_money
        self.total_money = self.total_money - money
        if self.total_money <= 0:
            #implement this with feed!!!!
            print('Not enough money to make purchase!')
            self.total_money = startcash
    def earn_money(self, money):
        self.total_money = self.total_money + money
    def earn_supporters(self, num):
        self.supporters += int(num)
    def get_donations_from_supporters(self):
        self.total_money += self.supporters
    def rescue(self, animal):
        self.total_sanctuary_animals.append(animal)
    def gain_land(self):
        self.spend_money(20)
        self.boardlist.append(Board())
#
# class SetUp(BoxLayout, Screen):
#     def __init__(self, **kwargs):
#         super(BoxLayout, self).__init__(**kwargs)
#         self.font_size = 50
#         self.orientation = "vertical"
#         self.buttons = []
#         self.pnum = 0
#         self.label = Label(text = "How Many Players?")
#         self.add_widget(self.label)
#         for i in range(1,5):
#             button = Button(text = str(i), font_size = self.font_size)
#             button.bind(on_press= self.buttonpressed)
#             self.add_widget(button)
#             self.buttons.append(button)
#     def buttonpressed(self, instance):
#         self.pnum = int(instance.text)
#         self.stop_game()
#     def stop_game(self):
#         App.get_running_app().stop()
#
# class SetupApp(App):
#
#     def build(self):
#         game = Screen()
#         table_screen = SetUp()
#         pnum = table_screen.pnum
#         game.add_widget(table_screen)
#         return game, pnum


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
        playernum = 1
        for i in range(1, playernum+1):
            board = Board()
            self.boardlist.append(board)
            self.add_widget(board)

class MainApp(App):
    def build(self):

        return GUI()