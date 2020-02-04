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

Config.set('graphics', 'resizable', 1)


class GraphicsDrawer(Widget):
    # this will be used to draw everything
    def __init__(self, imageStr = "None",**kwargs):
        super(GraphicsDrawer, self).__init__(**kwargs)
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
        super(Board, self).__init__('farm.jpg',**kwargs)
        self.small_animals = 0
        self.medium_animals = 0
        self.large_animals = 0
        self.total_animals = 0
        self.max_animals = 20
        self.ambassadors = []
        self.hasbeenlabored = False

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
            food.total_supply = food.total_supply - feed
            if food.total_supply < 0:
                game.end = True
                print('there is not enough food to feed all of the animals!')
                return 'lost'
            animal.givefood()
        self.hasbeenlabored = True

    def reset(self):
        for animal in self.ambassadors:
            animal.reset()
        self.hasbeenlabored = False


class Animal(GraphicsDrawer):
    def __init__(self, size = None, name= None, species= None, **kwargs):
        super(Animal, self).__init__(**kwargs)
        self.asize = str(size).lower()
        self.name = str(name)
        self.species = str(species).lower()
        self.hasbeenfed = False
        self.feed = 0
        self.inspiration = 0
        self.vp = 0

    #def __str__(self):
     #    return self.name

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
        super(Feed, self).__init__(**kwargs)
        self.total_supply = 0

    def buy_feed(self, money):
        purchased_feed = money // 2
        self.total_supply = self.total_supply + purchased_feed
        return purchased_feed


class Money(GraphicsDrawer):
    def __init__(self, **kwargs):
        super(Money, self).__init__(**kwargs)
        self.total_money = 0

    def spend_money(self, money):
        self.total_money = self.total_money - money



def test_classes():
    feed = Feed()
    feed.buy_feed(100)
    testcow = Animal('large', 'betsy', 'cow')
    testcow.calculate_stats()
    alist = [testcow]
    testland = Board()
    for n in range(1,10):
        testchicken = Animal('small', f'chicken {str(n)}', 'chicken')
        testchicken.calculate_stats()
        alist.append(testchicken)
    print(testland.ambassadors)
    testland.add_animals(alist) #this should return an error, due to adding more animals than is allowed
    print(testland.ambassadors)
    blist = []
    for n in range(1,4):
        testhorse = Animal('large', f'horse {str(n)}', 'horse')
        testhorse.calculate_stats()
        blist.append(testhorse)
    testland.add_animals(blist)    #this should be allowed
    testland.labor(feed,game=None) #this should be allowed
    print(testland.hasbeenlabored)
    for animal in blist:
        print(animal.hasbeenfed)
    testland.reset()
    print(testland.labor(feed, game=None))   #this should not be allowed; now there is not enough feed for the horses


    print(testland.ambassadors)
test_classes()

