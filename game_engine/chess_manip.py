from game_engine.pieces_moves import Move, CastleRights
from game_engine.game_objects import GameObjects


class MainMenuButton:
    """Class for main menu buttons. Includes their their coords and size."""
    def __init__(self, x, y, width, height=GameObjects.FONT_SIZE, is_text=True) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_text = is_text


class LangSettings:
    def __init__(self, lang) -> None:
        self.lang_name = lang
        if lang == "eng":
            # Endgame.
            self.w_win = "Checkmate! White won"
            self.b_win = "Checkmate! Black won"
            self.stale = "Stalemate! Draw"
            self.click = "Click any button to return to the Main Menu"
            self.surrender = "Are you sure you want to surrender?"
            self.confirm = "Confirm"
            # Main menu.
            self.main = "Main Menu"
            self.rating = "Play rating game"
            self.p_white = "Play as white"
            self.p_black = "Play as black"
            self.p_vs_f = "Play against a friend"
            self.custom_b = "Play with a custom board"
            # Settings.
            self.settings = "Settings"
            self.language = "Language:"
            self.difficulty = "Difficulty level:"
            self.board_theme = "Board theme:"
            self.piece_set = "Piece set:"
        elif lang == "rus":
            # Endgame.
            self.w_win = "Мат! Белые выиграли"
            self.b_win = "Мат! Черные выиграли"
            self.stale = "Пат! Ничья"
            self.click = "Нажмите любую кнопку, чтобы вернуться в Главное Меню"
            self.surrender = "Вы уверены, что хотите сдаться?"
            self.confirm = "Подтвердить"
            # Main menu.
            self.main = "Главное Меню"
            self.rating = "Играть в рейтинговую игру"
            self.p_white = "Играть за белых"
            self.p_black = "Играть за черных"
            self.p_vs_f = "Играть против друга"
            self.custom_b = "Игра co спец. доской"
            # Settings.
            self.settings = "Настройки"
            self.language = "Язык:"
            self.difficulty = "Уровень сложности:"
            self.board_theme = "Тема доски:"
            self.piece_set = "Тема фигур:"
        elif lang == "ger":
            # Endgame.
            self.w_win = "Schachmatt! Weiß hat gewonnen"
            self.b_win = "Schachmatt! Schwarz hat gewonnen"
            self.stale = "Patt! Unentschieden"
            self.click = "Klicken Sie auf eine beliebige Schaltfläche, um zum Hauptmenü zurückzukehren"
            self.surrender = "Sind Sie sicher, dass Sie aufgeben wollen?"
            self.confirm = "Bestätigen"
            # Main menu.
            self.main = "Hauptmenü"
            self.rating = "Bewertungsspiel spielen"
            self.p_white = "Als Weiß spielen"
            self.p_black = "Spiele als Schwarz"
            self.p_vs_f = "Spiele gegen einen Freund"
            self.custom_b = "Besonderes Spiel"
            # Settings.
            self.settings = "Einstellungen"
            self.language = "Sprache:"
            self.difficulty = "Schwierigkeitsgrad:"
            self.board_theme = "Board-Design:"
            self.piece_set = "Stücksatz:"
        elif lang == "fra":
            # Endgame.
            self.w_win = "Échec et mat! Les blancs ont gagné"
            self.b_win = "Échec et mat! Les noirs ont gagné"
            self.stale = "Impasse! Tirage au sort"
            self.click = "Cliquez sur n'importe quel bouton pour revenir au Menu Principal"
            self.surrender = "Êtes-vous sûr de vouloir vous rendre?"
            self.confirm = "Confirmer"
            # Main menu.
            self.main = "Menu Principal"
            self.rating = "Jouer au jeu d'évaluation"
            self.p_white = "Jouer en blanc"
            self.p_black = "Jouer en noir"
            self.p_vs_f = "Jouer contre un ami"
            self.custom_b = "Jeu spécial"
            # Settings.
            self.settings = "Paramètres"
            self.language = "Langue:"
            self.difficulty = "Niveau de difficulté:"
            self.board_theme = "Thème du tableau:"
            self.piece_set = "Ensemble de pièces:"
        elif lang == "chi":
            # Endgame.
            self.w_win = "将死！白方赢了"
            self.b_win = "将死！黑方赢了"
            self.stale = "僵局！平局"
            self.click = "点击任意按钮返回主菜单"
            self.surrender = "你确定要投降吗?"
            self.confirm = "确认"
            # Main menu.
            self.main = "主菜单"
            self.rating = "玩评级游戏"
            self.p_white = "扮演白人"
            self.p_black = "扮演黑人"
            self.p_vs_f = "和朋友对战"
            self.custom_b = "玩自定义棋盘"
            # Settings.
            self.settings = "设置"
            self.language = "语言:"
            self.difficulty = "难度等级"
            self.board_theme = "棋盘主题"
            self.piece_set = "棋子集"


