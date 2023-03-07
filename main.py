# __name__ = "__main__"
from game_engine.chess_manip import LangSettings, MainMenuButton, GameBoardState
from game_engine.game_objects import GameObjects
from game_engine.draw_game import DrawGame
from game_engine.pieces_moves import Move
from game_engine.elo_system import Elo
from game_engine.ai_main import AI
import multiprocessing
import pygame
import random
import sys


# Global constants
TOP_IN_MAIN_MENU = GameObjects.TOP_IN_MAIN_MENU
DEBUG_MODE = GameObjects.DEBUG_MODE
FONT_SIZE = GameObjects.FONT_SIZE
FONT_DELTA = GameObjects.FONT_DELTA
GAP_IN_MAIN_MENU = GameObjects.GAP_IN_MAIN_MENU
B_WIDTH = B_HEIGHT = GameObjects.B_HEIGHT
BORDER_SIZE = GameObjects.BORDER_SIZE
SQUARE_SIZE = GameObjects.SQUARE_SIZE
BUTTON_SIZE = GameObjects.BUTTON_SIZE
MAXIMUM_FRAMES_PER_SECOND_VALUE = GameObjects.MAXIMUM_FRAMES_PER_SECOND_VALUE
LANGUAGE_NAME = GameObjects.LANGUAGES
PIECE_THEMES_PACK = GameObjects.PIECE_THEMES_PACK
BOARD_THEMES_PACK = GameObjects.BOARD_THEMES_PACK
B_B_WIDTH = GameObjects.SCREENSIZE[1] * 2
pygame.mixer.init()
CAPTURE_SOUND = pygame.mixer.Sound("sounds/capture.wav")
MOVE_SOUND = pygame.mixer.Sound("sounds/move.wav")


def get_config() -> dict:
    data_dict = dict()
    with open("config.txt", "r") as file:
        data = file.read().split()
        data = [line.split("=") for line in data]

    for key, value in data:
        value = int(value)
        data_dict[key] = value
    return data_dict


def write_config(new_data) -> None:
    data = []
    for key, value in new_data.items():
        data.append(f"{key}={value}")

    with open("config.txt", "w") as file:
        file.write("\n".join(data) + "\n")


def endgame_stuff(language, text, game_screen, surrendered=False) -> None:
    while True:
        for single_event in pygame.event.get():
            if single_event.type == pygame.QUIT:
                sys.exit()
            # Mouse movement processing.
            elif single_event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                sys.exit(run_game())
        
        if surrendered:
            if text == language.w_win:
                text = language.b_sur
            elif text == language.b_win:
                text = language.w_sur

        DrawGame().draw_end_game_state(language, text, game_screen)
        pygame.display.flip()  # Next frame.


