import pygame

from consts import WINDOW_WIDTH, WINDOW_HEIGHT


class Figure:
    def get_mask(self):
        """

        :return:
        """
        return pygame.mask.from_surface(self.get_surface())

    def get_surface(self):
        surface = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        surface.set_colorkey((0, 0, 0))
        self.draw_figure(surface)

        return surface
