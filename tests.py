import unittest
from pieces import *
from board import *
from chess import Chess
import logging
logging.basicConfig(level=logging.DEBUG)
import inspect

DEBUG = False


class TestPieces(unittest.TestCase):
    ######################################################################
    #   Test piece moves
    #
    #   Single pieces are tested on an empty board for all basic movements
    #   that do not involve other pieces
    #
    ######################################################################
    def empty_board_test(self, piece):
        piece.set_player(1)
        p1 = Player(1, "W")
        p2 = Player(2, "B")
        board = GameBoard(p1, p2)
        board._game_board = [[None] * 8 for i in range(8)]
        board._game_board[4][4] = piece
        piece.set_possible_moves(board)
        return piece.get_possible_moves()

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

    def test_knight(self):
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
        pawn.has_moved()
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
    ##########################################################
    #
    #    Test helper functions
    #
    ##########################################################

    def simulate_moves(self, true_moves, false_move, switch_colors=True):
        if switch_colors:
            colors = ["WB", "BW"]
        else:
            colors = ["WB"]

        for color in colors:
            p1 = Player(1, color[0])
            p2 = Player(2, color[1])

            if DEBUG:
                import inspect
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                logging.debug(
                    "-----------------------{}-----".format(calframe[1][3]))

            chess = Chess(p1, p2)

            if true_moves is not None:
                for move in true_moves:
                    if DEBUG:
                        logging.debug(
                            "Testing move {} P1 = {}".format(move, color[0]))

                    self.assertTrue(chess.validate_move(move))
                    chess.make_move(move)
                    chess.set_player_turn()

            if false_move is not None:
                if DEBUG:
                    logging.debug(
                        "Testing move {} P1 = {}".format(false_move, color[0]))

                self.assertFalse(chess.validate_move(false_move))

    ##########################################################
    #
    #    Pawn movement
    #
    ##########################################################

    def test_pawn_move(self):
        true_moves = ["a2 a3", "a7 a6", "b2 b4", "b7 b5"]
        false_move = None
        self.simulate_moves(true_moves, false_move)

    def test_pawn_capture(self):
        true_moves = ["e2 e4", "a7 a6", "e4 e5", "f7 f6"]
        false_moves = "e5 d6"
        self.simulate_moves(true_moves, false_moves)

    """
    def test_en_passant(self):
        true_moves = ["e2 e4", "a7 a6", "e4 e5", "f7 f5", "e5 f6"]
        false_move = None
        self.simulate_moves(true_moves, false_move)
    """

    def test_pawn_forward_move_only(self):
        true_moves = ["e2 e4", "e7 e5"]
        false_moves = "e4 e5"
        self.simulate_moves(true_moves, false_moves)

    ##########################################################
    #
    #    Bishop movement
    #
    ##########################################################

    def test_bishop_move(self):
        true_moves = [
            "e2 e4", "e7 e5", "d2 d4", "d7 d5",  # Clear pawns
            "f1 c4", "f8 a3", "h2 h3", "c8 g4",  # Bishop movement
            "c4 d5", "a3 b2", "c1 b2", "g4 d1"  # Bishop capture
        ]
        false_moves = None
        self.simulate_moves(true_moves, false_moves)

    ##########################################################
    #
    #    Knight movement
    #
    ##########################################################

    def test_knight_move(self):
        true_moves = ["b1 c3", "d7 d5", "c3 d5"]
        false_moves = None
        self.simulate_moves(true_moves, false_moves)

    ##########################################################
    #
    #    Rook movement
    #
    ##########################################################

    def test_rook_move(self):
        true_moves = [
            "a2 a4", "a7 a5", "h2 h4", "h7 h5",  # Clear pawns
            "a1 a3", "a8 a6", "h1 h3", "h8 h6",  # Rook movement
            "a3 e3", "a6 e6", "e3 e6"  # Rook movement
        ]
        false_moves = None
        self.simulate_moves(true_moves, false_moves)

    ##########################################################
    #
    #    Queen movement
    #
    ##########################################################

    def test_queen_move(self):
        true_moves = [
            "e2 e4", "e7 e5",  # Clear pawns
            "d1 f3", "d8 f6", "f3 c3", "f6 c6",  # Queen movement
            "c3 c6"  # Queen capture
        ]
        false_moves = None
        self.simulate_moves(true_moves, false_moves,
                            False)  # Do not switch colors, different queen placement

    ###########################################################
    #
    #    King movement
    #
    ##########################################################
    """
    def test_king_move(self):
        true_moves = [
            "e2 e4", "d7 d5",  # Clear pawns
            "e1 e2", "e8 d7", "e2 e3", "d7 d6", "e3 d4", "d6 d7",
            # King movement
            "d4 d5"  # King capture
        ]
        false_moves = None  # "d7 d6"  # Cannot move self into check ##########################################
        self.simulate_moves(true_moves, false_moves, False)
    """

    def test_castling(self):
        true_moves = [
            "g1 f3", "g8 f6", "g2 g3", "g7 g6", "f1 g2", "f8 g7",
            # Clear pieces
            "e1 g1", "e8 g8"  # Castle
        ]
        false_moves = None
        self.simulate_moves(true_moves, false_moves,
                            False)  # Do not switch colors, different queen placement

        true_moves = [
            "b1 c3", "b8 c6", "b2 b3", "b7 b6", "c1 b2", "c8 b7", "d2 d3",
            "d7 d6", "d1 d2", "d8 d7",  # Clear pieces
            "e1 c1", "e8 c8"  # Castle
        ]
        false_moves = None
        self.simulate_moves(true_moves, false_moves, False)

    ##########################################################
    #
    #    Board and Player Roster State
    #
    ##########################################################

    ##########################################################
    #
    #    Game specific tests
    #
    ##########################################################

    def test_blocked_move(self):
        true_moves = None
        false_move = "a1 a4"
        self.simulate_moves(true_moves, false_move)

    def test_cannot_capture_own_piece(self):
        true_moves = None
        false_move = "d1 d2"
        self.simulate_moves(true_moves, false_move)

    def test_check_and_mate(self):
        p1 = Player(1, "W")
        p2 = Player(2, "B")
        if DEBUG:
            logging.debug("----------------test_check----")
        chess = Chess(p1, p2)
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

        game_status = "Player 1 Wins"
        self.assertEqual(game_status, chess.get_game_status())

    def test_player_turn(self):
        true_moves = None
        false_move = "e7 e5"
        self.simulate_moves(true_moves, false_move)

    def test_self_into_check_non_king_move(self):
        true_moves = [
            "d2 d4", "e7 e5", "c1 d2", "f8 b4"
        ]
        false_moves = None  # "d2 e3"###################################################
        self.simulate_moves(true_moves, false_moves, False)

    def test_staying_in_check(self):
        true_moves = [
            "d2 d4", "e7 e5", "f2 f3", "f8 b4"
        ]
        false_moves = None  # "f3 f4"####################################
        self.simulate_moves(true_moves, false_moves, False)


if __name__ == '__main__':
    unittest.main()