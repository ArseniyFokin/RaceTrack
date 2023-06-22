import sys
import json
import pygame
import pickle

from typing import Optional, Iterator

from entity import Bot, Player
from helpers import Button, Line
from consts import WINDOW_WIDTH, WINDOW_HEIGHT, StateDisplay, Location

from .switch import SwitchDisplay
from .cell_area import CellDisplay


class Level:
    def __init__(self, display: pygame.Surface, level_path: str, switch_display: Optional[SwitchDisplay] = None,
                 with_draw: bool = True):
        """

        """
        self.display = display
        self.switch_display = switch_display
        self.level_path = level_path
        self.with_draw = with_draw

        self.players: list[Player] = []
        self.moved_player: Optional[Player] = None
        self.__get_active_player = self.iterable_active_player()
        self.bots: list[Bot] = []
        self.graph = {}

        self.clock_timer = pygame.time.Clock()
        self.map_mask: Optional[pygame.Mask] = None
        self.map_img: pygame.image = None
        self.cell_display: Optional[CellDisplay] = None

        if with_draw and switch_display:
            back_button_img = pygame.image.load('./images/back.png').convert_alpha()
            self.__back_button = Button(display, 15, 15, back_button_img, scale=0.075, location=Location.TOP_LEFT)
        else:
            self.__back_button = None

        self.preview = pygame.image.load(self.level_path + '/preview.png').convert_alpha()

        self.__finishes_points = None

    def run(self):
        """
        Запуск уровня

        :return:
        """
        self.__init_from_path(self.level_path)

    def __init_from_path(self, level_path: str):
        """

        :param level_path:
        :return:
        """
        try:
            _map = pygame.image.load(level_path + '/map.png').convert_alpha()
            _map = pygame.transform.scale(_map, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.map_img = _map
            self.map_mask = pygame.mask.from_surface(_map)
        except pygame.error:
            pass

        with open(level_path + '/setting.json', 'r') as file:
            setting = json.load(file) or {}
            cell_size = setting['cell_size']
            bots = setting.get('bots', [])
            start = pygame.Vector2(setting['start'])
            finish = list(map(pygame.Vector2, setting['end']))

        self.start = start
        self.finish = finish
        self.cell_display = CellDisplay(self.display, cell_size)
        # self.players = [Player(self.start, color='red')]
        self.moved_player = None

        if self.with_draw:
            with open(level_path + '/graph.pickle', 'rb') as file:
                graph = pickle.load(file)
            with open(level_path + '/distance_matrix.pickle', 'rb') as file:
                matrix_distance = pickle.load(file)
            self.graph = graph
            self.bots = [Bot(start, self.finishes_points, {
                'graph': graph,
                'matrix_distance': matrix_distance,
                'level': self
            }, bot_setting) for bot_setting in bots]


    def draw(self, is_exit):
        if is_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.cell_display.event_input(event)
                if not self.moved_player and self.__get_active_player:
                    self.moved_player = next(self.__get_active_player)
                if self.moved_player:
                    click = self.cell_display.get_click()
                    if click and self.moved_player.run(click):
                        path_mask = Line(self.cell_display.get_coord_by_cell(click),
                                         self.cell_display.get_coord_by_cell(self.moved_player.history_way[-2])).get_mask()
                        if self.map_mask.overlap(path_mask, -self.cell_display.origin):
                            self.moved_player.is_alive = False
                        elif tuple(self.finish[0]) <= tuple(click) <= tuple(self.finish[1]):
                            self.moved_player.is_alive = False
                            self.moved_player.is_finish = True

                        self.moved_player = None
                elif self.bots:
                    for bot in self.bots:
                        if not bot.is_finish and bot.is_alive:
                            bot.run()

        finish_point_1 = self.cell_display.get_coord_by_cell(self.finish[0])
        finish_point_2 = self.cell_display.get_coord_by_cell(self.finish[1])
        pygame.draw.rect(self.display, 'green', (*finish_point_1, *(finish_point_2 - finish_point_1)))

        self.cell_display.draw(entities=[*self.bots, *self.players], active_player=self.moved_player)

        if self.map_img:
            self.display.blit(self.map_img, self.cell_display.origin)

        if self.__back_button and self.__back_button.check_click():
            self.switch_display.state_display = StateDisplay.SELECT_LEVEL

    def iterable_active_player(self) -> Iterator:
        """

        :return:
        """
        while True:
            for player in self.players:
                if player.is_alive:
                    yield player
            else:
                yield None

    @property
    def finishes_points(self):
        if self.__finishes_points:
            return self.__finishes_points

        points = {}
        for x in range(int(self.finish[0].x), int(self.finish[1].x + 1)):
            for y in range(int(self.finish[0].y) , int(self.finish[1].y + 1)):
                points[(x, y)] = True

        self.__finishes_points = points
        return points

    def check_intersection(self, point_1: tuple[int, int], point_2: tuple[int, int]):
        path_mask = Line(pygame.Vector2(point_1) * self.cell_display.cell_size,
                         pygame.Vector2(point_2) * self.cell_display.cell_size).get_mask()
        return self.map_mask.overlap(path_mask, (0, 0))