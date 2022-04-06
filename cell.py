import pygame

GROUND = 0
DIGGED = 1
FLAG = 2


class Cell(pygame.Rect):

    def __init__(self, left: float, top: float, width: float, height: float, value: int = 0):
        super(Cell, self).__init__(left, top, width, height)
        self.state = DIGGED
        self.value = value

    def open(self):
        self.state = DIGGED

    def mark(self):
        self.state = FLAG
