"""
Это основной драйвер игры, он будет преобразовывать входные данные и показывать текущее состояние объекта
"""

import pygame as p
import ChessEngine
import AI


BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def Game(white_is_human: bool, black_is_human: bool, board_color: str) -> None:
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial", 16, False, False)
    gs = ChessEngine.GameState()
    valid_moves = gs.getValidMoves()
    move_is_made = False
    loadImages()
    animate = False
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    while running:
        human_turn = (gs.whiteToMove and white_is_human) or (not gs.whiteToMove and black_is_human)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Нажата кнопка мыши
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and human_turn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or (sqSelected == () and gs.board[row][col] == "--") or col >= 8:
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
                    if white_is_human and black_is_human:
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
                if e.key == p.K_q:  # quit button
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
        drawGameState(screen, gs, valid_moves, sqSelected, moveLogFont)
        if gs.checkmate or gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate' if gs.stalemate else 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate')
        clock.tick(MAX_FPS)
        p.display.flip()
    p.quit()

def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont, board_color):
    drawBoard(screen, board_color)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)


def drawBoard(screen, board_colors):
    global colors
    colors = [p.Color(color) for color in board_colors.split("-")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

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

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("grey"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i+1]) + "  "
        moveTexts.append(moveString)
    movesPerRow = 3
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]
        text += "  "
        textObject = font.render(text, False, p.Color('Black'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, False, p.Color('Black'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2,
                                                                BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)

def animateMove(move, screen, board, clock, board_colors):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen, board_colors)
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