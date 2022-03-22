import pygame.font

class Displays:

    def __init__(self, game):
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

    def display_health_bars(self):
        # Player one
        player_one_label = self.font.render("Chad", True, self.text_color)
        player_one_label_rect = player_one_label.get_rect()
        player_one_label_rect.left = self.screen_rect.left + 20
        player_one_label_rect.bottom = self.screen_rect.bottom - 40
        self.screen.blit(player_one_label, player_one_label_rect)

        player_one_health_bar_width = 50 * self.game.player_one.health / 100
        player_one_health_bar_rect = pygame.Rect(20, self.screen_rect.bottom-30, player_one_health_bar_width, 10)
        pygame.draw.rect(self.screen, (0, 200, 50), player_one_health_bar_rect)

        # Displays the hp
        # player_one_health_bar_number = self.game.player_one.health
        # new_font = pygame.font.SysFont(None, 10)
        # self.image_1 = self.font.render(str(player_one_health_bar_number), True, self.text_color)
        # self.image_1_rect = self.image_1.get_rect()
        # self.image_1_rect.left = 10
        # self.image_1_rect.bottom = self.screen_rect.bottom-30
        # self.screen.blit(self.image_1, self.image_1_rect)

        # Player two
        player_two_label = self.font.render("Nerd", True, self.text_color)
        player_two_label_rect = player_two_label.get_rect()
        player_two_label_rect.right = self.screen_rect.right - 30
        player_two_label_rect.bottom = self.screen_rect.bottom - 40
        self.screen.blit(player_two_label, player_two_label_rect)

        player_two_health_bar_width = 50 * self.game.player_two.health / 100
        player_two_health_bar_rect = pygame.Rect(self.screen_rect.right - 60, self.screen_rect.bottom-30, player_two_health_bar_width, 10)
        pygame.draw.rect(self.screen, (0, 200, 50), player_two_health_bar_rect)