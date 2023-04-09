from random import randint

def findRandomMove(validMoves):
    return validMoves[randint(0, len(validMoves)-1)]
