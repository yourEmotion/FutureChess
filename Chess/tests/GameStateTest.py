import unittest
from Chess.chess_engine import GameState, Move
from copy import deepcopy

"""
Тестировка всех методов класса GameState происходит следующим образом:
на "живой" доске устанавливается произвольная позиция, и она же собирается некоторой комбинацией ходов,
которые могут иметь неосмысленный характер - важна конечная позиция. По живой доске определяются
ожидаемые (expected) результаты, а по результату выполнения метода - действительные (actual) результаты

Чтобы проверить истинность тестов, достаточно, например, в нужной функции для позиции добавить

for row in game_state.board:
    print(row)

чтобы увидеть состояние доски в данной позиции, и самостоятельно оценить возвращаемое значение функций
"""


def get_position_1(game_state):
    return game_state


def get_position_2(game_state):
    game_state.make_move(Move((6, 7), (4, 7), game_state.board))
    game_state.make_move(Move((0, 0), (6, 4), game_state.board))
    game_state.make_move(Move((6, 0), (4, 0), game_state.board))
    game_state.make_move(Move((0, 3), (6, 3), game_state.board))
    return game_state


def get_position_3(game_state):
    game_state.make_move(Move((6, 4), (4, 4), game_state.board))
    game_state.make_move(Move((1, 4), (3, 4), game_state.board))
    game_state.make_move(Move((7, 6), (5, 5), game_state.board))
    game_state.make_move(Move((0, 6), (2, 5), game_state.board))
    game_state.make_move(Move((6, 0), (2, 0), game_state.board))
    game_state.make_move(Move((0, 5), (4, 1), game_state.board))
    game_state.make_move(Move((0, 1), (2, 2), game_state.board))
    return game_state


def get_position_4(game_state):
    game_state.make_move(Move((6, 2), (1, 1), game_state.board))
    game_state.make_move(Move((1, 4), (3, 4), game_state.board))
    game_state.make_move(Move((6, 4), (4, 4), game_state.board))
    game_state.make_move(Move((1, 0), (3, 1), game_state.board))
    game_state.make_move(Move((7, 3), (4, 6), game_state.board))
    game_state.make_move(Move((1, 5), (3, 5), game_state.board))
    return game_state


def get_position_5(game_state):
    game_state.make_move(Move((7, 2), (1, 1), game_state.board))
    game_state.make_move(Move((0, 2), (1, 1), game_state.board))
    game_state.make_move(Move((7, 6), (1, 1), game_state.board))
    game_state.make_move(Move((1, 3), (1, 1), game_state.board))
    game_state.make_move(Move((7, 0), (1, 1), game_state.board))
    game_state.make_move(Move((1, 7), (2, 7), game_state.board))
    game_state.make_move(Move((7, 3), (2, 7), game_state.board))
    game_state.make_move(Move((0, 6), (2, 7), game_state.board))
    game_state.make_move(Move((6, 2), (4, 2), game_state.board))
    game_state.make_move(Move((6, 3), (4, 3), game_state.board))
    game_state.make_move(Move((6, 4), (4, 4), game_state.board))
    game_state.make_move(Move((6, 5), (3, 2), game_state.board))
    game_state.make_move(Move((1, 1), (2, 0), game_state.board))
    game_state.make_move(Move((0, 1), (3, 1), game_state.board))
    game_state.make_move(Move((7, 4), (4, 5), game_state.board))
    game_state.make_move(Move((7, 5), (4, 6), game_state.board))
    game_state.make_move(Move((7, 1), (2, 5), game_state.board))
    game_state.make_move(Move((0, 3), (1, 3), game_state.board))
    game_state.make_move(Move((6, 7), (5, 7), game_state.board))
    game_state.make_move(Move((0, 4), (3, 3), game_state.board))
    game_state.make_move(Move((5, 7), (3, 7), game_state.board))
    game_state.make_move(Move((1, 5), (2, 6), game_state.board))
    game_state.make_move(Move((7, 7), (7, 3), game_state.board))
    game_state.make_move(Move((6, 1), (5, 1), game_state.board))
    game_state.make_move(Move((0, 0), (0, 1), game_state.board))
    return game_state


def get_position_6(game_state):
    game_state.make_move(Move((6, 4), (3, 4), game_state.board))
    game_state.make_move(Move((1, 5), (3, 5), game_state.board))
    return game_state


def get_position_7(game_state):
    game_state.make_move(Move((6, 4), (3, 4), game_state.board))
    game_state.make_move(Move((1, 5), (3, 5), game_state.board))
    game_state.make_move(Move((6, 0), (5, 0), game_state.board))
    game_state.make_move(Move((1, 0), (2, 0), game_state.board))
    return game_state


