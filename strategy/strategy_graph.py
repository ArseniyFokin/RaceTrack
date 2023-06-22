from strategy.strategy import Strategy


class StrategyGraph(Strategy):
    """
    Базовый класс стратегий на графах
    """
    # Стандартный уровень глубины
    LIMIT = 10

    def __init__(self, graph: dict, start: tuple[int, int], finishes: dict[tuple[int, int], bool],
                 limit: int = None) -> None:
        """
        Инициализация базового класс

        :param graph: Граф игры
        :param start: Стартовая вершина
        :param finishes: Финальные вершины
        :param limit: Ограничение на глубину
        """
        super().__init__(start, finishes, limit or StrategyGraph.LIMIT)
        self.graph = graph or {}
