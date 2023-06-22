import pygame

from consts import Color
from helpers.custom_figure.fugure import Figure


class Line(Figure):
    def __init__(self, point_1: pygame.Vector2, point_2: pygame.Vector2):
        """

        :param point_1:
        :param point_2:
        """
        self.point_1 = point_1
        self.point_2 = point_2

    def draw_figure(self, surface):
        """

        :param surface:
        :return:
        """
        pygame.draw.line(surface, Color.BLUE, self.point_1, self.point_2)
