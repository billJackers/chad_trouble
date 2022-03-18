from pygame import draw
from config import FPS
from pygame.key import get_pressed as get_keys_pressed
from pygame.constants import K_UP, K_DOWN, K_RIGHT, K_LEFT, K_w, K_a, K_s, K_d
from enum import Enum

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
        self.input_keys = layout
        self.color = BLUE if layout.name == "WASD" else RED
        self.position = Position(50, 50)
        self.velocity = 500

    def update(self, screen):
        draw.circle(screen, self.color, self.position.xy(), 20)

    def handle_movement(self):
        keys = get_keys_pressed()
        if keys[self.input_keys.value[0]]:  # Handles UP / W
            self.position.y -= self.velocity / FPS
        if keys[self.input_keys.value[1]]:  # Handles LEFT / a
            self.position.x -= self.velocity / FPS
        if keys[self.input_keys.value[2]]:  # Handles DOWN / s
            self.position.y += self.velocity / FPS
        if keys[self.input_keys.value[3]]:  # Handles RIGHT / d
            self.position.x += self.velocity / FPS

