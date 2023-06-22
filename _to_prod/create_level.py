import pickle
import sys
import time

import pygame

from consts import WINDOW_WIDTH, WINDOW_HEIGHT
from displays.level import Level
from helpers.custom_figure.line import Line


class CreateLevel(Level):
    def __init__(self, display: pygame.Surface, level_path: str, with_draw=False):
        super().__init__(display, level_path, with_draw=False)
        self.run()

    def create_graph(self):
        time_1 = time.time()
        graph: dict = self.__create_graph_bfs_new((int(self.start.x), int(self.start.y)))
        print(f'Time create graph = {time.time() - time_1}')
        print(f'Count nodes = {len(graph)}')
        print(f'Count links = {sum(map(len, graph.values()))}')

        self.time_bfs(graph)

        time_2 = time.time()
        self.__optimize_graph_new(graph)
        print(f'Time optimize graph = {time.time() - time_2}')
        print(f'Count nodes = {len(graph)}')
        print(f'Count links = {sum(map(len, graph.values()))}')

        self.time_bfs(graph)

        with open(self.level_path + '/graph.pickle', 'w+b') as file:
            pickle.dump(graph, file)

        min_path = self.create_min_path()

        # with open(self.level_path + '/min_path.pickle', 'w+b') as file:
        #     pickle.dump(min_path, file)

        print(f'min_path -> {min_path}')
        print(list(map(list, min_path.keys())))

        available_nodes = self.get_available_nodes((int(self.start.x), int(self.start.y)))

        # with open(self.level_path + '/available_points.pickle', 'w+b') as file:
        #     pickle.dump(available_nodes, file)

        print(f'available_nodes -> {available_nodes}')
        print(list(map(list, available_nodes.keys())))

        # print(graph)

        # self.draw_graph(graph)

        self.draw_path(list(min_path))


    def time_bfs(self, graph):
        t1 = time.time()
        queue = [((int(self.start.x), int(self.start.y)), (0, 0))]
        visited = {}

        while queue:
            _node = queue.pop(0)
            if visited.get(_node) is not None:
                continue
            for link in graph[_node]:
                queue.append(link)
            visited[_node] = True

        print(f'time bfs -> {time.time() - t1}')

    def draw_points(self, points):
        self.display.fill((255, 255, 255))
        self.draw()
        cell_size = self.cell_display.cell_size
        for point in points:
            pygame.draw.circle(self.display, 'red', (point[0] * cell_size, point[1] * cell_size), 1)
        pygame.image.save(self.display, 'temp_5.jpeg')

    def draw_path(self, path):
        self.display.fill((255, 255, 255))
        self.draw()
        cell_size = self.cell_display.cell_size
        for idx in range(1, len(path)):
            prev, cur = path[idx - 1], path[idx]
            pygame.draw.line(self.display, 'red', (cur[0] * cell_size, cur[1] * cell_size), (prev[0] * cell_size, prev[1] * cell_size))
        pygame.image.save(self.display, 'temp_4.jpeg')


    def draw_graph(self, graph):
        self.display.fill((255, 255, 255))
        self.draw()
        cell_size = self.cell_display.cell_size
        for key, value in graph.items():
            current, _ = key
            for next_line in value:
                _next, _ = next_line
                pygame.draw.line(self.display, 'red', (current[0] * cell_size, current[1] * cell_size), (_next[0] * cell_size, _next[1] * cell_size))
        pygame.image.save(self.display,'temp_3.jpeg')


    def __create_graph_bfs_new(self, node: tuple[int, int]):
        queue_node = [(node, (0, 0))]
        all_points = {node}
        visited = {}

        while queue_node:
            current_node = queue_node.pop(0)
            if visited.get(current_node) is not None:
                continue
            current_point, speed = current_node
            center_new_point = (current_point[0] + speed[0], current_point[1] + speed[1])
            link_nodes = []
            for acceleration in ((0, 0), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)):
                new_point = (center_new_point[0] + acceleration[0], center_new_point[1] + acceleration[1])
                if new_point == current_point and acceleration == (0, 0):
                    continue
                new_node = (new_point, (speed[0] + acceleration[0], speed[1] + acceleration[1]))
                if visited.get(new_node):
                    continue
                if self.map_mask.overlap(Line(
                        self.cell_display.get_coord_by_cell(pygame.Vector2(current_point)),
                        self.cell_display.get_coord_by_cell(pygame.Vector2(new_point))).get_mask(), (0, 0)):
                    continue
                link_nodes.append(new_node)
                queue_node.append(new_node)
                all_points.add(new_point)
            visited[current_node] = link_nodes

        print(len(all_points))
        return visited

    def __optimize_graph_new(self, graph: dict):
        finish_nodes = []
        for x in range(int(self.finish[0].x), int(self.finish[1].x + 1)):
            for y in range(int(self.finish[0].y) , int(self.finish[1].y + 1)):
                finish_nodes.append((x, y))
        print(f'{finish_nodes = }')
        check_node = {}
        start = ((int(self.start.x), int(self.start.y)), (0, 0))
        self.__optimize_graph_dfs_new(check_node, graph, start, finish_nodes)

        del_keys = []
        for key in graph:
            if not check_node.get(key):
                del_keys.append(key)
        for key in del_keys:
            graph.pop(key)

        for key, value in graph.items():
            right_value = []
            for link in value:
                if graph.get(link) is not None:
                    right_value.append(link)
            graph[key] = right_value


    def __optimize_graph_dfs_new(self, check_node, graph, node, finish_nodes):
        if check_node.get(node) is not None:
            return check_node[node]
        if node[0] in finish_nodes:
            check_node[node] = True
            return True
        to_finish = False
        for link_node in graph[node]:
            __to_finish = self.__optimize_graph_dfs_new(check_node, graph, link_node, finish_nodes)
            to_finish |= __to_finish
        check_node[node] = to_finish
        return to_finish

    def create_min_path(self):
        result = self.__create_min_path((int(self.start.x), int(self.start.y)))

        # print(list(map(list, result)))
        # self.draw_path(result)

        return result

    def __create_min_path(self, node: tuple[int, int]):
        queue = [node]
        visited = {}
        prev = {node: []}

        finish_nodes = []
        for x in range(int(self.finish[0].x), int(self.finish[1].x + 1)):
            for y in range(int(self.finish[0].y) , int(self.finish[1].y + 1)):
                finish_nodes.append((x, y))

        while queue:
            _node = queue.pop(0)
            if visited.get(_node) is not None:
                continue
            visited[_node] = True

            if _node in finish_nodes:
                all_points = [node] + prev[_node]
                return {point: True for point in all_points}

            for acceleration in ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)):
                new_node = (_node[0] + acceleration[0], _node[1] + acceleration[1])
                if visited.get(new_node) is not None:
                    continue
                if self.map_mask.overlap(Line(
                        self.cell_display.get_coord_by_cell(pygame.Vector2(new_node)),
                        self.cell_display.get_coord_by_cell(pygame.Vector2(_node))).get_mask(), (0, 0)):
                    continue

                queue.append(new_node)
                if not prev.get(new_node):
                    prev[new_node] = prev[_node] + [new_node]

        return None

    def print_get_available_nodes(self):
        available_nodes = self.get_available_nodes((int(self.start.x), int(self.start.y)))

        # with open(self.level_path + '/available_points.pickle', 'w+b') as file:
        #     pickle.dump(available_nodes, file)

        print(f'available_nodes -> {available_nodes}')
        print(list(map(list, available_nodes.keys())))

    def get_available_nodes(self, point):
        queue_node = [point]
        visited = {}

        while queue_node:
            current_point = queue_node.pop(0)
            if visited.get(current_point) is not None:
                continue
            visited[current_point] = True
            for acceleration in ((0, 0), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)):
                new_point = (current_point[0] + acceleration[0], current_point[1] + acceleration[1])
                if visited.get(new_point):
                    continue
                if self.map_mask.overlap(Line(
                        self.cell_display.get_coord_by_cell(pygame.Vector2(current_point)),
                        self.cell_display.get_coord_by_cell(pygame.Vector2(new_point))).get_mask(), (0, 0)):
                    continue
                queue_node.append(new_point)

        return visited

if __name__ == '__main__':
    sys.setrecursionlimit(2**15)
    pygame.init()
    display = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
    CreateLevel(display, '../levels/level_3').print_get_available_nodes()
    # "min_path": [[19, 2], [18, 3], [17, 4], [16, 4], [15, 4], [14, 5], [13, 5], [12, 5], [11, 6], [10, 6], [9, 7], [8, 8], [7, 9], [6, 10], [6, 11], [6, 12], [6, 13], [6, 14], [7, 15], [8, 16], [9, 17], [10, 17], [11, 18], [12, 18], [13, 19], [14, 19], [15, 19], [16, 19], [17, 20], [18, 20], [19, 20], [20, 20], [21, 20], [22, 20], [23, 20], [24, 20], [25, 20], [26, 20], [27, 19], [28, 19], [29, 19], [30, 19], [31, 18], [32, 18], [33, 17], [34, 17], [35, 16], [36, 15], [36, 14], [37, 13], [37, 12], [37, 11], [37, 10], [36, 9], [35, 8], [34, 7], [33, 6], [32, 6], [31, 5], [30, 5], [29, 5], [28, 5], [27, 4], [26, 4], [25, 4], [24, 4], [23, 4]]
