from pieces import *
from player import Player
import logging
logging.basicConfig(level=logging.DEBUG)
from typing import Union


class GameBoard:
    def __init__(self, player_1, player_2):
        self._cols = "abcdefgh"
        self._rows = "12345678"
        self._p1 = player_1
        self._p2 = player_2

        self._game_board = []
        self.set_up_board()

        self.set_all_poss_moves()
        self._en_passant = False

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
        self._p2.set_king(piece_set.get_king(1))

        self._game_board = [
            [piece for piece in self._p1.get_roster()[:8]],
            [piece for piece in self._p1.get_roster()[8:]],
            [None] * 8, [None] * 8, [None] * 8, [None] * 8,
            [piece for piece in self._p2.get_roster()[8:]],
            [piece for piece in self._p2.get_roster()[:8]]
        ]

    def set_all_poss_moves(self):
        """
        Log of all possible moves a player can make is required to verify if a
        layer is in checkmate. This functions sets all the possile moves both
        players can make and stores in class attribute
        :return:
        """
        logging.disable(logging.DEBUG)

        for player in self._p1, self._p2:
            possible_moves = []
            roster = player.get_roster()

            for piece in roster:
                if piece.get_name() == "Pawn":
                    # NEED TO ACCOUNT FOR MOVE AND CAPTURE !!!!!!!!!!!!!!!!!!!!
                    all_moves = piece.get_possible_moves()
                    moves = all_moves["MOVE"]
                    captures = all_moves["CAPTURE"]
                    piece_moves = dict(**moves, **captures)
                    if len(all_moves["EN_PASSANT"]) > 0:
                        cur_loc = piece.get_location()
                        target = all_moves["EN_PASSANT"][1]
                        valid_move_check = self.validate_move(cur_loc, target)
                        if valid_move_check:
                            possible_moves.append([target, piece])
                else:
                    piece_moves = piece.get_possible_moves()

                cur_loc = piece.get_location()

                for target in piece_moves:
                    valid_move_check = self.validate_move(cur_loc, target)

                    if valid_move_check is True:
                        possible_moves.append([target, piece])

            player.set_pos_moves(possible_moves)
        logging.disable(logging.NOTSET)

    def verify_path_is_clear(self, target_path):
        """
        :param target_path: Path to location piece is trying to move
        :return: True if path is clear, false if blocked
        """
        for step in target_path[:-1]:
            if self.get_board_loc(step) is not None:
                return False
        return True

    def validate_move(self, current_loc, target_loc):
        cur_piece = self.get_board_loc(current_loc)
        target_piece = self.get_board_loc(target_loc)
        move_list = cur_piece.get_possible_moves()
        move_type = "MOVE" if target_piece is None else "CAPTURE"

        if cur_piece.get_name() == "Pawn":
            if len(move_list["EN_PASSANT"]) > 0:
                if target_loc == move_list["EN_PASSANT"][1]:
                    if target_piece is not None:
                        return False
                    else:
                        self._en_passant = True
                        return True
            else:
                move_list = move_list[move_type]

        # Move location is not in piece's move set
        if target_loc not in move_list:
            logging.debug("Not in moves")
            return False

        # Check if path is blocked
        if not self.verify_path_is_clear(target_path=move_list[target_loc]):
            logging.debug("Path blocked")
            return False

        if move_type == "CAPTURE":
            # Check that target space is empty or oppenents pieces
            if cur_piece.get_player() == target_piece.get_player():
                logging.debug("curPlayer={} == tarPlayer={}".format(
                    cur_piece.get_player(), target_piece.get_player())
                    )
                return False

        return True

    def board_state_moves(self):
        pass
        # rook / castle
        # transformation

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
            self.check_en_passant(cur_piece, cur_loc, tar_loc)

        # reset board after moved piece
        self.set_all_poss_moves()

    def check_en_passant(self, pawn, start_loc , end_loc):
        """
        Checks if given pawn can be captured from en passant, and sets the
        capturing pieces available moves to include en passant if true
        :param pawn:
        :return:
        """
        for row in self._game_board:
            for piece in row:
                if piece is not None and piece.get_name() == "Pawn":
                    piece.clear_en_passant()

        # Only Pawn that moves 2 spaces is eligable
        if abs(self._rows.index(start_loc[1]) - self._rows.index(end_loc[1])) != 2:
            return

        cur_loc = pawn.get_location()
        cur_col, cur_row = self.get_board_col_row(cur_loc)

        # Check east and west neighbor to see if they can perform en passant next turn
        for direction in 1, -1:
            neighbor_col = cur_col + direction
            board_boundary = range(8)

            if neighbor_col in board_boundary:
                neighbor = self.get_board_loc(self._cols[neighbor_col] + cur_loc[1])

                if neighbor is not None and neighbor.get_name() == "Pawn":
                    if neighbor.get_player() == 1:  # Move north of target pawn
                        en_move = cur_loc[0] + self._rows[cur_row + 1]
                    else:  # Move south
                        en_move = cur_loc[0] + self._rows[cur_row - 1]

                    neighbor.set_en_passant(cur_loc, en_move)


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