from board import GameBoard
from player import Player


class Chess:
    def __init__(self):
        self._game_status = "INCOMPLETE"
        self._p1 = Player(1, "W")
        self._p2 = Player(2, "B")
        self._board = GameBoard(self._p1, self._p2)
        self._player_turn = 1

    def start_game(self):
        while self._game_status == "INCOMPLETE":
            move = self.get_move()  # Should always return valid move

            self.make_move(move[0], move[1])

            self.set_player_turn()
            # self._game_status = "stop"

    def set_player_turn(self):
        if self._player_turn == 1:
            self._player_turn = 2
        else:
            self._player_turn = 1

    def get_move(self):
        valid_move = False

        while valid_move is False:
            prompt = "Player" + str(self._player_turn) + ": "
            move = input(prompt)

            if self.check_game_rules(move) is True:
                return move[:2], move[-2:]

    def check_game_rules(self, move):
        if move is None:  # Empty square
            return False

        cols = "abcedefgh"
        rows = "12345678"

        if len(move) != 5:
            return False

        cur_loc = move[:2]
        tar_loc = move[-2:]

        # check column
        if cur_loc[0] not in cols or tar_loc[0] not in cols:
            error_mess = "Invalid Input"
            print(error_mess)
            return False

        # check row
        if cur_loc[1] not in rows or tar_loc[1] not in rows:
            error_mess = "Invalid Input"
            print(error_mess)
            return False

        cur_piece = self.get_board_piece(cur_loc)

        if cur_piece.get_player() != self._player_turn:  # Not player turn
            error_mess = "Not player turn"
            print(error_mess)
            return False

        # Check target? or is this board??######################################

        if self._board.validate_move(cur_loc, tar_loc) is True:
            print("valid move")
        else:
            print("invalid move")
            return False

        return True

    def get_board_piece(self, location):
        return self._board.get_board_square(location)

    def make_move(self, start_loc, end_loc):
        self._board.move_piece(start_loc, end_loc)

        self._board.print_board()

        # validate the game is not over - is this needed? will freeze after game completion
        # check there is a piece in that location and who it is owned by
        # validate it is that players turn
        # validate with board that move can be made
        # check? checkmate? draw?
        # restart loop
        pass


if __name__ == "__main__":
    game = Chess()
    game.start_game()