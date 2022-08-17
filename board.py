from pieces import *
from player import Player


class GameBoard:
    def __init__(self, player_1, player_2):
        self._game_board = [
            # Player pieces
            [Rook(), Knight(), Bishop(), Queen(), King(), Bishop(), Knight(), Rook()],
            [Pawn(), Pawn(), Pawn(), Pawn(), Pawn(), Pawn(), Pawn(), Pawn()],
            # Empty Rows
            [None] * 8, [None] * 8, [None] * 8, [None] * 8,
            # Player Pieces
            [Pawn(), Pawn(), Pawn(), Pawn(), Pawn(), Pawn(), Pawn(), Pawn()],
            [Rook(), Knight(), Bishop(), Queen(), King(), Bishop(), Knight(), Rook()]
        ]
        self._p1_roster = None
        self._p2_roster = None
        self._p1 = player_1
        self._p2 = player_2
        self.initialize_rosters()
        self._col_to_int = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5,
                            "g": 6, "h": 7}
        self._row_to_int = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5,
                            "7": 6, "8": 7}

    def get_col_row(self, location):
        col = location[0]
        row = location[1]
        return self._col_to_int[col], self._row_to_int[row]

    def initialize_rosters(self):
        # Player 1
        self._p1_roster = self._game_board[0].copy() + self._game_board[1].copy()
        # Player 2
        self._p2_roster = self._game_board[7].copy() + self._game_board[6].copy()

        p1_board_locations = ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1",
                              "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"]

        p2_board_locations = ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
                              "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"]

        index = 0
        while index < len(p1_board_locations):
            # player 1
            self._p1_roster[index].set_player("player_1")
            self._p1_roster[index].set_location(p1_board_locations[index])

            # player 2
            self._p2_roster[index].set_player("player_2")
            self._p2_roster[index].set_location(p2_board_locations[index])
            index += 1

        self.set_all_possible_moves()

    def set_all_possible_moves(self):
        for piece in self._p1_roster:
            piece.get_possible_moves()
        for piece in self._p2_roster:
            piece.get_possible_moves()

    def get_board_square(self, location):
        col, row = self.get_col_row(location)
        piece = self._game_board[row][col]
        return piece

    def check_if_empty(self, location):
        if self.get_board_square(location) is None:
            return True
        else:
            return False

    def check_if_enemy(self, location, target):
        if self.get_board_square(location).get_player() == "player_1":
            if self.get_board_square(target).get_player() == "player_2":
                return True
        elif self.get_board_square(target).get_player() == "player_2":
            if self.get_board_square(location).get_player() == "player_1":
                return True
        return False

    def check_if_self(self, location, target):
        if self.get_board_square(location).get_player() == self.get_board_square(target).get_player():
            return True
        else:
            return False

    def validate_move(self, current_loc, target_loc):
        cur_piece = self.get_board_square(current_loc)
        all_moves_list = cur_piece.get_possible_moves()

        # Check if target move is in piece's possible moves
        if target_loc not in all_moves_list:
            return False

        # Check if path is blocked
        target_path = all_moves_list[target_loc]

        for step in target_path[:-1]:
            if self.check_if_empty(step) is False:
                return False

        # Check that target space is empty or oppenents pieces
        if self.check_if_empty(target_loc) is False:
            if self.check_if_self(current_loc, target_loc) is True:
                return False

        return True

    def special_moves(self):
        pass

    def all_player_moves(self):
        pass

    def print_board(self):
        print("      a     b     c      d     e     f     g      h ")
        print("   -----------------------------------------------")
        count = 1
        for rows in self._game_board:
            print(count, end=" | ")
            count += 1
            for piece in rows:
                if piece is not None:
                    print(piece.get_name(), end=" ")
                else:
                    print("  X  ", end=" ")
            print("\n")


if __name__ == "__main__":
    p1 = Player("Human", "W")
    p2 = Player("Humam", "B")
    board = GameBoard(p1, p2)
    print(board.validate_move("a2", "a3"))