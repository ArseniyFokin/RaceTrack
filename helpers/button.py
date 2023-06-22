from typing import Optional

import pygame

from consts import Location


class Button:
    def __init__(self, display, x: int, y: int, image, scale: Optional[float] = 1, is_mask: bool = True,
                 location: str = Location.CENTER, size: tuple[int, int] = None, ext_data: dict = None):
        """

        :param display:
        :param x:
        :param y:
        :param image:
        :param scale:
        """
        self.is_mask = is_mask
        self.display = display
        size = size or (int(image.get_width() * scale), int(image.get_height() * scale))
        self.image = pygame.transform.scale(image, size)
        self.mask = pygame.mask.from_surface(self.image)
        self.rec = self.image.get_rect(**{location: (x, y)})
        self.ext_data = ext_data

        self._clicked = False

    def check_click(self):
        """

        :return:
        """
        self.display.blit(self.image, self.rec)

        action = False
        pos = pygame.mouse.get_pos()
        if not self._clicked and pygame.mouse.get_pressed()[0] == 1 and self.rec.collidepoint(pos) \
                and (self.is_mask is False or self.mask.get_at((pos[0] - self.rec.x, pos[1] - self.rec.y))):
            self._clicked = True
            action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self._clicked = False

        return action
