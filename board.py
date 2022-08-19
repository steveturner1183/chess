from pieces import *
from player import Player


class GameBoard:
    def __init__(self, player_1, player_2):
        self._p1 = player_1
        self._p2 = player_2
        self._piece_set = PieceSet(player_1.get_color()).get_piece_sets()
        self._p1_roster, self._p2_roster = self._piece_set[0], self._piece_set[1]

        self._col_to_int = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5,
                            "g": 6, "h": 7}
        self._row_to_int = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5,
                            "2": 6, "1": 7}

        self._game_board = [
            [piece for piece in self._p2_roster[:8]],
            [piece for piece in self._p2_roster[8:]],
            [None] * 8, [None] * 8, [None] * 8, [None] * 8,
            [piece for piece in self._p1_roster[8:]],
            [piece for piece in self._p1_roster[:8]],
        ]

        self.set_all_possible_moves()


    def move_piece(self, cur_loc, tar_loc):
        c_col, c_row = self.get_col_row(cur_loc)
        t_col, t_row = self.get_col_row(tar_loc)

        self._game_board[t_row][t_col] = self._game_board[c_row][c_col]
        self._game_board[t_row][t_col].set_location(tar_loc)
        self._game_board[c_row][c_col] = None

        # reset board after moved piece
        self.set_all_possible_moves()

    def get_col_row(self, location):
        col = location[0]
        row = location[1]
        return self._col_to_int[col], self._row_to_int[row]

    def get_board_square(self, location):
        col, row = self.get_col_row(location)
        piece = self._game_board[row][col]
        return piece

    def set_all_possible_moves(self):

        for player in (self._p1, self._p1):
            possible_moves = []

            for piece in player.get_roster():
                piece_moves = piece.get_possible_moves()

                for target in piece_moves:
                    if self.validate_move(piece.get_location(), target) is True:
                        possible_moves.append([target, piece])

            player.set_pos_moves(possible_moves)

    def king_check(self, player):
        king = player.get_king()
        king_loc = king.get_location()

        if player == self._p1:
            moves = self._p2.get_pos_moves()
        else:
            moves = self._p1.get_pos_moves()

        for move in moves:
            if move[0] == king_loc:
                if self.king_check_mate(player, move, king, moves) is True:
                    return "CHECKMATE"
                else:
                    return "CHECK"

        return False

    def king_check_mate(self, player, move, king, moves):
        attack_piece = move[1]
        target = move[0]
        move_path = attack_piece.get_possible_moves()[target]
        player_moves = player.get_pos_moves()

        # See if move can be blocked
        for space in move_path[:-1]:
            if space in player_moves:
                return False

        # See if piece can be captured
        if attack_piece.get_current_location() in player_moves:
            return False

        # See if king can move out of check
        all_king_moves = king.get_possible_moves()
        valid_king_moves = []
        for x in all_king_moves:
            if self.validate_move(x) is True:
                valid_king_moves.append(x)
        for move in valid_king_moves:
            if move not in moves:
                return False

        return True

    def check_if_empty(self, location):
        if self.get_board_square(location) is None:
            return True
        else:
            return False

    """
    def check_if_enemy(self, location, target):
        if self.get_board_square(location).get_player() == "player_1":
            if self.get_board_square(target).get_player() == "player_2":
                return True
        elif self.get_board_square(target).get_player() == "player_2":
            if self.get_board_square(location).get_player() == "player_1":
                return True
        return False
    """
    def check_if_self(self, location, target):
        cur_player = self.get_board_square(location).get_player()
        tar_player = self.get_board_square(target).get_player()

        if cur_player == tar_player:
            return True
        else:
            return False

    def validate_move(self, current_loc, target_loc):
        cur_piece = self.get_board_square(current_loc)
        all_moves_list = cur_piece.get_possible_moves()

        # Check if target move is in piece's possible moves
        if target_loc not in all_moves_list:
            print(target_loc + " not in: ")
            print("MOVES LIST")
            for key in all_moves_list:
                print(key)
            return False

        # Check if path is blocked
        target_path = all_moves_list[target_loc]

        for step in target_path[:-1]:
            if self.check_if_empty(step) is False:
                print("path blocked")
                return False

        # Check that target space is empty or oppenents pieces
        if self.check_if_empty(target_loc) is False:
            print("space is not none")
            if self.check_if_self(current_loc, target_loc) is True:
                print("Current piece owned by: " + cur_piece.get_player())
                print("Space is owned by: " + self.get_board_square(target_loc).get_player())
                return False

        return True

    def special_moves(self):
        pass
        # pawn attack
        # en passant
        # rook / castle
        # transformation
        # pawn first move

    def print_board(self):
        print("      a     b     c      d     e     f     g      h ")
        print("   -----------------------------------------------")
        count = 8
        for rows in self._game_board:
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