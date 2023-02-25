def get_boards():
    with open("game_engine/boards.txt", "r") as file:
        data = file.read().split()

    white_board = [["0" for _ in range(8)] for _ in range(8)]
    c = 0
    for x in range(8):
        for y in range(8):
            white_board[x][y] = data[c]
            c += 1
    
    black_board = [["0" for _ in range(8)] for _ in range(8)]
    for x in range(8):
        for y in range(8):
            black_board[x][y] = data[c]
            c += 1

    custom_board = [["0" for _ in range(8)] for _ in range(8)]
    for x in range(8):
        for y in range(8):
            custom_board[x][y] = data[c]
            c += 1

    return white_board, black_board, custom_board
