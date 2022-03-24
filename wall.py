from pygame.sprite import Sprite, Group, spritecollide
from player import Position, Player
from pygame import Rect
from pygame.draw import rect as draw_rect
from pygame.draw import line
from pygame import Surface
import config
from random import randint


class Wall(Sprite):
    """A class that manages walls to block players and weapons"""

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
    """A maze of walls"""
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid = []  # a representation of our grid
        self.walls = Group()  # storing the walls

    def randomize_spawns(self, players: Group):
        for player in players:
            rand_x = ((config.WIDTH / self.cols) * randint(0, self.cols - 1)) + (config.WIDTH / self.cols) / 2 - 20
            rand_y = ((config.HEIGHT / self.rows) * randint(0, self.rows - 1)) + (config.HEIGHT / self.rows) / 2 - 20
            player.set_position(rand_x, rand_y)

    def generate_path(self, player_group: Group):  # not yet done
        path = Group()
        players = player_group.sprites()

        dx = config.WIDTH / self.cols
        dy = config.HEIGHT / self.rows

        points = []
        cur_point = players[0].position

        bias = 0.7

    def load_walls(self):
        wall_x = int(config.WIDTH / self.cols)
        wall_y = int(config.HEIGHT / self.rows)

        # PLAYER BORDERS
        top_wall = Wall(Position(0, 0), config.WIDTH, Wall.HORIZONTAL)  # Top wall
        bottom_wall = Wall(Position(0, config.HEIGHT - config.WALL_WIDTH), config.WIDTH, Wall.HORIZONTAL)  # Bottom wall
        left_wall = Wall(Position(0, 0), config.HEIGHT, Wall.VERTICAL)  # Left wall
        right_wall = Wall(Position(config.WIDTH - config.WALL_WIDTH, 0), config.HEIGHT, Wall.VERTICAL)  # Right wall
        self.walls.add(bottom_wall)
        self.walls.add(top_wall)
        self.walls.add(left_wall)
        self.walls.add(right_wall)

        for i in range(self.rows):
            for j in range(self.cols):
                if randint(0, 3) == 1:  # horizonal walls
                    wall = Wall(Position(j * wall_x, i * wall_y), wall_x, Wall.HORIZONTAL)
                    self.walls.add(wall)

                if randint(0, 3) == 1:  # vertical walls
                    wall = Wall(Position(j * wall_x, i * wall_y), wall_y, Wall.VERTICAL)
                    self.walls.add(wall)


    def create(self, players: Group):
        """Generate the maze"""
        self.load_walls()
        self.randomize_spawns(players)
        self.generate_path(players)

    def draw(self, screen):
        for wall in self.walls:
            wall.draw(screen)

    def is_collision(self, player: Player):
        """Detect player-wall collisions"""
        prev_rect = player.rect
        player.rect.x, player.rect.y = player.position.xy
        dummy_square = dummySquare(player, player.rect.width * 0.6, player.rect.height * 0.6)
        collision = spritecollide(dummy_square, self.walls, False, False)
        player.rect = prev_rect
        return collision

class dummySquare(Sprite):
    def __init__(self, player, length, width):
        super().__init__()
        self.rect = Rect(0, 0, length, width)
        self.rect.center = player.rect.center