def surrender_window(language, game_screen) -> bool:
    menu_open = True
    TEXT_SIZE = GameObjects.SCREENSIZE[1] // 30
    FOREGROUND_FONT_COLOUR = [180, 180, 190]
    BACKGROUND_FONT_COLOUR = [0, 0, 0]
    bg_dimmed = pygame.Surface((B_WIDTH, B_HEIGHT))
    bg_dimmed.set_alpha(200)
    bg_dimmed.fill(pygame.Color(10, 10, 10))
    game_screen.blit(bg_dimmed, (0, 0))
    while menu_open:
        for single_event in pygame.event.get():
            if single_event.type == pygame.QUIT:
                sys.exit()
            # Mouse movement processing.
            elif single_event.type == pygame.KEYDOWN:
                if single_event.key == pygame.K_ESCAPE:
                    menu_open = False
                    return False
            elif single_event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    if int(B_HEIGHT/2 + TEXT_SIZE // 2) < location[1] < int(B_HEIGHT/2 + TEXT_SIZE // 2) + int(TEXT_SIZE // 1.2):
                        menu_open = False
                        return True

        font_type = pygame.font.SysFont("Arial", TEXT_SIZE, True, False)
        text_object = font_type.render(language.surrender, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, int(B_HEIGHT/2.2 - TEXT_SIZE / 1.2), B_WIDTH, B_HEIGHT).move(B_WIDTH/2 - text_object.get_width()/2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.surrender, False, pygame.Color(FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        font_type = pygame.font.SysFont("Arial", int(TEXT_SIZE // 1.2), True, False)
        text_object = font_type.render(language.confirm, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, int(B_HEIGHT/2 + TEXT_SIZE // 2), B_WIDTH, B_HEIGHT).move(B_WIDTH/2 - text_object.get_width()/2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.confirm, False, pygame.Color(FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        location = pygame.mouse.get_pos()
        if int(B_HEIGHT/2 + TEXT_SIZE // 2) < location[1] < int(B_HEIGHT/2 + TEXT_SIZE // 2) + int(TEXT_SIZE / 0.8):
            text_object = font_type.render(language.confirm, False, pygame.Color(tuple(map(lambda x: x + 50, FOREGROUND_FONT_COLOUR))))
            game_screen.blit(text_object, text_location.move(2, 2))

        pygame.display.flip()  # Next frame.


def run_game() -> None:
    multiprocessing.freeze_support()  # If you use pyinstaller to convert .py file to .exe
    pygame.init()
    pygame.font.init()
    game_icon = pygame.image.load("images/icon.png")
    pygame.display.set_icon(game_icon)
    pygame.display.set_caption("Chess")
    game_over = False
    game_running_state = True
    game_screen = pygame.display.set_mode((B_WIDTH, B_HEIGHT))
    game_timer = pygame.time.Clock()
    move_made = False  # Flag for the completed movement.
    gamemode = False
    move_counter = 0
    ai_move_as_black = False
    black_down_flag = False
    in_main_menu = True
    surrendered = False
    surr_continue = False
    not_cap_move = False

    white_board = GameObjects.get_boards()[0]
    black_board = GameObjects.get_boards()[1]
    custom_board = GameObjects.get_boards()[2]

    data_dict = get_config()
    difficulty_level = data_dict["difficulty_level"]
    p_theme_num = data_dict["p_theme_num"]
    b_theme_num = data_dict["b_theme_num"]
    lang_num = data_dict["lang_num"]
    player_elo = data_dict["player_elo"]
    last_p_side = data_dict["last_p_side"]

    language = LangSettings(LANGUAGE_NAME[lang_num % len(LANGUAGE_NAME)])
    square_selected = tuple()
    player_clicks = list()
    ai_is_thinking = False
    chosen_button = None
    selected_button = None

    ### /* MENU (GUI)
    while gamemode == False:
        if in_main_menu:  # Main Menu.
            for single_event in pygame.event.get():
                if single_event.type == pygame.QUIT:
                    gamemode = "white"
                    game_running_state = False
                    in_main_menu = False
                # Mouse movement processing.
                elif single_event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    if BORDER_SIZE < location[1] < B_HEIGHT:
                        if TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU + FONT_SIZE:
                            gamemode = "rating"
                        elif TOP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + FONT_SIZE:
                            gamemode = "white"
                        elif TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU + FONT_SIZE:
                            gamemode = "black"
                        elif TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU + FONT_SIZE:
                            gamemode = "play_with_a_friend"
                        elif TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU + FONT_SIZE:
                            gamemode = "play_with_a_custom_board"
                        
                        if B_WIDTH - SQUARE_SIZE <= location[0] <= B_WIDTH and 0 <= location[1] <= SQUARE_SIZE:
                            lang_num = (lang_num + 1) % len(LANGUAGE_NAME)
                            language = LangSettings(LANGUAGE_NAME[lang_num])

                        if 0 <= location[0] <= SQUARE_SIZE and 0 <= location[1] <= SQUARE_SIZE:
                            in_main_menu = False

            # Main menu render.
            DrawGame().draw_main_menu(game_screen, language, selected_button)
            game_timer.tick(MAXIMUM_FRAMES_PER_SECOND_VALUE)

            # Highlighting the chosen button in main menu.
            location = pygame.mouse.get_pos()

            if TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU + FONT_SIZE:
                selected_button = 0
            elif TOP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + FONT_SIZE:
                selected_button = 1
            elif TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU + FONT_SIZE:
                selected_button = 2
            elif TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU + FONT_SIZE:
                selected_button = 3
            elif TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU + FONT_SIZE:
                selected_button = 4
            elif B_WIDTH - BUTTON_SIZE <= location[0] <= B_B_WIDTH and 0 <= location[1] <= BUTTON_SIZE:
                chosen_button = MainMenuButton(x=B_WIDTH - BUTTON_SIZE, y=0, width=BUTTON_SIZE, height=BUTTON_SIZE, is_text=False)
            elif 0 <= location[0] <= BUTTON_SIZE and 0 <= location[1] <= BUTTON_SIZE:
                selected_button = -1
            else:
                chosen_button = None
                selected_button = None

            DrawGame().hightlighting_the_button(game_screen, chosen_button)
            pygame.display.flip()
        else:  # Settings Menu.
            for single_event in pygame.event.get():
                if single_event.type == pygame.QUIT:
                    gamemode = "white"
                    game_running_state = False
                    in_main_menu = False
                # Mouse movement processing.
                elif single_event.type == pygame.MOUSEBUTTONDOWN:
                        if BORDER_SIZE < location[1] < B_HEIGHT:
                            if TOP_IN_MAIN_MENU - FONT_DELTA <= location[1] <= TOP_IN_MAIN_MENU + FONT_SIZE + FONT_DELTA:
                                difficulty_level = (difficulty_level + 1) % 3
                            elif TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU - FONT_DELTA <= location[1] <= TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU + FONT_SIZE + FONT_DELTA:
                                b_theme_num = (b_theme_num + 1) % len(BOARD_THEMES_PACK)
                            elif TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU - FONT_DELTA <= location[1] <= TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU + FONT_SIZE + FONT_DELTA:
                                p_theme_num = (p_theme_num + 1) % len(PIECE_THEMES_PACK)
                            
                            if B_WIDTH - SQUARE_SIZE <= location[0] <= B_WIDTH and 0 <= location[1] <= SQUARE_SIZE:
                                lang_num += 1
                                language = LangSettings(LANGUAGE_NAME[lang_num % len(LANGUAGE_NAME)])

                            if 0 <= location[0] <= SQUARE_SIZE and 0 <= location[1] <= SQUARE_SIZE:
                                in_main_menu = True

            # Settings menu render.
            DrawGame().draw_settings_menu(game_screen, language, difficulty_level, p_theme_num, b_theme_num, selected_button)
            game_timer.tick(MAXIMUM_FRAMES_PER_SECOND_VALUE)

            # Highlighting the chosen button in settings menu.
            location = pygame.mouse.get_pos()

            if TOP_IN_MAIN_MENU - FONT_DELTA <= location[1] <= TOP_IN_MAIN_MENU + FONT_SIZE + FONT_DELTA:
                selected_button = 0
            elif TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU - FONT_DELTA <= location[1] <= TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU + FONT_SIZE + FONT_DELTA:
                selected_button = 1
            elif TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU - FONT_DELTA <= location[1] <= TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU + FONT_SIZE + FONT_DELTA:
                selected_button = 2
            elif TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU - FONT_DELTA <= location[1] <= TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU + FONT_SIZE + FONT_DELTA:
                chosen_button = MainMenuButton(x=B_WIDTH//2 - int(B_B_WIDTH / 2), y=TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU - 2, width=int(B_B_WIDTH))
            elif B_WIDTH - BUTTON_SIZE <= location[0] <= B_B_WIDTH and 0 <= location[1] <= BUTTON_SIZE:
                chosen_button = MainMenuButton(x=B_WIDTH - BUTTON_SIZE, y=0, width=BUTTON_SIZE, height=BUTTON_SIZE, is_text=False)
            elif 0 <= location[0] <= BUTTON_SIZE and 0 <= location[1] <= BUTTON_SIZE:
                selected_button = -1
            else:
                chosen_button = None
                selected_button = None

            DrawGame().hightlighting_the_button(game_screen, chosen_button)
            pygame.display.flip()
    ### MENU (GUI) */

    new_data = {
        "difficulty_level": difficulty_level,
        "p_theme_num": p_theme_num,
        "b_theme_num": b_theme_num,
        "lang_num": lang_num,
        "player_elo": player_elo,
        "last_p_side": last_p_side,
    }

    write_config(new_data)

    # AI settings True == player exists.
    if gamemode == "rating":
        if last_p_side == 0:
            game_manip = GameBoardState(board_type=white_board, black_down=False)
        else:
            black_down_flag = True
            game_manip = GameBoardState(board_type=black_board, black_down=True)
            game_manip.white_king_location, game_manip.black_king_location = game_manip.black_king_location, game_manip.white_king_location
        valid_moves = game_manip.get_valid_moves()
        the_first_player = True if last_p_side == 0 else False
        the_second_player = False if last_p_side == 0 else True
        ai_move_as_black = True if last_p_side == 0 else False
    elif gamemode == "white":
        game_manip = GameBoardState(board_type=white_board)
        valid_moves = game_manip.get_valid_moves()
        the_first_player = True
        the_second_player = False
        ai_move_as_black = True
    elif gamemode == "black":
        black_down_flag = True
        game_manip = GameBoardState(board_type=black_board, black_down=True)
        the_first_player = False
        the_second_player = True
        game_manip.white_king_location, game_manip.black_king_location = game_manip.black_king_location, game_manip.white_king_location
        valid_moves = game_manip.get_valid_moves()
        ai_move_as_black = False
    elif gamemode == "play_with_a_friend":
        game_manip = GameBoardState(board_type=white_board)
        valid_moves = game_manip.get_valid_moves()
        the_first_player = True
        the_second_player = True
        ai_move_as_black = False
    else:
        game_manip = GameBoardState(board_type=custom_board, black_down=False)
        valid_moves = game_manip.get_valid_moves()
        # Change if its needed.
        the_first_player = True
        the_second_player = True
        ai_move_as_black = False
        move_counter = 100

    confirmed_move = Move((0, 0), (1, 1), game_manip.board)

    while game_running_state:
        DrawGame().draw_game_manip(game_screen, game_manip, valid_moves, square_selected, black_down_flag, p_theme_num, b_theme_num)
        game_timer.tick(MAXIMUM_FRAMES_PER_SECOND_VALUE)

        is_now_human_turn = (game_manip.white_to_move and the_first_player) or (not game_manip.white_to_move and the_second_player)

        for single_event in pygame.event.get():
            if single_event.type == pygame.QUIT:
                game_running_state = False  # Exit the game.
            # Mouse movement processing.
            elif single_event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and is_now_human_turn:
                    location = pygame.mouse.get_pos()

                    if BORDER_SIZE < location[0] < B_WIDTH - BORDER_SIZE and BORDER_SIZE < location[1] < B_HEIGHT - BORDER_SIZE:
                        colomn = (location[0] - BORDER_SIZE) // SQUARE_SIZE  # X coorditate.
                        row = (location[1] - BORDER_SIZE) // SQUARE_SIZE  # Y coordinate.

                        if square_selected == (row, colomn):
                            square_selected = tuple()
                            player_clicks = list()
                        else:
                            square_selected = (row, colomn)
                            player_clicks.append(square_selected)

                        if len(player_clicks) == 2:
                            move = Move(player_clicks[0], player_clicks[1], game_manip.board)

                            for stored_move in valid_moves:
                                if move == stored_move:
                                    not_cap_move = game_manip.board[player_clicks[1][0]][player_clicks[1][1]] != "--"
                                    game_manip.make_move(stored_move, game_screen, language, False)
                                    confirmed_move = move
                                    move_made = True
                                    square_selected = tuple()
                                    player_clicks = list()
                                    if DEBUG_MODE:
                                        print(move_counter)

                            if not move_made:
                                player_clicks = [square_selected]
            elif single_event.type == pygame.KEYDOWN:
                if single_event.key == pygame.K_ESCAPE:
                    if surrender_window(language, game_screen):
                        game_manip.checkmate = True
                        surrendered = True
                        surr_continue = True

        if surr_continue:
            surr_continue = False
            continue

        if not is_now_human_turn and ai_move_as_black and move_counter <= 2:
            move = AI().opening_move(ai_move_as_black=True, game_manip=game_manip)
            ai_move_as_black = False
            move_made = True
            confirmed_move = move
        elif move_counter == 0 and is_now_human_turn is False and move_counter <= 2:
            move = AI().opening_move(ai_move_as_black=False, game_manip=game_manip)
            move_made = True
            confirmed_move = move
        elif not game_over and not is_now_human_turn:
            if not ai_is_thinking:
                ai_is_thinking = True
                return_queue = multiprocessing.Queue()
                movement_process = multiprocessing.Process(target=AI(difficulty_level, black_down_flag).find_best_move, args=(move_counter, game_manip, valid_moves, return_queue))
                movement_process.start()

            if not movement_process.is_alive():
                ai_move = return_queue.get()

                if ai_move is None:
                    ai_move = AI().find_random_move(valid_moves)

                if DEBUG_MODE or ((random.randint(1, Elo.calc_mis_chance(player_elo)) != 1) if gamemode == "rating" \
                                   else (random.randint(1, 5 * 2**difficulty_level) != 1)):
                    move = ai_move
                else:
                    ai_move = AI().find_random_move(valid_moves)
                    move = ai_move
                    print("Oh, I probably made a mistake!")
                game_manip.make_move(ai_move,  game_screen, language, True)
                move_made = True
                ai_is_thinking = False
                confirmed_move = ai_move

        if move_made:
            DrawGame().animate_move(game_manip.move_log[-1], game_screen, game_manip.board, game_timer, p_theme_num, b_theme_num)
            valid_moves = game_manip.get_valid_moves()
            move_made = False
            move_counter += 1
            if not_cap_move:
                CAPTURE_SOUND.play()
            else:
                MOVE_SOUND.play()

        if game_manip.checkmate or Elo.score_board(game_manip, 0) < 100 or Elo.score_board(game_manip, 1) < 100:
            game_over = True
            if Elo.score_board(game_manip, 0) < 100:
                game_manip.white_to_move = True
            elif Elo.score_board(game_manip, 1) < 100:
                game_manip.white_to_move = False
            
            if game_manip.white_to_move:
                if gamemode == "rating":
                    if the_first_player:
                        result = -1
                    else:
                        result = 1
                    player_elo = Elo.calculate_elo(game_manip, player_elo, result, last_p_side, move_counter)
                    last_p_side = (last_p_side + 1) % 2
                    new_data = {
                        "difficulty_level": difficulty_level,
                        "p_theme_num": p_theme_num,
                        "b_theme_num": b_theme_num,
                        "lang_num": lang_num,
                        "player_elo": player_elo,
                        "last_p_side": last_p_side,
                    }
                    write_config(new_data)
                endgame_stuff(language, language.b_win, game_screen, surrendered)
            else:
                if gamemode == "rating":
                    if the_first_player:
                        result = 1
                    else:
                        result = -1
                    player_elo = Elo.calculate_elo(game_manip, player_elo, result, last_p_side, move_counter)
                    last_p_side = (last_p_side + 1) % 2
                    new_data = {
                        "difficulty_level": difficulty_level,
                        "p_theme_num": p_theme_num,
                        "b_theme_num": b_theme_num,
                        "lang_num": lang_num,
                        "player_elo": player_elo,
                        "last_p_side": last_p_side,
                    }
                    write_config(new_data)
                endgame_stuff(language, language.w_win, game_screen, surrendered)
        elif game_manip.stalemate or ((Elo.score_board(game_manip, 0) <= 103 and Elo.score_board(game_manip, 1) <= 103)):
            game_over = True
            if gamemode == "rating":
                player_elo = Elo.calculate_elo(game_manip, player_elo, 0, last_p_side, move_counter)
                last_p_side = (last_p_side + 1) % 2
                new_data = {
                    "difficulty_level": difficulty_level,
                    "p_theme_num": p_theme_num,
                    "b_theme_num": b_theme_num,
                    "lang_num": lang_num,
                    "player_elo": player_elo,
                    "last_p_side": last_p_side,
                }
                write_config(new_data)
            endgame_stuff(language, language.stale, game_screen)

        if move_counter >= 1 and (gamemode != "play_with_a_custom_board" or move_counter > 100):
            square = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            square.set_alpha(50)
            square.fill(pygame.Color("blue"))
            game_screen.blit(square, (BORDER_SIZE + confirmed_move.end_col*SQUARE_SIZE, BORDER_SIZE + confirmed_move.end_row*SQUARE_SIZE))
            game_screen.blit(square, (BORDER_SIZE + confirmed_move.start_col*SQUARE_SIZE, BORDER_SIZE + confirmed_move.start_row*SQUARE_SIZE))

        pygame.display.flip()  # Next frame.


if __name__ == "__main__":
    run_game()
