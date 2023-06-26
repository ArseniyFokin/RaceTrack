import random

from strategy.strategy_graph import StrategyGraph


class StrategyBFS(StrategyGraph):
    """
    Стратегия BFS
    """
    def __init__(self, start: tuple, finishes: dict[tuple[int, int], bool], graph: dict, limit: int = None) -> None:
        """
        Инициализация стратегии BFS

        :param graph: Граф состояний
        :param start: Начальная позиция
        :param finishes: Финальные позиции
        :param limit: Ограничение на глубину
        """
        super().__init__(graph, start, finishes, limit)

    def get_next_point(self, current_point: tuple[int, int], prev_point: tuple[int, int]) \
            -> tuple[tuple[tuple[int, int], tuple[int, int]], bool]:
        """
        Следующая позиция

        :param current_point:
        :param prev_point:
        :return:
        """
        node = (current_point, (current_point[0] - prev_point[0], current_point[1] - prev_point[1]))
        return self.bfs(node), True

    def bfs(self, node: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
        """
        BFS

        :param node: Вершина в графе
        :return: Следующая вершина в графе
        """
        # Очередь рассматриваемых вершин
        queue = [node]
        # Просмотренные позиции
        visited = {}
        # Предыдущие вершины
        prev = {node: []}
        # Текущая глубина
        _limit = 0

        while queue and _limit <= self.limit:
            self.count_check_nodes += 1
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

        # Выбираем случайную вершину из смежных
        return self.graph[node][random.randint(0, len(self.graph[node]) - 1)]
