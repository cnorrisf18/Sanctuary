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
Config.set('graphics','resizable',1)

class GraphicsDrawer(Widget):
    #this will be used to draw everything
    def __init__(self, imageStr, **kwargs):
        super(GraphicsDrawer, self).__init__(**kwargs)

class Board(GraphicsDrawer):
    #the board, containing all the animal houses it can
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.small_animals = 0
        self.medium_animals = 0
        self.large_animals = 0
        self.total_animals = self.small_animals + self.large_animals + self.medium_animals
        self.max_animals = 20
        self.ambassadors = []
        self.hasbeenlabored = False
    def add_animals(self, animals):
        #animals should be a list of objects of the Animals class
        starting_total = self.total_animals
        for animal in animals:
            if animal.size == 'large':
                self.max_animals = 5
                self.large_animals += 1
            elif animal.size == 'medium' and self.large_animals == 0:
                self.max_animals = 10
                self.medium_animals += 1
            if self.total_animals > self.max_animals:
                self.total_animals = starting_total
                return 'Could not perform operation; You are putting too many animals in one plot!'
            self.draw_shelter(animal.size)
            self.ambassadors.append(animal)
    def draw_shelter(self, size):
        #this will draw a graphic on the screen that indicates the animal or the animal's shelter
        if size == 'small':
            pass
        elif size == 'medium':
            pass
        elif size == 'large':
            pass
    def labor(self, food, game):
        #food supply will be an object from the Feed class; it is a number representing the total amount of food available
        for animal in self.ambassadors:
            feed = animal.feed
            food.total_supply = food.total_supply - feed
            if food.total_supply < 0:
                game.end = True
                print('there is not enough food to feed all of the animals!')
                return 'lost'
            animal.feed()
        self.hasbeenlabored = True
    def reset(self):
        self.hasbeenlabored = False

class Animal(GraphicsDrawer):
    def __init__(self, size, name, species, **kwargs):
        super(Animal, self).__init__(**kwargs)
        self.size = size
        self.name = name
        self.species = species
        self.hasbeenfed = False
        self.feed = 0
        self.inspiration = 0
        self.vp = 0

    def calculate_stats(self):
        if self.size == 'large':
            self.inspiration = 6
            self.feed = 10
            self.vp = 10
        elif self.size == 'medium':
            self.inspiration = 4
            self.feed = 6
            self.vp = 6
        elif self.size == 'small':
            self.inspiration = 1
            self.feed = 1
            self.vp = 1

    def feed(self):
        self.hasbeenfed = True
    def reset(self):
        self.hasbeenfed = False