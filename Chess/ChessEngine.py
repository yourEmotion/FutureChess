"""
Этот класс хранит всю информацию о нынешнем состоянии шахматной игры. Также этот класс будет определять какие
ходы можно делать, а какие нельзя. Также он будет хранить LOG игры.
"""


class GameState():
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

class Move():

    def __init__(self, sqStart, sqEnd, board):
        self.startCol = sqStart[0]
        self.startRow = sqStart[1]
        self.endCol = sqEnd[0]
        self.endRow = sqEnd[1]
