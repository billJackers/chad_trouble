import pygame
from pygame.image import load as load_image
from pygame.transform import rotate
from pygame.sprite import Sprite
from pygame import draw
from config import FPS
from pygame.key import get_pressed as get_keys_pressed
from pygame.constants import KEYDOWN, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_p, K_w, K_a, K_s, K_d, K_f
from enum import Enum
import math

RED = (255, 0, 0)
BLUE = (0, 0, 255)


class ControllerLayout(Enum):  # for different keyboard movements
    WASD = [K_w, K_a, K_s, K_d, K_f]
    ARROW = [K_UP, K_LEFT, K_DOWN, K_RIGHT, K_p]


class Position:  # to handle x and y stuff more easily
    """Stores info about an object's position"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def _set_xy(self, xy):
        self.x, self.y = xy

    def _get_xy(self):
        return [self.x, self.y]

    xy = property(_get_xy, _set_xy)


class Player(Sprite):
    """A class to manage player movements, attacks, etc"""
    def __init__(self, layout: ControllerLayout, weapon):
        super().__init__()
        
        # PLAYER LOADOUT
        self.input_keys = layout
        self.weapon = weapon

        self.health = 100

        # PLAYER IMAGE
        self.image = load_image("resources/images/player/topdowngigachad.png") if layout.name == "WASD" else load_image("resources/images/rroyalguard.bmp")  # python trolling
        self.rect = self.image.get_rect()

        # MOVEMENT VARIABLES
        self.position = Position(20, 20)
        self.velocity = 1
        self.rotation_velocity = 400
        self.angle = 90  # Measured in degrees

    def update(self, screen):
        # DRAW PLAYER AND WEAPON
        if self.weapon.weapon_type == "Sword":
            self.weapon.update_swing(self.position, self.angle, self.input_keys)

        rotated_image = rotate(self.image, self.angle-90)
        self.weapon.draw(screen, self.position, self.angle)
        screen.blit(rotated_image, self.position.xy)

    def handle_movement(self, grid):  # grid for collision detection
        # KEYS PRESSED
        keys = get_keys_pressed()

        # POTENTIAL CHANGE IN POSITION
        radians = math.radians(self.angle)
        dx = self.velocity * math.cos(radians) #/ FPS
        dy = self.velocity * math.sin(radians) #/ FPS

        # INPUT CHECKS
        if keys[self.input_keys.value[0]]:  # Handles UP / W
            prev_pos = Position(self.position.x - dx, self.position.y + dy)
            self.position.x += dx
            self.position.y -= dy
            if grid.is_collision(self):
                self.position = prev_pos

        if keys[self.input_keys.value[2]]:  # Handles DOWN / s
            prev_pos = Position(self.position.x + dx, self.position.y - dy)
            self.position.x -= dx
            self.position.y += dy
            if grid.is_collision(self):
                self.position = prev_pos

        self.angle += (self.rotation_velocity / FPS) * (bool(keys[self.input_keys.value[1]]) - bool(keys[self.input_keys.value[3]]))
        self.rect.x, self.rect.y = self.position.xy  # updating player rect coords

    def set_position(self, x, y):
        self.position.xy = x, y
        self.rect.x, self.rect.y = x, y

    def handle_action(self, event):
        if event.type == KEYDOWN:
            if event.key == self.input_keys.value[4]:
                self.weapon.attack(self.position, self.angle, self.input_keys)
