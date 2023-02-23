from game_engine.game_objects import GameObjects


class Move:
    """Class that handles all movements, including AI's."""
    ranks_to_rows = GameObjects.ranks_to_rows
    rows_to_ranks = GameObjects.rows_to_ranks
    files_to_cols = GameObjects.files_to_cols
    cols_to_files = GameObjects.cols_to_files

    def __init__(self, start_square, end_square, board, is_enpassant_move=False, is_castle_move=False) -> None:
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        
        self.is_pawn_promotion = self.piece_moved[1] == "p" and (self.end_row == 0 or self.end_row == 7)
        self.is_castle_move = is_castle_move
        self.is_enpassant_move = is_enpassant_move

        if self.is_enpassant_move:
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"

        self.is_capture = self.piece_captured != "--"
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        else:
            return False

    def get_chess_notation(self) -> str:
        if self.is_pawn_promotion:
            return self.get_rank_files(self.end_row, self.end_col) + "Q"

        if self.is_castle_move:
            if self.end_col == 1:
                return "0-0-0"
            else:
                return "0-0"

        if self.is_enpassant_move:
            return self.get_rank_files(self.start_row, self.start_col)[0] + "x" + self.get_rank_files(self.end_row, self.end_col) + " e.p."

        if self.piece_captured != "--":
            if self.piece_moved[1] == "p":
                return self.get_rank_files(self.start_row, self.start_col)[0] + "x" + self.get_rank_files(self.end_row, self.end_col)
            else:
                return self.piece_moved[1] + "x" + self.get_rank_files(self.end_row, self.end_col)
        else:
            if self.piece_moved[1] == "p":
                return self.get_rank_files(self.end_row, self.end_col)
            else:
                return self.piece_moved[1] + self.get_rank_files(self.end_row, self.end_col)

    def get_rank_files(self, row, col) -> str:
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def __str__(self) -> str:
        if self.is_castle_move:
            return "0-0" if self.end_col == 6 else "0-0-0"

        end_square = self.get_rank_files(self.end_row, self.end_col)

        if self.piece_moved[1] == "p":
            if self.is_capture:
                return self.cols_to_files[self.start_col] + "x" + end_square
            else:
                return end_square + "Q" if self.is_pawn_promotion else end_square

        move_string = self.piece_moved[1]

        if self.is_capture:
            move_string += "x"
            
        return move_string + end_square


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
