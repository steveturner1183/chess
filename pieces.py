from copy import deepcopy

class PieceSet:
    def __init__(self, p1_color):
        """
        Creates a roster for player 1 and 2 to use at the beginning of the game

        :param p1_color: White or black piece color chosen. Determines positions
        of King and Queen
        """

        # Chess rule - Queen will always go on their own color
        if p1_color == "W":
            p2_color = "B"
            k_loc = "e1", "e8"
            q_loc = "d1", "d8"
        else:
            p2_color = "W"
            k_loc = "d1", "d8"
            q_loc = "e1", "e8"

        self._p1_roster = [Rook("a1"), Knight("b1"), Bishop("c1"),
                           Queen(q_loc[0]), King(k_loc[0]), Bishop("f1"),
                           Knight("g1"), Rook("h1"), Pawn("a2"),
                           Pawn("b2"), Pawn("c2"), Pawn("d2"), Pawn("e2"),
                           Pawn("f2"), Pawn("g2"), Pawn("h2")]

        self._p2_roster = [Rook("a8"), Knight("b8"), Bishop("c8"),
                           Queen(q_loc[1]), King(k_loc[1]), Bishop("f8"),
                           Knight("g8"), Rook("h8"), Pawn("a7"),
                           Pawn("b7"), Pawn("c7"), Pawn("d7"), Pawn("e7"),
                           Pawn("f7"), Pawn("g7"), Pawn("h7")]

        for piece in self._p1_roster:
            piece.set_player(1)
            piece.set_image_path(p1_color)

        for piece in self._p2_roster:
            piece.set_player(2)
            piece.set_image_path(p2_color)

    def get_piece_sets(self):
        return self._p1_roster, self._p2_roster

    def get_king(self, player):
        if player == 1:
            return self._p1_roster[4]
        else:
            return self._p2_roster[4]


class GamePiece:
    def __init__(self, location):
        self._button = None
        self._image_path = None
        self._player = None
        self._name = None
        self._cur_loc = location
        self._rows = "12345678"   # CHANGE THIS PLZ
        self._rows_2 = "87654321"   # CHANGE THIS PLZ
        self._cols = "abcdefgh"

        self._directions = {"N": (0, 1), "NE": (1, 1), "E": (1, 0),
                            "SE": (1, -1), "S": (0, -1), "SW": (-1, -1),
                            "W": (-1, 0), "NW": (-1, 1)}

        self._move_set = []
        self._max_move = 7
        self._possible_moves = dict()

    def __repr__(self):
        return repr("P" + str(self._player) + "-" + self._name + "-" + self._cur_loc)

    def set_button(self, button):
        self._button = button

    def get_button(self):
        return self._button

    def set_image_path(self, color):
        path = color + "_" + self._name + ".PNG"
        self._image_path = path

    def get_image_path(self):
        return self._image_path

    def set_player(self, player):
        self._player = player

    def get_player(self):
        return self._player

    def set_location(self, location):
        self._cur_loc = location

    def get_location(self):
        return self._cur_loc

    def get_name(self):
        return self._name

    def format_grid_loc(self, col, row):
        return self._cols[col] + self._rows[row]

    def get_grid_col_row(self, location): ########################### CHANGE THESE TO BOARD
        col = location[0]
        row = location[1]
        return self._cols.index(col), self._rows.index(row)

    def add_move(self, move):
        self._possible_moves.update(move)

    def get_board_col_row(self, loc: str) -> (int, int):
        """
        Returns board grid coordinates for given location
        :param loc: Chess coordinate location, example "a1"
        :return: Grid coordinates for given location
        """
        col, row = loc[0], loc[1]
        return self._cols.index(col), self._rows.index(row)

    def get_board_loc(self, loc: str, board):
        """
        Retrieves value at given board location
        :param loc: Chess coordinate location, example "a1"
        :return: Piece if piece at given location, otherwise None
        """
        col, row = self.get_board_col_row(loc)
        return board[7-row][col]

    def get_possible_moves(self, board):
        self._possible_moves.clear()
        for directional_move in self._move_set:
            path = []
            valid_move = True

            move_step = self._directions[directional_move]
            col, row = board.get_board_col_row(self._cur_loc)

            col += move_step[0]  # starting loc
            row += move_step[1]
            move_count = 0

            while valid_move and col in range(8) and row in range(8) and move_count < self._max_move:
                target = board.get_location_format(col, row)
                target_piece = board.get_board_loc(target)

                if target_piece is not None:

                    if target_piece.get_player() == self._player:
                        valid_move = False

                    else:
                        path.append(target)
                        self._possible_moves[target] = deepcopy(path)
                        valid_move = False
                else:

                    path.append(target)
                    self._possible_moves[target] = deepcopy(path)
                move_count += 1

                col += move_step[0]  # starting loc
                row += move_step[1]

        return self._possible_moves

    def add_direction_move_set(self, direction):
        """
        :param direction: N, NE, E, etc; piece movement direction to find moves
        :return: All possible moves a piece can make in a given direction
        """
        # Get coordinates required to move piece in given direction
        move_step = self._directions[direction]
        possible_moves = []
        spaces_moved = 0

        cur_loc = self.get_grid_col_row(self._cur_loc)  # str coordinate to int
        col = cur_loc[0] + move_step[0]  # starting loc
        row = cur_loc[1] + move_step[1]

        # Find all potential moves from current position
        while col in range(8) and row in range(8) and spaces_moved < self._max_move:
            # Current piece can move to target space
            target = self.format_grid_loc(col, row)
            possible_moves.append(target)

            spaces_moved += 1
            col += move_step[0]
            row += move_step[1]

        # Find the path to each potential move from current piece location
        all_move_sets = dict()
        for target in possible_moves:
            all_move_sets[target] = self.find_path(target, move_step)

        return all_move_sets

    def find_path(self, target, move_step):
        """
        :param target: location piece is trying to move
        :param move_step: step increments to get to target
        :return: path required to reach target
        """
        move_path = []
        cur_loc = self._cur_loc

        while cur_loc != target:
            cur_loc = self._get_target_location(cur_loc, move_step)
            move_path.append(cur_loc)

        return move_path

    def _get_target_location(self, cur_loc: str, move_step: tuple):
        col, row = self.get_grid_col_row(cur_loc)
        col += move_step[0]
        row += move_step[1]
        return self.format_grid_loc(col, row)

