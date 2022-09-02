from pieces import *
from player import Player
from rules import ChessRules
import logging
logging.basicConfig(level=logging.DEBUG)
from typing import Union


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

    def set_castle(self, value):
        self._castle = value

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

    def set_board_loc(self, loc, value):
        """
        Sets the given board location to a new value
        :param loc: Chess coordinate location, example "a1"
        :param value: Piece or None if space is to be cleared
        :return: None
        """
        col, row = self.get_board_col_row(loc)
        self._game_board[row][col] = value

    def set_up_board(self):
        """
        Initialize the board set
        :return: None
        """
        # generate set of pieces based on player 1 color
        piece_set = PieceSet(self._p1.get_color())
        rosters = piece_set.get_piece_sets()

        # Distribute pieces to players
        self._p1.set_roster(rosters[0])
        self._p2.set_roster(rosters[1])

        # Track king for location checking
        self._p1.set_king(piece_set.get_king(1))
        self._p2.set_king(piece_set.get_king(2))


        self._game_board = [
            [piece for piece in self._p1.get_roster()[:8]],
            [piece for piece in self._p1.get_roster()[8:]],
            [None] * 8, [None] * 8, [None] * 8, [None] * 8,
            [piece for piece in self._p2.get_roster()[8:]],
            [piece for piece in self._p2.get_roster()[:8]]
        ]

        self.set_all_possible_moves()

    def set_all_possible_moves(self):
        for row in self._game_board:
            for piece in row:
                if piece is not None:
                    piece.set_possible_moves(self)

    #### King can move into Ccheck!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def move_piece(self, cur_loc, tar_loc):
        """
        Change the board to match a verified move
        :param cur_loc: Location of piece to be moved on board
        :param tar_loc: Location of square piece is moving to
        :return: None
        """
        # Move pieces on board
        cur_piece = self.get_board_loc(cur_loc)
        tar_piece = self.get_board_loc(tar_loc)

        # Special moving sequence for en passant
        if self._en_passant is True:
            cap_loc = self.get_board_loc(cur_loc).get_en_passant_capture()
            tar_piece = self.get_board_loc(cap_loc)

            self.set_board_loc(cap_loc, None)
            self._en_passant = False

        if self._castle is True:
            self.set_castle(False)
            cur_row = self.get_board_col_row(cur_loc)[1]
            cur_col, tar_col = self._cols.index(cur_loc[0]), self._cols.index(tar_loc[0])

            logging.debug("cur col = {} and tar col = {}".format(cur_col, tar_col))
            if cur_col > tar_col:  # Move left
                rook_direction = 1
                if cur_piece.get_player() == 1:
                    rook_cur_loc = "a1"
                else:
                    rook_cur_loc = "a8"

            else:
                rook_direction = -1
                if cur_piece.get_player() == 1:
                    rook_cur_loc = "h1"
                else:
                    rook_cur_loc = "h8"

            rook = self.get_board_loc(rook_cur_loc)
            rook_col = tar_col + rook_direction
            logging.debug("rook col = {}".format(rook_col))
            rook_loc = self.get_location_format(rook_col, cur_row)
            logging.debug("setting rook at {} to {}".format(rook_cur_loc, rook_loc))
            self.set_board_loc(rook_loc, rook)
            self.set_board_loc(rook_cur_loc, None)
            rook.set_location(rook_loc)

        # Remove captured piece from opposing players roster
        if tar_piece is not None:
            if cur_piece.get_player() == 1:
                self._p2.remove_piece(tar_piece)
            else:
                self._p1.remove_piece(tar_piece)

        # Move piece to new location
        cur_piece.set_location(tar_loc)
        self.set_board_loc(tar_loc, cur_piece)
        self.set_board_loc(cur_loc, None)

        if cur_piece is not None and cur_piece.get_name() == "Pawn":
            # Chess rule - Pawn can only move two spaces on first move
            cur_piece.made_first_move()

            # Chess rule - If piece moved 2 spaces, other pawns can en passant
            self._rules.check_en_passant(cur_piece, cur_loc, tar_loc, self._game_board)

        if cur_piece.get_name() == "Rook" or cur_piece.get_name() == "King":
            cur_piece.set_has_moved()
        # reset board after moved piece
        self.set_all_possible_moves()


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
                        "[" + piece.get_name()[:2] + " " + str(piece.get_player()) + "]", end=" ")
                else:
                    print("  X   ", end=" ")
            print("\n")


if __name__ == "__main__":
    p1 = Player("Human", "W")
    p2 = Player("Humam", "B")
    board = GameBoard(p1, p2)
    board.print_board()
    # print(board.king_check("player_1"))