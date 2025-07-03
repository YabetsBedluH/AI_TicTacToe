# -------------------------------
# Import required Python modules
# -------------------------------
import sys                      # Provides access to system-specific parameters and functions
import pygame                   # Used for creating games and graphical programs
import numpy as np              # For efficient numerical operations and array handling
import math                     # For mathematical functions
import time                     # For time-related functions
from pygame import gfxdraw      # For antialiased drawing of shapes (better visual quality)

# ----------------------
# Initialize Pygame
# ----------------------
pygame.init()                   # Initializes all imported Pygame modules

# ----------------------
# Define color constants
# ----------------------
# These RGB color tuples are used for consistent and easy-to-read color references 
# throughout the visual interface or game

WHITE = (255, 255, 255)             # Basic white
LIGHT_GRAY = (220, 220, 220)        # Light gray for soft UI elements
DARK_GRAY = (50, 50, 50)            # Dark gray for contrasting backgrounds or text
RED = (255, 87, 87)                 # Vibrant red, good for highlighting errors or important elements
GREEN = (80, 200, 120)              # Soft green for success indicators or active states
BLUE = (80, 160, 220)               # Calm blue for general UI or selection
BLACK = (0, 0, 0)                   # Standard black
YELLOW = (255, 215, 0)              # Bright yellow for warnings or alerts
PURPLE = (150, 120, 220)            # Purple for decorative or alternative highlights

# Specialized theme colors for UI
BG_COLOR = (25, 25, 35)             # Dark background color for modern UI look
GRID_COLOR = (60, 60, 80)           # Color used for drawing grid lines or guides
HIGHLIGHT_COLOR = (100, 100, 120)   # Used to highlight selections or active cells


# Board and window dimensions

# The size (width and height) of the square game board area in pixels
board_size = 400

# Height in pixels reserved for the button area below the game board
button_area = 80

# Total width of the game window (equal to board size, since it's square)
width = board_size

# Total height of the game window, including space for the button
height = board_size + button_area

# Line width in pixels for the grid lines separating the squares
line_width = 4

# Number of rows and columns in the game board (3x3 grid for Tic-Tac-Toe)
board_rows = 3
board_cols = 3

# Size of each square (cell) on the board, assuming all squares are equal
square_size = board_size // board_cols

# Radius of the circle used to represent player 'O'
# Slightly smaller than 1/3 of a square to fit nicely
circle_radius = square_size // 3 - 5

# Thickness of the circle outline
circle_width = 10

# Thickness of the cross (X) lines
cross_width = 12

# Thickness of the winning line that highlights the win
win_line_width = 8


