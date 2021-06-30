import unittest

from main import determine_surrounded_by, Player, PositionState


E = PositionState.Empty
W = PositionState.Black
B = PositionState.White


class TestDetermineSurroundedBy(unittest.TestCase):
    def test_get_surrounded_by_white(self):
        board = [
            [E, W],
            [W, E]
        ]
        position = (0, 0)
        self.assertEqual(
            Player.Black,
            determine_surrounded_by(board, position)
        )

    def test_get_surrounded_by_black(self):
        board = [
            [E, B],
            [B, E]
        ]
        position = (0, 0)
        self.assertEqual(
            Player.White,
            determine_surrounded_by(board, position)
        )

    def test_get_surrounded_by_white_2(self):
        board = [
            [E, W, E],
            [W, E, W],
            [E, W, E]
        ]
        position = (1, 1)
        self.assertEqual(
            Player.Black,
            determine_surrounded_by(board, position)
        )

    def test_get_surrounded_by_white_3(self):
        board = [
            [E, W, W, E],
            [W, E, E, W],
            [E, W, W, E]
        ]
        position = (1, 1)
        self.assertEqual(
            Player.Black,
            determine_surrounded_by(board, position)
        )

    def test_get_surrounded_by_white_4(self):
        board = [
            [E, W, W, E],
            [W, E, E, W],
            [W, E, E, W],
            [E, W, W, E]
        ]
        position = (1, 1)
        self.assertEqual(
            Player.Black,
            determine_surrounded_by(board, position)
        )

    def test_get_surrounded_by_none(self):
        board = [
            [E, E],
            [E, E]
        ]
        position = (0, 0)
        self.assertEqual(
            None,
            determine_surrounded_by(board, position)
        )

    def test_get_surrounded_by_none_2(self):
        board = [
            [W, B],
            [E, E]
        ]
        position = (0, 0)
        self.assertEqual(
            None,
            determine_surrounded_by(board, position)
        )


if __name__ == '__main__':
    unittest.main()
