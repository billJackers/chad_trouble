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

        # First build a box so players can't go outside of the window
        for x in range(self.cols):
            top_wall = Wall(Position(x*wall_x, 0), wall_x, Wall.HORIZONTAL) # Top
            self.walls.add(top_wall)
            bottom_wall = Wall(Position(x*wall_x, config.HEIGHT-config.WALL_WIDTH), wall_x, Wall.HORIZONTAL)
            self.walls.add(bottom_wall)

        for y in range(self.rows):
            left_wall = Wall(Position(0, y*wall_y), wall_y, Wall.VERTICAL) # Left
            self.walls.add(left_wall)
            right_wall = Wall(Position(config.WIDTH, y*wall_y), wall_y, Wall.VERTICAL)
            self.walls.add(right_wall)

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
        collisions = [False, False, False, False]
        for wall in self.walls:
            if wall.rect.colliderect(player.rect):
                if wall.rect.collidepoint((player.rect.right, player.rect.centery)):
                    collisions[0] = True # Collides from the left
                if wall.rect.collidepoint((player.rect.left, player.rect.centery)):
                    collisions[1] = True # Collides from the right
                if wall.rect.collidepoint((player.rect.centerx, player.rect.bottom)):
                    collisions[2] = True # Collides from the top
                if wall.rect.collidepoint((player.rect.centerx, player.rect.top)):
                    collisions[3] = True # Collides from the bottom
        return collisions