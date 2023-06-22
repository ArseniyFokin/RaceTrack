import pygame

from consts import WINDOW_CENTER, FPS, Color


class SwitchDisplay:
    """
    Класс реализующий хранение и изменение дисплеев
    """
    def __init__(self, display: pygame.Surface, state_display: int):
        """
        Инициализация

        :param state_display: Текущий дисплей
        """
        self.display = display
        self.radius = pygame.math.Vector2(WINDOW_CENTER).magnitude()
        self.__state_display = state_display

        self.__activated = None
        self.__temp_state_display = None
        self.__border_width = None
        self.__direction_circle = None
        self.__reset_temp_params()

    def is_active(self):
        return self.__activated

    def __reset_temp_params(self):
        """

        :return:
        """
        self.__activated = False
        self.__temp_state_display = self.state_display
        self.__border_width = 0
        self.__direction_circle = 1

    @property
    def state_display(self) -> int:
        """
        Текущее состояние дисплея

        :return:
        """
        return self.__state_display

    @state_display.setter
    def state_display(self, value: int):
        """
        Установка нового состояние дисплея

        :param value: Новое значение
        :return:
        """
        self.__temp_state_display = value
        self.__activated = True

    def draw(self) -> None:
        """

        :return:
        """
        if not self.__activated:
            return

        self.__border_width += self.__direction_circle * self.radius / FPS * 4
        if self.__border_width >= self.radius:
            self.__direction_circle = -1
            self.__state_display = self.__temp_state_display

        if self.__border_width < 0:
            self.__reset_temp_params()
            return

        pygame.draw.circle(self.display, Color.PAINT_COLOR, WINDOW_CENTER, self.radius, int(self.__border_width))