class Queen(GamePiece):
    def __init__(self, location):
        super().__init__(location)
        self._name = "Queen"
        self._move_set = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


class King(GamePiece):
    def __init__(self, location):
        super().__init__(location)
        self._name = "King"
        self._move_set = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        self._max_move = 1


class Pawn(GamePiece):  ### Need capture move and en passant  ## need transformation
    def __init__(self, location):
        super().__init__(location)
        self._name = "Pawn"
        self._first_move_made = False
        self._max_move = 2
        self._possible_moves = {
            "MOVE": dict(),
            "CAPTURE": dict(),
            "EN_PASSANT": []
        }
        self._capture_set = []
        self._move_set = []
        self._en_passant = False
        self._en_passant_locs = []

    def set_en_passant(self, capture_loc, move_loc):
        self._en_passant = True
        self._en_passant_locs.append(capture_loc)
        self._en_passant_locs.append(move_loc)

    def clear_en_passant(self):
        self._en_passant = False
        self._en_passant_locs.clear()
        self._possible_moves["EN_PASSANT"].clear()

    def get_en_passant_capture(self):
        return self._en_passant_locs[0]

    def set_player(self, player):
        self._player = player

        if self._player == 1:
            self._move_set = ["N"]
            self._capture_set = ["NW", "NE"]
        else:
            self._move_set = ["S"]
            self._capture_set = ["SW", "SE"]

    def made_first_move(self):  ### NEED TO CHANGE IN BOARD ###
        self._max_move = 1
        self._first_move_made = True

    def get_possible_moves(self):
        self._possible_moves["MOVE"].clear()
        self._possible_moves["CAPTURE"].clear()

        for directional_move in self._move_set:
            dir_move_set = self.add_direction_move_set(directional_move)
            self._possible_moves["MOVE"].update(dir_move_set)

        temp_move = self._max_move
        self._max_move = 1

        for directional_capture in self._capture_set:
            dir_capture_set = self.add_direction_move_set(directional_capture)
            self._possible_moves["CAPTURE"].update(dir_capture_set)

        self._max_move = temp_move

        if self._en_passant is True:
            self._possible_moves["EN_PASSANT"] = self._en_passant_locs

        return self._possible_moves


class Knight(GamePiece):
    def __init__(self, location):
        super().__init__(location)
        self._directions = {"NE": (1, 2), "EN": (2, 1), "ES": (2, -1),
                            "SE": (1, -2), "SW": (-1, -2), "WS": (-2, -1),
                            "WN": (-2, 1), "NW": (-1, 2)}
        self._move_set = ["NE", "EN", "ES", "SE", "SW", "WS", "WN", "NW"]
        self._max_move = 1
        self._name = "Knight"


class Rook(GamePiece):
    def __init__(self, location):
        super().__init__(location)
        self._name = "Rook"
        self._move_set = ["N", "E", "S", "W"]


class Bishop(GamePiece):
    def __init__(self, location):
        super().__init__(location)
        self._name = "Bishop"
        self._move_set = ["NE", "SE", "SW", "NW"]