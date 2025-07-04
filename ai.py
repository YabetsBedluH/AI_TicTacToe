from game_state import board, check_win, is_board_full, mark_square
from config import board_rows, board_cols
import numpy as np

def minimax_ab(minimax_board, depth, is_maximizing, alpha, beta):
    if check_win(2, minimax_board):
        return float('inf') - depth
    elif check_win(1, minimax_board):
        return float('-inf') + depth
    elif is_board_full(minimax_board):
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for row in range(board_rows):
            for col in range(board_cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    eval = minimax_ab(minimax_board, depth + 1, False, alpha, beta)
                    minimax_board[row][col] = 0
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for row in range(board_rows):
            for col in range(board_cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    eval = minimax_ab(minimax_board, depth + 1, True, alpha, beta)
                    minimax_board[row][col] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move():
    best_score = float('-inf')
    move = (-1, -1)
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax_ab(board, 0, False, float('-inf'), float('inf'))
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False
