from config import *
from game_state import *
from ai import best_move

class Game:
    def __init__(self):
        self.player = 1  # Human = 1 (X), AI = 2 (O)
        self.game_over = False
        self.winner_line = None
        self.winner_color = WHITE

    def reset(self):
        restart_game()
        self.player = 1
        self.game_over = False
        self.winner_line = None
        self.winner_color = WHITE

    def make_move(self, row, col):
        if available_square(row, col) and not self.game_over:
            mark_square(row, col, self.player)
            self.update_game_status(self.player)
            return True
        return False

    def update_game_status(self, player):
        if check_win(player):
            self.winner_line = get_winning_line(player)
            self.winner_color = GREEN if player == 1 else RED
            self.game_over = True
        elif is_board_full():
            self.winner_color = BLUE
            self.game_over = True
        else:
            self.player = 2 if player == 1 else 1

    def ai_move(self):
        if not self.game_over and self.player == 2:
            pygame.time.delay(300)  # Small delay for UX
            if best_move():
                self.update_game_status(2)
