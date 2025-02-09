"""
Tic Tac Toe Player
"""

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
    move_count = 0
    for list in board:
        for move in list:
            if move:
                move_count += 1
    if move_count % 2 == 0:
        return X
    else:
        return O


def actions(board):
    actions_set = set()
    for i in range(3):
        for j in range(3):
            if not board[i][j]:
                actions_set.add((i, j))
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid move")
    copy_board = copy.deepcopy(board)
    i, j = action[0], action[1]
    copy_board[i][j] = player(board)
    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0]:
            return board[i][0]
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i]:
            return board[0][i]
    if board[0][0] == board[1][1] == board [2][2] and board[0][0]:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                return False
    return True



def utility(board):
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
    if player(board) == X:
        best_value = float('-inf')
        best_move = None
        for action in actions(board):
            move_value = minimax_value(result(board, action))
            if move_value > best_value:
                best_value = move_value
                best_move = action
    if player(board) == O:
        best_value = float('inf')
        best_move = None
        for action in actions(board):
            move_value = minimax_value(result(board, action))
            if move_value < best_value:
                best_value = move_value
                best_move = action
    return best_move

def minimax_value(board):
    if terminal(board):
        return utility(board)
    if player(board) == X:
        return max(minimax_value(result(board, action)) for action in actions(board))
    if player(board) == O:
        return min(minimax_value(result(board, action)) for action in actions(board))
