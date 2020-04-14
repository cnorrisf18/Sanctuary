import kivy
from kivy.uix.floatlayout import FloatLayout
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
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
import random

Config.set('graphics', 'resizable', 1)


class CustomButton(ButtonBehavior, Image):
    def __init__(self, imageStr, name, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.source = imageStr
        self.name = name
        self.imageStr = imageStr
        self.text = 'hi'
    def on_press(self):
        if self.imageStr == 'images/farm.jpg':
            self.source = 'images/farmpressed.jpg'
        else:
            self.source = self.imageStr
            self.text = self.name

    def on_release(self):
        self.source = self.imageStr
        self.text = ''
class GraphicsDrawer(Widget):
    # this will be used to draw everything
    def __init__(self, imageStr = "None", name = None, **kwargs):
        super().__init__(**kwargs)
        #imageStr = 'images/farm.jpg'
        self.imageStr = imageStr
        self.name = name
        #print(f'imageStr for GRAPHICSDRAWER is {imageStr}')
        with self.canvas:
             #if imageStr == 'images/farm.jpg':
             #background_normal = imageStr
            self.rect_bg = CustomButton(self.imageStr, self.name, pos = self.pos, size = self.size)
            #self.image = Image(source = imageStr, allow_stretch = True, pos = self.rect_bg.pos)
            #self.rect_bg.add_widget(self.image)

            #self.rect_bg.bind(on_release = self.callback)
            #else:
            #print(self.imageStr)
            #self.rect_bg = Rectangle(source = self.imageStr, pos = self.pos, size = self.size)
            #self.rect_bg = Button(background_normal = self.imageStr, pos = self.pos, size=self.size, on_press = self.callback)

            self.rect_bg.pos = self.pos
            self.add_widget(self.rect_bg)
            if imageStr == 'images/farm.jpg':
                self.bind(pos=self.update_graphics_pos, size = self.update_graphics_size_board)
                #self.rect_bg.background_down = 'images/farmpressed.jpg'
                #self.rect_bg.bind(on_press=lambda x: self.rect_bg.setattr('source','images/farmpressed'))
                #self.rect_bg.bind(on_release =lambda x: self.rect_bg.setattr('source',self.imageStr))
                #self.image.bind(pos=self.update_graphics_pos, size = self.update_graphics_size_board)
            else:
                self.bind(pos=self.update_graphics_pos, size = self.update_graphics_size)
                #self.rect_bg.background_down = self.name
                #self.image.bind(pos=self.update_graphics_pos, size = self.update_graphics_size)

    def callback(self, event):
        print('button pressed')
    #def board_callback(self, event):


    def update_graphics_size_board(self, root, value):
        width, height = root.width/3, root.height/3
        #print(f'updating size{width, height}')
        self.rect_bg.size = (width,height)

    def update_graphics_pos(self, root, value):

        self.rect_bg.pos = self.pos

        #print(self.rect_bg.pos)
    def update_graphics_size(self, root, value):
        self.rect_bg.size = value

    def setSize(self, width, height):
        self.size = (width, height)

    def setPos(self, xpos, ypos):
        self.pos = (xpos,ypos)


class Board(GraphicsDrawer):
    # the board, containing all the animal houses it can
    def __init__(self, root, imageStr='None', **kwargs):

        self.small_animals = 0
        self.medium_animals = 0
        self.large_animals = 0
        self.total_animals = 0
        self.max_animals = 20
        self.ambassadors = []
        self.hasbeenlabored = False
        self.root = root


        super().__init__(imageStr = imageStr)

    def __str__(self):
        return  "A board"



    def add_animals(self, animals):
        #print(animals)
        # animals should be a list of objects of the Animals class
        starting_total = self.total_animals
        for animal in animals:
            self.add_widget(animal)
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
            self.ambassadors.append(animal)
            self.draw_shelter(animal)



    def draw_shelter(self, animal):
        # this will draw a graphic on the screen that indicates the animal or the animal's shelter
        for a in self.ambassadors:
            if a == animal:
                pos = self.ambassadors.index(a) + 1
                if animal.asize == 'small':
                    animal.setSize(self.height/3, self.height/3)
                    animal.setPos(pos * self.center_x, pos * self.center_y)
                elif animal.asize == 'medium':
                    animal.setSize(self.height/2, self.height / 2)
                    animal.setPos(pos * self.center_x, pos * self.center_y)
                elif animal.asize == 'large':
                    animal.setSize(self.height , self.height)
                    animal.setPos(pos * self.center_x, pos * self.center_y)

    def labor(self, team, game):
        # food supply will be an object from the Feed class; it is a number representing the total amount of food available
        for animal in self.ambassadors:
            feed = animal.feed
            print(f'It will take {feed} feed to feed {animal.aname}.')
            team.feed = team.feed - feed
            if team.feed < 0:
                game = True
                print('there is not enough food to feed all of the animals!')
                return game
            animal.givefood()
            print(f'Fed {animal.aname}.There is {team.feed} feed left.')
        self.hasbeenlabored = True
        return game
    def reset(self):
        for animal in self.ambassadors:
            animal.reset()
        self.hasbeenlabored = False



class Animal(GraphicsDrawer):
    def __init__(self, aname='', species= None, special = False, **kwargs):
        self.asize = ''
        self.aname = str(aname)
        self.special = special
        self.species = str(species).lower()
        self.hasbeenfed = False
        self.feed = 0
        self.inspiration = 0
        self.imageStr = 'None'
        self.vp = 0
        self.calculate_stats()
        super().__init__(self.imageStr, self.aname, **kwargs)
    def __str__(self):
        return self.aname

    def calculate_stats(self):
        with open('textfiles/animals', 'r') as file:
            lines = [line.strip().split(',') for line in file]
            for animal in lines:
                if animal[0] == self.species.lower():
                    # find info
                    self.asize = animal[1]
                    self.feed = int(animal[2])
                    self.inspiration = int(animal[3])
                    self.vp = int(animal[4])
                    self.imageStr = animal[5]
                # else:
                #     print(f'not a match, animal[0] is {animal[0]} while self.species.lower() is {self.species.lower()}')
        if self.special:
            self.vp = self.vp * 2

    def givefood(self):
        self.hasbeenfed = True

    def reset(self):
        self.hasbeenfed = False

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
    def __init__(self, playernum, playernames, root, boardlist, **kwargs):
        self.players = int(playernum)
        self.playernames = playernames
        self.inspiration = 0
        self.total_money = self.players * 10
        self.volunteers = 0
        self.new_volunteers = 0
        self.new_employees = 0
        self.employees = 0
        self.supporters = 0
        self.feed = self.players * 10
        self.overworked = 0
        self.total_sanctuary_animals = []
        self.boardlist = boardlist
        super().__init__('players',**kwargs)
    def calculate_labor_for_upkeep(self):
        return self.players*2 + self.volunteers//5 + self.employees
    def calculate_labor_for_actions(self):
        return self.players*2 + self.volunteers//5 + self.emplyees//2

    def hire_employees(self, numactions, *largs):
        self.new_employees += int(numactions)
        print (f'Hired {numactions} employee(s)')
    def change_new_to_ready_employees(self):
        self.employees += self.new_employees
        print(f'{self.new_employees} new employee(s) are ready to work next round! That means you will have to start paying them!')
        self.new_employees = 0
    def change_new_to_ready_volunteers(self):
        self.volunteers += self.new_volunteers
        self.new_volunteers = 0
    def add_starting_animals(self, animallist):
        pos = 0
        if len(animallist) == self.players:
            for animal in animallist:
                self.total_sanctuary_animals.append(animal)
                animal = [animal]
                self.boardlist[pos].add_animals(animal)
                pos += 1
        else:
            print(f'failed to work, len(animallist) is {len(animallist)} while self.players is {self.players}')
    def recruit_volunteers(self, numactions, *largs):
        total_recruits = 0
        for n in range(1, int(numactions) + 1):
            roll = random.randint(1, 20)  # might replace this with a cool dice rolling graphic later
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
    def pay_employees(self):
        money_to_pay = self.employees * 10
        print(f'You have {self.employees} employees, and need to pay them {money_to_pay} in total for their work this round.'
              f'You have ${self.total_money} available, and if you do not pay an employee their full salary they will '
              f'quit and not work for you next round.')
        paid_done = False
        while not paid_done:
            try:
                num_paid = int(input('How many employees would you like to pay?'))
            except ValueError:
                print('You did not enter an integer!')
                continue
            price = num_paid * 10
            if num_paid > self.employees:
                print('You do not have that many employees, stop wasting money!')
                continue
            elif self.spend_money(price):
                print(f'Paid {num_paid} employees')
                if num_paid < self.employees:
                    num_quit = self.employees - num_paid
                    print(f'Did not pay all employees, {num_quit} have quit!')
                    self.employees = self.employees - num_quit
                paid_done = True
            else:
                print('You cannot pay all of those employees!')
                continue
    def gain_inspiration_from_animals(self):
        #total_sanctuary_animals should be a list of objects of the Animals class
        for animal in self.total_sanctuary_animals:
            self.inspiration += animal.inspiration
            print(f'Gained {animal.inspiration} inspiration from {animal.aname}! What a cutie!')
        print(f'Gained inspiration, new total: {self.inspiration}')
    def gain_inspiration(self, inspiration):
        self.inspiration = self.inspiration + inspiration
        print(f"Gained {inspiration} inspiration")
    def lose_inspiration(self, inspiration):
        self.inspiration = self.inspiration - inspiration
        if inspiration != 0:
            print(f'Lost {self.overworked * 10} inspiration. New inspiration is {self.inspiration}.')
    def spend_money(self, money):
        startcash = self.total_money
        self.total_money = self.total_money - money
        if self.total_money < 0:
            print('Not enough money to make purchase!')
            self.total_money = startcash
            return False
        return True
    def buy_feed(self, money):
        purchased_feed = money//2
        if self.spend_money(money):
            self.feed = self.feed + purchased_feed
            return True
        return False
    def add_names(self, name):
        self.playernames.append(str(name))
        print(f'Added player {str(name)} in position {self.playernames.index(str(name))}')
    def earn_money(self, money):
        self.total_money = self.total_money + money
        print(f'Earned ${money}')
    def public_outreach(self, *largs):
        d20 = random.randint(1,20)
        self.supporters += d20
        print(f'Gained {d20} supporters')
    def get_donations_from_supporters(self):
        self.total_money += self.supporters
    def rescue(self, animal):
        self.total_sanctuary_animals.append(animal)
    def gain_land(self):
        self.spend_money(20)
        self.boardlist.append(Board(self.root))

class GUI(Screen):
    #the main game class that things will be drawn onto
    _disabled_count = 0
    def __init__(self, pnum, root, **kwargs):
        self.playernum = pnum
        self.boardlist = []
        self.root = root
        super().__init__(**kwargs)
        #l = Label(text = 'Sanctuary', pos_hint = )
        self.add_boards()
    def add_boards(self):
        for i in range(1, self.playernum+1):
            #print(f'i for playernum is {i}')
            board = Board(pos_hint= {1},imageStr='images/farm.jpg', root = self.root)
            self.boardlist.append(board)
            self.add_widget(board)
            self.set_boards_pos()
            #print(f'Added board for {i} players')
            '''#bind the boards position to the screen resize event'''
        #print(f'boardlist for {self.playernum} players: {self.boardlist}')
    def set_boards_pos(self):
        i = 1
        for board in self.boardlist:
            xpos1,ypos1 = 0, Window.height/3
            xpos2 = Window.width /3
            ypos2 = 0
            #print(f'i for boardlist is {i}')
            if i == 1:
                xpos = xpos1
                ypos = ypos1
            elif i == 2:
                xpos = xpos2
                ypos = ypos1
            elif i == 3:
                xpos = xpos1
                ypos = ypos2
            elif i == 4:
                xpos = xpos2
                ypos = ypos2
            else:
                xpos = xpos1
                ypos = ypos1
            board.setPos(xpos, ypos)
            #print(f'set pos for boardlist at pos {i}, new pos is {board.pos}')
            i += 1
