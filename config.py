import pygame

# --------------------------
# Color Constants
# --------------------------
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (50, 50, 50)
RED = (255, 87, 87)
GREEN = (80, 200, 120)
BLUE = (80, 160, 220)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
PURPLE = (150, 120, 220)

# Theme Colors
BG_COLOR = (25, 25, 35)
GRID_COLOR = (60, 60, 80)
HIGHLIGHT_COLOR = (100, 100, 120)

# --------------------------
# Game Dimensions
# --------------------------
board_size = 400
button_area = 80
width = board_size
height = board_size + button_area

line_width = 4
board_rows = 3
board_cols = 3
square_size = board_size // board_cols

circle_radius = square_size // 3 - 5
circle_width = 10
cross_width = 12
win_line_width = 8

# --------------------------
# Button Settings
# --------------------------
button_radius = 25
button_center = (width - 40, button_area // 2)
button_anim_duration = 0.3
hover_radius = 5

# --------------------------
# Animation
# --------------------------
animation_speed = 0.2

# --------------------------
# Font Loader
# --------------------------
def load_fonts():
    try:
        title_font = pygame.font.Font(None, 36)
        status_font = pygame.font.Font(None, 32)
        button_font = pygame.font.Font(None, 28)
    except:
        title_font = pygame.font.SysFont('arial', 36)
        status_font = pygame.font.SysFont('arial', 32)
        button_font = pygame.font.SysFont('arial', 28)
    return title_font, status_font, button_font

# --------------------------
# Pygame Screen Setup
# --------------------------
pygame.init()
screen = pygame.display.set_mode((width, height), pygame.SCALED)
pygame.display.set_caption('AI Tic Tac Toe')
screen.fill(BG_COLOR)
