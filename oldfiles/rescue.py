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
from classes import Players, Animal, MyLabel


def set_current_screen(screen_manager, name_of_screen, *largs):
    screen_manager.current = name_of_screen


def run_rescue(team, root, gui, n):
    rescue_id = random.randint(1, 15)
    rescue_screen = Screen(name=f'rescue{rescue_id}')
    root.add_widget(rescue_screen)
    set_current_screen(root, rescue_screen.name)
    layout = BoxLayout(orientation='vertical')
    rescue_screen.add_widget(layout)
    with open('textfiles/rescuedeck', 'r') as file:
        lines = [line.strip().split(', ') for line in file]
        for l in lines:
            if l[0] != 'id' and int(l[0]) == rescue_id:
                rescue_chosen = l
                r_name = l[1]
                r_type = l[2]
                r_desc = l[3]
                r_desc = r_desc.split('\\n')
                r_desc = '\n'.join(r_desc)
                print(r_desc)
                #r_desc = str(r_desc)
                result = l[4]
    try:
        name_label = MyLabel(.87, .19, .58, text=f"You drew: {r_name}")
        size_label = MyLabel(.50, .30, .70, text = f"This is a {r_type} sized animal rescue event.")
        desc_label = MyLabel(.54, .51, 1, text=f"{r_desc}")
        #choice1_label = MyLabel(.66, .37, 1, text=f"Choice 1: {choice_1}")
        effect1_button = Button(text=f"{result}", on_press=partial(perform_rescue, rescue_chosen, 1, team, root, gui, n))
        #choice2_label = MyLabel(.95, .46, 1, text=f"Choice 2: {choice_2}")
        effect2_button = Button(text=f"Don't take the rescue", on_press=partial(perform_rescue, rescue_chosen, 2, team, root, gui, n))
        wid_list = [name_label, size_label, desc_label, effect1_button, effect2_button]
        with layout.canvas:
            for wid in wid_list:
                layout.add_widget(wid)

    except UnboundLocalError:
        print('we did not find a name')

from Sanctuary import SanctuaryApp

def perform_rescue(rescue, took, team, root, gui, n, *largs):
    print(rescue)
    talk_about_rescue = Screen(name=f'talk{rescue[0]}')
    root.add_widget(talk_about_rescue)
    set_current_screen(root, f'talk{rescue[0]}')
    layout = BoxLayout(orientation='vertical')
    talk_about_rescue.add_widget(layout)
    id = int(rescue[0])
    if int(took) == 1:
        lay = take_rescue(id, team, layout)
    else:
        lay = ignore_rescue(id, team, layout)
    move_on = Button(text='Click to take another action', id='r_move')
    layout.add_widget(move_on)
    move_on.bind(on_press=partial(SanctuaryApp.call_Action, SanctuaryApp(), team, root, gui, n + 1))

def take_rescue(id, team, layout, *largs):

    with open('textfiles/names', 'r') as file:
        names = [line for line in file]
    if id == 1:
        buttons_for_animals(team, 10, 'small', names, layout)
    elif id == 2:
        buttons_for_animals(team, 1, 'medium', names, layout, twox = True)
    elif id == 3 or id == 7 or id == 8:
        if id == 3:
            number = 5
            size = 'large'
        elif id == 7:
            number = 3
            size = 'medium'
        else:
            number = 5
            size = 'small'
        num_but = MyLabel(.35, .15, .50, text = f'Pick how many {size} animals you want to rescue')
        b_list = [num_but]
        layout.add_widget(num_but)
        for i in range(1,number+1):
            button = Button(text = f'{i} animals')
            b_list.append(button)
            layout.add_widget(button)
            button.bind(on_press = partial(buttons_for_animals, team, i, size, names, layout, b_list))

    elif id == 4:
        buttons_for_animals(team, 2, 'medium', names, layout)
    elif id == 5:
        buttons_for_animals(team, 1, 'large', names, layout)
    elif id == 6:
        buttons_for_animals(team, 1, 'large', names, layout)
    elif id == 9:
        buttons_for_animals(team, 5, 'small', names, layout)
    elif id == 10:
        index10(id, team, layout)
    elif id == 11 or id == 12 or id == 13 or id == 14 or id == 15:
        if id == 11 or id == 12:
            size = 'small'
        elif id == 13 or id == 14:
            size = 'medium'
        else:
            size = 'large'
        buttons_for_animals(team, 1, size, names, layout)


