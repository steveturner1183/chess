from pieces import *


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
    def __init__(self):
        self._cols = "abcdefgh"
        self._rows = "12345678"

    def _get_board_col_row(self, loc: str) -> (int, int):
        """
        Returns board grid coordinates for given location
        :param loc: Chess coordinate location, example "a1"
        :return: Grid coordinates for given location
        """
        col, row = loc[0], loc[1]
        return self._cols.index(col), self._rows.index(row)

    def _get_board_loc(self, loc: str, board):
        """
        Retrieves value at given board location
        :param loc: Chess coordinate location, example "a1"
        :return: Piece if piece at given location, otherwise None
        """
        col, row = self._get_board_col_row(loc)
        return board[row][col]

    #####################################################################
    # Check
    #
    # Rule description:
    #
    #
    #####################################################################

    def check(self, attacking_player, defending_player, board):
        def_player_in_check = False

        def_king = defending_player.get_king()
        def_king_loc = def_king.get_location()
        atk_roster = attacking_player.get_roster()

        # See if any pieces in oppenents roster can capture King
        for atk_piece in atk_roster:
            atk_moves = atk_piece.get_possible_moves()

            if atk_piece.get_name() == "Pawn":
                if def_king_loc in atk_moves["CAPTURE"]:
                    in_check = board.validate_move(atk_piece.get_location(),
                                                   def_king_loc)
                    if in_check:
                        def_player_in_check = True
            else:
                if def_king_loc in atk_moves:
                    in_check = board.validate_move(atk_piece.get_location(),
                                                   def_king_loc)
                    if in_check:
                        def_player_in_check = True
                    if self.checkmate(attacking_player, defending_player,
                                           atk_moves[def_king_loc], atk_piece,
                                           board):
                        print("checkmate")

        return def_player_in_check

    #####################################################################
    # Checkmate
    #
    # Rule description:
    #
    #
    #####################################################################

    def checkmate(self, attacking_player, defending_player, attack_moves,
                   attack_piece, board):
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

        def_king = defending_player.get_king()
        def_king_loc = def_king.get_location()
        def_roster = defending_player.get_roster()

        for atk_move in attack_moves:  ########## SWAP AND just check if piece move is in attack moves???????????????????????????????????????????????
            for piece in def_roster:
                piece_moves = piece.get_possible_moves()  ######### PAWN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

                if piece.get_name() == "King":

                    for move in piece_moves:
                        valid_move = board.validate_move(def_king_loc, move)
                        self_in_check = self.self_into_check(move,
                                                             attacking_player.get_roster())  ####### this validation already needs to occur elseware !!!!!!!!!!!!!!!!!

                        if valid_move is True and self_in_check is False:
                            #  2. King captures attacking piece
                            if move == atk_move and atk_move == attack_piece.get_location():
                                return False

                            #  1. King moves to new location
                            if move != atk_move and move not in attack_moves:
                                return False

                #  3. Another piece blocks path to the king
                #  4. Another piece captures the attacking piece
                elif piece.get_name() != "King":
                    valid_move = board.validate_move(piece.get_location(),
                                                     atk_move)

                    if atk_move in piece_moves and valid_move is True:
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
            if piece.get_name() != "Pawn":
                all_moves = piece.get_possible_moves()
                if king_move in all_moves:
                    return True

            ## ADDD PAWNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
        return False

    #####################################################################
    # En passant
    #
    # Rule description:
    #
    #
    #####################################################################

    ## add to function call ---- self._board
    def check_en_passant(self, pawn, start_loc, end_loc, board):
        """
        Checks if given pawn can be captured from en passant, and sets the
        capturing pieces available moves to include en passant if true
        :param pawn:
        :return:
        """
        for row in board:
            for piece in row:
                if piece is not None and piece.get_name() == "Pawn":
                    piece.clear_en_passant()

        # Only Pawn that moves 2 spaces is eligable
        spaces_moved = abs(
            self._rows.index(start_loc[1]) - self._rows.index(end_loc[1]))
        if spaces_moved != 2:
            return

        cur_loc = pawn.get_location()
        cur_col, cur_row = self._get_board_col_row(cur_loc)

        # Check east and west neighbor to see if they can perform en passant next turn
        for direction in 1, -1:
            neighbor_col = cur_col + direction
            board_boundary = range(8)

            if neighbor_col in board_boundary:
                neighbor = self._get_board_loc(self._cols[neighbor_col] + cur_loc[1], board)

                if neighbor is not None and neighbor.get_name() == "Pawn":
                    if neighbor.get_player() == 1:  # Move north of target pawn
                        en_move = cur_loc[0] + self._rows[cur_row + 1]
                    else:  # Move south
                        en_move = cur_loc[0] + self._rows[cur_row - 1]

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

        if king.get_name != "King":
            return False

        cur_col, cur_row = board.get_board_col_row(cur_loc)
        tar_col, tar_row = board.get_board_col_row(tar_loc)
        col_move = cur_col - tar_col
        row_move = tar_col - tar_row

        if row_move != 0:
            return False

        if col_move == 2:  # Castle left
            direction = -1
            rook_col = 0
        elif col_move == -2:  # Castle right
            direction = 1
            rook_col = 7
        else:
            return False

        rook_loc = board.format_board_loc(rook_col, cur_row)
        rook = board.get_board_loc(rook_loc)

        if king.has_moved() or rook.has_moved():
            return False

        # ADD DIRECTIONAL MOVE TO BOARD

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
    # Draw after 3 identical moves
    #
    # Rule description:
    #
    #
    #####################################################################
    def draw_3_moves(self):
        pass