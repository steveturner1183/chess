from pieces import *
import random
import time


class Player:
    def __init__(self, player_turn, player_color):
        self._player_turn = player_turn
        self._color = player_color
        self._roster = None
        self._king = None
        self._in_check = False
        self._possible_moves = []
        self._captured_pieces = []

    def __repr__(self):
        return repr("Player " + str(self._player_turn))

    def set_in_check(self, value):
        self._in_check = value

    def get_in_check(self):
        return self._in_check

    def remove_piece(self, piece):
        self._captured_pieces.append(piece)
        self._roster.remove(piece)

    def get_captured_pieces(self):
        return self._captured_pieces

    def get_turn(self):
        return self._player_turn

    def get_color(self):
        return self._color

    def get_king(self):
        return self._king

    def get_roster(self):
        return self._roster

    def set_roster(self, roster):
        self._roster = roster
        self._king = roster[4]

    def get_pos_moves(self):
        return self._possible_moves

    def set_pos_moves(self, possible_moves):
        self._possible_moves = possible_moves


class RandomBot(Player):
    def __init__(self, player_turn, player_color):
        super().__init__(player_turn, player_color)

    def get_move(self):
        moves = []
        piece = None
        while len(moves) < 1:
            piece = random.choice(self._roster)
            moves = piece.get_possible_moves()

        move = random.choice(list(moves.keys()))
        start_loc = piece.get_location()
        end_loc = move

        print(move)

        return start_loc + " " + end_loc
