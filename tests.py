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
from classes import Feed, Animal, Board

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
    #testland.add_animals(alist) #this should return an error, due to adding more animals than is allowed
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
#test_classes()

with open('animals', 'r') as file:
    lines = [line.strip().split(',') for line in file]
    for animal in lines[1:]:
        #find info
        species = animal[0]
        size = animal [1]
        feed = animal [2]
        inspiration = animal[3]
        victorypoints = animal[4]
        print(species, size, feed, inspiration, victorypoints)