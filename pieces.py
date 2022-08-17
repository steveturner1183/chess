class GamePiece:
    def __init__(self):
        self._player = None
        self._cur_loc = None
        self._name = None
        self._rows = "12345678"
        self._cols = "abcdefgh"
        self._col_to_int = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5,
                            "g": 6, "h": 7}
        self._row_to_int = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5,
                            "7": 6, "8": 7}
        self._directions = {"N": (0, 1), "NE": (1, 1), "E": (1, 0),
                            "SE": (1, -1), "S": (0, -1), "SW": (-1, -1),
                            "W": (-1, 0), "NW": (-1, 1)}
        self._boundary = range(0, 8)
        self._move_set = []
        self._max_move = 7

        self._possible_moves = dict()

    def set_player(self, player):
        self._player = player

    def get_player(self):
        return self._player

    def set_location(self, location):
        self._cur_loc = location

    def get_name(self):
        return self._name

    def format_cell(self, col, row):
        return self._cols[col] + self._rows[row]

    def get_col_row(self, location):
        col = location[0]
        row = location[1]
        return (self._col_to_int[col], self._row_to_int[row])

    def get_possible_moves(self):
        self._possible_moves.clear()

        for directional_move in self._move_set:
            self.add_direction_move_set(directional_move)

        return self._possible_moves

    def add_direction_move_set(self, direction):
        move_step = self._directions[direction]
        cur_loc = self.get_col_row(self._cur_loc)

        col = cur_loc[0] + move_step[0]
        row = cur_loc[1] + move_step[1]

        possible_moves = []

        spaces_moved = 0
        while col in self._boundary and row in self._boundary and spaces_moved < self._max_move:
            target = self.format_cell(col, row)

            possible_moves.append(target)
            spaces_moved += 1
            col += move_step[0]
            row += move_step[1]

        for targets in possible_moves:
            self._possible_moves[targets] = self.find_path(targets, move_step)

    def find_path(self, target, move_step):
        move_path = []
        cur_loc = self.get_col_row(self._cur_loc)
        col = cur_loc[0]
        row = cur_loc[1]

        while cur_loc != target:
            col += move_step[0]
            row += move_step[1]
            cur_loc = self.format_cell(col, row)
            move_path.append(cur_loc)

        return move_path


class Queen(GamePiece):
    def __init__(self):
        super().__init__()
        self._name = "Queen"
        self._move_set = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


class King(GamePiece):
    def __init__(self):
        super().__init__()
        self._name = "King"
        self._move_set = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        self._max_move = 1


class Pawn(GamePiece):  ### Need attack move and en passant  ## need transformation
    def __init__(self):
        super().__init__()
        self._name = "Pawn"
        self._max_move = 2

    def set_player(self, player):
        self._player = player

        if self._player == "player_1":
            self._move_set = ["N"]
        else:
            self._move_set = ["S"]

    def set_max_move(self):  ### NEED TO CHANGE IN BOARD ###
        self._max_move = 1


class Knight(GamePiece):
    def __init__(self):
        super().__init__()
        self._directions = {"NE": (1, 2), "EN": (2, 1), "ES": (2, -1),
                            "SE": (1, -2), "SW": (-1, -2), "WS": (-2, -1),
                            "WN": (-2, 1), "NW": (-1, 2)}
        self._move_set = ["NE", "EN", "ES", "SE", "SW", "WS", "WN", "NW"]
        self._max_move = 1
        self._name = "Knight"


class Rook(GamePiece):
    def __init__(self):
        super().__init__()
        self._name = "Rook"
        self._move_set = ["N", "E", "S", "W"]


class Bishop(GamePiece):
    def __init__(self):
        super().__init__()
        self._name = "Bishop"
        self._move_set = ["NE", "SE", "SW", "NW"]
