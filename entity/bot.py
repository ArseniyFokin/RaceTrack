import time
import pygame

from typing import Optional

from strategy import Strategy, StrategyBFS, StrategyBestBFS, StrategyMonteCarlo, StrategyBFSCompare, \
    StrategyBestBFSNoGraph

from .entity_point import EntityPoint


class Bot(EntityPoint):
    """
    Бот
    """
    def __init__(self, position: pygame.Vector2, finishes: dict[tuple[int, int], bool],
                 params_level: dict, settings: Optional[dict] = None) -> None:
        """
        Инициализация бота

        :param position: Начальное положение
        :param finishes: Финишные вершины
        :param params_level: Параметры уровня
        :param settings: Параметры бота
        """
        settings = settings or {}
        super().__init__(position, color=settings.get('color'), title=settings.get('title'))
        # Финишные позиции
        self.finishes = finishes
        # Стратегия
        self.strategy = self.get_strategy(settings.get('strategy'), params_level)

        # Время для статистики
        self._time = 0

    def get_strategy(self, strategy_str: Optional[str], params_level) -> Optional[Strategy]:
        """
        Выбор стратегии с учётом параметров

        :param strategy_str: Стратегия заданная в настройках
        :param params_level: Параметры уровня
        :return:
        """
        graph = params_level.get('graph')
        matrix_distance = params_level.get('matrix_distance')
        level = params_level['level']
        strategy = None
        match strategy_str:
            case 'bfs':
                strategy = StrategyBFS(tuple(self.position_tuple), self.finishes, graph)
            case 'bfs_comp':
                strategy = StrategyBFSCompare(tuple(self.position_tuple), self.finishes, graph, matrix_distance)
            case 'best_bfs':
                strategy = StrategyBestBFS(tuple(self.position_tuple), self.finishes, graph, matrix_distance)
            case 'monte_carlo':
                strategy = StrategyMonteCarlo(self.position_tuple, self.finishes, matrix_distance, level)
            case 'best_bfs_no_graph':
                strategy = StrategyBestBFSNoGraph(self.position_tuple, self.finishes, matrix_distance, level)

        return strategy


    def run(self, _: pygame.Vector2 = None) -> None:
        """
        Надстройка над базовой функцией перемещения сущности с выбором следующей позиции

        :param _: Для поддержки совместимости
        """
        if not self.strategy:
            return
        # Текущее и предыдущее значения
        current, prev = self.history_way[-1], self.history_way[-2]
        t1 = time.time()
        # Следующая позиция
        next_position, is_available \
            = self.strategy.get_next_point((int(current[0]), int(current[1])), (int(prev[0]), int(prev[1])))
        self._time += (time.time() - t1)
        _next_node = next_position[0]
        super().run(pygame.Vector2(_next_node))
        if not is_available:
            self.is_alive = False
            print(f'crash -> time = {self._time}')
            return None
        # Ставим флажок, если следующая позиция в финишных вершинах
        if _next_node in self.finishes:
            print(f'finish -> time = {self._time}, nodes = {len(self.history_way)}, check_nodes = {self.strategy.count_check_nodes}')
            self.is_finish = True
