import unittest
from pieces import *
from board import *
from chess import *
import logging
logging.basicConfig(level=logging.DEBUG)


class TestPieces(unittest.TestCase):

    def test_queen(self):
        queen = Queen("e5")
        queen.set_player("player_1")
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
        king = King("e5")
        king.set_player("player_1")
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
        rook = Rook("e5")
        rook.set_player("player_1")
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
        bishop = Bishop("e5")
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

    """ REDIZZLEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE########@%#$^%$&34m
    def test_pawn_first_move(self):
        pawn = Pawn("e5")
        pawn.set_player(1)
        expected = {

            # North
            "e6": ["e6"],
            "e7": ["e6", "e7"],

        }
        actual = pawn.get_possible_moves()
        self.assertEqual(expected, actual)

    def test_pawn_second_move(self):
        pawn = Pawn("e5")
        pawn.set_player(1)
        expected = {
            # North
            "e6": ["e6"],
        }
        pawn.made_first_move()
        actual = pawn.get_possible_moves()
        self.assertEqual(expected, actual)
    """

    def test_pawn_en_passant(self):
        game = Chess()
        moves = ["d2 d4", "a7 a6", "d4 d5", "e7 e5", "d5 e6"]
        for move in moves:
            logging.debug("Testing move {}".format(move))
            self.assertTrue(game.check_game_rules(move))
            game.make_move(move[:2], move[-2:])
            game.set_player_turn()

    def test_blocked_pawn_move_1(self):
        logging.debug("----test_blocked_pawn_move_1----")
        game = Chess()
        moves = ["b1 b3", "a7 a6", "b2 b3"]
        count = 0
        for move in moves:
            count += 1
            logging.debug("Testing move {}".format(move))
            if count == 3:
                self.assertFalse(game.check_game_rules(move))
            else:
                game.make_move(move[:2], move[-2:])
                game.set_player_turn()

    def test_blocked_pawn_move_2(self):
        logging.debug("T----test_blocked_pawn_move_2----")
        game = Chess()
        moves = ["a2 a4", "a7 a5", "a4 a5"]
        count = 0
        for move in moves:
            count += 1
            logging.debug("Testing move {}".format(move))
            if count == 3:
                self.assertFalse(game.check_game_rules(move))
            else:
                game.make_move(move[:2], move[-2:])
                game.set_player_turn()

    def test_queen_pawn_move(self):
        logging.debug("----test_queen_pawn_move----")
        game = Chess()
        move = "d1 d2"
        self.assertFalse(game.check_game_rules(move))

if __name__ == '__main__':
    unittest.main()
