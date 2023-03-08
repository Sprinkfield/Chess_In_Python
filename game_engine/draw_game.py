from game_engine.game_objects import GameObjects
import pygame
import sys


# Global constants
B_WIDTH = B_HEIGHT = GameObjects.B_HEIGHT
DIMENSIONS = GameObjects.DIMENSIONS
BORDER_SIZE = GameObjects.BORDER_SIZE
LETTER_BORDER_SIZE = int(GameObjects.SCREENSIZE[1] / 36)
SQUARE_SIZE = GameObjects.SQUARE_SIZE
BUTTON_SIZE = GameObjects.BUTTON_SIZE
MAXIMUM_FPS = GameObjects.MAXIMUM_FRAMES_PER_SECOND_VALUE
IMAGES = dict()
SQUARE_IMAGES = dict()
TOP_IN_MAIN_MENU = GameObjects.TOP_IN_MAIN_MENU
FONT_SIZE = GameObjects.FONT_SIZE
GAP_IN_MAIN_MENU = GameObjects.GAP_IN_MAIN_MENU
SQUARE_TRANSPARENCY_VALUE = 120
BUTTON_TRANSPARENCY_VALUE = 100
BLACK_SQUAERS_COLOUR = "dark cyan"
ALPHABET = GameObjects.ALPHABET
BOLD_TEXT_SETTINGS = True
ANIMATION_SPEED = 1
FOREGROUND_FONT_COLOUR = [180, 180, 190]
BACKGROUND_FONT_COLOUR = [0, 0, 0]
LANGUAGES = GameObjects.LANGUAGES
MAIN_MENU_BACKGROUND = pygame.image.load("images/main_menu_background.png")
PIECE_THEMES_PACK = GameObjects.PIECE_THEMES_PACK
BOARD_THEMES_PACK = GameObjects.BOARD_THEMES_PACK


