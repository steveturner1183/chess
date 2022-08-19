from pieces import *


class Player:
    def __init__(self, player_turn, player_color):
        self._player_turn = player_turn
        self._color = player_color
        self._set = PieceSet(player_turn)
        self._roster = None
        self._king = None
        self._in_check = False
        self._possible_moves = []
        self._roster = []

    def get_turn(self):
        return self._player_turn

    def get_color(self):
        return self._color

    def get_king(self):
        return self._king

    def set_king(self, king):
        self._king = king

    def get_roster(self):
        return self._roster

    def set_roster(self, roster):
        self._roster = roster

    def get_pos_moves(self):
        return self._possible_moves

    def set_pos_moves(self, possible_moves):
        self._possible_moves = possible_moves
