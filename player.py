from pieces import *

class Player:
    def __init__(self, player_type, player_color):
        self._type = player_type
        self._color = player_color
        self._roster = []


    def get_color(self):
        return self._color