import pygame as pg
import os
from pygame.locals import *
from chess import Chess

WIDTH, HEIGHT = 1200, 700
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Chess")

BOARD_SIZE = 600  # Even number
TILE_SIZE = int(BOARD_SIZE / 8)
BOARD_ORIGIN = (50, 50)
BACKGROUND = (255, 80, 255)
DARK = (220, 220, 220)
LIGHT = (50, 50, 50)
FPS = 60
CHESS = Chess()

def draw_window(selected_piece):
    WIN.fill(BACKGROUND)
    WIN.blit(draw_board(), BOARD_ORIGIN)
    set_pieces(selected_piece)

    pg.display.update()

def draw_board():
    board_origin = 0
    board = pg.Surface((BOARD_SIZE, BOARD_SIZE))
    tile_color = DARK

    for row in range(8):
        for col in range(8):
            square = pg.Rect(row*TILE_SIZE, col*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            tile_color = DARK if tile_color == LIGHT else LIGHT
            pg.draw.rect(board, tile_color, square)

        tile_color = DARK if tile_color == LIGHT else LIGHT

    return board

def set_pieces(selected_piece):
    board = CHESS.get_board_state()
    for location in board:
        if board[location] is not None:
            image = pg.image.load(board[location].get_image_path())
            if board[location] == selected_piece:
                WIN.blit(image, pg.mouse.get_pos())
            else:
                x, y = convert_chess_cord(location)
                x += TILE_SIZE / 4
                y += TILE_SIZE / 4
                WIN.blit(image, (x, y))

def convert_chess_cord(chess_cord):
    cols = "abcdefgh"
    rows = "87654321"
    col = cols.index(chess_cord[0]) * TILE_SIZE + BOARD_ORIGIN[0]
    row = rows.index(chess_cord[1]) * TILE_SIZE + BOARD_ORIGIN[1]
    return col, row

def get_square_coordinate():
    cols = "abcdefgh"
    rows = "87654321"
    mouse_pos = pg.mouse.get_pos()
    board_pos = None

    col_pos = int((mouse_pos[0] - BOARD_ORIGIN[0]) // TILE_SIZE)
    row_pos = int((mouse_pos[1] - BOARD_ORIGIN[1]) // TILE_SIZE)

    if col_pos in range(8) and row_pos in range(8):
        board_pos = cols[col_pos] + rows[row_pos]
        print(board_pos)
    else:
        print("Out range")

    return board_pos

def main():
    selected_piece = None
    start_loc = None
    end_loc = None
    clock = pg.time.Clock()
    run = True

    while run:
        ### TO MUCH POWA
        # Event wait??

        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    loc = get_square_coordinate()
                    if loc is not None:
                        selected_piece = CHESS.get_board_state()[loc]
                        start_loc = loc
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    selected_piece = None
                    end_loc = get_square_coordinate()
                    if end_loc is not None:
                        move = start_loc + " " + end_loc
                        valid_move = CHESS.check_game_rules(move)
                        if valid_move:
                            CHESS.make_move(move[:2], move[-2:])
                            CHESS.set_player_turn()

        draw_window(selected_piece)

    pg.quit()


if __name__ == "__main__":
    main()