class DrawGame:
    """Class that draws GUI: main menu, game board, pieces, move animation, highlights of moves, etc."""
    def load_images(self, p_theme_num, b_theme_num) -> None:
        for piece in GameObjects.names_of_pieces:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"images/{PIECE_THEMES_PACK[p_theme_num]}/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE))
        
        IMAGES["white_square"] = pygame.transform.scale(pygame.image.load(f"images/{BOARD_THEMES_PACK[b_theme_num]}/zwhite_square.png"), (SQUARE_SIZE, SQUARE_SIZE))
        IMAGES["black_square"] = pygame.transform.scale(pygame.image.load(f"images/{BOARD_THEMES_PACK[b_theme_num]}/zblack_square.png"), (SQUARE_SIZE, SQUARE_SIZE))

    def dim_bg(self, game_screen, alpha=75):
        bg_dimmed = pygame.Surface((B_WIDTH, B_HEIGHT))
        bg_dimmed.set_alpha(alpha)
        bg_dimmed.fill(pygame.Color(10, 10, 10))
        game_screen.blit(bg_dimmed, (0, 0))

    def draw_main_menu(self, game_screen, language, selected_button) -> None:
        game_screen.blit(pygame.transform.scale(MAIN_MENU_BACKGROUND, (B_WIDTH, B_HEIGHT)), (0, 0))
        self.dim_bg(game_screen)

        font_type = pygame.font.SysFont("Arial", FONT_SIZE, True, False)
        font_type_main = pygame.font.SysFont("Arial", FONT_SIZE * 2, True, False)

        text_object = font_type_main.render(language.main, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, 80, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type_main.render(language.main, False, pygame.Color(FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        text_object = font_type.render(language.rating, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU - GAP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.rating, False, pygame.Color(list(map(lambda x: x + 65, FOREGROUND_FONT_COLOUR)) if selected_button == 0 else FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        text_object = font_type.render(language.p_white, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.p_white, False, pygame.Color(list(map(lambda x: x + 65, FOREGROUND_FONT_COLOUR)) if selected_button == 1 else FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        text_object = font_type.render(language.p_black, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.p_black, False, pygame.Color(list(map(lambda x: x + 65, FOREGROUND_FONT_COLOUR)) if selected_button == 2 else FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        text_object = font_type.render(language.p_vs_f, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.p_vs_f, False, pygame.Color(list(map(lambda x: x + 65, FOREGROUND_FONT_COLOUR)) if selected_button == 3 else FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        text_object = font_type.render(language.custom_b, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.custom_b, False, pygame.Color(list(map(lambda x: x + 65, FOREGROUND_FONT_COLOUR)) if selected_button == 4 else FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        if selected_button != -1:
            settings_image = pygame.transform.scale(pygame.image.load("images/settings_button.png"), (BUTTON_SIZE, BUTTON_SIZE))
        else:
            settings_image = pygame.transform.scale(pygame.image.load("images/settings_button_light.png"), (BUTTON_SIZE, BUTTON_SIZE))
        lang_image = pygame.transform.scale(pygame.image.load(f"images/flag_{language.lang_name}.png"), (BUTTON_SIZE, BUTTON_SIZE))
        game_screen.blit(lang_image, pygame.Rect(B_WIDTH - BUTTON_SIZE, 0, BUTTON_SIZE, BUTTON_SIZE))
        game_screen.blit(settings_image, pygame.Rect(0, 0, BUTTON_SIZE, BUTTON_SIZE))

    def draw_settings_menu(self, game_screen, language, level, p_theme_num, b_theme_num, selected_button) -> None:
        game_screen.blit(pygame.transform.scale(MAIN_MENU_BACKGROUND, (B_WIDTH, B_HEIGHT)), (0, 0))
        self.dim_bg(game_screen)
        dy = 2.6

        font_type = pygame.font.SysFont("Arial", FONT_SIZE, True, False)
        font_type_main = pygame.font.SysFont("Arial", FONT_SIZE * 2, True, False)

        text_object = font_type_main.render(language.settings, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, 80, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type_main.render(language.settings, False, pygame.Color(FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        # Difficulty settings.
        text_object = font_type.render(language.difficulty, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 1.8, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.difficulty, False, pygame.Color(list(map(lambda x: x + 65, FOREGROUND_FONT_COLOUR)) if selected_button == 0 else FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        diff_but_location = pygame.Rect(0, TOP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 + text_object.get_width() / 2.2, - FONT_SIZE / dy)

        lvl_easy = pygame.transform.scale(pygame.image.load(f"images/{PIECE_THEMES_PACK[p_theme_num]}/wp.png"), (SQUARE_SIZE, SQUARE_SIZE))
        lvl_medium = pygame.transform.scale(pygame.image.load(f"images/{PIECE_THEMES_PACK[p_theme_num]}/wN.png"), (SQUARE_SIZE, SQUARE_SIZE))
        lvl_hard = pygame.transform.scale(pygame.image.load(f"images/{PIECE_THEMES_PACK[p_theme_num]}/wQ.png"), (SQUARE_SIZE, SQUARE_SIZE))

        if level == 0:
            game_screen.blit(lvl_easy, diff_but_location)
        elif level == 1:
            game_screen.blit(lvl_medium, diff_but_location)
        elif level == 2:
            game_screen.blit(lvl_hard, diff_but_location)

        # Board type settings.
        text_object = font_type.render(language.board_theme, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 1.8, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.board_theme, False, pygame.Color(list(map(lambda x: x + 65, FOREGROUND_FONT_COLOUR)) if selected_button == 1 else FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        diff_but_location = pygame.Rect(0, TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 + text_object.get_width() / 2.2, - FONT_SIZE / dy)
        king_image = pygame.transform.scale(pygame.image.load(f"images/{BOARD_THEMES_PACK[b_theme_num]}/theme_img.png"), (SQUARE_SIZE, SQUARE_SIZE))
        game_screen.blit(king_image, diff_but_location)

        # Piece type settings.
        text_object = font_type.render(language.piece_set, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 1.8, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.piece_set, False, pygame.Color(list(map(lambda x: x + 65, FOREGROUND_FONT_COLOUR)) if selected_button == 2 else FOREGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        diff_but_location = pygame.Rect(0, TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 + text_object.get_width() / 2.2, - FONT_SIZE / dy)
        king_image = pygame.transform.scale(pygame.image.load(f"images/{PIECE_THEMES_PACK[p_theme_num]}/wK.png"), (SQUARE_SIZE, SQUARE_SIZE))
        game_screen.blit(king_image, diff_but_location)

        # Language mode settings.
        if selected_button != -1:
            main_menu_image = pygame.transform.scale(pygame.image.load("images/main_menu_button.png"), (BUTTON_SIZE, BUTTON_SIZE))
        else:
            main_menu_image = pygame.transform.scale(pygame.image.load("images/main_menu_button_light.png"), (BUTTON_SIZE, BUTTON_SIZE))
        lang_image = pygame.transform.scale(pygame.image.load(f"images/flag_{language.lang_name}.png"), (BUTTON_SIZE, BUTTON_SIZE))
        game_screen.blit(lang_image, pygame.Rect(B_WIDTH - BUTTON_SIZE, 0, BUTTON_SIZE, BUTTON_SIZE))
        game_screen.blit(main_menu_image, pygame.Rect(0, 0, BUTTON_SIZE, BUTTON_SIZE))

    def promote_choice(self, screen, language, colour) -> str:
        while True:
            for single_event in pygame.event.get():
                if single_event.type == pygame.QUIT:
                    sys.exit()
                # Mouse movement processing.
                elif single_event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    if int(B_HEIGHT / 2) - int(SQUARE_SIZE * 0.33) <= location[1] <= int(B_HEIGHT / 2) - int(SQUARE_SIZE * 0.33) + SQUARE_SIZE:
                        if int(B_WIDTH/2) - SQUARE_SIZE*2 - int(BORDER_SIZE/20) <= location[0] <= int(B_WIDTH/2) - SQUARE_SIZE*2 - int(BORDER_SIZE/20) + SQUARE_SIZE:
                            return"Q"
                        elif int(B_WIDTH/2) - SQUARE_SIZE - int(BORDER_SIZE/20) <= location[0] <= int(B_WIDTH/2) - SQUARE_SIZE - int(BORDER_SIZE/20) + SQUARE_SIZE:
                            return"R"
                        elif int(B_WIDTH/2) - int(BORDER_SIZE/20) <= location[0] <= int(B_WIDTH/2) - int(BORDER_SIZE/20) + SQUARE_SIZE:
                            return "B"
                        elif int(B_WIDTH/2) + SQUARE_SIZE - int(BORDER_SIZE/20) <= location[0] <= int(B_WIDTH/2) + SQUARE_SIZE - int(BORDER_SIZE/20) + SQUARE_SIZE:
                            return "N"

            DrawGame().promotion_gui(screen, language, colour)
            pygame.display.flip()  # Next frame.

    def promotion_gui(self, screen, language, colour) -> None:
        choice_bg = pygame.Surface((SQUARE_SIZE * 4, int(SQUARE_SIZE * 1.5)))
        choice_bg.fill(pygame.Color(50, 50, 50))
        screen.blit(choice_bg, (int(B_WIDTH/2) - SQUARE_SIZE*2 - int(BORDER_SIZE/20), B_HEIGHT//2 - int(SQUARE_SIZE * 0.75)))

        font_type = pygame.font.SysFont("Arial", int(SQUARE_SIZE * 0.25), True, False)
        text_object = font_type.render(language.promotion, False, pygame.Color(255, 255, 255))
        text_location = pygame.Rect(0, B_HEIGHT//2 - int(SQUARE_SIZE * 0.75), \
                                    B_WIDTH, B_HEIGHT).move(B_WIDTH/2 - text_object.get_width()/2, 0)
        screen.blit(text_object, text_location)

        screen.blit(IMAGES[f"{colour}Q"], pygame.Rect(int(B_WIDTH/2) - SQUARE_SIZE*2 - int(BORDER_SIZE/20), int(B_HEIGHT / 2) - int(SQUARE_SIZE * 0.33), SQUARE_SIZE, SQUARE_SIZE))
        screen.blit(IMAGES[f"{colour}R"], pygame.Rect(int(B_WIDTH/2) - SQUARE_SIZE - int(BORDER_SIZE/20), int(B_HEIGHT / 2) - int(SQUARE_SIZE * 0.33), SQUARE_SIZE, SQUARE_SIZE))
        screen.blit(IMAGES[f"{colour}B"], pygame.Rect(int(B_WIDTH/2) - int(BORDER_SIZE/20), int(B_HEIGHT / 2) - int(SQUARE_SIZE * 0.33), SQUARE_SIZE, SQUARE_SIZE))
        screen.blit(IMAGES[f"{colour}N"], pygame.Rect(int(B_WIDTH/2) + SQUARE_SIZE - int(BORDER_SIZE/20), int(B_HEIGHT / 2) - int(SQUARE_SIZE * 0.33), SQUARE_SIZE, SQUARE_SIZE))

    def hightlighting_possible_moves(self, screen, gs, valid_moves, square_selected) -> None:
        if square_selected != ():
            row, col = square_selected
            chosen_piece = gs.board[row][col][0]

            if gs.white_to_move:
                side_colour = "w"
            else:
                side_colour = "b"

            if chosen_piece == side_colour:
                square = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                square.set_alpha(SQUARE_TRANSPARENCY_VALUE)
                square.fill(pygame.Color("green"))
                screen.blit(square, (BORDER_SIZE + col*SQUARE_SIZE, BORDER_SIZE + row*SQUARE_SIZE))
                square.fill(pygame.Color("blue"))

                for move in valid_moves:
                    if move.start_row == row and move.start_col == col:
                        screen.blit(square, (BORDER_SIZE + SQUARE_SIZE * move.end_col, BORDER_SIZE + SQUARE_SIZE * move.end_row))

    def hightlighting_the_button(self, screen, chosen_button) -> None:
        if chosen_button:
            button = pygame.Surface((chosen_button.width, chosen_button.height))
            button.set_alpha(BUTTON_TRANSPARENCY_VALUE)
            button.fill(pygame.Color(100, 100, 100))
            screen.blit(button, (chosen_button.x, chosen_button.y))

    def highlight_move_made(self, game_screen, move) -> None:
        square = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        square.set_alpha(50)
        square.fill(pygame.Color("yellow"))
        game_screen.blit(square, (BORDER_SIZE + move.end_col*SQUARE_SIZE, BORDER_SIZE + move.end_row*SQUARE_SIZE))
        game_screen.blit(square, (BORDER_SIZE + move.start_col*SQUARE_SIZE, BORDER_SIZE + move.start_row*SQUARE_SIZE))

    def draw_game_manip(self, game_screen, game_manip, valid_moves, square_selected, is_black_down=False, p_theme_num=0, b_theme_num=0) -> None:
        game_screen.blit(pygame.transform.scale(pygame.image.load(f"images/{BOARD_THEMES_PACK[b_theme_num]}/zbackground_colour.png"), (B_WIDTH, B_HEIGHT)), (0, 0))
        self.draw_game(game_screen, p_theme_num, b_theme_num)
        self.hightlighting_possible_moves(game_screen, game_manip, valid_moves, square_selected)
        self.draw_pieces(game_screen, game_manip.board, p_theme_num, b_theme_num)

        # Drawing letters and numbers.
        if is_black_down:
            for i in range(DIMENSIONS, 0, -1):
                my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
                text_surface = my_font.render(str(abs(i)), BOLD_TEXT_SETTINGS, "white")
                game_screen.blit(text_surface, (BORDER_SIZE//3.6, SQUARE_SIZE * (i) - SQUARE_SIZE//4.5))

            for i in range(DIMENSIONS, 0, -1):
                my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
                text_surface = my_font.render(str(abs(i)), BOLD_TEXT_SETTINGS, "white")
                game_screen.blit(text_surface, (B_WIDTH - BORDER_SIZE//1.333, SQUARE_SIZE * (i) - SQUARE_SIZE//4.5))

            for i in range(DIMENSIONS - 1, -1, -1):
                my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
                text_surface = my_font.render(ALPHABET[-(i+1)], BOLD_TEXT_SETTINGS, "white")
                game_screen.blit(text_surface, (SQUARE_SIZE * (i+1) - SQUARE_SIZE//4.5, B_HEIGHT - BORDER_SIZE//1.05))

            for i in range(DIMENSIONS - 1, -1, -1):
                my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
                text_surface = my_font.render(ALPHABET[-(i+1)], BOLD_TEXT_SETTINGS, "white")
                game_screen.blit(text_surface, (SQUARE_SIZE * (i+1) - SQUARE_SIZE//4.5, BORDER_SIZE//6))
        else:
            for i in range(DIMENSIONS, 0, -1):
                my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
                text_surface = my_font.render(str(abs(i-9)), BOLD_TEXT_SETTINGS, "white")
                game_screen.blit(text_surface, (BORDER_SIZE//3.6, SQUARE_SIZE * (i) - SQUARE_SIZE//4.5))

            for i in range(DIMENSIONS, 0, -1):
                my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
                text_surface = my_font.render(str(abs(i-9)), BOLD_TEXT_SETTINGS, "white")
                game_screen.blit(text_surface, (B_WIDTH - BORDER_SIZE//1.333, SQUARE_SIZE * (i) - SQUARE_SIZE//4.5))
            
            for i in range(DIMENSIONS - 1, -1, -1):
                my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
                text_surface = my_font.render(ALPHABET[i], BOLD_TEXT_SETTINGS, "white")
                game_screen.blit(text_surface, (SQUARE_SIZE * (i+1) - SQUARE_SIZE//4.5, B_HEIGHT - BORDER_SIZE//1.05))

            for i in range(DIMENSIONS - 1, -1, -1):
                my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
                text_surface = my_font.render(ALPHABET[i], BOLD_TEXT_SETTINGS, "white")
                game_screen.blit(text_surface, (SQUARE_SIZE * (i+1) - SQUARE_SIZE//4.5, BORDER_SIZE//6))

    def draw_game(self, screen, p_theme_num, b_theme_num) -> None:
        self.load_images(p_theme_num, b_theme_num)
        white_colour = False

        for row in range(DIMENSIONS):
            white_colour = not white_colour
            for col in range(DIMENSIONS):
                if white_colour:
                    screen.blit(IMAGES["white_square"], pygame.Rect(BORDER_SIZE + col*SQUARE_SIZE, BORDER_SIZE + row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    screen.blit(IMAGES["black_square"], pygame.Rect(BORDER_SIZE + col*SQUARE_SIZE, BORDER_SIZE + row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                white_colour = not white_colour

    def draw_end_game_state(self, language, text_line, game_screen) -> None:
        endgame_text_size = int(GameObjects.SCREENSIZE[1] / 22)

        if language.lang_name in ["ger", "fra"]:
            endgame_text_size = int(endgame_text_size / 1.4)

        font_type = pygame.font.SysFont("Arial", endgame_text_size, True, False)
        text_object = font_type.render(text_line, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, int(B_HEIGHT/2 - endgame_text_size / 1.2), B_WIDTH, B_HEIGHT).move(B_WIDTH/2 - text_object.get_width()/2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(text_line, False, pygame.Color(tuple(map(lambda x: x + 50, FOREGROUND_FONT_COLOUR))))
        game_screen.blit(text_object, text_location.move(2, 2))

        font_type = pygame.font.SysFont("Arial", endgame_text_size // 2, True, False)
        text_object = font_type.render(language.click, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, int(B_HEIGHT/2 + endgame_text_size // 2), B_WIDTH, B_HEIGHT).move(B_WIDTH/2 - text_object.get_width()/2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.click, False, pygame.Color(tuple(map(lambda x: x + 50, FOREGROUND_FONT_COLOUR))))
        game_screen.blit(text_object, text_location.move(2, 2))

    def draw_pieces(self, game_screen, board, p_theme_num, b_theme_num) -> None:
        self.load_images(p_theme_num, b_theme_num)

        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
                piece = board[row][col]
                if piece != "--":
                    game_screen.blit(IMAGES[piece], pygame.Rect(BORDER_SIZE + col*SQUARE_SIZE, BORDER_SIZE + row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def animate_move(self, move, screen, board, clock, p_theme_num, b_theme_num) -> None:
        move_row = move.end_row - move.start_row
        move_col = move.end_col - move.start_col
        frame_count = (abs(move_row) + abs(move_col)) * ANIMATION_SPEED
        square_colour = ["white_square", "black_square"][(move.end_row + move.end_col) % 2]

        for frame in range(frame_count + 1):
            self.draw_game(screen, p_theme_num, b_theme_num)
            self.draw_pieces(screen, board, p_theme_num, b_theme_num)
            row, col = (move.start_row + move_row * frame / frame_count, move.start_col + move_col * frame / frame_count)
            end_square = pygame.Rect(BORDER_SIZE + move.end_col * SQUARE_SIZE, BORDER_SIZE + move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[square_colour], pygame.Rect(BORDER_SIZE + move.end_col*SQUARE_SIZE, BORDER_SIZE + move.end_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            if move.piece_captured != "--":
                if move.is_enpassant_move:
                    enpassant_row = move.end_row + 1 if move.piece_captured[0] == "b" else move.end_row - 1
                    end_square = pygame.Rect(BORDER_SIZE + move.end_col * SQUARE_SIZE, BORDER_SIZE + enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                screen.blit(IMAGES[move.piece_captured], end_square)

            screen.blit(IMAGES[move.piece_moved], pygame.Rect(BORDER_SIZE + col * SQUARE_SIZE, BORDER_SIZE + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            clock.tick(MAXIMUM_FPS)
            pygame.display.flip()
