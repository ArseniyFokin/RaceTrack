import random

from queue import PriorityQueue

import pygame

from helpers.custom_figure.line import Line
from strategy.strategy import Strategy
from strategy.strategy_graph import StrategyGraph


class StrategyBestBFSNoGraph(Strategy):
    """
    Стратегия Breadth-First Search
    """
    def __init__(self, start: tuple, finishes: dict[tuple[int, int], bool],
                 matrix_distance: dict[tuple[int, int], int], level, limit = None):
        super().__init__(start, finishes, limit or StrategyGraph.LIMIT)

        self.level = level
        self.matrix_distance = matrix_distance

    def get_next_point(self, current_point: tuple[int, int], prev_point: tuple[int, int]):
        """

        :param current_point:
        :param prev_point:
        :return:
        """
        next_point = self.best_bfs(current_point, prev_point)
        if next_point:
            next_point = (next_point, (next_point[0] - current_point[0], next_point[1] - current_point[1]))
        return next_point, True

    def best_bfs(self, current_point, prev_point):
        """
        Breadth-First Search

        :param current_point: Текущая позиция
        :param prev_point: Прошлая позиция
        :return: Следующая позиция
        """
        # Очередь с приоритетами
        queue = PriorityQueue()
        queue.put((float('inf'), float('inf'), (current_point, prev_point)))
        # Просмотренные вершины
        visited = {}
        # Предыдущие вершины
        prev = {(current_point, prev_point): []}
        # Текущая глубина
        _limit = 0
        # Текущая вершина
        node = None

        while not queue.empty() and _limit <= self.limit:
            node = queue.get()[2]
            if visited.get(node) is not None:
                continue

            if node[0] in self.finishes:
                break

            _current_point = node[0]
            for _move in self.get_available_moves(*node):
                new_node = (_move, _current_point)
                if self.matrix_distance.get(_move) is None:
                    continue
                if self.check_available_path(*new_node):
                    if prev.get(new_node) is None:
                        prev[new_node] = prev[node] + [new_node]
                    cost = self.matrix_distance[_move]
                    queue.put_nowait((cost, random.randint(0, 10), new_node))

            _limit = len(prev[node])
            visited[node] = True

        if not prev[node]:
            return None
        return prev[node][0][0]

    def check_available_path(self, point_1, point_2):
        path_mask = Line(self.level.cell_display.get_coord_by_cell(pygame.Vector2(point_1)),
                         self.level.cell_display.get_coord_by_cell(pygame.Vector2(point_2))).get_mask()
        return not self.level.map_mask.overlap(path_mask, (0, 0))
