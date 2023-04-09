"""
Это основной драйвер игры, он будет преобразовывать входные данные и показывать текущее состояние объекта
"""

import pygame as p
import ChessEngine
import AI
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
    animate = False
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    playerOne = True # True если играет человек
    playerTwo = True # True если играет человек
    while running:
        human_turn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Нажата кнопка мыши
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and human_turn:
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
                                animate = True
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
                    if playerOne and playerTwo:
                        gs.undoMove()
                    elif human_turn:
                        gs.undoMove()
                        gs.undoMove()
                    else:
                        gs.undoMove()
                    move_is_made = True
                    gameOver = False
                    animate = False
                if e.key == p.K_r: # reset button
                    gs = ChessEngine.GameState()
                    valid_moves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    move_is_made = False
                    gameOver = False
                    animate = False
                if e.key == p.K_q: # quit button
                    running = False
        # AI logic
        if not gameOver and not human_turn:
            AIMove = AI.findRandomMove(valid_moves)
            gs.makeMove(AIMove)
            animate = True
            move_is_made = True

        if move_is_made:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            valid_moves = gs.getValidMoves()
            move_is_made = False
            animate = False
        drawGameState(screen, gs, valid_moves, sqSelected)
        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
                result["game finished"] = True
                result["black victory"] = True
            else:
                drawText(screen, 'White wins by checkmate')
                result["game finished"] = True
                result["white victory"] = True
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate')
            result["game finished"] = True
        clock.tick(MAX_FPS)
        p.display.flip()
    p.quit()
    return result


def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    global colors
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
    if gs.moveLog:
        l = p.Surface((SQ_SIZE, SQ_SIZE))
        l.set_alpha(100)  # прозрачность (0, 255)
        l.fill(p.Color('red'))
        last_move = gs.moveLog[-1]
        r, c = last_move.startRow, last_move.startCol
        screen.blit(l, (c * SQ_SIZE, r * SQ_SIZE))
        r, c = last_move.endRow, last_move.endCol
        screen.blit(l, (c * SQ_SIZE, r * SQ_SIZE))
def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, False, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width()/2,
                                                    HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)

        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)

        if move.pieceCaptured != "--":
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


