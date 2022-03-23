from pygame.transform import rotate
from pygame.sprite import Sprite
from pygame.mask import from_surface as get_mask
from pygame.image import load as load_image
from player import Position, ControllerLayout
from pygame.draw import rect as draw_rect
import config
import math
import time
import random


class Weapon(Sprite):
    """Parent class for all weapons"""
    def __init__(self, damage: int, sprite):
        super().__init__()
        self.damage = damage
        self.image = sprite

    def draw(self, screen, position, angle):
        rotated_image = rotate(self.image, angle-45)

        to_radian = math.radians(angle)
        dx = 10*math.cos(to_radian)
        dy = 10*math.sin(to_radian)

        screen.blit(rotated_image, (position.x + dx, position.y - dy))

    def attack(self, player_position: Position, player_angle: float, input_type: ControllerLayout):  # player position is a Position() from player.py
        """Attempts to deal damage to another player"""
        print("override to implement an attack")


class Sword(Weapon):
    def __init__(self):
        self.image = load_image("resources/images/swords/broadsword.png")
        super().__init__(10, self.image)
        self.swinging = False
        self.swing_speed = 1
        self.angle_increment = 0

        self.attack_start_time = 0

    def attack(self, player_position, player_angle, input_type):
        """Sword swings 90 degrees in front of player"""
        # TODO
        return

class Arrow(Sprite):
    def __init__(self, initial_position, initial_angle, input_type):
        super().__init__()

        self.velocity = 1000
        self.angle = initial_angle
        self.alive = True

        self.damage = 20

        self.input_type = input_type

        self.image = load_image("resources/images/blue_arrow.bmp") if input_type == ControllerLayout.WASD else load_image("resources/images/red_arrow.bmp")
        self.mask = get_mask(self.image)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = initial_position.xy

        self.inactive_start_time = 0

    def update(self):
        radians = math.radians(self.angle)
        if self.alive:
            self.rect.x += self.velocity * math.cos(radians) / config.FPS
            self.rect.y -= self.velocity * math.sin(radians) / config.FPS
        elif time.time() - self.inactive_start_time >= 5:
            del self

    def draw(self, screen):
        rotated_image = rotate(self.image, self.angle-90)
        #  draw_rect(screen, (255, 0, 0), self.rect)  <--- to see arrow rect bounds
        screen.blit(rotated_image, (self.rect.x, self.rect.y))

    def __del__(self):
        return

class Bow(Weapon):
    def __init__(self, game):
        super().__init__(15, load_image("resources/images/bow.png"))
        self.game = game
        self.num_arrows = int(random.uniform(2, 5))

        print(str(self.num_arrows) + " arrows")

    def attack(self, player_position, player_angle, input_type):
        """Fire arrow"""
        if self.num_arrows > 0:
            arrow = Arrow(player_position, player_angle, input_type)
            self.game.arrows.add(arrow)

        self.num_arrows -= 1