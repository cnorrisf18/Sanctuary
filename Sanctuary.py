from kivy.config import Config

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'window_state', 'maximized')
Config.write()
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.textinput import TextInput
import random
from functools import partial
from kivy.uix.screenmanager import ScreenManager, Screen
from classes import GUI, Players, Animal, MyLabel
from events import run_event

from kivy.core.window import Window


class SanctuaryApp(App):
    def board_screen(self, count, scre, playernames, animals, *largs):
        #print('ready to set up the game')
        #for a in animals:
        #    print(a.species)
        #print(scre.children)
        gui = GUI(name=f'gui{str(count)}', pnum=int(count), root=scre)
        scre.add_widget(gui)
        #print(scre.children)
        players = Players(count, playernames, scre, gui.boardlist)
        #print(players.total_sanctuary_animals)
        players.add_starting_animals(animals)
        #print(players.total_sanctuary_animals)
        with gui.canvas:
            # setup
            feed_label = MyLabel(0, .7, .58, text=f'Feed Available: {players.feed}',
                                pos_hint={'top': 1, 'right': 1}, size_hint=(.2, .1), id='feed_label')
            money_label = MyLabel(0, .9, .75, text=f'Money Available: {players.total_money}', pos_hint={'top': 1, 'right': .8}
                                 , size_hint=(.2, .1), id='money_label')
            inspiration_label = MyLabel(.2, .1, .87, text=f'Inspiration level: {players.inspiration}',
                                       pos_hint={'top': 1, 'right': .6},
                                       size_hint=(.2, .1), id='inspiration_label')
            welcome_label = MyLabel(.4, .1, .9, text=f"Welcome {', '.join(str(p) for p in players.playernames)}",
                                   pos_hint={'top': 1, 'left': 1}, size_hint=(.4, .1))
            people_label = MyLabel(.5,.1,.58, text=f'Employees: {players.employees}, Volunteers: {players.volunteers}, Supporters: '
                                       f'{players.supporters}', pos_hint={'top': .9, 'left': 1}, size_hint=(.3, .1),
                                  id='people_label')
            new_people_label = MyLabel(.67,0, 1,
                text=f'New Employees: {players.new_employees}, New Volunteers: {players.new_volunteers}',
                pos_hint={'top': .9, 'right': .8}, size_hint=(.2, .1), id='new_people_label')
            label_list = [feed_label, money_label, inspiration_label, welcome_label, people_label,
                          new_people_label]
            for label in label_list:
                gui.add_widget(label)
            dyn_but = MyLabel(0, .47, .7, text='',
                             pos_hint={'top': .78, 'right': .65}, size_hint=(.5, .1), id='dyn_but')
            gui.add_widget(dyn_but)
        self.Action(gui, players, thirdact=False, n=0)
        self.set_current_screen(scre, gui.name)

    def remove_widgets(self, theguy, thebuttonlist, dyn_but, *largs):
        for thebutton in thebuttonlist:
            theguy.remove_widget(thebutton)
            thebutton.pos = (10000, 10000)
            if thebutton.id == 'no':
                dyn_but.text = 'Select an action'

    def thirdAction(self, gui, team, name, dyn_but, n):
        print('thirdact')
        gui.askedforthirdact[(n // 2) - 1] = True
        with gui.canvas:
            dyn_but.text = f'{name}, click the button if you would like to perform a third action'
            third_but = Button(text=f'{name}, Click for a third action', pos_hint={'top': .6, 'right': 1},
                               size_hint=(.2, .1), id='third')
            no_but = Button(text='No third action', pos_hint={'top': .5, 'right': 1}, size_hint=(.2, .1), id='no')
            gui.add_widget(third_but)
            gui.add_widget(no_but)
            blist = [third_but, no_but]
            no_but.bind(on_press=partial(self.Action, gui, team, False, gui.n))
            no_but.bind(on_release=partial(self.remove_widgets, gui, blist, dyn_but))
            third_but.bind(on_press=partial(self.Action, gui, team, True, 1))
            third_but.bind(on_release=partial(self.remove_widgets, gui, blist, dyn_but))

    def Action(self, gui, team, thirdact, n,*largs):

        self.set_new_people_label(gui, team)
        self.set_people_label(gui, team)
        self.set_inspiration_label(gui, team)
        self.set_money_label(gui, team)
        self.set_feed_label(gui, team)
        dyn_but = Button()
        for widget in gui.children:
            if widget.id == 'dyn_but':
                dyn_but = widget
            elif widget.id == 'third' or widget.id == 'no':
                self.remove_widgets(gui, [widget], dyn_but)
        if n == 0:
            dyn_but.text = ''
        if thirdact:
            num_actions = 1
            team.overworked += 1
            dyn_but.text = 'A third action has been chosen, the team will lose 10 inspiration due to overwork'
            name = team.playernames[(gui.n - 1) // 2]
        else:
            num_actions = team.players * 2 + team.employees + (team.volunteers // 5) - team.actions_used_for_event
            if n >= team.players * 2:
                name = 'Employees and Volunteers'
            else:
                name = team.playernames[n // 2]
        print(num_actions)
        print(n)
        ask = 0
        if team.players == 1:
            ask = 2
        elif team.players == 2:
            ask = 4
        elif team.players == 3:
            ask = 6
        elif team.players == 4:
            ask = 8
        if not thirdact and (n == 2 or n == 4 or n == 6 or n == 8) and not gui.askedforthirdact[(n // 2) - 1] \
                and n <= ask:
            gui.n = n
            self.thirdAction(gui, team, team.playernames[(gui.n - 1) // 2], dyn_but, n)

        elif n < num_actions or thirdact:
            with gui.canvas:
                na_but = Button(text=f'{name}, select an action.', size_hint=(.2, .1), pos_hint={'top': .9, 'right': 1})
                gui.add_widget(na_but)
                up_but = Button(text='Upkeep', size_hint=(.2, .1), pos_hint={'top': .8, 'right': 1})
                fe_but = Button(text='Purchase Feed', size_hint=(.2, .1), pos_hint={'top': .7, 'right': 1})
                fu_but = Button(text='Organize Fundraiser', size_hint=(.2, .1), pos_hint={'top': .6, 'right': 1})
                em_but = Button(text='Hire Employees', size_hint=(.2, .1), pos_hint={'top': .5, 'right': 1})
                vo_but = Button(text='Recruit Volunteers', size_hint=(.2, .1), pos_hint={'top': .4, 'right': 1})
                ou_but = Button(text='Public Outreach', size_hint=(.2, .1), pos_hint={'top': .3, 'right': 1})
                re_but = Button(text='Rescue Animals', size_hint=(.2, .1), pos_hint={'top': .2, 'right': 1})
                if thirdact:
                    up_but.bind(on_press=partial(self.actionUpkeep, team, gui, dyn_but, gui.n - 1))
                    fe_but.bind(on_press=partial(self.actionPurchaseFeed, team, gui, dyn_but, gui.n - 1))
                    fu_but.bind(on_press=partial(self.actionOrganizeFundraiser, team, gui, dyn_but, gui.n - 1))
                    em_but.bind(on_press=partial(self.actionHireEmployees, team, gui, dyn_but, gui.n - 1))
                    vo_but.bind(on_press=partial(self.actionRecruitVolunteers, team, gui, dyn_but, gui.n - 1))
                    ou_but.bind(on_press=partial(self.actionPublicOutreach, team, gui, dyn_but, gui.n - 1))
                    re_but.bind(on_press=partial(self.actionRescue, team, gui, dyn_but, gui.n - 1))
                else:
                    up_but.bind(on_press=partial(self.actionUpkeep, team, gui, dyn_but, n))
                    fe_but.bind(on_press=partial(self.actionPurchaseFeed, team, gui, dyn_but, n))
                    fu_but.bind(on_press=partial(self.actionOrganizeFundraiser, team, gui, dyn_but, n))
                    em_but.bind(on_press=partial(self.actionHireEmployees, team, gui, dyn_but, n))
                    vo_but.bind(on_press=partial(self.actionRecruitVolunteers, team, gui, dyn_but, n))
                    ou_but.bind(on_press=partial(self.actionPublicOutreach, team, gui, dyn_but, n))
                    re_but.bind(on_press=partial(self.actionRescue, team, gui, dyn_but, n))

                button_list = [up_but, fe_but, fu_but, em_but, vo_but, ou_but, re_but]

                # def remove_widgets(theguy, thebuttonlist, *largs):
                #     for thebutton in thebuttonlist:
                #         theguy.remove_widget(thebutton)
                #         thebutton.pos = (10000, 10000)

                for button in button_list:
                    gui.add_widget(button)
                    button.bind(on_press=partial(self.remove_widgets, gui, button_list, dyn_but))
        # if not thirdact and n % 2 == 2 and n <= team.players *2:

        elif n >= num_actions and not thirdact:
            print('finished with actions')
            with gui.canvas:
                na_but = Button(text='No more actions', size_hint=(.2, .1), pos_hint={'top': .9, 'right': 1})
                gui.add_widget(na_but)
            gui.turn_count += 1
            if gui.turn_count > 15:
                self.game_end(gui.parent, gui, team)
            self.Resolution(team, gui.parent, gui)

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
            self.game_end(gui.parent, gui, team)

    def set_people_label(self, gui, team, *largs):
        if team.supporters < 0:
            team.supporters = 0
        if team.employees < 0:
            team.employees = 0
        if team.volunteers < 0:
            team.volunteers = 0
        for widget in gui.children:
            if widget.id == 'people_label':
                widget.text = f'Employees: {team.employees}, Volunteers: {team.volunteers}, Supporters: {team.supporters}'

    def set_new_people_label(self, gui, team, *largs):
        for widget in gui.children:
            if widget.id == 'new_people_label':
                widget.text = f'New Employees: {team.new_employees}, New Volunteers: {team.new_volunteers}'

    def actionUpkeep(self, team, gui, where_button, n, *largs):
        #print(f'n from actionUpkeep: {n}')

        def are_you_sure(board, *largs):
            neededfeed = sum([animal.feed for animal in board.ambassadors])
            where_button.text = f"You need {neededfeed} feed to labor this board. Are you sure you'd like to continue?"
            yes_button = Button(text = 'Yes', size_hint=(.1, .1), pos_hint={'top': .5, 'right': .75})
            no_button = Button(text = 'No', size_hint = (.1,.1) , pos_hint = {'top':.4, 'right': .75})
            gui.add_widget(yes_button)
            gui.add_widget(no_button)
            yes_button.bind(on_press = partial(do_upkeep, board, yes_button, no_button))
            yes_button.bind(on_release = partial(self.remove_widgets, gui, [yes_button, no_button], where_button))
            no_button.bind(on_press = partial(act_and_unbind, board, yes_button, no_button))
            no_button.bind(on_release = partial(self.remove_widgets, gui, [yes_button, no_button], where_button))


        def do_upkeep(board, *largs):
            # board.rect_bg.unbind(on_press=partial(do_upkeep, board, team))
            #print('doing upkeep!')
            #print(f'n from doing upkeep:{n}')
            if not board.hasbeenlabored:
                end = board.labor(team, False)
                #print(f'Performed upkeep, end = {end}')
                if not end:
                    #print(f'Success. Food left:{team.feed}')
                    # self.Action(gui, theteam, False, n+1)
                    gui.add_one = True
                    act_and_unbind(board)
                    self.set_feed_label(gui, team)

                    where_button.text = 'Success! Click another action.'
                    for b in gui.boardlist:
                        print(f'{b.hasbeenlabored} for has been labored')
                if end:
                    print('Failed to feed everyone')
                    where_button.text = 'Failed to feed all of the animals on the board!'
                    self.game_end(gui.parent, gui, team)
            else:
                print('That board has already been done this turn! Action wasted.')
                where_button.text = 'That board has already been done this turn! Select another action.'
                #print(f'n from failure to upkeep:{n}')
                # self.Action(gui, theteam, False, n)
                gui.add_one = False
                act_and_unbind(board)

        where_button.text = 'Click the board where you would like to perform upkeep.'

        def act_and_unbind(board, *largs):
            # print('unbinding and sending to action')
            if gui.add_one:
                #print(f'sending n + 1 or {n + 1} to action')
                self.Action(gui, team, False, n + 1)
            else:
                #print(f'sending n or {n} to action')
                self.Action(gui, team, False, n)
            for b in gui.boardlist:
                b.rect_bg.unbind_uid('on_press', uid)
                #b.rect_bg.unbind_uid('on_release', fouruid)

        for myboard in gui.boardlist:
            # print(f'n from boardlist:{n}')
            uid = myboard.rect_bg.fbind('on_press', are_you_sure, myboard, team)
            # thirduid = myboard.rect_bg.fbind('on_release', send_to_action)
            # secuid = myboard.rect_bg.fbind('on_release', muunbind, myboard)
            #fouruid = myboard.rect_bg.fbind('on_release', act_and_unbind, myboard)
            # myboard.rect_bg.bind(on_release = partial(myboard.rect_bg.unbind_uid, 'on_press', uid))

    def actionPurchaseFeed(self, team, gui, dyn_but, n, *largs):
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
                        amount_to_purchase.pos = (100000, 100000)
                        purchase_btn.pos = (10000, 100000)
                        self.Action(gui, team, False, n + 1)
                        team.newly_earned_money += -(amount * 2)
                        team.newly_purchased_feed += amount
                        dyn_but.text = f'Successfully purchased {amount} feed, select another action'
                        self.set_feed_label(gui, team)
                        self.set_money_label(gui, team)
                else:
                    gui.remove_widget(amount_to_purchase)
                    gui.remove_widget(purchase_btn)
                    amount_to_purchase.pos = (100000, 100000)
                    purchase_btn.pos = (10000, 100000)
                    dyn_but.text = 'You cannot afford this amount of feed! Select another action'
                    self.Action(gui, team, False, n)
            except ValueError:
                dyn_but.text = "You didn't enter an integer! Please try again"

        with gui.canvas:
            amount_to_purchase = TextInput(multiline=False, size_hint=(.1, .1), pos_hint={'top': .5, 'right': .75},
                                           hint_text='Feed to buy (integer)')
            gui.add_widget(amount_to_purchase)
            purchase_btn = Button(text='Purchase feed', size_hint=(.1, .1), pos_hint={'top': .4, 'right': .75})
            gui.add_widget(purchase_btn)
            purchase_btn.bind(on_press=partial(purchase_feed, amount_to_purchase))

    def actionOrganizeFundraiser(self, team, gui, dyn_but, n, *largs):
        def roll_d20(*largs):
            d20 = random.randint(1, 20)
            team.earn_money(d20)
            insp = 0
            if 0 <= d20 <= 5:
                insp = -10
            elif 6 <= d20 <= 15:
                insp = 0
            elif 16 <= d20 <= 19:
                insp = 5
            elif d20 == 20:
                insp = 10
            team.gain_inspiration(insp)
            self.set_money_label(gui, team)
            self.set_inspiration_label(gui, team)
            d20_but.pos = (100000, 100000)
            gui.remove_widget(d20_but)
            team.newly_earned_money += d20
            team.new_inspiration += insp
            self.Action(gui, team, False, n + 1)
            dyn_but.text = f'You earned ${d20} and gained {insp} inspiration. Pick another action.'

        with gui.canvas:
            dyn_but.text = 'Click the button to roll a d20 to decide how successful your fundraiser was.'
            d20_but = Button(text='Roll d20', pos_hint={'top': .5, 'right': .75}, size_hint=(.1, .1),
                             )
            gui.add_widget(d20_but)
            d20_but.bind(on_press=roll_d20)

    def actionHireEmployees(self, team, gui, dyn_but, n, *largs):
        team.hire_employees(1)
        self.set_new_people_label(gui, team)
        dyn_but.text = 'Successfully hired 1 employee, they will start working next round. Select another action.'
        self.Action(gui, team, False, n + 1)

    def actionRecruitVolunteers(self, team, gui, dyn_but, n, *largs):
        def roll_d20(*largs):
            d20 = random.randint(1, 20)
            rnum = 0
            if 0 <= d20 <= 5:
                rnum = 2
            elif 6 <= d20 <= 10:
                rnum = 4
            elif 11 <= d20 <= 15:
                rnum = 6
            elif 16 <= d20 <= 20:
                rnum = 10
            team.new_volunteers += rnum
            self.set_people_label(gui, team)
            d20_but.pos = (100000, 100000)
            gui.remove_widget(d20_but)
            self.set_new_people_label(gui, team)
            self.Action(gui, team, False, n + 1)
            dyn_but.text = f'You rolled a {d20} and recruited {rnum} volunteers. Select another action.'

        with gui.canvas:
            dyn_but.text = 'Click the button to roll a d20 to see how many volunteers you recruited.'
            d20_but = Button(text='Roll d20', pos_hint={'top': .5, 'right': .75}, size_hint=(.1, .1))
            gui.add_widget(d20_but)
            d20_but.bind(on_press=roll_d20)

    def actionPublicOutreach(self, team, gui, dyn_but, n, *largs):
        def roll_d20(*largs):
            d20 = random.randint(1, 20)
            team.supporters += d20
            team.new_supporters += d20
            self.set_people_label(gui, team)
            d20_but.pos = (100000, 100000)
            gui.remove_widget(d20_but)
            self.Action(gui, team, False, n + 1)
            dyn_but.text = f'You rolled a {d20} and have {d20} new supporters. Select another action.'

        with gui.canvas:
            dyn_but.text = 'Click the button to roll a d20 to see how many new supporters you have.'
            d20_but = Button(text='Roll d20', pos_hint={'top': .5, 'right': .75}, size_hint=(.1, .1))
            gui.add_widget(d20_but)
            d20_but.bind(on_press=roll_d20)

    def actionRescue(self, team, gui, dyn_but, n, *largs):
        dyn_but.text = 'Success! Pick another action'
        from editrescue import run_rescue
        #print(f'ROOT:{gui.parent}')
        #print(f'N FROM ACTIONRESCUE: {n}')
        run_rescue(team, gui.parent, gui, n + 1)


    def Resolution(self, team, root, gui, *largs):
        print(root.children)
        resolution_screen = Screen(name=f'resolution{gui.turn_count}')
        info_layout = BoxLayout(orientation='vertical')
        summ_label = MyLabel(r=.68, g=1, b=.99, text=f'You have completed the actions for round {gui.turn_count}!'
                                                   ' Here is the summary of your actions:', color = [0,0,0,1])
        info_layout.add_widget(summ_label)
        end = team.check_if_lost()
        game_end_label = MyLabel(1, .83, .37, color = [0,0,0,1])
        info_layout.add_widget(game_end_label)
        if not end:
            game_end_label.text = 'You fed all of your animals, and will continue to the next round.'
        else:
            game_end_label.text = 'You did not feed all of your animals, and have lost the game!'
        inspiration_label = MyLabel(.42, 1, .94, text=f'You lost {team.overworked * 10} inspiration '
                                         f'due to overworking.', color = [0,0,0,1])
        info_layout.add_widget(inspiration_label)
        team.lose_inspiration(team.overworked * 10)
        earned_label = MyLabel(.09, .44, .11, text=f'You earned ${team.newly_earned_money},'
                                    f' bought {team.newly_purchased_feed} feed, and'
                                    f' earned {team.new_inspiration} inspiration'
                                    f' and {team.new_supporters} new supporters.', color = [0,0,0,1])
        info_layout.add_widget(earned_label)
        if team.employees != 0:
            self.pay_employees(team, info_layout)
        if team.new_volunteers != 0 or team.new_employees != 0:
            new_emp_and_vol_label = MyLabel(.79, .37, .37, text=f'You have {team.new_employees} new employees'
                                                 f' and {team.new_volunteers} new volunteers.'
                                                 f' They will start working for you next round.', color = [0,0,0,1])

            info_layout.add_widget(new_emp_and_vol_label)

        team.change_new_to_ready()

        next_button = Button(text='Click to move on...')

        if end:
            next_button.bind(on_press=partial(self.game_end, root, gui, team))
        else:
            next_button.bind(on_press=partial(self.Rejuv, team, root, gui))

        info_layout.add_widget(next_button)

        resolution_screen.add_widget(info_layout)
        root.add_widget(resolution_screen)

        self.set_current_screen(root, resolution_screen.name)

    def pay_employees(self, team, layout):
        def pay(numemp, *largs):
            numemp = numemp.text
            print(numemp)
            try:
                numemp = int(numemp)
                amount = numemp * 10
                if 0 <= amount <= team.total_money and numemp <= team.employees:
                    if team.spend_money(amount):
                        layout.remove_widget(amt_to_pay)
                        layout.remove_widget(pay_btn)
                        team.newly_earned_money += -(amount * 2)
                        info_label.text = f'Successfully paid {numemp} employees'
                        if numemp < team.employees:
                            num_quit = team.employees - numemp
                            info_label.text = f'Paid {numemp} employees, but ' \
                                              f'{num_quit} have quit because you did not pay them'
                            team.employees = team.employees - num_quit
                else:
                    info_label.text = 'You cannot afford paying these employees! Enter a smaller number'
            except ValueError:
                info_label.text = "You didn't enter an integer! Please try again"

        money_to_pay = team.employees * 10
        info_label = Label(text=f'You have {team.employees} employees, and need to pay them ${money_to_pay}'
                                f' in total for their work this round.'
                                f' You have ${team.total_money} available, and if you do not pay an employee their '
                                f' full salary they will quit and not work for you next round.')
        amt_to_pay = TextInput(multiline=False, hint_text='Employees to pay (integer)')
        layout.add_widget(info_label)
        layout.add_widget(amt_to_pay)
        pay_btn = Button(text='Pay employee(s)')
        layout.add_widget(pay_btn)
        pay_btn.bind(on_press=partial(pay, amt_to_pay))

    def Rejuv(self, team, root, gui, *largs):
        [board.reset() for board in team.boardlist]
        Rejuv_screen = Screen(name=f'rejuv{gui.turn_count}')
        info_layout = BoxLayout(orientation='vertical')
        summ_label = MyLabel(.69, 1, .78, text='Welcome to Rejuvenation! Relax a bit...,'
                                  ' then press the button when you are ready to continue!', color = [0,0,0,1])
        info_layout.add_widget(summ_label)
        cash_earned = team.supporters
        cash_earned_label = MyLabel(.85, .96, 1, text=f'You earned ${cash_earned} from supporters.', color = [0,0,0,1])
        info_layout.add_widget(cash_earned_label)
        team.earn_money(cash_earned)
        inspiration_start = team.inspiration
        gui.askedforthirdact = [False, False, False, False]
        team.gain_inspiration_from_animals()
        earned_inspiration = team.inspiration - inspiration_start
        earned_inspiration_label = MyLabel(.96, .59, 1, text=f"You earned {earned_inspiration} inspiration from the animals."
                                                f"They sure are adorable, aren't they?", color = [0,0,0,1])
        info_layout.add_widget(earned_inspiration_label)
        team.overworked = 0
        team.actions_used_for_event = 0
        move_on_button = Button(text='Click to move on to the event...')
        info_layout.add_widget(move_on_button)
        move_on_button.bind(on_press=partial(self.Event, team, root, gui))
        Rejuv_screen.add_widget(info_layout)
        root.add_widget(Rejuv_screen)
        self.set_current_screen(root, Rejuv_screen.name)

    def Event(self, team, root, gui, *largs):
        run_event(team, root, gui)

    def call_Action(self, team, root, gui, *largs, n = 0):
        self.set_current_screen(root, gui.name)
        self.Action(gui, team, False, n)

    def game_end(self, root, gui, team, *largs):
        print('The game is over!')
        end_label = MyLabel(.16, .09, .53, text = '')
        game_end_screen = Screen(name = 'end')
        root.add_widget(game_end_screen)
        self.set_current_screen(root, 'end')
        layout = BoxLayout(orientation = 'vertical')
        layout.add_widget(end_label)
        game_end_screen.add_widget(layout)
        if team.inspiration <= -50:
            end_label.text = 'You lost due to dropping below -50 inspiration!'
        elif team.check_if_lost():
            end_label.text = 'You lost due to not feeding all of your animals!'
        elif gui.turn_count > 15:
            end_label.text = 'You lasted 15 rounds and successfully completed the game!'
        total_vp = 0
        for animal in team.total_sanctuary_animals:
            total_vp += animal.vp
        vp_label = MyLabel(.18, .34, .53, text = f'You earned {total_vp} victory points from the animals.'
                                                 f' Try to beat that score next time!')
        layout.add_widget(vp_label)
        sum_label = MyLabel(.34, .37, .53, text = f"In total, you earned ${team.total_earned_money},"
                                                  f" purchased {team.total_purchased_feed} feed and"
                                                  f" earned {team.total_inspiration} inspiration."
                                                  f" You had {team.supporters} supporters,"
                                                  f" {team.volunteers} volunteers, and"
                                                  f" {team.employees} employees.")
        layout.add_widget(sum_label)
        finish_label = MyLabel(.09, .76, .69, text = 'Thanks for playing! Hope to see you again!')
        layout.add_widget(finish_label)
    def set_current_screen(self, screen, name_of_screen, *largs):
        screen.current = name_of_screen



    def add_to_lists(self, lista, aname, aspecies, listb, bname, *largs):
        lista.append(Animal(aname, aspecies, special=True))
        listb.append(bname)
        return

    def setup_setup_screen(self, root, reset=False, *largs):
        name_list = []
        animal_list = []
        for i in range(1, 5):
            name_list, animal_list = self.setup_screen(root, i, name_list, animal_list)
        return root

    def setup_screen(self, root, i, name_list, animal_list, *largs):

        animallist = ['Cow', 'Horse', 'Pig', 'Sheep', 'Goat', 'Dog', 'Cat', 'Chicken', 'Duck', 'Rabbit']
        layout = BoxLayout(orientation='vertical')
        layout.name = i
        welcome_label = MyLabel(.44, .87, .48, text=f'Welcome to Sanctuary, Player {i}!')
        name = TextInput(multiline=False, padding_x=695, padding_y=50,
                         hint_text='Enter your name', font_size=20, background_color=(.44, .87, .48, 1))
        dropdown = DropDown()
        for index in range(10):
            btn = Button(text=animallist[index], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        abutton = Button(text='Click to pick your starting animal')
        dropdown.bind(on_select=lambda instance, x: setattr(abutton, 'text', x))
        abutton.bind(on_release=dropdown.open)
        aname = TextInput(multiline=False, padding_x=680, padding_y=50,
                          hint_text=f"Enter animal name", font_size=20, background_color=(.44, .87, .48, 1))
        movebtn = Button(text='Set up the next player')
        movebtn.bind(on_press=lambda instance: animal_list.append(Animal(aname.text, abutton.text, True)))
        movebtn.bind(on_press=lambda instance: name_list.append(name.text))
        movebtn.bind(on_release=partial(self.set_current_screen, root, f'setup{i + 1}'))
        endbtn = Button(text='Finished setting up, go to the game!')
        endbtn.bind(on_press=lambda instance: animal_list.append(Animal(aname.text, abutton.text, True)))
        endbtn.bind(on_press=lambda instance: name_list.append(name.text))
        endbtn.bind(on_release=partial(self.board_screen, i, root, name_list, animal_list))
        layout.add_widget(welcome_label)
        layout.add_widget(name)
        layout.add_widget(abutton)
        layout.add_widget(aname)
        layout.add_widget(movebtn)
        layout.add_widget(endbtn)
        if i == 4:
            layout.remove_widget(movebtn)
        setup_screen = Screen(name=f'setup{i}')
        setup_screen.add_widget(layout)
        root.add_widget(setup_screen)
        return name_list, animal_list

    def build(self, *largs):
        root = ScreenManager()
        self.setup_setup_screen(root)
        return root


if __name__ == '__main__':
    SanctuaryApp().run()
