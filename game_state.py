import numpy as np
from config import board_rows, board_cols, board_size, button_area, square_size, width

board = np.zeros((board_rows, board_cols))

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=board):
    return not np.any(check_board == 0)

def get_winning_line(player, check_board=board):
    for col in range(board_cols):
        if np.all(check_board[:, col] == player):
            start = (col * square_size + square_size // 2, button_area)
            end = (col * square_size + square_size // 2, button_area + board_size)
            return (start, end)
    for row in range(board_rows):
        if np.all(check_board[row, :] == player):
            start = (0, button_area + row * square_size + square_size // 2)
            end = (width, button_area + row * square_size + square_size // 2)
            return (start, end)
    if check_board[0][0] == check_board[1][1] == check_board[2][2] == player:
        return ((0, button_area), (width, button_area + board_size))
    if check_board[0][2] == check_board[1][1] == check_board[2][0] == player:
        return ((width, button_area), (0, button_area + board_size))
    return None

def check_win(player, check_board=board):
    return get_winning_line(player, check_board) is not None

def reset_board():
    global board
    board = np.zeros((board_rows, board_cols))
