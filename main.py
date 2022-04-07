import pygame
from pygame.locals import *
from board import Board

pygame.init()

WIDTH, HEIGHT = 600, 630

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Buscaminas")

BG_COLOR = (230, 198, 166)
TEXT_COLOR = (241, 241, 241)
BG_BTN = (35, 202, 191)
ROWS, COLS = 20, 20
MINES = 40

# Game States
START = 0
WON = 1
PLAYING = 2
GAME_OVER = 3

# Fonts
FONT24 = pygame.font.SysFont("Arial", 20, True)
FONT40 = pygame.font.SysFont("Arial", 40, True)
FONT70 = pygame.font.SysFont("Arial", 70, True)
# Texts
TITLE = FONT70.render("MineSweeper", True, TEXT_COLOR)
PLAY_TEXT = FONT40.render("Play", True, TEXT_COLOR)
WIN_TEXT = FONT70.render("You Won!", True, TEXT_COLOR)
GAME_OVER_TEXT = FONT70.render("Game Over", True, TEXT_COLOR)

buttons = [
    {
        "text": FONT40.render("Play", True, TEXT_COLOR),
        "rect": pygame.Rect(0, 0, 140, 60)
    },
    {
        "text": FONT40.render("Play Again", True, TEXT_COLOR),
        "rect": pygame.Rect(0, 0, 140, 60)
    }
]


def draw(win: pygame.Surface, board: Board, state: int) -> None:
    win.fill(BG_COLOR)

    # Drawing the board
    board.render(win)

    if state == START:
        draw_home(win)
    elif state == GAME_OVER:
        draw_game_over(win)
    elif state == WON:
        draw_win(win)

    draw_mines_left(win, board)

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


def draw_button(win: pygame.Surface, button: dict):
    button["rect"].center = win.get_rect().center
    button["rect"].width = button["text"].get_rect().width + 40

    text_rect = button["text"].get_rect()
    text_rect.center = button["rect"].center

    pygame.draw.rect(win, BG_BTN, button["rect"])
    win.blit(button["text"], text_rect)


def draw_home(win: pygame.Surface):
    draw_layer(win)
    draw_text(win, TITLE)
    draw_button(win, buttons[0])


def draw_game_over(win: pygame.Surface):
    draw_layer(win)
    draw_text(win, GAME_OVER_TEXT)
    draw_button(win, buttons[1])


def draw_win(win: pygame.Surface):
    draw_layer(win)
    draw_text(win, WIN_TEXT)
    draw_button(win, buttons[1])


def draw_mines_left(win: pygame.Surface, board: Board):
    mines_text = FONT24.render(f"Mines: {MINES}", True, (10, 10, 10))
    flags_text = FONT24.render(
        f"Flags: {MINES - board.flags}", True, (225, 35, 35))

    win.blit(mines_text, (10, 605))
    win.blit(flags_text, (WIDTH - flags_text.get_rect().width - 10, 605))


def clicked_cell(board: Board, mouse_pos: tuple):
    for row in range(board.rows):
        for col in range(board.cols):
            cell = board.get_cell(row, col)
            if cell.collidepoint(*mouse_pos):
                return cell
    return None


def game_loop():
    board = Board(ROWS, COLS, MINES)
    state = START

    run = True
    mouse_pos = (0, 0)
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    board.restart(10, 10, 10)
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if state == PLAYING:
                    if pygame.mouse.get_pressed()[0] == 1:
                        cell = clicked_cell(board, mouse_pos)
                        if cell is not None:
                            board.dig(cell)
                            if cell.value == -1:
                                state = GAME_OVER

                        if board.has_won():
                            state = WON
                    if pygame.mouse.get_pressed()[2] == 1:
                        cell = clicked_cell(board, mouse_pos)
                        if cell is not None:
                            board.flags = cell.flag(board.flags)
                elif state == START:
                    if buttons[0]['rect'].collidepoint(*mouse_pos):
                        state = PLAYING
                elif state == WON or state == GAME_OVER:
                    if buttons[1]['rect'].collidepoint(*mouse_pos):
                        board.restart(ROWS, COLS, MINES)
                        state = PLAYING

        draw(WIN, board, state)

    pygame.quit()


if __name__ == '__main__':
    game_loop()
