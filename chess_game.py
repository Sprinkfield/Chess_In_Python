# __name__ = "__main__"
from game_engine import chess_manip
from game_engine import game_objects
from game_engine import draw_game
from game_engine import pieces_moves
from ai_engine import ai_main
import multiprocessing
import pygame
import random


# Global constants
DIMENSIONS = game_objects.GameObjects.DIMENSIONS
TOP_IN_MAIN_MENU = game_objects.GameObjects.TOP_IN_MAIN_MENU
FONT_SIZE = game_objects.GameObjects.FONT_SIZE
GAP_IN_MAIN_MENU = game_objects.GameObjects.GAP_IN_MAIN_MENU
B_WIDTH = B_HEIGHT = game_objects.GameObjects.B_HEIGHT
BORDER_SIZE = game_objects.GameObjects.BORDER_SIZE
SQUARE_SIZE = (B_HEIGHT - 2*BORDER_SIZE) // DIMENSIONS
MAXIMUM_FRAMES_PER_SECOND_VALUE = game_objects.GameObjects.MAXIMUM_FRAMES_PER_SECOND_VALUE
LANGUAGE_NAME = game_objects.GameObjects.LANGUAGES
B_B_WIDTH = game_objects.SCREENSIZE[1] * 2


def run_game():
    multiprocessing.freeze_support()  # If you use pyinstaller to convert .py file to .exe
    pygame.init()
    pygame.font.init()
    pygame_icon = pygame.image.load("images/icon.png")
    pygame.display.set_icon(pygame_icon)
    game_over = False
    game_running_state = True
    game_screen = pygame.display.set_mode((B_WIDTH, B_HEIGHT))
    pygame.display.set_caption("Chess")
    game_timer = pygame.time.Clock()
    move_made = False  # Flag for the completed movement
    side_choice = False
    move_counter = 0
    move_as_black = False
    black_down_flag = False
    lang_num = 0  # English
    language = chess_manip.LangSettings(LANGUAGE_NAME[lang_num % len(LANGUAGE_NAME)])
    difficulty_level = 1

    square_selected = tuple()
    player_clicks = list()
    ai_is_thinking = False
    chosen_button = None

    while side_choice == False:
        for single_event in pygame.event.get():
            if single_event.type == pygame.QUIT:
                side_choice = "white"
                game_running_state = False
            # Mouse movement processing.
            elif single_event.type == pygame.MOUSEBUTTONDOWN:
                    if BORDER_SIZE < location[1] < B_HEIGHT:
                        position_choice = (location[1])  # Y coordinate

                        if TOP_IN_MAIN_MENU <= position_choice <= TOP_IN_MAIN_MENU + FONT_SIZE:
                            side_choice = "white"
                        elif TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU <= position_choice <= TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU + FONT_SIZE:
                            side_choice = "black"
                        elif TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU <= position_choice <= TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU + FONT_SIZE:
                            side_choice = "play_with_a_friend"
                        elif TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU <= position_choice <= TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU + FONT_SIZE:
                            side_choice = "play_with_a_custom_board"
                        
                        if B_WIDTH - SQUARE_SIZE <= location[0] <= B_WIDTH and 0 <= location[1] <= SQUARE_SIZE:
                            lang_num += 1
                            language = chess_manip.LangSettings(LANGUAGE_NAME[lang_num % len(LANGUAGE_NAME)])

                        if 0 <= location[0] <= SQUARE_SIZE and 0 <= location[1] <= SQUARE_SIZE:
                            difficulty_level = (difficulty_level + 1) % 3

        # Main render
        draw_game.DrawGame().draw_main_menu(game_screen, language, difficulty_level)
        game_timer.tick(MAXIMUM_FRAMES_PER_SECOND_VALUE // 2)

        # Highlighting the chosen
        location = pygame.mouse.get_pos()

        if TOP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + FONT_SIZE:
            chosen_button = chess_manip.MainMenuButton(x=B_WIDTH//2 - int(B_B_WIDTH / 2), y=TOP_IN_MAIN_MENU - 2, width=int(B_B_WIDTH))
            draw_game.DrawGame().hightlighting_the_button(game_screen, chosen_button)
        elif TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU + FONT_SIZE:
            chosen_button = chess_manip.MainMenuButton(x=B_WIDTH//2 - int(B_B_WIDTH / 2), y=TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU - 2, width=int(B_B_WIDTH))
            draw_game.DrawGame().hightlighting_the_button(game_screen, chosen_button)
        elif TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU + FONT_SIZE:
            chosen_button = chess_manip.MainMenuButton(x=B_WIDTH//2 - int(B_B_WIDTH / 2), y=TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU - 2, width=int(B_B_WIDTH))
            draw_game.DrawGame().hightlighting_the_button(game_screen, chosen_button)
        elif TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU <= location[1] <= TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU + FONT_SIZE:
            chosen_button = chess_manip.MainMenuButton(x=B_WIDTH//2 - int(B_B_WIDTH / 2), y=TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU - 2, width=int(B_B_WIDTH))
            draw_game.DrawGame().hightlighting_the_button(game_screen, chosen_button)
        else:
            chosen_button = None

        pygame.display.flip()

    # AI settings True == player exists.
    if side_choice == "white": 
        game_manip = chess_manip.GameBoardState(board_type=game_objects.GameObjects.white_board)
        valid_moves = game_manip.get_valid_moves()
        the_first_player = True
        the_second_player = False
        move_as_black = True
    elif side_choice == "black":
        black_down_flag = True
        game_manip = chess_manip.GameBoardState(board_type=game_objects.GameObjects.black_board, black_down=True)
        the_first_player = False
        the_second_player = True
        game_manip.white_king_location, game_manip.black_king_location = game_manip.black_king_location, game_manip.white_king_location
        valid_moves = game_manip.get_valid_moves()
        move_as_black = False
    elif side_choice == "play_with_a_friend":
        game_manip = chess_manip.GameBoardState(board_type=game_objects.GameObjects.white_board)
        valid_moves = game_manip.get_valid_moves()
        the_first_player = True
        the_second_player = True
        move_as_black = False
    else:
        game_manip = chess_manip.GameBoardState(board_type=game_objects.GameObjects.custom_board)
        valid_moves = game_manip.get_valid_moves()
        # Change if its needed
        the_first_player = True
        the_second_player = True
        move_as_black = False

    game_screen.blit(pygame.transform.scale(pygame.image.load("images/zbackground_colour.png"), (B_WIDTH, B_HEIGHT)), (0, 0))

    while game_running_state:
        draw_game.DrawGame().draw_game_manip(game_screen, game_manip, valid_moves, square_selected, is_black_down=black_down_flag)
        game_timer.tick(MAXIMUM_FRAMES_PER_SECOND_VALUE)

        is_now_human_turn = (game_manip.white_to_move and the_first_player) or (not game_manip.white_to_move and the_second_player)

        for single_event in pygame.event.get():
            if single_event.type == pygame.QUIT:
                game_running_state = False  # Exit the game
            # Mouse movement processing.
            elif single_event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and is_now_human_turn:
                    location = pygame.mouse.get_pos()

                    if BORDER_SIZE < location[0] < B_WIDTH - BORDER_SIZE and BORDER_SIZE < location[1] < B_HEIGHT - BORDER_SIZE:
                        colomn = (location[0] - BORDER_SIZE) // SQUARE_SIZE  # X coorditate
                        row = (location[1] - BORDER_SIZE) // SQUARE_SIZE  # Y coordinate

                    if square_selected == (row, colomn):
                        square_selected = tuple()
                        player_clicks = list()
                    else:
                        square_selected = (row, colomn)
                        player_clicks.append(square_selected)

                    if len(player_clicks) == 2:
                        move = pieces_moves.Move(player_clicks[0], player_clicks[1], game_manip.board)

                        for stored_move in valid_moves:
                            if move == stored_move:
                                game_manip.make_move(stored_move)
                                move_made = True
                                square_selected = tuple()
                                player_clicks = list()

                        if not move_made:
                            player_clicks = [square_selected]

        if not is_now_human_turn and move_as_black:
            move = ai_main.AI().opening_move(move_as_black=True, game_manip=game_manip)
            move_as_black = False
            move_made = True
        elif move_counter == 0 and is_now_human_turn is False:
            move = ai_main.AI().opening_move(move_as_black=False, game_manip=game_manip)
            move_made = True
        elif not game_over and not is_now_human_turn:
            if not ai_is_thinking:
                ai_is_thinking = True
                return_queue = multiprocessing.Queue()
                movement_process = multiprocessing.Process(target=ai_main.AI(difficulty_level).find_best_move, args=(move_counter, game_manip, valid_moves, return_queue))
                movement_process.start()

            if not movement_process.is_alive():
                ai_move = return_queue.get()

                if ai_move is None:
                    ai_move = ai_main.AI().find_random_move(valid_moves)

                if random.randint(1, 5 * 2**difficulty_level) != 1:
                    move = ai_move
                else:
                    ai_move = ai_main.AI().find_random_move(valid_moves)
                    move = ai_move
                    print("Oh, I probably made a mistake!")

                game_manip.make_move(ai_move)
                move_made = True
                ai_is_thinking = False

        if move_made:
            draw_game.DrawGame().animate_move(game_manip.move_log[-1], game_screen, game_manip.board, game_timer)
            valid_moves = game_manip.get_valid_moves()
            move_made = False
            move_counter += 1

        if game_manip.checkmate:
            if game_manip.white_to_move:
                game_over = True
                draw_game.DrawGame.draw_end_game_state(text_line=language.b_win, game_screen=game_screen)
            else:
                game_over = True
                draw_game.DrawGame.draw_end_game_state(text_line=language.w_win, game_screen=game_screen)
        elif game_manip.stalemate:
            game_over = True
            draw_game.DrawGame.draw_end_game_state(text_line=language.stale, game_screen=game_screen)

        if move_counter >= 1:
            square = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            square.set_alpha(40)
            square.fill(pygame.Color("blue"))
            game_screen.blit(square, (BORDER_SIZE + move.end_col*SQUARE_SIZE, BORDER_SIZE + move.end_row*SQUARE_SIZE))
            game_screen.blit(square, (BORDER_SIZE + move.start_col*SQUARE_SIZE, BORDER_SIZE + move.start_row*SQUARE_SIZE))

        pygame.display.flip()  # Next frame


if __name__ == "__main__":
    run_game()
