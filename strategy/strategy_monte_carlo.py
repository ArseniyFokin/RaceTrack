import random

import pygame

from helpers.custom_figure.line import Line
from strategy.strategy import Strategy


class StrategyMonteCarlo(Strategy):
    LIMIT = 150
    LIMIT_POINTS = 10
    PROBABILITY_BEST = 0.5

    def __init__(self, start: tuple, finishes: dict[tuple[int, int], bool],
                 matrix_distance: dict[tuple[int, int], int], level, limit: int = None):
        super().__init__(start, finishes, limit or self.LIMIT)
        self.level = level

        self.matrix_distance = matrix_distance

    def get_next_point(self, current_point: tuple[int, int], prev_point: tuple[int, int]):
        """

        :param current_point:
        :param prev_point:
        :return:
        """
        available_next_points = self.get_available_moves(current_point, prev_point)
        next_point, is_available = self.monte_carlo(current_point, available_next_points)
        if next_point:
            next_point = (next_point, (next_point[0] - current_point[0], next_point[1] - current_point[1]))
        return next_point, is_available

    def monte_carlo(self, current_point: tuple[int, int], available_next_points: list[tuple[int, int]]):
        next_point, min_cost = available_next_points[0], 10**9
        for _ in range(self.limit):
            _current_point, _prev_point, _count_points = next_point, current_point, 0
            if random.random() > self.PROBABILITY_BEST:
                _current_point = random.choice(available_next_points)
            _next_point = _current_point

            while _count_points != self.LIMIT_POINTS \
                    and not self.finishes.get(_current_point) \
                    and self.matrix_distance.get(_current_point) is not None:
                __current_point, __prev_point = \
                    random.choice(self.get_available_moves(_current_point, _prev_point)), _current_point
                if self.check_available_path(__current_point, __prev_point):
                    _current_point, _prev_point = __current_point, __prev_point
                else:
                    break
                _count_points += 1

            _check_point = _current_point if self.finishes.get(_current_point) else _prev_point
            _cost = self.matrix_distance[_check_point]
            if _cost < min_cost:
                min_cost = _cost
                next_point = _next_point

        return next_point, self.matrix_distance.get(next_point) is not None

    def check_available_path(self, point_1, point_2):
        path_mask = Line(self.level.cell_display.get_coord_by_cell(pygame.Vector2(point_1)),
                         self.level.cell_display.get_coord_by_cell(pygame.Vector2(point_2))).get_mask()
        return not self.level.map_mask.overlap(path_mask, (0, 0))
