from game_engine import chess_manip
from game_engine import pieces_moves
from game_engine import game_objects
from functools import *
import random


# Global constants
CHECKMATE = 1000
STALEMATE = 0
PAWN_COST_VALUE = game_objects.GameObjects.PAWN_COST_VALUE
KNIGHT_COST_VALUE = game_objects.GameObjects.KNIGHT_COST_VALUE
BISHOP_COST_VALUE = game_objects.GameObjects.BISHOP_COST_VALUE
ROOK_COST_VALUE = game_objects.GameObjects.ROOK_COST_VALUE
QUEEN_COST_VALUE = game_objects.GameObjects.QUEEN_COST_VALUE

piece_value_cost = {"K": 100,
                    "p": 1,
                    "N": 3,
                    "B": 3.5,
                    "R": 5,
                    "Q": 9,
                    }

piece_position_cost_value = {"wN": KNIGHT_COST_VALUE,
                             "bN": KNIGHT_COST_VALUE[::-1],
                             "wB": BISHOP_COST_VALUE,
                             "bB": BISHOP_COST_VALUE[::-1],
                             "wQ": QUEEN_COST_VALUE,
                             "bQ": QUEEN_COST_VALUE[::-1],
                             "wR": ROOK_COST_VALUE,
                             "bR": ROOK_COST_VALUE[::-1],
                             "wp": PAWN_COST_VALUE,
                             "bp": PAWN_COST_VALUE[::-1],
                            }


class AI:
    def __init__(self, difficulty_level=0) -> None:
        self.DEPTH = difficulty_level + 2

    def opening_move(self, move_as_black=False, game_manip=None):
        if move_as_black and game_manip.board[4][3] == "wp":
            move = pieces_moves.Move([1, 3], [3, 3], game_manip.board)  # Queen
            game_manip.make_move(move)
        elif move_as_black and game_manip.board[4][4] == "wp":
            if random.randint(0, 5) >= 4:
                move = pieces_moves.Move([1, 2], [3, 2], game_manip.board)  # Sicilian
                game_manip.make_move(move)
            else:
                move = pieces_moves.Move([1, 4], [3, 4], game_manip.board)  # King
                game_manip.make_move(move)
        else:
            if random.randint(0, 4) < 4:
                move = pieces_moves.Move([1, 4], [3, 4], game_manip.board)  # King
                game_manip.make_move(move)
            else:
                if random.randint(0, 4) < 4:
                    move = pieces_moves.Move([1, 3], [3, 3], game_manip.board)  # Queen
                    game_manip.make_move(move)
                else:
                    move = pieces_moves.Move([1, 5], [3, 5], game_manip.board)  # Sicilian
                    game_manip.make_move(move)
        return move

    def find_best_move(self, move_counter, game_manip, valid_moves, return_queue) -> None:
        global next_move

        next_move = None
        random.shuffle(valid_moves)
        self.find_best_comparecent_move(move_counter, game_manip, valid_moves, self.DEPTH, -CHECKMATE, CHECKMATE, 1 if game_manip.white_to_move else -1)
        return_queue.put(next_move)

    def score_board(self, game_manip) -> float:
        score = 0

        for row in range(len(game_manip.board)):
            for col in range(len(game_manip.board[row])):
                piece = game_manip.board[row][col]

                if piece != "--":
                    piece_position_score = 0

                    if piece[1] != "K":
                        piece_position_score = piece_position_cost_value[piece][row][col]

                    if piece[0] == "w":
                        score += piece_value_cost[piece[1]] + piece_position_score

                    if piece[0] == "b":
                        score -= piece_value_cost[piece[1]] + piece_position_score

        return score

    def find_best_comparecent_move(self, move_counter, game_manip, valid_moves, depth, alpha, beta, turn_multiplier) -> float:
        global next_move

        if depth == 0:
            return turn_multiplier * self.score_board(game_manip)

        max_score = -CHECKMATE

        for move in valid_moves:
            if (move_counter < 6 and str(move)[0] == "Q") and not (game_manip.board[3][4] == "bp"):
                continue
            else:
                game_manip.make_move(move)
                next_moves = game_manip.get_valid_moves()
                score = - self.find_best_comparecent_move(move_counter, game_manip, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)

                if score > max_score:
                    max_score = score

                    if depth == self.DEPTH:
                        next_move = move

                game_manip.undo_move()

                if max_score > alpha:
                    alpha = max_score

                if alpha >= beta:
                    break
        
        return max_score

    def find_random_move(self, valid_moves):
        return random.choice(valid_moves)
