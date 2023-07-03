from pieces import *
from player import Player
from rules import ChessRules


class GameBoard:
    def __init__(self, player_1, player_2):
        self._cols = "abcdefgh"
        self._rows = "12345678"
        self._p1 = player_1
        self._p2 = player_2
        self._rules = ChessRules()

        self._game_board = []
        self.set_up_board()

        self._en_passant = False
        self._castle = False

    def get_board(self):
        return self._game_board

    def get_cols_and_rows(self):
        return self._cols, self._rows

    def set_castle(self, value):
        self._castle = value

    def set_en_passant(self, value):
        self._en_passant = value

    def get_location_format(self, col, row):
        return self._cols[col] + self._rows[row]

    def get_board_col_row(self, loc: str) -> (int, int):
        """
        Returns board grid coordinates for given location
        :param loc: Chess coordinate location, example "a1"
        :return: Grid coordinates for given location
        """
        col, row = loc[0], loc[1]
        return self._cols.index(col), self._rows.index(row)

    def get_board_loc(self, loc: str):
        """
        Retrieves value at given board location
        :param loc: Chess coordinate location, example "a1"
        :return: Piece if piece at given location, otherwise None
        """
        col, row = self.get_board_col_row(loc)
        return self._game_board[row][col]

    def move_board_piece(self, cur_loc, tar_loc):
        """
        Sets the given board location to a new value
        :param cur_loc: Chess coordinate location, example "a1"
        :param tar_loc: Piece or None if space is to be cleared
        :return: None
        """
        cur_col, cur_row = self.get_board_col_row(cur_loc)
        tar_col, tar_row = self.get_board_col_row(tar_loc)
        cur_piece = self.get_board_loc(cur_loc)

        self._game_board[tar_row][tar_col] = cur_piece
        cur_piece.set_location(tar_loc)
        self._game_board[cur_row][cur_col] = None

        if cur_piece.get_name() in ["King", "Rook", "Pawn"]:
            cur_piece.set_has_moved()

    def remove_captured_piece(self, loc):
        piece = self.get_board_loc(loc)
        if piece.get_player() == 1:
            self._p1.remove_piece(piece)
        else:
            self._p2.remove_piece(piece)

        # Remove captured piece from board
        col, row = self.get_board_col_row(loc)
        self._game_board[row][col] = None

    def get_neighbor_loc(self, cur_loc, col_dist, row_dist):
        cur_col, cur_row = self.get_board_col_row(cur_loc)
        cur_col += col_dist
        cur_row += row_dist
        if cur_col in range(8) and cur_row in range(8):
            tar_loc = self._cols[cur_col] + self._rows[cur_row]
            return tar_loc
        else:
            return None

    def set_up_board(self):
        """
        Initialize the board set
        :return: None
        """
        # generate set of pieces based on player 1 color
        piece_set = PieceSet()
        self._p1.set_roster(piece_set.get_roster(self._p1))
        self._p2.set_roster(piece_set.get_roster(self._p2))

        self._game_board = [
            [piece for piece in self._p1.get_roster()[:8]],
            [piece for piece in self._p1.get_roster()[8:]],
            [None] * 8, [None] * 8, [None] * 8, [None] * 8,
            [piece for piece in self._p2.get_roster()[8:]],
            [piece for piece in self._p2.get_roster()[:8]]
        ]

        if self._p1.get_color() == "B":
            self.reverse_board()

        self.set_all_possible_moves()

    def reverse_board(self):
        for row in self._game_board:
            row.reverse()
        self._cols = self._cols[::-1]
        self._rows = self._rows[::-1]

    def set_all_possible_moves(self):
        for row in self._game_board:
            for piece in row:
                if piece is not None:
                    piece.set_possible_moves(self)

    def castle_move(self, tar_loc):

        self.set_castle(False)
        rook_locs = {
            "g1": {"MOVE": "f1", "LOC": "h1"},
            "c1": {"MOVE": "d1", "LOC": "a1"},
            "g8": {"MOVE": "f8", "LOC": "h8"},
            "c8": {"MOVE": "d8", "LOC": "a8"}
        }

        rook_loc = rook_locs[tar_loc]["LOC"]
        rook_move = rook_locs[tar_loc]["MOVE"]

        self.get_board_loc(rook_loc).set_location(rook_move)
        self.move_board_piece(rook_loc, rook_move)

    def make_move(self, cur_loc, tar_loc):
        """
        Change the board to match a verified move
        :param cur_loc: Location of piece to be moved on board
        :param tar_loc: Location of square piece is moving to
        :return: None
        """
        # Move pieces on board
        cur_piece = self.get_board_loc(cur_loc)

        # Special moving sequence for en passant
        if self._en_passant is True:
            self._en_passant = False
            cap_loc = cur_piece.get_en_passant_moves()["Capture"]
            tar_piece = self.get_board_loc(cap_loc)
        else:
            cap_loc = tar_loc
            tar_piece = self.get_board_loc(cap_loc)

        if self._castle is True:
            self.castle_move(tar_loc)

        # Remove captured piece from opposing players roster
        if tar_piece is not None:
            self.remove_captured_piece(cap_loc)

        # Move piece to new location
        self.move_board_piece(cur_loc, tar_loc)

        # Must be reset every turn
        self.reset_en_passant()

        self._rules.en_passant(cur_piece, cur_loc, tar_loc, self)

        # reset board after moved piece
        self.set_all_possible_moves()

    def reset_en_passant(self):
        # Reset en passant
        self._en_passant = False

        for row in self._game_board:
            for piece in row:
                if piece is not None and piece.get_name() == "Pawn":
                    piece.clear_en_passant()

    def print_board(self):
        print("      a     b     c      d     e     f     g      h ")
        print("   -----------------------------------------------")
        count = 8
        print_board = [self._game_board[row] for row in range(7, -1, -1)]
        for rows in print_board:
            print(count, end=" | ")
            count -= 1
            for piece in rows:
                if piece is not None:
                    print(
                        "[" + piece.get_name()[:2] + " " +
                        str(piece.get_player()) + piece.get_color() + " " +
                        piece.get_location() + " " + "]", end=" ")
                else:
                    print("-----X-----", end=" ")
            print("\n")


if __name__ == "__main__":
    p1 = Player("Human", "B")
    p2 = Player("Humam", "W")
    board = GameBoard(p1, p2)