import pygame


class Cell(pygame.Rect):

    def __init__(self, left: float, top: float, width: float, height: float, value: int = 0):
        super(Cell, self).__init__(left, top, width, height)
        self.state = True
        self.value = value

    def open(self):
        self.state = True
