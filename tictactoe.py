import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    if board == initial_state():
        return X
    else:
        for i in range(3):
            for j in range(3):
                if board[i][j] == X:
                    x_count += 1
                elif board[i][j] == O:
                    o_count += 1
        if x_count > o_count:
            return O
        else:
            return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                moves.add((row, col))
    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    my_board = copy.deepcopy(board)
    i, j = action
    if my_board[i][j] != EMPTY:
        raise NameError("Invalid Move!")
    else:
        if player(my_board) == X:
            my_board[i][j] = X
        else:
            my_board[i][j] = O
    return my_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # Check rows and columns
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        elif board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(board[i][j] != EMPTY for i in range(3) for j in range(3))

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)
    if current_player == X:
        best_value = -math.inf
        best_move = None
        for move in actions(board):
            value = min_value(result(board, move), -math.inf, math.inf)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move
    else:
        best_value = math.inf
        best_move = None
        for move in actions(board):
            value = max_value(result(board, move), -math.inf, math.inf)
            if value < best_value:
                best_value = value
                best_move = move
        return best_move

def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = -math.inf
    for move in actions(board):
        v = max(v, min_value(result(board, move), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break  # Beta cut-off
    return v

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = math.inf
    for move in actions(board):
        v = min(v, max_value(result(board, move), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break  # Alpha cut-off
    return v