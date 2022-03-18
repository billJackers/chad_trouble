from pygame.image import load as load_image
from pygame.transform import rotate
from pygame import draw
from config import FPS
from pygame.key import get_pressed as get_keys_pressed
from pygame.constants import K_UP, K_DOWN, K_RIGHT, K_LEFT, K_w, K_a, K_s, K_d
from enum import Enum
import weapons
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

    def xy(self):
        return [self.x, self.y]


class Player:
    def __init__(self, layout: ControllerLayout):
        self.weapon = weapons.Sword(10, load_image("resources/images/swords/broadsword.png"))
        self.input_keys = layout

        self.image = load_image("resources/images/broyalguard.bmp") if layout.name == "WASD" else load_image("resources/images/rroyalguard.bmp")  # python trolling

        self.position = Position(50, 50)
        self.velocity = 500
        self.rotation_velocity = 500
        self.angle = 90 # Measured in degrees


    def update(self, screen):
        rotated_image = rotate(self.image, self.angle-90)
        self.draw_weapon(screen)
        screen.blit(rotated_image, self.position.xy())

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

        if keys[self.input_keys.value[2]]:  # Handles DOWN / s
            self.position.x -= self.velocity * math.cos(radians) / FPS
            self.position.y += self.velocity * math.sin(radians) / FPS

        if keys[self.input_keys.value[3]]:  # Handles RIGHT / d
            self.angle -= self.rotation_velocity / FPS