def ignore_rescue(id, team, layout):
    if id == 10:
        index10(id, team, layout)
    else:
        flexbut = MyLabel(0, .13, .39, text='Decided not to do the rescue, and lost 10 inspiration')
        layout.add_widget(flexbut)

        team.inspiration -= 10


def index10(id, team , layout, *largs):
    label = MyLabel(0, .13, .39, text='')
    layout.add_widget(label)
    with open('textfiles/names', 'r') as file:
        names = [line for line in file]
    pos = 0
    latest_arrival = team.total_sanctuary_animals[-1]
    for board in team.boardlist:
        if latest_arrival in board.ambassadors:
            pos = team.boardlist.index(board)
    if latest_arrival.asize.lower() == 'large':
        babies = 1
        size = 'large'
    elif latest_arrival.asize.lower() == 'medium':
        babies = 2
        size = 'medium'
    else:
        babies = 3
        size = 'small'
        # add_animals(team, pos, num, size, names, fbut, layout, twox, b_list=None, species = None, *largs):
    add_animals(team, pos, babies, size, names, label, layout, False, species=latest_arrival.species)

def buttons_for_animals(team, num, size, names, layout, b_list=None, twox = False, *largs):
    if b_list is None:
        b_list = []
    remove_button(layout, b_list)
    flexbut = MyLabel(0, .13, .39, text='Select the board for animals to be placed on')
    layout.add_widget(flexbut)
    board_button_list = []
    for i in range(1,team.players+1):
        b_but = Button(text = f'Board {i}, where {team.playernames[i-1]} started')
        layout.add_widget(b_but)
        board_button_list.append(b_but)
        b_but.bind(on_press = partial(add_animals, team, i, num, size, names, flexbut, layout, twox, board_button_list))
        #b_but.bind(on_release = partial(remove_button, layout, board_button_list))
#self, aname='', species= None, special = False, **kwargs)
def add_animals(team, pos, num, size, names, fbut, layout, twox, b_list=None, species = None, *largs):
    if b_list is None:
        b_list = []
    remove_button(layout, b_list)
    a_list = []
    if size == 'small':
        species_list = ['chicken', 'duck', 'rabbit']
    elif size == 'medium':
        species_list = ['goat', 'sheep', 'dog', 'cat']
    elif size == 'large':
        species_list = [ 'cow', 'horse', 'pig' ]
    else:
        species_list = [species]
    for i in range(1, num + 1):
        new_animal = Animal(aname = random.choice(names), species = random.choice(species_list))
        team.rescue(new_animal)
        a_list.append(new_animal)
        if twox:
            new_animal.feed = new_animal.feed * 2
            new_animal.vp = new_animal.vp * 2
            new_animal.inspiration = new_animal.inspiration * 2
    team.boardlist[pos-1].add_animals(a_list)
    c_list = []
    for fa in a_list:
        if fa in team.boardlist[pos-1].ambassadors:
            c_list.append(fa)
    fbut.text = f"Added {len(c_list)} animals to the board:"
    for animal in c_list:
        alab = MyLabel(.76, .62, .34, text = f"{animal.aname} the {animal.species}")
        layout.add_widget(alab)

def remove_button(layout, b_list, *largs):
    for button in b_list:
        layout.remove_widget(button)
        button.pos = (10000,10000)
class TestRescueApp(App):

    def build(self):
        root = ScreenManager()
        team = Players(1, 'Chloe')
        run_rescue(team, root, None)
        return root


if __name__ == '__main__':
    TestRescueApp().run()
