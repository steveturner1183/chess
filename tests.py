import unittest
from pieces import *
from board import *
from chess import Chess

DEBUG = True


class TestPieces(unittest.TestCase):
    def empty_board_test(self, piece):
        piece.set_player(1)
        p1 = Player(1, "W")
        p2 = Player(2, "B")
        board = GameBoard(p1, p2)
        board._game_board = [[None] * 8 for i in range(8)]
        board.set_board_loc("e5", piece)
        piece.set_possible_moves(board)
        return piece.get_possible_moves(board)

    def test_queen(self):
        queen = Queen("e5")
        actual = self.empty_board_test(queen)
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
        self.assertEqual(expected, actual)

    def test_king(self):
        king = King("e5")
        actual = self.empty_board_test(king)
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
        self.assertEqual(expected, actual)

    def test_rook(self):
        rook = Rook("e5")
        actual = self.empty_board_test(rook)
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
        self.assertEqual(expected, actual)

    def test_bishop(self):
        bishop = Bishop("e5")
        actual = self.empty_board_test(bishop)
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
        self.assertEqual(expected, actual)

    def test_knight_move(self):
        knight = Knight("e5")
        actual = self.empty_board_test(knight)

        expected = {
            # North
            "d7": ["d7"],
            "f7": ["f7"],

            # East
            "g6": ["g6"],
            "g4": ["g4"],

            # South
            "f3": ["f3"],
            "d3": ["d3"],

            # West
            "c6": ["c6"],
            "c4": ["c4"]
        }

        self.assertDictEqual(expected, actual)

    def test_pawn_second_move(self):
        pawn = Pawn("e5")
        pawn.made_first_move()
        actual = self.empty_board_test(pawn)

        expected = {
            # North
            "e6": ["e6"]
        }

        self.assertDictEqual(expected, actual)

    def test_pawn_first_move(self):
        pawn = Pawn("e5")
        actual = self.empty_board_test(pawn)
        expected = {
            # North
            "e6": ["e6"], "e7": ["e6", "e7"]
        }

        self.assertDictEqual(expected, actual)

    ##### TEST MOVES ############

    def simulate_moves(self, true_moves, false_move):
        if DEBUG:
            import inspect
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            logging.debug("----{}-----".format(calframe[1][3]))

        chess = Chess()

        if true_moves is not None:
            for move in true_moves:
                if DEBUG:
                    logging.debug("Testing move {}".format(move))

                self.assertTrue(chess.validate_move(move))
                chess.make_move(move)
                chess.set_player_turn()

        if false_move is not None:
            if DEBUG:
                logging.debug("Testing move {}".format(false_move))

            self.assertFalse(
                chess.validate_move(false_move))

    def test_pawn_move(self):
        true_moves = ["a2 a3"]
        false_move = None
        self.simulate_moves(true_moves, false_move)

    def test_blocked_move(self):
        true_moves = None
        false_move = "a1 a4"
        self.simulate_moves(true_moves, false_move)

    def test_en_passant(self):
        true_moves = ["e2 e4", "a7 a6", "e4 e5", "f7 f5", "e5 f6"]
        false_move = None
        self.simulate_moves(true_moves, false_move)

    def test_pawn_diag_move(self):
        true_moves = ["e2 e4", "a7 a6", "e4 e5", "f7 f6"]
        false_moves = "e5 d6"
        self.simulate_moves(true_moves, false_moves)

    def test_pawn_move_only(self):
        true_moves = ["e2 e4", "e7 e5"]
        false_moves = "e4 e5"
        self.simulate_moves(true_moves, false_moves)

    def test_knight_move_and_capture(self):
        true_moves = ["b1 c3", "d7 d5", "c3 d5"]
        false_moves = None
        self.simulate_moves(true_moves, false_moves)

    def test_check(self):
        logging.debug("----test_check----")
        chess = Chess()
        moves = ["e2 e3", "f7 f6", "c2 c3", "g7 g5"]

        for move in moves:
            if DEBUG:
                logging.debug("Testing move {}".format(move))

            self.assertTrue(chess.validate_move(move))
            chess.make_move(move)
            chess.set_player_turn()

        move = "d1 h5"
        self.assertTrue(chess.validate_move(move))
        chess.make_move(move)

        chess.king_check_status()
        self.assertTrue(chess.get_player(2).get_in_check())


if __name__ == '__main__':
    unittest.main()