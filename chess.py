import logging

logging.basicConfig(level=logging.DEBUG)
from board import GameBoard
from player import Player
from rules import ChessRules

# player cannot move other piece if they are in check
# change tile colors!!!!!!!!
# Mke sure all pieces are removed from player roster
class Chess:
    def __init__(self):
        self._game_status = "INCOMPLETE"
        self._p1 = Player(1, "W")
        self._p2 = Player(2, "B")
        self._board = GameBoard(self._p1, self._p2)
        self._player_turn = 1
        self._rules = ChessRules()
        self._castle = False

    def get_board_state(self):
        """
        FOR GUI
        :return:
        """
        board_state = dict()
        for col in range(8):
            for row in range(8):
                loc = self._board.get_location_format(col, row)
                piece = self._board.get_board_loc(loc)
                board_state[loc] = piece
        return board_state

    def get_player(self, player):
        if player == 1:
            return self._p1
        else:
            return self._p2

    def get_game_status(self):
        return self._game_status

    def king_check_status(self):
        # CHECK
        if self._player_turn == 1:
            atk_player = self._p1
            def_player = self._p2
        else:
            atk_player = self._p2
            def_player = self._p1

        status = self._rules.check(atk_player, def_player, self._board, self)
        if status == "CHECK":
            def_player.set_in_check(status)
        elif status == "CHECKMATE":
            def_player.set_in_check(status)
            self._game_status = "Player" + str(atk_player) + " Won"

    def game_incomplete(self):
        return self._game_status == "INCOMPLETE"

    def set_player_turn(self):
        if self._player_turn == 1:
            self._player_turn = 2
        else:
            self._player_turn = 1

    def get_board_piece(self, location):
        return self._board.get_board_loc(location)

    def make_move(self, move):
        current_loc = move[:2]
        target_loc = move[-2:]
        self._board.move_piece(current_loc, target_loc)

    def validate_move(self, move):
        current_loc = move[:2]
        target_loc = move[-2:]
        cur_piece = self._board.get_board_loc(current_loc)
        target_piece = self._board.get_board_loc(target_loc)

        if cur_piece is None:
            return False

        if cur_piece.get_player() != self._player_turn:  # Not player turn
            logging.debug("Not players turn")
            return False

        if cur_piece.get_name() == "Pawn":
            if cur_piece.available_en_passant:
                move_list = cur_piece.get_en_passant_moves()
                if target_loc == move_list["Move"]:
                    if target_piece is not None:
                        return False
                    else:
                        self._en_passant = True
                        return True

        if cur_piece.get_name() == "King":
            if self._rules.castle(current_loc, target_loc, self._board):
                self._board.set_castle(True)
                return True

        move_list = cur_piece.get_possible_moves(self._board)



        if cur_piece.get_name() == "King":
            if cur_piece.get_player() == 1:
                opp_roster = self._p2.get_roster()
            else:
                opp_roster = self._p1.get_roster()

            if self._rules.self_into_check(target_loc, opp_roster, self._board):
                logging.debug("Castle possible")
                return True
            else:
                logging.debug("Castle not possible")

        # Move location is not in piece's move set
        if target_loc not in move_list:
            logging.debug("{} not in {}".format(target_loc, move_list))
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
        game.validate_move(move)
        game.make_move(move)
        game.set_player_turn()
        game._board.print_board()