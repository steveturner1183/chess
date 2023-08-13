from copy import deepcopy
import os


class PieceSet:
    def __init__(self):
        """
        Creates a roster for player 1 and 2 to use at the beginning of the game
        """

        self._roster = {
                    "W":  [Rook("a1"), Knight("b1"), Bishop("c1"), Queen("d1"),
                           King("e1"), Bishop("f1"), Knight("g1"), Rook("h1"),
                           Pawn("a2"), Pawn("b2"), Pawn("c2"), Pawn("d2"),
                           Pawn("e2"), Pawn("f2"), Pawn("g2"), Pawn("h2")],

                    "B":  [Rook("a8"), Knight("b8"), Bishop("c8"), Queen("d8"),
                           King("e8"), Bishop("f8"), Knight("g8"), Rook("h8"),
                           Pawn("a7"), Pawn("b7"), Pawn("c7"), Pawn("d7"),
                           Pawn("e7"), Pawn("f7"), Pawn("g7"), Pawn("h7")]
        }

    def get_roster(self, player):
        player_turn = player.get_turn()
        player_color = player.get_color()
        roster = self._roster[player_color]

        for piece in roster:
            piece.set_player(player_turn)
            piece.set_image_path(player_color)

        return roster


class GamePiece:
    def __init__(self, location):
        self._image_path = None
        self._player = None
        self._name = None
        self._cur_loc = location
        self._max_move = 7
        self._possible_moves = dict()
        self._move_set = []
        self._has_moved = False
        self._color = None
        self._image_path = None

    def __repr__(self):
        return repr(
            "P" + str(self._player) + "-" + self._name + "-" + self._cur_loc)

    def set_image_path(self, color):
        """
        Image files from:
        https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent
        :param color:
        :return:
        """
        self._color = color
        path = os.path.join("Assets", color + "_" + self._name + ".PNG")
        self._image_path = path

    def set_has_moved(self):
        self._piece_has_moved = True

    def has_moved(self):
        return self._has_moved

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

    def get_color(self):
        return self._color

    def valid_move(self, target, move):
        if target is not None:
            if target.get_player() != self._player:
                return True
            else:
                return False
        else:
            return True

    def get_possible_moves(self):
        return self._possible_moves

### PIECES CAN JUMP OVER ENEMY PIECES
    def set_possible_moves(self, board):
        self._possible_moves.clear()

        for move in self._move_set:
            path = []
            valid_move = True
            capture_found = False
            move_count = 0

            col, row = board.get_board_col_row(self._cur_loc)
            col += move[0]  # starting loc
            row += move[1]

            while valid_move is True and capture_found is False:
                # Move is of board
                if col not in range(8) or row not in range(8):
                    valid_move = False

                # Piece's moves exceeded
                elif move_count >= self._max_move:
                    valid_move = False

                else:
                    target_loc = board.get_location_format(col, row)
                    target_piece = board.get_board_loc(target_loc)

                    move_is_valid = self.valid_move(target_piece, move)

                    if move_is_valid:
                        path.append(target_loc)
                        self._possible_moves[target_loc] = deepcopy(path)
                    else:
                        valid_move = False

                    if target_piece is not None:
                        capture_found = True

                move_count += 1
                col += move[0]  # starting loc
                row += move[1]

        return self._possible_moves


class Queen(GamePiece):
    def __init__(self, location):
        super().__init__(location)
        self._name = "Queen"
        self._move_set = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1),
                          (-1, 0), (-1, 1)]


class King(GamePiece):
    def __init__(self, location):
        super().__init__(location)
        self._name = "King"
        self._move_set = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1),
                          (-1, 0), (-1, 1)]
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

    def valid_move(self, target, move):
        if move == (0, 1) or move == (0, -1):
            if target is None:
                return True
            else:
                return False
        else:
            if target is not None:
                if target.get_player() != self._player:
                    return True
            return False

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
            self._move_set = [(0, 1), (-1, 1), (1, 1)]
        else:
            self._move_set = [(0, -1), (-1, -1), (1, -1)]

    def has_moved(self):
        self._max_move = 1
        self._first_move_made = True


class Knight(GamePiece):
    def __init__(self, location):
        super().__init__(location)
        self._move_set = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1),
                          (-2, 1), (-1, 2)]
        self._max_move = 1
        self._name = "Knight"


class Rook(GamePiece):
    def __init__(self, location):
        super().__init__(location)
        self._name = "Rook"
        self._move_set = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Bishop(GamePiece):
    def __init__(self, location):
        super().__init__(location)
        self._name = "Bishop"
        self._move_set = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
