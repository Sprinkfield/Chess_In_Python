class Elo:
    def calculate_elo(elo, result):
        new_elo = int(elo + 200 * result)
        return new_elo if new_elo > 0 else 0


    def set_difficulty(elo):
        if elo < 1000:
            diff_lvl = 0
        elif 1000 <= elo <= 2000:
            diff_lvl = 1
        elif elo > 2000:
            diff_lvl = 2
        return diff_lvl


    def calc_mis_chance(elo):
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
