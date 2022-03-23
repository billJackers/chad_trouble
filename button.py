import pygame

class Button:
    """Button object"""

    def __init__(self, width, height, text, x, y, color, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.button_color = color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 40)
        self.rect = pygame.Rect(x, y, width, height)

        self.display_text(text)

    def display_text(self, text):
        """Turn text into image"""
        self.text_image = self.font.render(text, True, self.text_color, self.button_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw the button onto the screen"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.text_image, self.text_image_rect)