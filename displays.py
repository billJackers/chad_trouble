import pygame
import pygame.font
from weapons import Arrow

class Displays:
    """A class to manage displayed info, such as health bars"""

    def __init__(self, game):
        """Initialize attributes"""        
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 20)

        self.player_one_health = 100
        self.player_two_health = 100

        self.display_health_bars()

    def update_displays(self):
        self.display_health_bars()
        self.display_arrows_left()
        self.display_num_wins()

    def display_health_bars(self):
        """Draw health bars"""
        # Player one
        player_one_label = self.font.render("PLAYER 1", True, self.text_color)
        player_one_label_rect = player_one_label.get_rect()
        player_one_label_rect.left = self.screen_rect.left + 20
        player_one_label_rect.bottom = self.screen_rect.bottom - 40
        self.screen.blit(player_one_label, player_one_label_rect)

        player_one_health_bar_width = 100 * self.game.player_one.health / 100
        player_one_health_bar_rect = pygame.Rect(20, self.screen_rect.bottom-30, player_one_health_bar_width, 20)
        pygame.draw.rect(self.screen, (0, 200, 50), player_one_health_bar_rect)

        # Player two
        player_two_label = self.font.render("PLAYER 2", True, self.text_color)
        player_two_label_rect = player_two_label.get_rect()
        player_two_label_rect.right = self.screen_rect.right - 30
        player_two_label_rect.bottom = self.screen_rect.bottom - 40
        self.screen.blit(player_two_label, player_two_label_rect)

        player_two_health_bar_width = 100 * self.game.player_two.health / 100
        player_two_health_bar_rect = pygame.Rect(self.screen_rect.right - 60, self.screen_rect.bottom-30, player_two_health_bar_width, 20)
        player_two_health_bar_rect.right = self.screen_rect.right-30
        pygame.draw.rect(self.screen, (0, 200, 50), player_two_health_bar_rect)

    def display_arrows_left(self):
        """Show how many arrows are left"""

        for arrow in range(self.game.player_one.num_arrows):
            arrow_image = pygame.image.load("resources/images/blue_arrow.bmp")
            self.screen.blit(arrow_image, (10 + (arrow * 10), self.screen_rect.bottom-85))

        for arrow in range(self.game.player_two.num_arrows):
            arrow_image = pygame.image.load("resources/images/red_arrow.bmp")
            self.screen.blit(arrow_image, (self.screen_rect.right - 45 - (arrow * 10), self.screen_rect.bottom-85))

    def display_num_wins(self):
        """Show the score"""

        new_font = pygame.font.SysFont(None, 50)

        player_one_wins = new_font.render(str(self.game.player_one_wins), True, (0, 0, 0))
        player_one_wins_rect = player_one_wins.get_rect()
        player_one_wins_rect.left = 100
        player_one_wins_rect.bottom = self.screen_rect.bottom - 30

        player_two_wins = new_font.render(str(self.game.player_two_wins), True, (0, 0, 0))
        player_two_wins_rect = player_two_wins.get_rect()
        player_two_wins_rect.right = self.screen_rect.right - 100
        player_two_wins_rect.bottom = self.screen_rect.bottom - 30

        self.screen.blit(player_one_wins, player_one_wins_rect)
        self.screen.blit(player_two_wins, player_two_wins_rect)