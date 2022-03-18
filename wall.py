import pygame
from pygame.sprite import Sprite
import config

class Wall(Sprite):

    def __init__(self, game):
        super().__init__()

        self.screen = game.screen
        self.color = (0, 0, 0)

        self.game = game

        self.rect = pygame.Rect(0, 0, 0, 0)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)