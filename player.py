import pygame
from pygame.image import load as load_image
from pygame.transform import rotate
from pygame.sprite import Sprite
from pygame import draw
from config import FPS
from pygame.key import get_pressed as get_keys_pressed
from pygame.constants import K_UP, K_DOWN, K_RIGHT, K_LEFT, K_w, K_a, K_s, K_d
from enum import Enum

import weapons

import math

RED = (255, 0, 0)
BLUE = (0, 0, 255)
# s

class ControllerLayout(Enum):  # for different keyboard movements
    WASD = [K_w, K_a, K_s, K_d]
    ARROW = [K_UP, K_LEFT, K_DOWN, K_RIGHT]


class Position:  # to handle x and y stuff more easily
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def xy(self):
        return [self.x, self.y]


class Player(Sprite):
    def __init__(self, layout: ControllerLayout):
        super().__init__()

        self.input_keys = layout
        self.weapon = weapons.Sword(10, load_image("resources/images/swords/broadsword.bmp"))

        self.color = BLUE if layout.name == "WASD" else RED

        self.image = pygame.image.load("resources/images/broyalguard.bmp")
        if self.color == RED:
            self.image = pygame.image.load("resources/images/rroyalguard.bmp")
        self.rect = self.image.get_rect()
        self.position = Position(50, 50)
        self.velocity = 500
        self.rotation_velocity = 500
        self.angle = 90 # Measured in degrees

        self.moving_forward = False
        self.moving_backward = False

    def update(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle-90)
        self.weapon.draw(screen, self.position, self.angle)
        screen.blit(rotated_image, (self.position.x, self.position.y))

    def handle_movement(self):
        keys = get_keys_pressed()

        radians = math.radians(self.angle)

        if keys[self.input_keys.value[0]]:  # Handles UP / W
            self.moving_forward = True
            self.position.x += self.velocity * math.cos(radians) / FPS
            self.position.y -= self.velocity * math.sin(radians) / FPS
            
        if keys[self.input_keys.value[1]]:  # Handles LEFT / a
            self.angle += self.rotation_velocity / FPS

        if keys[self.input_keys.value[2]]:  # Handles DOWN / s
            self.moving_backward = True
            self.position.x -= self.velocity * math.cos(radians) / FPS
            self.position.y += self.velocity * math.sin(radians) / FPS

        if keys[self.input_keys.value[3]]:  # Handles RIGHT / d
            self.angle -= self.rotation_velocity / FPS

        self.rect.x = self.position.x
        self.rect.y = self.position.y