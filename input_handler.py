import pygame
from ui import *
from config import *
from game_state import available_square, mark_square, check_win, is_board_full, get_winning_line

def handle_hover(game):
    mouse_pos = pygame.mouse.get_pos()
    hover_pos = None
    if not game.game_over and mouse_pos[1] >= button_area:
        mouseX = mouse_pos[0] // square_size
        mouseY = (mouse_pos[1] - button_area) // square_size
        if 0 <= mouseX < board_cols and 0 <= mouseY < board_rows and available_square(mouseY, mouseX):
            hover_pos = (mouseY, mouseX)
    return hover_pos

def handle_click(event_pos, anim_progress, current_time, game):
    # Check if clicked refresh button
    button_rect = draw_refresh_button(anim_progress)
    if button_rect.collidepoint(event_pos):
        return "restart"

    # Board click
    if not game.game_over and game.player == 1:
        if event_pos[1] >= button_area:
            mouseX = event_pos[0] // square_size
            mouseY = (event_pos[1] - button_area) // square_size
            if 0 <= mouseX < board_cols and 0 <= mouseY < board_rows:
                if game.make_move(mouseY, mouseX):
                    return "moved"
    return None

def handle_key(event, game):
    if event.key == pygame.K_r:
        return "restart"
    return None
