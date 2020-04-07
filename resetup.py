from kivy.config import Config
Config.set('graphics','resizable', 0)
Config.set('graphics','fullscreen',0)
Config.set('graphics','window_state','maximized')
Config.write()
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
import time
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from random import random as r
from functools import partial
from kivy.uix.screenmanager import ScreenManager, Screen
from classes import GUI, Players, Animal
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
#from textgame import Setup, Action, Rejuv, Resolution
#for some reason the line above just runs textgame.... weird
from kivy.clock import Clock

class GameApp(App):
    def board_screen(self, count, scre, playernames, animals, *largs):
        print('ready to set up the game')
        for a in animals:
            print(a.species)
        print(scre.children)
        gui = GUI(name = str(count), pnum = int(count), root = scre)
        scre.add_widget(gui)
        print(scre.children)
        players = Players(count, playernames, scre, gui.boardlist)
        print(players.total_sanctuary_animals)
        players.add_starting_animals(animals)
        print(players.total_sanctuary_animals)
        with gui.canvas:
            #setup
            btn_bts = Button(text = 'Back to Player Selection', on_press = partial(self.reset, scre, players, animals),
                            size_hint = (.2,.1), pos_hint = {"top":1,"left":1})
            gui.add_widget(btn_bts)
            feed_label = Button(text = f'Feed Available: {players.feed}',
                               pos_hint = {'top':1, 'right':1},size_hint = (.2,.1))
            money_label = Button(text = f'Money Available: {players.total_money}', pos_hint = {'top':1, 'right':.8}
                                 , size_hint = (.2,.1))
            welcome_label = Button(text = f"Welcome {', '.join(str(p) for p in players.playernames) }", pos_hint = {'top':1,'right':.6}, size_hint = (.4,.1))
            gui.add_widget(welcome_label)
            gui.add_widget(feed_label)
            gui.add_widget(money_label)


        #print(gui.boardlist)

        self.set_current_screen(scre, gui.name)
        self.turnAction(scre, gui, players, thirdact=False)
    def turnAction(self,root, gui, team, thirdact):
        if thirdact:
            num_actions = 1
            team.overworked += 1
        else:
            num_actions = team.players * 2 + team.employees + (team.volunteers//5)
        #for n in range(0,num_actions):
        #    self.Action(gui,team,thirdact)
        Clock.schedule_once(partial(self.Action, root, gui, team, thirdact), 2)
    def Action(self, screen, gui, team, thirdact, *largs):
        if thirdact:
            num_actions = 1
            team.overworked += 1
        else:
            num_actions = team.players * 2 + team.employees + (team.volunteers//5)
        for n in range(0,num_actions):
            global done
            #done = False
            #while not done:
            if not thirdact:
                if n >= team.players * 2:
                    name = 'Employees and Volunteers'
                else:
                    name = team.playernames[n//2]
            else:
                name = 'Player'
            with gui.canvas:
                na_but = Button(text = f'{name}, select an action.', size_hint = (.2,.1), pos_hint = {'top':.9,'right':1})
                gui.add_widget(na_but)
                up_but = Button(text = 'Upkeep', size_hint = (.2,.1), pos_hint = {'top':.8, 'right': 1},
                                on_press = partial(self.actionUpkeep, team))
                fe_but = Button(text = 'Purchase Feed', size_hint = (.2,.1), pos_hint = {'top':.7, 'right': 1},
                                on_press = partial(self.actionPurchaseFeed, team))
                fu_but = Button(text = 'Organize Fundraiser', size_hint = (.2,.1), pos_hint = {'top':.6, 'right': 1},
                                on_press = partial(self.actionOrganizeFundraiser, team))
                em_but = Button(text = 'Hire Employees', size_hint = (.2,.1), pos_hint = {'top':.5, 'right': 1},
                                on_press = partial(self.actionHireEmployees, team))
                vo_but = Button(text = 'Recruit Volunteers', size_hint = (.2,.1), pos_hint = {'top':.4, 'right': 1},
                                on_press = partial(self.actionRecruitVolunteers, team))
                ou_but = Button(text = 'Public Outreach', size_hint = (.2,.1), pos_hint = {'top':.3, 'right': 1},
                                on_press = partial(self.actionPublicOutreach, team))
                re_but = Button(text = 'Rescue Animals', size_hint = (.2,.1), pos_hint = {'top':.2, 'right':1},
                                on_press = partial(self.actionRescue, team))
                button_list = [up_but, fe_but, fu_but, em_but, vo_but, ou_but, re_but]
                for button in button_list:
                    gui.add_widget(button)
                    button.bind(on_release= self.setdone)
                self.set_current_screen(screen, gui.name)
                # gui.add_widget(up_but)
                # gui.add_widget(fe_but)
                # gui.add_widget(fu_but)
                # gui.add_widget(em_but)
                # gui.add_widget(vo_but)
                # gui.add_widget(ou_but)
                # gui.add_widget(re_but)
    def setdone(self, *largs):
        done = True

    def actionUpkeep(self, team, *largs):
        pass
    def actionPurchaseFeed(self, team, *largs):
        pass
    def actionOrganizeFundraiser(self, team, *largs):
        pass
    def actionHireEmployees(self, team, *largs):
        pass
    def actionRecruitVolunteers(self, team, *largs):
        pass
    def actionPublicOutreach(self, team, *largs):
        pass
    def actionRescue(self, team, *largs):
        pass



    def set_current_screen(self, screen, name_of_screen, *largs):
        #print(f'Changing screen to {name_of_screen}')
        screen.current = name_of_screen


    def reset(self, scre, players, animals, *largs):
        del animals
        for wid in scre.children:
            for ch in wid.children:
                for a in ch.children:
                    ch.remove_widget(a)
                wid.remove_widget(ch)
            scre.remove_widget(wid)
        del players
        self.build()

    def add_to_lists(self, lista, aname, aspecies, listb, bname, *largs):
        lista.append(Animal(aname, aspecies, special = True))
        listb.append(bname)
        return

    def setup_setup_screen(self, root,reset = False,*largs):
        name_list = []
        animal_list = []
        for i in range(1,5):
            if reset == True:
                name_list, animal_list, reset = self.setup_screen(root, i, name_list, animal_list, reset = reset)
            else:
                name_list, animal_list, reset = self.setup_screen(root, i, name_list, animal_list)
        return root
    def setup_screen(self, root, i, name_list, animal_list, reset = False , *largs):
        if reset == True:
            animal_list = []
            name_list = []
            reset = False
        animallist = ['Cow', 'Horse', 'Pig', 'Sheep', 'Goat', 'Dog', 'Cat', 'Chicken', 'Duck', 'Rabbit']
        layout = BoxLayout(orientation = 'vertical')
        layout.name = i
        welcome_label = Label(text = f'Welcome to Sanctuary, Player {i}!')
        name = TextInput(multiline = False, padding_x = 695, padding_y = 50,
                         hint_text = 'Enter your name', font_size = 20, background_color = (0, 128, 129, 1))
        dropdown = DropDown()
        for index in range(10):
            btn = Button(text=animallist[index], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            #btn.bind(on_release= )
            dropdown.add_widget(btn)
        abutton = Button(text='Click to pick your starting animal')
        dropdown.bind(on_select=lambda instance, x: setattr(abutton, 'text', x))
        abutton.bind(on_release=dropdown.open)
        #abutton.bind(on_release = lambda instance: print(abutton.text))
        aname = TextInput(multiline = False, padding_x = 680, padding_y = 50,
                          hint_text = f"Enter animal name", font_size = 20, background_color = (200, 0, 200, 1))
        #add_animal_btn = Button(text = 'Add your animal')
        #add_animal_btn.bind(on_release = lambda instance: animal_list.append(Animal(aname.text, abutton.text, True)))
        #animal_list.append(Animal(aname.text, abutton.text, True))
        movebtn = Button(text = 'Set up the next player')
        movebtn.bind(on_press = lambda instance: animal_list.append(Animal(aname.text, abutton.text, True)))
        movebtn.bind(on_press = lambda instance: name_list.append(name.text))
        movebtn.bind(on_release = partial(self.set_current_screen, root, f'setup{i + 1}'))
        endbtn = Button(text = 'Finished setting up, go to the game!')
        endbtn.bind(on_press = lambda instance: animal_list.append(Animal(aname.text, abutton.text, True)))
        endbtn.bind(on_press = lambda instance: name_list.append(name.text))
        endbtn.bind(on_release = partial(self.board_screen, i, root, name_list, animal_list))
        layout.add_widget(welcome_label)
        layout.add_widget(name)
        layout.add_widget(abutton)
        layout.add_widget(aname)
       # layout.add_widget(add_animal_btn)
        layout.add_widget(movebtn)
        layout.add_widget(endbtn)
        if i == 4:
            layout.remove_widget(movebtn)
        setup_screen = Screen(name = f'setup{i}')
        setup_screen.add_widget(layout)
        root.add_widget(setup_screen)
        return name_list, animal_list, reset

    def build(self, *largs):
        root = ScreenManager()
        self.setup_setup_screen(root)
        return root


if __name__ == '__main__':
    GameApp().run()


