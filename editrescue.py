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

def remove_button(layout, b_list, *largs):
    for button in b_list:
        layout.remove_widget(button)
        button.pos = (10000, 10000)

def run_rescue(team, root, gui, n, *largs):
    #print(f"N FROM RUN RESCUE: {n}")
    not_found = True
    rescue_id = 0
    while not_found:
        rescue_id = random.randint(1, 15)
        if rescue_id in team.rescue_deck:
            not_found = False
    team.rescue_deck.remove(rescue_id)
    #print(rescue_id)
    def set_resc_screen(rescue):
        talk_about_rescue = Screen(name=f'talk{rescue[0]}')
        root.add_widget(talk_about_rescue)
        set_current_screen(root, f'talk{rescue[0]}')
        layout = BoxLayout(orientation='vertical')
        talk_about_rescue.add_widget(layout)
        #print('made layout')
        return layout
    def perform_rescue(rescue, *largs):
        number = 0
        size = 'small'
        twox = False
        layout2 = set_resc_screen(rescue)
        #layout2.add_widget(Button())
        id = int(rescue[0])
        #print(id)
        #print('got layout2')
        if id == 1:
            number = 10
            size = 'small'
            #buttons_for_animals(10, 'small', layout2)
        elif id == 2:
            number = 1
            size = 'medium'
            twox = True
            #buttons_for_animals(1, 'medium', layout2, twox=True)
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
            #print('IDING')
            num_but = MyLabel(.35, .15, .50, text=f'Pick how many {size} animals you want to rescue')
            b_list = [num_but]
            layout2.add_widget(num_but)
            for i in range(1, number + 1):
                button = Button(text=f'{i} animals')
                b_list.append(button)
                layout2.add_widget(button)
                button.bind(on_press=partial(buttons_for_animals, i, size, layout2, button_board_list = b_list))
        elif id == 4:
            number = 2
            size = 'medium'
            #buttons_for_animals(2, 'medium', layout2)
        elif id == 5:
            number = 1
            size = 'large'
            #buttons_for_animals(1, 'large',  layout2)
        elif id == 6:
            number = 1
            size = 'large'
            #buttons_for_animals(1, 'large', layout2)
        elif id == 9:
            number = 5
            size = 'small'
            #buttons_for_animals(5, 'small', layout2)
        elif id == 10:
            index10(layout2)
        elif id == 11 or id == 12 or id == 13 or id == 14 or id == 15:
            if id == 11 or id == 12:
                size = 'small'
            elif id == 13 or id == 14:
                size = 'medium'
            else:
                size = 'large'
            number = 1
            #buttons_for_animals(1, size, layout2)
        if id != 3 and id != 7 and id != 8 and id != 10:
            buttons_for_animals(number, size, layout2, twox = twox)
    def ignore_rescue(rescue, *largs):

        from Sanctuary import SanctuaryApp

        layout3 = set_resc_screen(rescue)
        if int(rescue[0]) == 10:
            index10(layout3)
        else:
            flexbut = MyLabel(0, .13, .39, text='Decided not to do the rescue, and lost 10 inspiration')
            layout3.add_widget(flexbut)
            team.inspiration -= 10
            move_on = Button(text='Click to take another action', id='r_move')
            layout3.add_widget(move_on)
            #print(f"N FROM IGNORE RESCUE: {n}")
            move_on.bind(on_press=partial(SanctuaryApp.call_Action, SanctuaryApp(), team, root, gui, n = n))

    def index10(lay, *largs):
        pos = 0
        latest_arrival = team.total_sanctuary_animals[-1]
        birth_label = MyLabel(0, .13, .39, text=f'{latest_arrival.aname} is giving birth!')
        lay.add_widget(birth_label)
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
        add_animals(pos, babies, size, birth_label, lay, twox = False, species=latest_arrival.species)

    def buttons_for_animals( num, size, ley, *largs, button_board_list=None, twox=False ):
        if button_board_list is None:
            button_board_list = []
        remove_button(ley, button_board_list)
        flexbut = MyLabel(0, .13, .39, text='Select the board for animals to be placed on')
        ley.add_widget(flexbut)
        board_button_list = []
        for i in range(1, team.players + 1):
            b_but = Button(text=f'Board {i}, where {team.playernames[i - 1]} started')
            ley.add_widget(b_but)
            board_button_list.append(b_but)
            b_but.bind(on_press=partial(add_animals, i, num, size, flexbut, ley, twox, add_board_list = board_button_list))


    def add_animals( pos, num, size, fbut, lem, twox, *largs, add_board_list=None, species=None):
        if add_board_list is None:
            add_board_list = []
        remove_button(lem, add_board_list)
        a_list = []
        if size == 'small':
            species_list = ['chicken', 'duck', 'rabbit']
        elif size == 'medium':
            species_list = ['goat', 'sheep', 'dog', 'cat']
        else:
            species_list = ['cow', 'horse', 'pig']
        if species is not None:
            print(f'We have a species! {species}')
            species_list = [species]
        for i in range(1, num + 1):
            new_animal = Animal(aname=random.choice(names), species=random.choice(species_list))
            team.rescue(new_animal)
            a_list.append(new_animal)
            if twox:
                new_animal.feed = new_animal.feed * 2
                new_animal.vp = new_animal.vp * 2
                new_animal.inspiration = new_animal.inspiration * 2
        team.boardlist[pos - 1].add_animals(a_list)
        c_list = []
        for fa in a_list:
            if fa in team.boardlist[pos - 1].ambassadors:
                c_list.append(fa)
        fbut.text = f"Added {len(c_list)} animals to the board:"
        for animal in c_list:
            alab = MyLabel(.76, .62, .34, text=f"{animal.aname} the {animal.species}")
            lem.add_widget(alab)
        move_on = Button(text='Click to take another action', id='r_move')
        lem.add_widget(move_on)
        from Sanctuary import SanctuaryApp
        #print(f"N FROM ADD ANIMALS: {n}")
        move_on.bind(on_press=partial(SanctuaryApp.call_Action, SanctuaryApp(), team, root, gui, n = n ))


    #rescue_id = random.randint(1, 15)
    rescue_screen = Screen(name=f'rescue{rescue_id}')
    root.add_widget(rescue_screen)
    set_current_screen(root, rescue_screen.name)
    layout1 = BoxLayout(orientation='vertical')
    rescue_screen.add_widget(layout1)
    with open('textfiles/names', 'r') as file1:
        names = [line for line in file1]
    with open('textfiles/rescuedeck', 'r') as file2:
        lines = [line.strip().split(', ') for line in file2]
        for l in lines:
            if l[0] != 'id' and int(l[0]) == rescue_id:
                rescue_chosen = l
                r_name = l[1]
                r_type = l[2].lower()
                r_desc = l[3]
                r_desc = r_desc.split('\\n')
                r_desc = '\n'.join(r_desc)
                result = l[4]
    try:
        name_label = MyLabel(.87, .19, .58, text=f"You drew: {r_name}")
        size_label = MyLabel(.50, .30, .70, text = f"This is a {r_type} sized animal rescue event.")
        desc_label = MyLabel(.54, .51, 1, text=f"{r_desc}")
        #choice1_label = MyLabel(.66, .37, 1, text=f"Choice 1: {choice_1}")
        effect1_button = Button(text=f"{result}", on_press=partial(perform_rescue, rescue_chosen))
        #choice2_label = MyLabel(.95, .46, 1, text=f"Choice 2: {choice_2}")
        effect2_button = Button(text=f"Don't take the rescue", on_press=partial(ignore_rescue, rescue_chosen))
        wid_list = [name_label, size_label, desc_label, effect1_button, effect2_button]
        with layout1.canvas:
            for wid in wid_list:
                layout1.add_widget(wid)

    except UnboundLocalError:
        print('we did not find a name')





class TestRescueApp(App):

    def build(self):
        root = ScreenManager()
        team = Players(1, 'Chloe')
        run_rescue(team, root, None, 0)
        return root


if __name__ == '__main__':
    TestRescueApp().run()
