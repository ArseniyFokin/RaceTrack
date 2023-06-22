import pygame

from helpers.helpers import get_random_color
from strategy.strategy import Strategy


class EntityPoint:
    """
    Базовая сущность
    """
    def __init__(self, position: pygame.Vector2, color: tuple[int, int, int],
                 limits: tuple[pygame.Vector2, pygame.Vector2] = None, title: str = None):
        """
        Инициализация базовой сущности

        :param position: Начальное положение
        :param color: Цвет сущности
        :param limits: Ограничения на доступный размер карты
        """
        # Текущая позиция
        self.position = position
        # Текущая позиция в формате tuple, для работы стратегий
        self.position_tuple = (int(position.x), int(position.y))
        # Первая позиция
        self.first_position = position
        # Пройденный путь
        self.history_way = [position, position]
        self.limits = limits
        self.title = title
        self.color = color or get_random_color()
        # Сущность жива и может продолжать движение
        self.is_alive = True
        # Сущность достигла финиша
        self.is_finish = False

    def run(self, new_position: pygame.Vector2 = None) -> bool:
        """
        Переместится на новую позицию

        :param new_position: Новая позиция
        :return: Совершено перемещение
        """
        if not new_position or new_position not in self.get_available_moves():
            return False

        self.position = new_position
        self.history_way.append(new_position)

        return True

    def get_available_moves(self) -> list[pygame.Vector2]:
        """
        Доступные позиции
        """
        _result = Strategy.get_available_moves(tuple(self.position), tuple(self.history_way[-2]))

        return list(filter(self.__check_limits,  map(pygame.Vector2, _result)))

    def __check_limits(self, point: pygame.Vector2) -> bool:
        """
        Проверить ограничение лимитами

        :param point: Позиция
        :return: Доступна ли позиция
        """
        if not self.limits:
            return True

        top_right, bottom_right = self.limits
        if point.x < top_right.x or point.x > bottom_right.x:
            return False

        if point.y < top_right.y or point.y > bottom_right.y:
            return False

        return True

    def reset_speed(self) -> None:
        """
        Сбросить скорость до 0
        """
        self.history_way.append(self.position)
