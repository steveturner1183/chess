from board import GameBoard
from player import Player


class Chess:
    def __init__(self):
        self._game_status = "INCOMPLETE"
        self._p1 = Player("Human", "W")
        self._p2 = Player("Human", "B")
        self._board = GameBoard(self._p1, self._p2)
        self._player_turn = "1"

    def make_move(self, start_loc, end_loc):
        # validate the game is not over - is this needed? will freeze after game completion
        # check there is a piece in that location and who it is owned by
        # validate it is that players turn
        # validate with board that move can be made
        # check? checkmate? draw?
        # restart loop
        pass