from game_engine import game_objects
import pygame


# Global constants
B_WIDTH = B_HEIGHT = game_objects.GameObjects.B_HEIGHT
BORDER_SIZE = game_objects.GameObjects.BORDER_SIZE
LETTER_BORDER_SIZE = int(game_objects.SCREENSIZE[1] // 36)
LETTER_GAP_SIZE = int(game_objects.SCREENSIZE[1] // 43.2)
DIMENSIONS = 8
SQUARE_SIZE = (B_HEIGHT - 2*BORDER_SIZE) // DIMENSIONS
MAXIMUM_FPS = 60
IMAGES = dict()
SQUARE_IMAGES = dict()
TOP_IN_MAIN_MENU = game_objects.GameObjects.TOP_IN_MAIN_MENU
FONT_SIZE = game_objects.GameObjects.FONT_SIZE
GAP_IN_MAIN_MENU = game_objects.GameObjects.GAP_IN_MAIN_MENU
SQUARE_TRANSPARENCY_VALUE = 120
BUTTON_TRANSPARENCY_VALUE = 100
BLACK_SQUAERS_COLOUR = "dark cyan"
ALPHABET = game_objects.GameObjects.ALPHABET
BOLD_TEXT_SETTINGS = True
ANIMATION_SPEED = 1
ENDGAME_TEXT_SIZE = int(game_objects.SCREENSIZE[1] // 22)
BACKGROUND_FONT_COLOUR = (200, 220, 250)
FOREGROUND_FONT_COLOUR = (0, 0, 0)
LANGUAGES = game_objects.GameObjects.LANGUAGES


class DrawGame:
    """Class that draws GUI: main menu, game board, pieces, move animation, highlights of moves, etc."""
    def load_images(self) -> None:
        for piece in game_objects.GameObjects.names_of_pieces:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE))
        
        IMAGES["white_square"] = pygame.transform.scale(pygame.image.load("images/zwhite_square.png"), (SQUARE_SIZE, SQUARE_SIZE))
        IMAGES["black_square"] = pygame.transform.scale(pygame.image.load("images/zblack_square.png"), (SQUARE_SIZE, SQUARE_SIZE))

    def draw_main_menu(self, game_screen, language):
        game_screen.blit(pygame.transform.scale(pygame.image.load("images/zmain_menu_background.png"), (B_WIDTH, B_HEIGHT)), (0, 0))

        font_type = pygame.font.SysFont("Arial", FONT_SIZE, True, False)
        font_type_main = pygame.font.SysFont("Arial", FONT_SIZE * 2, True, False)

        text_object = font_type_main.render(language.main, False, pygame.Color(FOREGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, 80, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type_main.render(language.main, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        text_object = font_type.render(language.p_white, False, pygame.Color(FOREGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.p_white, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        text_object = font_type.render(language.p_black, False, pygame.Color(FOREGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU + GAP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.p_black, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        text_object = font_type.render(language.p_vs_f, False, pygame.Color(FOREGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU + 2*GAP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.p_vs_f, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        text_object = font_type.render(language.custom_b, False, pygame.Color(FOREGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, TOP_IN_MAIN_MENU + 3*GAP_IN_MAIN_MENU, B_WIDTH, 100).move(B_WIDTH / 2 - text_object.get_width() / 2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(language.custom_b, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

        lang_image = pygame.transform.scale(pygame.image.load(f"images/flag_{language.lang_name}.png"), (SQUARE_SIZE, SQUARE_SIZE))
        game_screen.blit(lang_image, pygame.Rect(B_WIDTH - SQUARE_SIZE, 0, SQUARE_SIZE, SQUARE_SIZE))

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
        if chosen_button is not None:
            button = pygame.Surface((chosen_button.width, FONT_SIZE + 5))
            button.set_alpha(BUTTON_TRANSPARENCY_VALUE)
            button.fill(pygame.Color(100, 100, 100))
            screen.blit(button, (chosen_button.x, chosen_button.y))

    def highlight_move_made(self, game_screen, move):
        square = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        square.set_alpha(50)
        square.fill(pygame.Color("yellow"))
        game_screen.blit(square, (BORDER_SIZE + move.end_col*SQUARE_SIZE, BORDER_SIZE + move.end_row*SQUARE_SIZE))
        game_screen.blit(square, (BORDER_SIZE + move.start_col*SQUARE_SIZE, BORDER_SIZE + move.start_row*SQUARE_SIZE))

    def draw_game_manip(self, game_screen, game_manip, valid_moves, square_selected, is_black_down=False) -> None:
        self.draw_game(game_screen)
        self.hightlighting_possible_moves(game_screen, game_manip, valid_moves, square_selected)
        self.draw_pieces(game_screen, game_manip.board)

        # Drawing letters and numbers.
        if is_black_down:
            for i in range(DIMENSIONS, 0, -1):
                my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
                text_surface = my_font.render(str(abs(i)), BOLD_TEXT_SETTINGS, "white")
                game_screen.blit(text_surface, (BORDER_SIZE//4, SQUARE_SIZE * (i) - LETTER_GAP_SIZE))

            for i in range(DIMENSIONS, 0, -1):
                my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
                text_surface = my_font.render(str(abs(i)), BOLD_TEXT_SETTINGS, "white")
                game_screen.blit(text_surface, (B_WIDTH - BORDER_SIZE//1.4, SQUARE_SIZE * (i) - LETTER_GAP_SIZE))
        else:
            for i in range(DIMENSIONS, 0, -1):
                my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
                text_surface = my_font.render(str(abs(i-9)), BOLD_TEXT_SETTINGS, "white")
                game_screen.blit(text_surface, (BORDER_SIZE//4, SQUARE_SIZE * (i) - LETTER_GAP_SIZE))

            for i in range(DIMENSIONS, 0, -1):
                my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
                text_surface = my_font.render(str(abs(i-9)), BOLD_TEXT_SETTINGS, "white")
                game_screen.blit(text_surface, (B_WIDTH - BORDER_SIZE//1.4, SQUARE_SIZE * (i) - LETTER_GAP_SIZE))
            
        for i in range(DIMENSIONS - 1, -1, -1):
            my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
            text_surface = my_font.render(ALPHABET[i], BOLD_TEXT_SETTINGS, "white")
            game_screen.blit(text_surface, (SQUARE_SIZE * (i+1) - LETTER_GAP_SIZE, B_HEIGHT - BORDER_SIZE//1.05))

        for i in range(DIMENSIONS - 1, -1, -1):
            my_font = pygame.font.SysFont('Arial', LETTER_BORDER_SIZE)
            text_surface = my_font.render(ALPHABET[i], BOLD_TEXT_SETTINGS, "white")
            game_screen.blit(text_surface, (SQUARE_SIZE * (i+1) - LETTER_GAP_SIZE, BORDER_SIZE//6))

    def draw_game(self, screen) -> None:
        self.load_images()
        white_colour = False

        for row in range(DIMENSIONS):
            white_colour = not white_colour
            for col in range(DIMENSIONS):
                if white_colour:
                    screen.blit(IMAGES["white_square"], pygame.Rect(BORDER_SIZE + col*SQUARE_SIZE, BORDER_SIZE + row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                else:
                    screen.blit(IMAGES["black_square"], pygame.Rect(BORDER_SIZE + col*SQUARE_SIZE, BORDER_SIZE + row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                white_colour = not white_colour

    def draw_end_game_state(text_line, game_screen) -> None:
        font_type = pygame.font.SysFont("Arial", ENDGAME_TEXT_SIZE, True, False)
        text_object = font_type.render(text_line, False, pygame.Color(FOREGROUND_FONT_COLOUR))
        text_location = pygame.Rect(0, B_HEIGHT/2 - 38, B_WIDTH, B_HEIGHT).move(B_WIDTH/2 - text_object.get_width()/2, 0)
        game_screen.blit(text_object, text_location)
        text_object = font_type.render(text_line, False, pygame.Color(BACKGROUND_FONT_COLOUR))
        game_screen.blit(text_object, text_location.move(2, 2))

    def draw_pieces(self, game_screen, board) -> None:
        self.load_images()

        for row in range(DIMENSIONS):
            for col in range(DIMENSIONS):
                piece = board[row][col]
                if piece != "--":
                    game_screen.blit(IMAGES[piece], pygame.Rect(BORDER_SIZE + col*SQUARE_SIZE, BORDER_SIZE + row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def animate_move(self, move, screen, board, clock) -> None:
        move_row = move.end_row - move.start_row
        move_col = move.end_col - move.start_col
        frames_per_second = ANIMATION_SPEED
        frame_count = (abs(move_row) + abs(move_col)) * frames_per_second
        square_colour = ["white_square", "black_square"][(move.end_row + move.end_col) % 2]

        for frame in range(frame_count + 1):
            self.draw_game(screen)
            self.draw_pieces(screen, board)
            row, col = (move.start_row + move_row * frame / frame_count, move.start_col + move_col * frame / frame_count)
            end_square = pygame.Rect(BORDER_SIZE + move.end_col * SQUARE_SIZE, BORDER_SIZE + move.end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            screen.blit(IMAGES[square_colour], pygame.Rect(BORDER_SIZE + move.end_col*SQUARE_SIZE, BORDER_SIZE + move.end_row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            if move.piece_captured != "--":
                if move.is_enpassant_move:
                    enpassant_row = move.end_row + 1 if move.piece_captured[0] == "b" else move.end_row - 1
                    end_square = pygame.Rect(BORDER_SIZE + move.end_col * SQUARE_SIZE, BORDER_SIZE + enpassant_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                screen.blit(IMAGES[move.piece_captured], end_square)

            screen.blit(IMAGES[move.piece_moved], pygame.Rect(BORDER_SIZE + col * SQUARE_SIZE, BORDER_SIZE + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # self.highlight_move_made(screen, move)  # Highlighting made move

            pygame.display.flip()
            clock.tick(MAXIMUM_FPS)
