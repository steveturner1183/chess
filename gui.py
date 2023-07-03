# Required for pygame
import pygame as pg
import pygame.transform
from pygame.locals import *

# Required for Chess
from chess import Chess
from player import *

# Other imports
import os


class ChessInterface:
    def __init__(self):
        # Pygame initialization
        pg.init()
        pg.font.init()
        pg.display.set_caption("Chess")
        self._win_width = 800
        self._win_height = 600
        self._win = pg.display.set_mode((self._win_width, self._win_height))
        self._fps = 60
        self._font = pg.font.SysFont("Comic Sans MS", 30)

        # Colors
        self._color_main_bg = (211, 211, 211)
        self._color_dark_tile = (118, 150, 86)
        self._color_light_tile = (238, 238, 210)
        self._color_menu = "gray"
        self._color_active_text = "yellow"
        self._color_inactive_text = "black"
        self._color_active_button = "yellow"
        self._color_inactive_button = "white"
        self._font_type = "Comic Sans MS"

        # Images
        self._image_w_piece, self._image_b_piece, self._image_bg = None, None, None
        self.load_images()

        # Required for chess game
        self._game_options = ["START", "COLOR", "GAME", "QUIT"]
        self._board_size = self._win_height * .95

        self._tile_size = int(self._board_size / 8)
        self._board_origin = ((self._win_width - self._board_size)/2-(self._win_width-self._win_height)/2, (self._win_height-self._board_size)/2)
        self._colors = None
        self._cols = None
        self._rows = None
        self._piece_images = dict()
        self._chess = None
        self._display_board = None
        self._p1 = None
        self._p2 = None

    def load_images(self):
        scale = (100, 100)
        # Load piece images for color selection
        w_piece = pg.image.load(os.path.join("Assets", "W_King.png"))
        self._image_w_piece = pygame.transform.scale(w_piece, scale)

        b_piece = pg.image.load(os.path.join("Assets", "B_King.png"))
        self._image_b_piece = pygame.transform.scale(b_piece, scale)

        # Load image for start background
        scale = (self._win_width, self._win_height)
        bg = pg.image.load(os.path.join("Assets", "Start_Background.PNG"))
        self._image_bg = pg.transform.scale(bg, scale)


    def run_game(self):
        run = True
        clock = pg.time.Clock()
        game_state = 0
        game_flow = {
            "START": self.start_window,
            "COLOR": self.select_color,
            "GAME": self.play_chess,
            "QUIT": self.end_screen
        }

        while run:
            clock.tick(self._fps)

            game_option = self._game_options[game_state]
            run_option = game_flow[game_option]()
            if run_option is True:
                game_state += 1
            elif run_option == "Restart":
                game_state = 1
            else:
                run = False

        pg.quit()

    def play_chess(self):

        # Initialize game
        self.initialize_game(self._colors[0], self._colors[1])
        run = True
        start_loc = None
        selected_piece = None
        # draw board
        self.initialize_board()

        while run:
            self._win.fill(self._color_main_bg)
            self.draw_board()
            self.set_pieces(selected_piece)
            self.player_display()
            for event in pg.event.get():

                # User exits game by clicking X
                if event.type == pg.QUIT:
                    return False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        loc = self.get_square_coordinate()
                        if loc is not None:
                            selected_piece = self._chess.get_board_location(loc)
                            start_loc = loc

                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        selected_piece = None
                        end_loc = self.get_square_coordinate()
                        if start_loc is not None and end_loc is not None:
                            move = start_loc + " " + end_loc

                            valid_move = self._chess.validate_move(move)
                            if valid_move:
                                self._chess.make_move(move)
                                self._chess.king_check_status()
                                if self._chess.get_game_status() != "INCOMPLETE":
                                    run = False
                                self._chess.set_player_turn()

            pg.display.update()

        return True

    def start_window(self):
        # Create window
        width = self._win_width
        height = self._win_height

        start_win = pg.Surface((width, height))

        # End when start button pressed
        run = True
        clock = pg.time.Clock()

        while run:
            clock.tick(self._fps)

            # Add image background
            start_win.blit(self._image_bg, (0, 0))

            # Add start button
            x = self._win_width / 2
            y = self._win_height * .1
            text = "Play Chess"
            start_button = self.create_display_text(x, y, text, start_win, False, True)

            # Display start window
            self._win.blit(start_win, (0, 0))
            pg.display.update()

            event = pg.event.wait()

            if event.type == pg.QUIT:
                return False

            elif event.type == pg.MOUSEBUTTONDOWN:
                if start_button.collidepoint(pg.mouse.get_pos()):
                    run = False

        return True

    def select_color(self):
        # Create window
        width = int(self._win_width * .5)
        height = int(self._win_height * .5)
        color_window = pg.Surface((width, height))
        color_window.fill(self._color_menu)

        run = True
        clock = pg.time.Clock()
        colors = None

        while run:
            clock.tick(self._fps)

            # Display text
            text = "Select a Color"
            text_x = color_window.get_width() * .5
            text_y = color_window.get_height() * .25
            self.create_display_text(text_x, text_y, text, color_window, True, True)

            # Create color selection buttons
            height = self._image_w_piece.get_height()
            width = self._image_w_piece.get_width()
            wh_x = color_window.get_width() * .25 - width / 2
            bl_x = color_window.get_width() * .75 - height / 2
            y = color_window.get_height() * .5

            w_button = self.create_button(height, width, wh_x, y, color_window, self._image_w_piece)
            b_button = self.create_button(height, width, bl_x, y, color_window, self._image_b_piece)

            color_window_pos = self.center_on_window(color_window)
            self._win.blit(color_window, color_window_pos)

            # Wait for button to be pressed
            event = pg.event.wait()
            if event.type == pg.QUIT:
                return False

            # Return selection
            elif event.type == pg.MOUSEBUTTONDOWN:
                mos_pos = pg.mouse.get_pos()
                mos_x = mos_pos[0] - color_window_pos[0]
                mos_y = mos_pos[1] - color_window_pos[1]

                if w_button.collidepoint(mos_x, mos_y):
                    colors = "W", "B"
                    run = False
                elif b_button.collidepoint(mos_x, mos_y):
                    colors = "B", "W"
                    run = False

            pg.display.update()

        self._colors = colors
        return True

    def center_on_window(self, surface):
        height = surface.get_height()
        width = surface.get_width()
        x_offset = (self._win.get_width() - width) / 2
        y_offset = (self._win.get_height() - height) / 2
        return x_offset, y_offset

    def initialize_game(self, p1_color, p2_color):
        p1 = Player(1, p1_color)
        p2 = Player(2, p2_color)
        chess = Chess(p1, p2)
        self._cols = chess.get_cols_and_rows()[0]
        self._rows = chess.get_cols_and_rows()[1][::-1]
        self._chess = chess
        self._p1 = p1
        self._p2 = p2
        return

    def initialize_board(self):
        display_board = pg.Surface((self._board_size, self._board_size))
        tile_color = self._color_dark_tile

        for row in range(8):
            for col in range(8):
                y_loc = row * self._tile_size
                x_loc = col * self._tile_size
                square = pg.Rect(x_loc, y_loc, self._tile_size, self._tile_size)
                tile_color = self._color_dark_tile if tile_color == self._color_light_tile else self._color_light_tile
                pg.draw.rect(display_board, tile_color, square)

            tile_color = self._color_dark_tile if tile_color == self._color_light_tile else self._color_light_tile

        self._display_board = display_board

    def draw_board(self):
        self._win.blit(self._display_board, self._board_origin)

    def set_pieces(self, selected_piece):
        game_board = self._chess.get_board()

        for row in game_board:
            for piece in row:
                if piece is not None:
                    image = pygame.image.load(piece.get_image_path())

                    if piece == selected_piece:
                        mos_pos_x, mos_pos_y = pg.mouse.get_pos()
                        mos_pos_x -= image.get_width() / 2
                        mos_pos_y -= image.get_height() / 2
                        piece_loc = mos_pos_x, mos_pos_y
                        self._win.blit(image, piece_loc)

                    else:
                        x_offset = self._board_origin[0] + (
                                self._tile_size - image.get_size()[0]) / 2
                        y_offset = self._board_origin[0] + (
                                self._tile_size - image.get_size()[1]) / 2
                        x, y = self.convert_chess_cord(piece.get_location())
                        x += x_offset
                        y += y_offset

                        self._win.blit(image, (x, y))

    def convert_chess_cord(self, chess_cord):
        col = self._cols.index(chess_cord[0]) * self._tile_size
        row = self._rows.index(chess_cord[1]) * self._tile_size
        return col, row

    def get_square_coordinate(self):
        mouse_pos = pg.mouse.get_pos()
        board_pos = None

        col_pos = int((mouse_pos[0] - self._board_origin[0]) // self._tile_size)
        row_pos = int((mouse_pos[1] - self._board_origin[1]) // self._tile_size)

        if col_pos in range(8) and row_pos in range(8):
            board_pos = self._cols[col_pos] + self._rows[row_pos]
        else:
            print("Out of range")

        return board_pos

    def player_display(self):
        font = pg.font.SysFont(self._font_type, 27)
        text_height = font.get_height()
        left_edge = self._board_origin[0] + self._board_size + self._tile_size/4
        top_height = self._board_origin[1]
        bot_height = top_height + self._board_size - text_height

        p1_text = font.render("Player 1", False, self._color_inactive_text)
        self._win.blit(p1_text, (left_edge, bot_height))

        p2_text = font.render("Player 2", False, self._color_inactive_text)
        self._win.blit(p2_text, (left_edge, top_height))

        self.display_captured_pieces(left_edge, bot_height - text_height, self._p2.get_captured_pieces())
        self.display_captured_pieces(left_edge, top_height + text_height, self._p1.get_captured_pieces())

    def display_captured_pieces(self, left_edge, height, captured_pieces):
        pieces = {
            "Pawn": [],
            "Bishop": [],
            "Knight": [],
            "Rook": [],
            "Queen": []
        }

        offset = left_edge-8
        p1_captures = captured_pieces

        for piece in p1_captures:
            image = pg.transform.scale(pg.image.load(piece.get_image_path()), (30, 30))
            pieces[piece.get_name()].append(image)

        for piece_type in pieces:
            for image in pieces[piece_type]:
                self._win.blit(image, (offset, height))
                offset += image.get_width() * .2
            if len(pieces[piece_type]) > 0:
                offset += self._tile_size * .3

    def end_screen(self):
        # Create window
        width = int(self._win_width * .5)
        height = int(self._win_height * .5)
        end_window = pg.Surface((width, height))
        end_window.fill(self._color_menu)

        run = True
        clock = pg.time.Clock()

        while run:
            clock.tick(self._fps)

            # Display text
            winner_text = self._chess.get_game_status()
            winner_text_x = end_window.get_width() * .5
            winner_text_y = end_window.get_height() * .25
            self.create_display_text(winner_text_x, winner_text_y, winner_text, end_window,
                                     True, True)

            # Display text
            restart_text = "Play Again?"
            restart_text_x = end_window.get_width() * .5
            restart_text_y = end_window.get_height() * .75
            restart = self.create_display_text(restart_text_x, restart_text_y, restart_text, end_window,
                                     False, True)

            end_window_pos = self.center_on_window(end_window)
            self._win.blit(end_window, end_window_pos)

            # Wait for button to be pressed
            event = pg.event.wait()
            if event.type == pg.QUIT:
                return False

            # Return selection
            elif event.type == pg.MOUSEBUTTONDOWN:
                mos_pos = pg.mouse.get_pos()
                mos_x = mos_pos[0] - end_window_pos[0]
                mos_y = mos_pos[1] - end_window_pos[1]

                if restart.collidepoint(mos_x, mos_y):
                    run = False

            pg.display.update()

        return "Restart"

    def create_button(self, height, width, x, y, surface, image):
        button_rect = pg.Rect(x, y, width, height)
        mos_pos = pg.mouse.get_pos()
        mos_x = mos_pos[0] - (self._win.get_width() - surface.get_width()) / 2
        mos_y = mos_pos[1] - (self._win.get_height() - surface.get_height()) / 2

        button_active = button_rect.collidepoint(mos_x, mos_y)

        if button_active:
            pg.draw.rect(surface, self._color_active_button, button_rect)
        else:
            pg.draw.rect(surface, self._color_inactive_button, button_rect)

        inside_button = button_rect.inflate(-5, -5)
        pg.draw.rect(surface, self._color_inactive_button, inside_button)
        surface.blit(image, (x, y))

        return inside_button

    def create_display_text(self, x, y, text, surface, static, centered):
        width, height = self._font.size(text)
        if centered is True:
            x = x - width/2
            y = y - height/2
        button_rect = Rect(x, y, width, height)
        mos_pos = pg.mouse.get_pos()
        mos_x = mos_pos[0] - (self._win.get_width() - surface.get_width()) / 2
        mos_y = mos_pos[1] - (self._win.get_height() - surface.get_height()) / 2


        active = self._color_active_text
        inactive = self._color_inactive_text

        if static is True:
            active = inactive

        if button_rect.collidepoint(mos_x, mos_y):
            button = self._font.render(text, False, active)
        else:
            button = self._font.render(text, False, inactive)

        surface.blit(button, (x, y))

        return button_rect


if __name__ == "__main__":
    game = ChessInterface()
    game.run_game()
