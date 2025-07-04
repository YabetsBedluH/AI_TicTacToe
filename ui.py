import pygame
import math
from pygame import gfxdraw

from config import (
    screen, width, height, button_area, board_rows, board_cols, square_size,
    circle_radius, circle_width, cross_width, line_width, win_line_width,
    button_radius, button_center, LIGHT_GRAY, DARK_GRAY, GRID_COLOR,
    WHITE, GREEN, RED, BLUE, YELLOW, BG_COLOR,
    load_fonts
)
from game_state import board, get_winning_line, check_win, is_board_full, reset_board

# Load fonts from config
title_font, status_font, button_font = load_fonts()

def draw_lines(color=GRID_COLOR):
    for i in range(1, board_rows):
        pygame.draw.line(screen, color, 
                        (0, button_area + square_size * i), 
                        (width, button_area + square_size * i), 
                        line_width)
        pygame.draw.line(screen, color, 
                        (square_size * i, button_area), 
                        (square_size * i, button_area + square_size * board_rows), 
                        line_width)

def draw_figures(color=WHITE, highlight=None):
    for row in range(board_rows):
        for col in range(board_cols):
            center_x = int(col * square_size + square_size // 2)
            center_y = int(row * square_size + square_size // 2 + button_area)

            if highlight and highlight == (row, col) and board[row][col] == 0:
                s = pygame.Surface((square_size - 10, square_size - 10), pygame.SRCALPHA)
                s.fill((*color, 20))
                screen.blit(s, (col * square_size + 5, row * square_size + 5 + button_area))

            if board[row][col] == 1:  # Circle
                gfxdraw.aacircle(screen, center_x, center_y, circle_radius, color)
                gfxdraw.filled_circle(screen, center_x, center_y, circle_radius, (*color, 50))
                gfxdraw.aacircle(screen, center_x, center_y, circle_radius - circle_width // 2, color)
            elif board[row][col] == 2:  # Cross
                offset = square_size // 3
                gfxdraw.line(screen, 
                            center_x - offset, center_y - offset,
                            center_x + offset, center_y + offset, 
                            color)
                gfxdraw.line(screen, 
                            center_x - offset, center_y + offset,
                            center_x + offset, center_y - offset, 
                            color)

def draw_refresh_icon(center, radius, color, thickness=3, angle=0):
    arc_rect = pygame.Rect(center[0] - radius + 2, center[1] - radius + 2, 
                          2 * (radius - 2), 2 * (radius - 2))
    start_angle = math.radians(40 + angle)
    end_angle = math.radians(320 + angle)

    points = []
    steps = 30
    for i in range(steps + 1):
        a = start_angle + (end_angle - start_angle) * i / steps
        x = center[0] + (radius - 2) * math.cos(a)
        y = center[1] + (radius - 2) * math.sin(a)
        points.append((x, y))

    if len(points) > 1:
        pygame.draw.aalines(screen, color, False, points, thickness)

    arrow_angle = end_angle
    arrow_length = radius * 0.7
    tip = (
        int(center[0] + arrow_length * math.cos(arrow_angle)),
        int(center[1] + arrow_length * math.sin(arrow_angle))
    )
    left = (
        int(tip[0] - 10 * math.cos(arrow_angle - math.pi / 8)),
        int(tip[1] - 10 * math.sin(arrow_angle - math.pi / 8))
    )
    right = (
        int(tip[0] - 10 * math.cos(arrow_angle + math.pi / 8)),
        int(tip[1] - 10 * math.sin(arrow_angle + math.pi / 8))
    )

    pygame.draw.polygon(screen, color, [tip, left, right])

def draw_refresh_button(anim_progress=0):
    scale = 1 + 0.2 * anim_progress
    anim_radius = int(button_radius * scale)

    for i in range(anim_radius, 0, -2):
        alpha = 100 - int(80 * i / anim_radius)
        color = (*LIGHT_GRAY, alpha)
        s = pygame.Surface((i * 2, i * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (i, i), i)
        screen.blit(s, (button_center[0] - i, button_center[1] - i))

    angle = anim_progress * 360
    draw_refresh_icon(button_center, button_radius - 6, DARK_GRAY, thickness=4, angle=angle)

    return pygame.Rect(button_center[0] - anim_radius, button_center[1] - anim_radius,
                       anim_radius * 2, anim_radius * 2)

def draw_status_text(player, game_over, winner_line, winner_color):
    if game_over:
        if winner_line:
            text = "You Win!" if winner_color == GREEN else "AI Wins!"
        else:
            text = "Game Tied!"
        text_surface = status_font.render(text, True, winner_color)
    else:
        turn_text = "Your Turn (X)" if player == 1 else "AI Thinking..."
        text_surface = status_font.render(turn_text, True, WHITE)

    text_rect = text_surface.get_rect(center=(width // 2, button_area // 2))
    screen.blit(text_surface, text_rect)

def draw_title():
    title_text = "AI Tic-Tac-Toe"
    title_surface = title_font.render(title_text, True, YELLOW)
    title_rect = title_surface.get_rect(center=(width // 2, 15))
    screen.blit(title_surface, title_rect)

def restart_game():
    screen.fill(BG_COLOR)
    draw_lines()
    reset_board()