class GameBoardState:
    """Class where all moves possibilities compute."""
    DIMENSIONS = GameObjects.DIMENSIONS

    def __init__(self, board_type=None, black_down=False) -> None:
        self.board = board_type
        self.white_to_move = True
        self.is_enpassant_possible = tuple()
        self.is_enpassant_possible_log = [self.is_enpassant_possible]
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castling_rights.wks, 
        self.current_castling_rights.bks, self.current_castling_rights.wqs, self.current_castling_rights.bqs)]
        self.move_log = list()
        self.white_king_location = (GameObjects.DIMENSIONS - 1, GameObjects.DIMENSIONS // 2)
        self.black_king_location = (0, GameObjects.DIMENSIONS // 2)
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        self.pins = list()
        self.checks = list()
        self.w_side_literal = "w"
        self.b_side_literal = "b"
        self.black_down = black_down

    def make_move(self, move) -> str:
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        if move.piece_moved == self.w_side_literal + "K":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == self.b_side_literal + "K":
            self.black_king_location = (move.end_row, move.end_col)

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"

        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = "--"

        if move.piece_moved[1] == "p" and abs(move.start_row - move.end_row) == 2:
            self.is_enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.is_enpassant_possible = tuple()

        if move.is_castle_move and not self.black_down:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = "--"
            else:
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                self.board[move.end_row][move.end_col - 2] = "--"
        elif move.is_castle_move and self.black_down:
            if move.end_col - move.start_col == -2:
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                self.board[move.end_row][move.end_col - 1] = "--"
            else:
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 2]
                self.board[move.end_row][move.end_col + 2] = "--"

        self.update_castle_rights(move)
        self.is_enpassant_possible_log.append(self.is_enpassant_possible)
        self.castle_rights_log.append(CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks, self.current_castling_rights.wqs, self.current_castling_rights.bqs))
        current_move_made = Move([move.start_row, move.start_col], [move.end_row, move.end_col], self.board).get_chess_notation()

        return current_move_made

    def undo_move(self) -> None:
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move  # swap players

            if move.piece_moved == self.w_side_literal + "K":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == self.b_side_literal + "K":
                self.black_king_location = (move.start_row, move.start_col)

            if move.is_enpassant_move:
                self.board[move.end_row][move.end_col] = "--"
                self.board[move.start_row][move.end_col] = move.piece_captured

            self.is_enpassant_possible_log.pop()
            self.is_enpassant_possible = self.is_enpassant_possible_log[-1]

            self.castle_rights_log.pop()
            self.current_castling_rights = self.castle_rights_log[-1]

            if move.is_castle_move:
                if move.end_col - move.start_col == 2:
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = '--'
                else:
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = '--'

            self.checkmate = False
            self.stalemate = False

    def get_all_poissible_moves(self) -> list:
        moves = list()

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == self.w_side_literal and self.white_to_move) or (turn == self.b_side_literal and not self.white_to_move):
                    piece = self.board[row][col][1]

                    if piece == "p":
                        self.get_pawn_moves(row, col, moves)
                    elif piece == "R":
                        self.get_rook_moves(row, col, moves)
                    elif piece == "N":
                        self.get_knight_moves(row, col, moves)
                    elif piece == "B":
                        self.get_bishop_moves(row, col, moves)
                    elif piece == "Q":
                        self.get_queen_moves(row, col, moves)
                    elif piece == "K":
                        self.get_king_moves(row, col, moves)

        return moves

    def get_pawn_moves(self, row, col, moves) -> None:
        piece_pinned = False
        pin_direction = tuple()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:
            move_amount = -1 if not self.black_down else 1
            start_row = 6 if not self.black_down else 1
            enemy_colour = self.b_side_literal
            king_row, king_col = self.white_king_location
        else:
            move_amount = 1 if not self.black_down else -1
            start_row = 1 if not self.black_down else 6
            enemy_colour = self.w_side_literal
            king_row, king_col = self.black_king_location

        if self.board[row + move_amount][col] == "--":
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move((row, col), (row + move_amount, col), self.board))
                if row == start_row and self.board[row + 2 * move_amount][col] == "--":
                    moves.append(Move((row, col), (row + 2 * move_amount, col), self.board))

        if col - 1 >= 0:
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[row + move_amount][col - 1][0] == enemy_colour:
                    moves.append(Move((row, col), (row + move_amount, col - 1), self.board))
                if (row + move_amount, col - 1) == self.is_enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:
                            inside_range = range(king_col + 1, col - 1)
                            outside_range = range(col + 1, 8)
                        else:
                            inside_range = range(king_col - 1, col, -1)
                            outside_range = range(col - 2, -1, -1)

                        for i in inside_range:
                            if self.board[row][i] != "--":
                                blocking_piece = True

                        for i in outside_range:
                            square = self.board[row][i]

                            if square[0] == enemy_colour and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True

                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, col), (row + move_amount, col - 1), self.board, is_enpassant_move=True))

        if col + 1 <= 7:
            if not piece_pinned or pin_direction == (move_amount, +1):
                if self.board[row + move_amount][col + 1][0] == enemy_colour:
                    moves.append(Move((row, col), (row + move_amount, col + 1), self.board))
                if (row + move_amount, col + 1) == self.is_enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:
                            inside_range = range(king_col + 1, col)
                            outside_range = range(col + 2, 8)
                        else:
                            inside_range = range(king_col - 1, col + 1, -1)
                            outside_range = range(col - 1, -1, -1)

                        for i in inside_range:
                            if self.board[row][i] != "--":
                                blocking_piece = True

                        for i in outside_range:
                            square = self.board[row][i]

                            if square[0] == enemy_colour and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True

                    if not attacking_piece or blocking_piece:
                        moves.append(Move((row, col), (row + move_amount, col + 1), self.board, is_enpassant_move=True))

    def get_rook_moves(self, row, col, moves) -> None:
        piece_pinned = False
        pin_direction = tuple()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_colour = self.b_side_literal if self.white_to_move else self.w_side_literal

        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]

                        if end_piece == "--":
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_colour:
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_knight_moves(self, row, col, moves) -> None:
        piece_pinned = False

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        ally_colour = self.w_side_literal if self.white_to_move else self.b_side_literal

        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]

            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]

                    if end_piece[0] != ally_colour:
                        moves.append(Move((row, col), (end_row, end_col), self.board))

    def get_bishop_moves(self, row, col, moves) -> None:
        piece_pinned = False
        pin_direction = tuple()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        enemy_colour = self.b_side_literal if self.white_to_move else self.w_side_literal

        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                        end_piece = self.board[end_row][end_col]

                        if end_piece == "--":
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_colour:
                            moves.append(Move((row, col), (end_row, end_col), self.board))
                            break
                        else:
                            break
                else:
                    break

    def get_queen_moves(self, row, col, moves) -> None:
        self.get_bishop_moves(row, col, moves)
        self.get_rook_moves(row, col, moves)

    def get_king_moves(self, row, col, moves) -> None:
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_colour = self.w_side_literal if self.white_to_move else self.b_side_literal

        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]

            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_colour:
                    if ally_colour == self.w_side_literal:
                        self.white_king_location = (end_row, end_col)
                    else:
                        self.black_king_location = (end_row, end_col)

                    in_check, pins, checks = self.check_for_pins_or_checks()

                    if not in_check:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    
                    if ally_colour == self.w_side_literal:
                        self.white_king_location = (row, col)
                    else:
                        self.black_king_location = (row, col)

    def update_castle_rights(self, move) -> None:
        if move.piece_captured == self.w_side_literal + "R":
            if move.end_col == 0:
                self.current_castling_rights.wqs = False
            elif move.end_col == 7:
                self.current_castling_rights.wks = False
        elif move.piece_captured == self.b_side_literal + "R":
            if move.end_col == 0:
                self.current_castling_rights.bqs = False
            elif move.end_col == 7:
                self.current_castling_rights.bks = False

        if move.piece_moved == self.w_side_literal + "K":
            self.current_castling_rights.wqs = False
            self.current_castling_rights.wks = False
        elif move.piece_moved == self.b_side_literal + "K":
            self.current_castling_rights.bqs = False
            self.current_castling_rights.bks = False
        elif move.piece_moved == self.w_side_literal + "R":
            if move.start_row == 7:
                if move.start_col == 0:
                    self.current_castling_rights.wqs = False
                elif move.start_col == 7:
                    self.current_castling_rights.wks = False
        elif move.piece_moved == self.b_side_literal + "R":
            if move.start_row == 0:
                if move.start_col == 0:
                    self.current_castling_rights.bqs = False
                elif move.start_col == 7:
                    self.current_castling_rights.bks = False

    def get_castle_moves(self, row, col, moves) -> None:
        if self.square_under_attack(row, col):
            return  # Nothing.

        if (self.white_to_move and self.current_castling_rights.wks) or (not self.white_to_move and self.current_castling_rights.bks):
            self.get_kingside_castle_moves(row, col, moves)

        if (self.white_to_move and self.current_castling_rights.wqs) or (not self.white_to_move and self.current_castling_rights.bqs):
            self.get_queenside_castle_moves(row, col, moves)

    def get_kingside_castle_moves(self, row, col, moves) -> None:
        try:
            if not self.black_down:
                if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--':
                    if not self.square_under_attack(row, col + 1) and not self.square_under_attack(row, col + 2) and (self.board[0][7][1] == "R" or self.board[7][7][1] == "R"):
                        moves.append(Move((row, col), (row, col + 2), self.board, is_castle_move=True))
            else:
                if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--':
                    if not self.square_under_attack(row, col - 1) and not self.square_under_attack(row, col - 2) and (self.board[0][7][1] == "R" or self.board[7][7][1] == "R"):
                        moves.append(Move((row, col), (row, col - 2), self.board, is_castle_move=True))
        except:
            print("Error!")

    def get_queenside_castle_moves(self, row, col, moves) -> None:
        try:
            if not self.black_down:
                if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--':
                    if not self.square_under_attack(row, col - 1) and not self.square_under_attack(row, col - 2) and (self.board[0][0][1] == "R" or self.board[7][0][1] == "R"):
                        moves.append(Move((row, col), (row, col - 2), self.board, is_castle_move=True))
            else:
                if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--' and self.board[row][col + 3] == '--':
                    if not self.square_under_attack(row, col + 1) and not self.square_under_attack(row, col + 2) and (self.board[0][0][1] == "R" or self.board[7][0][1] == "R"):
                        moves.append(Move((row, col), (row, col + 2), self.board, is_castle_move=True))
        except:
            print("Error!")

    def square_under_attack(self, row, col) -> bool:
        self.white_to_move = not self.white_to_move
        opponents_moves = self.get_all_poissible_moves()
        self.white_to_move = not self.white_to_move

        for move in opponents_moves:
            if move.end_row == row and move.end_col == col:
                return True
        return False
    
    def check_for_pins_or_checks(self) -> tuple():
        pins = list()
        checks = list()
        in_check = False

        if self.white_to_move:
            enemy_colour = self.b_side_literal
            ally_colour = self.w_side_literal
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_colour = self.w_side_literal
            ally_colour = self.b_side_literal
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = tuple()

            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i

                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_colour and end_piece[1] != "K":
                        if possible_pin == tuple():
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else:
                            break
                    elif end_piece[0] == enemy_colour:
                        enemy_type = end_piece[1]
                        if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or \
                            (i == 1 and enemy_type == "p" and \
                            ((enemy_colour == self.w_side_literal and 6 <= j <= 7) or \
                            (enemy_colour == self.b_side_literal and 4 <= j <= 5))) or \
                            (enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                            if possible_pin == tuple():
                                in_check = True
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else:
                    break

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                
                if end_piece[0] == enemy_colour and end_piece[1] == "N":
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))

        return in_check, pins, checks

    def get_valid_moves(self) -> list:
        temp_c_r = CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks, self.current_castling_rights.wqs, self.current_castling_rights.bqs)

        moves = list()
        self.in_check, self.pins, self.checks = self.check_for_pins_or_checks()

        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]

        if self.in_check:
            if len(self.checks) == 1:
                moves = self.get_all_poissible_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = list()

                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[
                            1] == check_col:
                            break

                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != "K":
                        if not (moves[i].end_row,
                                moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_all_poissible_moves()

            if self.white_to_move:
                self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
            else:
                self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)

        if len(moves) == 0:
            if self.in_check:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        self.current_castling_rights = temp_c_r

        return moves
