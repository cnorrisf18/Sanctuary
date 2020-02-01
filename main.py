try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    import kivy
    from socket import *
    from pygame.locals import *
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.app import App
    from kivy.uix.behaviors import ButtonBehavior
    from kivy.uix.screenmanager import Screen


except ImportError as err:
    print("couldn't load module. %sys" % err)
    sys.exit(2)



def load_png(name):

    """ Load image and return image object"""
    fullname = name
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    return image, image.get_rect()

class SetUp(BoxLayout, Screen):
    def __init__(self, **kwargs):
        super(SetUp, self).__init__(**kwargs)
        self.font_size = 50
        self.orientation = "vertical"
        self.buttons = []
        self.label = Label(text = "How Many Players?")
        self.add_widget(self.label)
        for i in range(1,5):
            button = Button(text = str(i), font_size = self.font_size)
            button.bind(on_press= self.buttonpressed)
            self.add_widget(button)
            self.buttons.append(button)
    def buttonpressed(self, instance):
        global playernum
        playernum = int(instance.text)
        App.get_running_app().stop()

class Board(pygame.Surface):
    #The boards for the game, start with one per player
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs, size =pygame.transform.scale(self,(250,250)))
        self.image = pygame.image.load('farm.jpg')
        self.size = pygame.transform.scale(self, (250,250))

class SetupApp(App):

    def build(self):
        game = Screen()
        table_screen = SetUp()
        game.add_widget(table_screen)
        return game


def main():
    SetupApp().run()

    #set number of players
    #playernum = int(input("how many players?"))
    print(playernum,"players selected")
    # Initialize screen
    pygame.init()
    screen = pygame.display.set_mode((750,750))
    pygame.display.set_caption('Sanctuary')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((135, 206, 235))

    #initialize boards
    boardlist = []
    for i in range(0,playernum):
        boardlist.append(Board())

    #initialize sprites
    ##boardsprite = pygame.sprite.RenderPlain(board)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        screen.blit(background, (0,0))
        xpos = 250
        ypos = 250
        for i in range(0,playernum):
            screen.blit(boardlist[i], (xpos, ypos))
            if i == 1:
                ypos += 255
                xpos = 250
            else:
                xpos += 255

        #boardsprite.draw(screen)
        pygame.display.flip()


if __name__ == '__main__': main()