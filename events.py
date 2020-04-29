from kivy.config import Config

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'window_state', 'maximized')
Config.write()
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
import random
from functools import partial
from kivy.uix.screenmanager import ScreenManager, Screen
from classes import Players, MyLabel


def set_current_screen(screen_manager, name_of_screen, *largs):
    screen_manager.current = name_of_screen


# currently, run_event should have the arguments team (Players) and screen_manager, or root
def run_event(team, screen_manager, gui, *largs):
    not_found = True
    event_id = 0
    while not_found:
        event_id = random.randint(1, 20)
        if event_id in team.event_list:
            not_found = False
    team.event_list.remove(event_id)
    event_screen = Screen(name=f'Event{event_id}')
    event_layout = BoxLayout(orientation='vertical')
    screen_manager.add_widget(event_screen)
    set_current_screen(screen_manager, f'Event{event_id}')
    with open('textfiles/events', 'r') as file:
        lines = [line.strip().split(', ') for line in file]
        print(event_id)
        for l in lines:
            if l[0] != 'id' and int(l[0]) == event_id:
                event_chosen = l
                e_name = l[1]
                e_desc = l[2]
                choice_1 = l[3]
                effect_1 = l[4]
                choice_2 = l[5]
                effect_2 = l[6]
    try:
        name_label = MyLabel(1, .33, .33, text=f"You drew: {e_name}")
        desc_label = MyLabel(.54, .51, 1, text=f"{e_desc}. Pick a choice!")
        choice1_label = MyLabel(.66, .37, 1, text=f"Choice 1: {choice_1}")
        effect1_button = Button(text=f"{effect_1}", on_press=partial(do_it, event_chosen, 1, team, screen_manager, gui))
        choice2_label = MyLabel(.95, .46, 1, text=f"Choice 2: {choice_2}")
        effect2_button = Button(text=f"{effect_2}", on_press=partial(do_it, event_chosen, 2, team, screen_manager, gui))
        wid_list = [name_label, desc_label, choice1_label, effect1_button, choice2_label, effect2_button]
        with event_layout.canvas:
            for wid in wid_list:
                event_layout.add_widget(wid)
        event_screen.add_widget(event_layout)
        return event_id

    except UnboundLocalError:
        print('we did not find a name')


from Sanctuary import SanctuaryApp


def do_it(event, oneortwo, team, root, gui, *largs):
    print(event)
    talk_about_events = Screen(name=f'talk{event[0]}')
    root.add_widget(talk_about_events)
    set_current_screen(root, f'talk{event[0]}')
    layout = BoxLayout(orientation='vertical')
    talk_about_events.add_widget(layout)
    id = int(event[0])
    if int(oneortwo) == 1:
        lay = runchoice1(id, team, layout)
    else:
        lay = runchoice2(id, team, layout)
    move_on = Button(text='Click to go to the next round', id='e_move')
    layout.add_widget(move_on)
    move_on.bind(on_press=partial(SanctuaryApp.call_Action, SanctuaryApp(), team, root, gui))


# noinspection SpellCheckingInspection
def runchoice1(id, team, layout, *largs):
    flexbut = MyLabel(0, .13, .39, text='')
    layout.add_widget(flexbut)

    def gain_sup_or_vol(sov, *largs):
        word = ''
        if sov == 'sup':
            team.supporters += 10
            word = 'supporters'
        elif sov == 'vol':
            team.volunteers += 10
            word = 'volunteers'
        vol.pos = (1000, 1000)
        sup.pos = (1000, 1000)
        layout.remove_widget(vol)
        layout.remove_widget(sup)
        flexbut.text = f"Gained 10 {word}, spent $10 and used 1 action"

    if id == 1:
        team.actions_used_for_event = 2
        team.feed -= 5
        flexbut.text = 'Used 2 labor and lost 5 feed.'
    elif id == 2:
        team.inspiration += 10
        team.supporters -= 5
        flexbut.text = 'Gained 10 inspiration and lost 5 supporters.'
    elif id == 3:
        team.inspiration += 20
        if not team.spend_money(30):
            flexbut.text = 'Cannot afford to do this!'
        else:
            flexbut.text = 'Gained 20 inspiration and spent $30'
    elif id == 4:
        team.actions_used_for_event = team.players
        flexbut.text = f'Used {team.players} labor.'
    elif id == 5:
        team.actions_used_for_event = team.volunteers / 5
        flexbut.text = 'Lost actions from volunteers this round'
    elif id == 6:
        team.actions_used_for_event = team.employees
        flexbut.text = 'Lost actions from employees this round'
    elif id == 7:
        team.actions_used_for_event = 1
        team.inspiration -= 10
        if not team.spend_money(10):
            flexbut.text = 'Cannot afford this!'
        else:
            flexbut.text = 'Paid $10, lost 10 inspiration and used an action'
    elif id == 8:
        team.total_money -= team.supporters
        flexbut.text = 'Lost donations from supporters this round'
    elif id == 9:
        with layout.canvas:
            vol = Button(text='Gain Volunteers', on_press=partial(gain_sup_or_vol, 'vol'))
            sup = Button(text='Gain Supporters', on_press=partial(gain_sup_or_vol, 'sup'))
            layout.add_widget(vol)
            layout.add_widget(sup)
        team.actions_used_for_event = 1
        if not team.spend_money(10):
            flexbut.text = 'Cannot afford this!'
    elif id == 10:
        team.total_money += team.supporters
        flexbut.text = 'Recieved double the usual amount from supporters this round'
    elif id == 11:
        team.actions_used_for_event = 1
        team.inspiration += 20
        if not team.spend_money(50):
            flexbut.text = 'Cannot afford this!'
        else:
            flexbut.text = 'Used 1 action, paid $50 to the vet and gained 20 inspiration'
    elif id == 12:
        team.actions_used_for_event = 1
        if not team.spend_money(10):
            flexbut.text = 'Cannot afford this!'
        else:
            flexbut.text = "Spent $10 and used an extra action to labor the board"
    elif id == 13:
        team.supporters += 5
        team.inspiration += 5
        flexbut.text = 'Gained 5 supporters and 5 inspiration'
    elif id == 14:
        team.overworked = -team.players
        flexbut.text = 'The team will not get overworked this round'
    elif id == 15:
        team.actions_used_for_event = team.players
        flexbut.text = 'Used extra actions to labor each board'
    elif id == 16 or id == 17:
        team.actions_used_for_event = 2
        if not team.spend_money(20):
            flexbut.text = 'Cannot afford this!'
        else:
            flexbut.text = 'Used 2 actions and spent $20'
    elif id == 18:
        for animal in team.total_sanctuary_animals:
            animal.event18 = True
        flexbut.text = 'Animals need 1.5 times the amount of food this round'
    elif id == 19:
        team.actions_used_for_event = team.players
        if not team.spend_money(10):
            flexbut.text = 'Cannot afford this!'
        else:
            flexbut.text = f"Spent {team.players} actions and $10"
    elif id == 20:
        if not team.spend_money(5 * team.players):
            flexbut.text = 'Cannot afford this!'
        else:
            flexbut.text = f"Spent ${team.players * 5}"
    return layout


