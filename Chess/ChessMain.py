"""
Это основной драйвер игры, он будет преобразовывать входные данные и показывать текущее состояние объекта
"""

import pygame as p
import ChessEngine
from collections import defaultdict


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def Game():
    result = defaultdict()
    result["game finished"] = False
    result["white victory"] = False
    result["black victory"] = False
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    valid_moves = gs.getValidMoves()
    move_is_made = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Нажата кнопка мыши
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col) or (sqSelected == () and gs.board[row][col] == "--"):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    for i in range(len(valid_moves)):
                        if move == valid_moves[i]:
                            move_is_made = True
                            print(move.getChessNotation())
                            gs.makeMove(valid_moves[i])
                            sqSelected = ()
                            playerClicks = []
                    if not move_is_made and gs.board[row][col] == "--":
                        sqSelected = ()
                        playerClicks = []
                    elif not move_is_made:
                        playerClicks = [sqSelected]


            # Нажата клавиша на клавиатуре
            elif e.type == p.KEYDOWN:
                if e.key == p.K_LCTRL:
                    gs.undoMove()
                    move_is_made = True
        if move_is_made:
            valid_moves = gs.getValidMoves()
            move_is_made = False
        drawGameState(screen, gs, valid_moves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()
        if gs.checkMate:
            running = False
            if gs.whiteToMove:
                result["game finished"] = True
                result["black victory"] = True
            else:
                result["game finished"] = True
                result["white victory"] = True
            p.quit()
    p.quit()
    return result


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # прозрачность (0, 255)
            s.fill(p.Color('green'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # p.draw.rect(screen, p.Color("green"), p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE), 2)
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))