import logging
logging.basicConfig(level=logging.DEBUG)
from board import GameBoard
from player import Player



class Chess:
    def __init__(self):
        self._game_status = "INCOMPLETE"
        self._p1 = Player(1, "W")
        self._p2 = Player(2, "B")
        self._board = GameBoard(self._p1, self._p2)
        self._player_turn = 1

    def get_board_state(self):
        board_state = dict()
        for col in range(8):
            for row in range(8):
                loc = self._board.get_location_format(col, row)
                piece = self._board.get_board_loc(loc)
                board_state[loc] = piece
        return  board_state

    def check_game_status(self):
        pass

    def get_player(self, player):
        if player == 1:
            return self._p1
        else:
            return self._p2


    def start_game(self):
        while self._game_status == "INCOMPLETE":
            move = self.get_move()  # Should always return valid move
            self.make_move(move[0], move[1])
            self.set_player_turn()
            self.check_game_status()
            # self._game_status = "stop"

    def set_player_turn(self):
        if self._player_turn == 1:
            self._player_turn = 2
        else:
            self._player_turn = 1

    def get_move(self):
        valid_move = False

        while valid_move is False:
            move = self.user_input()
            if self.check_game_rules(move) is True:
                logging.debug("{} is a valid move".format(move))
                return move[:2], move[-2:]

    def user_input(self):
        prompt = "Player" + str(self._player_turn) + ": "
        move = input(prompt)
        print("MOVE = ", move)
        return move


    def check_game_rules(self, move):
        cur_loc = move[:2]
        tar_loc = move[-2:]

        cur_piece = self.get_board_piece(cur_loc)

        if cur_piece is None:  # Empty square
            logging.debug("Selected location is {}".format(cur_piece))
            return False

        cols = "abcedefgh"
        rows = "12345678"

        if len(move) != 5:
            return False

        # check column
        if cur_loc[0] not in cols or tar_loc[0] not in cols:
            logging.debug(
                "COLS: {} or {} is out of bounds".format(cur_loc[0], tar_loc[0])
            )
            return False

        # check row
        if cur_loc[1] not in rows or tar_loc[1] not in rows:
            logging.debug(
                "ROWS: {} or {} is out of bounds".format(cur_loc[1], tar_loc[1])
            )
            return False

        if cur_piece.get_player() != self._player_turn:  # Not player turn
            logging.debug("Not players turn")
            return False

        if self._board.validate_move(cur_loc, tar_loc) is False:
            return False

        return True

    def get_board_piece(self, location):
        return self._board.get_board_loc(location)

    def make_move(self, start_loc, end_loc):
        self._board.move_piece(start_loc, end_loc)

        #self._board.print_board()

        # validate the game is not over - is this needed? will freeze after game completion
        # check there is a piece in that location and who it is owned by
        # validate it is that players turn
        # validate with board that move can be made
        # check? checkmate? draw?
        # restart loop

    def validate_move(self, current_loc, target_loc):
        cur_piece = self._board.get_board_loc(current_loc)
        target_piece = self._board.get_board_loc(target_loc)

        move_type = "MOVE" if target_piece is None else "CAPTURE"

        if cur_piece.get_name() == "Pawn":
            move_list = cur_piece.get_possible_moves()
            if len(move_list["EN_PASSANT"]) > 0:
                if target_loc == move_list["EN_PASSANT"][1]:
                    if target_piece is not None:
                        return False
                    else:
                        self._en_passant = True
                        return True
            else:
                move_list = move_list[move_type]

        else:
            move_list = cur_piece.get_possible_moves(self._board)

        # Move location is not in piece's move set
        if target_loc not in move_list:
            logging.debug("Not in moves")
            return False

        # Check if path is blocked
        if not self._board.verify_path_is_clear(target_path=move_list[target_loc]):
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


if __name__ == "__main__":
    logging.debug("----test_queen_pawn_move----")
    game = Chess()
    moves = ["d2 d4", "a7 a6", "d4 d5", "e7 e5", "d5 e6"]
    for move in moves:
        logging.debug("Testing move {}".format(move))

        if move == "d5 e6":
            print("e5 e6")
        game.check_game_rules(move)
        game.make_move(move[:2], move[-2:])
        game.set_player_turn()
        game._board.print_board()