# noinspection SpellCheckingInspection
def runchoice2(id, team, layout):
    def find_and_remove_animal(highest_ani, board):
        highest_ani.die_or_remove()
        team.inspiration -= 30
        for animal in board.ambassadors:
            if animal == highest_ani:
                board.ambassadors.remove(highest_ani)
                team.total_sanctuary_animals.remove(highest_ani)
        return highest_ani

    def flip(pos, *largs):
        num_flips = team.players
        if pos <= num_flips:
            heads_or_tails = random.randint(1, 2)
            if heads_or_tails == 1:
                flexbut.text = 'You flipped a heads; the animal is safe... flip again'
                flip_but.bind(on_press=partial(flip, pos + 1))
            elif heads_or_tails == 2:
                highest_insp = 0
                highest_ani = None
                try:
                    board = team.boardlist[pos - 1]
                    for animal in board.ambassadors:
                        if animal.inspiration > highest_insp:
                            highest_insp = animal.inspiration
                            highest_ani = animal
                except IndexError:
                    board = []
                    print('No boards')
                find_and_remove_animal(highest_ani, board)
                flexbut.text = f'You flipped a tails, and {highest_ani.aname} the {highest_ani.species} has passed away.' \
                               f' Your team lost 30 inspiration for letting an animal die.'
                flip_but.bind(on_press=partial(flip, pos + 1))
        else:
            flexbut.text = 'No more animals to flip for'
            layout.remove_widget(flip_but)
            flip_but.pos = (10000, 10000)

    flexbut = MyLabel(0, .13, .39, text='')
    layout.add_widget(flexbut)
    if id == 1 or id == 11 or id == 19:
        if id == 11:
            team.supporters -= 10
        flip_but = Button(text='Click to flip a coin.', on_press=partial(flip, 1))
        layout.add_widget(flip_but)
    elif id == 2:
        id2board = []
        team.inspiration -= 10
        latest_animal = team.total_sanctuary_animals[-1]
        for board in team.boardlist:
            if latest_animal in board.ambassadors:
                id2board = board
        find_and_remove_animal(latest_animal, id2board)
        flexbut.text = f"Gave {latest_animal.aname} the {latest_animal.species} to their previous owners"
    elif id == 3:
        team.inspiration -= 20
        flexbut.text = 'Lost 20 inspiration'
    elif id == 4:
        team.overworked = 3
        flexbut.text = 'The team is automatically overworked this round'
    elif id == 5 or id == 6 or id == 10 or id == 14:
        runchoice1(id, team, layout)
    elif id == 7:
        team.supporters -= 10
        team.volunteers -= 5
        flexbut.text = 'Lost 5 volunteers and 10 supporters'
    elif id == 8:
        team.actions_used_for_event = 2
        flexbut.text = 'Used 2 actions'
    elif id == 9:
        flexbut.text = 'Lost 5 inspiration'
        team.inspiration -= 5
    elif id == 12:
        team.supporters -= 5
        team.inspiration -= 5
        flexbut.text = 'Lost 5 inspiration and 5 supporters'
    elif id == 13:
        team.volunteers += 5
        team.inspiration += 5
        flexbut.text = 'Gained 5 volunteers and 5 inspiration'
    elif id == 15:
        startfeed = team.feed
        team.feed -= 10
        if team.feed < 0:
            flexbut.text = "You don't have enough feed!"
            team.feed = startfeed
        else:
            flexbut.text = 'Used 10 feed'
    elif id == 16 or id == 17:
        team.inspiration -= 10
        team.supporters -= 5
        flexbut.text = 'Lost 10 inspiration and 5 supporters'
    elif id == 18:
        team.overworked = team.players
        if not team.spend_money(10):
            flexbut.text = 'Cannot afford this!'
        else:
            flexbut.text = 'The team is overworked; spent $10'
    elif id == 20:
        team.inspiration -= 20
        flexbut.text = 'Lost 20 inspiration'
    return layout


class TestEventApp(App):

    def build(self):
        root = ScreenManager()
        team = Players(1, 'Chloe')
        run_event(team, root, None)
        return root


if __name__ == '__main__':
    TestEventApp().run()
