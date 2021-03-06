import pygame
import random
from cell import Cell
from cell import GROUND, DIGGED, FLAG

pygame.font.init()

COLORS = ((229, 194, 159), (51, 167, 242), (60, 225, 67), (234, 57, 65),
          (120, 63, 227), (242, 56, 23), (16, 172, 122), (172, 16, 132),
          (16, 18, 172))
BG_COLORS = ((242, 208, 174), (230, 198, 166), (167, 217, 72), (142, 204, 17))
FONT30 = pygame.font.SysFont("Arial", 24, True)


class Board:

    def __init__(self, rows: int, cols: int, mines: int) -> None:
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.flags = 0
        self.mines_pos = set()
        self.cells = None

        self.create()

    def render(self, win: pygame.Surface):
        # Drawing the board
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                if cell.state == DIGGED:
                    # Board style like chess
                    if (row + col) % 2 == 0:
                        pygame.draw.rect(win, BG_COLORS[0], cell)
                    else:
                        pygame.draw.rect(win, BG_COLORS[1], cell)

                    if cell.value == -1:
                        pygame.draw.circle(win, (44, 44, 44), cell.center, 8)
                    elif cell.value > 0:
                        number_text = FONT30.render(
                            str(cell.value), True, COLORS[cell.value])
                        text_rect = number_text.get_rect()
                        text_rect.center = cell.center
                        win.blit(number_text, text_rect)
                        # pygame.draw.rect(win, COLORS[value], rect)
                elif cell.state == GROUND:
                    if (row + col) % 2 == 0:
                        pygame.draw.rect(win, BG_COLORS[2], cell)
                    else:
                        pygame.draw.rect(win, BG_COLORS[3], cell)
                elif cell.state == FLAG:
                    # draw the flag
                    pygame.draw.rect(win, (255, 0, 0), cell)

    def restart(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.flags = 0
        self.mines_pos.clear()
        self.cells = None

        self.create()

    def create(self) -> None:
        win = pygame.display.get_surface()
        min_size = min(win.get_height() // self.rows,
                       win.get_width() // self.cols)

        self.cells = [[Cell(col * min_size, row * min_size, min_size, min_size, (row, col))
                       for col in range(self.cols)] for row in range(self.rows)]

        self.create_mines()

        for mine in self.mines_pos:
            adjs = self.get_adjacents(mine)
            for adj in adjs:
                if adj.value != -1:
                    adj.value += 1

    def has_won(self) -> bool:
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                if cell.state == GROUND or cell.state == FLAG:
                    count += 1

        if self.mines == count:
            return True
        else:
            return False

    def create_mines(self) -> None:
        mines_created = 0

        while mines_created < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            pos = row, col

            if pos not in self.mines_pos:
                self.mines_pos.add(pos)
                cell = self.cells[row][col]
                cell.value = -1
                mines_created += 1

    def get_cell(self, row: int, col: int) -> Cell:
        return self.cells[row][col]

    def get_adjacents(self, pos: tuple):
        adjacents = []

        x, y = pos
        for row in range(x - 1, x + 2):
            x, y = pos
            for col in range(y - 1, y + 2):
                if (row >= 0 and col >= 0) and (row != x or col != y) and (row < self.rows and col < self.cols):
                    adjacents.append(self.get_cell(row, col))

        return adjacents

    def dig(self, cell: Cell):
        if cell.state == GROUND:
            cell.dig()
            if cell.value == 0:
                beside = self.get_adjacents(cell.pos)
                for side in beside:
                    self.dig(side)
