import os
import sys
import pygame

from typing import Optional

from helpers import Button
from consts import WINDOW_WIDTH, WINDOW_HEIGHT, StateDisplay, Location

from .level import Level
from .switch import SwitchDisplay
from .cell_area import CellDisplay


class SelectLevel:
    """

    """
    def __init__(self, display: pygame.Surface, switch_display: SwitchDisplay):
        """
        Инициализация

        :param display:
        :param switch_display:
        """
        self.display = display
        self.switch_display = switch_display
        self.cell_display = CellDisplay(self.display, 15)
        self.levels: list[Level] = self.load_levels()
        self.stage = 0
        self.button_levels: list[Button] = self.create_buttons()

        back_button_img = pygame.image.load('./images/menu.png').convert_alpha()
        self.__back_button = Button(display, 15, 15, back_button_img, scale=0.075, location=Location.TOP_LEFT)

        next_button_img = pygame.image.load('./images/next.png').convert_alpha()
        self.__next_button = Button(display, WINDOW_WIDTH - 15, WINDOW_HEIGHT - 15, next_button_img, scale=0.075, location=Location.BOTTOM_RIGHT)

        self.current_level: Optional[Level] = None

    def load_levels(self) -> list[Level]:
        """
        Загрузка уровней

        :return:
        """
        print([level_path for level_path in  sorted(filter(lambda x: x[0] != '.', sorted(os.listdir('./levels'))), key=lambda x: int(x.split('_')[1]))])
        return [
            Level(self.display, f'./levels/{level_path}', switch_display=self.switch_display)
            for level_path in sorted(filter(lambda x: x[0] != '.', sorted(os.listdir('./levels'))), key=lambda x: int(x.split('_')[1]))
        ]

    def create_buttons(self) -> list[Button]:
        """

        :return:
        """
        size_full_cell = min(WINDOW_HEIGHT, WINDOW_WIDTH - 100)
        left_angle = pygame.Vector2((WINDOW_WIDTH - size_full_cell) // 2 + 5, 5)
        size_cell = size_full_cell // 3
        number_cell = 0
        button_levels = []
        for level in self.levels:
            button_levels.append(Button(
                self.display,
                *(left_angle + pygame.Vector2((number_cell % 9) % 3 * size_cell + 15, (number_cell % 9) // 3 * size_cell + 15)),
                level.preview,
                size=(size_cell - 30, size_cell - 30),
                location=Location.TOP_LEFT,
                ext_data={'level': level}
            ))
            number_cell += 1
        return button_levels

    def draw(self):
        """

        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.cell_display.event_input(event)

        self.cell_display.draw()

        for button in self.button_levels[self.stage * 9: (self.stage + 1) * 9]:
            if button.check_click():
                self.current_level = button.ext_data['level']
                self.current_level.run()
                self.switch_display.state_display = StateDisplay.LEVEL

        if self.__back_button.check_click():
            self.stage = 0
            self.switch_display.state_display = StateDisplay.MENU

        if self.stage != len(self.levels) // 9:
            if self.__next_button.check_click():
                self.stage += 1

    def draw_level(self):
        """

        :return:
        """
        self.current_level.draw(not self.switch_display.is_active())


