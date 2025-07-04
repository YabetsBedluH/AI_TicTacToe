import pygame
import sys
import time
from config import *
from ui import *
from game import Game
from input_handler import handle_hover, handle_click, handle_key

pygame.init()
title_font, status_font, button_font = load_fonts()
draw_lines()

game = Game()
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

    hover_pos = handle_hover(game)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            result = handle_click(event.pos, anim_progress, current_time, game)
            if result == "restart":
                button_animating = True
                button_anim_start = current_time
                game.reset()
            elif result == "moved":
                # Human moved, redraw will happen below
                # Now AI moves
                game.ai_move()

        if event.type == pygame.KEYDOWN:
            result = handle_key(event, game)
            if result == "restart":
                game.reset()

    # Draw everything
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures(highlight=hover_pos)
    draw_status_text(game.player, game.game_over, game.winner_line, game.winner_color)
    draw_title()
    draw_refresh_button(anim_progress)

    if game.winner_line:
        pygame.draw.line(screen, game.winner_color, game.winner_line[0], game.winner_line[1], win_line_width)
    elif game.game_over and game.winner_color == BLUE:
        draw_lines(color=BLUE)

    pygame.display.flip()
    clock.tick(60)
