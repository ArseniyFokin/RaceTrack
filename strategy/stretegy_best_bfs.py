import random

from queue import PriorityQueue

from strategy.strategy_bfs_compare import StrategyBFSCompare


class StrategyBestBFS(StrategyBFSCompare):
    """
    Стратегия Breadth-First Search
    """
    def bfs(self, node: tuple[tuple[int, int], tuple[int, int]]):
        """
        Breadth-First Search

        :param node: Вершина в графе
        :return: Следующая вершина в графе
        """
        # Очередь с приоритетами
        queue = PriorityQueue()
        queue.put((float('inf'), float('inf'), node))
        # Просмотренные вершины
        visited = {}
        # Предыдущие вершины
        prev = {node: []}
        # Текущая глубина
        _limit = 0
        # Текущая вершина
        current_node = None

        while not queue.empty() and _limit <= self.limit:
            current_node = queue.get()
            current_node=current_node[2]
            if visited.get(current_node) is not None:
                continue

            if current_node[0] in self.finishes:
                break

            for link in self.graph[current_node]:
                # Оценка позиции
                cost = self.matrix_distance[link[0]]
                # Добавляем вершину с учётом случайного второго параметра
                queue.put_nowait((cost, random.randint(0, 10), link))
                if not prev.get(link):
                    prev[link] = prev[current_node] + [link]

            _limit = len(prev[current_node])
            visited[current_node] = True

        return prev[current_node][0]
