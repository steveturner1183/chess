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
        self._image_path = None
        self._player = None
        self._name = None
        self._cur_loc = location
        self._rows = "12345678"
        self._cols = "abcdefgh"
        self._directions = {"N": (0, 1), "NE": (1, 1), "E": (1, 0),
                            "SE": (1, -1), "S": (0, -1), "SW": (-1, -1),
                            "W": (-1, 0), "NW": (-1, 1)}
        self._max_move = 7
        self._possible_moves = dict()
        self._move_set = []

    def __repr__(self):
        return repr("P" + str(self._player) + "-" + self._name + "-" + self._cur_loc)

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

    def valid_move_only(self, target):
        if target is None:
            return True
        else:
            return False

    def valid_capture_only(self, target):
        if target is not None:
            if target.get_player() != self._player:
                return True
        return False

    def get_possible_moves(self, board):
        self._possible_moves.clear()

        for directional_move in self._move_set:
            path = []
            valid_move = True
            move_step = self._directions[directional_move]
            move_count = 0

            col, row = board.get_board_col_row(self._cur_loc)
            col += move_step[0]  # starting loc
            row += move_step[1]

            while valid_move and col in range(8) and row in range(8) and move_count < self._max_move:
                target_loc = board.get_location_format(col, row)
                target_piece = board.get_board_loc(target_loc)

                valid_move_only = self.valid_move_only(target_piece)
                valid_capture_only = self.valid_capture_only(target_piece)

                if valid_move_only or valid_capture_only:
                    path.append(target_loc)
                    self._possible_moves[target_loc] = deepcopy(path)
                else:
                    valid_move = False

                move_count += 1
                col += move_step[0]  # starting loc
                row += move_step[1]

        return self._possible_moves

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
        self._move_set = []
        self._en_passant = False
        self._en_passant_locs = {"Capture": None, "Move": None}

    def set_en_passant(self, capture_loc, move_loc):
        self._en_passant = True
        self._en_passant_locs["Capture"] = capture_loc
        self._en_passant_locs["Move"] = move_loc

    def clear_en_passant(self):
        self._en_passant = False
        self._en_passant_locs["Capture"] = None
        self._en_passant_locs["Move"] = None

    def available_en_passant(self):
        return self._en_passant

    def get_en_passant_moves(self):
        return self._en_passant_locs

    def set_player(self, player):
        self._player = player

        if self._player == 1:
            self._move_set = ["N", "NW", "NE"]
        else:
            self._move_set = ["S", "SW", "SE"]

    def made_first_move(self):  ### NEED TO CHANGE IN BOARD ###
        self._max_move = 1
        self._first_move_made = True

    def get_possible_moves(self, board):
        self._possible_moves.clear()

        for directional_move in self._move_set:

            if directional_move == "N":
                move_check = self.valid_move_only
            else:
                move_check = self.valid_capture_only

            path = []
            valid_move = True
            move_step = self._directions[directional_move]
            move_count = 0

            col, row = board.get_board_col_row(self._cur_loc)
            col += move_step[0]  # starting loc
            row += move_step[1]

            while valid_move and col in range(8) and row in range(8) and move_count < self._max_move:
                target_loc = board.get_location_format(col, row)
                target_piece = board.get_board_loc(target_loc)

                if move_check(target_piece):
                    path.append(target_loc)
                    self._possible_moves[target_loc] = deepcopy(path)
                else:
                    valid_move = False

                move_count += 1
                col += move_step[0]  # starting loc
                row += move_step[1]

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