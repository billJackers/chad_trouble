from pygame.sprite import Sprite, Group
from player import Position, Player
from pygame import Rect
from pygame.draw import rect as draw_rect
from pygame import Surface
import config
from random import randint


class Wall(Sprite):

    VERTICAL = 0
    HORIZONTAL = 1

    def __init__(self, position: Position, length: int, type: int):  # type is vertical (0) or horizonal (1)
        super().__init__()
        width, height = (config.WALL_WIDTH, length) if type == Wall.VERTICAL else (length, config.WALL_WIDTH)
        self.image = Surface((width, height))
        self.rect = Rect(*position.xy, width, height)

    def draw(self, screen):
        draw_rect(screen, config.WALL_COLOR, self.rect)


class Grid:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.walls = Group()  # our grid is 1D

    def create(self):

        wall_x = int(config.WIDTH / self.cols)
        wall_y = int(config.HEIGHT / self.rows)

        for i in range(self.rows):
            for j in range(self.cols):
                if randint(0, 1) == 1:  # horizonal walls
                    wall = Wall(Position(j*wall_x, i*wall_y), wall_x, Wall.HORIZONTAL)
                    self.walls.add(wall)

                if randint(0, 1) == 1:  # vertical walls
                    wall = Wall(Position(j*wall_x, i*wall_y), wall_y, Wall.VERTICAL)
                    self.walls.add(wall)

    def draw(self, screen):
        for wall in self.walls:
            wall.draw(screen)

    def is_collision(self, player: Player):
        for wall in self.walls:
            if wall.rect.colliderect(player.rect):
                if wall.rect.left < player.rect.right:
                    return 1 # Collides from the left
                if wall.rect.right > player.rect.left:
                    return 2 # Collides from the right
                if wall.rect.top > player.rect.bottom:
                    return 3 # Collides from the top
                if wall.rect.bottom < player.rect.top:
                    return 4 # Collides from the bottom
        return 0