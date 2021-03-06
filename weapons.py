from pygame.transform import rotate
from pygame.sprite import Sprite, spritecollide
from pygame.mask import from_surface as get_mask
from pygame.image import load as load_image
from player import Position, ControllerLayout
from pygame.draw import rect as draw_rect
from threading import Thread
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
        self.drawable = True

    def draw(self, screen, position, angle):
        if not self.drawable:
            return
        rotated_image = rotate(self.image, angle-45)

        to_radian = math.radians(angle)
        dx = 10*math.cos(to_radian)
        dy = 10*math.sin(to_radian)

        screen.blit(rotated_image, (position.x + dx, position.y - dy))

    def attack(self, player_position: Position, player_angle: float, input_type: ControllerLayout):  # player position is a Position() from player.py
        """Attempts to deal damage to another player"""
        print("override to implement an attack")


class Sword(Weapon):
    def __init__(self, game):
        self.game = game
        self.image = load_image("resources/images/swords/broadsword.png")
        super().__init__(50, self.image)
        self.weapon_type = "Sword"
        self.rect = self.image.get_rect()
        self.swinging = False
        self.damage = 1

    def attack(self, player_position, player_angle, input_type):
        if self.swinging:
            return
        if not self.drawable:
            return
        self.drawable = False
        # Creating a thread to handle our animation
        animation_thread = Thread(target=self.swing, args=(player_position, player_angle), daemon=True)
        animation_thread.start()

    def swing(self, player_position, player_angle):
        # do better stuff here
        hit = False
        tick = 0
        while not hit and tick < 75:
            time.sleep(0.001)
            tick += 1
            rotated_image = rotate(self.image, player_angle - 45)
            to_radian = math.radians(player_angle)
            dx = (10 + tick/2) * math.cos(to_radian)
            dy = (10 + tick/2) * math.sin(to_radian)
            self.game.screen.blit(rotated_image, (player_position.x + dx, player_position.y - dy))
            self.game.player_one.update(self.game.screen)
            self.game.player_two.update(self.game.screen)
            self.rect.x, self.rect.y = (player_position.x + dx, player_position.y - dy)
            self.swinging = True
        self.drawable = True
        self.swinging = False
        



class Arrow(Sprite):
    def __init__(self, initial_position, initial_angle, input_type):
        super().__init__()

        self.velocity = 1000
        self.angle = initial_angle
        self.alive = True

        self.damage = 50

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
        self.weapon_type = "Bow"

    def attack(self, player_position, player_angle, input_type):
        """Fire arrow"""
        arrow = Arrow(player_position, player_angle, input_type)
        self.game.arrows.add(arrow)