import pickle
import random
import sys
from math import sqrt

import pygame

from consts import WINDOW_WIDTH, WINDOW_HEIGHT
from helpers.custom_figure.line import Line
from _to_prod.create_level import CreateLevel


class GeneticLevel(CreateLevel):
    def __init__(self, display: pygame.Surface, level_path: str):
        super().__init__(display, level_path, with_draw=False)
        self.run()

        self.limit_path = len(self.min_path)
        self.limit_population = 100


    def fit(self):
        matrix = {(19, 2): 66, (19, 1): 66, (20, 1): 67, (20, 2): 67, (20, 3): 67, (19, 3): 66, (18, 3): 65, (18, 2): 65, (18, 1): 65, (20, 4): 67, (19, 4): 66, (18, 4): 65, (17, 4): 64, (17, 3): 64, (17, 2): 64, (17, 1): 64, (16, 4): 63, (16, 3): 63, (16, 2): 63, (16, 1): 63, (15, 4): 62, (15, 3): 62, (15, 2): 62, (14, 5): 61, (14, 4): 61, (14, 3): 61, (14, 2): 61, (13, 5): 60, (13, 4): 60, (13, 3): 60, (13, 2): 61, (12, 5): 59, (12, 4): 59, (12, 3): 60, (12, 2): 61, (11, 6): 58, (11, 5): 58, (11, 4): 59, (11, 3): 60, (10, 6): 57, (10, 5): 58, (10, 4): 59, (10, 3): 60, (9, 7): 56, (9, 6): 57, (9, 5): 58, (9, 4): 59, (9, 3): 60, (8, 8): 55, (8, 7): 56, (8, 6): 57, (8, 5): 58, (8, 4): 59, (7, 9): 54, (7, 8): 55, (7, 7): 56, (7, 6): 57, (7, 5): 58, (7, 4): 59, (6, 10): 53, (6, 9): 54, (6, 8): 55, (6, 7): 56, (6, 6): 57, (6, 5): 58, (6, 11): 52, (5, 11): 52, (5, 10): 53, (5, 9): 54, (5, 8): 55, (5, 7): 56, (5, 6): 57, (5, 5): 58, (6, 12): 51, (5, 12): 51, (4, 12): 51, (4, 11): 52, (4, 10): 53, (4, 9): 54, (4, 8): 55, (4, 7): 56, (4, 6): 57, (6, 13): 50, (5, 13): 50, (4, 13): 51, (3, 13): 52, (3, 12): 52, (3, 11): 52, (3, 10): 53, (3, 9): 54, (3, 8): 55, (3, 7): 56, (6, 14): 49, (5, 14): 50, (4, 14): 51, (3, 14): 52, (2, 14): 53, (2, 13): 53, (2, 12): 53, (2, 11): 53, (2, 10): 53, (2, 9): 54, (2, 8): 55, (7, 15): 48, (6, 15): 49, (5, 15): 50, (4, 15): 51, (3, 15): 52, (2, 15): 53, (1, 13): 54, (1, 12): 54, (1, 11): 54, (8, 16): 47, (7, 16): 48, (6, 16): 49, (5, 16): 50, (4, 16): 51, (3, 16): 52, (9, 17): 46, (8, 17): 47, (7, 17): 48, (6, 17): 49, (5, 17): 50, (4, 17): 51, (3, 17): 52, (10, 17): 45, (10, 18): 45, (9, 18): 46, (8, 18): 47, (7, 18): 48, (6, 18): 49, (5, 18): 50, (11, 18): 44, (11, 19): 44, (10, 19): 45, (9, 19): 46, (8, 19): 47, (7, 19): 48, (6, 19): 49, (12, 18): 43, (12, 19): 43, (12, 20): 43, (11, 20): 44, (10, 20): 45, (9, 20): 46, (8, 20): 47, (13, 19): 42, (13, 20): 42, (13, 21): 42, (12, 21): 43, (11, 21): 44, (10, 21): 45, (14, 19): 41, (14, 20): 41, (14, 21): 41, (14, 22): 41, (13, 22): 42, (15, 19): 40, (15, 20): 40, (15, 21): 40, (15, 22): 40, (16, 19): 39, (16, 20): 39, (16, 21): 39, (16, 22): 39, (17, 20): 38, (17, 21): 38, (17, 22): 38, (18, 20): 37, (18, 21): 37, (18, 22): 37, (18, 23): 37, (19, 20): 36, (19, 21): 36, (19, 22): 36, (19, 23): 36, (20, 20): 35, (20, 21): 35, (20, 22): 35, (20, 23): 35, (21, 20): 34, (21, 21): 34, (21, 22): 34, (21, 23): 34, (22, 20): 33, (22, 21): 33, (22, 22): 33, (22, 23): 33, (23, 20): 32, (23, 21): 32, (23, 22): 32, (23, 23): 32, (24, 20): 31, (24, 21): 31, (24, 22): 31, (24, 23): 31, (25, 20): 30, (25, 21): 30, (25, 22): 30, (25, 23): 30, (26, 20): 29, (26, 21): 29, (26, 22): 29, (27, 19): 28, (27, 20): 28, (27, 21): 28, (27, 22): 28, (28, 19): 27, (28, 20): 27, (28, 21): 27, (28, 22): 27, (29, 19): 26, (29, 20): 26, (29, 21): 26, (29, 22): 26, (30, 19): 25, (30, 20): 25, (30, 21): 25, (30, 22): 26, (31, 18): 24, (31, 19): 24, (31, 20): 24, (31, 21): 25, (32, 18): 23, (32, 19): 23, (32, 20): 24, (32, 21): 25, (33, 17): 22, (33, 18): 22, (33, 19): 23, (33, 20): 24, (33, 21): 25, (34, 17): 21, (34, 18): 22, (34, 19): 23, (34, 20): 24, (35, 16): 20, (35, 17): 21, (35, 18): 22, (35, 19): 23, (35, 20): 24, (36, 15): 19, (36, 16): 20, (36, 17): 21, (36, 18): 22, (36, 19): 23, (36, 14): 18, (37, 14): 18, (37, 15): 19, (37, 16): 20, (37, 17): 21, (37, 18): 22, (37, 19): 23, (37, 13): 17, (38, 13): 17, (38, 14): 18, (38, 15): 19, (38, 16): 20, (38, 17): 21, (38, 18): 22, (37, 12): 16, (38, 12): 16, (39, 12): 16, (39, 13): 17, (39, 14): 18, (39, 15): 19, (39, 16): 20, (39, 17): 21, (37, 11): 15, (38, 11): 15, (39, 11): 16, (40, 11): 17, (40, 12): 17, (40, 13): 17, (40, 14): 18, (40, 15): 19, (40, 16): 20, (37, 10): 14, (38, 10): 15, (39, 10): 16, (40, 10): 17, (41, 10): 18, (41, 11): 18, (41, 12): 18, (41, 13): 18, (41, 14): 18, (41, 15): 19, (37, 9): 14, (38, 9): 15, (36, 9): 13, (39, 9): 16, (40, 9): 17, (41, 9): 18, (37, 8): 14, (38, 8): 15, (36, 8): 13, (39, 8): 16, (35, 8): 12, (40, 8): 17, (37, 7): 14, (38, 7): 15, (36, 7): 13, (39, 7): 16, (35, 7): 12, (34, 7): 11, (37, 6): 14, (38, 6): 15, (36, 6): 13, (35, 6): 12, (34, 6): 11, (33, 6): 10, (37, 5): 14, (36, 5): 13, (35, 5): 12, (34, 5): 11, (33, 5): 10, (32, 6): 9, (32, 5): 9, (36, 4): 13, (35, 4): 12, (34, 4): 11, (33, 4): 10, (32, 4): 9, (31, 5): 8, (31, 4): 8, (34, 3): 11, (33, 3): 10, (32, 3): 9, (31, 3): 8, (30, 5): 7, (30, 4): 7, (30, 3): 7, (31, 2): 8, (30, 2): 7, (29, 5): 6, (29, 4): 6, (29, 3): 6, (29, 2): 6, (28, 5): 5, (28, 4): 5, (28, 3): 5, (28, 2): 5, (27, 4): 4, (27, 3): 4, (27, 2): 4, (27, 1): 4, (26, 4): 3, (26, 3): 3, (26, 2): 3, (26, 1): 3, (25, 4): 2, (25, 3): 2, (25, 2): 2, (25, 1): 2, (24, 4): 1, (24, 3): 1, (24, 2): 1, (24, 1): 1, (23, 4): 0, (23, 3): 0, (23, 2): 0, (23, 1): 0, (22, 4): 0, (22, 3): 0, (22, 2): 0, (22, 1): 0, (21, 4): 0, (21, 3): 0, (21, 2): 0, (21, 1): 0}
        population = list([random.randint(0, 8) for _ in range(6075)] for __ in range(self.limit_population))
        genome_1 = population[0]
        genome_2 = population[1]

        finish_nodes = []
        for x in range(int(self.finish[0].x), int(self.finish[1].x + 1)):
            for y in range(int(self.finish[0].y) , int(self.finish[1].y + 1)):
                finish_nodes.append((x, y))

        print(self.run_bot(genome_1, finish_nodes, matrix))

    def run_bot(self, genome, finish, matrix_distance):
        num_turns = 0
        position_cur = (int(self.start.x), int(self.start.y))
        position_prev = (int(self.start.x), int(self.start.y))
        for turn in range(self.limit_path):
            num_turns += 1
            sensors = self.get_sensors(position_cur, position_prev)
            inertia = (position_cur[0] - position_prev[0], position_cur[1] - position_prev[1])
            action = self.get_action(genome, inertia, sensors)
            position_cur, position_prev = (position_cur[0] + action[0], position_cur[1] + action[1]), position_cur
            if position_cur in finish:
                return 0, num_turns
            if self.map_mask.overlap(Line(
                    self.cell_display.get_coord_by_cell(pygame.Vector2(position_cur)),
                    self.cell_display.get_coord_by_cell(pygame.Vector2(position_prev))).get_mask(), (0, 0)):
                return matrix_distance[position_prev], num_turns

        return matrix_distance[position_cur], num_turns

    def get_sensors(self, position_cur, position_prev):
        if position_prev == position_cur:
            return (2, 2, 2)
        sensors_ahead = 2
        if self.map_mask.overlap(Line(
                self.cell_display.get_coord_by_cell(pygame.Vector2(position_cur)),
                self.cell_display.get_coord_by_cell(pygame.Vector2(self.up_line(position_cur, position_prev, 2)[0]))
            ).get_mask(), (0, 0)):
            sensors_ahead = 0
        elif self.map_mask.overlap(Line(
                self.cell_display.get_coord_by_cell(pygame.Vector2(position_cur)),
                self.cell_display.get_coord_by_cell(pygame.Vector2(self.up_line(position_cur, position_prev, 4)[0]))
            ).get_mask(), (0, 0)):
            sensors_ahead = 1

        sensors_right = 2
        if self.map_mask.overlap(Line(
                self.cell_display.get_coord_by_cell(pygame.Vector2(position_cur)),
                self.cell_display.get_coord_by_cell(pygame.Vector2(self.up_line(position_cur, self.shift_line(position_cur, position_prev, True), 2)[0]))
            ).get_mask(), (0, 0)):
            sensors_right = 0
        elif self.map_mask.overlap(Line(
                self.cell_display.get_coord_by_cell(pygame.Vector2(position_cur)),
                self.cell_display.get_coord_by_cell(pygame.Vector2(self.up_line(position_cur, self.shift_line(position_cur, position_prev, True), 4)[0]))
            ).get_mask(), (0, 0)):
            sensors_right = 1

        sensors_left = 2
        if self.map_mask.overlap(Line(
                self.cell_display.get_coord_by_cell(pygame.Vector2(position_cur)),
                self.cell_display.get_coord_by_cell(pygame.Vector2(self.up_line(position_cur, self.shift_line(position_cur, position_prev, False), 2)[0]))
            ).get_mask(), (0, 0)):
            sensors_left = 0
        elif self.map_mask.overlap(Line(
                self.cell_display.get_coord_by_cell(pygame.Vector2(position_cur)),
                self.cell_display.get_coord_by_cell(pygame.Vector2(self.up_line(position_cur, self.shift_line(position_cur, position_prev, False), 4)[0]))
            ).get_mask(), (0, 0)):
            sensors_left = 1

        print(sensors_ahead, sensors_right, sensors_left)

        return sensors_left, sensors_ahead, sensors_right

        # self.display.fill((255, 255, 255))
        # self.draw()
        # pygame.draw.line(self.display, 'red', self.cell_display.get_coord_by_cell(pygame.Vector2(position_cur)), self.cell_display.get_coord_by_cell(pygame.Vector2(self.up_line(position_cur, self.shift_line(position_cur, position_prev, False), 4)[0])))
        # pygame.draw.line(self.display, 'red', self.cell_display.get_coord_by_cell(pygame.Vector2(position_cur)),
        #                  self.cell_display.get_coord_by_cell(pygame.Vector2(
        #                      self.up_line(position_cur, self.shift_line(position_cur, position_prev, True), 4)[0])))
        # pygame.image.save(self.display, 'temp_5.jpeg')


    def shift_line(self, cur, prev, is_right):
        v = (prev[0] - cur[0], prev[1] - cur[1])
        l = (v[0]**2 + v[1]**2)**0.5
        v = (v[0] / l, v[1] / l)

        if is_right:
            cs = -sqrt(2) / 2
            sn = sqrt(2) / 2
        else:
            cs = -sqrt(2) / 2
            sn = - sqrt(2) / 2
        rx = v[0] * cs - v[1] * sn
        ry = v[0] * sn + v[1] * cs
        return cur[0] - rx, cur[1] - ry

    def up_line(self, cur, prev, length):
        v = (prev[0] - cur[0], prev[1] - cur[1])
        l = (v[0]**2 + v[1]**2)**0.5
        v = (v[0] / l, v[1] / l)

        return (cur[0] - v[0] * length, cur[1] - v[1] * length), prev



    def get_action(self, genome, inertia, sensors):
        """

        :param genome:
        :param inertia:
        :param sensors:
        :return:
        """
        idx = inertia[0] + inertia[1] * (7 * 2 + 1) + (sensors[0] + sensors[1] * 3 + sensors[2] * 9) * (7 * 2 + 1)**2
        action = ((0, 0), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))[genome[idx]]
        return min(inertia[0] + action[0], 7), min(inertia[1] + action[1], 7)

    def matrix_distances(self):
        finish_nodes = []
        for x in range(int(self.finish[0].x), int(self.finish[1].x + 1)):
            for y in range(int(self.finish[0].y) , int(self.finish[1].y + 1)):
                finish_nodes.append((x, y))

        matrix = {}
        for position in self.get_available_nodes((int(self.start.x), int(self.start.y))):
            matrix[position] = self.get_distance(position, finish_nodes)

        print(matrix)


    def get_distance(self, position, finish_position):
        queue_node = [position]
        visited = {}
        prev = {position: []}

        while queue_node:
            _node = queue_node.pop(0)
            if visited.get(_node) is not None:
                continue
            visited[_node] = True

            if _node in finish_position:
                return len(prev[_node])

            for acceleration in ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)):
                new_node = (_node[0] + acceleration[0], _node[1] + acceleration[1])
                if visited.get(new_node) is not None:
                    continue
                if self.map_mask.overlap(Line(
                        self.cell_display.get_coord_by_cell(pygame.Vector2(new_node)),
                        self.cell_display.get_coord_by_cell(pygame.Vector2(_node))).get_mask(), (0, 0)):
                    continue

                queue_node.append(new_node)
                if not prev.get(new_node):
                    prev[new_node] = prev[_node] + [new_node]

        return None

    def generate_matrix_2(self):
        finish_nodes = []
        for x in range(int(self.finish[0].x), int(self.finish[1].x + 1)):
            for y in range(int(self.finish[0].y), int(self.finish[1].y + 1)):
                finish_nodes.append((x, y))

        queue_node = finish_nodes
        visited = {}
        matrix = dict(zip(finish_nodes, [0 for _ in range(len(finish_nodes))]))

        while queue_node:
            _node = queue_node.pop(0)
            if visited.get(_node) is not None:
                continue
            visited[_node] = True

            for acceleration in ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)):
                new_node = (_node[0] + acceleration[0], _node[1] + acceleration[1])
                if visited.get(new_node) is not None:
                    continue
                if self.map_mask.overlap(Line(
                        self.cell_display.get_coord_by_cell(pygame.Vector2(new_node)),
                        self.cell_display.get_coord_by_cell(pygame.Vector2(_node))).get_mask(), (0, 0)):
                    continue
                if matrix.get(new_node) is None:
                    matrix[new_node] = matrix[_node] + 1
                queue_node.append(new_node)

        print(matrix)

        with open(self.level_path + '/distance_matrix.pickle', 'w+b') as file:
            pickle.dump(matrix, file)

        return None


