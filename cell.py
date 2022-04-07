import pygame

GROUND = 0
DIGGED = 1
FLAG = 2


class Cell(pygame.Rect):

    def __init__(self, left: float, top: float, width: float, height: float, pos: tuple, value: int = 0):
        super(Cell, self).__init__(left, top, width, height)
        self.pos = pos
        self.state = GROUND
        self.value = value

    def dig(self):
        self.state = DIGGED

    def flag(self, num: int) -> int:
        if self.state == GROUND:
            self.state = FLAG
            num += 1
        elif self.state == FLAG:
            self.state = GROUND
            num -= 1

        return num
