import pygame

from .entity_point import EntityPoint


class Player(EntityPoint):
    def __init__(self, position: pygame.Vector2, color: tuple[int, int, int] = None,
                 limits: tuple[pygame.Vector2, pygame.Vector2] = None):
        """

        :param position: Начальное положение
        :param color: Цвет
        """
        super().__init__(position, color, limits)
