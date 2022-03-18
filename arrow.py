import pygame
from pygame.sprite import Sprite

import config
import player

import math

class Arrow(Sprite):

    def __init__(self, sprite):
        super().__init__()
        self.velocity = 700
        self.angle = sprite.angle

        self.active = True

        self.image = pygame.image.load("resources/images/blue_arrow.bmp")
        if sprite.input_keys.name == "ARROW":
            self.image = pygame.image.load("resources/images/red_arrow.bmp")

        self.rect = self.image.get_rect()
        self.rect.x = sprite.position.x
        self.rect.y = sprite.position.y

    def update(self, screen):
        radians = math.radians(self.angle)

        if self.active:
            self.rect.x += self.velocity * math.cos(radians) / config.FPS
            self.rect.y -= self.velocity * math.sin(radians) / config.FPS

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle-90)
        screen.blit(rotated_image, (self.rect.x, self.rect.y))

    def set_inactive(self):
        self.active = False