from board import GameBoard
from rules import ChessRules


class Chess:
    def __init__(self, p1, p2):
        self._game_status = "INCOMPLETE"

        self._p1 = p1
        self._p2 = p2
        self._p1_color = p1.get_color()
        self._p2_color = p2.get_color()

        self._board = GameBoard(self._p1, self._p2)

        if self._p1_color == "W":
            self._player_turn = 1
        else:
            self._player_turn = 2

        self._rules = ChessRules()

    def get_board_location(self, loc):
        return self._board.get_board_loc(loc)

    def get_turn(self):
        return self._player_turn

    def get_colors(self):
        return self._p1_color, self._p2_color

    def get_cols_and_rows(self):
        return self._board.get_cols_and_rows()

    def get_board(self):
        return self._board.get_board()

    def get_player(self, player):
        if player == 1:
            return self._p1
        else:
            return self._p2

    def get_opponent(self):
        if self._player_turn == 1:
            return self._p2
        else:
            return self._p1

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

        status = self._rules.check(atk_player, def_player)
        if status == "CHECK":
            def_player.set_in_check(status)
        elif status == "CHECKMATE":
            def_player.set_in_check(status)
            self._game_status = "Player " + str(atk_player.get_turn()) + " Wins"
        else:
            def_player.set_in_check(False)

    def game_incomplete(self):
        return self._game_status == "INCOMPLETE"

    def set_player_turn(self):
        if self._player_turn == 1:
            self._player_turn = 2
        else:
            self._player_turn = 1

    def get_player_turn(self):
        return self._player_turn

    def get_board_piece(self, location):
        return self._board.get_board_loc(location)

    def make_move(self, move):
        current_loc = move[:2]
        target_loc = move[-2:]
        self._board.make_move(current_loc, target_loc)
        self.king_check_status()

    def validate_en_passant(self, pawn, target_piece, target_loc):
        if pawn.available_en_passant:
            move_list = pawn.get_en_passant_moves()
            if target_loc == move_list["Move"]:

                if target_piece is not None:
                    return False
                else:
                    self._board.set_en_passant(True)
                    return True
        return False

    def validate_move(self, move):
        current_loc = move[:2]
        target_loc = move[-2:]

        cur_piece = self._board.get_board_loc(current_loc)
        target_piece = self._board.get_board_loc(target_loc)

        # Selected empty board location for start
        if cur_piece is None:
            return False

        # Not players turn
        if cur_piece.get_player() != self._player_turn:  # Not player turn
            return False

        # En passant
        if cur_piece.get_name() == "Pawn":
            if self.validate_en_passant(cur_piece, target_piece, target_loc):
                return True

        if cur_piece.get_name() == "King":
            opp_roster = self.get_opponent().get_roster()

            if self._rules.self_into_check(target_loc, opp_roster):
                return False

            if self._rules.castle(current_loc, target_loc, self._board):
                self._board.set_castle(True)
                return True

        move_list = cur_piece.get_possible_moves()

        # Move location is not in piece's move set
        if target_loc not in move_list:
            return False

        current_player = self.get_player(self._player_turn)
        if self._rules.still_in_check(move, self) is False:
            return False

        return True
