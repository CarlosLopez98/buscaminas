import pygame
from pygame.locals import *
from board import Board

pygame.init()

WIDTH, HEIGHT = 600, 600

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


def clicked_cell(board: Board, mouse_pos: tuple):
    for row in range(ROWS):
        for col in range(COLS):
            cell = board.get_cell(row, col)
            if cell.collidepoint(*mouse_pos):
                return cell
    return None


def game_loop():
    board = Board(ROWS, COLS, MINES)

    run = True
    mouse_pos = (0, 0)
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0] == 1:
                    cell = clicked_cell(board, mouse_pos)
                    if cell is not None:
                        board.dig(cell)
                if pygame.mouse.get_pressed()[2] == 1:
                    cell = clicked_cell(board, mouse_pos)
                    if cell is not None:
                        cell.flag()

        draw(WIN, board)

    pygame.quit()


if __name__ == '__main__':
    game_loop()
