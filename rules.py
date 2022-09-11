from pieces import *
import logging
from copy import deepcopy

###########################################################
# Chess Rules
#
# Contains all rules of chess included in this project

# Check
# Checkmate
# Self into check
# En Passant
# Pawn Transformation
# Castle
# Draw
# 3 move draw
#
# Piece responsible for analyzing board state
# Look at moves when king is in check
# !!!!!!!!!!!!!!!!!!! Should he entire baord just be reversed
# when first player is black
# Relativity!
# Start adding try and except clauses
# Function - should only do one thing, 10 lines of code try, no more than one level of indentation, less paragraph breaks
# Single leading undescore for class use only
# First word is capitalized
###########################################################


class ChessRules:

    #####################################################################
    # Check
    #
    # Rule description:
    #
    #
    #####################################################################

    def check(self, oppenent, defending_player):
        def_player_in_check = False

        def_king = defending_player.get_king()
        def_king_loc = def_king.get_location()
        opp_roster = oppenent.get_roster()

        # See if any pieces in oppenents roster can capture King
        for opp_piece in opp_roster:
            opp_moves = opp_piece.get_possible_moves()

            if def_king_loc in opp_moves:
                def_player_in_check = "CHECK"
                print(opp_piece)
                print(opp_moves)
                if self.checkmate(oppenent, defending_player,
                                  opp_moves[def_king_loc], opp_piece):
                    def_player_in_check = "CHECKMATE"
        return def_player_in_check

    #####################################################################
    # Checkmate
    #
    # Rule description:
    #
    #
    #####################################################################

    def checkmate(self, attacking_player, defending_player, attack_moves,
                   attack_piece):
        """
        Checks to see if opponents piece is in checkmate, i.e see if there are
        any ways to get out of check
        Chess Rule - Ways to get out of check:
        1. King moves to new location
        2. King captures attacking piece
        3. Another piece blocks path to the king
        4. Another piece captures the attacking piece
        :param player_moved:
        :param moves:
        :return:
        """
        def_roster = defending_player.get_roster()

        for atk_move in attack_moves:  ########## SWAP AND just check if piece move is in attack moves???????????????????????????????????????????????
            for piece in def_roster:
                piece_moves = piece.get_possible_moves()  ######### PAWN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                if piece.get_name() == "King":
                    for move in piece_moves:
                        self_in_check = self.self_into_check(move,
                                                             attacking_player.get_roster())  ####### this validation already needs to occur elseware !!!!!!!!!!!!!!!!!

                        if self_in_check is False:
                            #  2. King captures attacking piece
                            if move == atk_move and atk_move == attack_piece.get_location():
                                return False

                            #  1. King moves to new location
                            if move != atk_move and move not in attack_moves:
                                return False

                #  3. Another piece blocks path to the king
                #  4. Another piece captures the attacking piece
                elif piece.get_name() != "King":
                    if atk_move in piece_moves:
                        return False

        return True

    #####################################################################
    # Self into check
    #
    # Rule description:
    #
    #
    #####################################################################
    def self_into_check(self, king_move, opp_roster):

        for piece in opp_roster:
            all_moves = piece.get_possible_moves()
            if king_move in all_moves:
                return True

        return False

    #####################################################################
    # En passant
    #
    # Rule description:
    #
    #
    #####################################################################

    def en_passant(self, pawn, start_loc, end_loc, board):
        """
        Checks if given pawn can be captured from en passant, and sets the
        capturing pieces available moves to include en passant if true
        :param pawn:
        :return:
        """
        if pawn.get_name() != "Pawn":
            return

        cur_loc = pawn.get_location()
        rows = board.get_cols_and_rows()[1]

        # Only Pawn that moves 2 spaces is eligible
        move_start = rows.index(start_loc[1])
        move_end = rows.index(end_loc[1])
        eligible_move = abs(move_start - move_end) == 2

        if not eligible_move:
            return

        # Check east and west neighbor to see if they can perform en passant next turn
        for direction in 1, -1:
            neighbor_loc = board.get_neighbor_loc(cur_loc, direction, 0)

            if neighbor_loc is not None:
                neighbor = board.get_board_loc(neighbor_loc)

                if neighbor is not None and neighbor.get_name() == "Pawn":

                    if neighbor.get_color() == "W":  # Move north of target pawn
                        en_move = board.get_neighbor_loc(cur_loc, 0, 1)
                    else:  # Move south
                        en_move = board.get_neighbor_loc(cur_loc, 0, -1)

                    neighbor.set_en_passant(cur_loc, en_move)

    # SET THIS IN BOARD
    #####################################################################
    # Pawn Transformation
    #
    # Rule description:
    #
    #
    #####################################################################
    def pawn_transform(self, pawn, transform_selection):
        pawn_loc = pawn.get_location()
        pawn_player = pawn.get_player()
        pawn_color = pawn.get_color()

        pieces = {
            "Queen": Queen(pawn_loc),
            "Rook": Rook(pawn_loc),
            "Knight": Knight(pawn_loc),
            "Bishop": Bishop(pawn_loc)
        }

        transform = pieces[transform_selection]
        transform.set_location(pawn_loc)
        transform.set_player(pawn)
        transform.set_image(pawn_color)

        return transform

    # add board functions for castling and attributes for if baord castled
    # add tracker to see if piece has moved
    #####################################################################
    # Castle
    #
    # Rule description:
    #
    #
    #####################################################################
    def castle(self, cur_loc, tar_loc, board):
        # Has the king moved?
        # Has the rook moved?
        # What direction?
        # Is the path clear? king put in check on travel to path?
        # do not think you can castle out of check???

        king = board.get_board_loc(cur_loc)

        cur_col, cur_row = board.get_board_col_row(cur_loc)
        tar_col, tar_row = board.get_board_col_row(tar_loc)
        col_move = cur_col - tar_col
        row_move = tar_row - tar_row

        if row_move != 0:
            logging.debug("Not horizontal move")
            return False

        if col_move == 2:  # Castle left
            direction = -1
            rook_col = 0
        elif col_move == -2:  # Castle right
            direction = 1
            rook_col = 7
        else:
            return False

        rook_loc = board.get_location_format(rook_col, cur_row)
        rook = board.get_board_loc(rook_loc)

        for col in range(cur_col + direction, rook_col, direction):
            piece_loc = board.get_location_format(col, cur_row)
            piece = board.get_board_loc(piece_loc)
            if piece is not None:
                return False

        if king.has_moved() or rook.has_moved():
            return False

        return True

    #####################################################################
    # Draw
    #
    # Rule description:
    #
    #
    #####################################################################
    def draw(self, player):
        roster = player.get_roster()
        for piece in roster:
            moves = piece.get_possible_moves()
            if piece.get_name != "Pawn":
                if len(moves) != 0:
                    return False
            else:
                for move_set in roster:
                    if len(move_set) != 0:
                        return False
        return True

    #####################################################################
    # Player is still in check after move
    #
    # Rule description:
    #
    #
    #####################################################################

    def still_in_check(self, move, game):
        new_game = deepcopy(game)
        new_game.make_move(move)

        if new_game.get_player_turn() == 1:
            atk_player = new_game.get_player(2)
            def_player = new_game.get_player(1)
        else:
            atk_player = new_game.get_player(1)
            def_player = new_game.get_player(2)

        if self.check(atk_player, def_player) is not False:
            return False
        else:
            print("Player turn", new_game.get_player_turn())
            print("atk_player", atk_player)
            print(self.check(atk_player, def_player))

    #####################################################################
    # Draw after 3 identical moves
    #
    # Rule description:
    #
    #
    #####################################################################
    def draw_3_moves(self):
        pass