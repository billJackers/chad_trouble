from pygame.transform import rotate
import math

class Sword:
    def __init__(self, damage: int, sprite):
        self.damage = damage
        self.image = sprite

    def draw(self, screen, position, angle):
        rotated_image = rotate(self.image, angle-45)

        to_radian = math.radians(angle)
        dx = 10*math.cos(to_radian)
        dy = 10*math.sin(to_radian)

        screen.blit(rotated_image, (position.x + dx, position.y - dy))