if __name__ == '__main__':
    # sys.setrecursionlimit(2**15)
    pygame.init()
    display = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
    gl = GeneticLevel(display, '../levels/level_4').generate_matrix_2()
    # print(gl.get_sensors((18, 2), (19, 2)))
    # print(gl.up_line((18, 2), (19, 2), 2))
    # print(gl.shift_line((18, 2), (19, 2), True))
    # print(gl.shift_line((18, 2), (19, 2), False))
    # gl.fit()
    # "min_path": [[19, 2], [18, 3], [17, 4], [16, 4], [15, 4], [14, 5], [13, 5], [12, 5], [11, 6], [10, 6], [9, 7], [8, 8], [7, 9], [6, 10], [6, 11], [6, 12], [6, 13], [6, 14], [7, 15], [8, 16], [9, 17], [10, 17], [11, 18], [12, 18], [13, 19], [14, 19], [15, 19], [16, 19], [17, 20], [18, 20], [19, 20], [20, 20], [21, 20], [22, 20], [23, 20], [24, 20], [25, 20], [26, 20], [27, 19], [28, 19], [29, 19], [30, 19], [31, 18], [32, 18], [33, 17], [34, 17], [35, 16], [36, 15], [36, 14], [37, 13], [37, 12], [37, 11], [37, 10], [36, 9], [35, 8], [34, 7], [33, 6], [32, 6], [31, 5], [30, 5], [29, 5], [28, 5], [27, 4], [26, 4], [25, 4], [24, 4], [23, 4]]
