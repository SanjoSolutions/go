import unittest

from main import Go, Player, PositionState


class TestGo(unittest.TestCase):
    def test_1(self):
        board = [
            [0, 0, 2],
            [1, 2, 2],
            [1, 1, 0]
        ]
        prisoners = [0, 0]
        current_player = Player.Black
        can_place = generate_can_place(board)
        state = Go(board, prisoners, current_player, can_place)
        state = state.step((0, 1))
        self.assertEqual(
            [
                [0, 1, 2],
                [1, 2, 2],
                [1, 1, 0]
            ],
            state.board
        )


def generate_can_place(board):
    number_of_rows = len(board)
    number_of_columns = len(board[0])
    can_place = create_2d_array(number_of_columns, number_of_rows)
    for row in range(number_of_rows):
        for column in range(number_of_columns):
            can_place[row][column] = True if board[row][column] == PositionState.Empty else False
    return can_place


def create_2d_array(width, height, default_value=None):
    array = [None] * height
    for row in range(len(array)):
        array[row] = [default_value] * width
    return array
