from pieces import *
from player import Player


class GameBoard:
    def __init__(self, player_1, player_2):
        self._p1 = player_1
        self._p2 = player_2
        self._game_board = []
        self.set_up_board()
        self._col_to_int = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5,
                      "g": 6, "h": 7}
        self._row_to_int = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5,
                      "2": 6, "1": 7}


        self.set_all_poss_moves()

    def get_board_loc(self, location):
        col = self._col_to_int[location[0]]
        row = self._row_to_int[location[1]]

        board_loc = self._game_board[row][col]

        return board_loc

    def set_up_board(self):
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
            [piece for piece in self._p2.get_roster()[:8]],
            [piece for piece in self._p2.get_roster()[8:]],
            [None] * 8, [None] * 8, [None] * 8, [None] * 8,
            [piece for piece in self._p1.get_roster()[8:]],
            [piece for piece in self._p1.get_roster()[:8]]
        ]

    def set_all_poss_moves(self):

        for player in (self._p1, self._p2):
            possible_moves = []

            for piece in player.get_roster():
                piece_moves = piece.get_possible_moves()

                for target in piece_moves:
                    if self.validate_move(piece.get_location(), target) is True:
                        possible_moves.append([target, piece])

            player.set_pos_moves(possible_moves)

    def validate_move(self, current_loc, target_loc):
        cur_piece = self.get_board_loc(current_loc)
        all_moves_list = cur_piece.get_possible_moves()

        # Check if target move is in piece's possible moves
        if target_loc not in all_moves_list:
            return False

        # Check if path is blocked
        target_path = all_moves_list[target_loc]

        for step in target_path[:-1]:
            if self.get_board_loc(step) is None:
                return False

        # Check that target space is empty or oppenents pieces
        if self.get_board_loc(target_loc) is not None:

            target_piece = self.get_board_loc(target_loc)
            if cur_piece.get_player() == target_piece.get_player():
                return False

        return True

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

    def special_moves(self):
        pass
        # pawn attack
        # en passant
        # rook / castle
        # transformation
        # pawn first move

    def move_piece(self, cur_loc, tar_loc):
        c_col, c_row = self._col_to_int[cur_loc[0]], self._row_to_int[cur_loc[1]]
        t_col, t_row = self._col_to_int[tar_loc[0]], self._row_to_int[tar_loc[1]]

        self._game_board[t_row][t_col] = self._game_board[c_row][c_col]
        self._game_board[t_row][t_col].set_location(tar_loc)
        self._game_board[c_row][c_col] = None

        # reset board after moved piece
        self.set_all_poss_moves()

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