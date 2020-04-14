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
import random
from functools import partial
from kivy.uix.screenmanager import ScreenManager, Screen
from classes import GUI, Players, Animal
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
#from textgame import Setup, Action, Rejuv, Resolution
#for some reason the line above just runs textgame.... weird
from kivy.clock import Clock

class SanctuaryApp(App):
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
            btn_bts = Button(text = 'Player Selection', on_press = partial(self.reset, scre, players, animals),
                            size_hint = (.1,.1), pos_hint = {"top":1,"left":1})
            gui.add_widget(btn_bts)
            feed_label = Button(text = f'Feed Available: {players.feed}',
                               pos_hint = {'top':1, 'right':1},size_hint = (.2,.1), id = 'feed_label')
            #print(feed_label)
            #feed_label.bind(text = f'Feed Available: {players.feed}')
            money_label = Button(text = f'Money Available: {players.total_money}', pos_hint = {'top':1, 'right':.8}
                                 , size_hint = (.2,.1), id = 'money_label')
            inspiration_label = Button(text = f'Inspiration level: {players.inspiration}', pos_hint = {'top':1,'right':.6},
                                       size_hint = (.2,.1), id = 'inspiration_label')
            welcome_label = Button(text = f"Welcome {', '.join(str(p) for p in players.playernames) }", pos_hint = {'top':1,'right':.4}, size_hint = (.3,.1))
            people_label = Button(text = f'Employees: {players.employees}, Volunteers: {players.volunteers}, Supporters: '
                                           f'{players.supporters}', pos_hint = {'top':.9,'left':1}, size_hint = (.3,.1),
                                  id = 'people_label')
            new_people_label = Button(text = f'New Employees: {players.new_employees}, New Volunteers: {players.new_volunteers}',
                                      pos_hint = {'top':.9,'right':.8}, size_hint = (.2,.1), id = 'new_people_label')
            gui.add_widget(people_label)
            gui.add_widget(new_people_label)
            gui.add_widget(welcome_label)
            gui.add_widget(feed_label)
            gui.add_widget(money_label)
            gui.add_widget(inspiration_label)
            dyn_but = Button(text='',
                             pos_hint={'top': .78, 'right': .65}, size_hint=(.5, .1), id='dyn_but')
            #dyn_but.pos = (10000,10000)
            gui.add_widget(dyn_but)
        print(gui.children)

        #print(gui.boardlist)

        self.set_current_screen(scre, gui.name)
        self.Action(scre, gui, players, thirdact=False, n=0)
    # def turnAction(self,root, gui, team, thirdact):
    #     if thirdact:
    #         num_actions = 1
    #         team.overworked += 1
    #     else:
    #         num_actions = team.players * 2 + team.employees + (team.volunteers//5)
    #     #for n in range(0,num_actions):
    #     #    self.Action(gui,team,thirdact)
    #     Clock.schedule_once(partial(self.Action, root, gui, team, thirdact), 2)
    def Action(self, screen, gui, team, thirdact, n, button_list = [], *largs):
        # make the buttons do things, rather than a for loop-program is in control of the user, not the programmer
        # define functions inside of functions, or use lambda for changing variables when a button is pressed
        if thirdact:
            num_actions = 1
            team.overworked += 1
        else:
            num_actions = team.players * 2 + team.employees + (team.volunteers//5)
        #for n in range(0,num_actions):
        #global done
        #n = 1
        #done = False
        #while not done:
        if not thirdact:

            if n >= team.players * 2:
                name = 'Employees and Volunteers'
            else:
                name = team.playernames[n//2]
        else:
            name = 'Player'
        print(num_actions)
        print(n)
        dyn_but = Button()
        for widget in gui.children:
            if widget.id == 'dyn_but':
                dyn_but = widget
        with gui.canvas:
            na_but = Button(text=f'{name}, select an action.', size_hint=(.2, .1), pos_hint={'top': .9, 'right': 1})
            gui.add_widget(na_but)
        if n < num_actions:
            with gui.canvas:
                #na_but = Button(text = f'{name}, select an action.', size_hint = (.2,.1), pos_hint = {'top':.9,'right':1})
                #gui.add_widget(na_but)
                up_but = Button(text = 'Upkeep', size_hint = (.2,.1), pos_hint = {'top':.8, 'right': 1},
                                on_press = partial(self.actionUpkeep, team, gui, dyn_but))
                fe_but = Button(text = 'Purchase Feed', size_hint = (.2,.1), pos_hint = {'top':.7, 'right': 1},
                                on_press = partial(self.actionPurchaseFeed, team, gui, dyn_but))
                fu_but = Button(text = 'Organize Fundraiser', size_hint = (.2,.1), pos_hint = {'top':.6, 'right': 1},
                                on_press = partial(self.actionOrganizeFundraiser, team, gui, dyn_but))
                em_but = Button(text = 'Hire Employees', size_hint = (.2,.1), pos_hint = {'top':.5, 'right': 1},
                                on_press = partial(self.actionHireEmployees, team, gui, dyn_but))
                vo_but = Button(text = 'Recruit Volunteers', size_hint = (.2,.1), pos_hint = {'top':.4, 'right': 1},
                                on_press = partial(self.actionRecruitVolunteers, team, gui, dyn_but))
                ou_but = Button(text = 'Public Outreach', size_hint = (.2,.1), pos_hint = {'top':.3, 'right': 1},
                                on_press = partial(self.actionPublicOutreach, team, gui, dyn_but))
                re_but = Button(text = 'Rescue Animals', size_hint = (.2,.1), pos_hint = {'top':.2, 'right':1},
                                on_press = partial(self.actionRescue, team, gui, dyn_but))
                button_list = [up_but, fe_but, fu_but, em_but, vo_but, ou_but, re_but]
                def remove_widgets(theguy, thebuttonlist, *largs):
                    for thebutton in thebuttonlist:
                        theguy.remove_widget(thebutton)
                        thebutton.pos = (10000,10000)
                for button in button_list:
                    gui.add_widget(button)
                    #button.bind(on_release= partial(self.Action, screen, gui, team, False, n+1, button_list))
                    button.bind(on_release = partial(remove_widgets, gui, button_list))

                #self.set_current_screen(screen, gui.name)
        elif n >= num_actions:
            print('finished with actions')
            with gui.canvas:
                na_but.text = 'No more actions'
               # print(button_list)
                #for button in button_list:
                 #   gui.remove_widget(button)
                  #  button.pos = (100000,1000000)
                # gui.add_widget(up_but)
                # gui.add_widget(fe_but)
                # gui.add_widget(fu_but)
                # gui.add_widget(em_but)
                # gui.add_widget(vo_but)
                # gui.add_widget(ou_but)
                # gui.add_widget(re_but)
    #def setdone(self, *largs):
     #   done = True
    def set_feed_label(self, gui, team, *largs):
        for widget in gui.children:
            if widget.id == 'feed_label':
                widget.text = f'Feed Available: {team.feed}'
    def set_money_label(self, gui, team, *largs):
        for widget in gui.children:
            if widget.id == 'money_label':
                widget.text = f'Money Available: {team.total_money}'
    def set_inspiration_label(self, gui, team, *largs):
        for widget in gui.children:
            if widget.id == 'inspiration_label':
                widget.text = f'Inspiration level: {team.inspiration}'
        if team.inspiration <= -50:
            self.game_end()
    def set_people_label(self, gui, team, *largs):
        if team.supporters < 0:
            team.supporters = 0
        for widget in gui.children:
            if widget.id == 'people_label':
                widget.text = f'Employees: {team.employees}, Volunteers: {team.volunteers}, Supporters: {team.supporters}'
    def set_new_people_label(self, gui, team, *largs):
        for widget in gui.children:
            if widget.id == 'new_people_label':
                widget.text = f'New Employees: {team.new_employees}, New Volunteers: {team.new_volunteers}'
    def actionUpkeep(self, team, gui, where_button, *largs):
        def do_upkeep(board, team, *largs):
            if not board.hasbeenlabored:
                end = board.labor(team, False)
                print(f'Performed upkeep, end = {end}')
                if not end:
                    print(f'Success. Food left:{team.feed}')
                    self.set_feed_label(gui, team)
                    where_button.text = 'Success! Click another action.'
                if end:
                    print('Failed to feed everyone')
                    where_button.text = 'Failed to feed all of the animals on the board!'
                    return end
            else:
                print('That board has already been done this turn! Action wasted.')
                where_button.text = 'That board has already been done this turn!'

        #with gui.canvas:
            #where_button = Button(text = 'Click the board where you would like to perform upkeep.',
            #                      pos_hint = {'top':.8, 'right':.6}, size_hint =(.4,.1), id = 'dyn_but')
            #gui.add_widget(where_button)
        where_button.text = 'Click the board where you would like to perform upkeep.'
        for board in gui.boardlist:
            board.rect_bg.bind(on_press = partial(do_upkeep, board, team))
            #board.rect_bg.bind(on_release = gui.remove_widget(where_button))

    def actionPurchaseFeed(self, team, gui, dyn_but,  *largs):
        neededfeed = sum([animal.feed for animal in team.total_sanctuary_animals])
        possible_feed = team.total_money // 2
        neededmoney = neededfeed * 2
        dyn_but.text = f'You need {neededfeed} feed in order to feed all of your animals, which will cost ' \
                       f'${neededmoney}. Right now, you can buy {possible_feed} feed.'
        def purchase_feed(amount, *largs):
            amount = amount.text
            print(amount)
            try:
                amount = int(amount)
                if 0 <= amount <= possible_feed:
                    if team.buy_feed(amount * 2):
                        gui.remove_widget(amount_to_purchase)
                        gui.remove_widget(purchase_btn)
                        amount_to_purchase.pos = (100000,100000)
                        purchase_btn.pos = (10000,100000)
                        dyn_but.text = f'Successfully purchased {amount} feed, select another action'
                        self.set_feed_label(gui, team)
                        self.set_money_label(gui, team)
                else:
                    dyn_but.text = 'You cannot afford this amount of feed! Please try again'
            except ValueError:
                dyn_but.text = "You didn't enter an integer! Please try again"

        with gui.canvas:
            amount_to_purchase = TextInput(multiline = False, size_hint = (.1,.1), pos_hint = {'top':.5,'right':.75},
                                           hint_text = 'Feed to buy (integer)')
            gui.add_widget(amount_to_purchase)
            purchase_btn = Button(text = 'Purchase feed', size_hint = (.1,.1), pos_hint = {'top':.4, 'right':.75})
            gui.add_widget(purchase_btn)
            purchase_btn.bind(on_press = partial(purchase_feed, amount_to_purchase))


    def actionOrganizeFundraiser(self, team, gui, dyn_but, *largs):
        def roll_d20(*largs):
            d20 = random.randint(1, 20)
            team.earn_money(d20)
            insp = 0
            if 0 <= d20 <= 5:
                insp = -10
            elif 6 <= d20 <= 15:
                insp = 0
            elif 16<= d20 <= 19:
                insp = 5
            elif d20 == 20:
                insp = 10
            team.gain_inspiration(insp)
            self.set_money_label(gui, team)
            self.set_inspiration_label(gui, team)
            d20_but.pos = (100000,100000)
            gui.remove_widget(d20_but)
            #gui.canvas.remove(d20_but)
            dyn_but.text = f'You earned ${d20} and gained {insp} inspiration. Pick another action.'
        with gui.canvas:
            dyn_but.text = 'Click the button to roll a d20 to decide how successful your fundraiser was.'
            d20_but = Button(text= 'Roll d20', pos_hint = {'top':.5, 'right':.75}, size_hint = (.1,.1),
                    )
            gui.add_widget(d20_but)
            d20_but.bind(on_press = roll_d20)

    def actionHireEmployees(self, team, gui, dyn_but, *largs):
        team.hire_employees(1)
        self.set_new_people_label(gui, team)
        dyn_but.text = 'Successfully hired 1 employee, they will start working next round. Select another action.'
        pass

    def actionRecruitVolunteers(self, team, gui, dyn_but, *largs):
        def roll_d20(*largs):
            d20 = random.randint(1, 20)
            rnum = 0
            if 0 <= d20 <= 5:
                rnum = 2
            elif 6 <= d20 <= 10:
                rnum = 4
            elif 11<= d20 <= 15:
                rnum = 6
            elif 16 <= d20 <= 20:
                rnum = 10
            team.new_volunteers += rnum
            self.set_people_label(gui, team)
            d20_but.pos = (100000,100000)
            gui.remove_widget(d20_but)
            #gui.canvas.remove(d20_but)
            self.set_new_people_label(gui, team)
            dyn_but.text = f'You rolled a {d20} and recruited {rnum} volunteers. Select another action.'
        with gui.canvas:
            dyn_but.text = 'Click the button to roll a d20 to see how many volunteers you recruited.'
            d20_but = Button(text= 'Roll d20', pos_hint = {'top':.5, 'right':.75}, size_hint = (.1,.1))
            gui.add_widget(d20_but)
            d20_but.bind(on_press = roll_d20)
    def actionPublicOutreach(self, team, gui,dyn_but,  *largs):
        def roll_d20(*largs):
            d20 = random.randint(1, 20)
            team.supporters += d20
            self.set_people_label(gui, team)
            d20_but.pos = (100000, 100000)
            gui.remove_widget(d20_but)
            # gui.canvas.remove(d20_but)
            dyn_but.text = f'You rolled a {d20} and have {d20} new supporters. Select another action.'

        with gui.canvas:
            dyn_but.text = 'Click the button to roll a d20 to see how many new supporters you have.'
            d20_but = Button(text='Roll d20', pos_hint={'top': .5, 'right': .75}, size_hint=(.1, .1))
            gui.add_widget(d20_but)
            d20_but.bind(on_press=roll_d20)
    def actionRescue(self, team, gui,dyn_but, *largs):
        pass

    def game_end(self):
        print('The game is over!')

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
    SanctuaryApp().run()


