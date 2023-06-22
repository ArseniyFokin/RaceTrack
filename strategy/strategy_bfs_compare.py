import random

from strategy.strategy_bfs import StrategyBFS


class StrategyBFSCompare(StrategyBFS):
    """
    Стратегия BFS с учётом оценки конечных позиций
    """
    def __init__(self, start: tuple, finishes: dict[tuple[int, int], bool], graph: dict,
                 matrix_distance: dict[tuple[int, int], int], limit: int = None) -> None:
        """
        Инициализация стратегии

        :param graph: Граф состояний
        :param start: Начальная позиция
        :param finishes: Финальные позиции
        :param matrix_distance: Матрица с расстояниями
        :param limit: Ограничение на глубину
        """
        super().__init__(start, finishes, graph, limit)
        self.matrix_distance = matrix_distance

    def bfs(self, node: tuple[tuple[int, int], tuple[int, int]]):
        """
        BFS

        :param node: Вершина в графе
        :return: Следующая вершина в графе
        """
        # Очередь рассматриваемых вершин
        queue = [node]
        # Просмотренные вершины
        visited = {}
        # Предыдущие вершины
        prev = {node: []}
        # Текущая глубина
        _limit = 0

        while queue and _limit <= self.limit:
            _node = queue.pop(0)
            if visited.get(_node) is not None:
                continue

            if _node[0] in self.finishes:
                return prev[_node][0]

            for link in self.graph[_node]:
                queue.append(link)
                if not prev.get(link):
                    prev[link] = prev[_node] + [link]

            _limit = len(prev[_node])
            visited[_node] = True

        # Индекс максимального приближения к финишу
        _min_cost = 10**9
        # Вершины с максимальным индексом
        _max_nodes = []
        for node in queue:
            # Оценка позиции
            cost = self.matrix_distance[node[0]]
            if cost < _min_cost:
                _min_cost, _max_nodes = cost, [node]
            elif cost == _min_cost:
                _max_nodes.append(node)
        # Выбираем случайную из вершин с максимальным индексом
        return prev[random.choice(_max_nodes)][0]
