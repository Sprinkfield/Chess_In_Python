class Elo:
    def calculate_elo(game_manip, elo, result, side, turns) -> int:
        score = Elo.score_board(game_manip, side)
        side = 0**side  # side: 0 -> 1, 1 -> 0.
        new_elo = elo + 2*((0**side)*(score/turns) + (20*score/turns)**result - (0**abs(result))*(4*score/turns) - (20*score/turns)**(-result))
        return int(new_elo) if new_elo > 0 else 0

    def set_difficulty(elo) -> int:
        if elo < 1000:
            diff_lvl = 0
        elif 1000 <= elo <= 2000:
            diff_lvl = 1
        elif elo > 2000:
            diff_lvl = 2
        return diff_lvl

    def calc_mis_chance(elo) -> int:
        #  Actual chance = 1 / chance
        if elo <= 500:
            chance = 2
        elif 500 < elo < 1000:
            chance = 4
        elif 1000 <= elo <= 1500:
            chance = 10
        elif 1500 < elo < 2000:
            chance = 20
        elif 2000 <= elo <= 2200:
            chance = 100
        else:
            chance = 1000
        return chance
    
    def score_board(game_manip, side) -> float:
        score = 0
        side = "w" if side == 0 else "b"
        piece_value_cost = {"p": 1, "N": 3, "B": 3.5, "R": 5, "Q": 9, "K": 100}

        for row in range(len(game_manip.board)):
            for col in range(len(game_manip.board[row])):
                piece = game_manip.board[row][col]
                if piece != "--":
                    if piece[0] == "w" and side == "w":
                        score += piece_value_cost[piece[1]]
                    elif piece[0] == "b" and side == "b":
                        score += piece_value_cost[piece[1]]

        return score
