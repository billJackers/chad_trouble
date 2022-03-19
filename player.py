from pygame.image import load as load_image
from pygame.transform import rotate
from pygame.sprite import Sprite
from pygame import draw

import weapons
from config import FPS
from pygame.key import get_pressed as get_keys_pressed
from pygame.constants import K_UP, K_DOWN, K_RIGHT, K_LEFT, K_w, K_a, K_s, K_d
from enum import Enum

import math

RED = (255, 0, 0)
BLUE = (0, 0, 255)


class ControllerLayout(Enum):  # for different keyboard movements
    WASD = [K_w, K_a, K_s, K_d]
    ARROW = [K_UP, K_LEFT, K_DOWN, K_RIGHT]


class Position:  # to handle x and y stuff more easily
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def _set_xy(self, xy):
        self.x, self.y = xy
    def _get_xy(self):
        return [self.x, self.y]
    xy = property(_get_xy, _set_xy)


class Player(Sprite):
    def __init__(self, layout: ControllerLayout, game):
        super().__init__()

        self.game = game

        self.input_keys = layout
        self.weapon = weapons.Sword(10, load_image("resources/images/swords/broadsword.png"))

        self.image = load_image("resources/images/player/topdowngigachad.png") if layout.name == "WASD" else load_image("resources/images/rroyalguard.bmp")  # python trolling
        self.rect = self.image.get_rect()

        self.position = Position(50, 50)
        self.velocity = 500
        self.rotation_velocity = 400
        self.angle = 90  # Measured in degrees

        self.moving_forward = False
        self.moving_backward = False

    def update(self, screen):
        rotated_image = rotate(self.image, self.angle-90)
        self.draw_weapon(screen)
        screen.blit(rotated_image, self.position.xy)

    def draw_weapon(self, screen):
        self.weapon.draw(screen, self.position, self.angle)

    def handle_movement(self):
        keys = get_keys_pressed()

        radians = math.radians(self.angle)

        if keys[self.input_keys.value[0]]:  # Handles UP / W
            self.position.x += self.velocity * math.cos(radians) / FPS
            self.position.y -= self.velocity * math.sin(radians) / FPS
            
        if keys[self.input_keys.value[1]]:  # Handles LEFT / a
            self.angle += self.rotation_velocity / FPS
            if self.angle > 360:
                self.angle -= 360

        if keys[self.input_keys.value[2]]:  # Handles DOWN / s
            self.position.x -= self.velocity * math.cos(radians) / FPS
            self.position.y += self.velocity * math.sin(radians) / FPS

        if keys[self.input_keys.value[3]]:  # Handles RIGHT / d
            self.angle -= self.rotation_velocity / FPS
            if self.angle < 0:
                self.angle += 360

        self.rect.x = self.position.x
        self.rect.y = self.position.y