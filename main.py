import pygame
from pygame.locals import *
from board import Board

pygame.init()

WIDTH, HEIGHT = 600, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buscaminas")

BG_COLOR = (255, 255, 255)
ROWS, COLS = 10, 10
MINES = 10

FONT70 = pygame.font.SysFont("Arial", 70, True)
WIN_TEXT = FONT70.render("You Won!", True, (255, 255, 255))
GAME_OVER_TEXT = FONT70.render("Game Over", True, (255, 255, 255))


def draw(win: pygame.Surface, board: Board, game_over: bool, won: bool) -> None:
    win.fill(BG_COLOR)

    # Drawing the board
    board.render(win)

    if game_over:
        draw_game_over(win)
    elif won:
        draw_win(win)

    pygame.display.update()


def draw_layer(win: pygame.Surface):
    layer = pygame.Surface((WIDTH, HEIGHT))
    layer.set_alpha(100)
    layer.fill((0, 0, 0))
    win.blit(layer, (0, 0))


def draw_text(win: pygame.Surface, text: pygame.Surface):
    text_rect = text.get_rect()
    text_rect.centerx = win.get_rect().centerx
    text_rect.centery = 200
    win.blit(text, text_rect)


def draw_game_over(win: pygame.Surface):
    draw_layer(win)
    draw_text(win, GAME_OVER_TEXT)


def draw_win(win: pygame.Surface):
    draw_layer(win)
    draw_text(win, WIN_TEXT)


def clicked_cell(board: Board, mouse_pos: tuple):
    for row in range(ROWS):
        for col in range(COLS):
            cell = board.get_cell(row, col)
            if cell.collidepoint(*mouse_pos):
                return cell
    return None


def game_loop():
    board = Board(ROWS, COLS, MINES)
    won = False
    game_over = False

    run = True
    mouse_pos = (0, 0)
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not game_over:
                    if pygame.mouse.get_pressed()[0] == 1:
                        cell = clicked_cell(board, mouse_pos)
                        if cell is not None:
                            board.dig(cell)
                            if cell.value == -1:
                                game_over = True

                        if board.has_won():
                            won = True
                    if pygame.mouse.get_pressed()[2] == 1:
                        cell = clicked_cell(board, mouse_pos)
                        if cell is not None:
                            cell.flag()

        draw(WIN, board, game_over, won)

    pygame.quit()


if __name__ == '__main__':
    game_loop()
