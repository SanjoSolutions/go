from enum import IntEnum

NUMBER_OF_ROWS = 3
NUMBER_OF_COLUMNS = 3
KOMI = 6.5


class Player(IntEnum):
    Black = 1
    White = 2


class PositionState(IntEnum):
    Empty = 0
    Black = 1
    White = 2


class Result(IntEnum):
    Draw = 0
    Black = 1
    White = 2


class Go:
    @staticmethod
    def create_new_game():
        board = [None] * NUMBER_OF_ROWS
        for row in range(NUMBER_OF_ROWS):
            board[row] = [PositionState.Empty] * NUMBER_OF_COLUMNS
        prisoners = [0, 0]
        current_player = Player.White
        can_place = [None] * NUMBER_OF_ROWS
        for row in range(NUMBER_OF_ROWS):
            can_place[row] = [True] * NUMBER_OF_COLUMNS
        return Go(board, prisoners, current_player, can_place)

    def __init__(self, board, prisoners, current_player, can_place):
        self.board = board
        self.prisoners = prisoners
        self.current_player = current_player
        self._can_place = can_place

    def reset(self):
        return Go.create_new_game()

    def step(self, action):
        position = action

        row, column = position
        if row is None:
            raise ValueError('column ' + str(column) + ' is full.')
        board = copy_board(self.board)
        board[row][column] = self.current_player
        can_place = copy_board(self._can_place)
        can_place[row][column] = False

        board, new_prisoners = self._remove_captured_stones_by_move(board, position)
        prisoners = self.prisoners.copy()
        for index in range(len(prisoners)):
            prisoners[index] += new_prisoners[index]

        next_player = determine_next_player(self.current_player)

        return Go(board, prisoners, next_player, can_place)

    def _remove_captured_stones(self, board):
        prisoners = [0, 0]
        board = copy_board(board)
        number_of_rows = len(board)
        number_of_columns = len(board[0])
        for row in range(0, number_of_rows):
            for column in range(0, number_of_columns):
                position = (row, column)
                value = board[row][column]
                if value is not PositionState.Empty:
                    surrounded_by = determine_surrounded_by(board, position)
                    if (
                        (value == PositionState.Black and surrounded_by == Player.White) or
                        (value == PositionState.White and surrounded_by == Player.Black)
                    ):
                        board[row][column] = PositionState.Empty
                        prisoners[int(surrounded_by) - 1] += 1
        return board, prisoners

    def _remove_captured_stones_by_move(self, board, move):
        prisoners = [0, 0]
        board = copy_board(board)
        number_of_rows = len(board)
        number_of_columns = len(board[0])
        for row in range(0, number_of_rows):
            for column in range(0, number_of_columns):
                position = (row, column)
                value = board[row][column]
                if value is not PositionState.Empty:
                    surrounded_by = determine_surrounded_by_by_move(board, position, move)
                    if (
                        (value == PositionState.Black and surrounded_by == Player.White) or
                        (value == PositionState.White and surrounded_by == Player.Black)
                    ):
                        board[row][column] = PositionState.Empty
                        prisoners[int(surrounded_by) - 1] += 1
        return board, prisoners

    def determine_reward(self, player):
        result = self.determine_result()
        if result == player:
            reward = 1.0
        elif result == determine_other_player(player):
            reward = -1.0
        elif result == Result.Draw:
            reward = 0.5
        else:
            reward = 0.0
        return reward

    def is_done(self):
        for row in range(0, NUMBER_OF_ROWS):
            for column in range(0, NUMBER_OF_COLUMNS):
                if self._can_place[row][column]:
                    return False
        return True

    def _get_state(self):
        return self.board

    def determine_available_actions(self):
        positions = []
        for row in range(0, NUMBER_OF_ROWS):
            for column in range(0, NUMBER_OF_COLUMNS):
                if self._can_place[row][column]:
                    position = (row, column)
                    positions.append(position)

        return positions

    def determine_result(self):
        board = self.board
        prisoners = self.prisoners

        points = list(prisoners)
        points[1] += KOMI

        number_of_rows = len(board)
        number_of_columns = len(board[0])
        for row in range(0, number_of_rows):
            for column in range(0, number_of_columns):
                position = (row, column)
                surrounded_by = determine_surrounded_by(board, position)
                if surrounded_by == Player.Black:
                    points[0] += 1
                elif surrounded_by == Player.White:
                    points[1] += 1

        if points[0] == points[1]:
            return Result.Draw
        elif points[0] > points[1]:
            return Result.Black
        elif points[1] > points[0]:
            return Result.White

    def _next_player(self):
        self.current_player = determine_next_player(self.current_player)


def determine_next_player(player):
    return Player((player % len(Player)) + 1)


def determine_previous_player(player):
    return determine_next_player(player)


def determine_other_player(player):
    return determine_next_player(player)


def is_surrounded(board, position):
    return determine_surrounded_by(board, position) is not None


def determine_surrounded_by(board, position):
    number_of_rows = len(board)
    number_of_columns = len(board[0])
    for player in Player:
        for from_row in range(-1, number_of_rows):
            for from_column in range(-1, number_of_columns):
                for height in range(3, number_of_rows - from_row + 1):
                    for width in range(3, number_of_columns - from_column + 1):
                        area = (from_row, from_column, width, height)
                        if is_surrounded_by_area(board, position, player, area):
                            return player
    return None


def determine_surrounded_by_by_move(board, position, move):
    number_of_rows = len(board)
    number_of_columns = len(board[0])
    for player in Player:
        for from_row in range(-1, number_of_rows):
            for from_column in range(-1, number_of_columns):
                for height in range(3, number_of_rows - from_row + 1):
                    for width in range(3, number_of_columns - from_column + 1):
                        area = (from_row, from_column, width, height)
                        if is_position_in_area(position, area):
                            if is_surrounded_by_area(board, position, player, area):
                                return player
    return None


def is_position_in_area(position, area):
    row, column = position
    from_row, from_column, width, height = area
    return (
        from_row <= row <= from_row + width - 1 and
        from_column <= column <= from_column + height - 1
    )


def is_surrounded_by_area(board, position, player, area):
    from_row, from_column, width, height = area

    row, column = position
    if not (
        from_row < row < from_row + height - 1 and
        from_column < column < from_column + width - 1
    ):
        return False

    surrounder_positions = []

    row = from_row
    if row >= 0:
        for column in range(from_column + 1, from_column + width - 1):
            surrounder_positions.append((row, column))

    column = from_column + width - 1
    if column <= NUMBER_OF_COLUMNS - 1:
        for row in range(from_row + 1, from_row + height - 1):
            surrounder_positions.append((row, column))

    row = from_row + height - 1
    if row <= NUMBER_OF_ROWS - 1:
        for column in range(from_column + 1, from_column + width - 1):
            surrounder_positions.append((row, column))

    column = from_column
    if column >= 0:
        for row in range(from_row + 1, from_row + height - 1):
            surrounder_positions.append((row, column))

    return all(
        board[position[0]][position[1]] == player
        for position
        in surrounder_positions
    )


def is_board_full(board):
    for row in range(0, NUMBER_OF_ROWS):
        for column in range(0, NUMBER_OF_COLUMNS):
            if board[row][column] == PositionState.Empty:
                return False
    return True


def copy_board(board):
    board = board.copy()
    for row in range(0, len(board)):
        board[row] = board[row].copy()
    return board


def print_state(state):
    for row in state.board:
        print([cell.value for cell in row])
    print('')
