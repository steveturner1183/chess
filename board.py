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

        ########self.set_all_poss_moves()
        self._en_passant = False

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

    def verify_path_is_clear(self, target_path):
        """
        :param target_path: Path to location piece is trying to move
        :return: True if path is clear, false if blocked
        """
        for step in target_path[:-1]:
            if self.get_board_loc(step) is not None:
                return False
        return True

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
            cap_col, cap_row = self.get_board_col_row(cap_loc)
            tar_piece = self.get_board_loc(cap_loc)

            self.set_board_loc(cap_loc, None)
            self._en_passant = False

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

        # CHECK
        if cur_piece.get_player() == 1:
            check = self.king_check(1)
            if check is True:
                self._p2.set_in_check(True)
        else:
            check = self.king_check(2)
            if check is True:
                self._p1.set_in_check(True)

        # reset board after moved piece
        ############## self.set_all_poss_moves()


##@@#@#@ WHAT IF A PIECE MOVES OUT OF THE WAY AND PIECE PUT INT CHECK??????
    def king_check(self, player_move):
        check = False

        if player_move == 1:
            king = self._p2.get_king()
            roster = self._p1.get_roster()
        else:
            king = self._p1.get_king()
            roster = self._p2.get_roster()

        king_loc = king.get_location()

        for piece in roster:
            moves = piece.get_possible_moves(self)
            if king_loc in moves:
                in_check = self.validate_move(piece.get_location(), king_loc)
                if in_check:
                    check = True
                if self.king_checkmate(player_move, moves[king_loc], piece):
                    logging.debug("YOU DID IT")

        return check

    def king_checkmate(self, player_moved, moves, attack_piece):
        """
        Checks to see if opponents piece is in checkmate, i.e see if there are
        any ways to get out of check

        Chess Rule - Ways to get out of check:

        1. King moves to new location
        2. King captures attacking piece
        3. Another piece blocks path to the king
        4. Another piece captures the attacking piece

        :param player_moved:
        :param moves:
        :return:
        """
        if player_moved == 1:
            player = self._p1
            opp_player = self._p2
        else:
            player = self._p2
            opp_player = self._p1

        king = opp_player.get_king()
        king_loc = king.get_location()
        roster = opp_player.get_roster()

        for move in moves:
            for piece in roster:

                ### NEED TO SIMULATE?
                if piece.get_name() == "King":
                    king_moves = king.get_possible_moves(self._game_board)

                    for king_move in king_moves:
                        if self.validate_move(king_loc, king_move):
                            #  2. King captures attacking piece
                            if king_move == move:
                                if move == attack_piece.get_location():
                                    if not self.king_self_check(king_move, player.get_roster()):
                                        return False

                            #  1. King moves to new location
                            if king_move != move and king_move not in moves:
                                if not self.king_self_check(king_move, player.get_roster()):
                                    return False

                #  3. Another piece blocks path to the king
                #  4. Another piece captures the attacking piece
                elif piece.get_name() != "King":
                    if piece.get_name() == "Pawn":
                        piece.get_possible_moves()
                    else:
                        piece.get_possible_moves(self)

                    if move in piece.get_possible_moves(self):
                        if self.validate_move(piece.get_location(), move):
                            logging.debug("VALID -> {} to {}".format(piece, move))
                            return False

        return True


    def king_self_check(self, king_move, opp_roster):
        for piece in opp_roster:
            if piece.get_name() != "Pawn":
                all_moves = piece.get_possible_moves(self._game_board)
                if king_move in all_moves:
                    return True
        return False


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