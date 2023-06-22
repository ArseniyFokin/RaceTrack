import pygame

from typing import Optional

from entity import Player, EntityPoint
from consts import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH_SHIFT, WINDOW_HEIGHT_SHIFT


class CellDisplay:
    """

    """

    def __init__(self, display: pygame.Surface, cell_size: int):
        self.display = display
        self.cell_size = cell_size
        self.origin = pygame.Vector2((0, 0))

        self.__moving_active = False
        self.__event_prev_click = None
        self.__event_prev_shift = None
        self.__click_point: Optional[pygame.Vector2] = None

        self.__cell_shift_width = WINDOW_WIDTH_SHIFT % cell_size
        self.__cell_shift_height = WINDOW_HEIGHT_SHIFT % cell_size

        self.__lines = []

    def event_input(self, event: pygame.event.Event):
        """

        :return:
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.__event_prev_click = pygame.Vector2(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP:
            if self.__event_prev_click and not self.__event_prev_shift:
                self.__click_point = pygame.Vector2(pygame.mouse.get_pos()) - self.origin
            self.__event_prev_click = None
            self.__event_prev_shift = None

        if event.type == pygame.MOUSEMOTION:
            self.__click_point = None

        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[2] and self.__event_prev_click:
            shift = -(pygame.math.Vector2(pygame.mouse.get_pos()) - self.__event_prev_click) * 2
            self.origin += (self.__event_prev_shift or pygame.Vector2(0, 0)) - shift
            self.origin = pygame.Vector2(
                min(WINDOW_WIDTH_SHIFT, max(-WINDOW_WIDTH_SHIFT, self.origin.x)),
                min(WINDOW_HEIGHT_SHIFT, max(-WINDOW_HEIGHT_SHIFT, self.origin.y))
            )
            self.__event_prev_shift = shift
            self.__click_point = None

    def draw(self, entities: list[EntityPoint] = None, active_player: Player = None):
        """
        :return:
        """
        cols = WINDOW_WIDTH // self.cell_size
        rows = WINDOW_HEIGHT // self.cell_size

        offset = pygame.math.Vector2(
            self.origin.x - self.origin.x // self.cell_size * self.cell_size,
            self.origin.y - self.origin.y // self.cell_size * self.cell_size
        )

        for i in range(cols + 1):
            x = offset.x + i * self.cell_size
            pygame.draw.line(self.display, 'gray', (x, 0), (x, WINDOW_HEIGHT), 2)

        for i in range(rows + 1):
            y = offset.y + i * self.cell_size
            pygame.draw.line(self.display, 'gray', (0, y), (WINDOW_WIDTH, y), 2)

        font = None
        for entity in entities or []:
            if entity.title:
                font = font or pygame.font.SysFont("monospace", 14)
                label = font.render(entity.title, True, entity.color)
                self.display.blit(label, self.origin + entity.position * self.cell_size)
            pygame.draw.circle(self.display, entity.color, self.origin + entity.position * self.cell_size, 5)
            for i in range(1, len(entity.history_way)):
                pygame.draw.line(self.display, entity.color, self.get_coord_by_cell(entity.history_way[i - 1]),
                                 self.get_coord_by_cell(entity.history_way[i]), width=3)
                pygame.draw.circle(
                    self.display, entity.color, self.get_coord_by_cell(entity.history_way[i]), radius=4)

        if active_player:
            pygame.draw.circle(self.display, active_player.color, self.get_coord_by_circle(active_player.position), 5)
            pygame.draw.circle(self.display, 'red', self.get_coord_by_circle(active_player.position), 6, 1)
            for move in active_player.get_available_moves():
                pygame.draw.circle(self.display, 'red', self.get_coord_by_circle(move), 5, 1)

    def get_click(self):
        """

        :return:
        """
        if not self.__click_point:
            return None
        for x in range(-WINDOW_WIDTH_SHIFT + self.__cell_shift_width, WINDOW_WIDTH + WINDOW_WIDTH_SHIFT + 1, self.cell_size):
            for y in range(-WINDOW_HEIGHT_SHIFT + self.__cell_shift_height, WINDOW_HEIGHT + WINDOW_HEIGHT_SHIFT + 1, self.cell_size):
                if self.__click_point.distance_to(pygame.Vector2(x, y)) < 7:
                    return pygame.Vector2(x, y) // self.cell_size

        return None

    def get_coord_by_circle(self, point: pygame.Vector2):
        """

        :param point:
        :return:
        """
        return self.origin + point * self.cell_size + (1, 1)

    def get_coord_by_cell(self, point: pygame.Vector2):
        """

        :param point:
        :return:
        """
        return self.origin + point * self.cell_size

    def get_max_limit_cells(self):
        """

        :return:
        """
        return pygame.Vector2(-WINDOW_WIDTH_SHIFT // self.cell_size, -WINDOW_HEIGHT_SHIFT // self.cell_size), \
            pygame.Vector2((WINDOW_WIDTH + WINDOW_WIDTH_SHIFT) // self.cell_size,
                           (WINDOW_HEIGHT + WINDOW_HEIGHT_SHIFT) // self.cell_size)
