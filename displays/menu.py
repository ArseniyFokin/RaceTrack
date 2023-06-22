import sys
import pygame

from entity import Player
from helpers import Button
from consts import WINDOW_WIDTH_CENTER, WINDOW_HEIGHT_CENTER, StateDisplay

from .switch import SwitchDisplay
from .cell_area import CellDisplay


class Menu:
    def __init__(self, display: pygame.Surface, switch_display: SwitchDisplay):
        self.display = display
        self.switch_display = switch_display
        self.cell_display = CellDisplay(self.display, 15)

        select_level_image = pygame.image.load('./images/select_level.png').convert_alpha()
        self.__select_level_button = Button(
            self.display, WINDOW_WIDTH_CENTER, WINDOW_HEIGHT_CENTER // 2 + 200, select_level_image, scale=0.15)
        back_image = pygame.image.load('./images/exit.png').convert_alpha()
        self.__back_button = Button(
            self.display, WINDOW_WIDTH_CENTER, WINDOW_HEIGHT_CENTER // 2 * 3 + 30, back_image, scale=0.15)

        self.player = Player(pygame.Vector2(5, 5), limits=self.cell_display.get_max_limit_cells())

    def draw(self):
        """

        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.cell_display.event_input(event)
            self.player.run(self.cell_display.get_click())

        self.cell_display.draw(entities=[self.player], active_player=self.player)
        if not self.player.get_available_moves():
            self.player.reset_speed()

        if self.__back_button.check_click():
            pygame.quit()
            sys.exit()
        elif self.__select_level_button.check_click():
            self.switch_display.state_display = StateDisplay.SELECT_LEVEL
