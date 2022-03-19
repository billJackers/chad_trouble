from pygame.transform import rotate
from pygame.image import load as load_image
from player import Position, ControllerLayout
from game import ChadTrouble
import math


class Weapon:
    def __init__(self, damage: int, sprite):
        self.damage = damage
        self.image = sprite

    def draw(self, screen, position, angle):
        rotated_image = rotate(self.image, angle-45)

        to_radian = math.radians(angle)
        dx = 10*math.cos(to_radian)
        dy = 10*math.sin(to_radian)

        screen.blit(rotated_image, (position.x + dx, position.y - dy))

    def attack(self, player_position: Position, player_angle: float, input_type: ControllerLayout):  # player position is a Position() from player.py
        print("override to implement an attack")


class Sword(Weapon):
    def __init__(self):
        super().__init__(10, load_image("resources/images/swords/broadsword.png"))


class Arrow:
    def __init__(self, initial_position, initial_angle, input_type):
        self.velocity = 1000
        self.angle = initial_angle
        self.alive = True

        self.image = load_image("resources/images/blue_arrow.bmp") if input_type == ControllerLayout.WASD else load_image("resources/images/red_arrow.bmp")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = initial_position.xy

    def update(self):
        radians = math.radians(self.angle)
        if self.alive:
            self.rect.x += self.velocity * math.cos(radians) / config.FPS
            self.rect.y -= self.velocity * math.sin(radians) / config.FPS

    def draw(self, screen):
        print("drawing")
        rotated_image = pygame.transform.rotate(self.image, self.angle-90)
        screen.blit(rotated_image, (self.rect.x, self.rect.y))


class Bow(Weapon):
    def __init__(self):
        super().__init__(15, load_image("resources/images/bow.png"))

    def attack(self, player_position, player_angle, input_type):
        arrow = Arrow(player_position, player_angle, input_type)
        ChadTrouble.PROJECTILES.append(arrow)



