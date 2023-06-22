class Strategy:
    def __init__(self, start: tuple[int, int], finishes: dict[tuple[int, int], bool], limit: int):
        """
        Инициализация стратегии

        :param start: Стартовая позиция
        :param finishes: Финальные позиции
        """
        self.start = start
        self.finishes = finishes
        self.limit = limit

    @staticmethod
    def get_available_moves(current_point: tuple[int, int], prev_point: tuple[int, int]) -> list[tuple]:
        """
        Доступные позиции

        :param current_point: Текущая позиция
        :param prev_point: Предыдущая позиция
        :return: Список доступных вершин
        """
        result = []
        new_center = (current_point[0] * 2 - prev_point[0], current_point[1] * 2 - prev_point[1])
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                result.append((new_center[0] + i, new_center[1] + j))

        return result

    @staticmethod
    def get_distance(point_1: tuple[int, int], point_2: tuple[int, int]) -> float:
        """
        Евклидово расстояние между точками

        :param point_1: Точка 1
        :param point_2: Точка 2
        :return: Расстояние
        """
        return ((point_2[0] - point_1[0])**2 + (point_2[1] - point_1[1])**2)**0.5

    def get_next_point(self, point_1: tuple[int, int], point_2: tuple[int, int]):
        """
        :param point_1: Точка 1
        :param point_2: Точка 2
        :return:
        """
        return None, None
