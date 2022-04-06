import pygame
from pygame.locals import *
from board import Board

pygame.init()

WIDTH, HEIGHT = 600, 700

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buscaminas")

BG_COLOR = (255, 255, 255)
ROWS, COLS = 20, 20
MINES = 40


def draw(win, board: Board) -> None:
    win.fill(BG_COLOR)

    # Drawing the board
    board.render(win)

    pygame.display.update()


def game_loop():
    board = Board(ROWS, COLS, MINES)

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

        draw(WIN, board)

    pygame.quit()


if __name__ == '__main__':
    game_loop()
