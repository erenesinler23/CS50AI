import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns the initial state of the Tic-Tac-Toe board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns the player (X or O) who has the next turn on the board.
    """
    X_count = sum(row.count(X) for row in board)
    O_count = sum(row.count(O) for row in board)

    if X_count <= O_count:
        return X
    else:
        return O

def actions(board):
    """
    Returns a set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()

    for row_index, row in enumerate(board):
        for column_index, item in enumerate(row):
            if item is None:
                possible_moves.add((row_index, column_index))

    return possible_moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_move = player(board)

    new_board = deepcopy(board)
    i, j = action

    if board[i][j] is not None:
        raise Exception("Invalid action")
    else:
        new_board[i][j] = player_move

    return new_board

def winner(board):
    """
    Returns the winner of the game (X, O) if there is one, otherwise, returns None.
    """
    for player in (X, O):
        # Check vertical and horizontal
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
                return player

        # Check diagonals
        if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
            return player

    return None

def terminal(board):
    """
    Returns True if the game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        if EMPTY in row:
            return False

    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 for a tie.
    """
    win_player = winner(board)

    if win_player == X:
        return 1
    elif win_player == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board using the minimax algorithm.
    """
    def max_value(board):
        optimal_move = ()
        if terminal(board):
            return utility(board), optimal_move
        else:
            v = -math.inf
            for action in actions(board):
                min_val = min_value(result(board, action))[0]
                if min_val > v:
                    v = min_val
                    optimal_move = action
            return v, optimal_move

    def min_value(board):
        optimal_move = ()
        if terminal(board):
            return utility(board), optimal_move
        else:
            v = math.inf
            for action in actions(board):
                max_val = max_value(result(board, action))[0]
                if max_val < v:
                    v = max_val
                    optimal_move = action
            return v, optimal_move

    curr_player = player(board)

    if terminal(board):
        return None

    if curr_player == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]