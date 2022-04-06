import pygame
from pygame.locals import *
import random

pygame.init()

WIDTH, HEIGHT = 600, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buscaminas")

BG_COLOR = (255, 255, 255)
COLORS = ((229, 194, 159), (51, 167, 242), (60, 225, 67), (234, 57, 65),
          (120, 63, 227), (255, 255, 255), (255, 255, 255), (255, 255, 255),
          (255, 255, 255))
BG_COLORS = ((229, 194, 159), (215, 184, 153), (167, 217, 72), (142, 204, 17))
FONT30 = pygame.font.SysFont("Arial", 20, True)
ROWS, COLS = 20, 20
MINES = 40


def get_adjacents(pos, rows, cols):
    adjacents = set()
    x, y = pos
    for row in range(x - 1, x + 2):
        for col in range(y - 1, y + 2):
            if (row >= 0 and col >= 0) and (row != x or col != y) and (row < rows and col < cols):
                adj = row, col
                adjacents.add(adj)

    return adjacents


def create_board(rows, cols, mines):
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    board_over = [[0 for _ in range(cols)] for _ in range(rows)]
    mines_pos = set()
    mines_created = 0

    while mines_created < mines:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        pos = row, col

        if pos not in mines_pos:
            mines_pos.add(pos)
            board[row][col] = -1
            mines_created += 1

    for mine in mines_pos:
        adjs = get_adjacents(mine, rows, cols)
        for adj in adjs:
            x, y = adj
            if board[x][y] != -1:
                board[x][y] += 1

    return board, board_over


def cave(row, col, board, board_over):
    if board[row][col] != 1 and board_over[row][col] == 0:
        board_over[row][col] = 1
        adjs = get_adjacents((row, col), ROWS, COLS)
        for adj in adjs:
            x, y = adj
            if board[x][y] == 0:
                return cave(x, y, board, board_over)

    return


def draw(win, board, board_over):
    win.fill(BG_COLOR)

    # Drawing the board
    min_size = min(HEIGHT // ROWS, WIDTH // COLS)
    row_size = min_size
    col_size = min_size
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * col_size, row *
                               row_size, col_size, row_size)

            if board_over[row][col] == 1:
                # Board style like chess
                if (row + col) % 2 == 0:
                    pygame.draw.rect(win, BG_COLORS[0], rect)
                else:
                    pygame.draw.rect(win, BG_COLORS[1], rect)

                value = board[row][col]
                if value == -1:
                    pygame.draw.circle(win, (44, 44, 44),
                                       rect.center, min_size // 4)
                elif value > 0:
                    number_text = FONT30.render(
                        str(value), True, COLORS[value])
                    text_rect = number_text.get_rect()
                    text_rect.center = rect.center
                    win.blit(number_text, text_rect)
                    # pygame.draw.rect(win, COLORS[value], rect)
            else:
                if (row + col) % 2 == 0:
                    pygame.draw.rect(win, BG_COLORS[2], rect)
                else:
                    pygame.draw.rect(win, BG_COLORS[3], rect)

    pygame.display.update()


def game_loop():
    board, board_over = create_board(ROWS, COLS, MINES)

    run = True
    mouse_pos = (0, 0)
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    min_size = min(HEIGHT // ROWS, WIDTH // COLS)
                    for row in range(ROWS):
                        for col in range(COLS):
                            rect = pygame.Rect(col * min_size, row *
                                               min_size, min_size, min_size)
                            if rect.collidepoint(*mouse_pos):
                                cave(int(rect.top / min_size),
                                     int(rect.left / min_size), board, board_over)

        draw(WIN, board, board_over)

    pygame.quit()


if __name__ == '__main__':
    game_loop()
