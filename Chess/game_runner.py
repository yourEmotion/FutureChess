"""
Это основной драйвер игры, он будет преобразовывать входные данные и показывать текущее состояние объекта
"""

import pygame as p

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
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def game(white_is_human: bool, black_is_human: bool, board_color: str) -> None:
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    move_log_font = p.font.SysFont("Times New Roman", int(BOARD_WIDTH // 30), False, False)
    gs = chess_engine.GameState()
    valid_moves = gs.get_valid_moves()
    move_is_made = False
    load_images()
    animate = True
    running = True
    sq_selected = ()
    player_clicks = []
    game_over = False
    while running:
        human_turn = (gs.white_to_move and white_is_human) or (not gs.white_to_move and black_is_human)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Нажата кнопка мыши
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if col >= 8 or sq_selected == (row, col) or (sq_selected == () and gs.board[row][col] == "--"):
                        sq_selected = ()
                        player_clicks = []
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)
                    if len(player_clicks) == 2:
                        move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                move_is_made = True
                                gs.make_move(valid_moves[i])
                                animate = True
                                sq_selected = ()
                                player_clicks = []
                        if not move_is_made and gs.board[row][col] == "--":
                            sq_selected = ()
                            player_clicks = []
                        elif not move_is_made:
                            player_clicks = [sq_selected]

            # Нажата клавиша на клавиатуре
            elif e.type == p.KEYDOWN:
                if e.key == p.K_LCTRL:
                    if white_is_human and black_is_human:
                        gs.undo_move()
                    elif human_turn:
                        gs.undo_move()
                        gs.undo_move()
                    else:
                        gs.undo_move()
                    move_is_made = True
                    game_over = False
                    animate = False
                if e.key == p.K_r:  # reset button
                    gs = chess_engine.GameState()
                    valid_moves = gs.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_is_made = False
                    game_over = False
                    animate = False
                    human_turn = (gs.white_to_move and white_is_human) or (not gs.white_to_move and black_is_human)
                if e.key == p.K_q:  # quit button
                    running = False
        # AI logic
        if not game_over and not human_turn:
            ai_move = AI.find_best_move(gs, valid_moves)
            if ai_move is None:
                ai_move = AI.find_random_move(valid_moves)
            gs.make_move(ai_move)
            animate = True
            move_is_made = True

        if move_is_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock, board_color)
            valid_moves = gs.get_valid_moves()
            move_is_made = False
            animate = False
        draw_game_state(screen, gs, valid_moves, sq_selected, move_log_font, board_color)
        if gs.checkmate or gs.stalemate:
            game_over = True
            draw_text(screen,
                      'Stalemate' if gs.stalemate else 'Black wins by checkmate' if gs.white_to_move else 'White wins by checkmate')
        clock.tick(MAX_FPS)
        p.display.flip()
    p.quit()


def draw_game_state(screen, gs, valid_moves, sq_selected, move_log_font, board_color):
    draw_board(screen, board_color)
    highlight_squares(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)
    draw_move_log(screen, gs, move_log_font)


def draw_board(screen, board_colors):
    global colors
    colors = [p.Color(color) for color in board_colors.split("-")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_squares(screen, gs, valid_moves, sq_selected):
    if sq_selected != ():
        r, c = sq_selected
        if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # прозрачность (0, 255)
            s.fill(p.Color('green'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # p.draw.rect(screen, p.Color("green"), p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE), 2)
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (SQ_SIZE * move.end_col, SQ_SIZE * move.end_row))
    if gs.move_log:
        l = p.Surface((SQ_SIZE, SQ_SIZE))
        l.set_alpha(100)  # прозрачность (0, 255)
        l.fill(p.Color('red'))
        last_move = gs.move_log[-1]
        r, c = last_move.start_row, last_move.start_col
        screen.blit(l, (c * SQ_SIZE, r * SQ_SIZE))
        r, c = last_move.end_row, last_move.end_col
        screen.blit(l, (c * SQ_SIZE, r * SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_move_log(screen, gs, font):
    move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("grey"), move_log_rect)
    move_log = gs.move_log
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
        text_object = font.render(text, False, p.Color('Blue'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing


def draw_text(screen, text):
    font = p.font.SysFont("Helvitca", BOARD_HEIGHT // 16, True, False)
    text_object = font.render(text, False, p.Color('Black'))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
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
        end_square = p.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, end_square)

        if move.piece_captured != "--":
            if move.is_enpassant_move:
                en_passant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = p.Rect(move.end_col * SQ_SIZE, en_passant_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.piece_captured], end_square)

        screen.blit(IMAGES[move.piece_moved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(144)