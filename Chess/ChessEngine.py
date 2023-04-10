"""
Этот класс хранит всю информацию о нынешнем состоянии шахматной игры. Также этот класс будет определять какие
ходы можно делать, а какие нельзя. Также он будет хранить LOG игры.
"""


class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.move_repetition = False
        self.enpassantPossible = ()
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight = CastleRight(True, True, True, True)
        self.castleRightsLog = [CastleRight(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
            '''
            Надо бы здесь сделать всплывающее окно или типо того
            для выбора promotion, пока сразу в королеву 
            '''
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"

        if move.pieceMoved[1] == 'p' and abs(move.endRow - move.startRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

        if move.isCastlingMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "--"

        self.enpassantPossibleLog.append(self.enpassantPossible)
        # Рокировка
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRight(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                                self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.whiteToMove = not self.whiteToMove

            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            # undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            # undo castling
            self.castleRightsLog.pop()
            castleRight = CastleRight(self.castleRightsLog[-1].wks, self.castleRightsLog[-1].bks,
                                      self.castleRightsLog[-1].wqs, self.castleRightsLog[-1].bqs)
            self.currentCastlingRight = castleRight

            if move.isCastlingMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"
            self.checkmate = False
            self.stalemate = False

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wqs = False
            self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

        if move.pieceCaptured == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

    def hasMoveRepetition(self):
        return self.moveLog[-1] == self.moveLog[-5] == self.moveLog[-9] and\
            self.moveLog[-2] == self.moveLog[-6] == self.moveLog[-10]
    def getValidMoves(self):
        tmp_castle_rights = CastleRight(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        tmp_enapassant_possible = self.enpassantPossible
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        self.enpassantPossible = tmp_enapassant_possible
        self.currentCastlingRight = tmp_castle_rights
        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        opp_moves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for m in opp_moves:
            if m.endRow == r and m.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if r != 0:
                # движение на 1 клетку
                if self.board[r - 1][c] == "--":
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    # движение на 2 клетки
                    if r == 6 and self.board[r - 2][c] == "--":
                        moves.append(Move((r, c), (r - 2, c), self.board))
                # Атака налево и направо
                if 0 < c < 7:
                    if self.board[r - 1][c - 1][0] == 'b':
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
                    elif (r - 1, c - 1) == self.enpassantPossible:
                        moves.append(Move((r, c), (r - 1, c - 1), self.board, isEmpassantMove=True))

                    if self.board[r - 1][c + 1][0] == 'b':
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
                    elif (r - 1, c + 1) == self.enpassantPossible:
                        moves.append(Move((r, c), (r - 1, c + 1), self.board, isEmpassantMove=True))
                # Атака направо
                if c == 0 and self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif c == 0 and (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEmpassantMove=True))
                # Атака налево
                if c == 7 and self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif c == 7 and (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEmpassantMove=True))
        else:
            if r != 7:
                # движение на 1 клетку
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    # движение на 2 клетки
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move((r, c), (r + 2, c), self.board))
                # Атака налево и направо
                if 0 < c < 7:
                    if self.board[r + 1][c - 1][0] == 'w':
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                    elif (r + 1, c - 1) == self.enpassantPossible:
                        moves.append(Move((r, c), (r + 1, c - 1), self.board, isEmpassantMove=True))
                    if self.board[r + 1][c + 1][0] == 'w':
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
                    elif (r + 1, c + 1) == self.enpassantPossible:
                        moves.append(Move((r, c), (r + 1, c + 1), self.board, isEmpassantMove=True))
                # Атака направо
                if c == 0 and self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif c == 0 and (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEmpassantMove=True))
                # Атака налево
                if c == 7 and self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif c == 7 and (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEmpassantMove=True))

    def getRookMoves(self, r, c, moves):
        my_color = "w" if self.whiteToMove else "b"
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == my_color:
                        break
                    else:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        my_color = "w" if self.whiteToMove else "b"
        possibleMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for m in possibleMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != my_color:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        my_color = "w" if self.whiteToMove else "b"
        directions = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == my_color:
                        break
                    else:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        my_color = "w" if self.whiteToMove else "b"
        possibleMoves = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        for m in possibleMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != my_color:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.currentCastlingRight.wks and self.whiteToMove) or (self.currentCastlingRight.bks and not self.whiteToMove):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.currentCastlingRight.wqs and self.whiteToMove) or (self.currentCastlingRight.bqs and not self.whiteToMove):
            self.getQueensideCastleMoves(r, c, moves)

    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--":
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastlingMove=True))

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastlingMove=True))


class CastleRight():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEmpassantMove=False, isCastlingMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
            self.isPawnPromotion = True

        self.isEnpassantMove = isEmpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (
                self.pieceMoved == 'bp' and self.endRow == 7)

        self.isCastlingMove = isCastlingMove
        self.isCapture = self.pieceCaptured != '--'

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def __str__(self):
        #castle move
        if self.isCastlingMove:
            return "O-O" if self.endCol == 6 else "O-O-O"

        endSquare = self.getRankFile(self.endRow, self.endCol)

        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

            # add pawn promotions

        # add another + checks and checkmates

        #piece moves
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare
