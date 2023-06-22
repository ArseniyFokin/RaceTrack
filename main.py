"""

"""
import sys
import pygame

from displays import Menu, Editor, SwitchDisplay, SelectLevel
from consts import WINDOW_HEIGHT, WINDOW_WIDTH, Color, StateDisplay


class Main:
    """

    """
    def __init__(self) -> None:
        """

        """
        self.display = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('RaceTrack')
        self.switch_display = SwitchDisplay(self.display, StateDisplay.MENU)

        self.editor = Editor(self.display, self.switch_display)
        self.menu = Menu(self.display, self.switch_display)
        self.select_level = SelectLevel(self.display, self.switch_display)

        self.__state_run = True
        self.__clock = pygame.time.Clock()

    def run(self) -> None:
        """

        """
        while self.__state_run:
            # self.__clock.tick_busy_loop(FPS)
            self.display.fill(Color.WINDOW_COLOR)
            match self.switch_display.state_display:
                case StateDisplay.MENU:
                    self.menu.draw()
                case StateDisplay.EDITOR:
                    self.editor.draw()
                case StateDisplay.SELECT_LEVEL:
                    self.select_level.draw()
                case StateDisplay.LEVEL:
                    self.select_level.draw_level()
                case _:
                    pygame.quit()
                    self.__state_run = False
                    break

            if self.__state_run:
                self.switch_display.draw()
                pygame.display.update()


if __name__ == '__main__':
    sys.setrecursionlimit(10240)
    pygame.init()
    pygame.font.init()
    main = Main()
    main.run()
