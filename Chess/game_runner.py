"""
Это основной драйвер игры, он будет преобразовывать входные данные и показывать текущее состояние объекта
"""

import pygame

import AI
import chess_engine

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = BOARD_WIDTH // 1.5
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def game(white_is_human: bool, black_is_human: bool, board_color: str) -> None:
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    move_log_font = pygame.font.SysFont("Times New Roman", int(BOARD_WIDTH // 30), False, False)
    game_state = chess_engine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_is_made = False
    load_images()
    animate = True
    running = True
    sq_selected = ()
    player_clicks = []
    game_over = False
    while running:
        human_turn = (game_state.white_to_move and white_is_human) or (not game_state.white_to_move and black_is_human)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            # Нажата кнопка мыши
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = pygame.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if col >= 8 or sq_selected == (row, col) or (sq_selected == () and game_state.board[row][col] == "--"):
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)
                    if len(player_clicks) == 2:
                        move = chess_engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                move_is_made = True
                                game_state.make_move(valid_moves[i])
                                animate = True
                                sq_selected = ()
                                player_clicks = []
                        if not move_is_made and game_state.board[row][col] == "--":
                            sq_selected = ()
                            player_clicks = []
                        elif not move_is_made:
                            player_clicks = [sq_selected]

            # Нажата клавиша на клавиатуре
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LCTRL:
                    if white_is_human and black_is_human:
                        game_state.undo_move()
                    elif human_turn:
                        game_state.undo_move()
                        game_state.undo_move()
                    else:
                        game_state.undo_move()
                    move_is_made = True
                    game_over = False
                    animate = False
                if e.key == pygame.K_r:  # reset button
                    game_state = chess_engine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_is_made = False
                    game_over = False
                    animate = False
                    human_turn = (game_state.white_to_move and white_is_human) or (not game_state.white_to_move and black_is_human)
                if e.key == pygame.K_q:  # quit button
                    running = False
        # AI logic
        if not game_over and not human_turn:
            ai_move = AI.find_best_move(game_state, valid_moves)
            if ai_move is None:
                ai_move = AI.find_random_move(valid_moves)
            game_state.make_move(ai_move)
            animate = True
            move_is_made = True

        if move_is_made:
            if animate:
                animate_move(game_state.move_log[-1], screen, game_state.board, clock, board_color)
            valid_moves = game_state.get_valid_moves()
            move_is_made = False
            animate = False
        draw_game_state(screen, game_state, valid_moves, sq_selected, move_log_font, board_color)
        if game_state.checkmate or game_state.stalemate:
            game_over = True
            draw_text(screen,
                      'Stalemate' if game_state.stalemate else 'Black wins by checkmate' if game_state.white_to_move else 'White wins by checkmate')
        clock.tick(MAX_FPS)
        pygame.display.flip()
    pygame.quit()


def draw_game_state(screen, game_state, valid_moves, sq_selected, move_log_font, board_color):
    draw_board(screen, board_color)
    highlight_squares(screen, game_state, valid_moves, sq_selected)
    draw_pieces(screen, game_state.board)
    draw_move_log(screen, game_state, move_log_font)


def draw_board(screen, board_colors):
    global colors
    colors = [pygame.Color(color) for color in board_colors.split("-")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_squares(screen, game_state, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if game_state.board[r][c][0] == ('w' if game_state.white_to_move else 'b'):
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # прозрачность (0, 255)
            s.fill(pygame.Color('green'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(pygame.Color('yellow'))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (SQ_SIZE * move.end_col, SQ_SIZE * move.end_row))
    if game_state.move_log:
        l = pygame.Surface((SQ_SIZE, SQ_SIZE))
        l.set_alpha(100)  # прозрачность (0, 255)
        l.fill(pygame.Color('red'))
        last_move = game_state.move_log[-1]
        r, c = last_move.start_row, last_move.start_col
        screen.blit(l, (c * SQ_SIZE, r * SQ_SIZE))
        r, c = last_move.end_row, last_move.end_col
        screen.blit(l, (c * SQ_SIZE, r * SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_move_log(screen, game_state, font):
    move_log_rect = pygame.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    pygame.draw.rect(screen, pygame.Color("grey"), move_log_rect)
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        moveString = str(i // 2 + 1) + ". " + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            moveString += str(move_log[i + 1]) + "  "
        move_texts.append(moveString)
    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]
        text += "  "
        text_object = font.render(text, False, pygame.Color('Blue'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def draw_text(screen, text):
    font = pygame.font.SysFont("Helvitca", BOARD_HEIGHT // 16, True, False)
    text_object = font.render(text, False, pygame.Color('Black'))
    text_location = pygame.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                 BOARD_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)


def animate_move(move, screen, board, clock, board_colors):
    global colors
    dr = move.end_row - move.start_row
    dc = move.end_col - move.start_col
    frames_per_square = 10
    frame_count = (abs(dr) + abs(dc)) * frames_per_square
    for frame in range(frame_count + 1):
        r, c = (move.start_row + dr * frame / frame_count, move.start_col + dc * frame / frame_count)
        draw_board(screen, board_colors)
        draw_pieces(screen, board)

        color = colors[(move.end_row + move.end_col) % 2]
        end_square = pygame.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, end_square)

        if move.piece_captured != "--":
            if move.is_enpassant_move:
                en_passant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = pygame.Rect(move.end_col * SQ_SIZE, en_passant_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)

        screen.blit(IMAGES[move.piece_moved], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        clock.tick(144)
