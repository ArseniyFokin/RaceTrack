import sys
import pygame

from helpers import Button
from consts import StateDisplay, Location


class Editor:
    """

    """
    def __init__(self, display: pygame.Surface, switch_display: 'SwitchDisplay'):
        self.switch_display = switch_display
        back_button_img = pygame.image.load('./images/back.png').convert_alpha()
        self.__back_button = Button(display, 15, 15, back_button_img, scale=0.075, location=Location.TOP_LEFT)

        save_button_img = pygame.image.load('./images/back.png').convert_alpha()
        self.__save_button = Button(
            display, self.__back_button.rec.topright[0] + 15, self.__back_button.rec.topright[1], save_button_img,
            scale=0.075, location=Location.TOP_LEFT)

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if self.__back_button.check_click():
            self.switch_display.state_display = StateDisplay.MENU

        if self.__save_button.check_click():
            print('SAFE')
