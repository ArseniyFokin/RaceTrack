"""

"""

FPS = 60
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_WIDTH_SHIFT = WINDOW_WIDTH // 4
WINDOW_HEIGHT_SHIFT = WINDOW_HEIGHT // 4
WINDOW_WIDTH_CENTER = WINDOW_WIDTH // 2
WINDOW_HEIGHT_CENTER = WINDOW_HEIGHT // 2
WINDOW_CENTER = (WINDOW_WIDTH_CENTER, WINDOW_HEIGHT_CENTER)


class StateDisplay:
    """

    """
    MENU = 0
    EDITOR = 1
    SELECT_LEVEL = 2
    LEVEL = 3
    EXIT = 4


class Color:
    """

    """
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)

    WINDOW_COLOR = WHITE
    PAINT_COLOR = BLUE


class Location:
    """

    """
    TOP_LEFT = 'topleft'
    CENTER = 'center'
    BOTTOM_RIGHT = 'bottomright'
