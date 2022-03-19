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
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def _set_xy(self, xy):
        self.x, self.y = xy

    def _get_xy(self):
        return [self.x, self.y]

    xy = property(_get_xy, _set_xy)


class Player:
    def __init__(self, layout: ControllerLayout, weapon):

        self.input_keys = layout
        self.weapon = weapon

        self.image = load_image("resources/images/player/topdowngigachad.png") if layout.name == "WASD" else load_image("resources/images/rroyalguard.bmp")  # python trolling
        self.rect = self.image.get_rect()

        self.position = Position(20, 20)
        self.velocity = 100
        self.rotation_velocity = 500
        self.angle = 90  # Measured in degrees

    def update(self, screen):
        rotated_image = rotate(self.image, self.angle-90)
        self.draw_weapon(screen)
        screen.blit(rotated_image, self.position.xy)

    def draw_weapon(self, screen):
        self.weapon.draw(screen, self.position, self.angle)

    def handle_movement(self, grid):  # grid for collision detection
        keys = get_keys_pressed()

        radians = math.radians(self.angle)
        dx = self.velocity * math.cos(radians) / FPS
        dy = self.velocity * math.sin(radians) / FPS

        if keys[self.input_keys.value[0]]:  # Handles UP / W

            prev_pos = Position(self.position.x - dx, self.position.y + dy)
            self.position.x += dx
            self.position.y -= dy
            if grid.is_collision(self):
                self.position = prev_pos
            
        if keys[self.input_keys.value[1]]:  # Handles LEFT / a
            self.angle += self.rotation_velocity / FPS

        if keys[self.input_keys.value[2]]:  # Handles DOWN / s

            prev_pos = Position(self.position.x + dx, self.position.y - dy)
            self.position.x -= dx
            self.position.y += dy
            if grid.is_collision(self):
                self.position = prev_pos

        if keys[self.input_keys.value[3]]:  # Handles RIGHT / d
            self.angle -= self.rotation_velocity / FPS

        self.rect.x, self.rect.y = self.position.xy  # updating player rect coords

    def handle_action(self, event):
        if event.type == KEYDOWN:
            if event.key == self.input_keys.value[4]:
                self.weapon.attack(self.position, self.angle, self.input_keys)
