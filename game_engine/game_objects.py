import platform
import ctypes  # Is needed to get screen resolution (On Windows)
import subprocess  # Is needed to get screen resolution (On Linux)


class GameObjects:
    """This is one of the main classes where all useful information is stored."""
    if platform.system().lower() != "linux":
        ### For Windows ###
        user32 = ctypes.windll.user32
        SCREENSIZE = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    else:
        ### For Linux ###
        output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
        SCREENSIZE = tuple(map(int, output.split()[0].split(b'x')))

    # Constants
    DEBUG_MODE = False
    BORDER_SIZE = SCREENSIZE[1] // 27
    B_WIDTH = B_HEIGHT = int(SCREENSIZE[1]*0.7) + 4 * BORDER_SIZE
    DIMENSIONS = 8
    SQUARE_SIZE = (B_HEIGHT - 2*BORDER_SIZE) // DIMENSIONS
    BUTTON_SIZE = SQUARE_SIZE * 0.9
    ALPHABET = "ABCDEFGH"
    MAXIMUM_FRAMES_PER_SECOND_VALUE = 60
    TOP_IN_MAIN_MENU = SCREENSIZE[1] // 3
    FONT_SIZE = SCREENSIZE[1] // 18
    FONT_DELTA = int(FONT_SIZE / 3)
    GAP_IN_MAIN_MENU = FONT_SIZE * 2
    LANGUAGES = ["eng", "rus", "ger", "fra"]
    PIECE_THEMES_PACK = ["default", "pixel"]  # You can add piece_custom inside this list.
    BOARD_THEMES_PACK = ["board_classic", "board_b_w", "board_r_w", "board_g_lg", "board_b_r"]  # You can add board_custom inside this list.

    white_board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                   ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                   ["--", "--", "--", "--", "--", "--", "--", "--"],
                   ["--", "--", "--", "--", "--", "--", "--", "--"],
                   ["--", "--", "--", "--", "--", "--", "--", "--"],
                   ["--", "--", "--", "--", "--", "--", "--", "--"],
                   ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                   ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],]

    black_board = [["wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR"],
                   ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                   ["--", "--", "--", "--", "--", "--", "--", "--"],
                   ["--", "--", "--", "--", "--", "--", "--", "--"],
                   ["--", "--", "--", "--", "--", "--", "--", "--"],
                   ["--", "--", "--", "--", "--", "--", "--", "--"],
                   ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                   ["bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR"],]
    
    custom_board_ = [["--", "--", "--", "wK", "wN", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["bR", "--", "--", "bK", "--", "--", "--", "bR"],]

    custom_board = [["--", "--", "--", "--", "--", "--", "bK", "--"],
                    ["--", "--", "--", "--", "--", "--", "wp", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "wp"],
                    ["--", "--", "--", "--", "--", "wB", "wN", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "--", "--", "--", "--", "--", "--", "--"],
                    ["--", "wK", "--", "--", "--", "--", "--", "--"],]

    names_of_pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]

    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}

    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    cols_to_files = {v: k for k, v in files_to_cols.items()}

    KNIGHT_COST_VALUE = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                         [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                         [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                         [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                         [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                         [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                         [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                         [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

    BISHOP_COST_VALUE = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                         [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                         [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                         [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                         [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                         [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                         [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                         [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

    ROOK_COST_VALUE = [[0.25, 0.2, 0.25, 0.25, 0.25, 0.25, 0.2, 0.25],
                       [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
                       [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                       [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                       [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                       [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                       [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                       [0.25, 0.2, 0.25, 0.5, 0.5, 0.25, 0.2, 0.25]]

    QUEEN_COST_VALUE = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                        [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                        [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                        [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                        [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                        [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                        [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                        [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]
    
    KING_COST_VALUE = [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                       [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                       [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                       [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                       [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                       [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                       [0.1, 0.1, 0.1, 0.01, 0.01, 0.1, 0.1, 0.1],
                       [0.1, 0.1, 0.9, 0.1, 0.1, 0.1, 1, 0.1]]

    PAWN_COST_VALUE = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
                       [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                       [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
                       [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
                       [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
                       [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
                       [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
                       [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]
