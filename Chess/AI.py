import random
import numpy as np
from random import randint

piece_score = {"K": 0, "Q": 1000, "R": 500, "B": 350, "N": 300, "p": 100}
CHECKMATE = 100000
STALEMATE = 0
DEPTH = 2
count = 0

white_pawn_scores = np.array([[90, 90, 90, 90, 90, 90, 90, 90],
                              [30, 30, 30, 40, 40, 30, 30, 30],
                              [20, 20, 20, 30, 30, 30, 20, 20],
                              [10, 10, 10, 20, 20, 10, 10, 10],
                              [5, 5, 10, 20, 20, 5, 5, 5],
                              [0, 0, 0, 5, 5, 0, 0, 0],
                              [0, 0, 0, -10, -10, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0]], dtype=np.int32)

black_pawn_scores = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 10, 10, 0, 0, 0],
                              [0, 0, 0, -5, -5, 0, 0, 0],
                              [-5, -5, -10, -20, -20, -5, -5, -5],
                              [-10, -10, -10, -20, -20, -10, -10, -10],
                              [-20, -20, -20, -30, -30, -30, -20, -20],
                              [-30, -30, -30, -40, -40, -30, -30, -30],
                              [-90, -90, -90, -90, -90, -90, -90, -90]], dtype=np.int32)

white_rook_scores = np.array([[50, 50, 50, 50, 50, 50, 50, 50],
                              [50, 50, 50, 50, 50, 50, 50, 50],
                              [0, 0, 10, 20, 20, 10, 0, 0],
                              [0, 0, 10, 20, 20, 10, 0, 0],
                              [0, 0, 10, 20, 20, 10, 0, 0],
                              [0, 0, 10, 20, 20, 10, 0, 0],
                              [0, 0, 10, 20, 20, 10, 0, 0],
                              [0, 0, 0, 20, 20, 0, 0, 0]], dtype=np.int32)

black_rook_scores = np.array([[0, 0, 0, -20, -20, 0, 0, 0],
                              [0, 0, -10, -20, -20, -10, 0, 0],
                              [0, 0, -10, -20, -20, -10, 0, 0],
                              [0, 0, -10, -20, -20, -10, 0, 0],
                              [0, 0, -10, -20, -20, -10, 0, 0],
                              [0, 0, -10, -20, -20, -10, 0, 0],
                              [-50, -50, -50, -50, -50, -50, -50, 50],
                              [-50, -50, -50, -50, -50, -50, -50, 50]], dtype=np.int32)

white_knight_scores = np.array([[-5, 0, 0, 0, 0, 0, 0, -5],
                                [-5, 0, 0, 10, 10, 0, 0, -5],
                                [-5, 5, 20, 20, 20, 20, 5, -5],
                                [-5, 10, 20, 30, 30, 20, 10, -5],
                                [-5, 10, 20, 30, 30, 20, 10, -5],
                                [-5, 5, 20, 10, 10, 20, 5, -5],
                                [-5, 0, 0, 0, 0, 0, 0, -5],
                                [-5, -10, 0, 0, 0, 0, -10, -5]], dtype=np.int32)

black_knight_scores = np.array([[5, 10, 0, 0, 0, 0, 10, 5],
                                [5, 0, 0, 0, 0, 0, 0, 5],
                                [5, -5, -20, -10, -10, -20, -5, 5],
                                [5, -10, -20, -30, -30, -20, -10, 5],
                                [5, -10, -20, -30, -30, -20, -10, 5],
                                [5, -5, -20, -20, -20, -20, -5, 5],
                                [5, 0, 0, -10, -10, 0, 0, 5],
                                [5, 0, 0, 0, 0, 0, 0, 5]], dtype=np.int32)

white_bishop_scores = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 10, 10, 0, 0, 0],
                                [0, 0, 10, 20, 20, 10, 0, 0],
                                [0, 0, 10, 20, 20, 10, 0, 0],
                                [0, 10, 0, 0, 0, 0, 10, 0],
                                [0, 30, 0, 0, 0, 0, 30, 0],
                                [0, 0, -10, 0, 0, -10, 0, 0]], dtype=np.int32)

black_bishop_scores = np.array([[0, 0, 10, 0, 0, 10, 0, 0],
                                [0, -30, 0, 0, 0, 0, -30, 0],
                                [0, -10, 0, 0, 0, 0, -10, 0],
                                [0, 0, -10, -20, -20, -10, 0, 0],
                                [0, 0, -10, -20, -20, -10, 0, 0],
                                [0, 0, 0, -10, -10, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]], dtype=np.int32)

white_queen_scores = white_rook_scores + white_bishop_scores

black_queen_scores = black_bishop_scores + black_rook_scores

white_king_scores = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 5, 5, 5, 5, 0, 0],
                              [0, 5, 5, 10, 10, 5, 5, 0],
                              [0, 5, 10, 20, 20, 10, 5, 0],
                              [0, 5, 10, 20, 20, 10, 5, 0],
                              [0, 0, 5, 10, 10, 5, 0, 0],
                              [0, 5, 5, -5, -5, 0, 5, 0],
                              [0, 0, 5, 0, -15, 0, 10, 0]], dtype=np.int32)

black_king_scores = np.array([[0, 0, -5, 0, 15, 0, -10, 0],
                              [0, -5, -5, 5, 5, 0, -5, 0],
                              [0, 0, -5, -10, -10, -5, 0, 0],
                              [0, -5, -10, -20, -20, -10, -5, 0],
                              [0, -5, -10, -20, -20, -10, -5, 0],
                              [0, -5, -5, -10, -10, -5, -5, 0],
                              [0, 0, -5, -5, -5, -5, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0]], dtype=np.int32)

piece_positional_scores = {"wp": white_pawn_scores, "bp": black_pawn_scores, "wR": white_rook_scores, "bR": black_rook_scores,
                           "wN": white_knight_scores, "bN": black_knight_scores, "wB": white_bishop_scores, "bB": black_bishop_scores,
                           "wQ": white_queen_scores, "bQ": black_queen_scores, "wK": white_king_scores, "bK": black_king_scores}


def find_random_move(valid_moves):
    return valid_moves[randint(0, len(valid_moves) - 1)]


def find_best_move(gs, valid_moves):
    global next_move, count
    next_move = None
    # find_move_min_max(gs, valid_moves, DEPTH, gs.white_to_move)
    find_move_nega_max_alpha_beta(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.white_to_move else -1)
    print(count)
    count = 0
    return next_move


def find_move_nega_max_alpha_beta(gs, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move, count
    if depth == 0:
        return turn_multiplier * score_board(gs)

    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        count += 1
        next_moves = gs.get_valid_moves()
        score = -find_move_nega_max_alpha_beta(gs, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


def score_board(gs):
    if gs.checkmate:
        if gs.white_to_move:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                score += piece_positional_scores[square][row][col]
            if square[0] == "w":
                score += piece_score[square[1]]
            elif square[0] == "b":
                score -= piece_score[square[1]]

    return score