class GameStateTest(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()

    def test_get_pawn_moves(self):
        """test 1"""
        position_1 = get_position_1(deepcopy(self.game_state))

        position_1_moves = []

        for row in range(len(position_1.board)):
            for column in range(len(position_1.board[row])):
                turn = position_1.board[row][column][0]
                if (turn == 'w' and position_1.white_to_move) or \
                        (turn == 'b' and not position_1.white_to_move):
                    piece = position_1.board[row][column][1]
                    if piece == 'p':
                        position_1.get_pawn_moves(row, column, position_1_moves)

        self.assertEqual(sorted([str(move) for move in position_1_moves]),
                         sorted(["a3", "a4", "b3", "b4", "c3", "c4", "d3", "d4", "e3", "e4", "f3", "f4", "g3", "g4",
                                 "h3", "h4"]))

        """test 2"""
        position_2 = get_position_2(deepcopy(self.game_state))

        position_2_moves = []

        for row in range(len(position_2.board)):
            for column in range(len(position_2.board[row])):
                turn = position_2.board[row][column][0]
                if (turn == 'w' and position_2.white_to_move) or \
                        (turn == 'b' and not position_2.white_to_move):
                    piece = position_2.board[row][column][1]
                    if piece == 'p':
                        position_2.get_pawn_moves(row, column, position_2_moves)

        self.assertEqual(sorted([str(move) for move in position_2_moves]),
                         sorted(['a5', 'b3', 'b4', 'c3', 'c4', 'f3', 'f4', 'g3', 'g4', 'h5']))

        """test 3"""
        position_3 = get_position_3(deepcopy(self.game_state))

        position_3_moves = []

        for row in range(len(position_3.board)):
            for column in range(len(position_3.board[row])):
                turn = position_3.board[row][column][0]
                if (turn == 'w' and position_3.white_to_move) or \
                        (turn == 'b' and not position_3.white_to_move):
                    piece = position_3.board[row][column][1]
                    if piece == 'p':
                        position_3.get_pawn_moves(row, column, position_3_moves)

        self.assertEqual(sorted([str(move) for move in position_3_moves]),
                         sorted(['b5', 'b6', 'bxa6', 'd5', 'd6', 'g5', 'g6', 'h5', 'h6']))

        """test 4"""
        position_4 = get_position_4(deepcopy(self.game_state))

        position_4_moves = []

        for row in range(len(position_4.board)):
            for column in range(len(position_4.board[row])):
                turn = position_4.board[row][column][0]
                if (turn == 'w' and position_4.white_to_move) or \
                        (turn == 'b' and not position_4.white_to_move):
                    piece = position_4.board[row][column][1]
                    if piece == 'p':
                        position_4.get_pawn_moves(row, column, position_4_moves)

        self.assertEqual(sorted([str(move) for move in position_4_moves]),
                         sorted(['a3', 'a4', 'b3', 'b4', 'bxa8', 'bxc8', 'd3', 'd4', 'exf5', 'f3', 'f4', 'g3', 'h3',
                                 'h4']))

        """test 5"""
        position_5 = get_position_5(deepcopy(self.game_state))

        position_5_moves = []

        for row in range(len(position_5.board)):
            for column in range(len(position_5.board[row])):
                turn = position_5.board[row][column][0]
                if (turn == 'w' and position_5.white_to_move) or \
                        (turn == 'b' and not position_5.white_to_move):
                    piece = position_5.board[row][column][1]
                    if piece == 'p':
                        position_5.get_pawn_moves(row, column, position_5_moves)

        self.assertEqual(sorted([str(move) for move in position_5_moves]),
                         sorted(['c6', 'e5', 'e6', 'exf6', 'g5', 'gxf6', 'gxh5']))

        """test 6"""
        position_6 = get_position_6(deepcopy(self.game_state))

        position_6_moves = []

        for row in range(len(position_6.board)):
            for column in range(len(position_6.board[row])):
                turn = position_6.board[row][column][0]
                if (turn == 'w' and position_6.white_to_move) or \
                        (turn == 'b' and not position_6.white_to_move):
                    piece = position_6.board[row][column][1]
                    if piece == 'p':
                        position_6.get_pawn_moves(row, column, position_6_moves)

        self.assertEqual(sorted([str(move) for move in position_6_moves]),
                         sorted(['a3', 'a4', 'b3', 'b4', 'c3', 'c4', 'd3', 'd4', 'e6',
                                 'exf6', 'f3', 'f4', 'g3', 'g4', 'h3', 'h4']))

        """test 7"""
        position_7 = get_position_7(deepcopy(self.game_state))

        position_7_moves = []

        for row in range(len(position_7.board)):
            for column in range(len(position_7.board[row])):
                turn = position_7.board[row][column][0]
                if (turn == 'w' and position_7.white_to_move) or \
                        (turn == 'b' and not position_7.white_to_move):
                    piece = position_7.board[row][column][1]
                    if piece == 'p':
                        position_7.get_pawn_moves(row, column, position_7_moves)

        self.assertEqual(sorted([str(move) for move in position_7_moves]),
                         sorted(['a4', 'b3', 'b4', 'c3', 'c4', 'd3', 'd4', 'e6',
                                 'f3', 'f4', 'g3', 'g4', 'h3', 'h4']))

    def test_get_rook_moves(self):
        """test 1"""
        position_1 = get_position_1(deepcopy(self.game_state))

        position_1_moves = []

        for row in range(len(position_1.board)):
            for column in range(len(position_1.board[row])):
                turn = position_1.board[row][column][0]
                if (turn == 'w' and position_1.white_to_move) or \
                        (turn == 'b' and not position_1.white_to_move):
                    piece = position_1.board[row][column][1]
                    if piece == 'R':
                        position_1.get_rook_moves(row, column, position_1_moves)

        self.assertEqual(sorted([str(move) for move in position_1_moves]),
                         sorted([]))

        """test 2"""
        position_2 = get_position_2(deepcopy(self.game_state))

        position_2_moves = []

        for row in range(len(position_2.board)):
            for column in range(len(position_2.board[row])):
                turn = position_2.board[row][column][0]
                if (turn == 'w' and position_2.white_to_move) or \
                        (turn == 'b' and not position_2.white_to_move):
                    piece = position_2.board[row][column][1]
                    if piece == 'R':
                        position_2.get_rook_moves(row, column, position_2_moves)

        self.assertEqual(sorted([str(move) for move in position_2_moves]),
                         sorted(['Ra2', 'Ra3', 'Rh2', 'Rh3']))

        """test 3"""
        position_3 = get_position_3(deepcopy(self.game_state))

        position_3_moves = []

        for row in range(len(position_3.board)):
            for column in range(len(position_3.board[row])):
                turn = position_3.board[row][column][0]
                if (turn == 'w' and position_3.white_to_move) or \
                        (turn == 'b' and not position_3.white_to_move):
                    piece = position_3.board[row][column][1]
                    if piece == 'R':
                        position_3.get_rook_moves(row, column, position_3_moves)

        self.assertEqual(sorted([str(move) for move in position_3_moves]),
                         sorted(['Rb8', 'Rf8', 'Rg8']))

        """test 4"""
        position_4 = get_position_4(deepcopy(self.game_state))

        position_4_moves = []

        for row in range(len(position_4.board)):
            for column in range(len(position_4.board[row])):
                turn = position_4.board[row][column][0]
                if (turn == 'w' and position_4.white_to_move) or \
                        (turn == 'b' and not position_4.white_to_move):
                    piece = position_4.board[row][column][1]
                    if piece == 'R':
                        position_4.get_rook_moves(row, column, position_4_moves)

        self.assertEqual(sorted([str(move) for move in position_4_moves]),
                         sorted([]))

        """test 5"""
        position_5 = get_position_5(deepcopy(self.game_state))

        position_5_moves = []

        for row in range(len(position_5.board)):
            for column in range(len(position_5.board[row])):
                turn = position_5.board[row][column][0]
                if (turn == 'w' and position_5.white_to_move) or \
                        (turn == 'b' and not position_5.white_to_move):
                    piece = position_5.board[row][column][1]
                    if piece == 'R':
                        position_5.get_rook_moves(row, column, position_4_moves)

        self.assertEqual(sorted([str(move) for move in position_5_moves]),
                         sorted([]))

        """test 6"""
        position_6 = get_position_6(deepcopy(self.game_state))

        position_6_moves = []

        for row in range(len(position_6.board)):
            for column in range(len(position_6.board[row])):
                turn = position_6.board[row][column][0]
                if (turn == 'w' and position_6.white_to_move) or \
                        (turn == 'b' and not position_6.white_to_move):
                    piece = position_6.board[row][column][1]
                    if piece == 'R':
                        position_6.get_rook_moves(row, column, position_6_moves)

        self.assertEqual(sorted([str(move) for move in position_6_moves]),
                         sorted([]))

        """test 7"""
        position_7 = get_position_7(deepcopy(self.game_state))

        position_7_moves = []

        for row in range(len(position_7.board)):
            for column in range(len(position_7.board[row])):
                turn = position_7.board[row][column][0]
                if (turn == 'w' and position_7.white_to_move) or \
                        (turn == 'b' and not position_7.white_to_move):
                    piece = position_7.board[row][column][1]
                    if piece == 'R':
                        position_7.get_rook_moves(row, column, position_7_moves)

        self.assertEqual(sorted([str(move) for move in position_7_moves]),
                         sorted(['Ra2']))

    def test_get_knight_moves(self):
        """test 1"""
        position_1 = get_position_1(deepcopy(self.game_state))

        position_1_moves = []

        for row in range(len(position_1.board)):
            for column in range(len(position_1.board[row])):
                turn = position_1.board[row][column][0]
                if (turn == 'w' and position_1.white_to_move) or \
                        (turn == 'b' and not position_1.white_to_move):
                    piece = position_1.board[row][column][1]
                    if piece == 'N':
                        position_1.get_knight_moves(row, column, position_1_moves)

        self.assertEqual(sorted([str(move) for move in position_1_moves]),
                         sorted(['Na3', 'Nc3', 'Nf3', 'Nh3']))

        """test 2"""
        position_2 = get_position_2(deepcopy(self.game_state))

        position_2_moves = []

        for row in range(len(position_2.board)):
            for column in range(len(position_2.board[row])):
                turn = position_2.board[row][column][0]
                if (turn == 'w' and position_2.white_to_move) or \
                        (turn == 'b' and not position_2.white_to_move):
                    piece = position_2.board[row][column][1]
                    if piece == 'N':
                        position_2.get_knight_moves(row, column, position_2_moves)

        self.assertEqual(sorted([str(move) for move in position_2_moves]),
                         sorted(['Na3', 'Nc3','Nxd2', 'Nxe2',  'Nf3', 'Nh3']))

        """test 3"""
        position_3 = get_position_3(deepcopy(self.game_state))

        position_3_moves = []

        for row in range(len(position_3.board)):
            for column in range(len(position_3.board[row])):
                turn = position_3.board[row][column][0]
                if (turn == 'w' and position_3.white_to_move) or \
                        (turn == 'b' and not position_3.white_to_move):
                    piece = position_3.board[row][column][1]
                    if piece == 'N':
                        position_3.get_knight_moves(row, column, position_3_moves)

        self.assertEqual(sorted([str(move) for move in position_3_moves]),
                         sorted(['Na5', 'Nb8', 'Nd4', 'Nd5', 'Ne7', 'Ng4', 'Ng8', 'Nh5', 'Nxe4']))

        """test 4"""
        position_4 = get_position_4(deepcopy(self.game_state))

        position_4_moves = []

        for row in range(len(position_4.board)):
            for column in range(len(position_4.board[row])):
                turn = position_4.board[row][column][0]
                if (turn == 'w' and position_4.white_to_move) or \
                        (turn == 'b' and not position_4.white_to_move):
                    piece = position_4.board[row][column][1]
                    if piece == 'N':
                        position_4.get_knight_moves(row, column, position_4_moves)

        self.assertEqual(sorted([str(move) for move in position_4_moves]),
                         sorted(['Na3', 'Nc3', 'Ne2', 'Nf3', 'Nh3']))

        """test 5"""
        position_5 = get_position_5(deepcopy(self.game_state))

        position_5_moves = []

        for row in range(len(position_5.board)):
            for column in range(len(position_5.board[row])):
                turn = position_5.board[row][column][0]
                if (turn == 'w' and position_5.white_to_move) or \
                        (turn == 'b' and not position_5.white_to_move):
                    piece = position_5.board[row][column][1]
                    if piece == 'N':
                        position_5.get_knight_moves(row, column, position_5_moves)

        self.assertEqual(sorted([str(move) for move in position_5_moves]),
                         sorted(['Na3', 'Nc3', 'Nd6', 'Nf5', 'Nf7', 'Ng8', 'Nxd4', 'Nxg4']))

        """test 6"""
        position_6 = get_position_6(deepcopy(self.game_state))

        position_6_moves = []

        for row in range(len(position_6.board)):
            for column in range(len(position_6.board[row])):
                turn = position_6.board[row][column][0]
                if (turn == 'w' and position_6.white_to_move) or \
                        (turn == 'b' and not position_6.white_to_move):
                    piece = position_6.board[row][column][1]
                    if piece == 'N':
                        position_6.get_knight_moves(row, column, position_6_moves)

        self.assertEqual(sorted([str(move) for move in position_6_moves]),
                         sorted(['Na3', 'Nc3', 'Ne2', 'Nf3', 'Nh3']))

        """test 7"""
        position_7 = get_position_7(deepcopy(self.game_state))

        position_7_moves = []

        for row in range(len(position_7.board)):
            for column in range(len(position_7.board[row])):
                turn = position_7.board[row][column][0]
                if (turn == 'w' and position_7.white_to_move) or \
                        (turn == 'b' and not position_7.white_to_move):
                    piece = position_7.board[row][column][1]
                    if piece == 'N':
                        position_7.get_knight_moves(row, column, position_7_moves)

        self.assertEqual(sorted([str(move) for move in position_7_moves]),
                         sorted(['Nc3', 'Ne2', 'Nf3', 'Nh3']))

    def test_get_bishop_moves(self):
        """test 1"""
        position_1 = get_position_1(deepcopy(self.game_state))

        position_1_moves = []

        for row in range(len(position_1.board)):
            for column in range(len(position_1.board[row])):
                turn = position_1.board[row][column][0]
                if (turn == 'w' and position_1.white_to_move) or \
                        (turn == 'b' and not position_1.white_to_move):
                    piece = position_1.board[row][column][1]
                    if piece == 'B':
                        position_1.get_bishop_moves(row, column, position_1_moves)

        self.assertEqual(sorted([str(move) for move in position_1_moves]),
                         sorted([]))

        """test 2"""
        position_2 = get_position_2(deepcopy(self.game_state))

        position_2_moves = []

        for row in range(len(position_2.board)):
            for column in range(len(position_2.board[row])):
                turn = position_2.board[row][column][0]
                if (turn == 'w' and position_2.white_to_move) or \
                        (turn == 'b' and not position_2.white_to_move):
                    piece = position_2.board[row][column][1]
                    if piece == 'B':
                        position_2.get_bishop_moves(row, column, position_2_moves)

        self.assertEqual(sorted([str(move) for move in position_2_moves]),
                         sorted(['Bxd2', 'Bxe2']))

        """test 3"""
        position_3 = get_position_3(deepcopy(self.game_state))

        position_3_moves = []

        for row in range(len(position_3.board)):
            for column in range(len(position_3.board[row])):
                turn = position_3.board[row][column][0]
                if (turn == 'w' and position_3.white_to_move) or \
                        (turn == 'b' and not position_3.white_to_move):
                    piece = position_3.board[row][column][1]
                    if piece == 'B':
                        position_3.get_bishop_moves(row, column, position_3_moves)

        self.assertEqual(sorted([str(move) for move in position_3_moves]),
                         sorted(['Ba3', 'Ba5', 'Bc3', 'Bc5', 'Bd6', 'Be7', 'Bf8', 'Bxd2']))

        """test 4"""
        position_4 = get_position_4(deepcopy(self.game_state))

        position_4_moves = []

        for row in range(len(position_4.board)):
            for column in range(len(position_4.board[row])):
                turn = position_4.board[row][column][0]
                if (turn == 'w' and position_4.white_to_move) or \
                        (turn == 'b' and not position_4.white_to_move):
                    piece = position_4.board[row][column][1]
                    if piece == 'B':
                        position_4.get_bishop_moves(row, column, position_4_moves)

        self.assertEqual(sorted([str(move) for move in position_4_moves]),
                         sorted(['Bc4', 'Bd3', 'Be2', 'Bxb5']))

        """test 5"""
        position_5 = get_position_5(deepcopy(self.game_state))

        position_5_moves = []

        for row in range(len(position_5.board)):
            for column in range(len(position_5.board[row])):
                turn = position_5.board[row][column][0]
                if (turn == 'w' and position_5.white_to_move) or \
                        (turn == 'b' and not position_5.white_to_move):
                    piece = position_5.board[row][column][1]
                    if piece == 'B':
                        position_5.get_bishop_moves(row, column, position_5_moves)

        self.assertEqual(sorted([str(move) for move in position_5_moves]),
                         sorted([]))

        """test 6"""
        position_6 = get_position_6(deepcopy(self.game_state))

        position_6_moves = []

        for row in range(len(position_6.board)):
            for column in range(len(position_6.board[row])):
                turn = position_6.board[row][column][0]
                if (turn == 'w' and position_6.white_to_move) or \
                        (turn == 'b' and not position_6.white_to_move):
                    piece = position_6.board[row][column][1]
                    if piece == 'B':
                        position_6.get_bishop_moves(row, column, position_6_moves)

        self.assertEqual(sorted([str(move) for move in position_6_moves]),
                         sorted(['Ba6', 'Bb5', 'Bc4', 'Bd3', 'Be2']))

        """test 7"""
        position_7 = get_position_7(deepcopy(self.game_state))

        position_7_moves = []

        for row in range(len(position_7.board)):
            for column in range(len(position_7.board[row])):
                turn = position_7.board[row][column][0]
                if (turn == 'w' and position_7.white_to_move) or \
                        (turn == 'b' and not position_7.white_to_move):
                    piece = position_7.board[row][column][1]
                    if piece == 'B':
                        position_7.get_bishop_moves(row, column, position_7_moves)

        self.assertEqual(sorted([str(move) for move in position_7_moves]),
                         sorted(['Bxa6', 'Bb5', 'Bc4', 'Bd3', 'Be2']))

    def test_get_queen_moves(self):
        """test 1"""
        position_1 = get_position_1(deepcopy(self.game_state))

        position_1_moves = []

        for row in range(len(position_1.board)):
            for column in range(len(position_1.board[row])):
                turn = position_1.board[row][column][0]
                if (turn == 'w' and position_1.white_to_move) or \
                        (turn == 'b' and not position_1.white_to_move):
                    piece = position_1.board[row][column][1]
                    if piece == 'Q':
                        position_1.get_queen_moves(row, column, position_1_moves)

        self.assertEqual(sorted([str(move) for move in position_1_moves]),
                         sorted([]))

        """test 2"""
        position_2 = get_position_2(deepcopy(self.game_state))

        position_2_moves = []

        for row in range(len(position_2.board)):
            for column in range(len(position_2.board[row])):
                turn = position_2.board[row][column][0]
                if (turn == 'w' and position_2.white_to_move) or \
                        (turn == 'b' and not position_2.white_to_move):
                    piece = position_2.board[row][column][1]
                    if piece == 'Q':
                        position_2.get_queen_moves(row, column, position_2_moves)

        self.assertEqual(sorted([str(move) for move in position_2_moves]),
                         sorted(['Qxd2', 'Qxe2']))

        """test 3"""
        position_3 = get_position_3(deepcopy(self.game_state))

        position_3_moves = []

        for row in range(len(position_3.board)):
            for column in range(len(position_3.board[row])):
                turn = position_3.board[row][column][0]
                if (turn == 'w' and position_3.white_to_move) or \
                        (turn == 'b' and not position_3.white_to_move):
                    piece = position_3.board[row][column][1]
                    if piece == 'Q':
                        position_3.get_queen_moves(row, column, position_3_moves)

        self.assertEqual(sorted([str(move) for move in position_3_moves]),
                         sorted(['Qe7']))

        """test 4"""
        position_4 = get_position_4(deepcopy(self.game_state))

        position_4_moves = []

        for row in range(len(position_4.board)):
            for column in range(len(position_4.board[row])):
                turn = position_4.board[row][column][0]
                if (turn == 'w' and position_4.white_to_move) or \
                        (turn == 'b' and not position_4.white_to_move):
                    piece = position_4.board[row][column][1]
                    if piece == 'Q':
                        position_4.get_queen_moves(row, column, position_4_moves)

        self.assertEqual(sorted([str(move) for move in position_4_moves]),
                         sorted(['Qd1', 'Qe2', 'Qf3', 'Qf4', 'Qg3', 'Qg5', 'Qg6', 'Qh3', 'Qh4', 'Qh5', 'Qxf5', 'Qxg7']))

        """test 5"""
        position_5 = get_position_5(deepcopy(self.game_state))

        position_5_moves = []

        for row in range(len(position_5.board)):
            for column in range(len(position_5.board[row])):
                turn = position_5.board[row][column][0]
                if (turn == 'w' and position_5.white_to_move) or \
                        (turn == 'b' and not position_5.white_to_move):
                    piece = position_5.board[row][column][1]
                    if piece == 'Q':
                        position_5.get_queen_moves(row, column, position_5_moves)

        self.assertEqual(sorted([str(move) for move in position_5_moves]),
                         sorted(['Qc6', 'Qc8', 'Qd6', 'Qd8', 'Qe6', 'Qe8', 'Qf5', 'Qxg4']))

        """test 6"""
        position_6 = get_position_6(deepcopy(self.game_state))

        position_6_moves = []

        for row in range(len(position_6.board)):
            for column in range(len(position_6.board[row])):
                turn = position_6.board[row][column][0]
                if (turn == 'w' and position_6.white_to_move) or \
                        (turn == 'b' and not position_6.white_to_move):
                    piece = position_6.board[row][column][1]
                    if piece == 'Q':
                        position_6.get_queen_moves(row, column, position_6_moves)

        self.assertEqual(sorted([str(move) for move in position_6_moves]),
                         sorted(['Qe2', 'Qf3', 'Qg4', 'Qh5']))

        """test 7"""
        position_7 = get_position_7(deepcopy(self.game_state))

        position_7_moves = []

        for row in range(len(position_7.board)):
            for column in range(len(position_7.board[row])):
                turn = position_7.board[row][column][0]
                if (turn == 'w' and position_7.white_to_move) or \
                        (turn == 'b' and not position_7.white_to_move):
                    piece = position_7.board[row][column][1]
                    if piece == 'Q':
                        position_7.get_queen_moves(row, column, position_7_moves)

        self.assertEqual(sorted([str(move) for move in position_7_moves]),
                         sorted(['Qe2', 'Qf3', 'Qg4', 'Qh5']))

    def test_get_king_moves(self):
        """test 1"""
        position_1 = get_position_1(deepcopy(self.game_state))

        position_1_moves = []

        for row in range(len(position_1.board)):
            for column in range(len(position_1.board[row])):
                turn = position_1.board[row][column][0]
                if (turn == 'w' and position_1.white_to_move) or \
                        (turn == 'b' and not position_1.white_to_move):
                    piece = position_1.board[row][column][1]
                    if piece == 'K':
                        position_1.get_king_moves(row, column, position_1_moves)

        self.assertEqual(sorted([str(move) for move in position_1_moves]),
                         sorted([]))

        """test 2"""
        position_2 = get_position_2(deepcopy(self.game_state))

        position_2_moves = []

        for row in range(len(position_2.board)):
            for column in range(len(position_2.board[row])):
                turn = position_2.board[row][column][0]
                if (turn == 'w' and position_2.white_to_move) or \
                        (turn == 'b' and not position_2.white_to_move):
                    piece = position_2.board[row][column][1]
                    if piece == 'K':
                        position_2.get_king_moves(row, column, position_2_moves)

        self.assertEqual(sorted([str(move) for move in position_2_moves]),
                         sorted(['Kxd2', 'Kxe2']))

        """test 3"""
        position_3 = get_position_3(deepcopy(self.game_state))

        position_3_moves = []

        for row in range(len(position_3.board)):
            for column in range(len(position_3.board[row])):
                turn = position_3.board[row][column][0]
                if (turn == 'w' and position_3.white_to_move) or \
                        (turn == 'b' and not position_3.white_to_move):
                    piece = position_3.board[row][column][1]
                    if piece == 'K':
                        position_3.get_king_moves(row, column, position_3_moves)

        self.assertEqual(sorted([str(move) for move in position_3_moves]),
                         sorted(['Ke7', 'Kf8']))

        """test 4"""
        position_4 = get_position_4(deepcopy(self.game_state))

        position_4_moves = []

        for row in range(len(position_4.board)):
            for column in range(len(position_4.board[row])):
                turn = position_4.board[row][column][0]
                if (turn == 'w' and position_4.white_to_move) or \
                        (turn == 'b' and not position_4.white_to_move):
                    piece = position_4.board[row][column][1]
                    if piece == 'K':
                        position_4.get_king_moves(row, column, position_4_moves)

        self.assertEqual(sorted([str(move) for move in position_4_moves]),
                         sorted(['Kd1', 'Ke2']))

        """test 5"""
        position_5 = get_position_5(deepcopy(self.game_state))

        position_5_moves = []

        for row in range(len(position_5.board)):
            for column in range(len(position_5.board[row])):
                turn = position_5.board[row][column][0]
                if (turn == 'w' and position_5.white_to_move) or \
                        (turn == 'b' and not position_5.white_to_move):
                    piece = position_5.board[row][column][1]
                    if piece == 'K':
                        position_5.get_king_moves(row, column, position_5_moves)

        self.assertEqual(sorted([str(move) for move in position_5_moves]),
                         sorted(['Kc6', 'Kd6', 'Ke5', 'Ke6', 'Kxc4', 'Kxc5', 'Kxd4', 'Kxe4']))

        """test 6"""
        position_6 = get_position_6(deepcopy(self.game_state))

        position_6_moves = []

        for row in range(len(position_6.board)):
            for column in range(len(position_6.board[row])):
                turn = position_6.board[row][column][0]
                if (turn == 'w' and position_6.white_to_move) or \
                        (turn == 'b' and not position_6.white_to_move):
                    piece = position_6.board[row][column][1]
                    if piece == 'K':
                        position_6.get_king_moves(row, column, position_6_moves)

        self.assertEqual(sorted([str(move) for move in position_6_moves]),
                         sorted(['Ke2']))

        """test 7"""
        position_7 = get_position_7(deepcopy(self.game_state))

        position_7_moves = []

        for row in range(len(position_7.board)):
            for column in range(len(position_7.board[row])):
                turn = position_7.board[row][column][0]
                if (turn == 'w' and position_7.white_to_move) or \
                        (turn == 'b' and not position_7.white_to_move):
                    piece = position_7.board[row][column][1]
                    if piece == 'K':
                        position_7.get_king_moves(row, column, position_7_moves)

        self.assertEqual(sorted([str(move) for move in position_7_moves]),
                         sorted(['Ke2']))

    def test_get_all_possible_moves(self):
        """test 1"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_1(deepcopy(self.game_state)).get_all_possible_moves()]),
                         sorted(["a3", "a4", "b3", "b4", "c3", "c4", "d3", "d4", "e3", "e4", "f3", "f4", "g3", "g4",
                                 "h3", "h4", "Na3", "Nc3", "Nf3", "Nh3"]))

        """test 2"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_2(deepcopy(self.game_state)).get_all_possible_moves()]),
                         sorted(['Bxd2', 'Bxe2', 'Kxd2', 'Kxe2', 'Na3', 'Nc3', 'Nf3', 'Nh3', 'Nxd2', 'Nxe2',
                                 'Qxd2', 'Qxe2', 'Ra2', 'Ra3', 'Rh2', 'Rh3', 'a5', 'b3', 'b4', 'c3', 'c4',
                                 'f3', 'f4', 'g3', 'g4', 'h5']))

        """test 3"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_3(deepcopy(self.game_state)).get_all_possible_moves()]),
                         sorted(['Rb8', 'Qe7', 'Kf8', 'Ke7', 'Rg8', 'Rf8', 'b6', 'b5', 'bxa6', 'd6', 'd5', 'g6',
                                 'g5', 'h6', 'h5', 'Nb8', 'Ne7', 'Na5', 'Nd4', 'Ng8', 'Nd5', 'Nh5', 'Nxe4', 'Ng4',
                                 'Ba5', 'Ba3', 'Bc3', 'Bxd2', 'Bc5', 'Bd6', 'Be7', 'Bf8']))

        """test 4"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_4(deepcopy(self.game_state)).get_all_possible_moves()]),
                         sorted(['Bc4', 'Bd3', 'Be2', 'Bxb5', 'Kd1', 'Ke2', 'Na3', 'Nc3', 'Ne2', 'Nf3', 'Nh3',
                                 'Qd1', 'Qe2', 'Qf3', 'Qf4', 'Qg3', 'Qg5', 'Qg6', 'Qh3', 'Qh4', 'Qh5', 'Qxf5',
                                 'Qxg7', 'a3', 'a4', 'b3', 'b4', 'bxa8', 'bxc8', 'd3', 'd4', 'exf5', 'f3',
                                 'f4', 'g3', 'h3', 'h4']))

        """test 5"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_5(deepcopy(self.game_state)).get_all_possible_moves()]),
                         sorted(['Ra8', 'Rb7', 'Rb6', 'Rc8', 'Rd8', 'Re8', 'Rg8', 'Rh7', 'c6', 'Qc8', 'Qc6',
                                  'Qe6', 'Qf5', 'Qxg4', 'Qe8', 'Qd8', 'Qd6', 'e6', 'e5', 'exf6', 'gxf6', 'g5',
                                  'gxh5', 'Ng8', 'Nf7', 'Nf5', 'Nxg4', 'Nd6', 'Nxd4', 'Na3', 'Nc3', 'Ke5',
                                  'Kxe4', 'Kxd4', 'Kxc4', 'Kxc5', 'Kc6', 'Kd6', 'Ke6']))

        """test 6"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_6(deepcopy(self.game_state)).get_all_possible_moves()]),
                         sorted(['e6', 'exf6', 'a3', 'a4', 'b3', 'b4', 'c3', 'c4', 'd3', 'd4', 'f3', 'f4', 'g3',
                                 'g4', 'h3', 'h4', 'Na3', 'Nc3', 'Qe2', 'Qf3', 'Qg4', 'Qh5', 'Ke2', 'Be2', 'Bd3',
                                 'Bc4', 'Bb5', 'Ba6', 'Nf3', 'Nh3', 'Ne2']))

        """test 7"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_7(deepcopy(self.game_state)).get_all_possible_moves()]),
                         sorted(['e6', 'a4', 'b3', 'b4', 'c3', 'c4', 'd3', 'd4', 'f3', 'f4', 'g3', 'g4', 'h3',
                                 'h4', 'Ra2', 'Nc3', 'Qe2', 'Qf3', 'Qg4', 'Qh5', 'Ke2', 'Be2', 'Bd3', 'Bc4',
                                 'Bb5', 'Bxa6', 'Nf3', 'Nh3', 'Ne2']))

    def test_get_valid_moves(self):
        """test 1"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_1(deepcopy(self.game_state)).get_valid_moves()]),
                         sorted(["a3", "a4", "b3", "b4", "c3", "c4", "d3", "d4", "e3", "e4", "f3", "f4", "g3", "g4",
                                 "h3", "h4", "Na3", "Nc3", "Nf3", "Nh3"]))

        """test 2"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_2(deepcopy(self.game_state)).get_valid_moves()]),
                         sorted([]))

        """test 3"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_3(deepcopy(self.game_state)).get_valid_moves()]),
                         sorted(['b6', 'b5', 'bxa6', 'd6', 'd5', 'g6', 'g5', 'h6', 'h5', 'Nb8', 'Ne7', 'Na5', 'Nd4',
                                 'Ng8', 'Nd5', 'Nh5', 'Nxe4', 'Ng4', 'Ba5', 'Ba3', 'Bc3', 'Bxd2', 'Bc5', 'Bd6', 'Be7',
                                 'Bf8', 'Rb8', 'Qe7', 'Kf8', 'Ke7', 'Rg8', 'Rf8', 'O-O']))

        """test 4"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_4(deepcopy(self.game_state)).get_valid_moves()]),
                         sorted(['Kd1', 'Ke2', 'Na3', 'Nc3', 'Ne2', 'Nf3', 'Nh3', 'Qd1', 'Qe2', 'Qf3',
                                 'Qf4', 'Qg3', 'Qg5', 'Qg6', 'Qh3', 'Qh4', 'Qh5', 'Qxf5', 'Qxg7', 'a3', 'a4',
                                 'b3', 'b4', 'bxa8', 'bxc8', 'd3', 'd4', 'exf5', 'f3', 'f4', 'g3',
                                 'h3', 'h4', 'Bc4', 'Bd3', 'Be2', 'Bxb5']))

        """test 5"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_5(deepcopy(self.game_state)).get_valid_moves()]),
                         sorted([]))

        """test 6"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_6(deepcopy(self.game_state)).get_valid_moves()]),
                         sorted(['e6', 'exf6', 'a3', 'a4', 'b3', 'b4', 'c3', 'c4', 'd3', 'd4', 'f3', 'f4', 'g3',
                                 'g4', 'h3', 'h4', 'Na3', 'Nc3', 'Qe2', 'Qf3', 'Qg4', 'Qh5', 'Ke2', 'Be2', 'Bd3',
                                 'Bc4', 'Bb5', 'Ba6', 'Nf3', 'Nh3', 'Ne2']))

        """test 7"""
        self.assertEqual(sorted([str(move) for move in
                                 get_position_7(deepcopy(self.game_state)).get_valid_moves()]),
                         sorted(['e6', 'a4', 'b3', 'b4', 'c3', 'c4', 'd3', 'd4', 'f3', 'f4', 'g3', 'g4', 'h3',
                                 'h4', 'Ra2', 'Nc3', 'Qe2', 'Qf3', 'Qg4', 'Qh5', 'Ke2', 'Be2', 'Bd3', 'Bc4',
                                 'Bb5', 'Bxa6', 'Nf3', 'Nh3', 'Ne2']))


unittest.main()
