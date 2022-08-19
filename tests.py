import unittest
from pieces import *
from board import *


class TestPieces(unittest.TestCase):
    def test_queen(self):
        queen = Queen()
        queen.set_player("player_1")
        queen.set_location("e5")
        expected = {
            # South
            "e1": ["e4", "e3", "e2", "e1"], "e2": ["e4", "e3", "e2"],
            "e3": ["e4", "e3"], "e4": ["e4"],
            # North
            "e6": ["e6"], "e7": ["e6", "e7"], "e8": ["e6", "e7", "e8"],
            # East
            "f5": ["f5"], "g5": ["f5", "g5"], "h5": ["f5", "g5", "h5"],
            # West
            "d5": ["d5"], "c5": ["d5", "c5"], "b5": ["d5", "c5", "b5"],
            "a5": ["d5", "c5", "b5", "a5"],
            # Northeast
            "f4": ["f4"], "g3": ["f4", "g3"], "h2": ["f4", "g3", "h2"],
            # Southeast
            "f6": ["f6"], "g7": ["f6", "g7"], "h8": ["f6", "g7", "h8"],
            # Southwest
            "d6": ["d6"], "c7": ["d6", "c7"], "b8": ["d6", "c7", "b8"],
            # Northwest
            "d4": ["d4"], "c3": ["d4", "c3"], "b2": ["d4", "c3", "b2"],
            "a1": ["d4", "c3", "b2", "a1"]
        }
        actual = queen.get_possible_moves()
        self.assertEqual(expected, actual)

    def test_king(self):
        king = King()
        king.set_player("player_1")
        king.set_location("e5")
        expected = {
            # South
            "e4": ["e4"],
            # North
            "e6": ["e6"],
            # East
            "f5": ["f5"],
            # West
            "d5": ["d5"],
            # Northeast
            "f4": ["f4"],
            # Southeast
            "f6": ["f6"],
            # Southwest
            "d6": ["d6"],
            # Northwest
            "d4": ["d4"],
        }
        actual = king.get_possible_moves()
        self.assertEqual(expected, actual)

    def test_rook(self):
        rook = Rook()
        rook.set_player("player_1")
        rook.set_location("e5")
        expected = {
            # South
            "e1": ["e4", "e3", "e2", "e1"], "e2": ["e4", "e3", "e2"],
            "e3": ["e4", "e3"], "e4": ["e4"],
            # North
            "e6": ["e6"], "e7": ["e6", "e7"], "e8": ["e6", "e7", "e8"],
            # East
            "f5": ["f5"], "g5": ["f5", "g5"], "h5": ["f5", "g5", "h5"],
            # West
            "d5": ["d5"], "c5": ["d5", "c5"], "b5": ["d5", "c5", "b5"],
            "a5": ["d5", "c5", "b5", "a5"]
        }
        actual = rook.get_possible_moves()
        self.assertEqual(expected, actual)

    def test_bishop(self):
        bishop = Bishop()
        bishop.set_player("player_1")
        bishop.set_location("e5")
        expected = {
            # Northeast
            "f4": ["f4"], "g3": ["f4", "g3"], "h2": ["f4", "g3", "h2"],
            # Southeast
            "f6": ["f6"], "g7": ["f6", "g7"], "h8": ["f6", "g7", "h8"],
            # Southwest
            "d6": ["d6"], "c7": ["d6", "c7"], "b8": ["d6", "c7", "b8"],
            # Northwest
            "d4": ["d4"], "c3": ["d4", "c3"], "b2": ["d4", "c3", "b2"],
            "a1": ["d4", "c3", "b2", "a1"]
        }
        actual = bishop.get_possible_moves()
        self.assertEqual(expected, actual)

    def test_pawn_first_move(self):
        pawn = Pawn()
        pawn.set_player("player_1")
        pawn.set_location("e5")
        expected = {

            # North
            "e6": ["e6"],
            "e7": ["e6", "e7"],

        }
        actual = pawn.get_possible_moves()
        self.assertEqual(expected, actual)

    def test_pawn_second_move(self):
        pawn = Pawn()
        pawn.set_player("player_1")
        pawn.set_location("e5")
        expected = {
            # North
            "e6": ["e6"],
        }
        pawn.set_max_move()
        actual = pawn.get_possible_moves()
        self.assertEqual(expected, actual)

    def test_pawn_move(self):
        p1 = Player("Human", "player_1")
        p2 = Player("Human", "player_2")
        board = GameBoard(p1, p2)
        self.assertTrue(board.validate_move("a7", "a6"))


if __name__ == '__main__':
    unittest.main()