# Button properties
button_radius = 25
button_center = (width - 40, button_area // 2)  # Moved to top-right
button_animating = False
button_anim_start = 0
button_anim_duration = 0.3  # seconds

# Animation properties
animation_speed = 0.2  # seconds per animation
hover_radius = 5  # hover effect size

# Screen setup
screen = pygame.display.set_mode((width, height), pygame.SCALED)
pygame.display.set_caption('AI Tic Tac Toe')
screen.fill(BG_COLOR)

# Game board
board = np.zeros((board_rows, board_cols))

# Fonts
try:
    title_font = pygame.font.Font(None, 36)
    status_font = pygame.font.Font(None, 32)
    button_font = pygame.font.Font(None, 28)
except:
    title_font = pygame.font.SysFont('arial', 36)
    status_font = pygame.font.SysFont('arial', 32)
    button_font = pygame.font.SysFont('arial', 28)

def draw_lines(color=GRID_COLOR):
    # Draw grid lines with subtle glow
    for i in range(1, board_rows):
        pygame.draw.line(screen, color, 
                        (0, button_area + square_size * i), 
                        (width, button_area + square_size * i), 
                        line_width)
        pygame.draw.line(screen, color, 
                        (square_size * i, button_area), 
                        (square_size * i, button_area + board_size), 
                        line_width)

def draw_figures(color=WHITE, highlight=None):
    for row in range(board_rows):
        for col in range(board_cols):
            center_x = int(col * square_size + square_size // 2)
            center_y = int(row * square_size + square_size // 2 + button_area)

            # Draw hover effect
            if highlight and highlight == (row, col) and board[row][col] == 0:
                s = pygame.Surface((square_size-10, square_size-10), pygame.SRCALPHA)
                s.fill((*color, 20))
                screen.blit(s, (col*square_size+5, row*square_size+5+button_area))

            if board[row][col] == 1:  # O (circle)
                # Draw smooth anti-aliased circle
                gfxdraw.aacircle(screen, center_x, center_y, circle_radius, color)
                gfxdraw.filled_circle(screen, center_x, center_y, circle_radius, (*color, 50))
                gfxdraw.aacircle(screen, center_x, center_y, circle_radius - circle_width//2, color)

            elif board[row][col] == 2:  # X (cross)
                offset = square_size // 3
                # Draw smooth anti-aliased lines
                gfxdraw.line(screen, 
                            center_x - offset, center_y - offset,
                            center_x + offset, center_y + offset, 
                            color)
                gfxdraw.line(screen, 
                            center_x - offset, center_y + offset,
                            center_x + offset, center_y - offset, 
                            color)

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

def restart_game():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(board_rows):
        for col in range(board_cols):
            board[row][col] = 0

def draw_refresh_button(anim_progress=0):
    # anim_progress: 0 (normal) to 1 (fully animated)
    scale = 1 + 0.2 * anim_progress
    anim_radius = int(button_radius * scale)

    # Button background with gradient effect
    for i in range(anim_radius, 0, -2):
        alpha = 100 - int(80 * i / anim_radius)
        color = (*LIGHT_GRAY, alpha)
        s = pygame.Surface((i*2, i*2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (i, i), i)
        screen.blit(s, (button_center[0] - i, button_center[1] - i))

    # Draw refresh icon with animation rotation
    angle = anim_progress * 360
    draw_refresh_icon(button_center, button_radius - 6, DARK_GRAY, thickness=4, angle=angle)

    return pygame.Rect(button_center[0] - anim_radius, button_center[1] - anim_radius, 
                      anim_radius * 2, anim_radius * 2)

def draw_refresh_icon(center, radius, color, thickness=3, angle=0):
    # Draw a smooth refresh icon (arc + arrow)
    arc_rect = pygame.Rect(center[0] - radius + 2, center[1] - radius + 2, 
                          2 * (radius - 2), 2 * (radius - 2))
    start_angle = math.radians(40 + angle)
    end_angle = math.radians(320 + angle)

    # Draw anti-aliased arc
    points = []
    steps = 30
    for i in range(steps + 1):
        angle = start_angle + (end_angle - start_angle) * i / steps
        x = center[0] + (radius - 2) * math.cos(angle)
        y = center[1] + (radius - 2) * math.sin(angle)
        points.append((x, y))

    if len(points) > 1:
        pygame.draw.aalines(screen, color, False, points, thickness)

    # Arrowhead
    arrow_angle = end_angle
    arrow_length = radius * 0.7
    tip = (
        int(center[0] + arrow_length * math.cos(arrow_angle)),
        int(center[1] + arrow_length * math.sin(arrow_angle))
        )
    left = (
        int(tip[0] - 10 * math.cos(arrow_angle - math.pi / 8)),
        int(tip[1] - 10 * math.sin(arrow_angle - math.pi / 8)))
    right = (
        int(tip[0] - 10 * math.cos(arrow_angle + math.pi / 8)),
        int(tip[1] - 10 * math.sin(arrow_angle + math.pi / 8)))

    pygame.draw.polygon(screen, color, [tip, left, right])

def draw_status_text():
    if game_over:
        if winner_line:
            if winner_color == GREEN:
                text = "You Win!"
            else:
                text = "AI Wins!"
        else:
            text = "Game Tied!"
        text_surface = status_font.render(text, True, winner_color)
        text_rect = text_surface.get_rect(center=(width//2, button_area//2))
        screen.blit(text_surface, text_rect)
    else:
        turn_text = "Your Turn (X)" if player == 1 else "AI Thinking..."
        text_surface = status_font.render(turn_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(width//2, button_area//2))
        screen.blit(text_surface, text_rect)

def draw_title():
    title_text = "AI Tic-Tac-Toe"
    title_surface = title_font.render(title_text, True, YELLOW)
    title_rect = title_surface.get_rect(center=(width//2, 15))
    screen.blit(title_surface, title_rect)

# Initial setup
draw_lines()
player = 1  # Human is 1 (X), AI is 2 (O)
game_over = False
winner_line = None
winner_color = WHITE
hover_pos = None

# Animation state
button_animating = False
button_anim_start = 0

clock = pygame.time.Clock()

while True:
    current_time = time.time()
    anim_progress = 0
    if button_animating:
        elapsed = current_time - button_anim_start
        anim_progress = min(1, elapsed / button_anim_duration)
        if elapsed > button_anim_duration:
            button_animating = False

    # Get mouse position for hover effect
    mouse_pos = pygame.mouse.get_pos()
    hover_pos = None
    if not game_over and mouse_pos[1] >= button_area:
        mouseX = mouse_pos[0] // square_size
        mouseY = (mouse_pos[1] - button_area) // square_size
        if 0 <= mouseX < board_cols and 0 <= mouseY < board_rows and available_square(mouseY, mouseX):
            hover_pos = (mouseY, mouseX)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            button_rect = draw_refresh_button(anim_progress)

            if button_rect.collidepoint(mouse_pos):
                button_animating = True
                button_anim_start = current_time
                restart_game()
                game_over = False
                winner_line = None
                winner_color = WHITE
                player = 1
                continue  # Don't process as a board click

            if not game_over and player == 1:  # Only allow human move when it's their turn
                if mouse_pos[1] >= button_area:
                    mouseX = mouse_pos[0] // square_size
                    mouseY = (mouse_pos[1] - button_area) // square_size
                    if 0 <= mouseX < board_cols and 0 <= mouseY < board_rows:
                        if available_square(mouseY, mouseX):
                            mark_square(mouseY, mouseX, player)

                            if check_win(player):
                                winner_line = get_winning_line(player)
                                winner_color = GREEN
                                game_over = True
                            elif is_board_full():
                                winner_color = BLUE
                                game_over = True
                            else:
                                player = 2  # Switch to AI turn

                            # Redraw immediately to show human move
                            screen.fill(BG_COLOR)
                            draw_lines()
                            draw_figures(highlight=hover_pos)
                            draw_status_text()
                            draw_title()
                            button_rect = draw_refresh_button(anim_progress)
                            if winner_line:
                                pygame.draw.line(screen, winner_color, winner_line[0], winner_line[1], win_line_width)
                            pygame.display.flip()
import sys
import pygame
import numpy as np
import math
import time
from pygame import gfxdraw

pygame.init()

# Colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (50, 50, 50)
RED = (255, 87, 87)
GREEN = (80, 200, 120)
BLUE = (80, 160, 220)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
PURPLE = (150, 120, 220)
BG_COLOR = (25, 25, 35)
GRID_COLOR = (60, 60, 80)
HIGHLIGHT_COLOR = (100, 100, 120)

# Board and window dimensions
board_size = 400
button_area = 80  # Height reserved for the button
countdown_area = 30  # Extra space for countdown
width = board_size
height = board_size + button_area + countdown_area  # Added countdown area

line_width = 4
board_rows = 3
board_cols = 3
square_size = board_size // board_cols
circle_radius = square_size // 3 - 5
circle_width = 10
cross_width = 12
win_line_width = 8

# Button properties
button_radius = 25
button_center = (width - 40, button_area // 2)  # Moved to top-right
button_animating = False
button_anim_start = 0
button_anim_duration = 0.3  # seconds

# Animation properties
animation_speed = 0.2  # seconds per animation
hover_radius = 5  # hover effect size

# Screen setup
screen = pygame.display.set_mode((width, height), pygame.SCALED)
pygame.display.set_caption('AI Tic Tac Toe')
screen.fill(BG_COLOR)

# Game board
board = np.zeros((board_rows, board_cols))

# Fonts
try:
    title_font = pygame.font.Font(None, 36)
    status_font = pygame.font.Font(None, 32)
    button_font = pygame.font.Font(None, 28)
    countdown_font = pygame.font.Font(None, 24)
except:
    title_font = pygame.font.SysFont('arial', 36)
    status_font = pygame.font.SysFont('arial', 32)
    button_font = pygame.font.SysFont('arial', 28)
    countdown_font = pygame.font.SysFont('arial', 24)

def draw_lines(color=GRID_COLOR):
    # Draw grid lines with subtle glow
    for i in range(1, board_rows):
        pygame.draw.line(screen, color, 
                        (0, button_area + square_size * i), 
                        (width, button_area + square_size * i), 
                        line_width)
        pygame.draw.line(screen, color, 
                        (square_size * i, button_area), 
                        (square_size * i, button_area + board_size), 
                        line_width)

def draw_figures(color=WHITE, highlight=None):
    for row in range(board_rows):
        for col in range(board_cols):
            center_x = int(col * square_size + square_size // 2)
            center_y = int(row * square_size + square_size // 2 + button_area)

            # Draw hover effect
            if highlight and highlight == (row, col) and board[row][col] == 0:
                s = pygame.Surface((square_size-10, square_size-10), pygame.SRCALPHA)
                s.fill((*color, 20))
                screen.blit(s, (col*square_size+5, row*square_size+5+button_area))

            if board[row][col] == 1:  # O (circle)
                # Draw smooth anti-aliased circle
                gfxdraw.aacircle(screen, center_x, center_y, circle_radius, color)
                gfxdraw.filled_circle(screen, center_x, center_y, circle_radius, (*color, 50))
                gfxdraw.aacircle(screen, center_x, center_y, circle_radius - circle_width//2, color)

            elif board[row][col] == 2:  # X (cross)
                offset = square_size // 3
                # Draw smooth anti-aliased lines
                gfxdraw.line(screen, 
                            center_x - offset, center_y - offset,
                            center_x + offset, center_y + offset, 
                            color)
                gfxdraw.line(screen, 
                            center_x - offset, center_y + offset,
                            center_x + offset, center_y - offset, 
                            color)

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

def restart_game():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(board_rows):
        for col in range(board_cols):
            board[row][col] = 0

def draw_refresh_button(anim_progress=0):
    # anim_progress: 0 (normal) to 1 (fully animated)
    scale = 1 + 0.2 * anim_progress
    anim_radius = int(button_radius * scale)

    # Button background with gradient effect
    for i in range(anim_radius, 0, -2):
        alpha = 100 - int(80 * i / anim_radius)
        color = (*LIGHT_GRAY, alpha)
        s = pygame.Surface((i*2, i*2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (i, i), i)
        screen.blit(s, (button_center[0] - i, button_center[1] - i))

    # Draw refresh icon with animation rotation
    angle = anim_progress * 360
    draw_refresh_icon(button_center, button_radius - 6, DARK_GRAY, thickness=4, angle=angle)

    return pygame.Rect(button_center[0] - anim_radius, button_center[1] - anim_radius, 
                      anim_radius * 2, anim_radius * 2)



def draw_refresh_icon(center, radius, color, thickness=3, angle=0):
    # Draw a smooth refresh icon (arc + arrow)
    arc_rect = pygame.Rect(center[0] - radius + 2, center[1] - radius + 2, 
                          2 * (radius - 2), 2 * (radius - 2))
    start_angle = math.radians(40 + angle)
    end_angle = math.radians(320 + angle)

    # Draw anti-aliased arc
    points = []
    steps = 30
    for i in range(steps + 1):
        angle = start_angle + (end_angle - start_angle) * i / steps
        x = center[0] + (radius - 2) * math.cos(angle)
        y = center[1] + (radius - 2) * math.sin(angle)
        points.append((x, y))

    if len(points) > 1:
        pygame.draw.aalines(screen, color, False, points, thickness)

    # Arrowhead
    arrow_angle = end_angle
    arrow_length = radius * 0.7
    tip = (
        int(center[0] + arrow_length * math.cos(arrow_angle)),
        int(center[1] + arrow_length * math.sin(arrow_angle)))
    left = (
        int(tip[0] - 10 * math.cos(arrow_angle - math.pi / 8)),
        int(tip[1] - 10 * math.sin(arrow_angle - math.pi / 8)))
    right = (
        int(tip[0] - 10 * math.cos(arrow_angle + math.pi / 8)),
        int(tip[1] - 10 * math.sin(arrow_angle + math.pi / 8)))

    pygame.draw.polygon(screen, color, [tip, left, right])

def draw_status_text():
    if game_over:
        if winner_line:
            if winner_color == GREEN:
                text = "You Win!"
            else:
                text = "AI Wins!"
        else:
            text = "Game Tied!"
        text_surface = status_font.render(text, True, winner_color)
        text_rect = text_surface.get_rect(center=(width//2, button_area//2))
        screen.blit(text_surface, text_rect)
    else:
        turn_text = "Your Turn (X)" if player == 1 else "AI Thinking..."
        text_surface = status_font.render(turn_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(width//2, button_area//2))
        screen.blit(text_surface, text_rect)

def draw_countdown(seconds_left):
    countdown_text = f"New game in: {seconds_left}"
    countdown_surface = countdown_font.render(countdown_text, True, WHITE)
    countdown_rect = countdown_surface.get_rect(center=(width//2, height - countdown_area//2))
    screen.blit(countdown_surface, countdown_rect)

def draw_title():
    title_text = "AI Tic-Tac-Toe"
    title_surface = title_font.render(title_text, True, YELLOW)
    title_rect = title_surface.get_rect(center=(width//2, 15))
    screen.blit(title_surface, title_rect)

# Initial setup
draw_lines()
player = 1  # Human is 1 (X), AI is 2 (O)
game_over = False
winner_line = None
winner_color = WHITE
hover_pos = None
game_end_time = None  # Track when the game ended for auto-restart

# Animation state
button_animating = False
button_anim_start = 0

clock = pygame.time.Clock()

while True:
    current_time = time.time()
    anim_progress = 0
    if button_animating:
        elapsed = current_time - button_anim_start
        anim_progress = min(1, elapsed / button_anim_duration)
        if elapsed > button_anim_duration:
            button_animating = False

    # Check if game is over and countdown is active
    if game_over:
        if game_end_time is None:
            game_end_time = current_time
        else:
            time_left = 5 - (current_time - game_end_time)
            if time_left <= 0:
                restart_game()
                game_over = False
                winner_line = None
                winner_color = WHITE
                player = 1
                game_end_time = None

    # Get mouse position for hover effect


    if winner_line:
        pygame.draw.line(screen, winner_color, winner_line[0], winner_line[1], win_line_width)
    elif game_over and winner_color == BLUE:
        draw_lines(color=BLUE)

    # Draw countdown if game is over
    if game_over and game_end_time is not None:
        time_left = max(0, 5 - (current_time - game_end_time))
        draw_countdown(math.ceil(time_left))

    pygame.display.flip()
    clock.tick(60)
                         
                            # AI move
                            if not game_over and player == 2:
                                pygame.time.delay(300)  # Small delay for better UX
                                if best_move():
                                    if check_win(2):
                                        winner_line = get_winning_line(2)
                                        winner_color = RED
                                        game_over = True
                                    elif is_board_full():
                                        winner_color = BLUE
                                        game_over = True
                                    else:
                                        player = 1  # Switch back to human

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                winner_line = None
                winner_color = WHITE
                player = 1

    # Main drawing
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures(highlight=hover_pos)
    draw_status_text()
    draw_title()
    button_rect = draw_refresh_button(anim_progress)

    if winner_line:
        pygame.draw.line(screen, winner_color, winner_line[0], winner_line[1], win_line_width)
    elif game_over and winner_color == BLUE:
        draw_lines(color=BLUE)

    pygame.display.flip()
    clock.tick(60)
